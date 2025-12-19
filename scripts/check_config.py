#!/usr/bin/env python3
"""Script de diagnostic de configuration pour la Plateforme NAO."""
import os
import sys
from urllib.parse import urlparse

def check_database_url():
    """Vérifie la configuration de DATABASE_URL."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ DATABASE_URL n'est pas définie")
        print("   → Configure DATABASE_URL dans tes variables d'environnement")
        return False

    # Parser l'URL
    parsed = urlparse(database_url)

    print(f"✅ DATABASE_URL est définie")
    print(f"   Schéma: {parsed.scheme}")
    print(f"   Hôte: {parsed.hostname}")
    print(f"   Port: {parsed.port}")
    print(f"   Base: {parsed.path.lstrip('/')}")

    # Vérifier si c'est localhost
    if parsed.hostname in ["localhost", "127.0.0.1", "::1"]:
        print("⚠️  WARNING: DATABASE_URL pointe vers localhost !")
        print("   → Sur Railway, utilise la DATABASE_URL du service PostgreSQL")
        print("   → Voir RAILWAY_DATABASE_FIX.md pour plus d'infos")
        return False

    # Vérifier si c'est Railway
    if "railway" in parsed.hostname:
        print("✅ DATABASE_URL pointe vers Railway")
        return True

    return True

def check_secret_key():
    """Vérifie la configuration de SECRET_KEY."""
    secret_key = os.getenv("SECRET_KEY")

    if not secret_key:
        print("❌ SECRET_KEY n'est pas définie")
        print("   → Génère une clé avec: python3 scripts/generate_secret_key.py")
        return False

    if len(secret_key) < 32:
        print("⚠️  SECRET_KEY est trop courte (< 32 caractères)")
        print("   → Génère une nouvelle clé avec: python3 scripts/generate_secret_key.py")
        return False

    if secret_key == "your_super_secret_key_change_this_in_production":
        print("⚠️  SECRET_KEY utilise la valeur par défaut !")
        print("   → Génère une nouvelle clé avec: python3 scripts/generate_secret_key.py")
        return False

    print("✅ SECRET_KEY est configurée correctement")
    return True

def check_cors_origins():
    """Vérifie la configuration de CORS_ORIGINS."""
    cors_origins = os.getenv("CORS_ORIGINS_STR")

    if not cors_origins:
        print("ℹ️  CORS_ORIGINS_STR n'est pas définie")
        print("   → Utilise les valeurs par défaut: localhost:3000, localhost:8000")
        return True

    origins = [o.strip() for o in cors_origins.split(",")]
    print(f"✅ CORS_ORIGINS_STR configurée avec {len(origins)} origine(s):")
    for origin in origins:
        print(f"   - {origin}")

    return True

def check_optional_config():
    """Vérifie les configurations optionnelles."""
    app_name = os.getenv("APP_NAME", "Plateforme NAO")
    debug = os.getenv("DEBUG", "False")

    print(f"ℹ️  APP_NAME: {app_name}")
    print(f"ℹ️  DEBUG: {debug}")

    if debug.lower() == "true":
        print("⚠️  DEBUG est activé - désactive en production !")

    # Email config (optionnel)
    smtp_host = os.getenv("SMTP_HOST")
    if smtp_host:
        print(f"✅ SMTP configuré: {smtp_host}")
    else:
        print("ℹ️  SMTP non configuré (optionnel)")

def main():
    """Fonction principale."""
    print("=" * 80)
    print("🔍 Diagnostic de configuration - Plateforme NAO")
    print("=" * 80)
    print()

    # Vérifier si on est sur Railway
    if os.getenv("RAILWAY_ENVIRONMENT"):
        print(f"🚂 Environnement Railway détecté: {os.getenv('RAILWAY_ENVIRONMENT')}")
        print()

    results = []

    print("📋 Configuration de base")
    print("-" * 80)
    results.append(("DATABASE_URL", check_database_url()))
    print()
    results.append(("SECRET_KEY", check_secret_key()))
    print()
    results.append(("CORS_ORIGINS", check_cors_origins()))
    print()

    print("📋 Configuration optionnelle")
    print("-" * 80)
    check_optional_config()
    print()

    print("=" * 80)

    # Résumé
    failed = [name for name, result in results if not result]

    if failed:
        print(f"❌ {len(failed)} problème(s) détecté(s): {', '.join(failed)}")
        print()
        print("📖 Voir la documentation:")
        print("   - RAILWAY_QUICKSTART.md pour le démarrage rapide")
        print("   - RAILWAY_DATABASE_FIX.md pour corriger DATABASE_URL")
        print("   - DEPLOYMENT_RAILWAY.md pour le guide complet")
        print("=" * 80)
        sys.exit(1)
    else:
        print("✅ Toutes les configurations critiques sont OK !")
        print("=" * 80)
        sys.exit(0)

if __name__ == "__main__":
    main()
