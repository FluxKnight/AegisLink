from dataclasses import dataclass

from app.core.constants import (
    BRAND_TOKENS,
    LONG_URL_THRESHOLD,
    MIN_SUBDOMAINS_FOR_WARNING,
    SUSPICIOUS_KEYWORDS,
    SUSPICIOUS_TLDS,
    URL_SHORTENER_HOSTS,
    VERY_LONG_URL_THRESHOLD,
)
from app.services.url_parser import ParsedUrl


@dataclass(frozen=True)
class Finding:
    code: str
    title: str
    description: str
    weight: int


def _url_search_text(parsed: ParsedUrl) -> str:
    return parsed.normalized_url.lower()


def _has_suspicious_keyword(text: str) -> bool:
    return any(keyword in text for keyword in SUSPICIOUS_KEYWORDS)


def _matched_keywords(text: str) -> list[str]:
    return [keyword for keyword in SUSPICIOUS_KEYWORDS if keyword in text]


def rule_missing_https(parsed: ParsedUrl) -> Finding | None:
    if parsed.scheme == "http":
        return Finding(
            code="MISSING_HTTPS",
            title="Connection is not using HTTPS",
            description=(
                "The URL uses HTTP instead of HTTPS. Sensitive data may be "
                "sent without encryption."
            ),
            weight=15,
        )
    return None


def rule_missing_scheme(parsed: ParsedUrl) -> Finding | None:
    if parsed.had_missing_scheme:
        return Finding(
            code="MISSING_SCHEME",
            title="URL had no scheme",
            description=(
                "The URL was submitted without http:// or https://. It was "
                "normalized for analysis, but the original input lacked a clear scheme."
            ),
            weight=5,
        )
    return None


def rule_suspicious_keywords(parsed: ParsedUrl) -> Finding | None:
    text = _url_search_text(parsed)
    matched = _matched_keywords(text)
    if not matched:
        return None
    sample = ", ".join(matched[:4])
    return Finding(
        code="SUSPICIOUS_KEYWORD",
        title="Suspicious keyword detected",
        description=(
            f"The URL contains words such as {sample} that are often used in "
            "phishing or social engineering attempts."
        ),
        weight=20,
    )


def rule_long_url(parsed: ParsedUrl) -> Finding | None:
    if parsed.url_length > LONG_URL_THRESHOLD:
        return Finding(
            code="LONG_URL",
            title="Long URL detected",
            description=(
                "The URL is longer than 100 characters, which may be used to "
                "hide suspicious parts of the link."
            ),
            weight=10,
        )
    return None


def rule_very_long_url(parsed: ParsedUrl) -> Finding | None:
    if parsed.url_length > VERY_LONG_URL_THRESHOLD:
        return Finding(
            code="VERY_LONG_URL",
            title="Very long URL detected",
            description=(
                "The URL is longer than 180 characters, which may indicate an "
                "attempt to confuse users with excessive length."
            ),
            weight=20,
        )
    return None


def rule_ip_address_domain(parsed: ParsedUrl) -> Finding | None:
    if parsed.is_ip_host:
        return Finding(
            code="IP_ADDRESS_DOMAIN",
            title="IP address used instead of domain",
            description=(
                "The URL points to an IP address instead of a normal domain name. "
                "Legitimate services usually use recognizable domain names."
            ),
            weight=25,
        )
    return None


def rule_too_many_subdomains(parsed: ParsedUrl) -> Finding | None:
    if parsed.subdomain_count >= MIN_SUBDOMAINS_FOR_WARNING:
        return Finding(
            code="TOO_MANY_SUBDOMAINS",
            title="Too many subdomains",
            description=(
                f"The domain has {parsed.subdomain_count} subdomain levels, which may "
                "be used to imitate trusted sites."
            ),
            weight=15,
        )
    return None


def rule_suspicious_tld(parsed: ParsedUrl) -> Finding | None:
    if not parsed.tld:
        return None
    if parsed.tld not in SUSPICIOUS_TLDS:
        return None
    return Finding(
        code="SUSPICIOUS_TLD",
        title="Suspicious top-level domain",
        description=(
            f"The URL uses the {parsed.tld} TLD, which is sometimes associated "
            "with risky or misleading links."
        ),
        weight=15,
    )


def rule_url_shortener(parsed: ParsedUrl) -> Finding | None:
    host = parsed.domain or ""
    if host not in URL_SHORTENER_HOSTS:
        return None
    return Finding(
        code="URL_SHORTENER",
        title="URL shortener detected",
        description=(
            "The link uses a URL shortener, so the final destination is hidden "
            "until the link is opened."
        ),
        weight=10,
    )


def _is_suspicious_context(text: str, parsed: ParsedUrl) -> bool:
    if _has_suspicious_keyword(text):
        return True
    if parsed.tld in SUSPICIOUS_TLDS:
        return True
    host = parsed.domain or ""
    if host in URL_SHORTENER_HOSTS:
        return True
    return False


def rule_brand_impersonation_hint(parsed: ParsedUrl) -> Finding | None:
    text = _url_search_text(parsed)
    matched_brands = [brand for brand in BRAND_TOKENS if brand in text]
    if not matched_brands:
        return None
    if not _is_suspicious_context(text, parsed):
        return None
    brand_list = ", ".join(matched_brands[:3])
    return Finding(
        code="BRAND_IMPERSONATION_HINT",
        title="Possible brand impersonation",
        description=(
            f"The URL references well-known brands such as {brand_list} together "
            "with suspicious patterns. This may be an impersonation attempt, but it "
            "is not proof of phishing."
        ),
        weight=20,
    )


RULE_FUNCTIONS = (
    rule_missing_https,
    rule_missing_scheme,
    rule_suspicious_keywords,
    rule_long_url,
    rule_very_long_url,
    rule_ip_address_domain,
    rule_too_many_subdomains,
    rule_suspicious_tld,
    rule_url_shortener,
    rule_brand_impersonation_hint,
)


def evaluate_all_rules(parsed: ParsedUrl) -> list[Finding]:
    findings: list[Finding] = []
    for rule_fn in RULE_FUNCTIONS:
        finding = rule_fn(parsed)
        if finding is not None:
            findings.append(finding)
    return findings
