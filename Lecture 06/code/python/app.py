from chat_controller import ChatController
from chat_service import ChatService


chat_service = ChatService()
chat_controller = ChatController(chat_service)


def chat(message):
    return chat_controller.chat(message)


if __name__ == "__main__":
    import asyncio

    async def main():
        print("=" * 60)
        print("Lecture 06: Sarcastic Chatbot with Streaming Output (CLI)")
        print("Type 'exit' or press Ctrl+C to quit")
        print("=" * 60)
        while True:
            try:
                msg = input("\nYou: ").strip()
                if not msg:
                    continue
                if msg.lower() in ("exit", "quit"):
                    break
                print("\nAI: ", end="", flush=True)
                async for chunk in chat(msg):
                    print(chunk, end="", flush=True)
                print()
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break

    asyncio.run(main())
