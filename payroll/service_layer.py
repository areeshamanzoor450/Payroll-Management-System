"""
Service Layer - Component Principle
Business logic services that coordinate between repositories and domain models
Each service is a component that can be reused independently
"""
from typing import List, Optional
from domain_models import Employee, Payroll, Attendance
from repository_pattern import EmployeeRepository, PayrollRepository, AttendanceRepository
from validators import EmployeeValidator, PayrollValidator, AttendanceValidator
from strategy_pattern import PayrollCalculator


class EmployeeService:
    """Service component for Employee operations - Component Principle"""
    
    def __init__(self, employee_repo: EmployeeRepository, validator: EmployeeValidator):
        self.employee_repo = employee_repo
        self.validator = validator
    
    def create_employee(self, first_name: str, last_name: str, email: str,
                       position: str, department: str, base_salary: float, hire_date) -> tuple[bool, Optional[str], Optional[Employee]]:
        """Create a new employee with validation"""
        from factory_pattern import DomainObjectFactory
        employee = DomainObjectFactory.create_employee(
            None, first_name, last_name, email, position, department, base_salary, hire_date
        )
        
        is_valid, error_message = self.validator.validate(employee)
        if not is_valid:
            return False, error_message, None
        
        if self.employee_repo.save(employee):
            return True, None, employee
        return False, "Failed to save employee", None
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return self.employee_repo.find_all()
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return self.employee_repo.find_by_id(employee_id)
    
    def get_employees_by_department(self, department: str) -> List[Employee]:
        """Get employees by department"""
        return self.employee_repo.find_by_department(department)


class PayrollService:
    """Service component for Payroll operations - Component Principle"""
    
    def __init__(self, payroll_repo: PayrollRepository, validator: PayrollValidator,
                 calculator: PayrollCalculator):
        self.payroll_repo = payroll_repo
        self.validator = validator
        self.calculator = calculator
    
    def process_payroll(self, employee_id: int, pay_date, basic_salary: float,
                        allowances: List, deductions: List) -> tuple[bool, Optional[str], Optional[Payroll]]:
        """Process payroll with validation and calculation"""
        from factory_pattern import DomainObjectFactory
        payroll = DomainObjectFactory.create_payroll(
            None, employee_id, pay_date, basic_salary, allowances, deductions
        )
        
        is_valid, error_message = self.validator.validate(payroll)
        if not is_valid:
            return False, error_message, None
        
        # Use calculator strategies if needed
        # For now, payroll calculates itself (Information Expert)
        
        if self.payroll_repo.save(payroll):
            return True, None, payroll
        return False, "Failed to process payroll", None
    
    def get_all_payrolls(self) -> List[Payroll]:
        """Get all payroll records"""
        return self.payroll_repo.find_all()
    
    def get_payroll_by_employee(self, employee_id: int) -> List[Payroll]:
        """Get payroll records for an employee"""
        return self.payroll_repo.find_by_employee(employee_id)


class AttendanceService:
    """Service component for Attendance operations - Component Principle"""
    
    def __init__(self, attendance_repo: AttendanceRepository, validator: AttendanceValidator):
        self.attendance_repo = attendance_repo
        self.validator = validator
    
    def record_attendance(self, employee_id: int, date, status: str,
                         hours_worked: float) -> tuple[bool, Optional[str], Optional[Attendance]]:
        """Record attendance with validation"""
        from factory_pattern import DomainObjectFactory
        attendance = DomainObjectFactory.create_attendance(
            None, employee_id, date, status, hours_worked
        )
        
        is_valid, error_message = self.validator.validate(attendance)
        if not is_valid:
            return False, error_message, None
        
        if self.attendance_repo.save(attendance):
            return True, None, attendance
        return False, "Failed to record attendance", None
    
    def get_all_attendances(self) -> List[Attendance]:
        """Get all attendance records"""
        return self.attendance_repo.find_all()
    
    def get_attendance_by_employee(self, employee_id: int) -> List[Attendance]:
        """Get attendance records for an employee"""
        return self.attendance_repo.find_by_employee(employee_id)
    
    def calculate_attendance_summary(self, employee_id: int, start_date, end_date) -> dict:
        """Calculate attendance summary for an employee - Information Expert"""
        attendances = self.attendance_repo.find_by_employee(employee_id)
        filtered = [a for a in attendances if start_date <= a.date <= end_date]
        
        present_count = sum(1 for a in filtered if a.is_present())
        absent_count = len(filtered) - present_count
        total_hours = sum(a.hours_worked for a in filtered)
        
        return {
            'total_days': len(filtered),
            'present_days': present_count,
            'absent_days': absent_count,
            'total_hours': total_hours
        }

