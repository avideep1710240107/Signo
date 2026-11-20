# SIGNOVA AI — runnable MVP foundation

A responsive accessibility-focused web application with browser-based speech transcription, a FastAPI backend, transcript processing/history, conversation UI, emergency phrase shortcuts, and a strict verified-ISL-asset gate.

## Honest feature status

**Working in this MVP**
- Premium responsive web interface.
- Browser microphone speech recognition using the Web Speech API (best support in current Chrome/Edge; availability and language quality depend on browser/device).
- Language selection for English, Hindi, Bengali, Urdu and Tamil. The selected locale is sent to the browser speech engine; auto mode currently defaults to English (India), not true automatic multilingual detection.
- Text submission to FastAPI, local JSONL history, health and language endpoints.
- Conversation UI and emergency phrase shortcuts.
- A gate that only accepts exact phrase assets marked verified and carrying reviewer metadata.

**Not yet implemented**
- True multilingual automatic language identification and ASR backend.
- Semantic spoken-language-to-ISL translation.
- Native-reviewed ISL lexicon / grammar model / motion dataset.
- 3D avatar animation and facial grammar.
- Sign-to-voice computer vision model.
- User accounts, PostgreSQL, Redis, production authentication and deployment hardening.

The app intentionally does not fabricate sign gestures. An empty `data/verified_signs.json` means no sign animations can be played.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000 in a recent Chrome or Edge browser. Allow microphone permission. Speech recognition may require an internet connection and a secure context; localhost is treated as secure by modern browsers.

## Docker

```bash
docker compose up --build
```

Open http://localhost:8000.

## API

- `GET /api/health`
- `GET /api/languages`
- `POST /api/translate` with `{ "text": "Hello", "source_language": "en", "target_sign_language": "ISL" }`
- `GET /api/history?limit=30`
- `POST /api/feedback` with `{ "translation_id": "...", "feedback": "..." }`

Interactive API docs: http://127.0.0.1:8000/docs

## Verified sign asset format

Only add an asset after obtaining permission and review from qualified ISL users / linguists. Keep the asset path relative to the frontend directory and serve it from a controlled asset directory. Example metadata shape:

```json
{
  "example phrase": {
    "verified": true,
    "reviewed_by": "Named qualified reviewer / review panel ID",
    "asset": "/assets/approved-clip.mp4",
    "license": "documented permission / license reference",
    "review_date": "2026-11-20"
  }
}
```

The starter project does not include fabricated signs or third-party sign recordings.

## Production checklist

Before public deployment: replace wildcard CORS with exact origins; add authentication and authorization; use managed secrets; add rate limits; configure TLS; implement consent and retention controls; move history to PostgreSQL; add Redis only when needed; validate ASR and translation on representative Indian language datasets; obtain licensed native-reviewed ISL data; conduct usability testing with Deaf signers; security test uploads and WebSockets; measure semantic adequacy and sign sequence correctness. Do not use this MVP as a substitute for an interpreter in medical, legal or emergency-critical conversations.
