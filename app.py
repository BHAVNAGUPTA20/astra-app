import streamlit as st
import google.generativeai as genai

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ASTRA™",
    page_icon="🩺",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("🩺 ASTRA™")
st.subheader("AI-Supported Structured Thinking & Reasoning in Anaesthesia")
st.markdown("### Excellence in Clinical Cognition")

st.markdown("""
### Clinical Intelligence Simulator  
Not a chatbot. A cognition engine.

Built for:
- Consultant crisis simulation  
- PG viva mastery  
- Clinical reasoning refinement  
- MCQ and vignette assessment  
""")

st.markdown("---")

# ============================================================
# SIDEBAR – USER API KEY (BYOK SYSTEM)
# ============================================================

st.sidebar.title("🔑 Gemini API Key")

api_key = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password"
)

st.sidebar.markdown(
    "Get your free API key from: https://ai.google.dev/"
)

if not api_key:
    st.warning("Please enter your Gemini API key to continue.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Create stable model
model = genai.GenerativeModel("gemini-1.5-flash")

# ============================================================
# MODE SELECTION
# ============================================================

mode = st.selectbox(
    "Select Mode:",
    [
        "Consultant Rapid Mode",
        "PG Teaching Mode",
        "Reasoning Refinement Mode",
        "MCQ Generator Mode",
        "Clinical Vignette Mode"
    ]
)

clinical_input = st.text_area("Enter Clinical Scenario:", height=200)

# ============================================================
# SAFE GENERATION FUNCTION
# ============================================================

def generate_response(prompt):
    response = model.generate_content(
        contents=[{"role": "user", "parts": [prompt]}]
    )
    return response.text

# ============================================================
# CONSULTANT RAPID MODE
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
3. Drug dosing table
4. Red flags
5. Escalation ladder
"""

        with st.spinner("Analyzing scenario..."):
            output = generate_response(prompt)

        st.markdown(output)

# ============================================================
# PG TEACHING MODE
# ============================================================

elif mode == "PG Teaching Mode" and clinical_input:

    if "pg_questions" not in st.session_state:
        st.session_state.pg_questions = None
        st.session_state.pg_feedback = None

    if st.button("Start Viva Simulation"):

        prompt = f"""
Conduct postgraduate viva for this scenario:

{clinical_input}

Generate 3 structured probing questions only.
Do NOT provide answers.
"""

        st.session_state.pg_questions = generate_response(prompt)
        st.session_state.pg_feedback = None

    if st.session_state.pg_questions:
        st.markdown(st.session_state.pg_questions)

        pg_answer = st.text_area("Enter PG Answers Here:", height=200)

        if st.button("Evaluate PG Performance") and pg_answer:

            feedback_prompt = f"""
Scenario:
{clinical_input}

Questions:
{st.session_state.pg_questions}

PG Answers:
{pg_answer}

Evaluate performance.
Give:
- Strengths
- Gaps
- Score out of 10
"""

            st.session_state.pg_feedback = generate_response(feedback_prompt)

    if st.session_state.pg_feedback:
        st.markdown(st.session_state.pg_feedback)

# ============================================================
# REASONING REFINEMENT MODE
# ============================================================

elif mode == "Reasoning Refinement Mode":

    pg_answer = st.text_area("Paste PG Answer:", height=200)

    if clinical_input and pg_answer and st.button("Refine Answer"):

        prompt = f"""
Scenario:
{clinical_input}

PG Answer:
{pg_answer}

Evaluate strengths, reasoning gaps,
and rewrite to consultant level.
"""

        output = generate_response(prompt)
        st.markdown(output)

# ============================================================
# MCQ GENERATOR MODE
# ============================================================

elif mode == "MCQ Generator Mode" and clinical_input:

    if st.button("Generate 5 MCQs"):

        prompt = f"""
Create 5 high-quality single-best-answer MCQs.

Scenario:
{clinical_input}

Each must include:
- Question stem
- 4 options (A-D)
- Correct answer
- Explanation
"""

        output = generate_response(prompt)
        st.markdown(output)

# ============================================================
# CLINICAL VIGNETTE MODE
# ============================================================

elif mode == "Clinical Vignette Mode" and clinical_input:

    if "vignette_step" not in st.session_state:
        st.session_state.vignette_step = None
        st.session_state.vignette_feedback = None

    if st.button("Start Vignette Simulation"):

        prompt = f"""
Create an interactive clinical vignette
based on this scenario:

{clinical_input}

Present first step and ask:
"What would you do next?"

Do NOT reveal answer yet.
"""

        st.session_state.vignette_step = generate_response(prompt)
        st.session_state.vignette_feedback = None

    if st.session_state.vignette_step:
        st.markdown(st.session_state.vignette_step)

        user_response = st.text_area("Your Decision:", height=150)

        if st.button("Reveal Next Step") and user_response:

            feedback_prompt = f"""
Scenario:
{clinical_input}

Initial vignette:
{st.session_state.vignette_step}

User decision:
{user_response}

Now:
1. Evaluate user's choice
2. Provide expert reasoning
3. Continue vignette progression
"""

            st.session_state.vignette_feedback = generate_response(feedback_prompt)

    if st.session_state.vignette_feedback:
        st.markdown(st.session_state.vignette_feedback)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption("ASTRA™ | Educational Use Only | Does Not Replace Clinical Judgment")
