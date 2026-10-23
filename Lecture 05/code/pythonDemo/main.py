import json
import math
import os
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
model = "gpt-4o-mini"
website_workspace = Path("generated-sites").resolve()
chat_history = []
website_history = []

CHAT_SYSTEM_PROMPT = """You are a helpful AI assistant with access to external tools.

Follow these rules:
1. For arithmetic calculations, ALWAYS use the calculator tool.
2. Always use calculator tool for even trivial calculation
3. For current weather, ALWAYS use the currentWeather tool.
4. For currency conversion or exchange rates, ALWAYS use the convertCurrency tool.
5. You may call multiple tools when solving a multi-step request.
6. After receiving tool results, explain the answer naturally.
7. Never invent current weather or exchange-rate information."""

WEBSITE_SYSTEM_PROMPT = """You are an expert frontend website developer.

Your job is to create complete static websites using the available tools.

Follow these rules:
1. Create a separate directory for every website.
2. Create index.html.
3. Create style.css.
4. Create script.js when JavaScript is useful.
5. Build modern, beautiful and responsive websites.
6. Use only HTML, CSS and vanilla JavaScript.
7. Do not just return website code in your response. Actually create the files using tools.
8. After creating the website, list the project files.
9. Read important files again if needed and fix obvious problems.
10. Finish only when the complete website has been created."""


def calculate(operation, a, b):
    print("Calculator tool called")

    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by 0")
        return a / b
    if operation == "mod":
        if b == 0:
            raise ValueError("Cannot calculate mod by 0")
        return a % b
    if operation == "power":
        return math.pow(a, b)
    raise ValueError(f"Unsupported operation {operation}")


def current_weather(city):
    print("Weather tool called")
    api_key = os.environ.get("WEATHER_API_KEY", "").strip()
    if not api_key:
        return json.dumps({"error": "WEATHER_API_KEY is not set. Please set it in .env to use weather tool."})
    query = urlencode({"key": api_key, "q": city})
    req = Request(f"https://api.weatherapi.com/v1/current.json?{query}", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req) as response:
            return response.read().decode()
    except Exception as error:
        return json.dumps({"error": f"Failed to fetch weather: {error}"})


def get_exchange_rate(from_currency, to_currency):
    print("Currency Exchange tool called")
    # Frankfurter requires a User-Agent header to avoid HTTP 403 Forbidden
    url = f"https://api.frankfurter.dev/v2/rate/{quote(from_currency)}/{quote(to_currency)}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req) as response:
            return response.read().decode()
    except Exception:
        # Fallback to frankfurter.app latest endpoint
        try:
            fallback_url = f"https://api.frankfurter.app/latest?from={quote(from_currency)}&to={quote(to_currency)}"
            req_fallback = Request(fallback_url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req_fallback) as response:
                return response.read().decode()
        except Exception as error:
            return json.dumps({"error": f"Failed to fetch exchange rate: {error}"})


def safe_path(relative_path):
    resolved = (website_workspace / relative_path).resolve()
    if resolved != website_workspace and website_workspace not in resolved.parents:
        raise ValueError("Access outside generated-sites is not allowed")
    return resolved


def create_directory(path):
    try:
        safe_path(path).mkdir(parents=True, exist_ok=True)
        return f"Directory created successfully: {path}"
    except OSError as error:
        return f"Failed to create directory: {error}"


def write_file(path, content):
    try:
        file = safe_path(path)
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8")
        return f"File written successfully: {path}"
    except OSError as error:
        return f"Failed to write file: {error}"


def read_file(path):
    try:
        return safe_path(path).read_text(encoding="utf-8")
    except OSError as error:
        return f"Failed to read file: {error}"


def list_files(path):
    try:
        directory = safe_path(path)
        if not directory.exists():
            return f"Directory does not exist: {path}"
        return "\n".join(
            str(item.relative_to(website_workspace))
            for item in directory.rglob("*")
        )
    except OSError as error:
        return f"Failed to list files: {error}"


def tool(name, description, properties):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": list(properties),
            },
        },
    }


CHAT_TOOLS = [
    tool("calculate", "Performs arithmetic calculations. Supported operations: add, subtract, multiply, divide, mod, power.", {
        "operation": {"type": "string", "description": "Operation: add, subtract, multiply, divide, mod, power"},
        "a": {"type": "number", "description": "First number"},
        "b": {"type": "number", "description": "Second number"},
    }),
    tool("currentWeather", "Get the current weather of a city.", {
        "city": {"type": "string", "description": "Name of the city"},
    }),
    tool("getExchangeRate", "Gets the latest exchange rate between two currencies.", {
        "from": {"type": "string", "description": "Source currency code, for example USD"},
        "to": {"type": "string", "description": "Target currency code, for example INR"},
    }),
]

WEBSITE_TOOLS = [
    tool("createDirectory", "Creates a new directory inside the website workspace.", {
        "path": {"type": "string", "description": "Relative directory path, for example brewlab"},
    }),
    tool("writeFile", "Creates or overwrites a text file inside the website workspace. Use this to create HTML, CSS and JavaScript files.", {
        "path": {"type": "string", "description": "Relative file path, for example brewlab/index.html"},
        "content": {"type": "string", "description": "Complete content that should be written into the file"},
    }),
    tool("readFile", "Reads the contents of an existing file from the website workspace.", {
        "path": {"type": "string", "description": "Relative file path"},
    }),
    tool("listFiles", "Lists all files and directories inside a website project.", {
        "path": {"type": "string", "description": "Relative directory path, for example brewlab"},
    }),
]


def complete(system_prompt, history, tools, functions, message):
    history.append({"role": "user", "content": message})
    messages = [{"role": "system", "content": system_prompt}, *history]

    while True:
        response = client.chat.completions.create(model=model, messages=messages, tools=tools)
        reply = response.choices[0].message
        if not reply.tool_calls:
            history.append({"role": "assistant", "content": reply.content})
            return reply.content

        messages.append(reply)
        for call in reply.tool_calls:
            arguments = json.loads(call.function.arguments)
            try:
                result = functions[call.function.name](**arguments)
            except Exception as error:
                result = f"Error executing tool {call.function.name}: {error}"
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result if isinstance(result, str) else json.dumps(result),
            })


def chat(message):
    return complete(CHAT_SYSTEM_PROMPT, chat_history, CHAT_TOOLS, {
        "calculate": calculate,
        "currentWeather": current_weather,
        "getExchangeRate": lambda **arguments: get_exchange_rate(
            arguments["from"], arguments["to"]
        ),
    }, message)


def generate_website(message):
    website_workspace.mkdir(parents=True, exist_ok=True)
    return complete(WEBSITE_SYSTEM_PROMPT, website_history, WEBSITE_TOOLS, {
        "createDirectory": create_directory,
        "writeFile": write_file,
        "readFile": read_file,
        "listFiles": list_files,
    }, message)


if __name__ == "__main__":
    import sys

    if sys.flags.interactive:
        print("=" * 60)
        print("Lecture 05: Loaded in Interactive Mode (REPL)")
        print("Call functions directly:")
        print("  chat(\"What is 78965 * 34576?\")")
        print("  chat(\"Convert 50 USD to INR\")")
        print("  generate_website(\"Create a modern portfolio site\")")
        print("=" * 60)
    else:
        print("=" * 60)
        print("Lecture 05: AI Agent with Tool Calling")
        print("=" * 60)
        print("Select an option:")
        print("1: Chat Assistant (Tools: Calculator, Currency Exchange, Weather)")
        print("2: Website Generator Agent (Creates files in generated-sites/)")
        print("=" * 60)

        mode = input("Enter 1 or 2 (default is 1): ").strip()

    if mode == "2":
        prompt = input("Enter website prompt (e.g. 'Create a modern portfolio website for a developer'): ").strip()
        if not prompt:
            prompt = "Create a modern portfolio website for a developer named Alex."
        print(f"\n[Agent] Working on: {prompt}\n")
        result = generate_website(prompt)
        print("\n[Result]:\n", result)
        print(f"\n[Done] Check the output directory: {website_workspace}")
    else:
        print("\n--- Chat Assistant with Tools ---")
        print("Examples you can try:")
        print("  - What is 78965 * 34576?")
        print("  - I have 10,000 INR. How much USD will I get based on today's exchange rate?")
        print("Type 'exit' or press Ctrl+C to quit.\n")
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit"):
                    break
                print("\nThinking and executing tools...")
                answer = chat(user_input)
                print(f"\nAI: {answer}\n")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
