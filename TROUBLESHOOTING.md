# 🔧 Guide de dépannage - Plateforme NAO

## Problèmes courants et solutions

### 1. Erreur de connexion PostgreSQL

**Symptômes** :
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError)
connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

**Cause** : DATABASE_URL pointe vers localhost au lieu du service Railway PostgreSQL.

**Solution** : 👉 [RAILWAY_DATABASE_FIX.md](./RAILWAY_DATABASE_FIX.md)

---

### 2. Erreur CORS / JSON parsing

**Symptômes** :
```
pydantic_settings.sources.SettingsError: error parsing value for field "CORS_ORIGINS"
JSONDecodeError: Expecting value: line 1 column 1
```

**Cause** : Format incorrect de la variable CORS_ORIGINS.

**Solution** :
- Utilise `CORS_ORIGINS_STR` au lieu de `CORS_ORIGINS`
- Format : `https://domain1.com,https://domain2.com` (séparé par des virgules)
- Exemple :
  ```
  CORS_ORIGINS_STR=https://mon-frontend.vercel.app,https://www.monsite.fr
  ```

---

### 3. SECRET_KEY manquante ou invalide

**Symptômes** :
```
ValidationError: SECRET_KEY field required
```

**Solution** :
```bash
# Générer une clé sécurisée
python3 scripts/generate_secret_key.py

# Ajouter sur Railway :
# Settings → Variables → + New Variable
# Nom : SECRET_KEY
# Valeur : [la clé générée]
```

---

### 4. Erreur de migration Alembic

**Symptômes** :
```
alembic.util.exc.CommandError: Can't locate revision identified by 'xxxx'
```

**Solution** :
```bash
# Réinitialiser les migrations
alembic stamp head

# Ou créer une nouvelle migration
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

### 5. Port déjà utilisé (développement local)

**Symptômes** :
```
OSError: [Errno 48] Address already in use
```

**Solution** :
```bash
# Trouver le processus
lsof -i :8000

# Tuer le processus
kill -9 [PID]

# Ou utiliser un autre port
uvicorn app.main:app --reload --port 8001
```

---

### 6. Module non trouvé

**Symptômes** :
```
ModuleNotFoundError: No module named 'app'
```

**Solution** :
```bash
# Vérifier que tu es dans le bon répertoire
pwd  # Doit afficher .../KIT-NAO

# Vérifier l'environnement virtuel
which python  # Doit pointer vers venv/bin/python

# Réinstaller les dépendances
pip install -r requirements.txt
```

---

## Scripts de diagnostic

### Vérifier la configuration

```bash
python3 scripts/check_config.py
```

Ce script vérifie :
- ✅ DATABASE_URL (format et destination)
- ✅ SECRET_KEY (présence et sécurité)
- ✅ CORS_ORIGINS_STR
- ℹ️  Variables optionnelles (SMTP, DEBUG, etc.)

### Générer SECRET_KEY

```bash
python3 scripts/generate_secret_key.py
```

Génère une clé sécurisée de 64 caractères pour l'authentification JWT.

### Configuration locale

```bash
./scripts/setup_local.sh
```

Configure automatiquement :
- Environnement virtuel Python
- Fichier .env avec SECRET_KEY
- Dossier uploads
- Dépendances

---

## Logs utiles

### Sur Railway

1. Va sur ton service **KIT-NAO**
2. Onglet **Deployments**
3. Clique sur le dernier déploiement
4. Consulte les logs en temps réel

### En local

```bash
# Lancer avec logs détaillés
uvicorn app.main:app --reload --log-level debug

# Logs SQLAlchemy
# Dans .env, ajoute :
DEBUG=True
```

---

## Checklist de déploiement Railway

Avant de déployer, vérifie que tu as :

- [ ] Service PostgreSQL créé et actif
- [ ] DATABASE_URL référencée depuis le service Postgres
- [ ] SECRET_KEY générée et configurée
- [ ] CORS_ORIGINS_STR configurée (si nécessaire)
- [ ] railway.toml présent à la racine
- [ ] requirements.txt à jour
- [ ] Alembic configuré (alembic.ini + migrations/)

---

## Besoin d'aide ?

1. **Vérifie les logs** sur Railway
2. **Lance le script de diagnostic** : `python3 scripts/check_config.py`
3. **Consulte les guides** :
   - [RAILWAY_QUICKSTART.md](./RAILWAY_QUICKSTART.md) - Démarrage rapide
   - [RAILWAY_DATABASE_FIX.md](./RAILWAY_DATABASE_FIX.md) - Fix DATABASE_URL
   - [DEPLOYMENT_RAILWAY.md](./DEPLOYMENT_RAILWAY.md) - Guide complet
4. **Vérifie les variables d'environnement** sur Railway

---

## Variables d'environnement requises

### Minimales (obligatoires)

```bash
DATABASE_URL=postgresql://postgres:...@postgres.railway.internal:5432/railway
SECRET_KEY=votre_cle_secrete_de_64_caracteres
```

### Recommandées

```bash
APP_NAME=Plateforme NAO
DEBUG=False
CORS_ORIGINS_STR=https://votre-frontend.com
```

### Optionnelles

```bash
# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre.email@gmail.com
SMTP_PASSWORD=votre_mot_de_passe
SMTP_FROM=noreply@plateforme-nao.fr

# Fichiers
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=10485760  # 10 MB en octets
```
