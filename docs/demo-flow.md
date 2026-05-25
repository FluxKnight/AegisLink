# AegisLink Demo Flow (2 Minutes)

## Setup (30 seconds)

```bash
cd xvslen_project/03_aegislink/backend
.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Step 1 — Health (10 seconds)

```bash
curl http://127.0.0.1:8000/health
```

Show `"status": "ok"` and service name.

## Step 2 — Analyze a suspicious URL (45 seconds)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/analyses ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"http://192.168.1.1/login/verify-account?reset=1\"}"
```

Highlight:

- `risk_score` and `risk_level`
- `findings` array (IP, keywords, missing HTTPS)
- `explanation` in plain language
- `recommendations`

## Step 3 — History (20 seconds)

```bash
curl "http://127.0.0.1:8000/api/v1/analyses?limit=5"
```

Show stored analyses.

## Step 4 — Markdown report (25 seconds)

Use `id` from step 2:

```bash
curl http://127.0.0.1:8000/api/v1/reports/analyses/1
```

Paste `report_markdown` into a README or blog snippet.

## Closing Line

"This tool never visits the link. It teaches users what URL patterns to question before they click."
