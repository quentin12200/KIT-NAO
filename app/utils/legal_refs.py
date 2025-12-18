"""Legal references from French labor code (Code du travail)."""

CODE_TRAVAIL = {
    "L2242-1": {
        "title": "Négociation annuelle obligatoire - Thèmes",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035652899",
        "text": (
            "Dans les entreprises où sont constituées une ou plusieurs sections syndicales "
            "d'organisations représentatives, l'employeur engage au moins une fois tous les "
            "quatre ans une négociation sur la rémunération, notamment les salaires effectifs, "
            "le temps de travail et le partage de la valeur ajoutée dans l'entreprise."
        ),
    },
    "L2242-2": {
        "title": "NAO - Rémunération et temps de travail",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035652901",
        "text": (
            "La négociation annuelle sur la rémunération, le temps de travail et le partage "
            "de la valeur ajoutée dans l'entreprise porte sur les salaires effectifs, "
            "la durée effective et l'organisation du temps de travail, notamment la mise "
            "en place du travail à temps partiel."
        ),
    },
    "L2242-3": {
        "title": "NAO - Égalité professionnelle",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035652903",
        "text": (
            "La négociation annuelle obligatoire porte également sur l'égalité professionnelle "
            "entre les femmes et les hommes et la qualité de vie au travail."
        ),
    },
    "L2242-5": {
        "title": "NAO - Obligation de négocier",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035652907",
        "text": (
            "L'employeur est tenu de convoquer les organisations syndicales à la négociation "
            "prévue aux articles L. 2242-1 et L. 2242-2."
        ),
    },
    "L2242-8": {
        "title": "Périodicité des négociations",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035652913",
        "text": (
            "La négociation annuelle obligatoire peut se tenir à une périodicité différente "
            "de la périodicité annuelle si un accord d'entreprise le prévoit."
        ),
    },
    "L3221-3": {
        "title": "Égalité de rémunération femmes-hommes",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006902836",
        "text": (
            "Tout employeur assure, pour un même travail ou pour un travail de valeur égale, "
            "l'égalité de rémunération entre les femmes et les hommes."
        ),
    },
    "L3141-1": {
        "title": "Droit aux congés payés",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033020517",
        "text": (
            "Tout salarié a droit chaque année à un congé payé à la charge de l'employeur."
        ),
    },
    "L1225-65": {
        "title": "Congé pour enfant malade",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006900927",
        "text": (
            "Le salarié bénéficie d'un congé non rémunéré en cas de maladie ou d'accident, "
            "constatés par certificat médical, d'un enfant de moins de seize ans dont il "
            "assume la charge au sens de l'article L. 513-1 du code de la sécurité sociale."
        ),
    },
    "L4121-1": {
        "title": "Obligation de sécurité de l'employeur",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035640828",
        "text": (
            "L'employeur prend les mesures nécessaires pour assurer la sécurité et protéger "
            "la santé physique et mentale des travailleurs."
        ),
    },
    "L4121-2": {
        "title": "Principes généraux de prévention",
        "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035640830",
        "text": (
            "L'employeur met en œuvre les mesures prévues à l'article L. 4121-1 sur le "
            "fondement des principes généraux de prévention suivants : éviter les risques, "
            "évaluer les risques, combattre les risques à la source..."
        ),
    },
}


CONVENTION_COLLECTIVE_51 = {
    "title": "Convention collective nationale des établissements privés d'hospitalisation, "
    "de soins, de cure et de garde à but non lucratif du 31 octobre 1951",
    "idcc": "51",
    "url": "https://www.legifrance.gouv.fr/conv_coll/id/KALICONT000005635407",
    "salaire_minimum": {
        "2024": {
            "niveau_1": 1766.92,
            "niveau_2": 1855.27,
            "niveau_3": 1943.61,
            "description": "Salaires minima mensuels bruts au 1er janvier 2024",
        }
    },
}


def get_code_article(article_code: str) -> dict:
    """Get a Code du travail article by its code."""
    return CODE_TRAVAIL.get(article_code, {})


def format_legal_reference(article_code: str) -> str:
    """Format a legal reference for inclusion in documents."""
    article = get_code_article(article_code)
    if not article:
        return f"Article {article_code} du Code du travail"

    return f"Article {article_code} du Code du travail - {article['title']}"


def get_all_nao_articles() -> list:
    """Get all articles related to NAO."""
    nao_articles = ["L2242-1", "L2242-2", "L2242-3", "L2242-5", "L2242-8"]
    return [get_code_article(code) for code in nao_articles]
