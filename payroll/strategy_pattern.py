"""
Strategy Pattern Implementation for Payroll Calculations
Different strategies for calculating allowances, deductions, and taxes
"""
from abc import ABC, abstractmethod
from typing import List
from domain_models import Payroll, SalaryComponent


# Strategy Interface
class CalculationStrategy(ABC):
    """Abstract strategy for payroll calculations"""
    @abstractmethod
    def calculate(self, payroll: Payroll) -> float:
        pass


# Concrete Strategies for Allowances
class FixedAllowanceStrategy(CalculationStrategy):
    """Strategy for fixed amount allowances"""
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate(self, payroll: Payroll) -> float:
        return self.amount


class PercentageAllowanceStrategy(CalculationStrategy):
    """Strategy for percentage-based allowances"""
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, payroll: Payroll) -> float:
        return (payroll.basic_salary * self.percentage) / 100.0


class TieredAllowanceStrategy(CalculationStrategy):
    """Strategy for tiered allowances based on salary ranges"""
    def __init__(self, tiers: List[tuple]):
        """
        tiers: List of (min_salary, max_salary, percentage) tuples
        """
        self.tiers = tiers
    
    def calculate(self, payroll: Payroll) -> float:
        for min_sal, max_sal, percentage in self.tiers:
            if min_sal <= payroll.basic_salary <= max_sal:
                return (payroll.basic_salary * percentage) / 100.0
        return 0.0


# Concrete Strategies for Deductions
class FixedDeductionStrategy(CalculationStrategy):
    """Strategy for fixed amount deductions"""
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate(self, payroll: Payroll) -> float:
        return self.amount


class PercentageDeductionStrategy(CalculationStrategy):
    """Strategy for percentage-based deductions"""
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, payroll: Payroll) -> float:
        return (payroll.basic_salary * self.percentage) / 100.0


class ProgressiveTaxStrategy(CalculationStrategy):
    """Strategy for progressive tax calculation"""
    def __init__(self, tax_brackets: List[tuple]):
        """
        tax_brackets: List of (min_income, max_income, rate) tuples
        """
        self.tax_brackets = sorted(tax_brackets, key=lambda x: x[0])
    
    def calculate(self, payroll: Payroll) -> float:
        taxable_income = payroll.basic_salary + payroll.calculate_total_allowances()
        tax = 0.0
        remaining_income = taxable_income
        
        for min_income, max_income, rate in self.tax_brackets:
            if remaining_income <= 0:
                break
            if taxable_income > min_income:
                bracket_income = min(remaining_income, max_income - min_income)
                tax += (bracket_income * rate) / 100.0
                remaining_income -= bracket_income
        
        return tax


# Context class that uses strategies
class PayrollCalculator:
    """Context class that uses calculation strategies"""
    def __init__(self):
        self.allowance_strategies: List[CalculationStrategy] = []
        self.deduction_strategies: List[CalculationStrategy] = []
    
    def add_allowance_strategy(self, strategy: CalculationStrategy):
        """Add an allowance calculation strategy"""
        self.allowance_strategies.append(strategy)
    
    def add_deduction_strategy(self, strategy: CalculationStrategy):
        """Add a deduction calculation strategy"""
        self.deduction_strategies.append(strategy)
    
    def calculate_total_allowances(self, payroll: Payroll) -> float:
        """Calculate total allowances using all strategies"""
        total = 0.0
        for strategy in self.allowance_strategies:
            total += strategy.calculate(payroll)
        return total
    
    def calculate_total_deductions(self, payroll: Payroll) -> float:
        """Calculate total deductions using all strategies"""
        total = 0.0
        for strategy in self.deduction_strategies:
            total += strategy.calculate(payroll)
        return total
    
    def calculate_net_salary(self, payroll: Payroll) -> float:
        """Calculate net salary using all strategies"""
        allowances = self.calculate_total_allowances(payroll)
        deductions = self.calculate_total_deductions(payroll)
        return payroll.basic_salary + allowances - deductions

