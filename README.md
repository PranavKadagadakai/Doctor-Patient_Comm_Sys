# 🩺 Doctor-Patient Communication System

An AI-powered healthcare platform to enhance doctor-patient interaction, improve medical communication, and provide intelligent assistance through cutting-edge NLP technologies.

---

## 📋 Overview

This system offers the following features:

- **Medical Report Summarization** using LLMs (e.g., BART, T5)
- **AI Medical Chatbot** for health-related queries
- **Doctor-Patient Messaging Interface** with secure real-time chat
- **Language Translation + TTS** for multilingual communication
- **Doctor Discussion Forum** for knowledge sharing
- **Medical History Tracker** for personalized timeline-based logging

---

## 🚀 Features

| Feature                      | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| Medical Report Summarization| Simplifies complex reports for patients using LLMs                         |
| AI Chatbot                  | Answers health queries using Hugging Face/Gemini                           |
| Secure Messaging            | Real-time chat between doctor and patient                                  |
| Language Translator + TTS   | Breaks language barriers with speech feedback                              |
| Doctors Forum               | Exclusive space for verified medical professionals                        |
| Medical History Tracker     | Chronological logging of symptoms, medications, diagnoses                  |

---

## 🛠️ Technology Stack

| Component        | Tech Stack                        |
|------------------|-----------------------------------|
| Backend          | Flask (Python)                    |
| LLM Integration  | Hugging Face Transformers, Gemini |
| Frontend         | HTML, CSS, Bootstrap              |
| DB               | SQLite / PostgreSQL / MongoDB     |
| TTS              | gTTS, pyttsx3                     |
| Auth             | JWT-based login & role management |

---

## 📦 Setup Instructions

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Doctor-Patient-Communication-System
```

2. **Ensure `requirements.txt` is present**

3. **Run the setup script**
```bash
chmod +x setup_project.sh
./setup_project.sh
```

This script will:
- Create a virtual environment
- Activate it
- Upgrade `pip`
- Install dependencies from `requirements.txt`

4. **Run the app**
```bash
flask run
```

---

## 🧪 Testing

- Unit Testing for summarization and chatbot logic
- Integration Testing for frontend-backend APIs
- User Acceptance Testing with real user flows
- Security Testing with JWT and role validation

---

## 🔄 Future Enhancements

- X-ray/MRI analysis using CNNs
- WebRTC-based voice chat
- Appointment system integration
- Push notifications (Twilio/Firebase)

---

## 👥 Team Roles

| Role              | Responsibility                        |
|-------------------|----------------------------------------|
| Backend Developer | API, Auth, DB                          |
| ML Engineer       | Model selection & deployment           |
| Frontend Developer| UI/UX implementation                   |
| QA Tester         | Testing and bug tracking               |
| DevOps Engineer   | Deployment, CI/CD                      |

---

## 📄 License

This project is for educational purposes and prototype development.

