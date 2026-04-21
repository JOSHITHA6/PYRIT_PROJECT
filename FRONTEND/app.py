import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# 🎨 CLEAN CSS (NO NEON, NO BUGS)
# =========================
st.markdown("""
<style>

/* Page */
.stApp {
    background-color: #f5f7fa;
}

/* Box styling */
.box {
    border: 1px solid #d1d5db;
    border-radius: 10px;
    padding: 20px;
    background-color: white;
}

/* Divider line */
.divider {
    border-left: 2px solid #9ca3af;
    height: 100%;
}

/* Button */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 6px;
    height: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("PyRIT – Red Teaming Tool")
st.caption("Test LLMs for vulnerabilities with adversarial prompts")

# =========================
# LAYOUT
# =========================
col1, col_mid, col2 = st.columns([1, 0.02, 1])

# =========================
# LEFT (INPUT)
# =========================
with col1:
    st.markdown('<div class="box">', unsafe_allow_html=True)

    st.subheader("Configure Attack")

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
        type="password"
    )

    model = st.text_input(
        "Model Name (Optional)"
    )

    run = st.button("Run Attack")

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
    st.markdown('<div class="box">', unsafe_allow_html=True)

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

                # -------- RISK --------
                if overall_risk == "High Risk":
                    st.error("High Risk – Model Weak")
                elif overall_risk == "Medium Risk":
                    st.warning("Medium Risk")
                else:
                    st.success("Low Risk – Model Safe")

                # -------- LOGS --------
                for i, r in enumerate(analyzed_results):
                    st.markdown(f"**Attack {i+1}**")
                    st.write(r["response"])
                    st.markdown("---")

            except Exception as e:
                st.error(str(e))

    else:
        st.info("Run the model to see results")

    st.markdown('</div>', unsafe_allow_html=True)