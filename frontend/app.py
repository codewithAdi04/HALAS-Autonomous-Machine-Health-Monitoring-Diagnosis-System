import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/query"

st.set_page_config(page_title="HALAS AI", layout="centered")
st.title("🤖 HALAS – Hybrid Autonomous Learning Agent System")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input box
user_input = st.text_input("Enter your message", key="user_input")

# Send button
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"message": user_input},
                timeout=10
            )

            result = response.json()

         
            data = result.get("data", {})

            st.session_state.messages.append({
                "user": user_input,
                "bot": data.get("response", "No response from HALAS"),
                "reward": data.get("reward", 0.0),
                "latency": data.get("latency", 0.0),
            })

        except Exception as e:
            st.error(f"API connection failed: {e}")

# Chat display
st.divider()
for msg in st.session_state.messages:
    st.markdown(f"**You:** {msg['user']}")
    st.markdown(f"**HALAS:** {msg['bot']}")
    st.caption(f"Reward: {msg['reward']} | Latency: {msg['latency']:.4f}s")
    st.divider()