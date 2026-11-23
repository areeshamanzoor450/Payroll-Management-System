from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from database import Database # Assuming database connection is available
import csv # Import the csv module

class AdminReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("Admin Reports")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        placeholder_label = QLabel("Admin reporting features will be implemented here.\nExamples: User activity logs, system configuration reports, financial summaries.")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder_label)

        # Report Table
        self.report_table = QTableWidget()
        layout.addWidget(self.report_table)

        # Buttons
        button_layout = QHBoxLayout()

        self.generate_user_report_btn = QPushButton("Generate User Report")
        self.generate_user_report_btn.clicked.connect(self.generate_user_report)
        button_layout.addWidget(self.generate_user_report_btn)

        self.generate_employee_report_btn = QPushButton("Generate Employee Report")
        self.generate_employee_report_btn.clicked.connect(self.generate_employee_report)
        button_layout.addWidget(self.generate_employee_report_btn)

        self.generate_payroll_report_btn = QPushButton("Generate Payroll Summary Report")
        self.generate_payroll_report_btn.clicked.connect(self.generate_payroll_report)
        button_layout.addWidget(self.generate_payroll_report_btn)

        self.generate_attendance_report_btn = QPushButton("Generate Attendance Summary Report")
        self.generate_attendance_report_btn.clicked.connect(self.generate_attendance_report)
        button_layout.addWidget(self.generate_attendance_report_btn)

        # self.generate_leave_report_btn = QPushButton("Generate Leave Balance Report") # Commenting out as EmployeeLeave table not defined
        # self.generate_leave_report_btn.clicked.connect(self.generate_leave_report) # Commenting out
        # button_layout.addWidget(self.generate_leave_report_btn) # Commenting out

        self.generate_overtime_report_btn = QPushButton("Generate Overtime Summary Report")
        self.generate_overtime_report_btn.clicked.connect(self.generate_overtime_report)
        button_layout.addWidget(self.generate_overtime_report_btn)

        self.export_csv_btn = QPushButton("Export to CSV")
        self.export_csv_btn.clicked.connect(self.export_report_to_csv)
        button_layout.addWidget(self.export_csv_btn)

        layout.addLayout(button_layout)

        layout.addStretch()
        self.setLayout(layout)

    def generate_user_report(self):
        self.report_table.setRowCount(0) # Clear existing rows
        self.report_table.setColumnCount(2) # Columns for Username and Role
        self.report_table.setHorizontalHeaderLabels(["Username", "Role"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        query = "SELECT username, role FROM Users"
        users = self.db.fetch_all(query)

        for row_num, user in enumerate(users):
            self.report_table.insertRow(row_num)
            self.report_table.setItem(row_num, 0, QTableWidgetItem(user[0]))
            self.report_table.setItem(row_num, 1, QTableWidgetItem(user[1]))

    def generate_employee_report(self):
        self.report_table.setRowCount(0) # Clear existing rows
        # Assuming an Employees table with columns like employee_id, first_name, last_name, department, position, email
        self.report_table.setColumnCount(6) # Columns for Employee ID, First Name, Last Name, Department, Position, Email
        self.report_table.setHorizontalHeaderLabels(["Employee ID", "First Name", "Last Name", "Department", "Position", "Email"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Example query - adjust according to your actual Employees table schema
        query = "SELECT employee_id, first_name, last_name, department, position, email FROM Employees"
        employees = self.db.fetch_all(query)

        for row_num, employee in enumerate(employees):
            self.report_table.insertRow(row_num)
            self.report_table.setItem(row_num, 0, QTableWidgetItem(str(employee[0])))
            self.report_table.setItem(row_num, 1, QTableWidgetItem(employee[1]))
            self.report_table.setItem(row_num, 2, QTableWidgetItem(employee[2]))
            self.report_table.setItem(row_num, 3, QTableWidgetItem(employee[3]))
            self.report_table.setItem(row_num, 4, QTableWidgetItem(employee[4]))
            self.report_table.setItem(row_num, 5, QTableWidgetItem(employee[5]))

    def generate_payroll_report(self):
        self.report_table.setRowCount(0) # Clear existing rows
        # Assuming a Payroll table with columns employee_id, pay_date, basic_salary, allowances, deductions, net_salary
        # And an Employees table for employee first and last name
        self.report_table.setColumnCount(7) # Columns for Employee First Name, Last Name, Pay Date, Basic Salary, Allowances, Deductions, Net Salary
        self.report_table.setHorizontalHeaderLabels(["First Name", "Last Name", "Pay Date", "Basic Salary", "Allowances", "Deductions", "Net Salary"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Example query joining Employees and Payroll tables
        query = """
            SELECT E.first_name, E.last_name, P.pay_date, P.basic_salary, P.allowances, P.deductions, P.net_salary
            FROM Payroll P
            JOIN Employees E ON P.employee_id = E.employee_id
        """
        payroll_data = self.db.fetch_all(query)

        for row_num, data in enumerate(payroll_data):
            self.report_table.insertRow(row_num)
            self.report_table.setItem(row_num, 0, QTableWidgetItem(data[0]))
            self.report_table.setItem(row_num, 1, QTableWidgetItem(data[1]))
            self.report_table.setItem(row_num, 2, QTableWidgetItem(str(data[2])))
            self.report_table.setItem(row_num, 3, QTableWidgetItem(str(data[3])))
            self.report_table.setItem(row_num, 4, QTableWidgetItem(str(data[4])))
            self.report_table.setItem(row_num, 5, QTableWidgetItem(str(data[5])))
            self.report_table.setItem(row_num, 6, QTableWidgetItem(str(data[6])))

    def generate_attendance_report(self):
        self.report_table.setRowCount(0) # Clear existing rows
        # Assuming an Attendance table with columns employee_id, date, hours_worked, status
        # And an Employees table for employee first and last name
        self.report_table.setColumnCount(4) # Columns for Employee First Name, Last Name, Date, Hours Worked, Status
        self.report_table.setHorizontalHeaderLabels(["First Name", "Last Name", "Date", "Hours Worked", "Status"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Example query joining Employees and Attendance tables
        query = """
            SELECT E.first_name, E.last_name, A.date, A.hours_worked, A.status
            FROM Attendance A
            JOIN Employees E ON A.employee_id = E.employee_id
        """
        attendance_data = self.db.fetch_all(query)

        for row_num, data in enumerate(attendance_data):
            self.report_table.insertRow(row_num)
            self.report_table.setItem(row_num, 0, QTableWidgetItem(data[0]))
            self.report_table.setItem(row_num, 1, QTableWidgetItem(data[1]))
            self.report_table.setItem(row_num, 2, QTableWidgetItem(str(data[2])))
            self.report_table.setItem(row_num, 3, QTableWidgetItem(str(data[3])))
            self.report_table.setItem(row_num, 4, QTableWidgetItem(data[4]))

    # def generate_leave_report(self): # Commenting out as EmployeeLeave table not defined
    #     self.report_table.setRowCount(0) # Clear existing rows
    #     # Assuming an EmployeeLeave table with columns employee_id, leave_type, days_taken, year
    #     # And an Employees table for employee name
    #     self.report_table.setColumnCount(4) # Columns for Employee Name, Leave Type, Days Taken, Year
    #     self.report_table.setHorizontalHeaderLabels(["Employee Name", "Leave Type", "Days Taken", "Year"])
    #     self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    #     # Example query joining Employees and EmployeeLeave tables
    #     query = """
    #         SELECT E.name, EL.leave_type, EL.days_taken, EL.year
    #         FROM EmployeeLeave EL
    #         JOIN Employees E ON EL.employee_id = E.employee_id
    #     """\n    #     leave_data = self.db.fetch_all(query)

    #     for row_num, data in enumerate(leave_data):
    #         self.report_table.insertRow(row_num)
    #         self.report_table.setItem(row_num, 0, QTableWidgetItem(data[0]))
    #         self.report_table.setItem(row_num, 1, QTableWidgetItem(data[1]))
    #         self.report_table.setItem(row_num, 2, QTableWidgetItem(str(data[2])))
    #         self.report_table.setItem(row_num, 3, QTableWidgetItem(str(data[3]))) # Assuming year is stored as text or number

    def generate_overtime_report(self):
        self.report_table.setRowCount(0) # Clear existing rows
        # Assuming an Attendance table with columns employee_id, date, hours_worked, status
        # And an Employees table for employee first and last name
        # Note: Actual overtime calculation based on hours_worked and configured working hours
        # would be implemented here.
        self.report_table.setColumnCount(4) # Columns for Employee First Name, Last Name, Date, Hours Worked
        self.report_table.setHorizontalHeaderLabels(["First Name", "Last Name", "Date", "Hours Worked"])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Example query to get attendance data for potential overtime calculation
        query = """
            SELECT E.first_name, E.last_name, A.date, A.hours_worked
            FROM Attendance A
            JOIN Employees E ON A.employee_id = E.employee_id
            -- Add filtering by date range or employee here as needed
        """
        overtime_data = self.db.fetch_all(query)

        for row_num, data in enumerate(overtime_data):
            self.report_table.insertRow(row_num)
            self.report_table.setItem(row_num, 0, QTableWidgetItem(data[0]))
            self.report_table.setItem(row_num, 1, QTableWidgetItem(data[1]))
            self.report_table.setItem(row_num, 2, QTableWidgetItem(str(data[2])))
            self.report_table.setItem(row_num, 3, QTableWidgetItem(str(data[3])))
            # Overtime calculation logic would be applied here, and perhaps an additional column
            # for calculated overtime hours would be added.

    def export_report_to_csv(self):
        if self.report_table.rowCount() == 0:
            QMessageBox.warning(self, "Export Error", "No data to export.")
            return

        options = QFileDialog.Option.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write header row
                    header = [self.report_table.horizontalHeaderItem(i).text() for i in range(self.report_table.columnCount())]
                    writer.writerow(header)

                    # Write data rows
                    for row in range(self.report_table.rowCount()):
                        row_data = []
                        for column in range(self.report_table.columnCount()):
                            item = self.report_table.item(row, column)
                            if item is not None:
                                row_data.append(item.text())
                            else:
                                row_data.append("")
                        writer.writerow(row_data)

                QMessageBox.information(self, "Export Successful", f"Report successfully exported to {file_name}")

            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Error exporting report: {str(e)}") 