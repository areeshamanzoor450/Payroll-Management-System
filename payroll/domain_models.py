"""
Domain Models implementing OOP relationships:
- Aggregation: Employee aggregates Payroll records
- Composition: Payroll composed of Salary components
- Association: Employee associated with Attendance
- Dependency: Models depend on abstractions
"""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional


# Dependency: Abstract base for data access
class IRepository(ABC):
    """Abstract repository interface - Dependency Inversion Principle"""
    @abstractmethod
    def save(self, entity): pass
    
    @abstractmethod
    def find_by_id(self, entity_id): pass
    
    @abstractmethod
    def find_all(self): pass


# Information Expert: SalaryComponent knows how to calculate itself
class SalaryComponent:
    """Component representing a salary component (allowance/deduction)"""
    def __init__(self, name: str, amount: float, is_percentage: bool = False, base_amount: float = 0.0):
        self.name = name
        self.amount = amount
        self.is_percentage = is_percentage
        self.base_amount = base_amount
    
    def calculate(self) -> float:
        """Information Expert: Component calculates its own value"""
        if self.is_percentage:
            return (self.base_amount * self.amount) / 100.0
        return self.amount
    
    def __repr__(self):
        return f"{self.name}: {self.calculate():.2f}"


# Composition: Payroll is composed of SalaryComponents
class Payroll:
    """Payroll entity - Composition relationship with SalaryComponents"""
    def __init__(self, payroll_id: Optional[int], employee_id: int, pay_date: date,
                 basic_salary: float, allowances: List[SalaryComponent] = None,
                 deductions: List[SalaryComponent] = None):
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.pay_date = pay_date
        self.basic_salary = basic_salary
        self.allowances = allowances or []
        self.deductions = deductions or []
    
    def calculate_total_allowances(self) -> float:
        """Information Expert: Payroll knows how to calculate its allowances"""
        total = 0.0
        for allowance in self.allowances:
            allowance.base_amount = self.basic_salary
            total += allowance.calculate()
        return total
    
    def calculate_total_deductions(self) -> float:
        """Information Expert: Payroll knows how to calculate its deductions"""
        total = 0.0
        for deduction in self.deductions:
            deduction.base_amount = self.basic_salary
            total += deduction.calculate()
        return total
    
    def calculate_net_salary(self) -> float:
        """Information Expert: Payroll calculates its own net salary"""
        return self.basic_salary + self.calculate_total_allowances() - self.calculate_total_deductions()


# Aggregation: Employee aggregates Payroll records (Employee has Payrolls)
class Employee:
    """Employee entity - Aggregation relationship with Payroll"""
    def __init__(self, employee_id: Optional[int], first_name: str, last_name: str,
                 email: str, position: str, department: str, base_salary: float, hire_date: date):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.position = position
        self.department = department
        self.base_salary = base_salary
        self.hire_date = hire_date
        self._payroll_records: List[Payroll] = []  # Aggregation: Employee has Payroll records
    
    def add_payroll(self, payroll: Payroll):
        """Aggregation: Employee can have multiple Payroll records"""
        if payroll.employee_id == self.employee_id:
            self._payroll_records.append(payroll)
    
    def get_payroll_records(self) -> List[Payroll]:
        """Get all payroll records for this employee"""
        return self._payroll_records.copy()
    
    def get_full_name(self) -> str:
        """Information Expert: Employee knows its own full name"""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"Employee({self.employee_id}, {self.get_full_name()}, {self.department})"


# Association: Employee associated with Attendance (many-to-many relationship)
class Attendance:
    """Attendance entity - Association relationship with Employee"""
    def __init__(self, attendance_id: Optional[int], employee_id: int, date: date,
                 status: str, hours_worked: float):
        self.attendance_id = attendance_id
        self.employee_id = employee_id
        self.date = date
        self.status = status
        self.hours_worked = hours_worked
    
    def is_present(self) -> bool:
        """Information Expert: Attendance knows its own status"""
        return self.status.lower() == 'present'
    
    def __repr__(self):
        return f"Attendance({self.attendance_id}, Employee:{self.employee_id}, {self.date}, {self.status})"


# Composition: Department composed of Employees
class Department:
    """Department entity - Composition relationship with Employees"""
    def __init__(self, name: str):
        self.name = name
        self._employees: List[Employee] = []  # Composition: Department owns Employees
    
    def add_employee(self, employee: Employee):
        """Composition: Department manages its employees"""
        if employee.department == self.name:
            self._employees.append(employee)
    
    def get_employees(self) -> List[Employee]:
        """Get all employees in this department"""
        return self._employees.copy()
    
    def calculate_total_salary(self) -> float:
        """Information Expert: Department calculates total salary"""
        return sum(emp.base_salary for emp in self._employees)
    
    def __repr__(self):
        return f"Department({self.name}, {len(self._employees)} employees)"

