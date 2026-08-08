# 🤖 AI Interview Coach

### Personalised AI-Powered Interview Preparation System

AI Interview Coach is a personalised interview preparation platform that acts like a **personal AI tutor** for students and job seekers.

Instead of providing generic interview questions, the system analyses the user's profile, resume, uploaded documents, knowledge level, and previous performance to create an adaptive preparation experience.

> **Learn → Practice → Evaluate → Improve → Repeat**

---

## 🎯 Project Objective

The goal of this project is to build a simple and user-friendly AI interview preparation system that can:

* Understand a candidate's background and target role
* Analyse resumes and uploaded documents
* Assess the candidate's current knowledge
* Identify strengths and weaknesses
* Provide personalised learning
* Conduct text and voice mock interviews
* Analyse communication and interview behaviour
* Recommend what the candidate should improve next

The complexity stays behind the scenes so that the user gets a **simple and clean experience**.

---

# 🚀 User Flow

```text
                    ┌──────────────┐
                    │   Open App   │
                    └──────┬───────┘
                           ↓
                  ┌─────────────────┐
                  │ Basic Profile  │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ Upload Resume   │
                  │ & Documents     │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ Select Target   │
                  │ Job / Company   │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ AI Assessment   │
                  │ 5–10 Questions  │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ Personalised    │
                  │ Learning Plan   │
                  └───────┬─────────┘
                          ↓
              ┌───────────┴────────────┐
              ↓                        ↓
      ┌───────────────┐        ┌────────────────┐
      │ Learn &       │        │ Mock Interview │
      │ Practice      │        │ Text / Voice   │
      └───────┬───────┘        └───────┬────────┘
              ↓                        ↓
              └───────────┬────────────┘
                          ↓
                  ┌─────────────────┐
                  │ AI Evaluation   │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ Weaknesses &    │
                  │ Improvements    │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ Update Progress │
                  └───────┬─────────┘
                          ↓
                  ┌─────────────────┐
                  │ Next AI         │
                  │ Recommendation  │
                  └─────────────────┘
```

---

# 🧠 System Architecture

```text
                         ┌───────────────────┐
                         │       USER        │
                         └─────────┬─────────┘
                                   │
                                   ↓
                         ┌───────────────────┐
                         │   React Frontend  │
                         │                   │
                         │ Dashboard         │
                         │ Learning          │
                         │ Mock Interview    │
                         │ Voice Interview   │
                         │ Progress          │
                         └─────────┬─────────┘
                                   │
                              REST API
                                   │
                                   ↓
                         ┌───────────────────┐
                         │   FastAPI Backend │
                         └─────────┬─────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 ↓                 ↓                 ↓
        ┌────────────────┐ ┌───────────────┐ ┌───────────────┐
        │   AI Coach     │ │ RAG Pipeline  │ │ SQLite DB     │
        │     Agent      │ │               │ │               │
        └───────┬────────┘ └───────┬───────┘ └───────────────┘
                │                  │
                ↓                  ↓
        ┌────────────────┐  ┌────────────────┐
        │ LLM Provider   │  │ FAISS Vector   │
        │                │  │ Database       │
        └────────────────┘  └────────────────┘
                │
                ↓
        ┌────────────────────────┐
        │ Personalised Learning  │
        │ & Interview Feedback   │
        └────────────────────────┘
```

---

# 🤖 AI Coach

The **AI Coach** is the central intelligence of the system.

It uses:

* Candidate profile
* Resume
* Uploaded documents
* Assessment results
* Previous learning performance
* Interview performance
* Weak topics
* Target job role

The AI Coach decides what the student should do next.

For example:

> "You struggled with SQL JOINs in your previous session. Let's spend the next 15 minutes improving that before your next mock interview."

---

# 📄 Document Intelligence & RAG

Users can upload:

* Resume
* Project documents
* Certificates
* Notes
* Job descriptions
* Study material

The documents are processed through:

```text
Document
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
FAISS
   ↓
Relevant Context Retrieval
   ↓
AI Coach
```

This allows the AI to ask questions based on the **candidate's actual documents** instead of generating completely generic questions.

---

# 🎯 Personalised Assessment

During onboarding, the AI conducts a short assessment.

The questions adapt according to the user's answers.

```text
Correct Answer
      ↓
Increase Difficulty

Incorrect Answer
      ↓
Test Fundamentals
```

The assessment identifies:

* Strong topics
* Weak topics
* Knowledge level
* Areas requiring improvement

The results are then used to create a personalised preparation plan.

---

# 📚 Learning System

The learning experience follows a simple tutor-like approach:

```text
Teach
 ↓
Explain
 ↓
Example
 ↓
Ask
 ↓
Evaluate
 ↓
Identify Weakness
 ↓
Re-teach
 ↓
Practice
 ↓
Re-test
```

This allows the AI to adapt the learning experience according to the student's performance.

---

# 🎤 Mock Interview

The system provides multiple interview modes:

### HR Interview

Behavioural and general interview questions.

### Technical Interview

Questions based on the candidate's target role and skills.

### Resume / Project Interview

Questions generated from the candidate's own resume and projects.

### Voice Interview

The candidate can answer questions using their microphone.

```text
AI asks question
      ↓
Candidate speaks
      ↓
Speech-to-Text
      ↓
AI evaluates answer
      ↓
Next question
```

---

# 📊 Interview Feedback

After the interview, the system provides feedback such as:

```text
Interview Score: 78%

Technical Knowledge    82%
Communication          75%
Confidence             70%

Strengths
✓ Good technical understanding
✓ Good project explanation

Improve
• Answers are too long
• Weak SQL joins
• Improve answer structure

Communication
• Reduce "like"
• Reduce "basically"
• Reduce unnecessary repetition
• Avoid excessive slang

Next Focus
→ SQL Joins
→ Communication Practice
```

The goal is not only to test the candidate but to **help them become better at interviewing**.

---

# 🧠 Personalised Progress

The system stores previous performance.

Example:

```text
SQL

Session 1 → 50%
Session 2 → 68%
Session 3 → 84%
```

The AI uses this history to determine:

* What the student has mastered
* What still needs revision
* What should be practised next

---

# ✨ Key Features

* 🤖 Personal AI Coach
* 📄 Resume Analysis
* 📚 Document Upload
* 🔎 RAG-based Document Retrieval
* 🧠 Adaptive Skill Assessment
* 🎯 Personalised Learning Plan
* 📖 AI Teaching Sessions
* 💻 Interview Practice
* 🎤 Voice Mock Interviews
* 📊 Interview Evaluation
* 🗣️ Communication Analysis
* 🔥 Weakness Detection
* 📈 Progress Tracking
* 💡 Daily Motivational Quotes
* 🎯 Next-step Recommendations

---

# 🛠️ Technology Stack

### Frontend

* React
* TypeScript
* CSS / Tailwind CSS

### Backend

* Python
* FastAPI

### AI

* LLM API
* LangGraph

### RAG

* Embeddings
* FAISS

### Database

* SQLite

### Voice

* Browser Microphone API
* Speech-to-Text
* Text-to-Speech

---

# 📁 Project Structure

```text
ai-interview-coach/
│
├── frontend/
│
├── backend/
│   ├── agents/
│   ├── rag/
│   ├── services/
│   ├── models/
│   ├── database/
│   └── main.py
│
├── uploads/
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 🔐 Security

* API keys stored in environment variables
* API keys never exposed to frontend
* Uploaded files validated
* Backend input validation
* User data stored locally in the application database

---

# 🚀 Future Improvements

Possible future additions:

* Real-time conversational voice interviews
* Company-specific interview preparation
* Coding platform integration
* Advanced communication analysis
* Interview readiness prediction
* More personalised memory
* Mobile application
* Multi-language interview support

---

# 🎓 Capstone Project

**Project:** Personalised AI Interview Preparation System

**Concept:** Agentic AI + RAG + Adaptive Learning + Voice Interview

### Core Idea

> **An AI coach that understands the candidate, identifies their weaknesses, teaches them, evaluates their interview performance, and continuously adapts their preparation journey.**

---

## ⭐ Project Philosophy

**Keep the user experience simple.**

The student should only see:

```text
What should I learn?
        ↓
What should I practice?
        ↓
How am I performing?
        ↓
What should I improve next?
```

The AI handles the complexity behind the scenes.
