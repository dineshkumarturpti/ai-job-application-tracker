# 🗂️ AI Job Application Tracker

> A full-stack AI-powered job application tracker — track every application, analyze your resume against any job description, and get back a verdict with missing skills, suggested keywords, and interview prep topics.

[![Backend CI](https://github.com/dineshkumarturpti/ai-job-application-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/dineshkumarturpti/ai-job-application-tracker/actions)![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)

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
