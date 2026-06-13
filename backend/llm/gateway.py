import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question: str, context: str) -> str:
    prompt = (
        "You are a helpful assistant for NETSOL Technologies.\n"
        "Answer based on context below.\n"
        "If not in context, say: I do not have enough information.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}\n\nAnswer:"
    )
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content
