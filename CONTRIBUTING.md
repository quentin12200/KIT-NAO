# 🤝 Guide de contribution

Merci de vouloir contribuer à la Plateforme NAO ! Ce guide vous explique comment participer au projet.

## 🎯 Types de contributions

### 🐛 Signaler un bug

1. Vérifier que le bug n'est pas déjà signalé dans les [Issues](https://github.com/votre-repo/issues)
2. Créer une nouvelle issue avec le template "Bug Report"
3. Décrire :
   - Ce que vous faisiez
   - Ce que vous attendiez
   - Ce qui s'est passé
   - Comment reproduire le bug

### ✨ Proposer une fonctionnalité

1. Ouvrir une issue avec le template "Feature Request"
2. Expliquer :
   - Quel problème ça résout
   - Comment ça devrait fonctionner
   - Des exemples d'utilisation

### 📖 Améliorer la documentation

- Corriger des fautes
- Clarifier des explications
- Ajouter des exemples
- Traduire (anglais, espagnol...)

### 💻 Contribuer du code

## 🛠️ Setup développement

### 1. Fork et clone

```bash
# Fork le repo sur GitHub, puis :
git clone https://github.com/votre-username/plateforme-nao.git
cd plateforme-nao
```

### 2. Environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer dépendances

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Outils dev (pytest, black, flake8)
```

### 4. Configuration

```bash
cp .env.example .env
# Éditer .env avec vos paramètres locaux
```

### 5. Base de données

```bash
# Créer la DB PostgreSQL
createdb plateforme_nao

# Appliquer les migrations
alembic upgrade head
```

### 6. Lancer les tests

```bash
pytest
```

### 7. Lancer le serveur

```bash
uvicorn app.main:app --reload
```

## 📝 Workflow de contribution

### 1. Créer une branche

```bash
git checkout -b feature/ma-fonctionnalite
# ou
git checkout -b fix/correction-bug
```

**Conventions de nommage des branches :**
- `feature/nom-fonctionnalite` : nouvelle fonctionnalité
- `fix/nom-bug` : correction de bug
- `docs/nom-doc` : documentation
- `refactor/nom` : refactoring

### 2. Développer

- Écrire du code clair et commenté
- Suivre les conventions Python (PEP 8)
- Ajouter des tests si nécessaire
- Mettre à jour la documentation

### 3. Formater le code

```bash
# Auto-formatting avec Black
black app/ tests/

# Vérifier avec Flake8
flake8 app/ tests/
```

### 4. Tester

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app tests/
```

### 5. Commit

```bash
git add .
git commit -m "feat: ajout génération tract personnalisé"
```

**Convention de commit (Conventional Commits) :**
- `feat:` : nouvelle fonctionnalité
- `fix:` : correction de bug
- `docs:` : documentation
- `style:` : formatage (sans changement de code)
- `refactor:` : refactoring
- `test:` : ajout/modification de tests
- `chore:` : maintenance (deps, config...)

### 6. Push

```bash
git push origin feature/ma-fonctionnalite
```

### 7. Pull Request

1. Aller sur GitHub → onglet "Pull Requests"
2. "New Pull Request"
3. Remplir la description :
   - Qu'est-ce que ça fait ?
   - Pourquoi c'est nécessaire ?
   - Comment tester ?
4. Lier à une issue si applicable (ex: "Closes #42")

## ✅ Checklist avant PR

- [ ] Le code fonctionne localement
- [ ] Les tests passent (`pytest`)
- [ ] Le code est formaté (`black` + `flake8`)
- [ ] La documentation est à jour
- [ ] Les commits suivent la convention
- [ ] La PR a une description claire

## 🎨 Standards de code

### Python

- **PEP 8** : style guide Python standard
- **Type hints** : utiliser autant que possible
- **Docstrings** : pour toutes les fonctions publiques

```python
def generate_document(campaign_id: int, doc_type: str) -> dict:
    """
    Génère un document pour une campagne NAO.
    
    Args:
        campaign_id: ID de la campagne
        doc_type: Type de document (lettre, tract, petition...)
    
    Returns:
        dict: Document généré avec content, format, etc.
    
    Raises:
        CampaignNotFoundError: Si la campagne n'existe pas
        InvalidDocTypeError: Si le type de doc est invalide
    """
    pass
```

### Structure des routes FastAPI

```python
@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Campaign:
    """Créer une nouvelle campagne NAO."""
    # Logique ici
    pass
```

### Tests

```python
def test_create_campaign():
    """Test de création d'une campagne."""
    response = client.post("/api/campaigns", json={
        "title": "NAO 2025 - Test",
        "establishment_name": "Test Corp"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "NAO 2025 - Test"
```

## ⚖️ Juridique et contenu

### Références légales

Quand tu ajoutes des références juridiques :
- Citer l'article exact du Code du travail
- Indiquer la version/date (ex: "Version en vigueur au 01/01/2025")
- Ajouter un lien Legifrance si possible

### Templates de documents

- Les templates doivent être **génériques** (adaptables à tout établissement)
- Utiliser des **variables Jinja2** pour personnalisation
- Inclure des **commentaires explicatifs** pour les militant·es

Exemple :

```jinja2
{# Ce paragraphe concerne les jours enfants malades #}
{% if demands.leaves.sick_children_days > 0 %}
La CGT revendique l'instauration de {{ demands.leaves.sick_children_days }} jours
pour enfants malades, conformément à l'article L.1225-61 du Code du travail.
{% endif %}
```

## 🌍 Traductions

Pour traduire l'interface :

1. Les chaînes à traduire sont dans `app/locales/`
2. Format : fichiers JSON par langue

```json
// fr.json
{
  "campaign.create": "Créer une campagne",
  "document.generate": "Générer les documents"
}

// en.json
{
  "campaign.create": "Create campaign",
  "document.generate": "Generate documents"
}
```

## 🔒 Sécurité

### Signaler une vulnérabilité

**NE PAS** ouvrir une issue publique pour une faille de sécurité !

Envoyer un email à : [security@plateforme-nao.fr]

Inclure :
- Description de la vulnérabilité
- Impact potentiel
- Étapes pour reproduire
- Suggestion de correctif (si possible)

### Bonnes pratiques

- Ne jamais commit de secrets (clés API, mots de passe...)
- Utiliser `.env` pour les secrets locaux
- Valider toutes les entrées utilisateur
- Utiliser des paramètres Pydantic avec validation

## 📞 Questions ?

- 💬 **Discussions** : [Forum / Discord] [À compléter]
- 📧 **Email** : [contact@plateforme-nao.fr]
- 🐛 **Issues** : https://github.com/votre-repo/issues

## 🙏 Merci !

Chaque contribution, petite ou grande, aide à renforcer les outils du mouvement syndical. Merci de prendre le temps de contribuer ! ✊

---

**Code de conduite** : Ce projet suit les valeurs du mouvement syndical : solidarité, respect, entraide.
