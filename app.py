import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ASTRA", page_icon="🧠")

st.title("🧠 ASTRA – Anaesthesia Smart Teaching & Research Assistant")

# API KEY
api_key = st.text_input("Enter Gemini API Key", type="password")

if api_key:

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    mode = st.selectbox(
        "Choose Mode",
        [
            "Consultant Mode",
            "Resident Teaching Mode",
            "Secure Prompt Generator",
            "Clinical Widget"
        ]
    )

    user_input = st.text_area("Enter your query")

    if st.button("Generate Response"):

        if mode == "Consultant Mode":

            prompt = f"""
            You are a senior consultant anaesthesiologist.
            Provide a concise clinical decision answer.

            Question:
            {user_input}
            """

        elif mode == "Resident Teaching Mode":

            prompt = f"""
            You are teaching an anaesthesia resident.

            Explain stepwise with:
            - Key concepts
            - Clinical pearls
            - Viva points

            Topic:
            {user_input}
            """

        elif mode == "Secure Prompt Generator":

            prompt = f"""
            Convert this clinical question into a safe structured prompt:

            {user_input}
            """

        elif mode == "Clinical Widget":

            prompt = f"""
            Provide quick clinical reference points for:

            {user_input}

            Format:
            - Definition
            - Key facts
            - Clinical relevance
            """

        response = model.generate_content(prompt)

        st.markdown("### Response")
        st.write(response.text)

else:
    st.info("Enter your Gemini API key to start.")
