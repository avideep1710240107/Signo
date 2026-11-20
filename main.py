from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
from datetime import datetime, timezone
import json, os, re, uuid

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
HISTORY = DATA / "history.jsonl"
SIGNS = DATA / "verified_signs.json"

app = FastAPI(title="SIGNOVA AI API", version="0.1.0", description="Accessible multilingual speech-to-sign platform foundation")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

class TranslationRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    source_language: str = "auto"
    target_sign_language: str = "ISL"

class FeedbackRequest(BaseModel):
    translation_id: str
    feedback: str = Field(min_length=1, max_length=2000)

LANGUAGES = {"en":"English", "hi":"Hindi", "bn":"Bengali", "ur":"Urdu", "ta":"Tamil"}

def load_signs():
    if not SIGNS.exists(): return {}
    try: return json.loads(SIGNS.read_text(encoding="utf-8"))
    except Exception: return {}

@app.get("/api/health")
def health():
    return {"status":"ok", "service":"SIGNOVA AI", "version":"0.1.0", "speech":"browser-dependent", "sign_assets":len(load_signs()), "sign_language":"ISL", "notice":"Only assets explicitly reviewed and marked verified are eligible for sign playback."}

@app.get("/api/languages")
def languages():
    return {"spoken_languages":LANGUAGES, "target_sign_languages":[{"code":"ISL","name":"Indian Sign Language","status":"initial target"}]}

@app.post("/api/translate")
def translate(req: TranslationRequest):
    text = req.text.strip()
    if not text: raise HTTPException(400, "Text cannot be empty")
    if req.source_language != "auto" and req.source_language not in LANGUAGES:
        raise HTTPException(400, "Unsupported source language")
    # This MVP deliberately does not invent a semantic translation or sign gloss.
    # A verified sign asset can be served only when its exact phrase key is present.
    signs = load_signs()
    key = re.sub(r"\s+", " ", text.casefold()).strip()
    asset = signs.get(key)
    verified = bool(asset and asset.get("verified") is True and asset.get("reviewed_by") and asset.get("asset"))
    tid = str(uuid.uuid4())
    result = {
        "id":tid, "original_text":text, "source_language":req.source_language,
        "target_sign_language":req.target_sign_language,
        "status":"verified_asset_available" if verified else "transcription_ready_sign_asset_missing",
        "sign": asset if verified else None,
        "confidence": None,
        "message": "A reviewed sign asset is available." if verified else "Speech text received. No reviewed ISL animation matches this exact phrase. Do not treat this as a completed sign-language translation.",
        "created_at":datetime.now(timezone.utc).isoformat()
    }
    with HISTORY.open("a", encoding="utf-8") as f: f.write(json.dumps(result, ensure_ascii=False)+"\n")
    return result

@app.get("/api/history")
def history(limit: int = 30):
    if not HISTORY.exists(): return {"items":[]}
    rows=[]
    for line in HISTORY.read_text(encoding="utf-8").splitlines()[-max(1,min(limit,100)):]:
        try: rows.append(json.loads(line))
        except json.JSONDecodeError: pass
    return {"items":list(reversed(rows))}

@app.post("/api/feedback")
def feedback(req: FeedbackRequest):
    path=DATA/"feedback.jsonl"
    item={"translation_id":req.translation_id,"feedback":req.feedback,"created_at":datetime.now(timezone.utc).isoformat()}
    with path.open("a",encoding="utf-8") as f: f.write(json.dumps(item,ensure_ascii=False)+"\n")
    return {"saved":True}

app.mount("/", StaticFiles(directory=ROOT/"frontend", html=True), name="frontend")
