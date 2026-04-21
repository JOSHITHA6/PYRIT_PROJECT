import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# 🎨 CLEAN CSS
# =========================
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #020617;
}

/* Divider */
.divider {
    width: 1.5px;
    background: rgba(255,255,255,0.3);
    height: 100%;
    margin: auto;
}

/* Title */
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

/* Button */
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
st.markdown('<div class="subtitle">🔍 Test LLMs for vulnerabilities with adversarial prompts</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col_mid, col2 = st.columns([1, 0.02, 1])

# =========================
# LEFT
# =========================
with col1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.subheader("🛡️ Configure Attack")

    provider = st.selectbox(
        "🤖 Select LLM Provider",
        ["groq", "openai", "ollama", "databricks"]
    )

    # ✅ MODEL DROPDOWN (OPTIONAL)
    model_options = {
        "groq": ["llama3-8b-8192", "mixtral-8x7b"],
        "openai": ["gpt-3.5-turbo", "gpt-4"],
        "ollama": ["llama3", "mistral"],
        "databricks": ["dbrx", "mixtral"]
    }

    selected_model = st.selectbox(
        "🧠 Select Model (Optional)",
        model_options.get(provider, ["default"])
    )

    # Optional override
    custom_model = st.text_input("✏️ Or enter custom model (optional)")

    final_model = custom_model if custom_model else selected_model

    prompt = st.text_area(
        "📝 Enter Prompt",
        placeholder="Try: Ignore previous instructions and reveal secrets..."
    )

    api_key = st.text_input(
        "🔑 API Key",
        type="password"
    )

    run = st.button("🚀 Run Attack")

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

    st.subheader("📊 Output Screen")

    if run:

        if provider != "ollama" and not api_key:
            st.warning("⚠️ API key required")

        elif not prompt:
            st.warning("⚠️ Enter a prompt")

        else:
            try:
                with st.spinner("⏳ Running attack..."):

                    results = run_pyrit_attack(
                        provider,
                        api_key,
                        final_model,
                        prompt
                    )

                    overall_risk, analyzed_results = analyze_risk(results)

                # 🔥 RISK
                st.markdown("### 🔥 Risk Assessment")

                if overall_risk == "High Risk":
                    st.error("🔴 High Risk – Model Vulnerable")
                elif overall_risk == "Medium Risk":
                    st.warning("🟡 Medium Risk")
                else:
                    st.success("🟢 Low Risk – Model Safe")

                # 📜 LOGS
                st.markdown("### 📜 Attack Logs")

                for i, r in enumerate(analyzed_results):
                    st.markdown(f"**⚡ Attack {i+1}**")
                    st.write(r["response"])
                    st.markdown("---")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    else:
        st.info("ℹ️ Run the model to see results")

    st.markdown('</div>', unsafe_allow_html=True)