from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk
import streamlit as st
st.markdown("""
<style>
.stButton>button {
    width: 100%;
    background-color: #2b6cb0;
    color: white;
    border-radius: 8px;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="PyRIT GUI", layout="wide")

# Title
st.title("PyRIT – Red Teaming Tool")
st.caption("Test LLMs for vulnerabilities with adversarial prompts and risk scoring")

# Layout
col1, col2 = st.columns([1, 1])

# LEFT SIDE
with col1:
    st.subheader("TARGET")
    target = st.text_input("", placeholder="e.g. customer support bot, internal HR tool")

    st.subheader("MODEL")
    model = st.selectbox("", ["Claude Sonnet 4", "GPT-4", "Gemini"])

    st.subheader("ADVERSARIAL PROMPT")
    adversarial_prompt = st.text_area("", placeholder="Enter your adversarial prompt here...")

    st.subheader("PRESET ATTACK TYPE")
    attack_type = st.selectbox("", ["None (custom prompt)", "Prompt Injection", "Jailbreak"])

    st.subheader("SYSTEM PROMPT (OPTIONAL)")
    system_prompt = st.text_area("", placeholder="Override system instructions here...")

    run_button = st.button("Run test")

# RIGHT SIDE
with col2:
    st.subheader("OUTPUT SCREEN")
    
    st.markdown("### RISK SCORE") #//TE
    risk_placeholder = st.empty()

    st.markdown("### MODEL RESPONSE") #//TE
    response_placeholder = st.empty()

# Logic (temporary)
if run_button:
    if "hack" in adversarial_prompt.lower():
        risk = "High risk"
        response = "⚠️ Model exposed sensitive behavior."
    else:
        risk = "Low risk / Safe"
        response = "✅ Model response is safe."

    # Show risk
    if risk == "High risk":
        risk_placeholder.error(risk)
    else:
        risk_placeholder.success(risk)

    # Show response
    response_placeholder.text_area("Model Response", response, height=200)