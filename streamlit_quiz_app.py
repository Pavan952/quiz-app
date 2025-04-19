# streamlit_quiz_app.py
import streamlit as st
import google.generativeai as genai
import json
import time
import random

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

st.title("🎓 Smart Quiz Generator")

# Input fields
student_class = st.selectbox("Select your class", [str(i) for i in range(6, 13)], index=3)
subject = st.text_input("Enter subject", "Physics")
topic = st.text_input("Enter topic", "Force")
question_type = st.selectbox("Select question type", ["MCQ", "True/False", "Fill in the Blanks"])
time_limit = st.number_input("Time limit per question (in seconds)", min_value=0, value=0)
mode = st.selectbox("Mode", ["Practice", "Test"])
num_questions = st.slider("Number of questions", 1, 20, 10)

difficulty = "Medium"
if mode == "Test":
    difficulty = st.selectbox("Set difficulty", ["Easy", "Medium", "Hard"], index=1)

if st.button("Generate Quiz"):
    with st.spinner("Generating questions..."):
        prompt = f"""
        Generate {num_questions} {question_type} questions for Class {student_class} students on the topic "{topic}" in {subject}.
        Use {difficulty} difficulty.
        Return each question in this format:
        {{
            "question": "...",
            "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
            "answer": "A",
            "explanation": "...",
            "hint": "...",
            "image": "link_to_image_if_needed"
        }}
        Use JSON format only.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"): text = text[7:]
        if text.endswith("```"): text = text[:-3]

        try:
            questions = json.loads(text)
            st.session_state.questions = questions
            st.session_state.current = 0
            st.session_state.score = 0
        except Exception as e:
            st.error(f"Failed to parse questions: {e}")
