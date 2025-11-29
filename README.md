# Intro-scoring

A full-stack application that scores spoken-style self-introductions.

* Backend: FastAPI (Python) — computes metrics like content structure, speech rate, grammar/vocabulary, clarity, engagement.
* Frontend: React — simple UI to input a transcript & duration, get a scoring breakdown.

The repository contains both backend and frontend — deployable independently or together (frontend on Vercel, backend on Render).

## Features

* Evaluate a spoken-style introduction based on:

  * **Content & Structure:** Does it include basic items (name, age, hobbies, background), and a proper flow (greeting, body, conclusion).

  * **Speech Rate:** Ability to judge based on duration & text length.

  * **Language & Vocabulary quality –** grammar/spelling (via spell-checker) and vocabulary diversity (TTR).

  * **Clarity & Engagement** 

* Simple React frontend to submit transcript + duration and display a breakdown of scores and sub-criteria.
* Easy deployment: frontend and backend can live on different services (e.g. Vercel + Render) with CORS configured.

## Quick Start (Local Development)
#### Backend
```
# Navigate to root
cd api   # or ensure you're in project root and path is correct

python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt

uvicorn api.main:app --reload
```

The backend will run at: `http://localhost:8000`

You can view API docs at: `http://localhost:8000/docs`

#### Frontend
```
cd frontend
npm install
npm start
```
Open your browser at: `http://localhost:3000` (or whatever port React sets)

## Deployment Setup (Frontend + Backend on Production)

Here’s a recommended deployment strategy:

|Service  |  Purpose
----------|------------------------------
|Render	  |  Host the FastAPI backend
|Vercel   |	 Host the React frontend

#### Backend (Render) Setup

* Ensure your requirements.txt includes all dependencies (and no heavy system-build dependencies).
* Add CORS middleware in `api/main.py`:
```
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "https://<your-frontend-domain>",
      "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

* Start command:
```
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

* (Optional) Use a `render.yaml` to define build & start steps.

## Frontend (Vercel) Setup

* In React code, set the backend URL to your deployed backend, e.g.:
```
const API_URL = "https://intro-scoring.onrender.com/score";
```

* Deploy to Vercel — it will build and host your static React app.

## API
`POST /score`

Request body (JSON):
```
{
  "text": "Your spoken transcript here …",
  "duration_sec": 30
}
```

* `text` — full transcript (plain text).

* `duration_sec` — spoken duration in seconds.

Response: JSON with overall score (`0–100`) and breakdown per criterion.

## Customization & Extension

Because the scoring logic is modular (in `models/`), you can:

* Change / add new criteria (e.g. pronunciation score, repetition penalty, etc.)
* Integrate with audio transcription: you can feed actual audio → get text → send to API
* Add user interface enhancements (audio upload → auto-transcribe → score)
* Extend backend (e.g. store scoring history, analytics)
