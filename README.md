# 🎤 InterviewAI – Voice-Powered AI Mock Interview Platform

An AI-powered mock interview platform that simulates realistic technical interviews using Large Language Models (LLMs), voice interaction, resume-based questioning, and performance analytics.

Built to help students, software engineers, and AI professionals prepare for technical interviews through personalized, company-specific interview experiences.

---

## 🌐 Live Demo

**Application:** https://ai-voice-interviewer-pzefhizbrfhm97otf8ajpw.streamlit.app/

---

## 🚀 Features

### 🤖 AI-Powered Interview Questions

* Dynamic interview questions generated using Groq LLMs
* Company-specific interview preparation
* Role-based interview customization
* Difficulty-based question generation
* Non-repetitive question generation

Supported Companies:

* Google
* Amazon
* Microsoft
* Meta
* Netflix
* Apple
* General Interview Mode

Supported Roles:

* Software Engineer
* Machine Learning Engineer
* Data Scientist
* Frontend Developer
* Backend Developer

---

### 📄 Resume-Aware Interviewing

Upload your resume and receive:

* Project-specific questions
* Skill-based questions
* Resume-tailored technical discussions
* Personalized interview experience

Supported Format:

* PDF Resume Upload

---

### 🎙️ Voice Interview Experience

The platform supports a complete voice-based workflow:

* AI speaks interview questions
* User records verbal answers
* Audio is automatically transcribed
* Answer box is auto-filled
* AI evaluates responses

Technologies Used:

* Browser Speech Synthesis API
* Streamlit Mic Recorder
* OpenAI Whisper

---

### 📊 AI Interview Evaluation

Every answer is evaluated across multiple dimensions:

| Metric              | Description                                |
| ------------------- | ------------------------------------------ |
| Technical Knowledge | Understanding of concepts and technologies |
| Communication       | Clarity and explanation quality            |
| Problem Solving     | Analytical and logical thinking            |
| Confidence          | Confidence and delivery quality            |
| Overall Score       | Final interview performance score          |

---

### 📈 Performance Dashboard

Track your progress with:

* Average Score
* Best Score
* Latest Score
* Score Trend Graph
* Score Distribution Chart
* Interview Progress Tracking
* Completion Percentage

---

### 📚 Interview History

View complete interview history including:

* Question Asked
* Candidate Response
* AI Evaluation
* Individual Score

---

### 📄 PDF Interview Report

Generate downloadable PDF reports containing:

* Interview Questions
* Candidate Answers
* Detailed Evaluations
* Individual Scores
* Final Summary
* Overall Performance Metrics

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ├── Resume Upload
 │
 ├── Voice Recording
 │
 ├── Text Input
 │
 ▼
Application Layer
 │
 ├── Question Generator
 │
 ├── Resume Parser
 │
 ├── Speech To Text
 │
 ├── Answer Evaluation
 │
 └── Report Generator
 │
 ▼
Groq LLM
 │
 ├── Interview Question Generation
 │
 └── Answer Evaluation
 │
 ▼
Analytics Engine
 │
 ├── Technical Score
 │
 ├── Communication Score
 │
 ├── Problem Solving Score
 │
 ├── Confidence Score
 │
 └── Overall Score
 │
 ▼
PDF Report Export
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### AI & LLM

* Groq API
* Llama 3.3 70B Versatile

### Speech Processing

* OpenAI Whisper
* Browser Speech Synthesis API
* streamlit-mic-recorder

### Resume Processing

* PyMuPDF (fitz)

### Analytics

* Pandas
* Altair

### PDF Generation

* ReportLab

### Deployment

* Streamlit Community Cloud

---

## 📂 Project Structure

```text
AI-Voice-Interviewer/
│
├── app.py
│
├── utils/
│   ├── question_generator.py
│   ├── evaluator.py
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── resume_parser.py
│   └── pdf_generator.py
│
├── requirements.txt
├── .env
├── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Voice-Interviewer.git

cd AI-Voice-Interviewer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your free Groq API Key:

https://console.groq.com/

---

## ▶️ Run Application

```bash
streamlit run app.py
```

## 🎯 Future Enhancements

Planned improvements:

* Multi-language interviews
* Video interview support
* AI-generated interview feedback reports
* Interview replay functionality
* Interview difficulty adaptation
* ATS Resume Analysis
* Real-time sentiment analysis
* Company-specific interview datasets
* Leaderboards and progress tracking
* Interview performance benchmarking

---

## 👨‍💻 About the Creator

### Shubh Beniwal

AI Engineer | Software Developer

VIT Chennai Graduate

Passionate about:

* Artificial Intelligence
* Large Language Models (LLMs)
* Natural Language Processing
* Machine Learning
* Software Engineering

### Connect With Me

LinkedIn:
https://www.linkedin.com/in/shubh-beniwal/

GitHub:
https://github.com/shubhbeniwal

Email:
[beniwal.shubh2003@gmail.com](mailto:beniwal.shubh2003@gmail.com)

---

## ⭐ Support

If you found this project useful:

* Star the repository
* Fork the repository
* Share it with others
* Connect with me on LinkedIn


Built with ❤️ using Streamlit, Groq, Whisper, Python, and AI.
