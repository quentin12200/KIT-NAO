#!/usr/bin/env python3
"""Generate a secure SECRET_KEY for the application."""
import secrets

if __name__ == "__main__":
    secret_key = secrets.token_hex(32)
    print("=" * 80)
    print("🔐 SECRET_KEY générée pour l'application Plateforme NAO")
    print("=" * 80)
    print()
    print(f"SECRET_KEY={secret_key}")
    print()
    print("📋 Instructions :")
    print("1. Copie la ligne ci-dessus")
    print("2. Sur Railway : Settings → Variables")
    print("3. Ajoute SECRET_KEY avec cette valeur")
    print()
    print("⚠️  IMPORTANT : Ne partage JAMAIS cette clé publiquement !")
    print("=" * 80)
