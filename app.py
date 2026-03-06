
import time
import re
import streamlit as st
from google import genai

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ASTRA™",
    page_icon="🩺",
    layout="wide"
)

# ============================================================
# SIMPLE PROFESSIONAL STYLE
# ============================================================

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #050d1a, #0c1a2e);
    color: white;
}
h1 { color: #00f7ff; }
h2, h3 { color: #ff00c8; }
.stButton button {
    background-color: #00f7ff;
    color: black;
    font-weight: bold;
}
.footer {
    text-align:center;
    margin-top:40px;
    font-size:0.8rem;
    color:#94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.title("🩺 ASTRA™")
st.subheader("AI-Supported Structured Thinking & Reasoning in Anaesthesia")
st.markdown("### eXcellence in Clinical Cognition")

st.markdown("""
Clinical Intelligence Engine built for:

• Consultant crisis simulation  
• Postgraduate viva mastery  
• Structured reasoning refinement  
• MCQ & clinical vignette assessment  

Developed by **Dr Bhavna Gupta**  
Associate Professor – Anaesthesiology  
Research Mentor | AI in Medical Education Advocate
""")

st.markdown("---")

# ============================================================
# API KEY SECTION
# ============================================================

with st.expander("🔑 How to Generate Gemini API Key"):
    st.markdown("""
1. Visit: https://aistudio.google.com/app/apikey  
2. Click "Create API Key"  
3. Copy the key  
4. Paste in sidebar  

Your key is not stored.
""")

st.sidebar.title("Gemini API Key")
api_key = st.sidebar.text_input("Enter API Key", type="password")

if not api_key:
    st.info("Enter your Gemini API key to begin.")
    st.stop()

client = genai.Client(api_key=api_key)

# ============================================================
# MODEL FALLBACK (STABLE)
# ============================================================

def _parse_retry_delay(err_str):
    """Extract retry delay in seconds from a RESOURCE_EXHAUSTED error."""
    match = re.search(r"retry(?:Delay)?[\"': ]*(\d+)", err_str, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def _try_model(model_name, prompt, max_retries=2):
    """Try a single model with automatic retry on transient 429s."""
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text, None
        except Exception as e:
            err_str = str(e)
            last_err = err_str

            if "NOT_FOUND" in err_str or "404" in err_str:
                return None, f"Model not found (deprecated or removed)"

            if "INVALID" in err_str or "API key" in err_str.lower() or "401" in err_str:
                return None, f"API key error: {err_str}"

            if "PERMISSION_DENIED" in err_str or "403" in err_str:
                return None, "Permission denied — enable the Generative Language API"

            if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                if "limit: 0" in err_str:
                    return None, "Free tier limit is **0** — billing must be enabled"
                delay = _parse_retry_delay(err_str) or (15 * (attempt + 1))
                if attempt < max_retries:
                    time.sleep(min(delay, 60))
                    continue
                return None, f"Quota exhausted after {max_retries + 1} attempts"

            return None, f"Unexpected: {err_str}"

    return None, f"Failed after retries: {last_err}"


def generate_with_fallback(prompt):

    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
    ]

    errors = {}
    for model_name in models_to_try:
        result, err = _try_model(model_name, prompt)
        if result is not None:
            return result
        errors[model_name] = err

    error_lines = "\n".join(f"- **{m}**: {e}" for m, e in errors.items())
    return f"""❌ **All models failed.**

{error_lines}

**What to do:**
1. Go to [Google AI Studio → API Keys](https://aistudio.google.com/app/apikey) and verify your key is active
2. If you see "limit is 0" above, your free tier is depleted — **enable billing** in [Google Cloud Console](https://console.cloud.google.com/billing) to get paid-tier quotas
3. Run `pip install -U google-genai` to ensure you have the latest model names
"""

# ============================================================
# MODE SELECTION
# ============================================================

mode = st.selectbox(
    "Select Mode:",
    [
        "Consultant Rapid Mode",
        "PG Teaching Mode",
        "Clinical Vignette Mode"
    ]
)

clinical_input = st.text_area("Enter Clinical Scenario:", height=180)

# ============================================================
# CONSULTANT MODE
# ============================================================

if mode == "Consultant Rapid Mode" and clinical_input:

    if st.button("Generate Consultant Plan"):

        prompt = f"""
You are a senior consultant anaesthesiologist.

Scenario:
{clinical_input}

Provide:

1. Ranked differentials
2. Immediate 5-minute management
3. Drug dosing with examples
4. Red flags
5. Escalation ladder
"""

        with st.spinner("Analyzing scenario..."):
            output = generate_with_fallback(prompt)

        st.markdown(output)

        st.download_button(
            "Download as Text",
            output,
            file_name="ASTRA_Consultant_Output.txt"
        )

# ============================================================
# PG TEACHING MODE (FULLY INTERACTIVE)
# ============================================================

elif mode == "PG Teaching Mode" and clinical_input:

    if "pg_questions" not in st.session_state:
        st.session_state.pg_questions = None
        st.session_state.pg_feedback = None

    if st.button("Start Viva Simulation"):

        question_prompt = f"""
You are a senior anaesthesia faculty.

Scenario:
{clinical_input}

Generate exactly 3 structured viva questions.
Do NOT provide answers.
"""

        with st.spinner("Preparing viva questions..."):
            st.session_state.pg_questions = generate_with_fallback(question_prompt)
            st.session_state.pg_feedback = None

    if st.session_state.pg_questions:

        st.markdown("### Viva Questions")
        st.markdown(st.session_state.pg_questions)

        pg_answer = st.text_area("Enter your answers:", height=200)

        if st.button("Submit for Evaluation") and pg_answer:

            eval_prompt = f"""
Scenario:
{clinical_input}

Questions:
{st.session_state.pg_questions}

PG Answers:
{pg_answer}

Evaluate:
1. Strengths
2. Gaps
3. Missed priorities
4. Score out of 10
"""

            with st.spinner("Evaluating answers..."):
                st.session_state.pg_feedback = generate_with_fallback(eval_prompt)

    if st.session_state.pg_feedback:
        st.markdown("### Faculty Feedback")
        st.markdown(st.session_state.pg_feedback)

        st.download_button(
            "Download Feedback",
            st.session_state.pg_feedback,
            file_name="ASTRA_Viva_Feedback.txt"
        )

# ============================================================
# CLINICAL VIGNETTE MODE (FIXED INTERACTIVE FLOW)
# ============================================================

elif mode == "Clinical Vignette Mode" and clinical_input:

    if "vignette_case" not in st.session_state:
        st.session_state.vignette_case = None
        st.session_state.vignette_feedback = None

    if st.button("Start Vignette Simulation"):

        vignette_prompt = f"""
Create a clinical vignette based on:

{clinical_input}

End with the question:
"What would you do next?"

Do NOT reveal the answer yet.
"""

        with st.spinner("Generating vignette..."):
            st.session_state.vignette_case = generate_with_fallback(vignette_prompt)
            st.session_state.vignette_feedback = None

    if st.session_state.vignette_case:

        st.markdown("### Clinical Scenario")
        st.markdown(st.session_state.vignette_case)

        user_decision = st.text_area("Your clinical decision:", height=150)

        if st.button("Evaluate My Decision") and user_decision:

            eval_prompt = f"""
Scenario:
{clinical_input}

User Decision:
{user_decision}

Evaluate:
1. Correct aspects
2. Missed priorities
3. Safety concerns
4. Consultant-level upgrade
"""

            with st.spinner("Evaluating decision..."):
                st.session_state.vignette_feedback = generate_with_fallback(eval_prompt)

    if st.session_state.vignette_feedback:
        st.markdown("### Faculty Evaluation")
        st.markdown(st.session_state.vignette_feedback)

        st.download_button(
            "Download Evaluation",
            st.session_state.vignette_feedback,
            file_name="ASTRA_Vignette_Feedback.txt"
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
ASTRA™ | AI Clinical Intelligence Engine  
Developed by Dr Bhavna Gupta  
Educational Use Only | Does not replace clinical judgment
</div>
""", unsafe_allow_html=True)
