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

if run_button:

    if provider != "ollama" and not api_key:
        risk_placeholder.warning("API key required")
    
    elif not adversarial_prompt:
        risk_placeholder.warning("Enter a prompt")

    else:
        try:
            with st.spinner("Running PyRIT attack..."):

                results = run_pyrit_attack(
                    provider,
                    api_key,
                    model,
                    adversarial_prompt
                )

                risk = analyze_risk(results)

            # -------- RISK --------
            if risk == "High Risk":
                risk_placeholder.error("🔴 High Risk")
            elif risk == "Medium Risk":
                risk_placeholder.warning("🟡 Medium Risk")
            else:
                risk_placeholder.success("🟢 Low Risk")

            # -------- RESPONSE --------
            combined_response = ""

            for i, r in enumerate(results):
                combined_response += f"Attack {i+1}:\n{r['response']}\n\n"

            response_placeholder.text_area(
                "Model Responses",
                combined_response,
                height=250
            )

        except Exception as e:
            risk_placeholder.error(str(e))