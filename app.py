import streamlit as st
import re
import tempfile

from utils.question_generator import generate_question
from utils.evaluator import evaluate_answer
from streamlit_mic_recorder import mic_recorder
from utils.speech_to_text import transcribe_audio
from utils.text_to_speech import speak
from utils.pdf_report import generate_pdf_report


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="InterviewAI – Voice-Powered AI Mock Interview Platform",
    page_icon="🎤",
    layout="wide"
)

st.markdown("""
<style>
button {
    border-radius: 10px !important;
}

button[kind="secondary"] {
    border: 1px solid #4a4a4a !important;
    padding: 0.5rem 1rem !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE INIT ----------------
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "answers" not in st.session_state:
    st.session_state.answers = []

if "evaluations" not in st.session_state:
    st.session_state.evaluations = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "technical_scores" not in st.session_state:
    st.session_state.technical_scores = []

if "communication_scores" not in st.session_state:
    st.session_state.communication_scores = []

if "problem_solving_scores" not in st.session_state:
    st.session_state.problem_solving_scores = []

if "confidence_scores" not in st.session_state:
    st.session_state.confidence_scores = []
    
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "pending_speech" not in st.session_state:
    st.session_state.pending_speech = None

if "answer_key" not in st.session_state:
    st.session_state.answer_key = 0


MAX_QUESTIONS = 5


# ---------------- SCORE EXTRACTION ----------------
def extract_score(text):
    match = re.search(
        r"Overall Score:\s*(\d+)",
        text
    )
    return int(match.group(1)) if match else 0

def get_metric(text, metric):

        match = re.search(
            rf"{metric}:\s*(\d+)",
            text
        )

        if match:
            return int(match.group(1))

        return 0


# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
# 🚀 About the Creator

### Shubh Beniwal

AI Engineer | Software Developer

VIT Chennai Graduate

Passionate about:
- Artificial Intelligence
- Large Language Models
- NLP
- Software Engineering

📍 Bengaluru, Karnataka

📧 beniwal.shubh2003@gmail.com

🔗 LinkedIn:
https://www.linkedin.com/in/shubh-beniwal/

💻 GitHub:
https://github.com/shubhbeniwal
""")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Session Stats")

st.sidebar.metric(
    "Questions Answered",
    len(st.session_state.get("answers", []))
)

if st.session_state.get("scores"):
    st.sidebar.metric(
        "Average Score",
        round(
            sum(st.session_state.scores) / len(st.session_state.scores),
            2
        )
    )


# ---------------- HEADER ----------------
st.markdown("""
# 🎤 InterviewAI – Voice-Powered AI Mock Interview Platform

### Practice Real AI Interviews with Voice Interaction

Get company-specific interview questions, answer using your voice, receive AI-powered feedback, and track your interview performance.

---

✅ Voice-Based Interviews

✅ Resume-Aware Question Generation

✅ Company-Specific Mock Interviews

✅ Real-Time AI Evaluation

✅ Downloadable PDF Reports

---
""")

st.info(
    "🚀 Powered by Groq + Llama 3.3 + Whisper AI"
)


# ---------------- PROGRESS ----------------
progress = min(len(st.session_state.answers), MAX_QUESTIONS)

st.progress(progress / MAX_QUESTIONS)

st.write(f"Interview Progress: {progress}/{MAX_QUESTIONS}")

completion_percentage = int((progress / MAX_QUESTIONS) * 100)

st.write(f"Completion: {completion_percentage}%")

if progress == 0:
    st.info("🟡 Interview Not Started")
elif progress < MAX_QUESTIONS:
    st.warning("🟠 Interview In Progress")
else:
    st.success("🟢 Interview Completed")


# ---------------- SETTINGS ----------------
role = st.selectbox(
    "Select Role",
    [
        "Software Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Frontend Developer",
        "Backend Developer"
    ]
)

difficulty = st.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

company = st.selectbox(
    "Target Company",
    [
        "General",
        "Google",
        "Amazon",
        "Microsoft",
        "Meta",
        "Netflix",
        "Apple"
    ]
)

uploaded_resume = st.file_uploader(
    "📄 Upload Resume (Optional)",
    type=["pdf"]
)

from utils.resume_parser import extract_resume_text

resume_text = ""

if uploaded_resume:

    resume_text = extract_resume_text(
        uploaded_resume
    )

# ---------------- GENERATE QUESTION ----------------
if st.button("Generate Question"):

    with st.spinner("Generating question..."):
        question = generate_question(
            role,
            difficulty,
            company,
            resume_text,
            st.session_state.questions
        )

    st.session_state.current_question = question
    st.session_state.questions.append(question)

    # IMPORTANT: only queue speech (no direct speak)
    st.session_state.pending_speech = question

    st.rerun()


# ---------------- SHOW QUESTION + RECORDING ----------------
if st.session_state.current_question:

    st.subheader("Interview Question")

    st.info(st.session_state.current_question)

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key=f"mic_{len(st.session_state.answers)}"
    )


# ---------------- SPEECH TO TEXT ----------------
    if audio is not None and isinstance(audio, dict) and "bytes" in audio:

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".webm"
            ) as temp_audio:

                temp_audio.write(audio["bytes"])
                audio_path = temp_audio.name

            with st.spinner("Transcribing audio..."):
                spoken_text = transcribe_audio(audio_path)

            st.success("🎤 Voice converted to text!")

            st.session_state.voice_text = spoken_text

            st.session_state[
                f"answer_text_{st.session_state.answer_key}"
            ] = spoken_text

        except Exception as e:
            st.error(f"Transcription Error: {e}")
    # ---------------- ANSWER INPUT ----------------
    answer = st.text_area(
        "Your Answer",
        height=150,
        key=f"answer_text_{st.session_state.answer_key}"
    )

    # ---------------- NEXT QUESTION ----------------
    if st.button("Next Question"):

        if answer.strip():

            evaluation = evaluate_answer(
                st.session_state.current_question,
                answer
            )
            
            technical = get_metric(
                evaluation,
                "Technical Knowledge"
            )

            communication = get_metric(
                evaluation,
                "Communication"
            )

            problem_solving = get_metric(
                evaluation,
                "Problem Solving"
            )

            confidence = get_metric(
                evaluation,
                "Confidence"
            )
            
            st.session_state.technical_scores.append(
                technical
            )

            st.session_state.communication_scores.append(
                communication
            )

            st.session_state.problem_solving_scores.append(
                problem_solving
            )

            st.session_state.confidence_scores.append(
                confidence
            )

            st.session_state.answers.append(answer)
            st.session_state.evaluations.append(evaluation)

            score = extract_score(evaluation)
            st.session_state.scores.append(score)

            st.session_state.history.append({
                "question": st.session_state.current_question,
                "answer": answer,
                "evaluation": evaluation,
                "score": score
            })
            
            # reset input cleanly
            pass

            # NEXT QUESTION LOGIC
            if len(st.session_state.answers) < MAX_QUESTIONS:

                with st.spinner("Generating next question..."):
                    next_question = generate_question(
                        role,
                        difficulty,
                        company,
                        resume_text,
                        st.session_state.questions
                    )

                st.success(next_question)
                st.session_state.current_question = next_question
                st.session_state.questions.append(next_question)
                st.session_state.answer_key += 1

                # FIX: queue speech instead of direct speak()
                st.session_state.pending_speech = next_question

            else:
                st.session_state.current_question = ""
                st.session_state.pending_speech = None

            st.rerun()


# ---------------- LATEST EVALUATION ----------------
if st.session_state.evaluations:

    st.subheader("Latest Evaluation")

    st.success(st.session_state.evaluations[-1])


# ---------------- FINAL SUMMARY ----------------
if len(st.session_state.answers) >= MAX_QUESTIONS:

    st.success("🎉 Interview Completed!")
    st.balloons()

    st.header("🏆 Final Interview Summary")

    st.write(f"Total Questions: {MAX_QUESTIONS}")

    st.write(
        f"Average Score: {round(sum(st.session_state.scores) / len(st.session_state.scores), 2)}"
    )

    st.write(f"Best Score: {max(st.session_state.scores)}")
    
    pdf_file = f"{company}_{role}_Interview_Report.pdf"

    generate_pdf_report(
        pdf_file,
        role,
        company,
        difficulty,
        st.session_state.history,
        round(
            sum(st.session_state.scores)
            /
            len(st.session_state.scores),
            2
        ),
        max(st.session_state.scores)
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name=pdf_file,
            mime="application/pdf"
        )
        
        # ---------------- REPORT GENERATION ----------------

    report_text = f"""
AI VOICE INTERVIEW REPORT

Role: {role}
Company: {company}
Difficulty: {difficulty}

========================================
"""

    for i, item in enumerate(st.session_state.history, start=1):

        report_text += f"""

Question {i}
----------------------------------------

Question:
{item['question']}

Answer:
{item['answer']}

Evaluation:
{item['evaluation']}

Score:
{item['score']}
"""

    report_text += f"""

========================================

FINAL SUMMARY

Total Questions:
{MAX_QUESTIONS}

Average Score:
{round(sum(st.session_state.scores) / len(st.session_state.scores), 2)}

Best Score:
{max(st.session_state.scores)}

========================================
"""

# ---------------- DASHBOARD ----------------
st.markdown("---")
st.header("📊 Performance Dashboard")
st.markdown("---")
st.header("📈 Interview Analytics")
if st.session_state.technical_scores:

    avg_technical = round(
        sum(st.session_state.technical_scores)
        /
        len(st.session_state.technical_scores),
        2
    )

    avg_communication = round(
        sum(st.session_state.communication_scores)
        /
        len(st.session_state.communication_scores),
        2
    )

    avg_problem_solving = round(
        sum(st.session_state.problem_solving_scores)
        /
        len(st.session_state.problem_solving_scores),
        2
    )

    avg_confidence = round(
        sum(st.session_state.confidence_scores)
        /
        len(st.session_state.confidence_scores),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Technical", avg_technical)

    with col2:
        st.metric("Communication", avg_communication)

    with col3:
        st.metric("Problem Solving", avg_problem_solving)

    with col4:
        st.metric("Confidence", avg_confidence)
        
if st.session_state.scores:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Score",
            round(sum(st.session_state.scores) / len(st.session_state.scores), 2)
        )

    with col2:
        st.metric("Best Score", max(st.session_state.scores))

    with col3:
        st.metric("Latest Score", st.session_state.scores[-1])

    st.subheader("📈 Score Trend")
    st.line_chart(st.session_state.scores)

    st.subheader("📊 Score Distribution")
    st.bar_chart(st.session_state.scores)

    st.subheader("Score Progress")
    st.line_chart(st.session_state.scores)

    # ---------------- HISTORY (NO SIDE EFFECTS INSIDE) ----------------
    st.markdown("---")
    st.header("📚 Interview History")

    for i, item in enumerate(reversed(st.session_state.history)):

        with st.expander(f"Question {len(st.session_state.history) - i}"):

            st.write("**Question:**", item["question"])
            st.write("**Answer:**", item["answer"])
            st.write("**Evaluation:**", item["evaluation"])
            st.write(f"**Score:** {item['score']}")

            st.markdown("---")

            st.caption(
                "🚀 About the Creator — Shubh Beniwal, AI Engineer | Software Developer, VIT Chennai Graduate | Passionate about AI, LLMs, NLP, and Software Engineering."
            )


# ---------------- SYNCHRONIZED SPEECH (GLOBAL SAFE ZONE) ----------------
if st.session_state.pending_speech:

    st.components.v1.html(f"""
        <script>
            window.speechSynthesis.cancel();

            setTimeout(() => {{
                var msg = new SpeechSynthesisUtterance("{st.session_state.pending_speech}");
                msg.rate = 1;
                msg.pitch = 1;
                window.speechSynthesis.speak(msg);
            }}, 400);
        </script>
    """, height=0)

    st.session_state.pending_speech = None
