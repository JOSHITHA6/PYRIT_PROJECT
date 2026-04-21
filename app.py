import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# 🎨 PREMIUM UI CSS
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
}

/* CENTER CONTAINER */
.block-container {
    max-width: 1100px;
    margin: auto;
    margin-top: 60px;
}

/* GLASS CARD */
.section-box {
    padding: 25px;
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}

/* DIVIDER */
.divider {
    width: 2px;
    height: 100%;
    background: linear-gradient(to bottom, #38bdf8, #c084fc);
    margin: auto;
    border-radius: 10px;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    height: 48px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    color: white;
    border: none;
    transition: 0.2s;
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 12px rgba(192,132,252,0.6);
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="title">PyRIT – Red Teaming Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Test LLMs for vulnerabilities with adversarial prompts</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col_mid, col2 = st.columns([1, 0.03, 1])

# =========================
# LEFT (INPUT)
# =========================
with col1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DIVIDER
# =========================
with col_mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# RIGHT (OUTPUT)
# =========================
with col2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

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
                    st.markdown(f"### Attack {i+1}")
                    st.write(r["response"])
                    st.markdown("---")

            except Exception as e:
                st.error(str(e))

    else:
        st.info("Run the model to see results")

    st.markdown('</div>', unsafe_allow_html=True)