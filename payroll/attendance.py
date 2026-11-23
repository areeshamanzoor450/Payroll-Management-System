from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QComboBox, QDateEdit, QFrame, QMessageBox,
                            QSizePolicy, QFormLayout, QHeaderView, QDoubleSpinBox, QAbstractItemView)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QColor
from database import Database
from datetime import datetime, timedelta
import styles
# Import new patterns
from factory_pattern import DatabaseFactory, DomainObjectFactory
from repository_pattern import AttendanceRepository, EmployeeRepository
from validators import AttendanceValidator

class AttendanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Use Factory Pattern to create database connection
        db_factory = DatabaseFactory()
        self.db = db_factory.create_database()
        # Initialize repositories (Dependency Injection)
        self.attendance_repo = AttendanceRepository(self.db)
        self.employee_repo = EmployeeRepository(self.db)
        # Initialize validator
        self.attendance_validator = AttendanceValidator()
        self.current_attendance_id = None # To keep track of the selected record for update/delete
        self.init_ui()
        
    def init_ui(self):
        # Apply basic main window style (Attendance page)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial;
                background-color: #F5F5F5;
            }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Attendance Management")
        title.setStyleSheet("""
            QLabel {
                color: #1976D2;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Form Frame
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
        form_layout.setSpacing(15)
        
        # Employee Selection
        self.employee_combo = QComboBox() # Use standard QComboBox
        self.populate_employee_dropdown()
        # Basic input style for combo box
        self.employee_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        form_layout.addRow("Employee:", self.employee_combo)
        
        # Date Selection
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        # Basic input style for date edit
        self.date_edit.setStyleSheet("""
            QDateEdit {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        form_layout.addRow("Date:", self.date_edit)
        
        # Status
        self.status_combo = QComboBox() # Use standard QComboBox
        self.status_combo.addItems(["Present", "Late", "Absent"])
        # Basic input style for combo box
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        self.status_combo.currentIndexChanged.connect(self.update_hours_worked_field) # Connect signal
        form_layout.addRow("Status:", self.status_combo)
        
        # Hours Worked
        self.hours_worked_input = QDoubleSpinBox()
        self.hours_worked_input.setMaximum(24)
        self.hours_worked_input.setMinimum(0)
        # Basic input style for double spin box
        self.hours_worked_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 3px;
            }
        """)
        form_layout.addRow("Hours Worked:", self.hours_worked_input)
        
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_btn = QPushButton("Add Record") # Use standard QPushButton
        # Basic button style
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D5D5D5;
            }
        """)
        self.add_btn.clicked.connect(self.add_attendance)
        button_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("Update Record") # Use standard QPushButton
        # Basic button style
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D5D5D5;
            }
        """)
        self.update_btn.clicked.connect(self.update_attendance)
        self.update_btn.setEnabled(False) # Disable initially
        button_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("Delete Record") # Use standard QPushButton
        # Basic button style
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #D5D5D5;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_attendance)
        self.delete_btn.setEnabled(False) # Disable initially
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        # Attendance Table
        self.attendance_table = QTableWidget() # Use standard QTableWidget
        self.setup_attendance_table()
        self.attendance_table.cellClicked.connect(self.load_attendance_from_table) # Connect signal
        layout.addWidget(self.attendance_table, 1) # Add stretch to the attendance table
        
        self.setLayout(layout)
        
    def populate_employee_dropdown(self):
        try:
            # Use Repository Pattern to load employees
            employees_list = self.employee_repo.find_all()
            
            self.employee_combo.clear()
            # Add a default item
            self.employee_combo.addItem("Select Employee", None)
            for employee in employees_list:
                self.employee_combo.addItem(employee.get_full_name(), employee.employee_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load employees: {str(e)}")
            
    def setup_attendance_table(self):
        """Setup the attendance table with modern styling"""
        self.attendance_table.setColumnCount(5) # Adjusted column count
        self.attendance_table.setHorizontalHeaderLabels([
            "ID", "Employee", "Date", "Status", "Hours Worked" # Updated headers
        ])
        
        # Set modern table properties
        self.attendance_table.setStyleSheet(styles.get_table_style(styles.BASE_RADIUS, styles.BASE_PADDING, styles.BASE_FONT_SIZE, styles.BASE_HEIGHT))
        
        # Set column widths to be responsive
        header = self.attendance_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Employee
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Date
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Hours Worked
        
        # Set fixed width for ID column
        self.attendance_table.setColumnWidth(0, 60)
        
        # Enable sorting
        self.attendance_table.setSortingEnabled(True)
        
        # Set alternating row colors
        self.attendance_table.setAlternatingRowColors(True)
        
        # Set row height
        self.attendance_table.verticalHeader().setDefaultSectionSize(int(styles.BASE_HEIGHT * 1.2)) # Responsive row height
        
        # Hide vertical header
        self.attendance_table.verticalHeader().setVisible(False)
        
        # Set selection behavior
        self.attendance_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.attendance_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # Enable word wrap
        self.attendance_table.setWordWrap(True)
        
        # Set text alignment
        self.attendance_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Load initial data
        self.load_attendance_data()
        
    def load_attendance_data(self):
        """Load attendance data with modern styling"""
        try:
            # Use Repository Pattern to load attendance records
            attendance_list = self.attendance_repo.find_all()
            employees_dict = {emp.employee_id: emp for emp in self.employee_repo.find_all()}
            
            # Convert to list of tuples for table display
            records = []
            for attendance in attendance_list:
                employee = employees_dict.get(attendance.employee_id)
                employee_name = employee.get_full_name() if employee else f"Employee {attendance.employee_id}"
                records.append((
                    attendance.attendance_id, employee_name, attendance.date,
                    attendance.status, attendance.hours_worked
                ))
            
            self.attendance_table.setRowCount(len(records))
            
            for row, record in enumerate(records):
                # Create styled items
                for col, value in enumerate(record):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    
                    # Add custom styling for different columns
                    if col == 0:  # ID
                        item.setForeground(QColor("#1976D2"))
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                    elif col == 3:  # Status (adjusted index)
                        if value == "Present":
                            item.setForeground(QColor("#2E7D32"))
                        elif value == "Late":
                            item.setForeground(QColor("#F57F17"))
                        else:
                            item.setForeground(QColor("#C62828"))
                    elif col == 4: # Hours Worked (adjusted index)
                        item.setText(f"{value:.2f}") # Format as float
                    
                    self.attendance_table.setItem(row, col, item)
                
                # Set row height
                self.attendance_table.setRowHeight(row, int(styles.BASE_HEIGHT * 1.2)) # Responsive row height
            
            # Resize columns to content
            self.attendance_table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load attendance data: {str(e)}")
            
    def load_attendance_from_table(self, row, column):
        """Load data from selected table row into the form"""
        if row >= 0:
            self.current_attendance_id = int(self.attendance_table.item(row, 0).text())
            
            # Use Repository Pattern to fetch attendance record
            attendance = self.attendance_repo.find_by_id(self.current_attendance_id)
            
            if attendance:
                # Populate form fields
                # Find the index of the employee in the combo box by employee_id
                index = self.employee_combo.findData(attendance.employee_id)
                if index >= 0:
                    self.employee_combo.setCurrentIndex(index)
                    
                self.date_edit.setDate(QDate(attendance.date))
                
                # Find the index of the status in the combo box
                status_index = self.status_combo.findText(attendance.status)
                if status_index >= 0:
                    self.status_combo.setCurrentIndex(status_index)
                    
                self.hours_worked_input.setValue(float(attendance.hours_worked))
                
                # Enable update and delete buttons
                self.update_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
            else:
                self.clear_form()
                QMessageBox.warning(self, "Error", "Could not fetch attendance record details.")

    def add_attendance(self):
        try:
            employee_id = self.employee_combo.currentData()
            att_date = self.date_edit.date().toPyDate()
            status = self.status_combo.currentText()
            hours_worked = self.hours_worked_input.value()

            if employee_id is None:
                QMessageBox.warning(self, "Error", "Please select an employee.")
                return

            # Create Attendance object using Factory Pattern
            attendance = DomainObjectFactory.create_attendance(
                None, employee_id, att_date, status, hours_worked
            )
            
            # Validate using Validator (Single Responsibility Principle)
            is_valid, error_message = self.attendance_validator.validate(attendance)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_message)
                return

            # Save using Repository Pattern
            if self.attendance_repo.save(attendance):
                QMessageBox.information(self, "Success", "Attendance record added successfully!")
                self.load_attendance_data()
                self.clear_form()
            else:
                QMessageBox.warning(self, "Error", "Failed to add attendance record!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_attendance(self):
        if self.current_attendance_id is None:
            QMessageBox.warning(self, "Error", "Please select a record to update.")
            return

        try:
            employee_id = self.employee_combo.currentData()
            att_date = self.date_edit.date().toPyDate()
            status = self.status_combo.currentText()
            hours_worked = self.hours_worked_input.value()

            if employee_id is None:
                QMessageBox.warning(self, "Error", "Please select an employee.")
                return

            # Create Attendance object using Factory Pattern
            attendance = DomainObjectFactory.create_attendance(
                self.current_attendance_id, employee_id, att_date, status, hours_worked
            )
            
            # Validate using Validator (Single Responsibility Principle)
            is_valid, error_message = self.attendance_validator.validate(attendance)
            if not is_valid:
                QMessageBox.warning(self, "Validation Error", error_message)
                return

            # Save using Repository Pattern
            if self.attendance_repo.save(attendance):
                QMessageBox.information(self, "Success", "Attendance record updated successfully!")
                self.load_attendance_data()
                self.clear_form()
            else:
                QMessageBox.warning(self, "Error", "Failed to update attendance record!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def delete_attendance(self):
        if self.current_attendance_id is None:
            QMessageBox.warning(self, "Error", "Please select a record to delete.")
            return

        reply = QMessageBox.question(self, 'Confirm Delete', 
                                     "Are you sure you want to delete this record?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Fetch the attendance record first
                attendance = self.attendance_repo.find_by_id(self.current_attendance_id)
                if attendance:
                    # For deletion, we'll use direct database call since repository doesn't have delete method
                    # In a full implementation, we'd add delete method to repository
                    query = "DELETE FROM Attendance WHERE attendance_id = ?"
                    params = [self.current_attendance_id]

                    if self.db.execute_query(query, params):
                        QMessageBox.information(self, "Success", "Attendance record deleted successfully!")
                        self.load_attendance_data()
                        self.clear_form()
                    else:
                        QMessageBox.warning(self, "Error", "Failed to delete attendance record!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def clear_form(self):
        """Clears the form fields and resets state"""
        self.employee_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())
        self.status_combo.setCurrentIndex(0) # Assuming 'Present' is the first item
        self.hours_worked_input.setValue(0)
        self.current_attendance_id = None
        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        
    def update_hours_worked_field(self, index):
        status = self.status_combo.currentText()
        if status == "Absent":
            self.hours_worked_input.setValue(0) # Set hours to 0 for absent
            self.hours_worked_input.setEnabled(False)
        else:
            self.hours_worked_input.setEnabled(True)
            # Optionally clear or set a default for other statuses
            # self.hours_worked_input.setValue(8) # Example default for Present 