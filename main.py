# --- main.py ---
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
import tempfile
import os

# OpenRouter GPT client (mock transcription only)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

app = FastAPI()

class JournalEntry(BaseModel):
    text: str
    client_id: str

@app.post("/analyze-journal")
async def analyze_journal(entry: JournalEntry):
    try:
        prompt = (
            f"Analyze the following journal entry. "
            f"Identify emotional tone (e.g., sadness, anxiety, joy). "
            f"Respond with an empathetic message using CBT principles.\n\n"
            f"Entry: {entry.text}"
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a compassionate CBT-aligned therapist."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "The Third Space"
            },
            temperature=0.7
        )

        reply = response.choices[0].message.content

        return {
            "client_id": entry.client_id,
            "original_entry": entry.text,
            "analysis": reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

@app.post("/match-therapy-style")
async def match_therapy_style(entry: JournalEntry):
    try:
        prompt = (
            f"Based on the journal entry, suggest the most suitable therapy style. "
            f"Choose from: CBT, DBT, Psychodynamic, ACT, SFBT. Explain your reasoning briefly.\n\n"
            f"Entry: {entry.text}"
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a clinical psychologist trained in multiple therapy styles."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "The Third Space"
            },
            temperature=0.7
        )

        reply = response.choices[0].message.content

        return {
            "client_id": entry.client_id,
            "therapy_recommendation": reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

@app.post("/transcribe-journal")
async def transcribe_journal(file: UploadFile = File(...)):
    try:
        _ = await file.read()

        transcript_text = (
            "I'm feeling really disconnected lately. I’m trying to keep it together but everything feels harder."
        )

        prompt = (
            f"Analyze the following journal entry. "
            f"Identify emotional tone. "
            f"Respond with an empathetic CBT message.\n\n"
            f"{transcript_text}"
        )

        ai_response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a compassionate CBT-aligned therapist."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "The Third Space"
            },
            temperature=0.7
        )

        reply = ai_response.choices[0].message.content

        return {
            "transcript": transcript_text,
            "analysis": reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription Error: {str(e)}")
