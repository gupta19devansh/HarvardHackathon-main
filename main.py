from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI  # This works with OpenRouter's SDK

# Replace with your actual key
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
            f"Step 1: Identify emotional tone (e.g., sadness, anxiety, joy). "
            f"Step 2: Respond with an empathetic message using CBT principles.\n\n"
            f"Entry: {entry.text}"
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o",  # Or another model on OpenRouter
            messages=[
                {"role": "system", "content": "You are a compassionate CBT-aligned therapist."},
                {"role": "user", "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",  # Optional
                "X-Title": "TheraBridge"
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
        style_prompt = (
            f"Based on the journal entry, suggest the most suitable therapy style. "
            f"Choose from: CBT, DBT, Psychodynamic, ACT, SFBT. Explain your reasoning briefly.\n\n"
            f"Entry: {entry.text}"
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You are a clinical psychologist trained in multiple therapy styles."},
                {"role": "user", "content": style_prompt}
            ],
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "TheraBridge"
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
