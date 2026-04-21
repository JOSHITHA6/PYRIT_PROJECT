import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

st.set_page_config(layout="wide")

# =========================
# 🎨 GLOBAL CSS (CORRECT FIX)
# =========================
st.markdown("""
<style>

/* 🌌 FULL PAGE BACKGROUND */
.stApp {
    background-color: #020617;
}

/* 🔥 TARGET STREAMLIT MAIN CONTAINER (IMPORTANT FIX) */
.block-container {
    padding: 2rem 2rem;
    border-radius: 18px;
    border: 2px solid rgba(56,189,248,0.4);
    box-shadow: 0 0 25px rgba(56,189,248,0.6),
                0 0 45px rgba(192,132,252,0.4);
    background-color: #020617;
}

/* 🧱 INNER BOXES */
.section-box {
    padding: 20px;
    border-radius: 14px;
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ➖ DIVIDER */
.divider {
    border-left: 2px solid rgba(255,255,255,0.15);
    height: 100%;
}

/* 🎯 TITLE */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* 🧾 SUBTITLE */
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 20px;
}

/* 🚀 BUTTON */
.stButton>button {
    width: 100%;
    height: 48px;
    border-radius: 10px;
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