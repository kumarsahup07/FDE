# Lecture 06: Streaming Sarcastic Chatbot (Python / FastAPI)

This lecture demonstrates **Streaming Responses (SSE / Chunk-by-Chunk Delivery)** using OpenAI's Responses API (`stream=True`).

## Quick Setup (Windows / PowerShell)

In your terminal:
```powershell
cd "Lecture 06\code\python"

# 1. Create and activate virtual environment
python -m venv myenv
.\myenv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt
```

---

## How to Run

### Option 1: Run in Terminal (CLI Streaming)
Run directly in the console to see tokens stream as they are generated:
```powershell
python app.py
```

### Option 2: Run with Web UI (`ChatBotFE`)
1. **Start the FastAPI Streaming Server**:
   ```powershell
   python server.py
   ```
   *(or `uvicorn server:app --port 8080 --reload`)*

2. **Open the Frontend**:
   Double click or open [Lecture 06/code/ChatBotFE/index.html](../ChatBotFE/index.html) in your browser.
   Type your message and watch the sarcastic chatbot stream responses in real-time!
