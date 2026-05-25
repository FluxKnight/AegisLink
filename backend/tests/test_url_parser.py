from app.services.url_parser import parse_url


def test_normalize_url_without_scheme():
    parsed = parse_url("example.com/login")
    assert parsed.normalized_url == "https://example.com/login"
    assert parsed.scheme == "missing"
    assert parsed.had_missing_scheme is True
    assert parsed.domain == "example.com"


def test_parse_https_url():
    parsed = parse_url("https://www.example.com/path?q=1")
    assert parsed.scheme == "https"
    assert parsed.domain == "www.example.com"
    assert parsed.path == "/path"
    assert parsed.query == "q=1"


def test_detect_ip_host():
    parsed = parse_url("http://192.168.1.1/login")
    assert parsed.is_ip_host is True
    assert parsed.domain == "192.168.1.1"
