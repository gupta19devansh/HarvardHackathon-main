# --- dashboard.py ---
import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="The Third Space", layout="centered")
st.title("🧠 The Third Space - AI Mental Health Companion")

st.markdown("Submit your journal (text or voice), and get an AI-powered reflection and therapy insights.")

client_id = st.text_input("Client ID", value="client_123")
user_role = st.radio("Select your role:", ["🧍 Client", "🧑‍⚕️ Therapist"], horizontal=True)

# --- TEXT JOURNAL ---
st.header("📝 Text-Based Journal Entry")
journal_entry = st.text_area("What's on your mind today?", height=200)

button_text = "📤 Submit Journal" if user_role == "🧍 Client" else "🔍 Analyze Emotion & Get CBT Response"
if st.button(button_text):
    if journal_entry.strip() == "":
        st.warning("Please enter a journal entry.")
    else:
        with st.spinner("Analyzing with AI..."):
            response = requests.post(f"{API_BASE}/analyze-journal", json={"text": journal_entry, "client_id": client_id})
        if response.status_code == 200:
            result = response.json()
            if user_role == "🧍 Client":
                st.markdown("---")
                st.markdown(f"{result['analysis']}")
            else:
                st.success("🧠 Therapist Diagnostic View")
                st.markdown(f"**Client's Entry:**\n\n{result['original_entry']}")
                st.markdown(f"**AI CBT Reflection:**\n\n{result['analysis']}")
        else:
            st.error("❌ Failed to analyze journal entry.")

if user_role == "🧑‍⚕️ Therapist":
    if st.button("🧠 Generate Therapy Style Diagnostic"):
        if journal_entry.strip() == "":
            st.warning("Please enter a journal entry.")
        else:
            with st.spinner("Running diagnostic..."):
                response = requests.post(f"{API_BASE}/match-therapy-style", json={"text": journal_entry, "client_id": client_id})
            if response.status_code == 200:
                result = response.json()
                st.info("🩺 Suggested Therapeutic Pathway")
                st.markdown(result["therapy_recommendation"])
            else:
                st.error("❌ Failed to suggest therapy style.")

# --- VOICE JOURNAL ---
st.header("🎙️ Voice Journal Upload (MP3/WAV)")
audio_file = st.file_uploader("Upload a voice note (max 60 sec)", type=["mp3", "wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/mp3")

    if st.button("🎧 Transcribe & Analyze Voice Journal"):
        with st.spinner("Transcribing and analyzing..."):
            files = {"file": audio_file.getvalue()}
            response = requests.post(f"{API_BASE}/transcribe-journal", files=files)

        if response.status_code == 200:
            result = response.json()
            if user_role == "🧍 Client":
                st.markdown("---")
                st.markdown(f"🎧 **Transcript:**\n\n{result['transcript']}")
                st.markdown(f"🤖 **Response:**\n\n{result['analysis']}")
            else:
                st.success("🩺 Therapist Diagnostic View")
                st.markdown(f"**Transcript:**\n\n{result['transcript']}")
                st.markdown(f"**AI CBT Reflection:**\n\n{result['analysis']}")

                with st.spinner("Running therapeutic style analysis..."):
                    text_input = result['transcript']
                    response = requests.post(f"{API_BASE}/match-therapy-style", json={"text": text_input, "client_id": client_id})
                    if response.status_code == 200:
                        style_result = response.json()
                        st.info("🧭 Therapy Style Suggested:")
                        st.markdown(style_result["therapy_recommendation"])
                    else:
                        st.warning("⚠️ Therapy match failed.")
        else:
            st.error(f"❌ Failed: {response.text}")
