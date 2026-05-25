from app.services.risk_rules import evaluate_all_rules
from app.services.risk_scoring import calculate_score
from app.services.url_parser import parse_url


def test_suspicious_keywords_detected():
    parsed = parse_url("https://secure-login.example.com/verify-password")
    findings = evaluate_all_rules(parsed)
    codes = {finding.code for finding in findings}
    assert "SUSPICIOUS_KEYWORD" in codes


def test_ip_address_domain_detected():
    parsed = parse_url("http://192.168.1.1/login")
    findings = evaluate_all_rules(parsed)
    codes = {finding.code for finding in findings}
    assert "IP_ADDRESS_DOMAIN" in codes


def test_long_url_increases_risk():
    long_path = "a" * 120
    parsed = parse_url(f"https://example.com/{long_path}")
    findings = evaluate_all_rules(parsed)
    score = calculate_score(findings)
    assert score >= 10
    codes = {finding.code for finding in findings}
    assert "LONG_URL" in codes


def test_risk_score_caps_at_100():
    from app.services.risk_rules import Finding

    findings = [
        Finding("RULE_A", "Rule A", "First heavy signal.", 60),
        Finding("RULE_B", "Rule B", "Second heavy signal.", 60),
    ]
    score = calculate_score(findings)
    assert score == 100
