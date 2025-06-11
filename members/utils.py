import requests

def suggest_questions(job_description):
    try:
        prompt = f"""
                You are an expert technical recruiter. Given the following job description, generate 5 highly relevant interview questions a candidate might be asked.

                Job Description:
                {job_description}

                List only the questions.
                """

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })

        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"Error from Ollama: {response.text}"

    except Exception as e:
        return f"Error generating questions:\n\n{str(e)}"
