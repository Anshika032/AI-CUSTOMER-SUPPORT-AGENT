import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=_api_key) if _api_key else None
_api_disabled_reason = None

ACTIONS = [
    "RESET_PASSWORD",
    "ESCALATE_TECH",
    "ESCALATE_BILLING",
    "OFFER_RETENTION_DISCOUNT",
]


def llm_status():
    if _api_disabled_reason:
        return False, _api_disabled_reason
    if not _api_key:
        return False, "OPENAI_API_KEY is missing"
    return True, "LLM API available"


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _local_fallback_action(state):
    """Deterministic fallback used when the API is unavailable."""
    message = str(state.get("message", "")).lower()
    sentiment = str(state.get("sentiment", "")).lower()
    churn_risk = _safe_float(state.get("churn_risk", 0.0), 0.0)

    if ("angry" in sentiment or "frustrat" in sentiment) and churn_risk >= 0.7:
        return "OFFER_RETENTION_DISCOUNT", "Fallback: angry user with high churn risk"

    if any(k in message for k in ["password", "reset", "login", "sign in", "signin"]):
        return "RESET_PASSWORD", "Fallback: account access issue"

    if any(k in message for k in ["payment", "billing", "invoice", "refund", "charged"]):
        return "ESCALATE_BILLING", "Fallback: billing-related issue"

    if any(k in message for k in ["crash", "error", "bug", "not working", "doesn't work", "issue"]):
        return "ESCALATE_TECH", "Fallback: technical issue"

    if churn_risk >= 0.75:
        return "OFFER_RETENTION_DISCOUNT", "Fallback: high churn risk"

    return "ESCALATE_TECH", "Fallback: general support escalation"


def _parse_json_response(content):
    text = (content or "").strip()

    # Handle model responses wrapped in markdown fences.
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    return json.loads(text)


def _is_quota_error(exc):
    status_code = getattr(exc, "status_code", None)
    message = str(exc).lower()
    return status_code == 429 or "insufficient_quota" in message or "quota" in message


def _is_auth_error(exc):
    status_code = getattr(exc, "status_code", None)
    message = str(exc).lower()
    return status_code in (401, 403) or "invalid api key" in message or "authentication" in message


def _set_api_disabled(reason):
    global _api_disabled_reason
    if _api_disabled_reason is None:
        _api_disabled_reason = reason


def _build_prompt(state):
    history = state.get("history", [])
    history_text = " | ".join(history) if history else "(none)"

    return f"""
You are an intelligent Tier-1 customer support agent.

Goals:
- Solve simple issues
- Escalate only when required (costly)
- Reduce frustration
- Prevent churn

Rules:
- Angry + high churn → retain customer
- Simple issue → solve directly
- Avoid unnecessary escalation

Allowed actions:
{', '.join(ACTIONS)}

Customer message: {state.get('message', '')}
Sentiment: {state.get('sentiment', '')}
Churn Risk: {state.get('churn_risk', '')}
History: {history_text}

Return JSON ONLY:
{{"action": "<ACTION>", "reason": "<short reason>"}}
"""


def choose_action(state):
    api_ok, api_reason = llm_status()
    if not api_ok:
        action, reason = _local_fallback_action(state)
        return action, f"{reason} ({api_reason})"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": _build_prompt(state)},
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        parsed = _parse_json_response(content)

        action = parsed.get("action")
        reason = parsed.get("reason", "")

        if action not in ACTIONS:
            return _local_fallback_action(state)

        return action, reason

    except Exception as e:
        if _is_quota_error(e):
            _set_api_disabled("OpenAI quota exceeded")
            action, reason = _local_fallback_action(state)
            return action, f"{reason} (OpenAI quota exceeded)"

        if _is_auth_error(e):
            _set_api_disabled("OpenAI authentication failed")
            action, reason = _local_fallback_action(state)
            return action, f"{reason} (OpenAI authentication failed)"

        action, reason = _local_fallback_action(state)
        return action, f"{reason} (OpenAI API unavailable)"