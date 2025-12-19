# 🔧 Correction de la connexion PostgreSQL sur Railway

## Problème
```
connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

**Cause** : La variable `DATABASE_URL` pointe vers `localhost` au lieu du service PostgreSQL de Railway.

## Solution en 3 étapes

### Étape 1 : Trouver la bonne DATABASE_URL

1. **Va sur ton projet Railway**
2. **Clique sur le service PostgreSQL** (icône violette avec "Postgres")
3. **Va dans l'onglet "Variables"**
4. **Cherche la variable `DATABASE_URL`** ou `DATABASE_PUBLIC_URL`

   Elle ressemble à ça :
   ```
   postgresql://postgres:XXXXXXX@postgres.railway.internal:5432/railway
   ```

5. **Clique sur l'icône de copie** 📋 à côté de la valeur

### Étape 2 : Lier les services (si pas déjà fait)

1. **Retourne sur le service "KIT-NAO"** (ton application FastAPI)
2. **Va dans "Settings"**
3. **Scroll jusqu'à "Service Variables"**
4. **Clique sur "+ New Variable"**
5. **Clique sur "Add Reference"**
6. **Sélectionne le service PostgreSQL**
7. **Sélectionne `DATABASE_URL`**

✅ Railway va automatiquement injecter la bonne URL !

### Étape 3 : Alternative manuelle

Si l'étape 2 ne fonctionne pas :

1. **Va dans le service KIT-NAO**
2. **Onglet "Variables"**
3. **Si `DATABASE_URL` existe déjà** :
   - Clique sur les 3 points ⋮
   - "Edit"
   - Remplace par la valeur copiée à l'étape 1
4. **Si `DATABASE_URL` n'existe pas** :
   - Clique "+ New Variable"
   - Nom : `DATABASE_URL`
   - Valeur : colle la valeur de l'étape 1
5. **Clique "Add"**

## Redémarrage

Railway va automatiquement redémarrer ton service. Attends ~1-2 minutes.

## Vérification

1. **Va dans "Deployments"**
2. **Clique sur le dernier déploiement**
3. **Vérifie les logs** - tu devrais voir :
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

4. **Teste l'API** :
   - Va sur `https://ton-app.railway.app/health`
   - Tu devrais voir : `{"status": "ok"}`

## Encore des problèmes ?

### Vérifier que PostgreSQL tourne

1. **Clique sur le service PostgreSQL**
2. **Vérifie qu'il est "Active" (vert)**
3. **Si rouge/jaune** : attends qu'il redémarre

### Vérifier les variables

Dans le service KIT-NAO, tu dois avoir AU MINIMUM :
```
DATABASE_URL=postgresql://postgres:...@postgres.railway.internal:5432/railway
SECRET_KEY=ton_secret_key_généré
```

Variables optionnelles mais recommandées :
```
DEBUG=False
APP_NAME=Plateforme NAO
CORS_ORIGINS_STR=https://ton-frontend.com,https://autre-domaine.com
```

## Format de DATABASE_URL

✅ **CORRECT** (Railway) :
```
postgresql://postgres:PASSWORD@postgres.railway.internal:5432/railway
```

❌ **INCORRECT** (localhost) :
```
postgresql://user:password@localhost:5432/plateforme_nao
```

## Notes importantes

- Railway génère automatiquement la DATABASE_URL pour le service PostgreSQL
- Utilise toujours la référence de service plutôt que de copier-coller manuellement
- Si tu recrées le service PostgreSQL, la DATABASE_URL changera
- Ne partage JAMAIS ta DATABASE_URL publiquement (elle contient le mot de passe)
