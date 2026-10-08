import streamlit as st
from ai import analyze_error
from practice import make_practice

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


st.set_page_config(page_title="DebugBuddy", page_icon="🐞")

# ---- Sidebar: mistake tracker ----
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

st.title("🐞 DebugBuddy")
st.caption("Paste your code and error. Learn why it broke, not just how to fix it.")

language = st.selectbox("Language", ["Python", "C", "Java", "JavaScript"])
mode = st.radio("Mode", ["Learn (hints)", "Fix (show answer)"], horizontal=True)
explain_in = st.selectbox("Explain in", ["English", "Tamil", "Malayalam", "Hindi"])

st.selectbox(
    "Try an example (Python)",
    ["- choose -"] + list(EXAMPLES),
    key="example",
    on_change=load_example,
)
code = st.text_area("Your code", height=200, key="code")
error = st.text_area("Error message", height=100, key="error")

if st.button("Help me understand"):
    with st.spinner("Thinking..."):
        res = analyze_error(
            code, error, language,
            "learn" if mode.startswith("Learn") else "fix",
            explain_in,
        )
        st.session_state["result"] = res
        st.session_state["shown"] = 0
        st.session_state["practice"] = None
        if res["error_type"] != "Unknown":
            st.session_state["history"].append(res["error_type"])
            st.rerun()

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
