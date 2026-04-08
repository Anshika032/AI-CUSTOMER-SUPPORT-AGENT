import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://router.huggingface.co/hf-inference/models/valhalla/distilbart-mnli-12-1"
SENTIMENT_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
LABELS = [
    "payment problem",
    "hardware problem",
    "software bug",
    "refund issue",
    "general question",
]

_last_intent_confidence = 0.0


def detect_intent(text):
    global _last_intent_confidence

    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": LABELS,
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
    result = response.json()
    print(result)

    # Fix: extract top label safely when API returns expected payload.
    if "labels" in result and result["labels"]:
        scores = result.get("scores", [0.0])
        _last_intent_confidence = float(scores[0]) if scores else 0.0
        return result["labels"][0]
    elif isinstance(result, list) and result and "label" in result[0]:
        _last_intent_confidence = float(result[0].get("score", 0.0))
        return result[0]["label"]
    else:
        print("ERROR:", result)
        _last_intent_confidence = 0.0
        return "general query"


def detect_sentiment(text):
    try:
        response = requests.post(
            SENTIMENT_URL,
            headers=headers,
            json={"inputs": text},
            timeout=20,
        )
        response.raise_for_status()
        result = response.json()
    except Exception as exc:
        print("Sentiment ERROR:", str(exc))
        try:
            print("Sentiment RAW:", response.text[:500])
        except Exception:
            pass
        return "NEUTRAL"

    # Debug
    print("Sentiment RAW:", result)

    if isinstance(result, list) and result:
        if isinstance(result[0], dict):
            return result[0].get("label", "NEUTRAL")
        if isinstance(result[0], list) and result[0]:
            return result[0][0].get("label", "NEUTRAL")
    return "NEUTRAL"


def analyze_query(text):
    intent = detect_intent(text)
    sentiment = detect_sentiment(text)

    return {
        "intent": intent,
        "sentiment": sentiment,
        "confidence": _last_intent_confidence,
    }
