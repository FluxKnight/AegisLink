import json
from dataclasses import asdict

from sqlalchemy.orm import Session

from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisResponse, FindingSchema, RiskLevelEnum
from app.services.explanation import build_explanation
from app.services.risk_rules import Finding, evaluate_all_rules
from app.services.risk_scoring import calculate_risk
from app.services.url_parser import ParsedUrl, parse_url


def analyze_url_string(raw_url: str) -> tuple[ParsedUrl, list[Finding], int, str, str, list[str]]:
    parsed = parse_url(raw_url)
    findings = evaluate_all_rules(parsed)
    score, level = calculate_risk(findings)
    explanation, recommendations = build_explanation(findings, score, level)
    return parsed, findings, score, level.value, explanation, recommendations


def findings_to_json(findings: list[Finding]) -> str:
    payload = [asdict(finding) for finding in findings]
    return json.dumps(payload)


def persist_analysis(
    db: Session,
    raw_url: str,
    parsed: ParsedUrl,
    findings: list[Finding],
    score: int,
    risk_level: str,
    explanation: str,
    recommendations: list[str],
) -> Analysis:
    record = Analysis(
        original_url=parsed.original_url,
        normalized_url=parsed.normalized_url,
        domain=parsed.domain,
        scheme=parsed.scheme,
        risk_score=score,
        risk_level=risk_level,
        findings_json=findings_to_json(findings),
        explanation=explanation,
        recommendations_json=json.dumps(recommendations),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def analysis_to_response(record: Analysis) -> AnalysisResponse:
    findings_data = json.loads(record.findings_json)
    recommendations = json.loads(record.recommendations_json)
    findings = [FindingSchema(**item) for item in findings_data]

    return AnalysisResponse(
        id=record.id,
        original_url=record.original_url,
        normalized_url=record.normalized_url,
        domain=record.domain,
        scheme=record.scheme,
        risk_score=record.risk_score,
        risk_level=RiskLevelEnum(record.risk_level),
        findings=findings,
        explanation=record.explanation,
        recommendations=recommendations,
        created_at=record.created_at,
    )
