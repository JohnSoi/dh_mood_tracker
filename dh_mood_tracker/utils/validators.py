import re


def email_validator(email: str) -> bool:
    PATTERN: str = r"^(?!\.)(?!.*\.\.)([A-Za-z0-9\._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})$"
    return bool(re.match(PATTERN, email))
