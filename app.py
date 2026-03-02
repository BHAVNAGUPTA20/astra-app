import streamlit as st
from google import genai

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
    text-shadow: 0 0 10px #00f7ff, 0 0 20px #00f7ff;
}

h2, h3 {
    color: #ff00c8;
    text-shadow: 0 0 6px #ff00c8;
}

.stButton button {
    background: linear-gradient(135deg, #00f7ff, #008cff);
    border-radius: 12px;
    font-weight: bold;
    color: black;
}

.stTextArea textarea, .stTextInput input {
    background-color: #0b1b33;
    color: white;
    border-radius: 12px;
    border: 1px solid #00f7ff;
}

.footer {
    text-align:center;
    margin-top:50px;
    font-size:0.8rem;
    color:#94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.title("🩺 ASTRA")
st.subheader("AI-Supported Structured Thinking & Reasoning in Anaesthesia")
st.markdown("### eXcellence in Clinical Cognition")

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
# DEVELOPER SECTION
# ============================================================

with st.expander("About the Developer - Dr Bhavna Gupta"):

    st.markdown("""
### Dr Bhavna Gupta  
Associate Professor - Anaesthesiology  

Research Mentor | AI in Medical Education Advocate | Academic Strategist  

---

#### Academic Impact
- 175+ Peer-Reviewed Publications  
- 15+ Book Chapters  
- Author of 2 Textbooks in Anaesthesia  
- Active Research Mentor  

---

#### National Recognition
- National Young Researcher Awardee  
- Dr KPR Award Recipient  
- Prof PK Singh Young Anaesthesiologist Awardee  
- National Best Essay Competition Winner  

---

#### Academic Leadership
- Faculty on Artificial Intelligence in Medical Research  
- Advocate for Ethical AI Integration  
- Mentor in Structured Clinical Reasoning  

---

#### Vision Behind ASTRA
ASTRA bridges traditional clinical wisdom with structured artificial intelligence reasoning.

Built on:
1. Structured Thinking  
2. Ethical AI Use  
3. Consultant-Level Precision  

The aim is not automation - but elevation of clinical cognition.
""")

st.markdown("---")

# ============================================================
# API KEY
# ============================================================

st.sidebar.title("Gemini API Key")
api_key = st.sidebar.text_input("Enter API Key", type="password")

if not api_key:
    st.info("Enter your Gemini API key to begin.")
    st.stop()

client = genai.Client(api_key=api_key)

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
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

        st.markdown(response.text)

# ============================================================
# PG TEACHING MODE
# ============================================================

elif mode == "PG Teaching Mode" and clinical_input:

    if st.button("Start Viva Simulation"):

        prompt = f"""
Conduct postgraduate viva.

Scenario:
{clinical_input}

Generate 3 structured probing questions.
After PG answers, provide score out of 10.
"""

        with st.spinner("Preparing viva..."):
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

        st.markdown(response.text)

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
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

        st.markdown(response.text)

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
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

        st.markdown(response.text)

# ============================================================
# VIGNETTE MODE
# ============================================================

elif mode == "Clinical Vignette Mode" and clinical_input:

    if st.button("Start Vignette Simulation"):

        prompt = f"""
Create interactive clinical vignette.

Scenario:
{clinical_input}

Pause after each step asking:
"What would you do next?"

Reveal reasoning progressively.
"""

        with st.spinner("Simulating clinical pathway..."):
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

        st.markdown(response.text)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
ASTRA - AI Clinical Intelligence Engine  
Educational Use Only | Does not replace clinical judgement
</div>
""", unsafe_allow_html=True)