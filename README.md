# 🗂️ AI Job Application Tracker

> A full-stack AI-powered job application tracker — track every application, analyze your resume against any job description, and get back a verdict with missing skills, suggested keywords, and interview prep topics.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat&logo=openai&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat&logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## ✨ Features

- 🔐 User registration & login with **JWT authentication**
- 📋 Create, edit, delete job applications
- 🎯 Track status: **Saved → Applied → Interview → Offer / Rejected**
- 🗃️ Store job description, resume version, notes, deadline, and job link
- 📊 **Kanban board** with drag-and-drop between stages
- 🔍 Table view with search and status filters
- 🤖 **AI Resume Analyzer** — paste your resume + job description and get:
  - ✅ Match verdict (Strong Match / Partial Match / Needs Work)
  - 📌 Missing skills
  - 🔑 Suggested keywords to add to your resume
  - 🎤 Likely interview topics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Vanilla JS (ES6+), CSS3 |
| Backend | Python 3.11+, FastAPI |
| Database | PostgreSQL (SQLAlchemy ORM) |
| Auth | JWT (PyJWT + bcrypt) |
| AI | OpenAI API (`gpt-5.4-mini`) via server-side call |
| Caching | Redis *(Phase 3 — coming soon)* |
| Containers | Docker + Docker Compose *(Phase 4 — coming soon)* |
| CI/CD | GitHub Actions |
| Deployment | AWS EC2 *(Phase 6 — coming soon)* |

---

## 📁 Project Structure
