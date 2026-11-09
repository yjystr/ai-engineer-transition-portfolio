# Phase 0 — Weekend setup (Nov 7–8, ~3 hrs)

From the 90-day plan (`AI_Engineer_90_Day_Transition_Plan.md`): create the repo,
set up keys with spend caps, and deploy a trivial FastAPI app live. This folder
is the starter kit — copy it into a new public GitHub repo named
`ai-transition-portfolio` and work through the checklist below.

**Rule from the plan:** synthetic / public data only — never TikTok or Capital
One data in this repo.

## Checklist

### 1. Repo (~20 min)
- [ ] GitHub → New repository → `ai-transition-portfolio`, Public, add a README
- [ ] Copy everything in this folder into it (including hidden files: `.env.example`,
      `.gitignore`, `.github/workflows/ci.yml`)
- [ ] `git add . && git commit -m "Phase 0: hello-world API" && git push`

### 2. Local environment (~30 min)
- [ ] Python 3.11+ (3.12 used here), Git, Docker Desktop, VS Code installed
- [ ] `python -m venv .venv && source .venv/bin/activate` (or `uv venv`)
- [ ] `pip install -r requirements.txt`
- [ ] `cp .env.example .env` — leave keys blank until step 3
- [ ] `uvicorn app.main:app --reload` → open http://127.0.0.1:8000/docs
- [ ] `pytest -q` → 2 passed (`/` and `/health`)

### 3. API keys — with spend caps (~20 min)
- [ ] OpenAI platform → API key → set a **$20/month** spend cap / hard limit
- [ ] Anthropic Console → API key → set a **$20/month** spend cap
- [ ] Paste both into `.env` only — never commit `.env`, never paste keys into
      code, issues, or chat. Rotate a key immediately if it ever leaks.
- [ ] Keys are not needed to run the Phase 0 app — they are for Weeks 2–4.

### 4. Deploy the hello-world app (~60 min)
- [ ] Option A (easiest): Render — New → Web Service → connect the repo.
      It reads `render.yaml`; health check is `/health`. Free tier sleeps
      when idle, which is fine for Phase 0.
- [ ] Option B: Fly.io — `fly launch` with the included `Dockerfile`.
- [ ] Verify the live URL: `curl <your-url>/health` returns
      `{"status":"ok","service":"ai-transition-portfolio"}`
- [ ] Sanity-check Docker locally first if deploy fails:
      `docker compose up --build`, then `curl localhost:8000/health`

### 5. Done when…
- [ ] Public repo exists, CI is green on the first push, and the live
      `/health` URL responds. That is the Phase 0 exit deliverable —
      everything else in the plan builds on it.

## What's in this folder

| File | Why |
|---|---|
| `app/main.py` | FastAPI app: `/` hello world, `/health`, `/docs` |
| `tests/test_health.py` | 2 smoke tests (run with `pytest -q`) |
| `requirements.txt` | FastAPI, uvicorn, pydantic, pytest, httpx |
| `Dockerfile` | Container for Render / Fly.io / local Docker |
| `docker-compose.yml` | API + Postgres/pgvector (pgvector is for Weeks 4–5 RAG, already wired) |
| `render.yaml` | Render web service, health check `/health` |
| `.github/workflows/ci.yml` | Runs `pytest` on every push |
| `.env.example` / `.gitignore` | Key placeholders; `.env` is never committed |

## If you get stuck
- Deploy fails but local works → check the host's build log first; the
  usual culprit is the start command — it must be
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (Render sets `$PORT`).
  The Dockerfile already binds `0.0.0.0:8000`; Render's Docker path uses it.
- `pytest` can't import `app` → run it from the repo root, not from `tests/`.
- Docker Desktop not starting → Phase 0 deploy does not need local Docker;
  skip `docker compose` and come back to it in Week 3.
