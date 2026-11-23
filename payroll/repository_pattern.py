"""
Repository Pattern Implementation
Separates data access logic from business logic (SOLID - Single Responsibility)
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from domain_models import Employee, Payroll, Attendance, IRepository
from database import Database


# Employee Repository
class EmployeeRepository(IRepository):
    """Repository for Employee data access - Single Responsibility Principle"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, employee: Employee) -> bool:
        """Save employee to database"""
        if employee.employee_id is None:
            # Insert new employee
            query = '''
                INSERT INTO Employees (first_name, last_name, email, position, 
                                     department, base_salary, hire_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            params = [
                employee.first_name, employee.last_name, employee.email,
                employee.position, employee.department, employee.base_salary,
                employee.hire_date
            ]
            return self.db.execute_query(query, params)
        else:
            # Update existing employee
            query = '''
                UPDATE Employees SET first_name=?, last_name=?, email=?, 
                position=?, department=?, base_salary=?, hire_date=?
                WHERE employee_id=?
            '''
            params = [
                employee.first_name, employee.last_name, employee.email,
                employee.position, employee.department, employee.base_salary,
                employee.hire_date, employee.employee_id
            ]
            return self.db.execute_query(query, params)
    
    def find_by_id(self, employee_id: int) -> Optional[Employee]:
        """Find employee by ID"""
        query = "SELECT employee_id, first_name, last_name, email, position, department, base_salary, hire_date FROM Employees WHERE employee_id = ?"
        result = self.db.fetch_all(query, [employee_id])
        if result:
            row = result[0]
            from domain_models import Employee
            from datetime import datetime
            hire_date = row[7] if isinstance(row[7], date) else datetime.strptime(str(row[7]), '%Y-%m-%d').date()
            return Employee(row[0], row[1], row[2], row[3], row[4], row[5], float(row[6]), hire_date)
        return None
    
    def find_all(self) -> List[Employee]:
        """Find all employees"""
        query = "SELECT employee_id, first_name, last_name, email, position, department, base_salary, hire_date FROM Employees ORDER BY first_name, last_name"
        results = self.db.fetch_all(query)
        employees = []
        from datetime import datetime
        for row in results:
            hire_date = row[7] if isinstance(row[7], date) else datetime.strptime(str(row[7]), '%Y-%m-%d').date()
            employees.append(Employee(row[0], row[1], row[2], row[3], row[4], row[5], float(row[6]), hire_date))
        return employees
    
    def find_by_department(self, department: str) -> List[Employee]:
        """Find employees by department"""
        query = "SELECT employee_id, first_name, last_name, email, position, department, base_salary, hire_date FROM Employees WHERE department = ? ORDER BY first_name, last_name"
        results = self.db.fetch_all(query, [department])
        employees = []
        from datetime import datetime
        for row in results:
            hire_date = row[7] if isinstance(row[7], date) else datetime.strptime(str(row[7]), '%Y-%m-%d').date()
            employees.append(Employee(row[0], row[1], row[2], row[3], row[4], row[5], float(row[6]), hire_date))
        return employees


# Payroll Repository
class PayrollRepository(IRepository):
    """Repository for Payroll data access - Single Responsibility Principle"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, payroll: Payroll) -> bool:
        """Save payroll to database"""
        if payroll.payroll_id is None:
            # Insert new payroll
            query = '''
                INSERT INTO Payroll (employee_id, pay_date, basic_salary,
                                   allowances, deductions, net_salary)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            params = [
                payroll.employee_id,
                payroll.pay_date,
                payroll.basic_salary,
                payroll.calculate_total_allowances(),
                payroll.calculate_total_deductions(),
                payroll.calculate_net_salary()
            ]
            return self.db.execute_query(query, params)
        else:
            # Update existing payroll
            query = '''
                UPDATE Payroll SET employee_id=?, pay_date=?, basic_salary=?,
                allowances=?, deductions=?, net_salary=?
                WHERE payroll_id=?
            '''
            params = [
                payroll.employee_id, payroll.pay_date, payroll.basic_salary,
                payroll.calculate_total_allowances(),
                payroll.calculate_total_deductions(),
                payroll.calculate_net_salary(),
                payroll.payroll_id
            ]
            return self.db.execute_query(query, params)
    
    def find_by_id(self, payroll_id: int) -> Optional[Payroll]:
        """Find payroll by ID"""
        query = "SELECT payroll_id, employee_id, pay_date, basic_salary, allowances, deductions, net_salary FROM Payroll WHERE payroll_id = ?"
        result = self.db.fetch_all(query, [payroll_id])
        if result:
            row = result[0]
            from datetime import datetime
            pay_date = row[2] if isinstance(row[2], date) else datetime.strptime(str(row[2]), '%Y-%m-%d').date()
            return Payroll(row[0], row[1], pay_date, float(row[3]), [], [])
        return None
    
    def find_all(self) -> List[Payroll]:
        """Find all payroll records"""
        query = "SELECT payroll_id, employee_id, pay_date, basic_salary, allowances, deductions, net_salary FROM Payroll ORDER BY pay_date DESC"
        results = self.db.fetch_all(query)
        payrolls = []
        from datetime import datetime
        for row in results:
            pay_date = row[2] if isinstance(row[2], date) else datetime.strptime(str(row[2]), '%Y-%m-%d').date()
            payrolls.append(Payroll(row[0], row[1], pay_date, float(row[3]), [], []))
        return payrolls
    
    def find_by_employee(self, employee_id: int) -> List[Payroll]:
        """Find payroll records by employee ID"""
        query = "SELECT payroll_id, employee_id, pay_date, basic_salary, allowances, deductions, net_salary FROM Payroll WHERE employee_id = ? ORDER BY pay_date DESC"
        results = self.db.fetch_all(query, [employee_id])
        payrolls = []
        from datetime import datetime
        for row in results:
            pay_date = row[2] if isinstance(row[2], date) else datetime.strptime(str(row[2]), '%Y-%m-%d').date()
            payrolls.append(Payroll(row[0], row[1], pay_date, float(row[3]), [], []))
        return payrolls


# Attendance Repository
class AttendanceRepository(IRepository):
    """Repository for Attendance data access - Single Responsibility Principle"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, attendance: Attendance) -> bool:
        """Save attendance to database"""
        if attendance.attendance_id is None:
            query = "INSERT INTO Attendance (employee_id, date, status, hours_worked) VALUES (?, ?, ?, ?)"
            params = [attendance.employee_id, attendance.date, attendance.status, attendance.hours_worked]
            return self.db.execute_query(query, params)
        else:
            query = "UPDATE Attendance SET employee_id=?, date=?, status=?, hours_worked=? WHERE attendance_id=?"
            params = [attendance.employee_id, attendance.date, attendance.status, attendance.hours_worked, attendance.attendance_id]
            return self.db.execute_query(query, params)
    
    def find_by_id(self, attendance_id: int) -> Optional[Attendance]:
        """Find attendance by ID"""
        query = "SELECT attendance_id, employee_id, date, status, hours_worked FROM Attendance WHERE attendance_id = ?"
        result = self.db.fetch_all(query, [attendance_id])
        if result:
            row = result[0]
            from datetime import datetime
            att_date = row[2] if isinstance(row[2], date) else datetime.strptime(str(row[2]), '%Y-%m-%d').date()
            return Attendance(row[0], row[1], att_date, row[3], float(row[4]))
        return None
    
    def find_all(self) -> List[Attendance]:
        """Find all attendance records"""
        query = "SELECT attendance_id, employee_id, date, status, hours_worked FROM Attendance ORDER BY date DESC"
        results = self.db.fetch_all(query)
        attendances = []
        from datetime import datetime
        for row in results:
            att_date = row[2] if isinstance(row[2], date) else datetime.strptime(str(row[2]), '%Y-%m-%d').date()
            attendances.append(Attendance(row[0], row[1], att_date, row[3], float(row[4])))
        return attendances
    
    def find_by_employee(self, employee_id: int) -> List[Attendance]:
        """Find attendance records by employee ID"""
        query = "SELECT attendance_id, employee_id, date, status, hours_worked FROM Attendance WHERE employee_id = ? ORDER BY date DESC"
        results = self.db.fetch_all(query, [employee_id])
        attendances = []
        from datetime import datetime
        for row in results:
            att_date = row[2] if isinstance(row[2], date) else datetime.strptime(str(row[2]), '%Y-%m-%d').date()
            attendances.append(Attendance(row[0], row[1], att_date, row[3], float(row[4])))
        return attendances

