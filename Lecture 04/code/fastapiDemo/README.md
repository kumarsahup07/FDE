# Tomato Chat API (Lecture 04)

Customer support AI chatbot for the "Tomato" food ordering app using FastAPI and OpenAI Responses API.

## Run (Windows / PowerShell)

In your activated virtual environment:

```powershell
uvicorn app.main:app --port 8000 --reload
```

## Test Endpoints (in a second terminal)

### 1. Send a chat message:
```powershell
curl.exe -X POST http://localhost:8000/api/chat -H "Content-Type: text/plain" --data "Where is my order? It has been 45 minutes."
```

Or multi-line:
```powershell
curl.exe -X POST http://localhost:8000/api/chat `
  -H "Content-Type: text/plain" `
  --data "Where is my order? It has been 45 minutes."
```

### 2. Clear chat history:
```powershell
curl.exe -X DELETE http://localhost:8000/api
```

### 3. Interactive Swagger UI:
Open `http://localhost:8000/docs` in your browser.
