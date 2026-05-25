# AegisLink API Design

Base URL (local): `http://127.0.0.1:8000`

Interactive docs: `/docs`, `/redoc`

## Health Check

**GET** `/health`

Response `200`:

```json
{
  "status": "ok",
  "service": "AegisLink API"
}
```

## Analyze URL

**POST** `/api/v1/analyses`

Request body:

```json
{
  "url": "https://example-login-security.com/verify-account"
}
```

Response `201`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Database ID |
| `original_url` | string | Submitted URL |
| `normalized_url` | string | Normalized for analysis |
| `domain` | string \| null | Hostname |
| `scheme` | string \| null | `http`, `https`, or `missing` |
| `risk_score` | integer | 0–100 |
| `risk_level` | string | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `findings` | array | Rule findings with `code`, `title`, `description`, `weight` |
| `explanation` | string | Human-readable summary |
| `recommendations` | array of strings | Safe actions |
| `created_at` | datetime | UTC timestamp |

Errors:

- `422` — invalid or empty URL

## List Analyses

**GET** `/api/v1/analyses`

Query parameters:

| Name | Default | Description |
|------|---------|-------------|
| `limit` | 20 | Page size (1–100) |
| `offset` | 0 | Skip count |
| `risk_level` | — | Optional filter: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |

Response `200`:

```json
{
  "items": [],
  "limit": 20,
  "offset": 0,
  "total": 0
}
```

## Get Analysis Detail

**GET** `/api/v1/analyses/{analysis_id}`

Response `200`: same shape as single analyze response.

Response `404`: analysis not found.

## Markdown Report

**GET** `/api/v1/reports/analyses/{analysis_id}`

Response `200`:

```json
{
  "analysis_id": 1,
  "report_markdown": "# AegisLink Security Report\n..."
}
```

Response `404`: analysis not found.
