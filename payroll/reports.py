from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QDateEdit, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database import Database
import pandas as pd
from datetime import datetime, timedelta
import styles

class ModernComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.get_input_style(styles.BASE_PADDING, styles.BASE_RADIUS, styles.BASE_FONT_SIZE, styles.BASE_HEIGHT))
        self.setMinimumHeight(styles.BASE_HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class ModernTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.get_table_style(styles.BASE_RADIUS, styles.BASE_PADDING, styles.BASE_FONT_SIZE, styles.BASE_HEIGHT))
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class ReportsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet(styles.get_main_window_style(styles.BASE_FONT_SIZE))
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Report Type Selection
        report_frame = QFrame()
        report_frame.setStyleSheet(styles.get_form_frame_style(styles.BASE_RADIUS, styles.BASE_PADDING, styles.BASE_MARGIN))
        report_layout = QVBoxLayout()
        report_layout.setSpacing(16)
        
        # Report Type
        report_type_layout = QHBoxLayout()
        report_type_label = QLabel("Report Type:")
        report_type_label.setStyleSheet(styles.get_label_style(styles.BASE_FONT_SIZE, styles.BASE_PADDING))
        self.report_type = ModernComboBox()
        self.report_type.addItems([
            "Department Salary Summary",
            "Employee Attendance Report",
            "Payroll History",
            "Tax Deduction Summary"
        ])
        self.report_type.currentIndexChanged.connect(self.update_report)
        report_type_layout.addWidget(report_type_label)
        report_type_layout.addWidget(self.report_type)
        report_layout.addLayout(report_type_layout)
        
        # Date Range
        date_layout = QHBoxLayout()
        start_date_label = QLabel("Start Date:")
        start_date_label.setStyleSheet(styles.get_label_style(styles.BASE_FONT_SIZE, styles.BASE_PADDING))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setStyleSheet(styles.get_input_style(styles.BASE_PADDING, styles.BASE_RADIUS, styles.BASE_FONT_SIZE, styles.BASE_HEIGHT))
        self.start_date.dateChanged.connect(self.update_report)
        
        end_date_label = QLabel("End Date:")
        end_date_label.setStyleSheet(styles.get_label_style(styles.BASE_FONT_SIZE, styles.BASE_PADDING))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setStyleSheet(styles.get_input_style(styles.BASE_PADDING, styles.BASE_RADIUS, styles.BASE_FONT_SIZE, styles.BASE_HEIGHT))
        self.end_date.dateChanged.connect(self.update_report)
        
        date_layout.addWidget(start_date_label)
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(end_date_label)
        date_layout.addWidget(self.end_date)
        report_layout.addLayout(date_layout)
        
        report_frame.setLayout(report_layout)
        layout.addWidget(report_frame)
        
        # Results Table
        self.results_table = ModernTableWidget()
        layout.addWidget(self.results_table)
        
        self.setLayout(layout)
        self.update_report()
        
    def update_report(self):
        report_type = self.report_type.currentText()
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        
        if report_type == "Department Salary Summary":
            self.show_department_summary(start_date, end_date)
        elif report_type == "Employee Attendance Report":
            self.show_attendance_report(start_date, end_date)
        elif report_type == "Payroll History":
            self.show_payroll_history(start_date, end_date)
        elif report_type == "Tax Deduction Summary":
            self.show_tax_summary(start_date, end_date)
            
    def show_department_summary(self, start_date, end_date):
        query = """
            SELECT 
                e.department,
                COUNT(DISTINCT e.employee_id) as employee_count,
                SUM(p.net_salary) as total_salary,
                AVG(p.net_salary) as avg_salary,
                MIN(p.net_salary) as min_salary,
                MAX(p.net_salary) as max_salary
            FROM Employees e
            JOIN Payroll p ON e.employee_id = p.employee_id
            WHERE p.pay_date BETWEEN ? AND ?
            GROUP BY e.department
            ORDER BY total_salary DESC
        """
        results = self.db.fetch_all(query, [start_date, end_date])
        
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels([
            "Department", "Employee Count", "Total Salary",
            "Average Salary", "Minimum Salary", "Maximum Salary"
        ])
        
        self.results_table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                if col > 1:  # Format salary values
                    value = f"${value:,.2f}"
                self.results_table.setItem(row, col, QTableWidgetItem(str(value)))
                
    def show_attendance_report(self, start_date, end_date):
        query = """
            SELECT 
                e.first_name + ' ' + e.last_name as employee_name,
                e.department,
                COUNT(CASE WHEN a.status = 'Present' THEN 1 END) as days_present,
                COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) as days_absent,
                SUM(a.hours_worked) as total_hours
            FROM Employees e
            LEFT JOIN Attendance a ON e.employee_id = a.employee_id
            WHERE a.date BETWEEN ? AND ?
            GROUP BY e.employee_id, e.first_name, e.last_name, e.department
            ORDER BY e.department, employee_name
        """
        results = self.db.fetch_all(query, [start_date, end_date])
        
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "Employee Name", "Department", "Days Present",
            "Days Absent", "Total Hours"
        ])
        
        self.results_table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                self.results_table.setItem(row, col, QTableWidgetItem(str(value)))
                
    def show_payroll_history(self, start_date, end_date):
        query = """
            SELECT 
                e.first_name + ' ' + e.last_name as employee_name,
                e.department,
                p.pay_date,
                p.basic_salary,
                p.allowances,
                p.deductions,
                p.net_salary
            FROM Payroll p
            JOIN Employees e ON p.employee_id = e.employee_id
            WHERE p.pay_date BETWEEN ? AND ?
            ORDER BY p.pay_date DESC, e.department, employee_name
        """
        results = self.db.fetch_all(query, [start_date, end_date])
        
        self.results_table.setColumnCount(7)
        self.results_table.setHorizontalHeaderLabels([
            "Employee Name", "Department", "Pay Date",
            "Basic Salary", "Allowances", "Deductions", "Net Salary"
        ])
        
        self.results_table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                if col >= 3:  # Format salary values
                    value = f"${value:,.2f}"
                self.results_table.setItem(row, col, QTableWidgetItem(str(value)))
                
    def show_tax_summary(self, start_date, end_date):
        query = """
            SELECT 
                e.department,
                COUNT(DISTINCT e.employee_id) as employee_count,
                SUM(p.deductions) as total_deductions,
                AVG(p.deductions) as avg_deductions,
                SUM(p.net_salary) as total_net_salary
            FROM Employees e
            JOIN Payroll p ON e.employee_id = p.employee_id
            WHERE p.pay_date BETWEEN ? AND ?
            GROUP BY e.department
            ORDER BY total_deductions DESC
        """
        results = self.db.fetch_all(query, [start_date, end_date])
        
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            "Department", "Employee Count", "Total Deductions",
            "Average Deductions", "Total Net Salary"
        ])
        
        self.results_table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                if col >= 2:  # Format salary values
                    value = f"${value:,.2f}"
                self.results_table.setItem(row, col, QTableWidgetItem(str(value))) 