"""
app.py
Streamlit frontend for the Titanic AI Chatbot.
"""

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🚢 Titanic AI Chatbot",
    page_icon="🚢",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000/ask"
HEALTH_URL = "http://127.0.0.1:8000/"

# ─────────────────────────────────────────────
# Load Titanic Dataset (for visualizations)
# ─────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "titanic.csv")

try:
    titanic_df = pd.read_csv(DATA_PATH)
except Exception:
    titanic_df = None

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🚢 Titanic AI Chatbot")
    st.markdown("Ask questions about the Titanic dataset and get instant insights.")


    st.divider()

    # Sample Questions
    st.subheader("💡 Sample Questions")
    samples = [
        "What was the overall survival rate?",
        "Show me a histogram of passenger ages",
        "How many passengers embarked from each port?",
        "Which gender had a higher survival rate?"
    ]

    for sample in samples:
        if st.button(sample):
            st.session_state.prefill = sample

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ─────────────────────────────────────────────
# Main Chat Area
# ─────────────────────────────────────────────
st.header("🚢 Titanic Dataset AI Assistant")

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle Input
prefill = st.session_state.pop("prefill", None)
prompt = st.chat_input("Ask about the Titanic dataset...") or prefill

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing data..."):
            try:
                response = requests.post(
                    BACKEND_URL,
                    json={"question": prompt},
                    timeout=60
                )

                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer returned.")
                else:
                    answer = f"Server error (Status {response.status_code})"

            except requests.exceptions.ConnectionError:
                answer = "Backend server is not running."
            except requests.exceptions.Timeout:
                answer = "Request timed out."
            except Exception as exc:
                answer = f"Unexpected error: {exc}"

        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # ─────────────────────────────────────────
    # Automatic Visualization Logic
    # ─────────────────────────────────────────
    if titanic_df is not None:

        prompt_lower = prompt.lower()

        try:
            if "histogram" in prompt_lower and "age" in prompt_lower:
                st.subheader("📊 Age Distribution")
                fig, ax = plt.subplots()
                sns.histplot(titanic_df["Age"].dropna(), bins=20, kde=True, ax=ax)
                st.pyplot(fig)

            elif "embarked" in prompt_lower:
                st.subheader("📊 Passengers by Embarkation Port")
                fig, ax = plt.subplots()
                counts = titanic_df["Embarked"].value_counts()
                sns.barplot(x=counts.index, y=counts.values, ax=ax)
                st.pyplot(fig)

            elif "survival" in prompt_lower:
                st.subheader("📊 Survival Distribution")
                fig, ax = plt.subplots()
                counts = titanic_df["Survived"].value_counts()
                ax.pie(counts, labels=["Not Survived", "Survived"], autopct="%1.1f%%")
                st.pyplot(fig)

        except Exception as viz_error:
            st.warning(f"Could not generate visualization: {viz_error}")