CREATE DATABASE PayrollDB;
GO
USE PayrollDB;
GO

-- Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Employees table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY IDENTITY(1,1),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    position VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    base_salary DECIMAL(10,2) NOT NULL,
    hire_date DATE NOT NULL
);

-- Payroll table
CREATE TABLE Payroll (
    payroll_id INT PRIMARY KEY IDENTITY(1,1),
    employee_id INT FOREIGN KEY REFERENCES Employees(employee_id),
    pay_date DATE NOT NULL,
    basic_salary DECIMAL(10,2) NOT NULL,
    allowances DECIMAL(10,2) NOT NULL,
    deductions DECIMAL(10,2) NOT NULL,
    net_salary DECIMAL(10,2) NOT NULL
);

-- Attendance table
CREATE TABLE Attendance (
    attendance_id INT PRIMARY KEY IDENTITY(1,1),
    employee_id INT FOREIGN KEY REFERENCES Employees(employee_id),
    date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    hours_worked DECIMAL(5,2) NOT NULL
);

-- Insert default admin user
INSERT INTO Users (username, password, role)
VALUES ('admin', 'admin', 'admin');

-- Insert sample employees
INSERT INTO Employees (first_name, last_name, email, position, department, base_salary, hire_date)
VALUES 
('John', 'Doe', 'john.doe@company.com', 'Software Engineer', 'IT', 5000.00, '2023-01-01'),
('Jane', 'Smith', 'jane.smith@company.com', 'HR Manager', 'Human Resources', 6000.00, '2023-02-15'),
('Mike', 'Johnson', 'mike.johnson@company.com', 'Accountant', 'Finance', 5500.00, '2023-03-01');

-- Insert sample payroll records
INSERT INTO Payroll (employee_id, pay_date, basic_salary, allowances, deductions, net_salary)
VALUES 
(1, '2024-03-01', 5000.00, 500.00, 200.00, 5300.00),
(2, '2024-03-01', 6000.00, 600.00, 300.00, 6300.00),
(3, '2024-03-01', 5500.00, 550.00, 250.00, 5800.00);

-- Insert sample attendance records
INSERT INTO Attendance (employee_id, date, status, hours_worked)
VALUES 
(1, '2024-03-01', 'Present', 8.00),
(2, '2024-03-01', 'Present', 8.00),
(3, '2024-03-01', 'Present', 8.00);

-- Get all employees with their latest payroll
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.position,
    e.department,
    e.base_salary,
    p.pay_date,
    p.net_salary
FROM Employees e
LEFT JOIN Payroll p ON e.employee_id = p.employee_id
WHERE p.pay_date = (
    SELECT MAX(pay_date) 
    FROM Payroll 
    WHERE employee_id = e.employee_id
);

-- Get monthly payroll summary
SELECT 
    e.department,
    COUNT(DISTINCT p.employee_id) as employee_count,
    SUM(p.net_salary) as total_salary,
    AVG(p.net_salary) as average_salary
FROM Payroll p
JOIN Employees e ON p.employee_id = e.employee_id
WHERE p.pay_date >= DATEADD(MONTH, -1, GETDATE())
GROUP BY e.department;

-- Get employee attendance summary
SELECT 
    e.first_name,
    e.last_name,
    COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as days_present,
    COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) as days_absent,
    SUM(a.hours_worked) as total_hours
FROM Employees e
LEFT JOIN Attendance a ON e.employee_id = a.employee_id
WHERE a.date >= DATEADD(MONTH, -1, GETDATE())
GROUP BY e.employee_id, e.first_name, e.last_name;

-- Get employee salary history
SELECT 
    e.first_name,
    e.last_name,
    p.pay_date,
    p.basic_salary,
    p.allowances,
    p.deductions,
    p.net_salary
FROM Employees e
JOIN Payroll p ON e.employee_id = p.employee_id
ORDER BY p.pay_date DESC;

-- Search employees by name or department
SELECT *
FROM Employees
WHERE first_name LIKE '%John%'
   OR last_name LIKE '%Doe%'
   OR department LIKE '%IT%';

-- Get department-wise salary statistics
SELECT 
    department,
    COUNT(*) as employee_count,
    MIN(base_salary) as min_salary,
    MAX(base_salary) as max_salary,
    AVG(base_salary) as avg_salary
FROM Employees
GROUP BY department;












-- Create index for faster searches
CREATE INDEX idx_employee_name ON Employees(first_name, last_name);
CREATE INDEX idx_payroll_date ON Payroll(pay_date);
CREATE INDEX idx_attendance_date ON Attendance(date);

-- Update employee salary
UPDATE Employees
SET base_salary = 5500.00
WHERE employee_id = 1;

-- Delete old payroll records (older than 1 year)
DELETE FROM Payroll
WHERE pay_date < DATEADD(YEAR, -1, GETDATE());