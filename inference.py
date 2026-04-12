import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "dummy")
SPACE_URL = os.getenv("SPACE_URL", "https://anshika032-ai-customer-support-agent.hf.space")

TASKS = ["handle-complaint", "handle-refund", "handle-inquiry"]
MAX_STEPS = 8

SYSTEM_PROMPT = """
You are an AI customer support agent.
Help users with their queries professionally and concisely.
Reply with a helpful response to the customer's message.
"""

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def get_response(message):
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            max_tokens=150,
        )
        return (completion.choices[0].message.content or "").strip()
    except Exception as e:
        return "I'm here to help. Could you please provide more details?"

def run_task(task_name):
    res = requests.post(f"{SPACE_URL}/reset")
    data = res.json()
    session_id = data.get("session_id", "default")
    observation = data.get("observation", "Hello! How can I help you?")
    rewards = []
    score = 0.0

    print(f"[START] task={task_name} env=ai-customer-support model={MODEL_NAME}", flush=True)

    for step in range(1, MAX_STEPS + 1):
        action = get_response(observation)

        step_res = requests.post(f"{SPACE_URL}/step", json={
            "action": action,
            "session_id": session_id
        }).json()

        reward = float(step_res.get("reward", 0.0))
        done = step_res.get("done", False)
        error = step_res.get("error", None)
        score = float(step_res.get("score", 0.0))
        observation = step_res.get("observation", "")
        rewards.append(reward)

        print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}", flush=True)

        if done:
            break

    success = score >= 0.1
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={len(rewards)} score={score:.2f} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    for task in TASKS:
        run_task(task)
