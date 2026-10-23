# Python ticket summarizer

This is the Python/FastAPI equivalent of the Spring Boot project. It exposes the
same `POST /api/summarize` endpoint, accepts a support ticket as raw text, and
returns a plain-text two-line summary.

## Run (Windows / PowerShell)

Requires Python 3.11 or newer.

```powershell
cd pythonDemo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

> **Note**: If you get a script execution policy error when activating the virtual environment, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

Set your real `OPENAI_API_KEY` in `.env`, then start the API in **Terminal 1**:

```powershell
uvicorn app.main:app --port 8080 --reload --reload-dir app
```

Test it in **Terminal 2** with:

```powershell
curl.exe -X POST http://localhost:8080/api/summarize `
  -H "Content-Type: text/plain" `
  --data "Customers cannot complete checkout because the payment page times out."
```

Or on a single line:

```powershell
curl.exe -X POST http://localhost:8080/api/summarize -H "Content-Type: text/plain" --data "Customers cannot complete checkout because the payment page times out."
```

## Testing

For development and tests, install `requirements-dev.txt` and run `pytest`. The
tests use a fake OpenAI client and do not make paid API calls:

```powershell
pip install -r requirements-dev.txt
pytest
```

