import asyncio
import os
from typing import List, Optional
from openai import OpenAI

from my_env_v4 import MyEnvV4Action, MyEnvV4Env

IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
TASK_NAME = os.getenv("TASK_NAME", "customer-support")
BENCHMARK = os.getenv("BENCHMARK", "my_env_v4")
MAX_STEPS = 8

SYSTEM_PROMPT = """
You are an AI customer support agent. 
Help users with their queries professionally and concisely.
Reply with a helpful response to the customer's message.
"""

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_response(client, message):
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
        print(f"[DEBUG] Error: {e}", flush=True)
        return "I'm here to help. Could you please provide more details?"

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = await MyEnvV4Env.from_docker_image(IMAGE_NAME)

    rewards = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset()
        
        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            message = get_response(client, str(result.observation))
            result = await env.step(MyEnvV4Action(message=message))

            reward = result.reward or 0.0
            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=message, reward=reward, done=result.done, error=None)

            if result.done:
                break

        score = sum(rewards) / (MAX_STEPS * 10) if rewards else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= 0.1

    finally:
        try:
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())
