import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# 🎨 PYRIT COLOR THEME ONLY (NO COMPLEX DIVS)
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #020617;
}

/* Titles */
h1, h2, h3 {
    color: #e2e8f0;
}

/* Subtext */
p {
    color: #94a3b8;
}

/* Divider column */
[data-testid="column"]:nth-child(2) {
    border-left: 2px solid rgba(255,255,255,0.15);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    box-shadow: 0 0 12px rgba(192,132,252,0.6);
    transform: scale(1.02);
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background-color: #0f172a;
    color: white;
    border-radius: 8px;
}

/* Select */
.stSelectbox div {
    background-color: #0f172a;
    color: white;
}

/* Info / messages */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("🔐 PyRIT – Red Teaming Tool")
st.caption("Test LLMs for vulnerabilities with adversarial prompts")

# =========================
# LAYOUT (SHAP STYLE)
# =========================
col1, col2 = st.columns([1, 1])

# =========================
# LEFT SIDE (INPUT)
# =========================
with col1:
    st.subheader("🛡️ Configure Attack")

    provider = st.selectbox(
        "Select the LLM",
        ["groq", "openai", "ollama", "databricks"]
    )

    prompt = st.text_area(
        "Enter the Prompt",
        placeholder="Enter your adversarial prompt here..."
    )

    api_key = st.text_input(
        "Enter API Key",
        type="password",
        placeholder="Required for most providers"
    )

    model = st.text_input(
        "Model Name (Optional)",
        placeholder="e.g. llama3-8b-8192 / gpt-3.5-turbo"
    )

    run = st.button("🚀 Run Attack")


# =========================
# RIGHT SIDE (OUTPUT)
# =========================
with col2:
    st.subheader("💻 Output Screen")

    if run:

        if provider != "ollama" and not api_key:
            st.warning("API key required")

        elif not prompt:
            st.warning("Enter a prompt")

        else:
            try:
                with st.spinner("Running PyRIT attack..."):

                    results = run_pyrit_attack(
                        provider,
                        api_key,
                        model,
                        prompt
                    )

                    overall_risk, analyzed_results = analyze_risk(results)

                # -------- RISK --------
                st.markdown("### 🔥 Overall Risk")

                if overall_risk == "High Risk":
                    st.error("🔴 High Risk – Model Weak")
                elif overall_risk == "Medium Risk":
                    st.warning("🟡 Medium Risk")
                else:
                    st.success("🟢 Low Risk – Model Safe")

                # -------- LOGS --------
                st.markdown("### 📜 Attack Logs")

                for i, r in enumerate(analyzed_results):
                    st.markdown(f"**Attack {i+1}**")
                    st.write(r["response"])
                    st.markdown("---")

            except Exception as e:
                st.error(str(e))

    else:
        st.info("Run the model to see results")