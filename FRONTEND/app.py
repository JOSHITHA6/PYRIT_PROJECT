import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# 🎨 GLOBAL CSS (CORRECT FIX)
# =========================
st.markdown("""
<style>

/* Background */
body {
    background-color: #020617;
}

/* MAIN OUTER NEON BOX */
.outer-container {
    padding: 25px;
    border-radius: 18px;
    background: #020617;
    border: 2px solid rgba(56,189,248,0.4);
    box-shadow: 0 0 20px rgba(56,189,248,0.6),
                0 0 40px rgba(192,132,252,0.4);
}

/* LEFT + RIGHT CARDS */
.inner-box {
    padding: 20px;
    border-radius: 15px;
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.08);
}

/* DIVIDER */
.divider {
    border-left: 2px solid rgba(255,255,255,0.15);
    height: 100%;
    margin: auto;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    color: white;
    border: none;
    box-shadow: 0 0 12px rgba(56,189,248,0.6);
}

.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 18px rgba(192,132,252,0.8);
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown('<div class="title">PyRIT – Red Teaming Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Test LLMs for vulnerabilities with adversarial prompts</div>', unsafe_allow_html=True)

# =========================
# 🔥 OUTER NEON BOX START
# =========================
st.markdown('<div class="outer-container">', unsafe_allow_html=True)

col1, col_mid, col2 = st.columns([1, 0.03, 1])

# =========================
# LEFT PANEL
# =========================
with col1:
    st.markdown('<div class="inner-box">', unsafe_allow_html=True)

    st.subheader("🛡️ CONFIGURE ATTACK")

    provider = st.selectbox("Select the LLM",
                            ["groq", "openai", "ollama", "databricks"])

    prompt = st.text_area("Enter the Prompt",
                          placeholder="Enter your adversarial prompt here...")

    api_key = st.text_input("Enter API Key",
                            type="password",
                            placeholder="Required for most providers")

    model = st.text_input("Model Name (Optional)",
                          placeholder="e.g. llama3-8b-8192 / gpt-3.5-turbo")

    run = st.button("🚀 Run Attack")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# DIVIDER
# =========================
with col_mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# =========================
# RIGHT PANEL
# =========================
with col2:
    st.markdown('<div class="inner-box">', unsafe_allow_html=True)

    st.subheader("💻 OUTPUT SCREEN")

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

# =========================
# 🔥 OUTER NEON BOX END
# =========================
st.markdown('</div>', unsafe_allow_html=True)