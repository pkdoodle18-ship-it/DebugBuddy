import os
import json
import requests

API_KEY = os.environ.get("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5-coder:3b"

SYSTEM_PROMPT = """You are a patient programming teacher for first-year students.
The student gives you code (with line numbers) and an error message.
Reply with ONLY valid JSON using exactly these keys:
error_type, line, explanation, hints, fix, concept.

Rules:
- Use simple words. Explain any jargon.
- "line" is the line number where the problem is (integer, or null if unsure).
- "explanation" is 2-3 sentences on what went wrong and why. Describe the problem only. Do NOT say how to fix it; the fix belongs only in the hints and the "fix" field.
- "hints" is a list of exactly 3 strings. Hint 1 is a gentle nudge,
  Hint 2 is more specific, Hint 3 almost gives the answer but not the full code.
- "fix" is the full corrected code, without line numbers.
- "concept" is a short explanation of the underlying idea with a tiny example.
- Write "explanation", "hints", and "concept" in the language the student asks for.
  Keep code, variable names, and error names (like IndexError) in English.
- Adjust to the student level given: for "Complete beginner" use very simple words, short sentences and everyday analogies; for "I know the basics" you may use normal programming terms.
- Never invent errors that are not in the code."""

EMPTY = {
    "error_type": "Unknown",
    "line": None,
    "explanation": "Sorry, I couldn't analyze this. Please try again.",
    "hints": [],
    "fix": "",
    "concept": "",
}


def number_lines(code):
    return "\n".join(f"{i}: {line}" for i, line in enumerate(code.splitlines(), 1))


def _call_model(messages, provider):
    if provider.startswith("Ollama"):
        r = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "messages": messages,
                  "stream": False, "format": "json"},
            timeout=180,
        )
        return r.json()["message"]["content"]
    r = requests.post(
        URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": MODEL, "messages": messages,
              "response_format": {"type": "json_object"}},
        timeout=60,
    )
    return r.json()["choices"][0]["message"]["content"]


def analyze_error(code, error, language="Python", mode="learn",
                  explain_in="English", level="Complete beginner",
                  provider="Groq"):
    if not code.strip() or not error.strip():
        return {**EMPTY, "explanation": "Please paste both your code and the error."}

    user_msg = (
        f"Language: {language}\n"
        f"Explain in: {explain_in}\n"
        f"Student level: {level}\n\n"
        f"Code:\n{number_lines(code)}\n\nError:\n{error}"
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]
    try:
        data = json.loads(_call_model(messages, provider))
    except Exception as e:
        print("Error:", e)
        return EMPTY

    result = {**EMPTY, **data}
    if mode == "learn":
        result["fix"] = ""  # hide the answer in learn mode
    return result
