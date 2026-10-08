# Contributing to DebugBuddy

Thanks for helping! This project is built for beginners, so beginner contributions are very welcome.

## Run it locally
```bash
git clone https://github.com/pkdoodle18-ship-it/DebugBuddy.git
cd DebugBuddy
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GROQ_API_KEY="your_key_here"
streamlit run app.py
```

## Ideas for first contributions
- Add more example errors to the dropdown in `app.py`
- Support more explanation languages (Telugu, Kannada, Bengali...)
- Improve the prompts in `ai.py` and `practice.py`
- Add support for running C or Java code in `runner.py` (safely!)

## How to contribute
1. Fork the repo and create a branch
2. Make your change and test it with `streamlit run app.py`
3. Open a pull request explaining what you changed

Never commit API keys.
