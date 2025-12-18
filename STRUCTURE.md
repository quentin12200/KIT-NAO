# 📁 Structure du projet Plateforme NAO

```
plateforme-nao/
│
├── app/                                # Application FastAPI
│   ├── __init__.py
│   ├── main.py                         # Point d'entrée FastAPI
│   ├── config.py                       # Configuration (env vars, settings)
│   ├── database.py                     # SQLAlchemy setup
│   │
│   ├── models/                         # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── organization.py             # Modèle Organisation syndicale
│   │   ├── campaign.py                 # Modèle Campagne NAO
│   │   ├── document.py                 # Modèle Document généré
│   │   ├── user.py                     # Modèle Utilisateur
│   │   └── meeting.py                  # Modèle Réunion de négociation
│   │
│   ├── schemas/                        # Schémas Pydantic (validation)
│   │   ├── __init__.py
│   │   ├── organization.py
│   │   ├── campaign.py
│   │   ├── document.py
│   │   ├── user.py
│   │   └── auth.py
│   │
│   ├── routers/                        # Routes API
│   │   ├── __init__.py
│   │   ├── campaigns.py                # CRUD campagnes
│   │   ├── documents.py                # Génération documents
│   │   ├── meetings.py                 # Suivi réunions
│   │   ├── organizations.py            # Gestion organisations
│   │   ├── auth.py                     # Authentification
│   │   └── admin.py                    # Routes admin
│   │
│   ├── services/                       # Logique métier
│   │   ├── __init__.py
│   │   ├── generator.py                # Service génération documents
│   │   ├── calculator.py               # Calculateurs (pouvoir achat, etc.)
│   │   ├── analyzer.py                 # Analyse réponses Direction
│   │   └── email_service.py            # Envoi emails
│   │
│   ├── templates/                      # Templates Jinja2
│   │   │
│   │   ├── documents/                  # Templates documents NAO
│   │   │   ├── lettre_ouverture.j2
│   │   │   ├── revendications.j2
│   │   │   ├── motion_cse.j2
│   │   │   ├── tract.j2
│   │   │   ├── communique_presse.j2
│   │   │   ├── petition.j2
│   │   │   ├── reponse_direction.j2
│   │   │   └── argumentaires.j2
│   │   │
│   │   └── web/                        # Templates pages web
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── campaign_list.html
│   │       ├── campaign_detail.html
│   │       ├── campaign_create.html
│   │       └── dashboard.html
│   │
│   ├── utils/                          # Utilitaires
│   │   ├── __init__.py
│   │   ├── docx_utils.py               # Helpers python-docx
│   │   ├── pdf_utils.py                # Génération PDF
│   │   ├── legal_refs.py               # Références Code du travail
│   │   ├── auth.py                     # Utils authentification
│   │   └── validators.py               # Validateurs custom
│   │
│   └── static/                         # Fichiers statiques
│       ├── css/
│       │   └── styles.css              # Styles (ou Tailwind compilé)
│       ├── js/
│       │   └── app.js                  # JavaScript (Alpine.js)
│       └── img/
│           ├── logo.png
│           └── illustrations/
│
├── alembic/                            # Migrations base de données
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/                              # Tests
│   ├── __init__.py
│   ├── conftest.py                     # Configuration pytest
│   ├── test_campaigns.py
│   ├── test_documents.py
│   ├── test_generator.py
│   └── test_auth.py
│
├── docs/                               # Documentation
│   ├── api.md                          # Documentation API
│   ├── deployment.md                   # Guide déploiement
│   ├── user_guide.md                   # Guide utilisateur
│   └── developer_guide.md              # Guide développeur
│
├── scripts/                            # Scripts utilitaires
│   ├── seed_demo_data.py               # Données de démo
│   ├── export_templates.py             # Export templates
│   └── backup_db.py                    # Sauvegarde DB
│
├── .github/                            # GitHub Actions
│   └── workflows/
│       ├── tests.yml                   # CI : tests auto
│       └── deploy.yml                  # CD : déploiement Railway
│
├── README.md                           # Documentation principale
├── CONTRIBUTING.md                     # Guide contribution
├── LICENSE                             # Licence AGPL-3.0
├── STRUCTURE.md                        # Ce fichier
│
├── requirements.txt                    # Dépendances Python
├── requirements-dev.txt                # Dépendances dev (pytest, black...)
│
├── .env.example                        # Variables d'environnement (exemple)
├── .gitignore                          # Fichiers ignorés par Git
├── railway.toml                        # Configuration Railway
├── alembic.ini                         # Configuration Alembic
└── pytest.ini                          # Configuration pytest
```

## 🗂️ Description des dossiers

### `/app` - Application principale

**`main.py`** : Point d'entrée FastAPI
- Initialisation de l'app
- Configuration CORS, middleware
- Inclusion des routers
- Routes root (`/`, `/health`)

**`config.py`** : Configuration centralisée
- Settings Pydantic
- Variables d'environnement
- Configuration par environnement (dev/prod)

**`database.py`** : Setup SQLAlchemy
- Engine PostgreSQL
- SessionLocal
- Base déclarative

### `/app/models` - Modèles de données

Tables SQL (via SQLAlchemy ORM) :

- **Organization** : organisations syndicales (CGT Aveyron, SUD...)
- **Campaign** : campagnes NAO
- **Document** : documents générés
- **User** : utilisateurs
- **Meeting** : réunions de négociation
- **Demand** : revendications détaillées (relation avec Campaign)

### `/app/schemas` - Validation des données

Schémas Pydantic pour validation entrées/sorties API :

- `CampaignCreate`, `CampaignResponse`
- `DocumentGenerate`, `DocumentResponse`
- `UserCreate`, `UserLogin`, `Token`

### `/app/routers` - Routes API

Endpoints REST :

```python
# Campaigns
GET    /api/campaigns           # Liste des campagnes
POST   /api/campaigns           # Créer campagne
GET    /api/campaigns/{id}      # Détail campagne
PUT    /api/campaigns/{id}      # Modifier campagne
DELETE /api/campaigns/{id}      # Supprimer campagne

# Documents
POST   /api/campaigns/{id}/documents/generate    # Générer documents
GET    /api/campaigns/{id}/documents             # Liste documents
GET    /api/documents/{id}/download              # Télécharger document

# Auth
POST   /api/auth/register       # Inscription
POST   /api/auth/login          # Connexion (JWT)
GET    /api/auth/me             # Profil utilisateur
```

### `/app/services` - Logique métier

Services réutilisables :

**`generator.py`** :
- `generate_letter_ouverture(campaign)` → DOCX
- `generate_revendications(campaign)` → DOCX
- `generate_tract(campaign)` → DOCX
- `generate_all_documents(campaign)` → ZIP

**`calculator.py`** :
- `calculate_purchasing_power_loss(salary, years)` → dict
- `calculate_salary_increase(current, target_increase)` → float

**`analyzer.py`** :
- `analyze_direction_response(response)` → dict
- `generate_counter_arguments(demands, responses)` → list

### `/app/templates` - Templates Jinja2

**Documents NAO** (`/templates/documents/`) :
- Variables : `{{ campaign.establishment_name }}`
- Conditions : `{% if demands.leaves.enabled %}`
- Boucles : `{% for demand in demands %}`

**Pages web** (`/templates/web/`) :
- Layout de base : `base.html`
- Pages héritent : `{% extends "base.html" %}`

### `/app/utils` - Utilitaires

**`docx_utils.py`** :
```python
def add_styled_paragraph(doc, text, style='Normal')
def add_table_with_data(doc, headers, rows)
def set_document_margins(doc, top, bottom, left, right)
```

**`legal_refs.py`** :
```python
CODE_TRAVAIL = {
    "L2242-1": {
        "title": "Négociation annuelle obligatoire",
        "url": "https://...",
        "text": "..."
    }
}
```

### `/alembic` - Migrations DB

Gestion des évolutions du schéma de base de données :

```bash
# Créer une migration
alembic revision --autogenerate -m "Add meeting table"

# Appliquer les migrations
alembic upgrade head

# Revenir en arrière
alembic downgrade -1
```

### `/tests` - Tests automatisés

```python
# tests/test_campaigns.py
def test_create_campaign():
    response = client.post("/api/campaigns", json={...})
    assert response.status_code == 201

# tests/test_generator.py
def test_generate_letter():
    doc = generate_letter_ouverture(campaign)
    assert len(doc.paragraphs) > 10
```

### `/docs` - Documentation

- **api.md** : Documentation de l'API REST (ou auto-générée via Swagger)
- **deployment.md** : Guide déploiement Railway, configuration domaine
- **user_guide.md** : Guide utilisateur (captures d'écran, tutoriels)
- **developer_guide.md** : Architecture, choix techniques, conventions

### `/scripts` - Scripts maintenance

**`seed_demo_data.py`** :
```python
# Créer une campagne de démo pour tester
python scripts/seed_demo_data.py
```

**`backup_db.py`** :
```python
# Sauvegarder la base de données
python scripts/backup_db.py --output backup.sql
```

## 🔄 Flux de données

```
1. Utilisateur remplit formulaire "Nouvelle campagne NAO"
   ↓
2. Frontend envoie POST /api/campaigns
   ↓
3. Router campaigns.py reçoit la requête
   ↓
4. Schéma Pydantic valide les données (CampaignCreate)
   ↓
5. Modèle Campaign créé et sauvegardé en DB
   ↓
6. Réponse JSON (CampaignResponse) renvoyée
   ↓
7. Utilisateur clique "Générer documents"
   ↓
8. Frontend envoie POST /api/campaigns/{id}/documents/generate
   ↓
9. Service generator.py :
   - Charge le template Jinja2
   - Remplit avec données campagne
   - Génère DOCX via python-docx
   ↓
10. Document sauvegardé en DB + fichier sur disque
   ↓
11. Lien de téléchargement renvoyé
```

## 📦 Déploiement

### En local (dev)

```bash
# 1. Cloner et setup
git clone https://github.com/ton-username/plateforme-nao.git
cd plateforme-nao
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configuration
cp .env.example .env
# Éditer .env

# 3. Base de données
createdb plateforme_nao
alembic upgrade head

# 4. Lancer
uvicorn app.main:app --reload
```

### Sur Railway (prod)

```bash
# 1. Créer projet Railway
railway init

# 2. Ajouter PostgreSQL
railway add --plugin postgresql

# 3. Variables d'env
railway variables set SECRET_KEY=xxx

# 4. Deploy
git push
# Railway build et deploy automatiquement
```

## 🧪 Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=app tests/

# Un seul fichier
pytest tests/test_campaigns.py

# Mode verbeux
pytest -v
```

## 🎨 Frontend

### Stack minimal

- **HTML5** : structure sémantique
- **TailwindCSS** : styling (via CDN ou compilé)
- **Alpine.js** : interactivité légère (< 15 KB)

### Exemple de composant Alpine.js

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Contenu</div>
</div>
```

### Pages principales

1. **`/`** : Page d'accueil
2. **`/campaigns`** : Liste campagnes
3. **`/campaigns/new`** : Créer campagne
4. **`/campaigns/{id}`** : Détail campagne + génération docs
5. **`/campaigns/{id}/meetings`** : Suivi réunions
6. **`/dashboard`** : Tableau de bord (stats, actions)

## 📚 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [python-docx](https://python-docx.readthedocs.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [Alembic](https://alembic.sqlalchemy.org/)

---

✊ **Structure conçue pour être simple, maintenable et extensible !**
