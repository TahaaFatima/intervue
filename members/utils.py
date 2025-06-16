from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def suggest_questions(job_description):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    You're an expert interview coach. Based on this job description, generate 5 specific and relevant interview questions:

                    {job_description}

                    Only list the questions in plain text. Do not include explanations or headings.
                    """
                }
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating questions:\n\n{str(e)}"
