# 🚂 Railway Quickstart - Plateforme NAO

## Configuration Rapide (5 minutes)

### 1. Sur Railway

1. **Nouveau Projet** → Deploy from GitHub → Sélectionne `KIT-NAO`
2. **Ajouter PostgreSQL** : + New → Database → PostgreSQL
3. **Générer SECRET_KEY** :
   ```bash
   python3 scripts/generate_secret_key.py
   ```
4. **Ajouter Variables** (Settings → Variables) :
   ```
   SECRET_KEY=<la_clé_générée>
   APP_NAME=Plateforme NAO
   DEBUG=False
   ```
5. **Générer Domaine** : Settings → Domains → Generate Domain

### 2. Tester

- **API** : https://ton-app.railway.app/docs
- **Health** : https://ton-app.railway.app/health

### 3. Créer Premier Utilisateur

Via Swagger UI (`/docs`) → `POST /api/auth/register` :
```json
{
  "email": "admin@exemple.fr",
  "password": "MotDePasseSecurise123!",
  "full_name": "Administrateur",
  "role": "admin"
}
```

✅ **C'est tout ! Ton app est déployée.**

---

## 🔧 Dépannage

### Erreur : "Connection refused" PostgreSQL

Si tu vois cette erreur dans les logs :
```
connection to server at "localhost" failed: Connection refused
```

➡️ **Consulte le guide** : [RAILWAY_DATABASE_FIX.md](./RAILWAY_DATABASE_FIX.md)

**Solution rapide** :
1. Va sur le service **PostgreSQL** → Variables
2. Copie la variable `DATABASE_URL`
3. Va sur le service **KIT-NAO** → Variables
4. Ajoute une référence vers `DATABASE_URL` du service Postgres

### Vérifier la configuration

Lance le script de diagnostic :
```bash
python3 scripts/check_config.py
```

---

📖 Guides complets :
- [RAILWAY_DATABASE_FIX.md](./RAILWAY_DATABASE_FIX.md) - Corriger la connexion PostgreSQL
- [DEPLOYMENT_RAILWAY.md](./DEPLOYMENT_RAILWAY.md) - Guide de déploiement détaillé
