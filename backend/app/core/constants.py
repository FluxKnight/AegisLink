from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


RISK_LEVEL_THRESHOLDS: list[tuple[int, RiskLevel]] = [
    (75, RiskLevel.CRITICAL),
    (50, RiskLevel.HIGH),
    (25, RiskLevel.MEDIUM),
    (0, RiskLevel.LOW),
]

MAX_RISK_SCORE = 100

SUSPICIOUS_KEYWORDS: tuple[str, ...] = (
    "login",
    "verify",
    "password",
    "reset",
    "account",
    "secure",
    "security",
    "update",
    "payment",
    "bank",
    "wallet",
    "crypto",
    "free",
    "gift",
    "prize",
    "urgent",
)

SUSPICIOUS_TLDS: tuple[str, ...] = (
    ".zip",
    ".mov",
    ".click",
    ".top",
    ".xyz",
    ".loan",
)

URL_SHORTENER_HOSTS: tuple[str, ...] = (
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "shorturl.at",
)

BRAND_TOKENS: tuple[str, ...] = (
    "paypal",
    "google",
    "microsoft",
    "apple",
    "facebook",
    "instagram",
    "binance",
    "metamask",
)

LONG_URL_THRESHOLD = 100
VERY_LONG_URL_THRESHOLD = 180
MIN_SUBDOMAINS_FOR_WARNING = 3

MAX_URL_INPUT_LENGTH = 2048
