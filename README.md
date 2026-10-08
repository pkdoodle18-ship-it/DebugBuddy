# 🐞 DebugBuddy

An AI tutor that helps beginners understand their coding errors instead of just copying the fix.

**Live demo:** https://debugbuddy-atwnvibs4f37dbuubepuvw.streamlit.app/

## The problem
First-year students get stuck on cryptic error messages. They often paste them into a chatbot, copy the answer, and learn nothing.

## What DebugBuddy does
- **Learn mode:** 3 progressive hints, revealed one at a time
- **Fix mode:** the corrected code with a short explanation
- Points to the **exact line** and explains the **concept** behind the mistake
- Explains in **English, Tamil, Malayalam, or Hindi**
- **Student level** selector (complete beginner / knows the basics)
- **Practice problem generator** for the same kind of mistake
- **Mistake tracker** that shows which errors you make most
- **Example errors** dropdown for quick tries
- **Run my code** mode (local): paste only your code and DebugBuddy finds the error itself
- Works with **Groq (gpt-oss-120b)** or a **local open-source model via Ollama**

## Tech stack
Python, Streamlit, Groq API with the open-weight `gpt-oss-120b` model, optional Ollama (`qwen2.5-coder`).

## Run it locally
```bash
git clone https://github.com/pkdoodle18-ship-it/DebugBuddy.git
cd DebugBuddy
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_key_here"
export ENABLE_RUN=1   # optional: enables "Run my code" mode
streamlit run app.py
```
Get a free key at [console.groq.com](https://console.groq.com).

## Project structure
- `app.py`: Streamlit interface
- `ai.py`: prompt, model calls, JSON handling
- `practice.py`: practice problem generator
- `runner.py`: runs Python code with a timeout

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Good first issues are labeled in the Issues tab.

## Built at
Hacktoberfest Hack Day Coimbatore (Open Source × AI)

## License
MIT
