import pyodbc
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def connect(self):
        try:
            # First try to connect to master database
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=DESKTOP-H67KM9B\\SQLEXPRESS;'
                'DATABASE=master;'
                'Trusted_Connection=yes;'
                'Encrypt=no;'
            )
            self.cursor = self.conn.cursor()
            
            # Check if PayrollDB exists, if not create it
            self.cursor.execute("SELECT database_id FROM sys.databases WHERE Name = 'PayrollDB'")
            if not self.cursor.fetchone():
                self.cursor.execute("CREATE DATABASE PayrollDB")
                self.conn.commit()
            
            # Close connection to master
            self.cursor.close()
            self.conn.close()
            
            # Connect to PayrollDB
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 18 for SQL Server};'
                'SERVER=DESKTOP-H67KM9B\\SQLEXPRESS;'
                'DATABASE=PayrollDB;'
                'Trusted_Connection=yes;'
                'Encrypt=no;'
            )
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            self.create_tables()
            
            return True
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")
            return False
            
    def create_tables(self):
        try:
            # Users table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' and xtype='U')
                CREATE TABLE Users (
                    user_id INT PRIMARY KEY IDENTITY(1,1),
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    role VARCHAR(20) NOT NULL
                )
            ''')
            
            # Employees table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Employees' and xtype='U')
                CREATE TABLE Employees (
                    employee_id INT PRIMARY KEY IDENTITY(1,1),
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    position VARCHAR(50) NOT NULL,
                    department VARCHAR(50) NOT NULL,
                    base_salary DECIMAL(10,2) NOT NULL,
                    hire_date DATE NOT NULL
                )
            ''')
            
            # Payroll table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Payroll' and xtype='U')
                CREATE TABLE Payroll (
                    payroll_id INT PRIMARY KEY IDENTITY(1,1),
                    employee_id INT FOREIGN KEY REFERENCES Employees(employee_id),
                    pay_date DATE NOT NULL,
                    basic_salary DECIMAL(10,2) NOT NULL,
                    allowances DECIMAL(10,2) NOT NULL,
                    deductions DECIMAL(10,2) NOT NULL,
                    net_salary DECIMAL(10,2) NOT NULL
                )
            ''')
            
            # Attendance table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Attendance' and xtype='U')
                CREATE TABLE Attendance (
                    attendance_id INT PRIMARY KEY IDENTITY(1,1),
                    employee_id INT FOREIGN KEY REFERENCES Employees(employee_id),
                    date DATE NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    hours_worked DECIMAL(5,2) NOT NULL
                )
            ''')
            
            # AuditLogs table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AuditLogs' and xtype='U')
                CREATE TABLE AuditLogs (
                    log_id INT PRIMARY KEY IDENTITY(1,1),
                    timestamp DATETIME NOT NULL,
                    [user] VARCHAR(50) NOT NULL,
                    action VARCHAR(50) NOT NULL,
                    details VARCHAR(MAX)
                )
            ''')
            
            # Insert default admin user if not exists
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM Users WHERE username = 'admin')
                INSERT INTO Users (username, password, role)
                VALUES ('admin', 'admin', 'admin')
            ''')

            # Insert default hr user if not exists
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM Users WHERE username = 'hr')
                INSERT INTO Users (username, password, role)
                VALUES ('hr', 'hr', 'hr')
            ''')
            
            # DeductionTypes table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='DeductionTypes' and xtype='U')
                CREATE TABLE DeductionTypes (
                    deduction_type_id INT PRIMARY KEY IDENTITY(1,1),
                    name VARCHAR(50) UNIQUE NOT NULL,
                    is_percentage BIT NOT NULL,
                    default_value DECIMAL(10,2) NOT NULL
                )
            ''')
            
            # EarningTypes table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='EarningTypes' and xtype='U')
                CREATE TABLE EarningTypes (
                    earning_type_id INT PRIMARY KEY IDENTITY(1,1),
                    name VARCHAR(50) UNIQUE NOT NULL,
                    is_percentage BIT NOT NULL,
                    default_value DECIMAL(10,2) NOT NULL
                )
            ''')
            
            # BenefitTypes table
            self.cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BenefitTypes' and xtype='U')
                CREATE TABLE BenefitTypes (
                    benefit_type_id INT PRIMARY KEY IDENTITY(1,1),
                    name VARCHAR(50) UNIQUE NOT NULL,
                    description VARCHAR(255),
                    default_employer_contribution DECIMAL(10,2)
                )
            ''')
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            return False
            
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            
    def execute_query(self, query, params=None):
        try:
            if not self.conn or not self.cursor:
                if not self.connect():
                    return False

            if params is not None:
                # Ensure params is a list
                if not isinstance(params, (list, tuple)):
                    params = [params]
                elif isinstance(params, tuple):
                    params = list(params)
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            raise e
            
    def fetch_all(self, query, params=None):
        try:
            if not self.conn or not self.cursor:
                if not self.connect():
                    return []

            if params is not None:
                # Ensure params is a list
                if not isinstance(params, (list, tuple)):
                    params = [params]
                elif isinstance(params, tuple):
                    params = list(params)
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return []

    def log_action(self, user, action, details=None):
        """Logs an administrative action to the AuditLogs table."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO AuditLogs (timestamp, user, action, details) VALUES (?, ?, ?, ?)"
        params = [timestamp, user, action, details]
        self.execute_query(query, params)

    # New methods for DeductionTypes
    def get_deduction_types(self):
        query = "SELECT deduction_type_id, name, is_percentage, default_value FROM DeductionTypes"
        return self.fetch_all(query)

    def add_deduction_type(self, name, is_percentage, default_value):
        query = "INSERT INTO DeductionTypes (name, is_percentage, default_value) VALUES (?, ?, ?)"
        params = [name, is_percentage, default_value]
        self.execute_query(query, params)

    def update_deduction_type(self, deduction_type_id, name, is_percentage, default_value):
        query = "UPDATE DeductionTypes SET name = ?, is_percentage = ?, default_value = ? WHERE deduction_type_id = ?"
        params = [name, is_percentage, default_value, deduction_type_id]
        self.execute_query(query, params)

    def delete_deduction_type(self, deduction_type_id):
        query = "DELETE FROM DeductionTypes WHERE deduction_type_id = ?"
        params = [deduction_type_id]
        self.execute_query(query, params)

    # New methods for EarningTypes
    def get_earning_types(self):
        query = "SELECT earning_type_id, name, is_percentage, default_value FROM EarningTypes"
        return self.fetch_all(query)

    def add_earning_type(self, name, is_percentage, default_value):
        query = "INSERT INTO EarningTypes (name, is_percentage, default_value) VALUES (?, ?, ?)"
        params = [name, is_percentage, default_value]
        self.execute_query(query, params)

    def update_earning_type(self, earning_type_id, name, is_percentage, default_value):
        query = "UPDATE EarningTypes SET name = ?, is_percentage = ?, default_value = ? WHERE earning_type_id = ?"
        params = [name, is_percentage, default_value, earning_type_id]
        self.execute_query(query, params)

    def delete_earning_type(self, earning_type_id):
        query = "DELETE FROM EarningTypes WHERE earning_type_id = ?"
        params = [earning_type_id]
        self.execute_query(query, params)

    # New methods for BenefitTypes
    def get_benefit_types(self):
        query = "SELECT benefit_type_id, name, description, default_employer_contribution FROM BenefitTypes"
        return self.fetch_all(query)

    def add_benefit_type(self, name, description, default_employer_contribution):
        query = "INSERT INTO BenefitTypes (name, description, default_employer_contribution) VALUES (?, ?, ?)"
        params = [name, description, default_employer_contribution]
        self.execute_query(query, params)

    def update_benefit_type(self, benefit_type_id, name, description, default_employer_contribution):
        query = "UPDATE BenefitTypes SET name = ?, description = ?, default_employer_contribution = ? WHERE benefit_type_id = ?"
        params = [name, description, default_employer_contribution, benefit_type_id]
        self.execute_query(query, params)

    def delete_benefit_type(self, benefit_type_id):
        query = "DELETE FROM BenefitTypes WHERE benefit_type_id = ?"
        params = [benefit_type_id]
        self.execute_query(query, params) 