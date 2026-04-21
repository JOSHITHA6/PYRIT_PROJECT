import streamlit as st
from backend.pyrit_wrapper import run_pyrit_attack
from backend.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# GLOBAL STYLES (NEON UI)
# =========================
st.markdown("""
<style>

/* Page */
body {
    background-color: #0f172a;
}

/* Outer Neon Box */
.main-box {
    padding: 30px;
    border-radius: 20px;
    background: #0b1220;
    border: 2px solid transparent;
    background-clip: padding-box;
    box-shadow: 0 0 25px rgba(0, 123, 255, 0.4),
                0 0 35px rgba(255, 0, 255, 0.2);
}

/* Divider */
.divider {
    border-left: 2px solid rgba(255,255,255,0.15);
    height: 100%;
    margin: auto;
}

/* Section Boxes */
.section-box {
    padding: 20px;
    border-radius: 15px;
    background: #111827;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Titles */
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
    color: #9ca3af;
    margin-bottom: 30px;
}

/* Run Button */
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    border: none;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    color: white;
    box-shadow: 0 0 12px rgba(56,189,248,0.6);
    transition: 0.3s;
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
# MAIN BOX
# =========================
st.markdown('<div class="main-box">', unsafe_allow_html=True)

col1, col_mid, col2 = st.columns([1, 0.05, 1])

# =========================
# LEFT SIDE (INPUT)
# =========================
with col1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.subheader("🛡️ CONFIGURE ATTACK")

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
# RIGHT SIDE (OUTPUT)
# =========================
with col2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.subheader("💻 OUTPUT SCREEN")

    if run:

        if provider != "ollama" and not api_key:
            st.warning("API key required for this provider")

        elif not prompt:
            st.warning("Please enter a prompt")

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
                    st.error("🔴 High Risk – Model Vulnerable")
                elif overall_risk == "Medium Risk":
                    st.warning("🟡 Medium Risk")
                else:
                    st.success("🟢 Low Risk – Model Safe")

                # -------- LOGS --------
                st.markdown("### 📜 Attack Logs")

                for i, r in enumerate(analyzed_results):

                    st.markdown(f"### Attack {i+1}")
                    st.markdown(f"**Prompt:** {r['prompt']}")
                    st.markdown(f"**Response:** {r['response']}")

                    if r["attack_detected"]:
                        st.warning("⚠️ Malicious Prompt Detected")

                    if r["leakage_detected"]:
                        st.error("🚨 Data Leakage Detected")

                    st.markdown(f"**Verdict:** {r['verdict']}")
                    st.markdown("---")

            except Exception as e:
                st.error(str(e))

    else:
        st.info("Run the model to see results")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CLOSE MAIN BOX
# =========================
st.markdown('</div>', unsafe_allow_html=True)