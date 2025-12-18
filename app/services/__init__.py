"""Services package."""
from app.services.calculator import (
    calculate_purchasing_power_loss,
    calculate_salary_increase,
    calculate_employer_cost,
    compare_salary_inflation,
)
from app.services.analyzer import (
    analyze_response_sentiment,
    analyze_direction_response,
    generate_counter_arguments,
    generate_action_plan,
)
from app.services.generator import (
    generate_letter_ouverture,
    generate_revendications,
    generate_tract,
    generate_all_documents,
)

__all__ = [
    "calculate_purchasing_power_loss",
    "calculate_salary_increase",
    "calculate_employer_cost",
    "compare_salary_inflation",
    "analyze_response_sentiment",
    "analyze_direction_response",
    "generate_counter_arguments",
    "generate_action_plan",
    "generate_letter_ouverture",
    "generate_revendications",
    "generate_tract",
    "generate_all_documents",
]
