from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_question(
    role,
    difficulty,
    company,
    previous_questions
):

    prompt = f"""
You are a professional technical interviewer.

Target Company: {company}
Role: {role}
Difficulty: {difficulty}

Previous Questions:
{chr(10).join(previous_questions)}

Generate ONE interview question only.

Rules:
- Do NOT repeat previous questions.
- Ask a realistic interview question.
- Match the style of {company} interviews.
- Do NOT provide answers.
- Do NOT provide explanations.
- Return only the question.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    

    return response.choices[0].message.content