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

📖 Guide complet : [DEPLOYMENT_RAILWAY.md](./DEPLOYMENT_RAILWAY.md)
