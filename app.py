import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# CSS (UPDATED TO LIGHT THEME)
# =========================
st.markdown("""
<style>
.stApp { background-color: white; }

.divider {
    width: 1.5px;
    background: rgba(0,0,0,0.2);
    height: 100%;
    margin: auto;
}

.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: black;
}

.subtitle {
    text-align: center;
    color: #374151;
    margin-bottom: 20px;
}

/* Force all text to black */
html, body, [class*="css"] {
    color: black;
}

/* Inputs */
input, textarea {
    background-color: white !important;
    color: black !important;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
}

/* Button (kept gradient, readable) */
.stButton>button {
    width: 100%;
    height: 45px;
    border-radius: 8px;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="title">🚨 PyRIT – Red Teaming Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Test LLMs for vulnerabilities with adversarial prompts</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col_mid, col2 = st.columns([1, 0.02, 1])

# =========================
# LEFT
# =========================
with col1:
    st.subheader("🛡️ Configure Attack")

    provider = st.selectbox("Select LLM Provider",
                            ["groq", "openai", "ollama"])

    model = st.text_input(
        "Model Name (Optional)",
        placeholder="Leave empty OR enter your own model"
    )
    api_key = st.text_input("API Key", type="password")

    prompt = st.text_area("Enter Prompt")

    run = st.button("🚀 Run Attack")

# =========================
# DIVIDER
# =========================
with col_mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# RIGHT
# =========================
with col2:
    st.subheader("📊 Output")

    if run:

        if provider != "ollama" and not api_key:
            st.warning("API key required")

        elif not prompt:
            st.warning("Enter prompt")

        else:
            try:
                with st.spinner("Running attack..."):

                    results = run_pyrit_attack(
                        provider,
                        api_key,
                        model if model else None,
                        prompt
                    )

                    overall_risk, analyzed_results = analyze_risk(results)

                st.markdown("### 🔥 Risk")

                if overall_risk == "High Risk":
                    st.error("High Risk")
                elif overall_risk == "Medium Risk":
                    st.warning("Medium Risk")
                else:
                    st.success("Low Risk")

                st.markdown("### 📜 Logs")

                for i, r in enumerate(analyzed_results):
                    st.write(f"Attack {i+1}")
                    st.write(r["response"])
                    st.markdown("---")

            except Exception as e:
                st.error(str(e))

    else:
        st.info("Run model to see results")