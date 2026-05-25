# AegisLink

AegisLink is a defensive cybersecurity backend API that analyzes suspicious links and explains potential risks in simple language.

## Why I Built This

I built AegisLink because many people click links without understanding why a URL might be dangerous. I wanted to create a tool that does more than label a link as safe or unsafe. It explains the risk clearly and helps users make better decisions.

## What This Project Demonstrates

- Python backend engineering
- FastAPI API design
- Defensive cybersecurity thinking
- Rule-based risk analysis
- AI-style explanation generation
- Database modeling
- Clean project architecture
- Testing and documentation

## Core Features

- URL risk analysis
- Risk scoring
- Human-readable explanations
- Safe recommendations
- Analysis history
- Markdown incident reports
- OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Service health check |
| `POST` | `/api/v1/analyses` | Analyze a suspicious URL |
| `GET` | `/api/v1/analyses` | List analysis history |
| `GET` | `/api/v1/analyses/{analysis_id}` | Get analysis detail |
| `GET` | `/api/v1/reports/analyses/{analysis_id}` | Generate Markdown report |

## Quick Start

```bash
cd xvslen_project/03_aegislink/backend
python -m venv .venv
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open API docs: http://127.0.0.1:8000/docs

## Demo Flow

1. User submits a suspicious URL.
2. AegisLink parses the URL.
3. Risk rules detect suspicious patterns.
4. The backend calculates a risk score.
5. The explanation engine generates a clear explanation.
6. The result is stored in the database.
7. User can generate a Markdown report.

See [docs/demo-flow.md](docs/demo-flow.md) for a 2-minute demo script.

## Project Structure

```
03_aegislink/
├── backend/          # FastAPI application
├── docs/             # Architecture and API documentation
└── demo-assets/      # Sample URLs and responses
```

## Safety Note

AegisLink does not perform attacks, exploitation, phishing, credential collection, malware analysis, or live website interaction. It only performs static URL pattern analysis for defensive education.

## Hackathon Relevance

This project shows that I can design and build a backend system with practical cybersecurity use cases, clean APIs, database storage, and AI-style explanation logic.

## Documentation

- [Architecture](docs/architecture.md)
- [API Design](docs/api-design.md)
- [Risk Scoring](docs/risk-scoring.md)
- [Demo Flow](docs/demo-flow.md)
