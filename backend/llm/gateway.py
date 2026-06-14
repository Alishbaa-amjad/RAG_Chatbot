import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question: str, context: str) -> str:
    prompt = (
        "You are a helpful assistant for NETSOL Technologies.\n"
        "Use the context below to answer the question.\n"
        "The context contains real information from NETSOL website.\n"
        "Answer directly and clearly from the context.\n"
        "Only say 'I do not have enough information' if the context truly has nothing related.\n\n"
        "CONTEXT:\n"
        f"{context}\n\n"
        "QUESTION:\n"
        f"{question}\n\n"
        "ANSWER:"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a NETSOL Technologies assistant. Always answer from the provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content