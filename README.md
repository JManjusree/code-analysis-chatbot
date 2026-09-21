# 💻 Code Analysis Chatbot

An AI-powered code analysis assistant built with **Streamlit**, **LangChain**, **LangGraph**, and **Groq**. Paste any code snippet and get a structured breakdown of syntax errors, logic errors, runtime errors, performance issues, readability suggestions, and best practices — explained in beginner-friendly language, with corrected code where needed.

## Features

-  **Deep code analysis** — syntax, logic, and runtime error detection
- **Performance & readability suggestions**
-  **Best practices guidance** tailored for beginners
-  **Corrected code snippets** when issues are found
-  **Conversation history** — review past analyses in the same session
-  Powered by a **LangGraph** workflow (prompt construction → LLM analysis) running on **Groq's** `openai/gpt-oss-20b` model

##  Tech Stack

| Layer | Tool |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) |
| LLM Framework | [LangChain](https://www.langchain.com/) |
| LLM Provider | [Groq](https://groq.com/) (`openai/gpt-oss-20b`) |
| Config | `python-dotenv` |

##  Project Structure

```
code-analyzer/
├── app.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not committed)
└── README.md
```

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Get a free API key from [console.groq.com](https://console.groq.com/).

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

##  How It Works

1. **User Input** — You paste a code snippet into the text area and click **Analyze Code**.
2. **Prompt Construction** (`create_prompt_node`) — The app builds a detailed prompt asking the LLM to check for errors, performance issues, and best practices.
3. **Agent Execution** (`generate_response_node`) — A LangChain agent (backed by Groq's LLM) processes the prompt and returns a structured analysis.
4. **Display** — The analysis is rendered in the UI, along with the context used and a running conversation history.

The workflow is orchestrated as a simple two-node **LangGraph** state machine:

```
START → create_prompt → generate_response → END
```

##  Example Usage

1. Paste a Python snippet into the text box.
2. Click **🔍 Analyze Code**.
3. Review the structured breakdown: errors found, suggestions, and corrected code (if applicable).

## Notes

- Requires a valid `GROQ_API_KEY` — the app will stop with an error if it's missing.
- Currently supports single-turn code analysis per submission; history is kept only for the active session.
