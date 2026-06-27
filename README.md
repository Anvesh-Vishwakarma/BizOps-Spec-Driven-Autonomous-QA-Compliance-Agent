# BizOps: Spec-Driven Autonomous QA & Compliance Agent

An autonomous, multi-agent AI workforce designed to ingest highly structured company software requirement documents, automatically generate `pytest` test cases, physically execute the code in an isolated E2B cloud sandbox, and verify the execution results against legal and compliance standards.

## 🚀 Features

- **Automated Specification Parsing**: Upload standard PDF or DOCX requirement documents and let the AI extract precise structured rules and logic.
- **Autonomous Test Generation**: Dynamically writes runnable Python `pytest` automation scripts for UI testing (via Playwright) or Data Pipelines (via Pandas).
- **Secure Sandbox Execution**: Uses [E2B](https://e2b.dev/) to instantly provision secure, isolated cloud sandboxes to run the generated code and capture the execution logs safely.
- **AI Compliance Auditing**: Automatically evaluates the execution stack traces and test logs against the original compliance rules using a custom Gemini-powered Auditor.
- **Interactive Agent UI**: Built with Chainlit to provide real-time visibility into the multi-agent reasoning process (Architect -> Coder -> Auditor).

## 🧠 Architecture & Tech Stack

This project utilizes a modern AI stack separated into a robust backend and an interactive frontend.

- **Orchestration:** [LangGraph](https://python.langchain.com/docs/langgraph) & [LangChain](https://python.langchain.com/)
- **LLM Engine:** [Google Gemini 1.5 Pro](https://deepmind.google/technologies/gemini/)
- **Frontend UI:** [Chainlit](https://docs.chainlit.io/)
- **Backend API:** [FastAPI](https://fastapi.tiangolo.com/)
- **Cloud Sandbox:** [E2B Code Interpreter](https://e2b.dev/)

### The Agent Workflow

1. 🏗️ **Architect Agent**: Parses the uploaded PDF/Word files to extract highly structured logic, constraints, and compliance rules.
2. 💻 **Coder Agent**: Takes the Architect's instructions and writes the `pytest` automation scripts.
3. ⚡ **Execution Engine (E2B)**: Takes the code, spins up an ephemeral cloud container, runs it, and captures stdout/stderr.
4. 🕵️ **Auditor Agent**: Evaluates the E2B execution logs against the legal standards, flagging security vulnerabilities and compliance gaps in a final Markdown report.

---

## 🛠️ Local Installation & Setup

### Prerequisites
- Python 3.10+
- An [E2B API Key](https://e2b.dev/docs/getting-started/api-key)
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/bizops-qa-agent.git
cd bizops-qa-agent
```

### 2. Set up the Environment Variables
Create a `.env` file in the root of the project and add your API keys:
```env
E2B_API_KEY="your_e2b_api_key_here"
GEMINI_API_KEY="your_gemini_api_key_here"
```

### 3. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 4. Run the Application
The application is split into a FastAPI backend and a Chainlit frontend. You must run both concurrently.

**Terminal 1 (Backend):**
```bash
uvicorn backend.main:app --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
chainlit run frontend/app.py -w --port 8501
```

Once both are running, open your browser to `http://localhost:8501` to use the application!

---

## ☁️ Deployment (Hugging Face Spaces)

This project includes a `Dockerfile` designed for easy, free deployment on [Hugging Face Spaces](https://huggingface.co/spaces).

1. Create a new Space on Hugging Face.
2. Choose **Docker** as the SDK and select the **Blank** template.
3. Upload all the project files (including the `Dockerfile`).
4. Go to your Space **Settings** -> **Variables and secrets**.
5. Add your `E2B_API_KEY` and `GEMINI_API_KEY` as Secrets.
6. The Space will automatically build the image and deploy both the backend and frontend simultaneously.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
