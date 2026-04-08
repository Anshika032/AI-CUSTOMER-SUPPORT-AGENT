import random


TECH_RESPONSES = [
    "Our engineering team is investigating this issue.",
    "We’ve identified a possible bug and are working on a fix.",
    "This looks like a backend issue. Our team is resolving it.",
]

BILLING_RESPONSES = [
    "I understand your concern. I've escalated this billing issue to our finance team. You'll get an update within 24 hours.",
    "Thanks for reporting this. Our billing team is reviewing the deduction and will update you soon.",
    "We've escalated this to billing specialists and marked it as priority.",
]

PASSWORD_RESPONSES = [
    "I've sent a password reset link to your registered email. Please check your inbox.",
    "A secure password reset link has been sent. Let me know if it doesn't arrive in a minute.",
    "Password reset initiated. Please use the email link to regain access.",
]


def simulate_customer(ticket, step_count, action):

    if step_count >= len(ticket["messages"]):
        return "Thanks, issue resolved."

    base_msg = ticket["messages"][step_count]

    if action == "RESET_PASSWORD" and ticket["intent"] == "password_reset":
        return random.choice(PASSWORD_RESPONSES)

    if action == "ESCALATE_TECH" and ticket["intent"] == "technical_issue":
        return random.choice(TECH_RESPONSES)

    if action == "ESCALATE_BILLING" and ticket["intent"] == "billing_issue":
        return random.choice(BILLING_RESPONSES)

    if action == "OFFER_RETENTION_DISCOUNT":
        return "Okay I will stay."

    if action == "RESET_PASSWORD":
        return random.choice(PASSWORD_RESPONSES)

    if action == "ESCALATE_TECH":
        return random.choice(TECH_RESPONSES)

    if action == "ESCALATE_BILLING":
        return random.choice(BILLING_RESPONSES)

    return base_msg