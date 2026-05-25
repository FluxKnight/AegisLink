# AegisLink Risk Scoring

Risk analysis is **rule-based** and **defensive**. Findings describe patterns that *may* indicate risk; they do not prove malicious intent.

## Scoring Formula

```
risk_score = min(100, sum(finding.weight for each finding))
```

## Risk Levels

| Score range | Level |
|-------------|-------|
| 0–24 | LOW |
| 25–49 | MEDIUM |
| 50–74 | HIGH |
| 75–100 | CRITICAL |

## Rules and Weights

| Code | Condition | Weight |
|------|-----------|--------|
| `MISSING_HTTPS` | Scheme is `http` | 15 |
| `MISSING_SCHEME` | Input had no `http://` or `https://` | 5 |
| `SUSPICIOUS_KEYWORD` | login, verify, password, reset, account, secure, security, update, payment, bank, wallet, crypto, free, gift, prize, urgent | 20 |
| `LONG_URL` | URL length > 100 | 10 |
| `VERY_LONG_URL` | URL length > 180 | 20 |
| `IP_ADDRESS_DOMAIN` | Host is IPv4 or IPv6 | 25 |
| `TOO_MANY_SUBDOMAINS` | Subdomain count ≥ 3 | 15 |
| `SUSPICIOUS_TLD` | `.zip`, `.mov`, `.click`, `.top`, `.xyz`, `.loan` | 15 |
| `URL_SHORTENER` | bit.ly, tinyurl.com, t.co, goo.gl, shorturl.at | 10 |
| `BRAND_IMPERSONATION_HINT` | Brand-like token in suspicious URL context | 20 |

## Brand Impersonation Context

A brand finding requires a known brand token (e.g. paypal, google, microsoft) in the URL string together with at least one suspicious keyword or a suspicious TLD/shortener. Wording always suggests *possible* impersonation, never certainty.

## Stacking

Multiple rules can fire on one URL (e.g. long URL + very long URL + keywords). The score caps at 100.

## Limitations

- No live page content or reputation checks.
- No malware execution or credential harvesting.
- Educational static analysis only.
