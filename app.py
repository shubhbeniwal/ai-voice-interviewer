import streamlit as st
import re
import tempfile

from utils.question_generator import generate_question
from utils.evaluator import evaluate_answer
from streamlit_mic_recorder import mic_recorder
from utils.speech_to_text import transcribe_audio
from utils.text_to_speech import speak


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Voice Interviewer",
    page_icon="🎤",
    layout="wide"
)


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

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "pending_speech" not in st.session_state:
    st.session_state.pending_speech = None
    
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

if "processing_audio" not in st.session_state:
    st.session_state.processing_audio = False


MAX_QUESTIONS = 5


# ---------------- SCORE EXTRACTION ----------------
def extract_score(text):
    match = re.search(r"Score:\s*(\d+)", text)
    return int(match.group(1)) if match else 0


# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 About the Creator")

st.sidebar.markdown("""
### Shubh Beniwal

AI Engineer | Software Developer  
VIT Chennai Graduate  

Passionate about AI, LLMs, NLP, and Software Engineering
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
# 🎤 AI Voice Interviewer

Practice realistic AI-powered interviews with voice interaction, speech-to-text, and performance analytics.
""")


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


# ---------------- GENERATE QUESTION ----------------
if st.button("Generate Question"):

    with st.spinner("Generating question..."):
        question = generate_question(role, difficulty)

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

    audio_hash = len(audio["bytes"]) if audio else None

    # ---------------- SPEECH TO TEXT (FIXED LOOP ISSUE) ----------------
    if (
        audio
        and audio_hash != st.session_state.last_audio_hash
        and not st.session_state.processing_audio
    ):

        st.session_state.processing_audio = True
        st.session_state.last_audio_hash = audio_hash

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            temp_audio.write(audio["bytes"])
            audio_path = temp_audio.name

        with st.spinner("Transcribing audio..."):
            spoken_text = transcribe_audio(audio_path)

        st.session_state.voice_text = spoken_text

        st.session_state.processing_audio = False
        st.rerun()

    # ---------------- ANSWER INPUT ----------------
    answer = st.text_area(
        "Your Answer",
        value=st.session_state.voice_text,
        height=150,
        key=f"answer_{len(st.session_state.answers)}"
    )

    # ---------------- NEXT QUESTION ----------------
    if st.button("Next Question"):

        if answer.strip():

            evaluation = evaluate_answer(
                st.session_state.current_question,
                answer
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
            st.session_state.voice_text = ""

            # NEXT QUESTION LOGIC
            if len(st.session_state.answers) < MAX_QUESTIONS:

                with st.spinner("Generating next question..."):
                    next_question = generate_question(role, difficulty)

                st.session_state.current_question = next_question

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


# ---------------- DASHBOARD ----------------
st.markdown("---")
st.header("📊 Performance Dashboard")

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
                "Built with Streamlit, Whisper, Groq LLMs and Python"
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