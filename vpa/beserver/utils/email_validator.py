import re
import logging

logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    """
    Validate an email address using a robust regex pattern.
    Returns True if valid, False otherwise.
    """
    if not email:
        return False

    # This regex allows letters, numbers, underscores, dots, plus, and hyphens in the local part
    # It allows letters, numbers, hyphens in the domain, and multiple subdomains
    pattern = re.compile(
        r"^[a-zA-Z0-9_.+-]+@"        # local part
        r"[a-zA-Z0-9-]+\."           # domain
        r"[a-zA-Z0-9-.]+$"           # top-level domain
    )

    return bool(pattern.fullmatch(email))



