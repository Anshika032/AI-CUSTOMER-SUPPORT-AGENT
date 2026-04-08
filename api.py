import os
import sqlite3
import threading
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from backend_service import analytics, process_query

app = FastAPI(title="Customer Support Agent API")
DB_PATH = os.path.join(os.path.dirname(__file__), "logs.db")
DB_LOCK = threading.Lock()
user_rewards = {}


class ProcessRequest(BaseModel):
    query: str
    agent_type: str = "LLM Agent"
    user_id: str = "guest"


class ChatRequest(BaseModel):
    user_input: str
    agent_type: str = "LLM Agent"
    user_id: str = "guest"


def add_reward(user_id, points):
    user_rewards[user_id] = user_rewards.get(user_id, 0) + points


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user TEXT,
                action TEXT,
                response TEXT,
                route TEXT,
                sentiment TEXT,
                reasoning TEXT
            )
            """
        )
        conn.commit()


def save_log(user, action, response, route, sentiment, reasoning):
    with DB_LOCK:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO logs (timestamp, user, action, response, route, sentiment, reasoning) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    datetime.utcnow().isoformat(timespec="seconds"),
                    user,
                    action,
                    response,
                    route,
                    sentiment,
                    reasoning,
                ),
            )
            conn.commit()


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/process")
def process(payload: ProcessRequest):
    result = process_query(payload.query, payload.agent_type)
    response_text = result["response"].lower()

    if "resolved" in response_text:
        add_reward(payload.user_id, 10)

    if "self fix" in response_text:
        add_reward(payload.user_id, 20)

    save_log(
        payload.query,
        result["action"],
        result["response"],
        result["route"],
        result["sentiment"],
        result["reasoning"],
    )
    return result


@app.post("/chat")
def chat(payload: ChatRequest):
    result = process_query(payload.user_input, payload.agent_type)
    response_text = result["response"].lower()

    if "resolved" in response_text:
        add_reward(payload.user_id, 10)

    if "self fix" in response_text:
        add_reward(payload.user_id, 20)

    save_log(
        payload.user_input,
        result["action"],
        result["response"],
        result["route"],
        result["sentiment"],
        result["reasoning"],
    )

    return {
        "response": result["response"],
        "intent": result.get("intent", "general query"),
        "sentiment": result.get("ai_sentiment", result.get("sentiment", "NEUTRAL")),
        "department": result.get("department", "Support Team"),
        "confidence": result.get("ai_confidence", 0.0),
        "action": result.get("action", "GENERAL"),
        "reward": result.get("reward", 0),
        "reasoning": result.get("reasoning", "General issue detected"),
    }


@app.get("/analytics")
def get_analytics():
    avg_time = sum(analytics["response_times"]) / max(len(analytics["response_times"]), 1)

    return {
        "total": analytics["total_queries"],
        "resolved": analytics["resolved"],
        "escalated": analytics["escalated"],
        "avg_time": avg_time,
    }


@app.get("/reward/{user_id}")
def get_reward(user_id: str):
    return {"points": user_rewards.get(user_id, 0)}
