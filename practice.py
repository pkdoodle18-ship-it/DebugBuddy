import json
import requests
from ai import API_KEY, URL, MODEL

PROMPT = """You are a programming teacher for first-year students.
You get the type of error a student made and the concept behind it.
Create ONE short practice exercise with a similar mistake.
Reply with ONLY valid JSON with exactly these keys: task, starter_code, solution.
- "task": 1-2 simple sentences telling the student what the program should do and to fix it.
- "starter_code": a small program (5-8 lines) containing a bug of the same kind. Do not add comments that reveal the bug.
- "solution": the corrected version of starter_code.
Write "task" in the language the student asks for. Keep code in English."""


def make_practice(error_type, concept, language="Python", explain_in="English"):
    user_msg = (
        f"Programming language: {language}\n"
        f"Write the task in: {explain_in}\n"
        f"Error type: {error_type}\n"
        f"Concept: {concept}"
    )
    try:
        r = requests.post(
            URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "response_format": {"type": "json_object"},
            },
            timeout=60,
        )
        data = json.loads(r.json()["choices"][0]["message"]["content"])
        return {
            "task": data.get("task", ""),
            "starter_code": data.get("starter_code", ""),
            "solution": data.get("solution", ""),
        }
    except Exception as e:
        print("Error:", e)
        return None
