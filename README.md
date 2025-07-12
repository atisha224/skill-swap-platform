# 🔁 Skill Swap Platform

A full-stack web app that enables users to exchange skills through swap requests and public profiles. Built from scratch in 7 hours during a hackathon challenge — with full backend, local DB, and responsive frontend (with dark mode support).

---

## 👥 Team Members

- **Atisha Jain** – Fullstack Developer, Frontend Integrator  
- **Ashlesha Verma** – Backend API Lead, ML Engineer  
- **Avani Sharma** – UI/UX + Tailwind Specialist  
- **Devi Modi** – Database Designer + QA Tester

---

## 🌟 Features

### 👤 Users
- Register/Login
- Create public/private profiles
- List skills offered and wanted
- Search users by skill
- Request, accept, reject, delete swaps
- Give feedback post-swap

### 🧑‍⚖️ Admins
- Ban users
- View swap stats
- Download logs (CSV)
- Moderate platform activity

---

## 💻 Tech Stack

| Frontend             | Backend         | Database | Version Control |
|----------------------|------------------|----------|-----------------|
| HTML, Tailwind CSS (Dark Mode) | Flask (Python) | SQLite   | Git + GitHub     |

---

## 🛠 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/atisha224/skill-swap-platform.git
cd skill-swap-platform/backend

# Create and activate env
conda create -n skill-swap-platform python=3.10
conda activate skill-swap-platform

# Install backend deps
pip install flask flask-cors flask-sqlalchemy

# Run backend
python app.py
