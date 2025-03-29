import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")  # Default to localhost

st.title("AI Empathy Gemini Chat")

user_message = st.text_input("Enter your message:")

if st.button("Get Empathetic Response"):
    if user_message:
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat/generate_response/",
                json={"user_message": user_message}
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            st.write("Empathetic Response:", data["response"])

            # Display Sentiment Analysis Results
            st.write("Sentiment Analysis:")
            st.write(f"  Label: {data['sentiment']['label']}")
            st.write(f"  Score: {data['sentiment']['score']}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {e}")
    else:
        st.warning("Please enter a message.")