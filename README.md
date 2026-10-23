# Forward Deployed Engineer (FDE) — Python & FastAPI (Windows Edition)

This repository contains my personal notes, implementations, and solutions for the **Forward Deployed Engineer (FDE)** course, redefined and adapted with a focus on **Python & FastAPI**, specifically optimized for **Windows (PowerShell)** development.

---

## 🌟 Acknowledgements & Credits

Special thanks and full credit to the original creators and instructors:

- **Original Course Repository**: [Aditya Tandon / Forward-Deployed-Engineer-Full-Course](https://github.com/adityatandon15/Forward-Deployed-Engineer-Full-Course)
- **YouTube Channel**: [Coder Army](https://www.youtube.com/@CoderArmy9)
- **Full Course Playlist**: [Forward Deployed Engineer Playlist on YouTube](https://youtube.com/playlist?list=PLWSlr9idVBc0&si=cr72JaMeeG5fFgPG)

---

## 🚀 What Makes This Repository Different?

While the original course features multiple stacks (Spring Boot, Node.js, Python), this repository has been **redefined and enhanced by me** with:

1. **Python & FastAPI Focus**: Clean, modern Python implementations leveraging FastAPI and OpenAI's latest APIs.
2. **Tailored for Windows / PowerShell**:
   - Fixed Windows path and activation commands (`Activate.ps1` vs Linux `source`).
   - Adapted cURL commands for PowerShell using `curl.exe` with proper line-continuation backticks (`` ` ``) and single-line scripts.
   - Comprehensive Windows setup instructions and notes for every lecture.
3. **Bug Fixes & Improvements**:
   - Configured robust `.env` handling across nested directory structures.
   - Fixed external API blocking issues (such as `User-Agent` headers for Frankfurter currency API).
   - Added safe tool execution so tool errors don't crash the agent loop.
   - Integrated `.gitignore` protection to ensure API keys and `.env` files are never exposed.

---

## 📚 Lecture Breakdown

| Lecture | Topic | Highlights |
| :--- | :--- | :--- |
| **Lecture 01** | Course Overview & Architecture | Notes & conceptual foundation |
| **Lecture 02** | LLM Foundations & Prompting | Core LLM concepts |
| **Lecture 03** | Python Ticket Summarizer | FastAPI server consuming OpenAI Responses API (`POST /api/summarize`) |
| **Lecture 04** | Tomato Customer Support Chatbot | Stateful conversational chatbot with chat history & system prompts (`POST /api/chat`, `DELETE /api`) |
| **Lecture 05** | AI Agent with Tool Calling | Autonomous agent executing tools: Calculator, Currency Exchange, Weather, and a dynamic Website Generator (`generated-sites/`) |
| *Upcoming* | Advanced Agentic Workflows | More implementations as course progresses |

---

## 💻 Quick Start (Windows / PowerShell)

### 1. Clone the repository
```powershell
git clone https://github.com/kumarsahup07/FDE.git
cd FDE
```

### 2. Run any Python Lecture (e.g., Lecture 05)
```powershell
cd "Lecture 05\code\pythonDemo"

# Create and activate virtual environment
python -m venv myenv
.\myenv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env with your OpenAI API Key
# OPENAI_API_KEY="your_api_key_here"

# Run the project
python main.py
```

---

## 🔒 Security
All sensitive configuration files (`.env`), virtual environments (`myenv/`), and Python bytecode caches are automatically ignored via `.gitignore` to prevent secret leaks.
