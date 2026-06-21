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
    previous_questions,
    resume_text=""
):

    prompt = f"""
You are a professional technical interviewer.

Target Company: {company}
Role: {role}
Difficulty: {difficulty}

Candidate Resume:
{resume_text}

Previous Questions:
{chr(10).join(previous_questions)}

Rules:

- Prefer asking questions about the candidate's projects.
- Prefer asking questions about the candidate's skills.
- Do not repeat previous questions.
- Ask only one question.
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