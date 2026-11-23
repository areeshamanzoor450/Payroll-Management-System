from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem, 
                            QLineEdit, QComboBox, QDateEdit, QMessageBox,
                            QTabWidget, QFormLayout, QSpinBox, QDoubleSpinBox,
                            QFrame, QScrollArea, QSizePolicy, QStackedWidget,
                            QHeaderView)
from PyQt6.QtCore import Qt, QDate, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from database import Database
from attendance import AttendanceWindow
from reports import ReportsWindow
import styles
# Import new patterns
from factory_pattern import DatabaseFactory, DomainObjectFactory
from repository_pattern import EmployeeRepository, PayrollRepository
from validators import EmployeeValidator, PayrollValidator
from strategy_pattern import PayrollCalculator, FixedAllowanceStrategy, FixedDeductionStrategy
from domain_models import SalaryComponent

class ModernButton(QPushButton):
    def __init__(self, text, base_padding, base_radius, base_font_size, base_height, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(styles.get_button_style(base_padding, base_radius, base_font_size, base_height))
        self.setMinimumHeight(base_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class ModernLineEdit(QLineEdit):
    def __init__(self, base_padding, base_radius, base_font_size, base_height, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.get_input_style(base_padding, base_radius, base_font_size, base_height))
        self.setMinimumHeight(base_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class ModernComboBox(QComboBox):
    def __init__(self, base_padding, base_radius, base_font_size, base_height, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.get_input_style(base_padding, base_radius, base_font_size, base_height))
        self.setMinimumHeight(base_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

class ModernTableWidget(QTableWidget):
    def __init__(self, base_radius, base_padding, base_font_size, base_height, parent=None):
        super().__init__(parent)
        self.setStyleSheet(styles.get_table_style(base_radius, base_padding, base_font_size, base_height))
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class MainAppWindow(QWidget):
    def __init__(self, db, current_user, base_font_size, base_padding, base_radius, base_height):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.base_font_size = base_font_size
        self.base_padding = base_padding
        self.base_radius = base_radius
        self.base_height = base_height
        if not self.db.connect():
            QMessageBox.critical(self, "Database Error", 
                               "Failed to connect to database. Please check your SQL Server installation.")
            return
        # Initialize repositories (Dependency Injection)
        self.employee_repo = EmployeeRepository(self.db)
        self.payroll_repo = PayrollRepository(self.db)
        # Initialize validators
        self.employee_validator = EmployeeValidator()
        self.payroll_validator = PayrollValidator()
        # Initialize payroll calculator with strategies
        self.payroll_calculator = PayrollCalculator()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Payroll Management System")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(styles.get_main_window_style(self.base_font_size))
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet(styles.get_sidebar_style(self.base_height, self.base_font_size, self.base_padding))
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        
        # Logo/Title
        title = QLabel("PMS")
        title.setStyleSheet(styles.get_label_style(self.base_font_size, self.base_padding) + """
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)
        
        # Navigation buttons
        nav_buttons = [
            ("Employee Management", self.show_employee_management),
            ("Payroll", self.show_payroll),
            ("Attendance", self.show_attendance),
            ("Reports", self.show_reports)
        ]
        
        for text, callback in nav_buttons:
            btn = ModernButton(text, self.base_padding, self.base_radius, self.base_font_size, self.base_height)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 12px;
                    text-align: left;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background-color: #2196F3;
                }
            """)
            btn.clicked.connect(callback)
            sidebar_layout.addWidget(btn)
            
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)
        
        # Content area with scroll
        content_scroll = QScrollArea()
        content_scroll.setWidgetResizable(True)
        content_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F5F5F5;
            }
        """)
        
        # Content stack
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(styles.get_content_area_style(self.base_padding))
        
        # Employee Management Page
        self.employee_page = QWidget()
        self.init_employee_page()
        self.content_stack.addWidget(self.employee_page)
        
        # Payroll Page
        self.payroll_page = QWidget()
        self.init_payroll_page()
        self.content_stack.addWidget(self.payroll_page)
        
        # Attendance Page
        self.attendance_page = AttendanceWindow()
        self.content_stack.addWidget(self.attendance_page)
        
        # Reports Page
        self.reports_page = ReportsWindow()
        self.content_stack.addWidget(self.reports_page)
        
        content_scroll.setWidget(self.content_stack)
        main_layout.addWidget(content_scroll, 1)
        self.setLayout(main_layout)
        
    def init_employee_page(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Employee Form
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 15px;
            }
        """) # Basic styling for form frame
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.employee_first_name = QLineEdit() # Use standard QLineEdit
        self.employee_last_name = QLineEdit() # Use standard QLineEdit
        self.employee_email = QLineEdit() # Use standard QLineEdit
        self.employee_position = QComboBox() # Use standard QComboBox
        self.employee_department = QComboBox() # Use standard QComboBox
        self.employee_salary = QDoubleSpinBox()
        self.employee_salary.setMaximum(1000000)
        self.employee_salary.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """)
        self.employee_hire_date = QDateEdit()
        self.employee_hire_date.setDate(QDate.currentDate())
        self.employee_hire_date.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """)
        # Add basic styles for standard QLineEdit and QComboBox
        self.employee_first_name.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.employee_last_name.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.employee_email.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.employee_position.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.employee_department.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)

        
        form_layout.addRow("First Name:", self.employee_first_name)
        form_layout.addRow("Last Name:", self.employee_last_name)
        form_layout.addRow("Email:", self.employee_email)
        form_layout.addRow("Position:", self.employee_position)
        form_layout.addRow("Department:", self.employee_department)
        form_layout.addRow("Base Salary:", self.employee_salary)
        form_layout.addRow("Hire Date:", self.employee_hire_date)
        
        add_employee_btn = QPushButton("Add Employee") # Use standard QPushButton
        add_employee_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D5D5D5;
            }
        """) # Basic styling for button
        add_employee_btn.clicked.connect(self.add_employee)
        form_layout.addRow(add_employee_btn)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        
        # Employee Table
        self.employee_table = QTableWidget() # Use standard QTableWidget
        self.setup_employee_table()
        layout.addWidget(self.employee_table, 1) # Ensure stretch is still applied here
        
        self.employee_page.setLayout(layout)
        self.load_positions()
        self.load_departments()
        
    def init_payroll_page(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Payroll Form
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 15px;
            }
        """) # Basic styling for form frame
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        self.payroll_employee = QComboBox() # Use standard QComboBox
        self.payroll_date = QDateEdit()
        self.payroll_date.setDate(QDate.currentDate())
        self.payroll_date.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """)
        self.payroll_allowances = QDoubleSpinBox()
        self.payroll_allowances.setMaximum(1000000)
        self.payroll_allowances.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """)
        self.payroll_deductions = QDoubleSpinBox()
        self.payroll_deductions.setMaximum(1000000)
        self.payroll_deductions.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
            }
        """)
        # Basic Salary Display
        self.basic_salary_display = QLabel("0.00")
        # Basic label style
        self.basic_salary_display.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333333;
            }
        """)
        # Add basic styles for standard QComboBox and QDoubleSpinBox
        self.payroll_employee.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.payroll_allowances.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.payroll_deductions.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)

        
        form_layout.addRow("Employee:", self.payroll_employee)
        form_layout.addRow("Pay Date:", self.payroll_date)
        form_layout.addRow("Basic Salary:", self.basic_salary_display)
        form_layout.addRow("Allowances:", self.payroll_allowances)
        form_layout.addRow("Deductions:", self.payroll_deductions)
        
        process_payroll_btn = QPushButton("Process Payroll") # Use standard QPushButton
        process_payroll_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D5D5D5;
            }
        """) # Basic styling for button
        process_payroll_btn.clicked.connect(self.process_payroll)
        form_layout.addRow(process_payroll_btn)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        
        # Payroll Table
        self.payroll_table = QTableWidget() # Use standard QTableWidget
        self.payroll_table.setColumnCount(9)
        self.payroll_table.setHorizontalHeaderLabels([
            "ID", "Employee", "Pay Date", "Basic Salary",
            "Allowances", "Deductions", "Net Salary", "Remaining Pay", "Actions"
        ])
        layout.addWidget(self.payroll_table, 1) # Add stretch to the payroll table
        
        self.payroll_page.setLayout(layout)
        
    def show_employee_management(self):
        self.load_employee_data()
        self.content_stack.setCurrentWidget(self.employee_page)
        
    def show_payroll(self):
        self.load_payroll()
        self.populate_payroll_employees_dropdown()
        self.content_stack.setCurrentWidget(self.payroll_page)
        
    def show_attendance(self):
        self.content_stack.setCurrentWidget(self.attendance_page)
        
    def show_reports(self):
        self.content_stack.setCurrentWidget(self.reports_page)
        
    def add_employee(self):
        try:
            # Get input values
            first_name = self.employee_first_name.text().strip()
            last_name = self.employee_last_name.text().strip()
            email = self.employee_email.text().strip()
            position = self.employee_position.currentText().strip()
            department = self.employee_department.currentText().strip()
            base_salary = self.employee_salary.value()
            hire_date = self.employee_hire_date.date().toPyDate()

            # Create employee using Factory Pattern
            employee = DomainObjectFactory.create_employee(
                None, first_name, last_name, email, position, department, base_salary, hire_date
            )
            
            # Validate using Validator (Single Responsibility Principle)
            is_valid, error_message = self.employee_validator.validate(employee)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_message)
                return
            
            # Save using Repository Pattern
            if self.employee_repo.save(employee):
                QMessageBox.information(self, "Success", "Employee added successfully!")
                # Reload employee table and payroll dropdown
                self.load_employee_data()
                self.populate_payroll_employees_dropdown()
                self.load_positions()
                self.load_departments()
                self.clear_employee_form()
            else:
                QMessageBox.warning(self, "Error", "Failed to add employee!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            
    def process_payroll(self):
        try:
            employee_data = self.payroll_employee.currentData()
            if not employee_data:
                QMessageBox.warning(self, "Error", "Please select an employee!")
                return
                
            employee_id, basic_salary = employee_data # Unpack the employee ID and stored basic salary

            pay_date = self.payroll_date.date().toPyDate()
            if not pay_date:
                QMessageBox.warning(self, "Error", "Please select a pay date!")
                return

            allowances_amount = float(self.payroll_allowances.value())
            deductions_amount = float(self.payroll_deductions.value())
            
            # Create salary components using Factory Pattern
            allowances = []
            deductions = []
            if allowances_amount > 0:
                allowances.append(DomainObjectFactory.create_salary_component(
                    "Allowances", allowances_amount, False
                ))
            if deductions_amount > 0:
                deductions.append(DomainObjectFactory.create_salary_component(
                    "Deductions", deductions_amount, False
                ))
            
            # Create Payroll object using Factory Pattern
            payroll = DomainObjectFactory.create_payroll(
                None, employee_id, pay_date, basic_salary, allowances, deductions
            )
            
            # Validate using Validator (Single Responsibility Principle)
            is_valid, error_message = self.payroll_validator.validate(payroll)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_message)
                return
            
            # Save using Repository Pattern
            if self.payroll_repo.save(payroll):
                QMessageBox.information(self, "Success", "Payroll processed successfully!")
                self.load_payroll()
                self.clear_payroll_form()
            else:
                QMessageBox.warning(self, "Error", "Failed to process payroll!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            
    def update_payroll_record(self, payroll_id):
        # This method will be implemented to handle updating payroll records
        QMessageBox.information(self, "Update", f"Update button clicked for Payroll ID: {payroll_id}")

    def load_payroll(self):
        try:
            # Use Repository Pattern to load payroll records
            payroll_list = self.payroll_repo.find_all()
            employees_dict = {emp.employee_id: emp for emp in self.employee_repo.find_all()}
            
            # Convert to list of tuples for table display
            results = []
            for payroll in payroll_list:
                employee = employees_dict.get(payroll.employee_id)
                employee_name = employee.get_full_name() if employee else f"Employee {payroll.employee_id}"
                results.append((
                    payroll.payroll_id, employee_name, payroll.pay_date,
                    payroll.basic_salary, payroll.calculate_total_allowances(),
                    payroll.calculate_total_deductions(), payroll.calculate_net_salary()
                ))
            
            self.payroll_table.setRowCount(0) # Clear existing rows
            self.payroll_table.setRowCount(len(results))
            for row, data in enumerate(results):
                payroll_id, employee_name, pay_date, basic_salary, allowances, deductions, net_salary = data

                # Calculate Remaining Pay based on the formula
                remaining_pay = basic_salary + allowances - deductions

                # Populate table cells
                self.payroll_table.setItem(row, 0, QTableWidgetItem(str(payroll_id)))
                self.payroll_table.setItem(row, 1, QTableWidgetItem(str(employee_name)))
                self.payroll_table.setItem(row, 2, QTableWidgetItem(str(pay_date)))
                self.payroll_table.setItem(row, 3, QTableWidgetItem(f"{basic_salary:,.2f}"))
                self.payroll_table.setItem(row, 4, QTableWidgetItem(f"{allowances:,.2f}"))
                self.payroll_table.setItem(row, 5, QTableWidgetItem(f"{deductions:,.2f}"))
                self.payroll_table.setItem(row, 6, QTableWidgetItem(f"{net_salary:,.2f}"))
                self.payroll_table.setItem(row, 7, QTableWidgetItem(f"{remaining_pay:,.2f}"))

                # Add Update button
                update_btn = ModernButton("Update", self.base_padding, self.base_radius, self.base_font_size, self.base_height)
                # Connect the button to a method, passing the payroll_id
                update_btn.clicked.connect(lambda checked, id=payroll_id: self.update_payroll_record(id))
                self.payroll_table.setCellWidget(row, 8, update_btn)
                
                # Set row height
                self.payroll_table.setRowHeight(row, int(self.base_height * 1.2)) # Adjust row height based on base_height
        except Exception as e:
            print(f"Error loading payroll: {str(e)}") # Print error to console
            QMessageBox.critical(self, "Error", f"Failed to load payroll: {str(e)}\nPlease check the console for details.") # Show error in message box
            
    def clear_employee_form(self):
        self.employee_first_name.clear()
        self.employee_last_name.clear()
        self.employee_email.clear()
        self.employee_position.setCurrentText("")
        self.employee_position.setCurrentIndex(-1)
        self.employee_department.setCurrentText("")
        self.employee_department.setCurrentIndex(-1)
        self.employee_salary.setValue(0)
        self.employee_hire_date.setDate(QDate.currentDate())
        
    def clear_payroll_form(self):
        self.payroll_allowances.setValue(0)
        self.payroll_deductions.setValue(0)
        self.payroll_date.setDate(QDate.currentDate())
        
    def load_positions(self):
        try:
            query = "SELECT DISTINCT position FROM Employees WHERE position IS NOT NULL AND position <> '' ORDER BY position"
            results = self.db.fetch_all(query)
            self.employee_position.clear()
            positions = [result[0] for result in results]
            self.employee_position.addItems(positions)
            self.employee_position.setEditable(True) # Allow adding new positions
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load positions: {str(e)}")
            
    def load_departments(self):
        try:
            query = "SELECT DISTINCT department FROM Employees WHERE department IS NOT NULL AND department <> '' ORDER BY department"
            results = self.db.fetch_all(query)
            self.employee_department.clear()
            departments = [result[0] for result in results]
            self.employee_department.addItems(departments)
            self.employee_department.setEditable(True) # Allow adding new departments
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load departments: {str(e)}")
            
    def update_basic_salary_display(self):
        employee_data = self.payroll_employee.currentData()
        if employee_data:
            employee_id, basic_salary = employee_data
            self.basic_salary_display.setText(f"{basic_salary:,.2f}")
        else:
            self.basic_salary_display.setText("0.00")

    def populate_payroll_employees_dropdown(self):
        try:
            # Use Repository Pattern to load employees
            employees_list = self.employee_repo.find_all()

            self.payroll_employee.clear()
            # Add a default empty item
            self.payroll_employee.addItem("Select Employee", None)
            for employee in employees_list:
                # Store employee ID and basic salary as user data
                self.payroll_employee.addItem(
                    employee.get_full_name(), 
                    (employee.employee_id, float(employee.base_salary))
                )
        except Exception as e:
            print(f"Error populating payroll employees dropdown: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load employees for payroll: {str(e)}\nPlease check the console for details.") 

    def setup_employee_table(self):
        """Setup the employee table with modern styling"""
        self.employee_table.setColumnCount(7)
        self.employee_table.setHorizontalHeaderLabels([
            "ID", "First Name", "Last Name", "Email", "Position", "Department", "Base Salary"
        ])
        
        # Set modern table properties
        # Apply basic table styling
        self.employee_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: white;
                gridline-color: #E0E0E0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #C0D9F2;
                color: black;
            }
            QHeaderView::section {
                background-color: #EFEFEF;
                padding: 5px;
                border: 1px solid #CCCCCC;
                font-weight: bold;
            }
        """)
        
        # Set column widths to be responsive
        # Column indices based on the actual columns loaded in load_employee_data
        header = self.employee_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # First Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Last Name
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Email
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Position
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Department
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)  # Base Salary
        
        # Set fixed width for ID column
        self.employee_table.setColumnWidth(0, 60)
        
        # Enable sorting
        self.employee_table.setSortingEnabled(True)
        
        # Set alternating row colors
        self.employee_table.setAlternatingRowColors(True)
        
        # Set row height
        self.employee_table.verticalHeader().setDefaultSectionSize(30) # Set a fixed basic row height
        
        # Hide vertical header
        self.employee_table.verticalHeader().setVisible(False)
        
        # Set selection behavior
        self.employee_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.employee_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Enable word wrap
        self.employee_table.setWordWrap(True)
        
        # Set text alignment
        self.employee_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Load initial data
        self.load_employee_data()
        
    def load_employee_data(self):
        """Load employee data with modern styling"""
        try:
            # Use Repository Pattern to load employees
            employees_list = self.employee_repo.find_all()
            
            # Convert to list of tuples for table display
            employees = []
            for emp in employees_list:
                employees.append((
                    emp.employee_id, emp.first_name, emp.last_name, emp.email,
                    emp.position, emp.department, emp.base_salary
                ))
            
            self.employee_table.setRowCount(0) # Clear existing rows
            self.employee_table.setRowCount(len(employees))
            
            for row, emp in enumerate(employees):
                # Create styled items
                for col, value in enumerate(emp):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    
                    # Add custom styling for different columns
                    if col == 6:  # Base Salary
                        item.setText(f"${float(value):,.2f}")
                        item.setForeground(QColor("#2E7D32"))
                    # No specific styling for other columns in this view
                    if col == 0: # ID
                         item.setForeground(QColor("#1976D2"))
                         font = item.font()
                         font.setBold(True)
                         item.setFont(font)
                    # elif col == 6:  # Status (This column is not present in this query)
                    #     if value == "Active":
                    #         item.setForeground(QColor("#2E7D32"))
                    #     else:
                    #         item.setForeground(QColor("#C62828"))
                    
                    # Apply consistent styling to items based on base font size if needed
                    # Example (if you want to set font for all items using base_font_size):
                    # font = item.font()
                    # font.setPointSize(self.base_font_size)
                    # item.setFont(font)

                    self.employee_table.setItem(row, col, item)
                
                # Set row height
                self.employee_table.setRowHeight(row, int(self.base_height * 1.2))
            
            # Resize columns to content
            self.employee_table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load employee data: {str(e)}")