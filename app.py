import os
import streamlit as st
from typing import TypedDict, Annotated
from operator import add

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from langgraph.graph import StateGraph, START, END


# Load .env from the same folder as this Python file
env_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ".env"
)

load_dotenv(env_path)  # still works fine for local dev
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set.")
    st.stop()

# Initialize Groq model
llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    temperature=0,
    api_key=api_key
)


class CodeState(TypedDict):
    query: str
    context: str
    messages: Annotated[list, add]
    response: str


def analyze_code_context(query: str) -> str:
    return f"Analyzing the following code snippet:\n{query}"


@tool
def get_code_analysis_guidance(query: str) -> str:
    """Get guidance on how to analyze code properly."""
    return (
        "Focus on syntax errors, logic errors, performance, "
        "readability, and best practices."
    )


tools = [get_code_analysis_guidance]


agent = create_agent(
    model=llm,
    tools=tools
)


def create_prompt_node(state: CodeState) -> CodeState:

    query = state["query"]

    context = analyze_code_context(query)

    prompt = f"""
You are an expert Code Analysis Assistant.

Analyze the following code carefully.

Context:
{context}

Tasks:
- Analyze the code.
- Identify syntax errors.
- Identify logical errors.
- Identify runtime errors.
- Suggest performance improvements.
- Suggest readability improvements.
- Suggest best practices.
- Explain the problems clearly for a beginner.
- Provide corrected code when necessary.
- If the code is correct, explain why it is correct.

User Code:
{query}

Give a clear and structured answer.
"""

    return {
        **state,
        "context": context,
        "messages": [
            HumanMessage(content=prompt)
        ]
    }


def generate_response_node(state: CodeState) -> CodeState:

    response = agent.invoke(
        {
            "messages": state["messages"]
        }
    )

    if response and "messages" in response:

        bot_message = response["messages"][-1]
        response_text = bot_message.content

    else:

        response_text = str(response)

    return {
        **state,
        "response": response_text,
        "messages": state["messages"] + [
            AIMessage(content=response_text)
        ]
    }


def build_code_graph():

    graph = StateGraph(CodeState)

    graph.add_node(
        "create_prompt",
        create_prompt_node
    )

    graph.add_node(
        "generate_response",
        generate_response_node
    )

    graph.add_edge(
        START,
        "create_prompt"
    )

    graph.add_edge(
        "create_prompt",
        "generate_response"
    )

    graph.add_edge(
        "generate_response",
        END
    )

    return graph.compile()


code_workflow = build_code_graph()


st.set_page_config(
    page_title="Code Analysis Chatbot",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Code Analysis Chatbot")

st.write(
    "Paste your code and get an AI-powered code analysis."
)


if "conversation" not in st.session_state:
    st.session_state.conversation = []


user_code = st.text_area(
    "Paste your code snippet here:",
    height=300
)


if st.button("🔍 Analyze Code"):

    if not user_code.strip():

        st.warning("Please enter some code first.")

    else:

        try:

            with st.spinner("Analyzing code..."):

                initial_state = {
                    "query": user_code,
                    "context": "",
                    "messages": [],
                    "response": ""
                }

                result = code_workflow.invoke(
                    initial_state
                )

                bot_response_text = result.get(
                    "response",
                    "No response generated."
                )

                st.session_state.conversation.append(
                    {
                        "user": user_code,
                        "bot": bot_response_text
                    }
                )

            st.success("Code analysis completed!")

            st.subheader("Your Code")

            st.code(
                user_code,
                language="python"
            )

            st.subheader("🤖 Assistant Analysis")

            st.markdown(
                bot_response_text
            )

            with st.expander("Context Used"):

                st.text(
                    result.get(
                        "context",
                        "No context generated."
                    )
                )

        except Exception as e:

            st.error(
                f"Error during code analysis: {str(e)}"
            )


if st.session_state.conversation:

    st.divider()

    st.subheader("📜 Conversation History")

    for turn in st.session_state.conversation:

        st.markdown("### 👤 You")

        st.code(
            turn["user"],
            language="python"
        )

        st.markdown("### 🤖 Assistant")

        st.markdown(
            turn["bot"]
        )

        st.divider()