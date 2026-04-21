import streamlit as st
from BACKEND.llm_connector import LLMConnector

st.set_page_config(layout="wide")

# =========================
# TITLE
# =========================
st.markdown("<h1 style='text-align:center;'>PyRIT – Red Teaming Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Test LLMs for vulnerabilities with adversarial prompts</p>", unsafe_allow_html=True)

# =========================
# MAIN CONTAINER (BOX)
# =========================
st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    margin: auto;
}

.outer-box {
    padding: 30px;
    border-radius: 16px;
    background-color: white;
    box-shadow: 0 0 20px rgba(0, 123, 255, 0.4);
}

.divider {
    border-left: 2px solid #e0e6f0;
    height: 100%;
}

.stButton>button {
    background-color: #28a745;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# OUTER BOX
# =========================
st.markdown('<div class="outer-box">', unsafe_allow_html=True)

col1, col_mid, col2 = st.columns([1, 0.05, 1])

# =========================
# LEFT SIDE (INPUT)
# =========================
with col1:
    st.subheader("CONFIGURE ATTACK")

    provider = st.selectbox(
        "Select the LLM",
        ["groq", "openai", "google", "ollama", "databricks"]
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

    run = st.button("Run Attack")

# =========================
# DIVIDER
# =========================
with col_mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# RIGHT SIDE (OUTPUT)
# =========================
with col2:
    st.subheader("OUTPUT SCREEN")

    if run:

        if provider != "ollama" and not api_key:
            st.warning("API key required for this provider")

        elif not prompt:
            st.warning("Please enter a prompt")

        else:
            try:
                with st.spinner("Running PyRIT attack..."):

                    # 🔥 Run multiple adversarial attacks
                    results = run_pyrit_attack(
                        provider,
                        api_key,
                        model,
                        prompt
                    )

                    # 🔥 Analyze risk + logs
                    overall_risk, analyzed_results = analyze_risk(results)

                # =========================
                # 🔥 OVERALL RISK DISPLAY
                # =========================
                st.markdown("### 🔥 Overall Risk")

                if overall_risk == "High Risk":
                    st.error("🔴 High Risk – Model Vulnerable")
                elif overall_risk == "Medium Risk":
                    st.warning("🟡 Medium Risk")
                else:
                    st.success("🟢 Low Risk – Model Safe")

                # =========================
                # 📜 DETAILED ATTACK LOGS
                # =========================
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