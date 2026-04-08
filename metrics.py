class Metrics:

    def __init__(self):
        self.total_episodes = 0
        self.success = 0
        self.total_reward = 0
        self.escalations = 0

    def update(self, reward, action, done):
        self.total_reward += reward

        if "ESCALATE" in action:
            self.escalations += 1

        if done and reward > 0:
            self.success += 1

    def report(self):
        print("\n📊 FINAL METRICS")
        print("Episodes:", self.total_episodes)
        print("Success Rate:", self.success / self.total_episodes)
        print("Avg Reward:", self.total_reward / self.total_episodes)
        print("Escalations:", self.escalations)
        