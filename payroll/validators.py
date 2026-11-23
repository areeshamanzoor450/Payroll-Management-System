"""
Validation classes following Single Responsibility Principle
Separates validation logic from business logic
"""
from abc import ABC, abstractmethod
from typing import Optional
from domain_models import Employee, Payroll, Attendance


class Validator(ABC):
    """Abstract validator interface"""
    @abstractmethod
    def validate(self, entity) -> tuple[bool, Optional[str]]:
        """Returns (is_valid, error_message)"""
        pass


class EmployeeValidator(Validator):
    """Validator for Employee entities - Single Responsibility Principle"""
    
    def validate(self, employee: Employee) -> tuple[bool, Optional[str]]:
        """Validate employee data"""
        if not employee.first_name or not employee.first_name.strip():
            return False, "First name is required"
        
        if not employee.last_name or not employee.last_name.strip():
            return False, "Last name is required"
        
        if not employee.email or not employee.email.strip():
            return False, "Email is required"
        
        if '@' not in employee.email or '.' not in employee.email:
            return False, "Invalid email format"
        
        if not employee.position or not employee.position.strip():
            return False, "Position is required"
        
        if not employee.department or not employee.department.strip():
            return False, "Department is required"
        
        if employee.base_salary <= 0:
            return False, "Base salary must be greater than 0"
        
        return True, None


class PayrollValidator(Validator):
    """Validator for Payroll entities - Single Responsibility Principle"""
    
    def validate(self, payroll: Payroll) -> tuple[bool, Optional[str]]:
        """Validate payroll data"""
        if payroll.employee_id <= 0:
            return False, "Invalid employee ID"
        
        if payroll.basic_salary <= 0:
            return False, "Basic salary must be greater than 0"
        
        net_salary = payroll.calculate_net_salary()
        if net_salary <= 0:
            return False, "Calculated net salary must be greater than 0"
        
        return True, None


class AttendanceValidator(Validator):
    """Validator for Attendance entities - Single Responsibility Principle"""
    
    def validate(self, attendance: Attendance) -> tuple[bool, Optional[str]]:
        """Validate attendance data"""
        if attendance.employee_id <= 0:
            return False, "Invalid employee ID"
        
        if not attendance.status or attendance.status.strip() == "":
            return False, "Status is required"
        
        valid_statuses = ['Present', 'Late', 'Absent']
        if attendance.status not in valid_statuses:
            return False, f"Status must be one of: {', '.join(valid_statuses)}"
        
        if attendance.status == 'Present' and attendance.hours_worked <= 0:
            return False, "Hours worked must be greater than 0 for Present status"
        
        if attendance.hours_worked < 0:
            return False, "Hours worked cannot be negative"
        
        if attendance.hours_worked > 24:
            return False, "Hours worked cannot exceed 24"
        
        return True, None

