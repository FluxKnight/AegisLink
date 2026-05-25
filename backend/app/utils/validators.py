from app.core.constants import MAX_URL_INPUT_LENGTH


def validate_url_input(url: str) -> str:
    cleaned = url.strip()
    if not cleaned:
        raise ValueError("URL cannot be empty.")
    if len(cleaned) > MAX_URL_INPUT_LENGTH:
        raise ValueError(f"URL exceeds maximum length of {MAX_URL_INPUT_LENGTH}.")
    if " " in cleaned:
        raise ValueError("URL cannot contain spaces.")
    return cleaned
