"""Calculators for NAO negotiations (salary, purchasing power, etc.)."""
from typing import Dict


def calculate_purchasing_power_loss(
    current_salary: float, years: int, annual_inflation: float = 2.0
) -> Dict:
    """
    Calculate purchasing power loss over years.

    Args:
        current_salary: Current monthly salary
        years: Number of years
        annual_inflation: Annual inflation rate (default 2%)

    Returns:
        Dictionary with loss details
    """
    # Calculate inflation multiplier
    inflation_multiplier = (1 + annual_inflation / 100) ** years

    # Calculate equivalent salary to maintain purchasing power
    equivalent_salary = current_salary * inflation_multiplier

    # Calculate loss
    loss_euros = equivalent_salary - current_salary
    loss_percentage = ((equivalent_salary - current_salary) / current_salary) * 100

    return {
        "current_salary": current_salary,
        "years": years,
        "annual_inflation": annual_inflation,
        "equivalent_salary": round(equivalent_salary, 2),
        "loss_euros": round(loss_euros, 2),
        "loss_percentage": round(loss_percentage, 2),
    }


def calculate_salary_increase(
    current_salary: float, increase_percentage: float
) -> Dict:
    """
    Calculate new salary after percentage increase.

    Args:
        current_salary: Current monthly salary
        increase_percentage: Increase percentage

    Returns:
        Dictionary with increase details
    """
    increase_euros = current_salary * (increase_percentage / 100)
    new_salary = current_salary + increase_euros
    annual_increase = increase_euros * 12

    return {
        "current_salary": round(current_salary, 2),
        "increase_percentage": increase_percentage,
        "increase_euros_monthly": round(increase_euros, 2),
        "new_salary": round(new_salary, 2),
        "annual_increase": round(annual_increase, 2),
    }


def calculate_employer_cost(
    employee_count: int, average_salary: float, increase_percentage: float
) -> Dict:
    """
    Calculate employer cost for salary increase.

    Args:
        employee_count: Number of employees
        average_salary: Average monthly salary
        increase_percentage: Increase percentage

    Returns:
        Dictionary with cost details
    """
    # Employer charges (approximately 45% in France)
    employer_charges_rate = 0.45

    # Calculate increase per employee
    increase_per_employee = average_salary * (increase_percentage / 100)
    charges_per_employee = increase_per_employee * employer_charges_rate

    # Total cost per employee (salary + charges)
    total_cost_per_employee = increase_per_employee + charges_per_employee

    # Annual cost
    monthly_cost = total_cost_per_employee * employee_count
    annual_cost = monthly_cost * 12

    return {
        "employee_count": employee_count,
        "average_salary": round(average_salary, 2),
        "increase_percentage": increase_percentage,
        "increase_per_employee": round(increase_per_employee, 2),
        "employer_charges_per_employee": round(charges_per_employee, 2),
        "total_cost_per_employee": round(total_cost_per_employee, 2),
        "monthly_cost_total": round(monthly_cost, 2),
        "annual_cost_total": round(annual_cost, 2),
    }


def compare_salary_inflation(
    current_salary: float, increase_percentage: float, inflation_rate: float
) -> Dict:
    """
    Compare salary increase with inflation.

    Args:
        current_salary: Current monthly salary
        increase_percentage: Proposed salary increase percentage
        inflation_rate: Current inflation rate

    Returns:
        Dictionary with comparison details
    """
    salary_increase = calculate_salary_increase(current_salary, increase_percentage)
    real_increase = increase_percentage - inflation_rate

    if real_increase > 0:
        verdict = "Augmentation supérieure à l'inflation"
        status = "positive"
    elif real_increase == 0:
        verdict = "Augmentation égale à l'inflation (pouvoir d'achat maintenu)"
        status = "neutral"
    else:
        verdict = "Augmentation inférieure à l'inflation (perte de pouvoir d'achat)"
        status = "negative"

    return {
        "current_salary": round(current_salary, 2),
        "increase_percentage": increase_percentage,
        "inflation_rate": inflation_rate,
        "real_increase_percentage": round(real_increase, 2),
        "new_salary": salary_increase["new_salary"],
        "verdict": verdict,
        "status": status,
    }
