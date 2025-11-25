import streamlit as st
import os
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="TripTailor Agent",
    page_icon="✈️",
    layout="wide"
)

# --- 1. SETUP & AUTH ---
st.sidebar.title("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# --- 2. OBSERVABILITY (REQUIRED FEATURE) ---
def log_trace(step, details):
    """Logs agent actions to the sidebar for observability."""
    if "trace_log" not in st.session_state:
        st.session_state.trace_log = []
    st.session_state.trace_log.append(f"**[{step}]**: {details}")

# --- 3. TOOLS (REQUIRED FEATURE) ---
def calculate_budget(daily_rate: float, days: int, travelers: int) -> float:
    """Calculates the total cost of the trip."""
    total = daily_rate * days * travelers
    log_trace("TOOL USE", f"calculate_budget invoked: {daily_rate} * {days} * {travelers} = {total}")
    return total

def search_attractions(city: str, interest: str) -> str:
    """Searches for top attractions in a city based on interest."""
    log_trace("TOOL USE", f"search_attractions invoked for {city} ({interest})")
    # Mock Database for Reliability
    db = {
        "Tokyo": "Senso-ji, Meiji Shrine, Shibuya Crossing",
        "Paris": "Eiffel Tower, Louvre, Montmartre",
        "New York": "Statue of Liberty, Central Park, Empire State Building"
    }
    return db.get(city, f"General top spots in {city} related to {interest}")

tools_list = [calculate_budget, search_attractions]

# --- 4. AGENT LOGIC ---
def get_gemini_response(user_prompt, history):
    if not api_key:
        return "⚠️ Please enter your API Key in the sidebar."
    
    genai.configure(api_key=api_key)
    
    # System Instruction = Context Engineering
    system_instruction = """
    You are TripTailor, an expert travel concierge.
    1. ALWAYS check if the user asked for a cost calculation. If so, use 'calculate_budget'.
    2. ALWAYS use 'search_attractions' if the user asks what to do.
    3. Be friendly and concise.
    """
    
    try:
        # Using Gemini 2.0 Flash for Speed + Bonus Points
        model = genai.GenerativeModel(
            model_name="models/gemini-2.0-flash", 
            tools=tools_list,
            system_instruction=system_instruction
        )
        
        # Enable automatic function calling
        chat = model.start_chat(history=history, enable_automatic_function_calling=True)
        
        log_trace("AGENT", "Sending prompt to Gemini 2.0...")
        response = chat.send_message(user_prompt)
        log_trace("AGENT", "Response received.")
        
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- 5. UI & SESSION MEMORY (REQUIRED FEATURE) ---
st.title("✈️ TripTailor: AI Travel Concierge")
st.markdown("Powered by **Gemini 2.0 Flash** | Built for Google AI Agent Course")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "model", "content": "Hi! I can plan your trip and calculate your budget. Where are we going?"})

# Display Chat History
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Ex: Trip to Tokyo for 5 days, $150/day. What is the total?"):
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Convert History for Gemini
    gemini_history = []
    for m in st.session_state.messages[:-1]:
        role = "user" if m["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [m["content"]]})

    # Get Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = get_gemini_response(prompt, gemini_history)
            st.write(response_text)
    
    st.session_state.messages.append({"role": "model", "content": response_text})

# Display Logs in Sidebar
st.sidebar.divider()
st.sidebar.subheader("🔍 Live Observability")
if "trace_log" in st.session_state:
    for log in st.session_state.trace_log[::-1]: # Reverse order
        st.sidebar.caption(log)