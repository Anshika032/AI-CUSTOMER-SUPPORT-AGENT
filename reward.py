def compute_reward(ticket, action, churn, done):

    reward = 0

    # correct resolution
    if ticket["intent"] == "password_reset" and action == "RESET_PASSWORD":
        reward += 10

    # correct escalation
    elif ticket["requires_escalation"] and "ESCALATE" in action:
        if action == "ESCALATE_TECH":
            reward += 8
        elif action == "ESCALATE_BILLING":
            reward += 7
        else:
            reward += 6

    # wrong escalation
    elif not ticket["requires_escalation"] and "ESCALATE" in action:
        reward -= 6

    # missed escalation
    elif ticket["requires_escalation"] and "ESCALATE" not in action:
        reward -= 10

    # retention bonus
    if churn < 0.3:
        reward += 5

    # churn penalty
    if churn > 0.8:
        reward -= 15

    # efficiency
    if done:
        reward += 5

    return reward