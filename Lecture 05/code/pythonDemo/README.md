# Lecture 05: AI Agent with Tool Calling

This project demonstrates OpenAI function calling / tool calling in two forms:
1. **Chat Assistant with Tools**: Calculator, Currency Exchange (Frankfurter API), and Weather.
2. **Website Generator Agent**: Creates full HTML/CSS/JS websites by calling file-system tools (`createDirectory`, `writeFile`, `listFiles`, `readFile`) into `generated-sites/`.

## How to Run (Windows / PowerShell)

Ensure your virtual environment is active:
```powershell
.\myenv\Scripts\activate
```

### Option 1: Run Interactive Program (Recommended)
Simply run:
```powershell
python main.py
```
This lets you select:
- `1` for **Chat Assistant** (try queries like `"What is 78965 * 34576?"` or `"Convert 10000 INR to USD"`).
- `2` for **Website Generator** (e.g., `"Create a modern portfolio website for a developer"`).

### Option 2: Run in Python Interactive Mode
Drop straight into the Python REPL with:
```powershell
python -i main.py
```
Then call the functions directly:
```python
# Test Tool Calling with Calculator / Currency:
chat("What is 78965 * 34576?")
chat("I have 10,000 INR. How much USD will I get based on today's exchange rate?")

# Test Website Generation Agent:
generate_website("Create a modern portfolio website for a developer named Alex")
```
Files will be created inside the `generated-sites/` folder!
