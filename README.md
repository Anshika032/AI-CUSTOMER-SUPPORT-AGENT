# 🤖 AI Customer Support Agent

🚀 Live Demo: https://ai-customer-support-agent-7mtkhpwe77fdbw9bdhcagq.streamlit.app/

An AI-powered customer support system that understands customer queries, detects their intent and emotional state, identifies potential churn signals, retrieves relevant information using **Retrieval-Augmented Generation (RAG)**, and uses a **Large Language Model (LLM)** to generate context-aware responses.

The system combines **Hugging Face NLP models, RAG, LLM-based response generation, FastAPI, and Streamlit** to create an intelligent customer-support workflow.

---

## 🚀 Overview

Traditional customer-support systems often depend on predefined rules or manual ticket routing. This project uses AI and NLP to understand customer conversations and automatically determine how a support request should be handled.

The system can:

- Understand customer queries
- Classify customer intent
- Analyze sentiment and emotion
- Detect frustration and anger
- Identify potential churn/cancellation signals
- Retrieve relevant information using RAG
- Generate context-aware responses using an LLM
- Route issues toward the appropriate support category
- Escalate situations that require additional attention

The objective is to make customer support **faster, more intelligent, and more context-aware**.

---

# ✨ Key Features

## 🧠 1. Intent Detection

The system analyzes the customer's message and identifies the type of issue being reported.

Examples include:

- Payment problems
- Hardware problems
- Software bugs
- Refund-related issues
- General questions

Intent detection allows the system to determine how the customer's request should be handled.

---

## 😊 2. Sentiment & Emotion Analysis

The system analyzes the emotional tone of customer messages using NLP models.

It can identify signals such as:

- Neutral
- Frustrated
- Angry

This information is used to make the generated response more appropriate to the customer's situation.

For example:

```text
Customer:
"I have contacted support three times and nobody has fixed this!"

Emotion:
Frustrated / Angry

The system can then generate a more empathetic response instead of treating the message like a normal FAQ request.

🚨 3. Churn-Risk Detection

The system identifies customer messages that may indicate dissatisfaction, cancellation intent, or potential churn.

Examples of signals include:

"I want to cancel my subscription."

"I am switching to another service."

"This is the third time I have complained."

"I don't want to use your service anymore."

When such signals are detected, the system can trigger an appropriate retention or escalation response.

🔍 4. Retrieval-Augmented Generation (RAG)

The project uses Retrieval-Augmented Generation (RAG) to improve the quality and relevance of AI-generated responses.

Instead of relying only on the LLM's pretrained knowledge, the system retrieves relevant information from the available support knowledge base and provides that information as context to the LLM.

RAG Pipeline
Customer Query
      │
      ▼
Query Processing
      │
      ▼
Relevant Knowledge Retrieval
      │
      ▼
Retrieved Context
      │
      ▼
Context + Customer Query
      │
      ▼
LLM
      │
      ▼
Context-Aware Support Response

This allows the agent to generate responses that are grounded in relevant support information.

🤖 5. Large Language Model (LLM)

An LLM is used to generate natural-language customer-support responses.

The LLM receives information such as:

Original customer query
Retrieved RAG context
Detected intent
Sentiment/emotion information
Churn-related signals

and generates a response appropriate to the customer's issue.

Conceptual Flow
                 ┌──────────────────┐
Customer Query ──►                  │
                 │                  │
RAG Context ─────►       LLM        ├──► AI Response
                 │                  │
Intent ──────────►                  │
                 │                  │
Sentiment ───────►                  │
                 └──────────────────┘
🏢 6. Support Routing & Escalation

After analyzing the customer message, the system determines the appropriate support path.

For example:

Customer Query	Intent	Support Action
"I was charged twice."	Payment Problem	Billing Support
"My device isn't turning on."	Hardware Problem	Technical Support
"The application keeps crashing."	Software Bug	Technical Support
"I want my money back."	Refund Issue	Refund Support
"I want to cancel my subscription."	Cancellation / Churn Signal	Retention / Escalation

This creates a workflow where the AI agent can handle straightforward requests while identifying situations that require escalation.

🖥️ 7. Interactive Streamlit Interface

The project includes a Streamlit-based interface for interacting with the AI customer-support agent.

The interface allows users to:

Enter customer queries
Interact with the AI support agent
View generated responses
Analyze customer intent
View sentiment/emotion information
Identify potential churn signals
Receive context-aware support responses
🏗️ System Architecture
                         ┌─────────────────────┐
                         │      Customer       │
                         │       Query         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Streamlit Interface │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
          │ Intent       │  │ Sentiment /  │  │ Churn Signal │
          │ Detection    │  │ Emotion      │  │ Detection    │
          └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
                 │                 │                 │
                 └─────────────────┼─────────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │   RAG Pipeline      │
                         │                     │
                         │ Query → Retrieval   │
                         │ → Context           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        LLM          │
                         │ Response Generation │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Support Response &  │
                         │ Routing / Escalation│
                         └─────────────────────┘
🔄 End-to-End Workflow
Step 1 — Customer Query

The customer enters a question, complaint, or support request.

Example:

"I was charged twice for my subscription and I am extremely frustrated."
Step 2 — Query Analysis

The system analyzes the message using NLP.

It determines:

Intent       → Payment Problem
Emotion      → Frustrated
Churn Signal → Possible
Step 3 — Knowledge Retrieval

The query is passed through the RAG pipeline.

Relevant information from the support knowledge base is retrieved.

Step 4 — Context Construction

The retrieved information is combined with the customer's original query and the results of the NLP analysis.

Step 5 — LLM Response Generation

The LLM uses the retrieved context and customer information to generate an appropriate response.

Step 6 — Routing / Escalation

The system identifies the appropriate support category and determines whether additional escalation or retention handling may be required.

Step 7 — Response

The final AI-generated response is presented to the customer through the Streamlit interface.

🛠️ Technology Stack
Programming
Python
AI / Machine Learning
Large Language Models (LLMs)
Retrieval-Augmented Generation (RAG)
Natural Language Processing (NLP)
Hugging Face
Hugging Face Transformers
Intent Classification
Sentiment Analysis
Emotion Detection
Churn-Risk Detection
Context-Aware Response Generation
Backend
FastAPI
REST APIs
Frontend
Streamlit
Supporting Tools
Environment Variables
API-based AI services
Python Virtual Environment
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

The .env file is used locally for API credentials and must not be committed to GitHub.

🔐 Environment Variables

Create a .env file in the project root and add the required credentials used by your implementation.

Example:

HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_api_key
⚠️ Security

Never upload API keys or access tokens to GitHub.

Your .gitignore should include:

.env
__pycache__/
*.pyc
⚙️ Installation
1. Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
2. Navigate to the Project
cd AI-CUSTOMER-SUPPORT-AGENT
3. Create a Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
5. Configure Environment Variables

Create the .env file and add the required API credentials.

▶️ Running the Project
Start the FastAPI Backend
uvicorn main:app --reload

The backend will run locally on:

http://127.0.0.1:8000

FastAPI's interactive API documentation can be accessed through:

http://127.0.0.1:8000/docs
Start the Streamlit Application

Open another terminal and run:

streamlit run app.py

The Streamlit interface will then open in the browser.

🧪 Example Customer Queries
Payment Problem
I was charged twice for my subscription.

Possible analysis:

Intent       → Payment Problem
Sentiment    → Negative
Department   → Billing
Software Issue
The application keeps crashing whenever I try to log in.

Possible analysis:

Intent       → Software Bug
Sentiment    → Negative
Department   → Technical Support
Hardware Issue
My device is not turning on even after charging it.

Possible analysis:

Intent       → Hardware Problem
Department   → Technical Support
Refund Request
I want a refund for my recent purchase.

Possible analysis:

Intent       → Refund Issue
Department   → Refund Support
Churn Signal
I am tired of these problems. I want to cancel my subscription.

Possible analysis:

Intent       → Cancellation
Emotion      → Frustrated
Churn Signal → High
Action       → Retention / Escalation
🎯 Project Objectives

The project was developed to:

Automate basic customer-support interactions.
Understand customer queries using NLP.
Classify customer intent automatically.
Analyze sentiment and emotional state.
Detect potential churn and cancellation signals.
Retrieve relevant information using RAG.
Use an LLM to generate context-aware responses.
Route support requests to relevant categories.
Identify conversations that may require escalation.
Provide an interactive AI-support experience.
🧠 AI Pipeline

The core intelligence of the system can be summarized as:

                 CUSTOMER MESSAGE
                        │
                        ▼
                ┌───────────────┐
                │ NLP Analysis  │
                └───────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Intent       Emotion        Churn
      Detection     Analysis       Signal
          │             │             │
          └─────────────┼─────────────┘
                        ▼
               ┌────────────────┐
               │ RAG Retrieval  │
               └───────┬────────┘
                       │
                       ▼
               Retrieved Context
                       │
                       ▼
               ┌────────────────┐
               │      LLM       │
               └───────┬────────┘
                       │
                       ▼
              AI Support Response
                       │
                       ▼
             Routing / Escalation
💡 Why RAG + LLM?

A traditional chatbot may generate responses based primarily on the model's pretrained knowledge.

This project combines RAG and an LLM so that the response-generation process can incorporate relevant information retrieved from the support knowledge base.

Without RAG
Customer Query
      ↓
     LLM
      ↓
Generated Response
With RAG
Customer Query
      ↓
Knowledge Retrieval
      ↓
Relevant Context
      ↓
Context + Query
      ↓
     LLM
      ↓
Grounded Support Response

This architecture is particularly useful for customer-support systems where responses need to reference specific support information.

📈 Potential Applications

The architecture can be adapted for:

E-commerce customer support
SaaS platforms
Technical support
Subscription services
Product support
Automated help desks
Customer-retention workflows
🔮 Future Improvements

Possible extensions include:

Multi-turn conversation memory
Larger customer knowledge bases
Automated ticket creation
CRM integration
Human-agent handoff
Support analytics dashboard
Automatic ticket prioritization
Multilingual customer support
Voice-based customer support
Production deployment and monitoring
📚 Concepts Demonstrated

This project demonstrates practical application of:

Artificial Intelligence
Machine Learning
Natural Language Processing
Large Language Models
Retrieval-Augmented Generation
Knowledge Retrieval
Intent Classification
Sentiment Analysis
Emotion Detection
Churn-Risk Detection
Prompt Engineering
Context-Aware Response Generation
Hugging Face Transformers
REST API Development
FastAPI
Streamlit
AI-based Customer Support Automation
⭐ Project Highlights

An AI-powered customer support agent combining Hugging Face NLP models, RAG, and LLM-based response generation to understand customer intent, analyze sentiment, detect churn signals, retrieve relevant knowledge, and generate context-aware support responses.

👩‍💻 Author
Anshika Shukla

Electronics & Communication Engineering
Banasthali University

Interests
Artificial Intelligence
Machine Learning
Natural Language Processing
Generative AI
Retrieval-Augmented Generation
Edge AI
Intelligent Systems

<img width="956" height="470" alt="Screenshot 2026-09-28 152125" src="https://github.com/user-attachments/assets/e504d8a9-7537-40dd-8fde-7d0e26f9ab94" />


