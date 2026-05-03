import streamlit as st
from BACKEND.pyrit_wrapper import run_pyrit_attack
from BACKEND.risk_analyzer import analyze_risk

# NEW IMPORTS: batch processor for automation mode
from utils.batch_processor import run_batch_assessment, get_csv_filename

st.set_page_config(layout="wide")

# =========================
# CSS (LIGHT THEME + DROPDOWN + ARROW FIX)
# Preserved exactly as original
# =========================

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: white;
}

/* 🔝 Fix Streamlit header */
header {
    background-color: white !important;
}

/* Toolbar (top right icons area) */
[data-testid="stToolbar"] {
    background-color: white !important;
}

/* Ensure header text/icons are visible */
[data-testid="stToolbar"] svg {
    fill: black !important;
}

[data-testid="stToolbar"] button {
    color: black !important;
}

/* Divider */
.divider {
    width: 1.5px;
    background: rgba(0,0,0,0.2);
    height: 100%;
    margin: auto;
}

/* Titles */
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

/* Force text visibility */
h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: black !important;
}

/* Inputs */
input, textarea {
    background-color: white !important;
    caret-color: black !important;
    color: black !important;
}

/* Placeholder */
input::placeholder, textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

/* 🔽 SELECTBOX FIX */
div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
}

/* Selected value */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* Text inside dropdown */
div[data-baseweb="select"] span {
    color: black !important;
}

/* Dropdown list */
ul[role="listbox"] {
    background-color: white !important;
    color: black !important;
}

/* Options */
li[role="option"] {
    background-color: white !important;
    color: black !important;
}

/* Hover */
li[role="option"]:hover {
    background-color: #f1f5f9 !important;
}

/* 🔽 FIX DROPDOWN ARROW */
div[data-baseweb="select"] svg {
    fill: black !important;
    color: black !important;
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
# Preserved exactly as original
# =========================

st.markdown('<div class="title">🚨 PyRIT – Red Teaming Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Test LLMs for vulnerabilities with adversarial prompts</div>', unsafe_allow_html=True)

# =========================
# LAYOUT
# Preserved exactly as original
# =========================

col1, col_mid, col2 = st.columns([1, 0.02, 1])

# =========================
# LEFT COLUMN
# =========================

with col1:
    st.subheader("🛡️ Configure Attack")

    # ── NEW: Radio button for input mode selection ──
    # Added at the top, before all existing inputs
    input_mode = st.radio(
        "Select Input Mode",
        options=["1. Enter manually", "2. Automate (Built-in 100 prompts)"],
        index=0,          # default: manual
        horizontal=True   # side by side layout
    )
    # ── END NEW ──

    # These three inputs are ALWAYS visible in both modes (LLM always needs them)
    provider = st.selectbox(
        "Select LLM Provider",
        ["groq", "openai", "ollama"]
    )

    model = st.text_input(
        "Model Name (Optional)",
        placeholder="Leave empty OR enter your own model"
    )

    api_key = st.text_input("API Key", type="password")

    # ── NEW: Show different input/button based on selected mode ──

    if input_mode == "1. Enter manually":
        # EXISTING behaviour — prompt textarea + run attack button (unchanged)
        prompt = st.text_area("Enter Prompt")
        run = st.button("🚀 Run Attack")
        run_batch = False  # not in batch mode

    else:
        # NEW automation mode — no prompt textarea, different button
        prompt = None
        run = False        # not in manual mode
        run_batch = st.button("🚀 Run Risk Assessment on 100 Prompts")

    # ── END NEW ──

# =========================
# DIVIDER
# Preserved exactly as original
# =========================

with col_mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================
# RIGHT COLUMN
# =========================

with col2:
    st.subheader("📊 Output")

    # ── EXISTING: Manual mode logic (visually identical, risk now uses embeddings internally) ──
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

                    # analyze_risk now uses embedding detection internally
                    # (BACKEND/risk_analyzer.py was updated — call is unchanged)
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

    # ── NEW: Automation mode logic ──
    elif run_batch:
        if provider != "ollama" and not api_key:
            st.warning("API key required")
        else:
            try:
                # run_batch_assessment shows its own progress bar inside
                csv_bytes = run_batch_assessment(
                    provider=provider,
                    api_key=api_key,
                    model=model if model else None
                )

                # Show download button after processing completes
                filename = get_csv_filename()
                st.success("✅ Assessment complete! Download your results below.")
                st.download_button(
                    label="⬇️ Download CSV Results",
                    data=csv_bytes,
                    file_name=filename,
                    mime="text/csv"
                )

            except Exception as e:
                st.error(str(e))

    # ── END NEW ──

    else:
        # Default state — preserved exactly as original
        st.info("Run model to see results")