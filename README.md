# 🤖 AI Customer Support Agent

🚀 Live Demo: https://ai-customer-support-agent-7mtkhpwe77fdbw9bdhcagq.streamlit.app/

An AI-powered customer support system that analyzes customer queries, identifies their intent and sentiment, generates appropriate responses, and routes the issue to the relevant support department.

The system combines **NLP, Hugging Face models, OpenAI-based response generation, FastAPI, and Streamlit** to provide an interactive customer-support experience.

---

## 🚀 Overview

Traditional customer-support systems often rely on predefined rules and manual ticket routing. This project uses AI to understand customer messages and automatically determine:

- What the customer is asking about
- Whether the customer is satisfied, neutral, frustrated, or angry
- Which department should handle the issue
- Whether the conversation contains potential churn/cancellation signals
- What response should be provided to the customer

The goal is to reduce manual support effort while providing faster and more context-aware responses.

---

## ✨ Key Features

### 🧠 Intent Detection

The system identifies the primary intent behind a customer message.

Supported intent categories include:

- Payment Problem
- Hardware Problem
- Software Bug
- Refund Issue
- General Question

Intent detection is implemented using **Hugging Face NLP models**.

---

### 😊 Sentiment & Emotion Analysis

The system analyzes the emotional tone of the customer's message.

It can identify signals such as:

- Neutral
- Frustrated
- Angry
- Positive

This allows the system to adapt its response according to the customer's emotional state.

---

### 💬 AI Response Generation

The agent generates customer-support responses based on the detected intent and sentiment.

Responses can be enhanced using an AI language model through the configured API integration.

The objective is to produce responses that are:

- Relevant to the customer's issue
- Context-aware
- Professional
- Appropriate to the customer's sentiment

---

### 🚨 Churn-Risk Detection

The system checks customer messages for signals indicating possible cancellation or dissatisfaction.

Examples of signals include:

- Cancellation requests
- Repeated complaints
- Strong dissatisfaction
- Switching to another service

When such signals are detected, the system can generate an appropriate retention-oriented response or escalation.

---

### 🏢 Department Routing

Based on the detected intent, the system identifies the appropriate support area.

For example:

| Customer Query | Detected Intent | Department |
|---|---|---|
| "I was charged twice" | Payment Problem | Billing |
| "My device is not turning on" | Hardware Problem | Technical Support |
| "The application keeps crashing" | Software Bug | Technical Support |
| "I want my money back" | Refund Issue | Refunds |
| "How can I change my account details?" | General Question | General Support |

---

### 🖥️ Interactive Streamlit Interface

The project provides an interactive chat interface using **Streamlit**.

The interface allows users to:

- Enter customer queries
- View AI-generated responses
- See detected intent
- View sentiment/emotion analysis
- View support routing information
- Adjust chat font size using the built-in font-size control

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      Customer       │
                    │       Query         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Streamlit Frontend │
                    │   Chat Interface    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI Backend  │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │ Intent       │ │ Sentiment /  │ │ Churn Signal │
        │ Detection    │ │ Emotion      │ │ Detection    │
        └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
               │                │                │
               └────────────────┼────────────────┘
                                ▼
                     ┌─────────────────────┐
                     │   AI Response       │
                     │   Generation        │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Department /        │
                     │ Support Routing     │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │ Response to Customer│
                     └─────────────────────┘
🛠️ Technology Stack
Programming Language
Python
AI / NLP
Hugging Face
Hugging Face Transformers / NLP models
OpenAI API
Sentiment Analysis
Intent Classification
Natural Language Processing
Backend
FastAPI
Uvicorn
REST API
Frontend
Streamlit
Environment & Configuration
Python-dotenv
Environment variables
.gitignore for API credentials
📂 Project Structure
AI-CUSTOMER-SUPPORT-AGENT/
│
├── main.py
├── ai_enhancer.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── .env

.env is used locally for API credentials and should never be uploaded to GitHub.

🔄 How It Works
Step 1 — Customer enters a query

The customer submits a support message through the Streamlit interface.

Example:

"I was charged twice for my subscription and I want a refund."
Step 2 — Intent Detection

The NLP model analyzes the query and determines the most relevant intent.

Intent → Payment Problem / Refund Issue
Step 3 — Sentiment Analysis

The customer's emotional state is analyzed.

Sentiment → Negative / Frustrated
Step 4 — Churn Signal Detection

The system checks whether the customer is showing signs of cancellation or dissatisfaction.

Churn Risk → Possible
Step 5 — AI Response Generation

The detected information is used to generate an appropriate customer-support response.

Step 6 — Support Routing

The system determines the appropriate support department.

Department → Billing / Refund Support
Step 7 — Response

The final response is displayed through the Streamlit interface.

🔐 Environment Variables

Create a .env file in the project root:

HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_api_key
Important

Never commit your .env file to GitHub.

Your .gitignore should contain:

.env
__pycache__/
*.pyc
⚙️ Installation
1. Clone the repository
git clone https://github.com/Anshika032/AI-CUSTOMER-SUPPORT-AGENT.git
2. Navigate to the project
cd AI-CUSTOMER-SUPPORT-AGENT
3. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate

For macOS/Linux:

source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Configure API keys

Create .env and add:

HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_api_key
▶️ Running the Application
Start the FastAPI Backend
uvicorn main:app --reload

The API will be available locally at:

http://127.0.0.1:8000

FastAPI also provides interactive API documentation at:

http://127.0.0.1:8000/docs
Start the Streamlit Frontend

In another terminal:

streamlit run app.py

The Streamlit application will open in your browser.

🧪 Example Queries
Billing
I was charged twice for my subscription.

Expected analysis:

Intent: Payment Problem
Sentiment: Negative
Department: Billing
Technical Issue
My application keeps crashing whenever I try to log in.

Expected analysis:

Intent: Software Bug
Sentiment: Negative
Department: Technical Support
Hardware Issue
My device is not turning on even after charging it.

Expected analysis:

Intent: Hardware Problem
Department: Technical Support
Refund
I want a refund for my recent purchase.

Expected analysis:

Intent: Refund Issue
Department: Refund Support
🎯 Project Objectives

The project was developed with the following objectives:

Automate basic customer-support interactions.
Use NLP to understand customer queries.
Automatically classify customer intent.
Detect customer sentiment and emotional signals.
Identify potential churn/cancellation signals.
Generate context-aware responses.
Route customer issues to relevant departments.
Provide an interactive support interface.
🔮 Future Improvements

Potential extensions include:

Conversation memory for multi-turn conversations
Customer profile integration
Automatic ticket creation
CRM integration
Knowledge-base / RAG integration
FAQ document retrieval
Human-agent handoff
Conversation analytics dashboard
Support-ticket prioritization
Multilingual customer support
Voice-based customer support
Production-scale deployment
📌 Use Cases

This system can be adapted for:

E-commerce customer support
SaaS platforms
Banking support
Technical support desks
Subscription-based services
Product support
Automated help desks
📚 Concepts Demonstrated

This project demonstrates practical implementation of:

Natural Language Processing
Intent Classification
Sentiment Analysis
Emotion Detection
Zero-shot Classification
Large Language Model APIs
AI Response Generation
REST APIs
FastAPI
Streamlit
API Authentication
Environment Variable Management
AI-based Customer Support Automation
👩‍💻 Author

Anshika Shukla

Electronics & Communication Engineering
Banasthali University

Areas of Interest
Artificial Intelligence
Machine Learning
Natural Language Processing
Edge AI
Computer Vision
Intelligent Systems
⭐ Project Highlights

AI-powered customer support system combining NLP-based intent detection, sentiment analysis, churn-signal detection, AI response generation, and automated support routing through a FastAPI + Streamlit architecture.


### One important correction

I would **not** put claims like *“95% accuracy”*, *“reduces support cost by 60%”*, *“production-ready”*, or similar metrics in your README unless you actually measured them. Your current README is based on the features you actually implemented rather than invented performance numbers. 

Also, because you specifically used **Hugging Face**, I've made that a central part of the
<img width="956" height="470" alt="image" src="https://github.com/user-attachments/assets/b511dc13-3218-4feb-aa70-f47b6f057b0f" />

