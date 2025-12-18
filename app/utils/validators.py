"""Custom validators for the application."""
from typing import Optional
import re


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.

    Returns:
        (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"

    if not re.search(r"[a-z]", password):
        return False, "Le mot de passe doit contenir au moins une lettre minuscule"

    if not re.search(r"[A-Z]", password):
        return False, "Le mot de passe doit contenir au moins une lettre majuscule"

    if not re.search(r"\d", password):
        return False, "Le mot de passe doit contenir au moins un chiffre"

    return True, None


def validate_hex_color(color: str) -> bool:
    """Validate hex color format (#RRGGBB)."""
    pattern = r"^#[0-9A-Fa-f]{6}$"
    return bool(re.match(pattern, color))


def validate_siret(siret: str) -> bool:
    """Validate French SIRET number (14 digits)."""
    if not siret.isdigit() or len(siret) != 14:
        return False

    # Luhn algorithm for SIRET validation
    total = 0
    for i, digit in enumerate(siret):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0
