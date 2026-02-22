# Physical AI & Humanoid Robotics Textbook 🤖

An AI-native interactive textbook for learning Physical AI and Humanoid Robotics, built with Docusaurus, Gemini AI, and modern web technologies.

## 🌟 Features

- 📚 **Comprehensive Content**: 4 modules, 13 weeks, 25+ chapters on Physical AI
- 🤖 **AI Chatbot**: RAG-powered chatbot using Gemini AI + Qdrant vector search
- 🎨 **Personalization**: Content adapts to your background and experience level
- 🌐 **Urdu Translation**: One-click Urdu translation using Gemini AI
- 🔐 **Authentication**: User profiles with background information
- 📱 **Responsive**: Works on all devices

## 🚀 Quick Start

### Frontend (Docusaurus)

```bash
npm install
npm start    # Development server at http://localhost:3000
npm run build  # Production build
```

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys
uvicorn app.main:app --reload
```

## 🔧 Configuration

Create `backend/.env` with:

```env
GEMINI_API_KEY=your_gemini_key
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_key
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
```

## 📖 Textbook Structure

- **Module 1**: The Robotic Nervous System (ROS 2)
- **Module 2**: The Digital Twin (Gazebo & Unity)
- **Module 3**: The AI-Robot Brain (NVIDIA Isaac™)
- **Module 4**: Vision-Language-Action (VLA)
- **Capstone**: Autonomous Humanoid Robot

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Docusaurus 3.x + React + TypeScript |
| AI Chatbot | Gemini 1.5 Flash + RAG |
| Vector DB | Qdrant Cloud (Free tier) |
| Database | Neon Serverless Postgres (Free tier) |
| Backend | FastAPI + Python |
| Auth | JWT with bcrypt |
| Deployment | GitHub Pages + Vercel |

## 🤖 Claude Code Agents

This project includes custom Claude Code subagents:
- **Content Writer**: Generate educational content
- **Code Generator**: Create ROS 2 and robotics code
- **Quiz Generator**: Create chapter assessments

And custom skills:
- `/translate-chapter`: Translate to Urdu
- `/personalize`: Adjust content level
- `/generate-quiz`: Create quizzes

## 📦 Deployment

Frontend automatically deploys to GitHub Pages via GitHub Actions.
Backend deploys to Vercel.

## 🏆 Hackathon

Built for the **Panaversity Hackathon I: Physical AI & Humanoid Robotics Textbook**

Built with ❤️ for Panaversity
