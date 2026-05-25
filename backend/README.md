# AegisLink Backend

FastAPI backend for defensive URL risk analysis.

## Setup

```bash
python -m venv .venv
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -v
```

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | AegisLink API | Service display name |
| `DATABASE_URL` | `sqlite:///./aegislink.db` | SQLAlchemy URL |
| `DEBUG` | `true` | Echo SQL when true |

PostgreSQL example:

```
DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/aegislink
```

## API

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
