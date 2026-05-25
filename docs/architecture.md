# AegisLink Architecture

AegisLink uses a layered backend design so API, business logic, and persistence stay separated.

## Layers

### API Layer (`app/api/`)

- Handles HTTP requests and responses only.
- Validates input with Pydantic schemas.
- Calls service functions; does not implement risk logic inline.
- Routes: `health.py`, `analyses.py`, `reports.py`, mounted via `router.py`.

### Schema Layer (`app/schemas/`)

- Request and response DTOs for OpenAPI and validation.
- Keeps API contracts independent from SQLAlchemy models.

### Service Layer (`app/services/`)

- **url_parser**: Normalizes URLs and extracts domain, scheme, TLD, subdomains, IP detection.
- **risk_rules**: Rule-based findings (code, title, description, weight).
- **risk_scoring**: Aggregates weights into score (0–100) and risk level.
- **explanation**: Template-based human-readable text and recommendations.
- **report_builder**: Markdown security report from stored analysis.

All analysis is **offline** — no HTTP requests to submitted URLs.

### Database Layer (`app/db/`, `app/models/`)

- SQLAlchemy engine and session management.
- `Analysis` model stores results and JSON-serialized findings/recommendations.
- SQLite for MVP; `DATABASE_URL` can switch to PostgreSQL without changing services.

### Core (`app/core/`)

- **config**: Environment-driven settings (`DATABASE_URL`, app name).
- **constants**: Keywords, TLD lists, thresholds shared by rules and explanation.

## Analysis Pipeline

```
POST /api/v1/analyses
    → validate URL input
    → url_parser.parse_url()
    → risk_rules.evaluate_all_rules()
    → risk_scoring.calculate_risk()
    → explanation.build_explanation()
    → persist Analysis
    → return AnalysisResponse
```

## Risk Engine

Rules are independent functions returning `Finding` objects. Weights sum to a capped score. Levels map to score bands (LOW through CRITICAL).

## Explanation Engine

Not a live LLM in MVP. Templates combine finding summaries with cautious language (`may`, `could`, `appears`) and level-based recommendations.

## PostgreSQL Migration Path

1. Set `DATABASE_URL=postgresql+psycopg://...` in `.env`.
2. Optionally replace `Text` JSON columns with `JSONB`.
3. Run Alembic migrations when the schema grows.
