# ✈️ TripTailor: The Dynamic Travel Concierge

### 🏆 Google AI Agents Capstone Project - Concierge Track

**TripTailor** is an intelligent agent designed to solve the fragmentation in travel planning. Instead of switching between calculator apps and search engines, TripTailor orchestrates these tools autonomously to provide accurate itineraries and budget forecasts.

## 🎥 Project Demo
https://youtu.be/E5wGB2yKns4

## 🚀 Live Deployment
https://app-capstone-project-cnj9ubftny722bcskdejwq.streamlit.app/

## 🤖 Features & Implementation
This agent demonstrates **3 Key Concepts** from the course:

1.  **Tool Use (Function Calling):** 
    - The agent acts as a router. If the user asks for math (e.g., "total cost"), it delegates to a Python function `calculate_budget` to ensure 100% accuracy, solving the common LLM math hallucination problem.
    - If the user asks for recommendations, it triggers `search_attractions`.
2.  **Observability:**
    - The application features a real-time "Glass Box" sidebar. Users and developers can see exactly when the agent decides to call a tool, what arguments it passes, and the raw output it receives.
3.  **Sessions & Memory:**
    - The agent utilizes `st.session_state` to maintain context across the conversation, allowing for follow-up questions like "What if I stay 2 more days?" without re-explaining the trip details.

## 🛠️ Tech Stack
- **Model:** Google Gemini 2.0 Flash (via `google-generativeai`)
- **Frontend:** Streamlit
- **Language:** Python

## 📦 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/TripTailor-Agent.git
