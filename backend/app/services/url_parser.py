import ipaddress
import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ParsedUrl:
    original_url: str
    normalized_url: str
    domain: str | None
    scheme: str | None
    path: str
    query: str
    had_missing_scheme: bool
    is_ip_host: bool
    subdomain_count: int
    tld: str | None
    url_length: int


_SCHEME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")


def _has_scheme(url: str) -> bool:
    return bool(_SCHEME_PATTERN.match(url))


def _normalize_url(raw_url: str) -> tuple[str, bool]:
    trimmed = raw_url.strip()
    if _has_scheme(trimmed):
        return trimmed, False
    return f"https://{trimmed}", True


def _extract_host(parsed) -> str | None:
    host = parsed.hostname
    if host:
        return host.lower()
    netloc = parsed.netloc
    if not netloc:
        return None
    return netloc.split("@")[-1].split(":")[0].lower()


def _is_ip_host(host: str | None) -> bool:
    if not host:
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _count_subdomains(host: str | None) -> int:
    if not host or _is_ip_host(host):
        return 0
    parts = host.split(".")
    if len(parts) <= 2:
        return 0
    return len(parts) - 2


def _extract_tld(host: str | None) -> str | None:
    if not host or _is_ip_host(host):
        return None
    parts = host.split(".")
    if len(parts) < 2:
        return None
    return f".{parts[-1]}"


def parse_url(raw_url: str) -> ParsedUrl:
    original = raw_url.strip()
    normalized, had_missing_scheme = _normalize_url(original)
    parsed = urlparse(normalized)

    host = _extract_host(parsed)
    if had_missing_scheme:
        scheme = "missing"
    elif parsed.scheme:
        scheme = parsed.scheme.lower()
    else:
        scheme = "missing"

    return ParsedUrl(
        original_url=original,
        normalized_url=normalized,
        domain=host,
        scheme=scheme,
        path=parsed.path or "",
        query=parsed.query or "",
        had_missing_scheme=had_missing_scheme,
        is_ip_host=_is_ip_host(host),
        subdomain_count=_count_subdomains(host),
        tld=_extract_tld(host),
        url_length=len(original),
    )
