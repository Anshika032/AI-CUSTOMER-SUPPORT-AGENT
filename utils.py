def detect_sentiment(text):
    text = str(text).lower()

    if "frustrated" in text or "angry" in text:
        return "😡 Angry"
    elif "not working" in text:
        return "😐 Neutral"
    return "🙂 Calm"


def update_churn(churn, action):
    
    if action == "OFFER_RETENTION_DISCOUNT":
        return max(0, churn - 0.3)

    elif "ESCALATE" in action:
        return churn - 0.1

    return churn + 0.05