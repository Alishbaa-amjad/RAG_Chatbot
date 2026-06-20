import os
import time
from google import genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(question, context):
    return (
        "You are a helpful assistant for NETSOL Technologies.\n"
        "Use the context below to answer the question.\n"
        "Read carefully — if context mentions someone as CEO, Chairman, or executive, "
        "they may also be a founder or co-founder.\n"
        "Give a detailed, informative answer like a professional assistant.\n"
        "If context has ANY related information, use it — do not say 'I do not have enough information' unless context is completely unrelated.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION:\n{question}\n\nANSWER:"
    )

def get_gemini_answer(prompt):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def get_groq_answer(prompt):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a NETSOL Technologies assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content

def get_answer(question: str, context: str) -> str:
    prompt = build_prompt(question, context)

    # Pehle Gemini try karo
    for attempt in range(2):
        try:
            return get_gemini_answer(prompt)
        except Exception as e:
            print(f"Gemini attempt {attempt+1} failed: {e}")
            if attempt < 1:
                time.sleep(3)

    # Gemini fail hua — Groq use karo
    print("Switching to Groq backup...")
    try:
        return get_groq_answer(prompt)
    except Exception as e:
        print(f"Groq also failed: {e}")
        return "Service is temporarily unavailable. Please try again."