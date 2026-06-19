from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found.")

client = Groq(api_key=api_key)

def analyze_resume(resume_text, job_role):

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze the following resume for the role: {job_role}

Resume:
{resume_text}

Return your answer in this format:

ATS Score: XX/100

Skills Found:
- ...

Missing Skills:
- ...

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- Give at least 5 specific improvements.
- Mention certifications if relevant.
- Recommend missing technical skills.
- Suggest better resume formatting if needed.
- ...

Suitable Job Roles:
- ...
Use bullet points where appropriate.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    return response.choices[0].message.content