# 🚀 Plateforme NAO - Négociations Annuelles Obligatoires

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/Deploy-Railway-blueviolet.svg)](https://railway.app/)

> **Plateforme web open-source pour lancer, suivre et documenter des campagnes NAO dans n'importe quelle organisation syndicale.**

Développée par et pour le mouvement syndical, cette application permet de générer automatiquement tous les documents nécessaires à une campagne NAO : revendications, lettres, tracts, communiqués de presse, pétitions, guides de mobilisation, et plus encore.

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Pourquoi cette plateforme ?](#-pourquoi-cette-plateforme-)
- [Architecture technique](#-architecture-technique)
- [Installation locale](#-installation-locale)
- [Déploiement sur Railway](#-déploiement-sur-railway)
- [Guide d'utilisation](#-guide-dutilisation)
- [Roadmap](#-roadmap)
- [Contribuer](#-contribuer)
- [Licence](#-licence)
- [Contact](#-contact)

---

## ✨ Fonctionnalités

### 🎯 Génération automatique de documents NAO

La plateforme génère instantanément un **pack complet de documents NAO** personnalisés :

#### 📄 Documents juridiques et officiels
- **Lettre d'ouverture des NAO** (article L.2242-1 Code du travail)
- **Revendications détaillées** avec bases juridiques
- **Réponse officielle à la Direction** après négociation
- **Motion de soutien CSE** prête à voter
- **Argumentaires juridiques** (Code du travail, conventions collectives)

#### 📢 Outils de communication
- **Tracts salarié·es** (format accessible et percutant)
- **Communiqué de presse** pour médias locaux
- **Guide de mobilisation** par profil de salarié·e
- **Pétition "prête à imprimer"** avec tableau de signatures
- **Publications réseaux sociaux** (Twitter, Facebook, LinkedIn)

#### 📊 Analyse et stratégie
- **Analyse des réponses de la Direction** (insuffisant/acceptable/flou)
- **Contre-argumentaires** détaillés par revendication
- **Plan d'action syndical progressif** (3 phases)
- **Tableau de suivi des négociations**

#### 🧮 Outils de calcul
- **Simulateur de perte de pouvoir d'achat**
- **Calculateur d'augmentation salariale** (comparaison inflation)
- **Estimation coût des revendications** pour l'employeur

### 🎨 Personnalisation complète

- Nom de l'établissement, secteur d'activité, effectifs
- Revendications modulables (salaires, congés, mutuelle, conditions de travail...)
- Contexte spécifique (accord de branche, convention collective)
- Charte graphique syndicale (couleurs, logos)
- Exports multiples : DOCX, PDF, HTML, Markdown

### 📈 Suivi de campagne

- **Tableau de bord** : état des revendications, dates de réunions, actions en cours
- **Historique** : comptes-rendus de réunions, positions Direction/syndicat
- **Indicateurs de mobilisation** : signatures pétitions, participation AG, actions menées
- **Base documentaire** : tous les documents générés archivés et accessibles

### 🔒 Multi-utilisateurs et confidentialité

- **Espaces séparés par organisation** (CGT Aveyron, CGT Hérault, SUD, etc.)
- **Gestion des droits** : admin, contributeur, lecteur
- **Données chiffrées** (respect RGPD)
- **Export de sauvegarde** complète

---

## 💡 Pourquoi cette plateforme ?

### 🎯 Le problème

Lancer une campagne NAO efficace demande :
- ⏰ **Du temps** : rédiger 10-15 documents différents
- 📚 **Des connaissances juridiques** : Code du travail, jurisprudence, conventions collectives
- ✍️ **De la rédaction** : argumentaires, tracts, communiqués percutants
- 📊 **De la méthode** : structurer la négociation, anticiper les réponses patronales
- 🔥 **De la mobilisation** : convaincre les salarié·es, organiser actions collectives

**Résultat** : Les petites sections syndicales ou les militant·es isolé·es peinent à mener des NAO de qualité, faute de ressources.

### ✅ La solution

Cette plateforme **automatise et mutualise** toute l'expertise nécessaire :

- 🚀 **Gain de temps** : générer un pack NAO complet en 5 minutes au lieu de plusieurs jours
- 📖 **Accès aux connaissances** : bases juridiques intégrées, jurisprudence à jour
- 🎯 **Qualité professionnelle** : documents rédigés par des militant·es expérimenté·es
- 🤝 **Mutualisation** : capitaliser sur l'expérience collective du mouvement syndical
- 💪 **Autonomie** : permettre à toute section syndicale de mener une NAO solide

### 🌍 Inspiration

Ce projet s'inspire du travail accompli avec le **PAP CSE Dashboard** (suivi des élections professionnelles en Occitanie), en appliquant la même logique de mutualisation et d'outillage numérique aux NAO.

---

## 🏗️ Architecture technique

### Stack

```
┌─────────────────────────────────────────┐
│            Frontend (Web UI)            │
│  HTML5 + TailwindCSS + Alpine.js        │
│  Templates Jinja2                        │
└─────────────────┬───────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────┐
│          Backend API (FastAPI)          │
│  Python 3.11+ | Pydantic | SQLAlchemy   │
│  Génération docs : python-docx, jinja2  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Base de données PostgreSQL      │
│  Organisations | Campagnes | Documents  │
│  Utilisateurs | Templates                │
└─────────────────────────────────────────┘
```

### Backend : FastAPI

**Pourquoi FastAPI ?**
- ⚡ Performance : asynchrone natif, génération de docs rapide
- 📖 Documentation auto : Swagger UI intégré (`/docs`)
- ✅ Validation : Pydantic pour validation automatique des données
- 🔐 Sécurité : OAuth2, JWT, CORS configurables
- 🐍 Python : écosystème riche (python-docx, ReportLab, Jinja2...)

**Structure backend**

```
app/
├── main.py                 # Point d'entrée FastAPI
├── config.py               # Configuration (env vars)
├── database.py             # SQLAlchemy setup
├── models/
│   ├── organization.py     # Modèle Organisation
│   ├── campaign.py         # Modèle Campagne NAO
│   ├── document.py         # Modèle Document généré
│   └── user.py             # Modèle Utilisateur
├── schemas/
│   ├── campaign.py         # Schémas Pydantic campagne
│   └── document.py         # Schémas Pydantic documents
├── routers/
│   ├── campaigns.py        # Routes CRUD campagnes
│   ├── documents.py        # Routes génération docs
│   └── auth.py             # Routes authentification
├── services/
│   ├── generator.py        # Service génération documents
│   ├── templates/          # Templates Jinja2 pour docs
│   │   ├── lettre_ouverture.j2
│   │   ├── revendications.j2
│   │   ├── tract.j2
│   │   └── ...
│   └── calculators.py      # Calculateurs (pouvoir achat, etc.)
└── utils/
    ├── docx_utils.py       # Helpers python-docx
    └── legal_refs.py       # Références juridiques (Code travail)
```

### Frontend : Simple et efficace

**Technologies**
- **HTML5 + Jinja2** : templates côté serveur
- **TailwindCSS** : styling moderne et responsive
- **Alpine.js** : interactions JS légères (< 15 KB)
- **HTMX** (optionnel) : pour interactions dynamiques sans SPA

**Pourquoi pas un frontend JS lourd (React/Vue) ?**
- 🎯 **Simplicité** : cible = militant·es syndicaux, pas développeurs
- ⚡ **Performance** : SSR (Server-Side Rendering) = chargement instantané
- 🔌 **Déploiement** : un seul serveur = moins de complexité
- ♿ **Accessibilité** : HTML sémantique = meilleur a11y

### Base de données : PostgreSQL

**Modèles principaux**

```python
# Organization (ex: CGT Aveyron, SUD Santé 34)
- id, name, sector, logo_url, color_scheme
- created_at, updated_at

# Campaign (campagne NAO)
- id, organization_id, title, establishment_name
- start_date, status (draft/active/closed)
- demands (JSON), context (JSON)
- created_at, updated_at

# Document (document généré)
- id, campaign_id, type (lettre/tract/petition...)
- content (text), format (docx/pdf/html)
- generated_at, downloaded_at

# User (utilisateur)
- id, email, hashed_password, role (admin/contributor/reader)
- organization_id, created_at, last_login
```

### Déploiement : Railway

**Pourquoi Railway ?**
- 🚂 **Simplicité** : deploy en 1 clic depuis GitHub
- 💰 **Gratuit** : plan Hobby gratuit (500h/mois)
- 🔌 **PostgreSQL inclus** : addon natif
- 🌍 **Domaine custom** : possibilité d'avoir nao.cgt-aveyron.fr
- 📊 **Logs et monitoring** : interface claire

---

## 🛠️ Installation locale

### Prérequis

- Python 3.11+
- PostgreSQL 14+
- pip / pipenv / poetry

### 1. Cloner le repo

```bash
git clone https://github.com/ton-username/plateforme-nao.git
cd plateforme-nao
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances principales** (voir `requirements.txt` complet) :

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.31
psycopg2-binary==2.9.9
alembic==1.13.2
pydantic==2.8.2
pydantic-settings==2.4.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9

# Génération de documents
python-docx==1.1.2
Jinja2==3.1.4
reportlab==4.2.2  # Pour génération PDF

# Frontend
Jinja2==3.1.4
```

### 4. Configuration

Créer un fichier `.env` à la racine :

```env
# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/plateforme_nao

# Secret JWT (générer avec : openssl rand -hex 32)
SECRET_KEY=votre_secret_key_super_securisee

# Configuration app
APP_NAME="Plateforme NAO"
APP_VERSION="1.0.0"
DEBUG=True

# Email (optionnel, pour envoi docs par email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-app
```

### 5. Initialiser la base de données

```bash
# Créer les tables
alembic upgrade head

# (Optionnel) Charger données de démo
python scripts/seed_demo_data.py
```

### 6. Lancer le serveur

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

🎉 **L'application est disponible sur** : http://localhost:8000

📖 **Documentation API** : http://localhost:8000/docs

---

## 🚀 Déploiement sur Railway

### Méthode 1 : Via l'interface Railway (recommandé)

1. **Créer un compte** : https://railway.app/
2. **Nouveau projet** : "New Project" → "Deploy from GitHub repo"
3. **Connecter le repo** : Sélectionner `plateforme-nao`
4. **Ajouter PostgreSQL** : "+ New" → "Database" → "Add PostgreSQL"
5. **Variables d'environnement** :
   - Railway détecte automatiquement `DATABASE_URL` depuis PostgreSQL
   - Ajouter les autres variables :
     ```
     SECRET_KEY=votre_secret_key
     APP_NAME=Plateforme NAO
     DEBUG=False
     ```
6. **Deploy** : Railway build et deploy automatiquement
7. **Domaine custom** (optionnel) :
   - Settings → Domains → Generate Domain (ou custom domain)

### Méthode 2 : Via Railway CLI

```bash
# Installer Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialiser le projet
railway init

# Ajouter PostgreSQL
railway add --plugin postgresql

# Set variables d'environnement
railway variables set SECRET_KEY=votre_secret_key

# Deploy
railway up
```

### Configuration Railway

Créer un fichier `railway.toml` :

```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "on-failure"
restartPolicyMaxRetries = 10
```

### Migrations automatiques

Railway exécute automatiquement `alembic upgrade head` au démarrage (via `startCommand`).

Pour créer une nouvelle migration en local :

```bash
alembic revision --autogenerate -m "Description de la migration"
git add . && git commit -m "Migration: description"
git push
# Railway redéploie automatiquement
```

---

## 📖 Guide d'utilisation

### 1. Créer une campagne NAO

**Interface Web :**
1. Se connecter
2. "Nouvelle campagne NAO"
3. Remplir le formulaire :
   - Nom établissement : "Sainte Claire"
   - Secteur : "Santé"
   - Effectif : 120 salarié·es
   - Convention collective : 51 (Établissements privés à but non lucratif)
   - Date ouverture NAO : 10/12/2024

**API :**

```bash
curl -X POST "http://localhost:8000/api/campaigns" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "NAO 2025 - Sainte Claire",
    "establishment_name": "Sainte Claire",
    "sector": "Santé",
    "employee_count": 120,
    "collective_agreement": "51",
    "start_date": "2024-12-10"
  }'
```

### 2. Définir les revendications

**Revendications modulables** :

- ✅ **Salaires** : augmentation générale, prime ancienneté, grille salariale
- ✅ **Congés** : jours enfants malades, jours aidant, congés supplémentaires
- ✅ **Protection sociale** : mutuelle, prévoyance
- ✅ **Conditions de travail** : plan prévention TMS/RPS, équipements, coupés
- ✅ **Temps de travail** : pointeuse, flexibilité, télétravail
- ✅ **Égalité** : égalité salariale F/H, mixité
- ✅ **Autres** : budget CSE, formation, mobilité...

**Exemple de saisie** :

```json
{
  "demands": {
    "salaries": {
      "enabled": true,
      "general_increase": 3.0,  // %
      "seniority_bonus": true,
      "salary_grid_update": true
    },
    "leaves": {
      "enabled": true,
      "sick_children_days": 3,
      "caregiver_days": 3,
      "paid": true
    },
    "health_insurance": {
      "enabled": true,
      "employer_contribution": 80  // %
    },
    "working_conditions": {
      "enabled": true,
      "prevention_plan": true,
      "equipment_renewal": true,
      "shift_split_removal": true
    }
  }
}
```

### 3. Générer le pack de documents

**Un clic = tous les documents** :

Interface : Bouton "Générer pack NAO complet"

La plateforme génère instantanément :
- 📄 Lettre d'ouverture NAO
- 📋 Revendications détaillées (9 pages avec bases juridiques)
- 🗳️ Motion CSE
- 📢 Tract salarié·es
- 📰 Communiqué de presse
- 📝 Pétition
- 📊 Guide mobilisation
- ⚖️ Argumentaires juridiques
- 📈 Plan d'action syndical

**Formats disponibles** : DOCX, PDF, HTML, Markdown

### 4. Suivre la négociation

Après chaque réunion Direction :

1. **Ajouter compte-rendu** : importer ou saisir les réponses de la Direction
2. **Analyse automatique** : la plateforme génère :
   - Tableau récapitulatif (revendication | réponse Direction | analyse CGT)
   - Contre-argumentaires adaptés
   - Réponse officielle à la Direction
   - Nouveau tract pour informer les salarié·es
3. **Actualiser plan d'action** selon l'évolution

### 5. Mobiliser

La plateforme fournit :
- 📊 **Simulateur pouvoir d'achat** personnalisé par salarié·e
- 📝 **Pétition** avec compteur de signatures
- 🎤 **Scripts de réunion d'information** (AG)
- 📱 **Posts réseaux sociaux** prêts à publier
- 📞 **Guide de porte-à-porte** / discussions individuelles

---

## 🗺️ Roadmap

### Version 1.0 (MVP) - Q1 2025 ✅ En cours

- [x] Génération pack NAO complet (9 documents)
- [x] Interface de création campagne
- [x] Exports DOCX/PDF
- [x] Authentification utilisateurs
- [ ] Déploiement Railway
- [ ] Documentation complète

### Version 1.1 - Q2 2025

- [ ] Suivi de négociation (comptes-rendus de réunions)
- [ ] Analyse automatique réponses Direction
- [ ] Génération contre-argumentaires adaptatifs
- [ ] Tableau de bord campagne

### Version 1.2 - Q3 2025

- [ ] Multi-organisations (espaces séparés)
- [ ] Gestion des droits utilisateurs (admin/contributeur/lecteur)
- [ ] Templates personnalisables
- [ ] Charte graphique par organisation

### Version 2.0 - Q4 2025

- [ ] Module "Mobilisation" :
  - Pétition en ligne avec signatures
  - Compteur de mobilisation
  - Planning d'actions
- [ ] Intégration email (envoi automatique docs)
- [ ] Exports avancés (ODT, slides Reveal.js)
- [ ] Base de données jurisprudence NAO

### Version 3.0 - 2026

- [ ] Analyse de convention collective automatique
- [ ] Comparateur inter-branches
- [ ] Module "Accords d'entreprise"
- [ ] API publique pour intégrations
- [ ] Mobile app (React Native)

---

## 🤝 Contribuer

Ce projet est **open-source et collaboratif** ! Toutes les contributions sont bienvenues.

### Comment contribuer ?

1. **Fork** le projet
2. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
3. Commit : `git commit -m 'Ajout de ma fonctionnalité'`
4. Push : `git push origin feature/ma-fonctionnalite`
5. Ouvrir une **Pull Request**

### Types de contributions

- 🐛 **Bugs** : signaler ou corriger
- ✨ **Fonctionnalités** : proposer ou développer
- 📖 **Documentation** : améliorer le README, guides, exemples
- 🎨 **Design** : améliorer l'UX/UI
- ⚖️ **Juridique** : enrichir les bases légales, jurisprudence
- 🌍 **Traduction** : traduire l'interface (anglais, espagnol...)

### Code de conduite

Ce projet suit le code de conduite du mouvement syndical : **solidarité, respect, entraide**.

---

## 📜 Licence

Ce projet est sous licence **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### Pourquoi l'AGPL ?

L'AGPL garantit que :
- ✅ Le code reste **libre et ouvert**
- ✅ Toute modification doit être **partagée** (même si hébergée sur un serveur)
- ✅ Impossibilité de créer une version propriétaire fermée
- ✅ Protection contre la récupération par des acteurs anti-syndicaux

**En résumé** : si quelqu'un améliore cette plateforme, tout le monde en bénéficie.

---

## 📞 Contact

### Mainteneur principal

**Quentin Leyrat** - CGT Aveyron  
Conseiller confédéral, développeur de la plateforme

- 🌐 Site : [À compléter]
- 📧 Email : [À compléter]
- 💬 Mastodon : [À compléter]

### Organisations partenaires

Cette plateforme est développée en collaboration avec :
- **CGT Occitanie** : retours terrain, besoins utilisateurs
- **[Autres organisations syndicales]** : [À compléter]

### Support

- 🐛 **Bugs / Questions** : ouvrir une issue sur GitHub
- 💬 **Discussions** : [Forum / Discord / Matrix] [À compléter]
- 📖 **Documentation** : voir `/docs` ou https://nao-docs.example.com

---

## 🙏 Remerciements

Un immense merci à :

- **Les militant·es CGT Aveyron** pour les retours et tests terrain
- **Les camarades du PAP CSE Dashboard** pour l'inspiration et la méthodologie
- **Tous les contributeurs et contributrices** qui feront vivre ce projet
- **Le mouvement syndical** pour son combat quotidien pour les droits des travailleur·ses

---

## 🔗 Liens utiles

### Ressources syndicales

- [CGT Nationale](https://www.cgt.fr/)
- [CGT Occitanie](https://www.cgt-occitanie.org/)
- [Code du travail numérique](https://code.travail.gouv.fr/)
- [Legifrance - Code du travail](https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006072050/)

### Outils similaires

- **PAP CSE Dashboard** : suivi élections professionnelles (même développeur)
- [À compléter : autres outils syndicaux open-source]

### Technologies utilisées

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [python-docx](https://python-docx.readthedocs.io/)
- [TailwindCSS](https://tailwindcss.com/)
- [Railway](https://railway.app/)

---

**✊ Ensemble, outillons le mouvement syndical pour des NAO ambitieuses et gagnantes ! ✊**

---

<p align="center">
  <i>Développé avec ❤️ et ✊ par et pour les travailleur·ses</i>
</p>
