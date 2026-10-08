import os
import streamlit as st
from ai import analyze_error
from practice import make_practice
from runner import run_python

RUN_ENABLED = os.environ.get("ENABLE_RUN") == "1"

EXAMPLES = {
    "IndexError": (
        """fruits = ["apple", "banana", "mango"]
for i in range(4):
    print(fruits[i])""",
        "IndexError: list index out of range",
    ),
    "NameError": (
        """name = "Asha"
print("Hello " + nme)""",
        "NameError: name 'nme' is not defined",
    ),
    "TypeError": (
        """age = 18
print("I am " + age + " years old")""",
        'TypeError: can only concatenate str (not "int") to str',
    ),
    "SyntaxError": (
        """x = 5
if x > 3
    print("big")""",
        "SyntaxError: expected ':'",
    ),
    "IndentationError": (
        """def greet():
print("hi")

greet()""",
        "IndentationError: expected an indented block after function definition on line 1",
    ),
    "ZeroDivisionError": (
        """a = 10
b = 0
print(a / b)""",
        "ZeroDivisionError: division by zero",
    ),
    "KeyError": (
        """student = {"name": "Asha", "age": 18}
print(student["grade"])""",
        "KeyError: 'grade'",
    ),
    "ValueError": (
        """number = int("abc")
print(number)""",
        "ValueError: invalid literal for int() with base 10: 'abc'",
    ),
}


def load_example():
    choice = st.session_state["example"]
    if choice in EXAMPLES:
        st.session_state["code"], st.session_state["error"] = EXAMPLES[choice]


def clear_all():
    st.session_state["code"] = ""
    st.session_state["error"] = ""
    st.session_state["example"] = "- choose -"
    st.session_state["result"] = None
    st.session_state["practice"] = None
    st.session_state["captured"] = None


st.set_page_config(page_title="DebugBuddy", page_icon="🐞")

# ---- Sidebar: mistake tracker + model choice ----
history = st.session_state.setdefault("history", [])
with st.sidebar:
    st.header("📊 Your mistakes")
    if history:
        counts = {}
        for e in history:
            counts[e] = counts.get(e, 0) + 1
        st.bar_chart(counts)
        top = max(counts, key=counts.get)
        st.write(f"Most common: **{top}** ({counts[top]}x)")
        st.caption("Try the practice problem button to work on it.")
        if st.button("Clear history"):
            st.session_state["history"] = []
            st.rerun()
    else:
        st.caption("Analyze an error and your mistakes will show up here.")

    st.divider()
    st.header("⚙️ AI model")
    provider = st.selectbox("Run with", ["Groq (gpt-oss-120b)", "Ollama (local)"])
    if provider.startswith("Ollama"):
        st.caption("Needs Ollama running on your own computer. It will not work on the public demo.")

st.title("🐞 DebugBuddy")
st.caption("Paste your code and error. Learn why it broke, not just how to fix it.")

with st.expander("How does this work?"):
    st.markdown(
        "- **Learn mode** gives you 3 hints, one at a time, so you can try to solve it yourself.\n"
        "- **Fix mode** shows the corrected code.\n"
        "- Pick your language and level, then use **practice problem** to train on the same kind of mistake."
    )

language = st.selectbox("Language", ["Python", "C", "Java", "JavaScript"])
mode = st.radio("Mode", ["Learn (hints)", "Fix (show answer)"], horizontal=True)
explain_in = st.selectbox("Explain in", ["English", "Tamil", "Malayalam", "Hindi"])
level = st.selectbox("Your level", ["Complete beginner", "I know the basics"])

run_mode = False
if RUN_ENABLED:
    run_mode = st.checkbox("Run my code for me (Python only): I'll find the error automatically")
else:
    st.caption("Auto-run is switched off on the public demo for safety.")

st.selectbox(
    "Try an example (Python)",
    ["- choose -"] + list(EXAMPLES),
    key="example",
    on_change=load_example,
)
code = st.text_area("Your code", height=200, key="code")
if run_mode:
    error = ""
else:
    error = st.text_area("Error message", height=100, key="error")

col1, col2 = st.columns([3, 1])
go = col1.button("Help me understand", type="primary")
col2.button("Clear", on_click=clear_all)

if go:
    err_text = error
    proceed = True
    st.session_state["captured"] = None

    if run_mode:
        if not code.strip():
            st.warning("Please paste your code first.")
            proceed = False
        else:
            with st.spinner("Running your code..."):
                out, err_text = run_python(code)
            if not err_text.strip():
                st.success("Your program ran without any errors!")
                if out:
                    st.code(out)
                proceed = False
            else:
                st.session_state["captured"] = err_text

    if proceed:
        with st.spinner("Thinking..."):
            res = analyze_error(
                code, err_text, language,
                "learn" if mode.startswith("Learn") else "fix",
                explain_in, level, provider,
            )
            st.session_state["result"] = res
            st.session_state["shown"] = 0
            st.session_state["practice"] = None
            if res["error_type"] != "Unknown":
                st.session_state["history"].append(res["error_type"])
                st.rerun()

captured = st.session_state.get("captured")
if captured:
    with st.expander("Error found by running your code"):
        st.code(captured)

result = st.session_state.get("result")
if result:
    st.subheader(f"{result['error_type']} (line {result['line']})")
    st.write(result["explanation"])

    hints = result["hints"]
    for i in range(st.session_state.get("shown", 0)):
        st.info(f"Hint {i + 1}: {hints[i]}")
    if st.session_state.get("shown", 0) < len(hints):
        if st.button("Show next hint"):
            st.session_state["shown"] += 1
            st.rerun()

    if result["fix"]:
        st.subheader("Fixed code")
        st.code(result["fix"], language=language.lower())

    if result["concept"]:
        st.subheader("Concept")
        st.write(result["concept"])

    st.divider()
    if st.button("Give me a practice problem"):
        with st.spinner("Creating a practice problem..."):
            st.session_state["practice"] = make_practice(
                result["error_type"], result["concept"], language, explain_in
            )

    practice = st.session_state.get("practice")
    if practice:
        st.subheader("Practice")
        st.write(practice["task"])
        st.code(practice["starter_code"], language=language.lower())
        with st.expander("Show solution"):
            st.code(practice["solution"], language=language.lower())
