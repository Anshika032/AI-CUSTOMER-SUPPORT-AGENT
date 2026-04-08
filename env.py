from ticket_generator import generate_ticket
from simulator import simulate_customer
from reward import compute_reward
from utils import detect_sentiment, update_churn
import tools


class SupportEnv:

    def __init__(self):
        self.ticket = None
        self.step_count = 0
        self.history = []
        self.churn = 0
        self.done = False

    def reset(self):
        self.ticket = generate_ticket()
        self.step_count = 0
        self.history = []
        self.churn = self.ticket["churn_risk"]
        self.done = False

        return self._get_state(self.ticket["messages"][0])

    def _get_state(self, message):
        return {
            "message": message,
            "history": self.history,
            "churn_risk": round(self.churn, 2),
            "sentiment": detect_sentiment(message)
        }

    def step(self, action):

        self.step_count += 1
        self.history.append(action)

        # TOOL EXECUTION
        if action == "RESET_PASSWORD":
            tools.reset_password()

        elif action == "ESCALATE_TECH":
            tools.tech_support()

        elif action == "ESCALATE_BILLING":
            tools.billing_support()

        elif action == "OFFER_RETENTION_DISCOUNT":
            tools.offer_discount()

        # UPDATE CHURN
        self.churn = update_churn(self.churn, action)

        # CUSTOMER RESPONSE
        response = simulate_customer(self.ticket, self.step_count, action)

        # DONE CONDITION
        if "Thanks" in response or "stay" in response or self.step_count > 5:
            self.done = True

        reward = compute_reward(self.ticket, action, self.churn, self.done)

        return self._get_state(response), reward, self.done, {}