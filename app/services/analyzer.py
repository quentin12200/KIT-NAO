"""Analyzer for management responses during NAO negotiations."""
from typing import Dict, List


def analyze_response_sentiment(response_text: str) -> str:
    """
    Analyze sentiment of management response.

    Args:
        response_text: Management response text

    Returns:
        Sentiment: "positive", "negative", or "neutral"
    """
    response_lower = response_text.lower()

    # Positive keywords
    positive_keywords = [
        "accepte",
        "accord",
        "favorable",
        "oui",
        "d'accord",
        "augmentation",
        "amélioration",
    ]

    # Negative keywords
    negative_keywords = [
        "refuse",
        "non",
        "impossible",
        "rejet",
        "défavorable",
        "ne peut pas",
        "ne peux pas",
    ]

    # Count keywords
    positive_count = sum(
        1 for keyword in positive_keywords if keyword in response_lower
    )
    negative_count = sum(
        1 for keyword in negative_keywords if keyword in response_lower
    )

    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"


def analyze_direction_response(demands: Dict, responses: Dict) -> List[Dict]:
    """
    Analyze management responses to union demands.

    Args:
        demands: Dictionary of union demands
        responses: Dictionary of management responses

    Returns:
        List of analysis dictionaries
    """
    analysis = []

    for demand_key, demand_value in demands.items():
        if not demand_value.get("enabled", False):
            continue

        response = responses.get(demand_key, {})
        response_text = response.get("text", "Pas de réponse")
        sentiment = analyze_response_sentiment(response_text)

        # Categorize response
        if sentiment == "positive":
            category = "Accepté"
            action = "Formaliser l'accord par écrit"
        elif sentiment == "negative":
            category = "Refusé"
            action = "Préparer contre-argumentaire et mobilisation"
        else:
            category = "Flou / À préciser"
            action = "Demander clarification écrite"

        analysis.append(
            {
                "demand": demand_key,
                "demand_title": demand_value.get("title", demand_key),
                "response_text": response_text,
                "sentiment": sentiment,
                "category": category,
                "recommended_action": action,
            }
        )

    return analysis


def generate_counter_arguments(demand_type: str, context: Dict = None) -> List[str]:
    """
    Generate counter-arguments for common management objections.

    Args:
        demand_type: Type of demand (salaries, leaves, etc.)
        context: Additional context

    Returns:
        List of counter-arguments
    """
    counter_args = {
        "salaries": [
            "L'augmentation demandée compense à peine l'inflation des dernières années",
            "Les salarié·es ont maintenu la productivité malgré les conditions difficiles",
            "Une augmentation salariale améliore la motivation et réduit le turnover",
            "Le Code du travail (L2242-2) impose une négociation annuelle sur les salaires",
        ],
        "leaves": [
            "Les congés pour enfants malades sont prévus par l'article L1225-65",
            "Ces congés améliorent la qualité de vie au travail et la fidélisation",
            "La charge de travail peut être réorganisée pour absorber ces absences",
            "D'autres entreprises du secteur ont déjà mis en place ces mesures",
        ],
        "health_insurance": [
            "Une bonne mutuelle réduit l'absentéisme pour raisons de santé",
            "C'est un élément de rémunération attractif à coût maîtrisé",
            "La contribution employeur peut être échelonnée sur plusieurs années",
            "Obligation de qualité de vie au travail (article L2242-3)",
        ],
        "working_conditions": [
            "L'employeur a une obligation de sécurité (article L4121-1)",
            "Un plan de prévention réduit les accidents du travail et les arrêts",
            "Des équipements adaptés améliorent la productivité",
            "Les TMS et RPS génèrent des coûts importants pour l'entreprise",
        ],
    }

    return counter_args.get(
        demand_type,
        [
            "Cette revendication améliore les conditions de travail des salarié·es",
            "C'est une mesure d'équité et de justice sociale",
            "Le dialogue social est essentiel pour l'avenir de l'entreprise",
        ],
    )


def generate_action_plan(analysis: List[Dict]) -> Dict:
    """
    Generate action plan based on analysis.

    Args:
        analysis: List of demand analyses

    Returns:
        Dictionary with action plan
    """
    accepted = [a for a in analysis if a["category"] == "Accepté"]
    refused = [a for a in analysis if a["category"] == "Refusé"]
    unclear = [a for a in analysis if a["category"] == "Flou / À préciser"]

    # Determine mobilization level
    if len(refused) > len(accepted):
        mobilization_level = "Fort"
        actions = [
            "Organiser une Assemblée Générale pour informer les salarié·es",
            "Lancer une pétition de soutien aux revendications",
            "Diffuser un tract expliquant les positions de la Direction",
            "Préparer une action symbolique (débrayage, rassemblement)",
            "Demander une nouvelle réunion de négociation",
        ]
    elif len(unclear) > 3:
        mobilization_level = "Modéré"
        actions = [
            "Envoyer un courrier demandant des clarifications",
            "Organiser une réunion d'information syndicale",
            "Préparer les contre-argumentaires",
            "Maintenir la pression via les élus CSE",
        ]
    else:
        mobilization_level = "Léger"
        actions = [
            "Formaliser les accords obtenus par écrit",
            "Communiquer les avancées aux salarié·es",
            "Rester vigilant sur la mise en œuvre",
            "Préparer la prochaine échéance de négociation",
        ]

    return {
        "accepted_count": len(accepted),
        "refused_count": len(refused),
        "unclear_count": len(unclear),
        "mobilization_level": mobilization_level,
        "recommended_actions": actions,
    }
