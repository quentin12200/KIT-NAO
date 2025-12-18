#!/bin/bash
# Script de configuration locale pour développement

echo "🚀 Configuration locale de la Plateforme NAO"
echo "=============================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✅ Python détecté : $(python3 --version)"

# Créer environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Copier .env.example si .env n'existe pas
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env

    # Générer SECRET_KEY
    echo "🔐 Génération de SECRET_KEY..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

    # Remplacer dans .env (macOS et Linux compatible)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your_super_secret_key_change_this_in_production/$SECRET_KEY/g" .env
    else
        # Linux
        sed -i "s/your_super_secret_key_change_this_in_production/$SECRET_KEY/g" .env
    fi

    echo "✅ Fichier .env créé avec SECRET_KEY générée"
    echo "⚠️  N'oublie pas de configurer DATABASE_URL dans .env"
else
    echo "ℹ️  Fichier .env existe déjà"
fi

# Créer le dossier uploads
mkdir -p uploads

echo ""
echo "✅ Configuration terminée !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Configure DATABASE_URL dans .env"
echo "2. Crée la base de données : createdb plateforme_nao"
echo "3. Lance les migrations : alembic upgrade head"
echo "4. Démarre l'app : uvicorn app.main:app --reload"
echo ""
