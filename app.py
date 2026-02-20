import os
import random
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Req(BaseModel):
    data: str = ""

LIBRARY = {
    "stressed": ["Lo-fi hip hop beats", "432Hz piano rain mix", "Theta binaural 6Hz"],
    "anxious": ["432Hz healing tones", "Nature sounds + strings", "Theta wave ambient"],
    "tired": ["Upbeat lo-fi chill", "Alpha wave energizer 10Hz", "Cafe jazz upbeat"],
    "happy": ["Indie pop instrumental", "Bright bossa nova", "Upbeat acoustic jazz"],
    "angry": ["Post-rock instrumental", "Intense orchestral", "Drum + bass ambient"],
    "bored": ["Synthwave chill", "Video game OST lo-fi", "Chillhop beats"],
    "focused": ["40Hz gamma waves", "Deep focus classical", "Minimal piano"],
    "calm": ["Ambient piano meditation", "Soft acoustic guitar", "Slow jazz trio"],
}

def fallback(text: str) -> str:
    t = text.lower() if text else ""
    genre = next((LIBRARY[k] for k in LIBRARY if k in t), LIBRARY["focused"])
    hours = next((int(w) for w in t.split() if w.isdigit()), 1)
    picks = random.sample(genre, min(3, len(genre)))
    return (
        f"Session: {hours}h | Genres: {', '.join(picks)}. "
        f"Start with '{picks[0]}' for your first 25-min Pomodoro, "
        f"switch to '{picks[-1]}' after breaks. "
        f"Adjust volume to 40-50% for peak focus."
    )

@app.post("/solve")
async def solve(req: Req):
    data = (req.data or "").strip()
    if not data:
        return {"output": fallback("focused")}
    key = os.environ.get("GROQ_API_KEY")
    if key:
        try:
            async with httpx.AsyncClient(timeout=7) as c:
                r = await c.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {key}"},
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": "You are a study music advisor. Given mood and study context, suggest exactly 3 specific music genres/playlists with a timing tip. Reply in 2 sentences max."},
                            {"role": "user", "content": data}
                        ],
                        "max_tokens": 120,
                        "temperature": 0.7
                    }
                )
                if r.status_code == 200:
                    return {"output": r.json()["choices"][0]["message"]["content"].strip()}
        except Exception:
            pass
    return {"output": fallback(data)}

@app.get("/")
async def index():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
