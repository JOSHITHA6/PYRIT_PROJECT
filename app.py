import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# 🎨 CLEAN CSS (NO GHOST BOXES)
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #020617;
}

/* 🔥 DO NOT STYLE block-container heavily */
.block-container {
    max-width: 1000px;
    margin: auto;
    padding-top: 2rem;
}

/* SINGLE OUTER BORDER (SAFE WAY) */
.main-wrapper {
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 16px;
    padding: 25px;
    background: rgba(15,23,42,0.6);
}

/* INNER SECTIONS */
.section-box {
    padding: 18px;
    border-radius: 12px;
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(255,255,255,0.08);
}

/* CLEAN DIVIDER */
.divider {
    width: 1.5px;
    background: rgba(255,255,255,0.3);
    height: 100%;
    margin: auto;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #e2e8f0;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 20px;
}

/* BUTTON */
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
st.markdown('<div class="title">PyRIT – Red Teaming Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Test LLMs for vulnerabilities with adversarial prompts</div>', unsafe_allow_html=True)

# =========================
# WRAPPER (ONLY ONE BOX)
# =========================
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

col1, col_mid, col2 = st.columns([1, 0.02, 1])

# =========================
# LEFT
# =========================
with col1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.subheader("Configure Attack")

    provider = st.selectbox("Select the LLM",
                            ["groq", "openai", "ollama", "databricks"])

    prompt = st.text_area("Enter the Prompt")

    api_key = st.text_input("Enter API Key", type="password")

    model = st.text_input("Model Name (Optional)")

    run = st.button("Run Attack")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# DIVIDER
# =========================
with col_mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# RIGHT
# =========================
with col2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.subheader("Output Screen")

    if run:

        if provider != "ollama" and not api_key:
            st.warning("API key required")

        elif not prompt:
            st.warning("Enter a prompt")

        else:
            try:
                with st.spinner("Running attack..."):

                    results = run_pyrit_attack(
                        provider,
                        api_key,
                        model,
                        prompt
                    )

                    overall_risk, analyzed_results = analyze_risk(results)

                if overall_risk == "High Risk":
                    st.error("High Risk – Model Weak")
                elif overall_risk == "Medium Risk":
                    st.warning("Medium Risk")
                else:
                    st.success("Low Risk – Model Safe")

                for i, r in enumerate(analyzed_results):
                    st.markdown(f"**Attack {i+1}**")
                    st.write(r["response"])
                    st.markdown("---")

            except Exception as e:
                st.error(str(e))

    else:
        st.info("Run the model to see results")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)