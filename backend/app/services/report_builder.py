import json

from app.models.analysis import Analysis


def build_markdown_report(analysis: Analysis) -> str:
    findings = json.loads(analysis.findings_json)
    recommendations = json.loads(analysis.recommendations_json)

    findings_lines = "\n".join(
        f"- **{item['title']}**: {item['description']}" for item in findings
    )
    recommendations_lines = "\n".join(f"- {item}" for item in recommendations)

    summary = (
        f"The analyzed URL received a **{analysis.risk_level}** risk rating "
        f"with a score of **{analysis.risk_score}/100**."
    )

    return f"""# AegisLink Security Report

## Summary
{summary}

## URL
- **Original URL:** {analysis.original_url}
- **Normalized URL:** {analysis.normalized_url}
- **Domain:** {analysis.domain or "N/A"}

## Risk
- **Score:** {analysis.risk_score}
- **Level:** {analysis.risk_level}

## Findings
{findings_lines or "- No findings recorded."}

## Explanation
{analysis.explanation}

## Recommendations
{recommendations_lines or "- No recommendations recorded."}

## Note
This analysis is based on static URL patterns only. It does not prove that a website is malicious.
"""
