import os

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def evaluate_answer(question, answer):

    prompt = f"""
You are an expert technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return EXACTLY in this format:

Technical Knowledge: X/10
Communication: X/10
Problem Solving: X/10
Confidence: X/10
Overall Score: X/10

Strengths:
- point 1
- point 2

Improvements:
- point 1
- point 2
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    return response.choices[0].message.content