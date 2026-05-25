from app.core.constants import MAX_RISK_SCORE, RISK_LEVEL_THRESHOLDS, RiskLevel
from app.services.risk_rules import Finding


def calculate_score(findings: list[Finding]) -> int:
    total = sum(finding.weight for finding in findings)
    return min(MAX_RISK_SCORE, total)


def score_to_level(score: int) -> RiskLevel:
    for threshold, level in RISK_LEVEL_THRESHOLDS:
        if score >= threshold:
            return level
    return RiskLevel.LOW


def calculate_risk(findings: list[Finding]) -> tuple[int, RiskLevel]:
    score = calculate_score(findings)
    level = score_to_level(score)
    return score, level
