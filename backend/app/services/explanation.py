from app.core.constants import RiskLevel
from app.services.risk_rules import Finding


LEVEL_RECOMMENDATIONS: dict[RiskLevel, list[str]] = {
    RiskLevel.LOW: [
        "Still verify the domain before entering sensitive information.",
    ],
    RiskLevel.MEDIUM: [
        "Avoid entering passwords unless you are sure the site is official.",
        "Open the official website manually instead of clicking the link.",
    ],
    RiskLevel.HIGH: [
        "Do not enter credentials or payment information.",
        "Verify the sender and domain through an official channel.",
    ],
    RiskLevel.CRITICAL: [
        "Do not open or interact with this link.",
        "Report it to a security team or trusted adult/administrator.",
    ],
}

FINDING_PHRASES: dict[str, str] = {
    "MISSING_HTTPS": "it does not use HTTPS encryption",
    "MISSING_SCHEME": "the original link did not specify a secure scheme",
    "SUSPICIOUS_KEYWORD": "it contains account or payment-related wording",
    "LONG_URL": "the URL is unusually long",
    "VERY_LONG_URL": "the URL is very long and may hide its true intent",
    "IP_ADDRESS_DOMAIN": "it uses an IP address instead of a trusted domain name",
    "TOO_MANY_SUBDOMAINS": "it has many subdomains that could mimic a real service",
    "SUSPICIOUS_TLD": "it uses a top-level domain that is sometimes linked to risky sites",
    "URL_SHORTENER": "it uses a URL shortener that hides the destination",
    "BRAND_IMPERSONATION_HINT": "it may be trying to imitate a well-known brand",
}


def _level_opener(level: RiskLevel, score: int) -> str:
    openers = {
        RiskLevel.LOW: (
            f"This URL has a low risk score ({score}/100). "
            "No major suspicious patterns were detected, but caution is still advised."
        ),
        RiskLevel.MEDIUM: (
            f"This URL has a medium risk score ({score}/100). "
            "Some patterns could indicate social engineering or misleading intent."
        ),
        RiskLevel.HIGH: (
            f"This URL has a high risk score ({score}/100). "
            "Several suspicious patterns appear together and it should be treated carefully."
        ),
        RiskLevel.CRITICAL: (
            f"This URL has a critical risk score ({score}/100). "
            "Multiple strong warning signs are present and the link should be avoided."
        ),
    }
    return openers[level]


def build_explanation(
    findings: list[Finding],
    score: int,
    level: RiskLevel,
) -> tuple[str, list[str]]:
    opener = _level_opener(level, score)

    if findings:
        phrases = [
            FINDING_PHRASES.get(finding.code, finding.title.lower())
            for finding in findings
        ]
        detail = (
            " This may be risky because "
            + ", ".join(phrases[:4])
            + (
                f", and {len(phrases) - 4} other pattern(s)."
                if len(phrases) > 4
                else "."
            )
        )
    else:
        detail = " No strong suspicious patterns were found in the URL structure."

    disclaimer = (
        " This does not prove the link is malicious, but it could be used to "
        "trick users into sharing sensitive information."
    )

    explanation = opener + detail + disclaimer
    recommendations = list(LEVEL_RECOMMENDATIONS[level])

    if any(f.code == "URL_SHORTENER" for f in findings):
        recommendations.append(
            "Expand shortened links through a trusted security tool before opening them."
        )
    if any(f.code == "BRAND_IMPERSONATION_HINT" for f in findings):
        recommendations.append(
            "Check the official brand website or app instead of using this link."
        )

    return explanation, recommendations
