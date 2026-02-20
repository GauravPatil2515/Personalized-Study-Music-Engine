# Personalized Study Music Engine

Generate adaptive focus music recommendations based on your mood, study duration, and subject.

## Demo

**Live Demo:** https://YOUR-APP-NAME.onrender.com

---

## Local Run

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
Open http://localhost:8000

---

## Deploy to Render (Free Tier)

1. Push this repo to GitHub (only 4 files needed).
2. Go to https://render.com → New → Web Service.
3. Connect your GitHub repo.
4. Set these fields:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variable (optional, for AI responses):
   - `GROQ_API_KEY` = your_groq_api_key
6. Click **Create Web Service**.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Optional | Enables AI-powered recommendations via Groq (llama-3.3-70b-versatile). Falls back to local logic if absent or on failure. |
| `PORT` | Auto-set by Render | Port the server listens on. |

---

## API

**POST /solve**

Request:
```json
{"data": "stressed, 2 hours, math exam"}
```

Response:
```json
{"output": "Session: 2h | Genres: Lo-fi hip hop beats, 432Hz piano rain mix, Theta binaural 6Hz. Start with 'Lo-fi hip hop beats' for your first 25-min Pomodoro, switch to 'Theta binaural 6Hz' after breaks. Adjust volume to 40-50% for peak focus."}
```
