import streamlit as st
import google.generativeai as genai
import os

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ASTRA",
    page_icon="🩺",
    layout="wide"
)

# ============================================================
# NEON STYLE
# ============================================================

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #050d1a, #0c1a2e);
    color: white;
}
h1 {
    color: #00f7ff;
    text-shadow: 0 0 10px #00f7ff;
}
h2, h3 {
    color: #ff00c8;
}
.stButton button {
    background: linear-gradient(135deg, #00f7ff, #008cff);
    border-radius: 10px;
    font-weight: bold;
    color: black;
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
st.subheader("AI-Supported Structured Thinking in Anaesthesia")
st.markdown("### Excellence in Clinical Cognition")

st.markdown("---")

# ============================================================
# DEVELOPER SECTION
# ============================================================

with st.expander("About the Developer - Dr Bhavna Gupta"):

    st.markdown("""
**Associate Professor – Anaesthesiology**

• 175+ Peer-Reviewed Publications  
• 15+ Book Chapters  
• Author of 2 Textbooks  
• National Young Researcher Awardee  
• Dr KPR Award Recipient  
• Prof PK Singh Young Anaesthesiologist Awardee  
• National Essay Competition Winner  

**Vision:**  
ASTRA bridges traditional clinical wisdom with structured AI reasoning.
The aim is not automation — but elevation of clinical cognition.
""")

st.markdown("---")

# ============================================================
# API KEY
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key not found. Please set GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ============================================================
# SAFE MODEL FUNCTION WITH FALLBACK
# ============================================================

def generate_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        try:
            fallback_model = genai.GenerativeModel("gemini-1.5-flash")
            response = fallback_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error occurred: {str(e)}"

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

clinical_input = st.text_area("Enter Clinical Scenario:", height=180)

# ============================================================
# CONSULTANT MODE
# ============================================================

if mode == "Consultant Rapid Mode" and clinical_input:

    if st.button("Generate Consultant Plan"):

        prompt = f"""
Senior consultant anaesthesiologist perspective.

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
# PG TEACHING MODE (WITH ANSWER BOX)
# ============================================================

elif mode == "PG Teaching Mode" and clinical_input:

    if st.button("Start Viva Simulation"):

        prompt = f"""
Conduct postgraduate viva.

Scenario:
{clinical_input}

Generate 3 structured probing questions only.
"""

        with st.spinner("Preparing viva..."):
            output = generate_response(prompt)

        st.markdown(output)

        pg_answer = st.text_area("Enter PG Answers Here:")

        if st.button("Evaluate PG Answers"):

            eval_prompt = f"""
Scenario:
{clinical_input}

PG Answers:
{pg_answer}

Evaluate and score out of 10 with feedback.
"""

            result = generate_response(eval_prompt)
            st.markdown(result)

# ============================================================
# REFINEMENT MODE
# ============================================================

elif mode == "Reasoning Refinement Mode":

    pg_answer = st.text_area("Paste PG Answer:", height=180)

    if clinical_input and pg_answer and st.button("Refine Answer"):

        prompt = f"""
Scenario:
{clinical_input}

PG Answer:
{pg_answer}

Evaluate strengths, reasoning gaps, and rewrite to consultant level.
"""

        with st.spinner("Refining answer..."):
            output = generate_response(prompt)

        st.markdown(output)

# ============================================================
# MCQ MODE
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

        with st.spinner("Generating MCQs..."):
            output = generate_response(prompt)

        st.markdown(output)

# ============================================================
# CLINICAL VIGNETTE MODE (WITH ANSWER BOX)
# ============================================================

elif mode == "Clinical Vignette Mode" and clinical_input:

    if st.button("Start Vignette Simulation"):

        prompt = f"""
Create an interactive clinical vignette.

Scenario:
{clinical_input}

End by asking: What would you do next?
"""

        with st.spinner("Simulating clinical pathway..."):
            output = generate_response(prompt)

        st.markdown(output)

        user_answer = st.text_area("Your Clinical Decision:")

        if st.button("Reveal Analysis"):

            analysis_prompt = f"""
Scenario:
{clinical_input}

User Decision:
{user_answer}

Provide structured feedback and consultant-level reasoning.
"""

            result = generate_response(analysis_prompt)
            st.markdown(result)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
ASTRA™ | AI Clinical Intelligence Engine  
Educational Use Only | Does not replace clinical judgement
</div>
""", unsafe_allow_html=True)
