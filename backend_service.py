import random
import time

from ai_enhancer import detect_intent, detect_sentiment as detect_sentiment_ai
from llm_agent import choose_action
from rule_agent import rule_based_agent
from utils import detect_sentiment as detect_sentiment_state

RESPONSES = {
    "ESCALATE_TECH": [
        "Our engineering team is working on this.",
        "We’ve identified the issue and fixing it.",
        "This bug is being resolved urgently.",
    ],
    "ESCALATE_BILLING": [
        "Our billing team is reviewing this now.",
        "We’ve escalated this to finance for immediate follow-up.",
        "This billing issue is being handled as a priority.",
    ],
    "RESET_PASSWORD": [
        "I’ve sent a password reset link to your registered email.",
        "Please check your inbox for the reset link.",
        "Your password reset request has been processed.",
    ],
    "OFFER_RETENTION_DISCOUNT": [
        "We value your business and have applied a retention offer.",
        "I’ve added a special retention discount to your account.",
        "We’d like to keep you with us and have noted a loyalty offer.",
    ],
}

analytics = {
    "total_queries": 0,
    "resolved": 0,
    "escalated": 0,
    "response_times": [],
}


def get_reasoning(text):
    text = str(text).lower()
    if "payment" in text or "billing" in text or "invoice" in text or "refund" in text:
        return "Detected billing-related keywords"
    elif "crash" in text or "technical" in text or "bug" in text or "error" in text:
        return "Detected technical failure keywords"
    return "General issue detected"


def route_agent(action):
    if action == "ESCALATE_TECH":
        return "🛠 Tech Agent"
    elif action == "ESCALATE_BILLING":
        return "💳 Billing Agent"
    elif action == "RESET_PASSWORD":
        return "🔐 Account Agent"
    return "🎯 General Agent"


def route_issue(intent):
    intent_text = str(intent).lower()
    if "hardware" in intent_text:
        return "Hardware Team"
    elif "billing" in intent_text:
        return "Billing Team"
    else:
        return "Support Team"


def get_response(action):
    return random.choice(RESPONSES.get(action, ["We are checking this issue."]))


def calculate_reward(query, action):
    text = str(query).lower()

    if action == "RESET_PASSWORD":
        return 10

    if action == "ESCALATE_TECH":
        if any(word in text for word in ["crash", "error", "bug", "not working", "issue", "technical"]):
            return 8
        return 6

    if action == "ESCALATE_BILLING":
        if any(word in text for word in ["payment", "billing", "invoice", "refund", "charged", "deducted"]):
            return 7
        return 5

    if action == "OFFER_RETENTION_DISCOUNT":
        return 6

    return 2


def build_state(query):
    return {
        "message": query,
        "sentiment": detect_sentiment_state(query),
        "churn_risk": 0.5,
        "history": [],
    }


def decide_action(query, agent_type="LLM Agent"):
    state = build_state(query)

    if agent_type == "Rule-Based Agent":
        action = rule_based_agent(state)
        reason = "Rule-based decision"
    else:
        action, reason = choose_action(state)

    return action, reason, state


def process_query(query, agent_type="LLM Agent"):
    start_time = time.perf_counter()
    user_input = query
    intent = detect_intent(user_input)
    sentiment = detect_sentiment_ai(user_input)

    print("USER:", user_input)
    print("INTENT:", intent)
    print("SENTIMENT:", sentiment)

    action, reason, state = decide_action(query, agent_type)
    route = route_agent(action)
    department = route_issue(intent)
    response = get_response(action)
    reasoning = get_reasoning(query)
    reward = calculate_reward(query, action)

    if sentiment == "NEGATIVE":
        response += "\n⚠️ High priority detected"

    analytics["total_queries"] += 1
    if action.startswith("ESCALATE"):
        analytics["escalated"] += 1
    else:
        analytics["resolved"] += 1
    analytics["response_times"].append(time.perf_counter() - start_time)

    return {
        "query": query,
        "sentiment": state["sentiment"],
        "intent": intent,
        "ai_sentiment": sentiment,
        "ai_confidence": 0.0,
        "department": department,
        "action": action,
        "route": route,
        "response": response,
        "reason": reason,
        "reasoning": reasoning,
        "reward": reward,
    }
