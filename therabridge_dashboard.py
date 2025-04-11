import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"  # Change if deployed elsewhere

st.set_page_config(page_title="TheraBridge AI Journal", layout="centered")

st.title("🧠 TheraBridge - Client Journal Analysis")
st.write("Submit your journal entry and receive AI-assisted emotional analysis and therapy insights.")

client_id = st.text_input("Client ID", value="client_123")

journal_entry = st.text_area("📝 Your Journal Entry", height=200)

if st.button("Analyze Emotion & Get CBT Response"):
    if journal_entry.strip() == "":
        st.warning("Please enter your journal entry.")
    else:
        with st.spinner("Analyzing with AI..."):
            response = requests.post(
                f"{API_BASE}/analyze-journal",
                json={"text": journal_entry, "client_id": client_id}
            )

        if response.status_code == 200:
            result = response.json()
            st.subheader("🧠 AI Analysis")
            st.markdown(f"**Original Entry:**\n\n{result['original_entry']}")
            st.markdown(f"**AI Feedback:**\n\n{result['analysis']}")
        else:
            st.error("Something went wrong. Check your backend or input.")

if st.button("Get Therapy Style Recommendation"):
    if journal_entry.strip() == "":
        st.warning("Please enter your journal entry.")
    else:
        with st.spinner("Finding best-fit therapy style..."):
            response = requests.post(
                f"{API_BASE}/match-therapy-style",
                json={"text": journal_entry, "client_id": client_id}
            )

        if response.status_code == 200:
            result = response.json()
            st.subheader("🧭 Suggested Therapy Style")
            st.markdown(result["therapy_recommendation"])
        else:
            st.error("Failed to fetch recommendation.")
