"""
Factory Pattern Implementation
Creates database connections, UI components, and domain objects
"""
from abc import ABC, abstractmethod
from database import Database
from domain_models import Employee, Payroll, Attendance, SalaryComponent
from datetime import date
from typing import Optional, Dict, Any, List


# Abstract Factory Interface
class IDatabaseFactory(ABC):
    """Abstract factory for database connections"""
    @abstractmethod
    def create_database(self) -> Database:
        pass


class DatabaseFactory(IDatabaseFactory):
    """Concrete factory for creating database connections"""
    _instance = None
    
    def __new__(cls):
        """Singleton pattern for factory"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def create_database(self) -> Database:
        """Factory method to create database connection"""
        db = Database()
        db.connect()
        return db


# Factory for creating domain objects
class DomainObjectFactory:
    """Factory for creating domain model objects"""
    
    @staticmethod
    def create_employee(employee_id: Optional[int], first_name: str, last_name: str,
                       email: str, position: str, department: str, base_salary: float,
                       hire_date: date) -> Employee:
        """Factory method to create Employee object"""
        return Employee(employee_id, first_name, last_name, email, position,
                       department, base_salary, hire_date)
    
    @staticmethod
    def create_employee_from_dict(data: Dict[str, Any]) -> Employee:
        """Factory method to create Employee from dictionary"""
        return Employee(
            employee_id=data.get('employee_id'),
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            position=data['position'],
            department=data['department'],
            base_salary=float(data['base_salary']),
            hire_date=data['hire_date'] if isinstance(data['hire_date'], date) 
                     else date.fromisoformat(str(data['hire_date']))
        )
    
    @staticmethod
    def create_payroll(payroll_id: Optional[int], employee_id: int, pay_date: date,
                      basic_salary: float, allowances: List[SalaryComponent] = None,
                      deductions: List[SalaryComponent] = None) -> Payroll:
        """Factory method to create Payroll object"""
        return Payroll(payroll_id, employee_id, pay_date, basic_salary,
                      allowances, deductions)
    
    @staticmethod
    def create_payroll_from_dict(data: Dict[str, Any]) -> Payroll:
        """Factory method to create Payroll from dictionary"""
        allowances = [SalaryComponent(**a) for a in data.get('allowances', [])]
        deductions = [SalaryComponent(**d) for d in data.get('deductions', [])]
        
        return Payroll(
            payroll_id=data.get('payroll_id'),
            employee_id=data['employee_id'],
            pay_date=data['pay_date'] if isinstance(data['pay_date'], date)
                     else date.fromisoformat(str(data['pay_date'])),
            basic_salary=float(data['basic_salary']),
            allowances=allowances,
            deductions=deductions
        )
    
    @staticmethod
    def create_attendance(attendance_id: Optional[int], employee_id: int, date: date,
                         status: str, hours_worked: float) -> Attendance:
        """Factory method to create Attendance object"""
        return Attendance(attendance_id, employee_id, date, status, hours_worked)
    
    @staticmethod
    def create_attendance_from_dict(data: Dict[str, Any]) -> Attendance:
        """Factory method to create Attendance from dictionary"""
        return Attendance(
            attendance_id=data.get('attendance_id'),
            employee_id=data['employee_id'],
            date=data['date'] if isinstance(data['date'], date)
                 else date.fromisoformat(str(data['date'])),
            status=data['status'],
            hours_worked=float(data['hours_worked'])
        )
    
    @staticmethod
    def create_salary_component(name: str, amount: float, is_percentage: bool = False,
                               base_amount: float = 0.0) -> SalaryComponent:
        """Factory method to create SalaryComponent"""
        return SalaryComponent(name, amount, is_percentage, base_amount)


# Factory for UI Components (can be extended)
class UIComponentFactory(ABC):
    """Abstract factory for UI components"""
    @abstractmethod
    def create_button(self, text: str):
        pass
    
    @abstractmethod
    def create_input(self, placeholder: str):
        pass


# Window Factory
class WindowFactory:
    """Factory for creating application windows"""
    
    @staticmethod
    def create_main_window(db: Database, current_user: str, styles_config: Dict):
        """Factory method to create main application window"""
        from app_window import MainAppWindow
        return MainAppWindow(db, current_user, 
                            styles_config['base_font_size'],
                            styles_config['base_padding'],
                            styles_config['base_radius'],
                            styles_config['base_height'])
    
    @staticmethod
    def create_admin_window(db: Database, current_user: str):
        """Factory method to create admin window"""
        from main import AdminMainWindow
        return AdminMainWindow(db, current_user)

