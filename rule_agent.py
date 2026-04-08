def rule_based_agent(state):

    msg = state["message"].lower()

    if "password" in msg:
        return "RESET_PASSWORD"

    if "payment" in msg:
        return "ESCALATE_BILLING"

    if "crash" in msg:
        return "ESCALATE_TECH"

    if state["churn_risk"] > 0.7:
        return "OFFER_RETENTION_DISCOUNT"

    return "ESCALATE_TECH"