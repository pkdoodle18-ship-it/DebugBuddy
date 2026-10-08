import streamlit as st
from ai import analyze_error
from practice import make_practice

st.set_page_config(page_title="DebugBuddy", page_icon="🐞")
st.title("🐞 DebugBuddy")
st.caption("Paste your code and error. Learn why it broke, not just how to fix it.")

language = st.selectbox("Language", ["Python", "C", "Java", "JavaScript"])
mode = st.radio("Mode", ["Learn (hints)", "Fix (show answer)"], horizontal=True)
explain_in = st.selectbox("Explain in", ["English", "Tamil", "Malayalam", "Hindi"])
code = st.text_area("Your code", height=200)
error = st.text_area("Error message", height=100)

if st.button("Help me understand"):
    with st.spinner("Thinking..."):
        st.session_state["result"] = analyze_error(
            code, error, language,
            "learn" if mode.startswith("Learn") else "fix",
            explain_in,
        )
        st.session_state["shown"] = 0
        st.session_state["practice"] = None

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
