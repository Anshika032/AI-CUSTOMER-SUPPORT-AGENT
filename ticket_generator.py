import random

CUSTOMER_QUERIES = [
    "Your app crashes every time",
    "I can't use your service properly",
    "This is very frustrating, nothing works",
]

def generate_ticket():

    tickets = [
        {
            "id": 1,
            "messages": [
                "I forgot my password",
                "I really need access urgently"
            ],
            "intent": "password_reset",
            "difficulty": "easy",
            "requires_escalation": False,
            "churn_risk": 0.2
        },
        {
            "id": 2,
            "messages": [
                "Payment failed but money deducted",
                "This is unacceptable",
                "Fix this or I will stop using your service"
            ],
            "intent": "billing_issue",
            "difficulty": "medium",
            "requires_escalation": True,
            "churn_risk": 0.7
        },
        {
            "id": 3,
            "messages": [
                random.choice(CUSTOMER_QUERIES),
                "I am extremely frustrated",
                "I am thinking to uninstall"
            ],
            "intent": "technical_issue",
            "difficulty": "hard",
            "requires_escalation": True,
            "churn_risk": 0.9
        }
    ]

    return random.choice(tickets)