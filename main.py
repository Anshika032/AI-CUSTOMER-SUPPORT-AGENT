from env import SupportEnv
from llm_agent import choose_action
from rule_agent import rule_based_agent
from metrics import Metrics

import time


def run_agent(agent_type="llm", episodes=5):

    env = SupportEnv()
    metrics = Metrics()

    print("\n==============================")
    print(f"🚀 RUNNING {agent_type.upper()} AGENT")
    print("==============================\n")

    for ep in range(episodes):

        state = env.reset()

        print("\n----------------------------------")
        print(f"📌 EPISODE {ep+1}")
        print("----------------------------------")

        print("👤 Customer:", state["message"])
        print(f"📊 Sentiment: {state['sentiment']} | Churn: {state['churn_risk']}")

        done = False
        total_reward = 0
        step_count = 0

        while not done:

            step_count += 1

            print("\n🔹 Step:", step_count)

            # SELECT AGENT
            if agent_type == "llm":
                action, reason = choose_action(state)
            else:
                action = rule_based_agent(state)
                reason = "Rule-based decision"

            # DISPLAY ACTION
            print("🤖 Action:", action)
            print("💡 Reason:", reason)

            # ENV STEP
            state, reward, done, _ = env.step(action)

            # DISPLAY RESPONSE
            print("👤 Customer:", state["message"])
            print("🎯 Reward:", reward)

            print(f"📊 Updated → Sentiment: {state['sentiment']} | Churn: {state['churn_risk']}")

            total_reward += reward
            metrics.update(reward, action, done)

            time.sleep(0.5)  # smooth output

        print("\n✅ Episode Finished")
        print(f"⭐ Total Reward: {total_reward}")
        print(f"🔁 Steps Taken: {step_count}")

        metrics.total_episodes += 1

    return metrics


def compare_agents():

    print("\n\n🔥 STARTING AGENT COMPARISON\n")

    llm_metrics = run_agent("llm", episodes=5)
    rule_metrics = run_agent("rule", episodes=5)

    print("\n==============================")
    print("📊 FINAL COMPARISON")
    print("==============================")

    print("\n🤖 LLM AGENT PERFORMANCE")
    llm_metrics.report()

    print("\n📏 RULE-BASED AGENT PERFORMANCE")
    rule_metrics.report()

    print("\n🏆 RESULT:")

    if llm_metrics.total_reward > rule_metrics.total_reward:
        print("✅ LLM Agent Outperforms Rule-Based Agent 🚀")
    else:
        print("⚠️ Rule-Based Agent Performing Better (Needs Tuning)")


if __name__ == "__main__":

    print("""
========================================
💡 CUSTOMER SUPPORT AI EVALUATION SYSTEM
========================================
1. Run LLM Agent
2. Run Rule-Based Agent
3. Compare Both
========================================
""")

    choice = input("Select option (1/2/3): ")

    if choice == "1":
        run_agent("llm", episodes=5)

    elif choice == "2":
        run_agent("rule", episodes=5)

    elif choice == "3":
        compare_agents()

    else:
        print("Invalid choice ❌")