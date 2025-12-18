# 🚂 Guide de Déploiement Railway - Plateforme NAO

## 📋 Prérequis

- Compte Railway : https://railway.app/
- Code pushé sur GitHub

## 🚀 Étapes de Déploiement

### 1. Créer un Nouveau Projet Railway

1. Va sur https://railway.app/
2. Clique sur **"New Project"**
3. Sélectionne **"Deploy from GitHub repo"**
4. Choisis le repo `KIT-NAO`
5. Sélectionne la branche `claude/continue-structure-work-GpIcf` (ou `main`)

### 2. Ajouter PostgreSQL

1. Dans ton projet Railway, clique sur **"+ New"**
2. Sélectionne **"Database"** → **"Add PostgreSQL"**
3. Railway créera automatiquement une base PostgreSQL
4. La variable `DATABASE_URL` sera automatiquement disponible

### 3. Configurer les Variables d'Environnement

Dans Railway, va dans **Settings** → **Variables** et ajoute :

#### Variables Obligatoires

```bash
# Secret pour JWT (générer avec: openssl rand -hex 32)
SECRET_KEY=ton_secret_key_super_securise_a_generer

# Application
APP_NAME=Plateforme NAO
APP_VERSION=1.0.0
DEBUG=False

# CORS (optionnel, Railway fournit l'URL)
CORS_ORIGINS=https://ton-app.railway.app,http://localhost:3000
```

#### Variables Optionnelles (Email)

```bash
# Configuration Email (si besoin)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ton-email@gmail.com
SMTP_PASSWORD=ton-mot-de-passe-app
SMTP_FROM=noreply@plateforme-nao.org
```

### 4. Générer une SECRET_KEY Sécurisée

**Option A : Via OpenSSL (recommandé)**
```bash
openssl rand -hex 32
```

**Option B : Via Python**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie le résultat et ajoute-le comme variable `SECRET_KEY` sur Railway.

### 5. Vérifier la Configuration

Le fichier `railway.toml` est déjà configuré avec :

```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "on-failure"
restartPolicyMaxRetries = 10
```

Cela signifie que Railway va :
1. ✅ Installer les dépendances Python
2. ✅ Exécuter les migrations Alembic automatiquement
3. ✅ Lancer l'application FastAPI

### 6. Déployer

Railway déploie automatiquement dès que tu push sur GitHub :

```bash
git push origin claude/continue-structure-work-GpIcf
```

Railway détecte le push et redéploie automatiquement.

### 7. Accéder à l'Application

1. Dans Railway, va dans **Settings** → **Domains**
2. Clique sur **"Generate Domain"**
3. Railway génère une URL : `https://ton-app.railway.app`
4. L'application est accessible à cette URL

### 8. Tester l'API

Une fois déployé :

- **Application** : https://ton-app.railway.app/
- **Documentation Swagger** : https://ton-app.railway.app/docs
- **Health Check** : https://ton-app.railway.app/health

### 9. Créer un Premier Utilisateur

**Via l'API Swagger** :
1. Va sur `https://ton-app.railway.app/docs`
2. Trouve `POST /api/auth/register`
3. Clique sur "Try it out"
4. Entre :
```json
{
  "email": "admin@cgt.fr",
  "password": "MotDePasseSecurise123!",
  "full_name": "Admin CGT",
  "role": "admin"
}
```
5. Exécute et récupère le token

**Via curl** :
```bash
curl -X POST "https://ton-app.railway.app/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cgt.fr",
    "password": "MotDePasseSecurise123!",
    "full_name": "Admin CGT",
    "role": "admin"
  }'
```

### 10. Se Connecter

```bash
curl -X POST "https://ton-app.railway.app/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@cgt.fr&password=MotDePasseSecurise123!"
```

Tu recevras un token JWT à utiliser pour les requêtes authentifiées.

## 🔍 Monitoring et Logs

### Voir les Logs
1. Dans Railway, clique sur ton service
2. Onglet **"Logs"**
3. Logs en temps réel de l'application

### Métriques
- **CPU** : Utilisation processeur
- **Memory** : Utilisation mémoire
- **Network** : Trafic réseau

## 🔧 Commandes Utiles

### Via Railway CLI

```bash
# Installer Railway CLI
npm i -g @railway/cli

# Login
railway login

# Lier au projet
railway link

# Voir les logs
railway logs

# Ouvrir dans le navigateur
railway open
```

## 🐛 Dépannage

### Problème : L'application ne démarre pas

**Solution** : Vérifie les logs Railway
- `railway logs` pour voir les erreurs
- Vérifie que `SECRET_KEY` est configurée
- Vérifie que `DATABASE_URL` est présente (fournie automatiquement par PostgreSQL)

### Problème : Migrations Alembic échouent

**Solution** :
```bash
# Se connecter via Railway CLI
railway run bash

# Vérifier les migrations
alembic current

# Forcer la migration
alembic upgrade head
```

### Problème : Erreur de connexion à la base

**Solution** :
- Vérifie que PostgreSQL est bien ajouté au projet
- Railway fournit automatiquement `DATABASE_URL`
- Redémarre le service

## 📦 Domaine Personnalisé (Optionnel)

Pour utiliser ton propre domaine (ex: nao.cgt-aveyron.fr) :

1. Dans Railway : **Settings** → **Domains** → **Custom Domain**
2. Ajoute ton domaine : `nao.cgt-aveyron.fr`
3. Railway te donne un CNAME à configurer
4. Chez ton registrar (OVH, Gandi, etc.) :
   - Ajoute un enregistrement CNAME
   - Pointe vers le domaine Railway

## 🔄 Mises à Jour

Pour déployer une nouvelle version :

```bash
# 1. Faire tes modifications
# 2. Commit
git add .
git commit -m "Description des changements"

# 3. Push
git push origin claude/continue-structure-work-GpIcf

# Railway redéploie automatiquement !
```

## 💰 Tarification

- **Hobby Plan** : Gratuit avec 500h/mois (suffisant pour démarrer)
- **Pro Plan** : $5/mois/service (pour production)

## ✅ Checklist Post-Déploiement

- [ ] PostgreSQL ajouté au projet
- [ ] SECRET_KEY configurée
- [ ] Domain généré
- [ ] Application accessible via l'URL
- [ ] Health check fonctionne : `/health`
- [ ] Documentation accessible : `/docs`
- [ ] Premier utilisateur créé
- [ ] Connexion JWT testée
- [ ] Première campagne NAO créée (test)

---

🎉 **Ton application Plateforme NAO est maintenant déployée sur Railway !**
