import os
import subprocess
import sys
import time

import pandas as pd
import requests
import streamlit as st

sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv

load_dotenv()

try:
    from backend_service import get_reasoning, process_query
except Exception as e:
    import streamlit as st

    st.error(f"Import failed: {e}")
    raise


API_URL = "http://127.0.0.1:8000"

analytics = {
    "total_queries": 0,
    "resolved": 0,
    "escalated": 0,
    "response_times": [],
}


st.set_page_config(page_title="AI Support System", layout="wide")

st.markdown(
    """
<style>
    body {
        background: linear-gradient(135deg, #0f172a, #020617);
        color: #e2e8f0;
        font-family: Inter, "Segoe UI", sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a, #020617);
        color: #e2e8f0;
    }

    footer, #MainMenu {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 600;
    }

    p, span, div {
        color: #cbd5f5 !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
        padding-top: 0.5rem;
    }

    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMetric,
    [data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.9rem;
    }

    [data-testid="stSidebar"] .stSelectbox > div {
        background: rgba(30, 41, 59, 0.85);
        border-radius: 18px;
        padding: 0.25rem 0.15rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18);
    }

    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-size: 3.4rem;
        line-height: 1;
        color: #f8fafc;
        font-weight: 700;
    }

    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #cbd5e1;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .sidebar-card {
        background: rgba(30, 41, 59, 0.65);
        border-radius: 16px;
        padding: 1rem 1rem 0.85rem 1rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.24);
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    .hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        color: transparent;
        letter-spacing: -0.03em;
        margin: 0.35rem 0 0.2rem 0;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd5f5;
        margin-bottom: 1.1rem;
        font-weight: 600;
    }

    .status-strip {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 0.55rem 0.9rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.24);
        margin-bottom: 1rem;
    }

    .card {
        background: rgba(30, 41, 59, 0.6);
        padding: 20px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
    }

    .status {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 14px;
    }

    textarea {
        background: #020617 !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        color: white !important;
    }

    div[data-testid="stChatMessage"] {
        background: transparent;
        padding: 0.15rem 0;
    }

    div[data-testid="stChatMessage"] > div {
        border-radius: 18px;
        padding: 1rem 1.05rem;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
        border: 1px solid rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
        margin-bottom: 0.45rem;
    }

    div[data-testid="stChatMessage"] [data-testid="stAvatarIcon"] {
        background: #ff9f1c;
        color: #fff;
        border-radius: 14px;
    }

    .stChatInputContainer {
        background: rgba(30, 41, 59, 0.72);
        border-radius: 20px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 16px 30px rgba(15, 23, 42, 0.28);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border-radius: 999px;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: 700;
        box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24);
    }

    .stAlert {
        border-radius: 18px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def _api_is_live():
    try:
        response = requests.get(f"{API_URL}/health", timeout=1.5)
        return response.ok
    except requests.RequestException:
        return False


@st.cache_resource
def ensure_api_server():
    if _api_is_live():
        return True

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "api:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd=os.path.dirname(__file__),
    )

    for _ in range(30):
        if _api_is_live():
            return True
        time.sleep(1)

    return False


def call_backend(query, agent_type):
    payload = {"user_input": query, "agent_type": agent_type, "user_id": "guest"}

    try:
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=20)
        response.raise_for_status()
        return response.json(), True
    except requests.RequestException:
        return process_query(query, agent_type), False


def typing_effect(text):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(f"<div class='card'>{output}</div>", unsafe_allow_html=True)
        time.sleep(0.01)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "turns" not in st.session_state:
    st.session_state.turns = 0

if "reasoning" not in st.session_state:
    st.session_state.reasoning = "General issue detected"

if "backend_ready" not in st.session_state:
    st.session_state.backend_ready = False

if "reward_history" not in st.session_state:
    st.session_state.reward_history = []

if "scores" not in st.session_state:
    st.session_state.scores = [0]

if "action_history" not in st.session_state:
    st.session_state.action_history = []

if "latest_reward" not in st.session_state:
    st.session_state.latest_reward = 0

if not st.session_state.messages:
    st.session_state.messages = []

st.session_state.backend_ready = ensure_api_server()

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #0f172a);
        border-right: 1px solid #1e293b;
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_dashboard():
    st.title("🏠 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("⚡ Status", "Active")
    col2.metric("🎯 Score", st.session_state.get("score", 0))
    col3.metric("🔄 Turns", st.session_state.get("turns", 0))

    st.markdown("### 📨 Recent Activity")
    if st.session_state.messages:
        recent_role, recent_msg = st.session_state.messages[-1]
        if isinstance(recent_msg, dict):
            recent_text = recent_msg.get("response", "")
        else:
            recent_text = str(recent_msg)
        st.markdown(
            f"<p style='font-size:{font_size}px'>{recent_text}</p>",
            unsafe_allow_html=True,
        )
    else:
        st.info("No messages yet. Go to Chat.")


def show_chat():
    st.title("💬 AI Support Chat")

    user_input = st.chat_input("Type your issue...")

    if user_input:
        st.session_state.messages.append(("user", user_input))

        start = time.time()

        result, used_api = call_backend(user_input, agent_type)
        end = time.time()

        analytics["total_queries"] += 1
        analytics["response_times"].append(end - start)

        response_text = result.get("response", "")
        if "escalate" in response_text.lower():
            analytics["escalated"] += 1
        else:
            analytics["resolved"] += 1

        response = result.get("response", "I’m here to help with your support request.")
        intent = result.get("intent", "general query")
        sentiment = result.get("sentiment", result.get("ai_sentiment", "NEUTRAL"))
        department = result.get("department", "Support Team")

        st.session_state.latest_reward = result.get("reward", 0)
        st.session_state.reward_history.append(st.session_state.latest_reward)
        st.session_state.scores.append(st.session_state.latest_reward)
        st.session_state.action_history.append(result.get("action", "GENERAL"))
        st.session_state.score += 1 + st.session_state.latest_reward
        st.session_state.turns += 1
        st.session_state.reasoning = get_reasoning(user_input)

        st.session_state.messages.append(
            (
                "bot",
                {
                    "response": response,
                    "intent": intent,
                    "sentiment": sentiment,
                    "department": department,
                },
            )
        )

        if not used_api:
            st.info("Running in simulation mode.")

    for role, msg in st.session_state.messages:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(
                    f"<p style='font-size:{font_size}px'>{msg}</p>",
                    unsafe_allow_html=True,
                )
        else:
            with st.chat_message("assistant"):
                if isinstance(msg, dict):
                    st.markdown(
                        f"<p style='font-size:{font_size}px'>{msg.get('response', '')}</p>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f"""
                        <div style="font-size:{font_size}px">
                            <b>Intent:</b> {msg.get('intent', 'general query')}<br>
                            <b>Sentiment:</b> {msg.get('sentiment', 'NEUTRAL')}<br>
                            <b>Department:</b> {msg.get('department', 'Support Team')}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<p style='font-size:{font_size}px'>{msg}</p>",
                        unsafe_allow_html=True,
                    )


def show_analytics():
    st.title("📊 Analytics")
    st.line_chart(st.session_state.get("scores", [0]))


with st.sidebar:
    st.markdown("## 🚀 AI Support")

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "💬 Chat", "📊 Analytics"],
    )

    st.markdown("---")

    agent_type = st.selectbox("🤖 Agent", ["LLM Agent"])

    st.sidebar.markdown("### 🎨 UI Controls")
    font_size = st.sidebar.slider(
        "Adjust Chat Font Size",
        min_value=12,
        max_value=28,
        value=16,
    )

    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.success("🟢 System Active")


if page == "🏠 Dashboard":
    show_dashboard()
elif page == "💬 Chat":
    show_chat()
elif page == "📊 Analytics":
    show_analytics()