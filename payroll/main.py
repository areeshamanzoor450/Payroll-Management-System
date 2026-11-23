import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QFrame, QSizePolicy, QStackedWidget, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap
from app_window import MainAppWindow
from database import Database
import styles
from user_management import UserManagementPage # Import the user management page
from admin_reports import AdminReportsPage # Import the admin reports page
from admin_config import AdminConfigPage # Import the admin config page
from admin_audit_log import AdminAuditLogPage # Import the admin audit log page
# Import Factory Pattern
from factory_pattern import DatabaseFactory, WindowFactory

# New window to select user role
class RoleSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Select Role")
        self.setFixedSize(300, 200) # Fixed size for simplicity
        
        # Basic window style
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F8F8; /* Very light grey background */
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #E0E0E0; /* Light grey button */
                border: 1px solid #B0B0B0;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D5D5D5;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Select Your Role")
        # Basic title style
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 10px; /* Add some space below the title */
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.admin_btn = QPushButton("Admin Login")
        self.admin_btn.clicked.connect(self.open_admin_login)
        layout.addWidget(self.admin_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.hr_btn = QPushButton("HR Login")
        self.hr_btn.clicked.connect(self.open_hr_login)
        layout.addWidget(self.hr_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
    def open_admin_login(self):
        self.admin_login_window = AdminLoginWindow()
        self.admin_login_window.show()
        self.close()
        
    def open_hr_login(self):
        self.hr_login_window = LoginWindow()
        self.hr_login_window.show()
        self.close()

# Admin Login Window
class AdminLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Use Factory Pattern to create database connection
        db_factory = DatabaseFactory()
        self.db = db_factory.create_database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Payroll Management System - Admin Login")
        # Apply basic window style
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial;
                background-color: #F0F0F0;
            }
            QLabel {
                font-weight: bold;
                color: #333333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #5CB85C;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4CAE4C;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 60, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Admin Login")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Admin Username")
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Admin Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Sign In")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password!")
            return

        try:
            query = "SELECT role, username FROM Users WHERE username = ? AND password = ?"
            params = [username, password]
            result = self.db.fetch_all(query, params)

            if result:
                user_role = result[0][0]
                logged_in_username = result[0][1]
                print(f"Logged in as {logged_in_username} with role {user_role}") # Debug print
                if user_role == 'admin':
                    # Use Factory Pattern to create admin window
                    window_factory = WindowFactory()
                    self.admin_main_window = window_factory.create_admin_window(self.db, logged_in_username)
                    self.admin_main_window.show()
                    self.close()
                else:
                    QMessageBox.warning(self, "Error", "Invalid username or password for Admin!")
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

# Admin Main Window
class AdminMainWindow(QWidget):
    def __init__(self, db, current_user):
        super().__init__()
        self.setWindowTitle("Payroll Management System - Admin Dashboard")
        self.setMinimumSize(1000, 700) # Set a minimum size
        self.db = db
        self.current_user = current_user
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar for navigation
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #333333;") # Dark grey sidebar
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(10)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # Title/Logo (Optional Admin Title)
        admin_title = QLabel("Admin Panel")
        admin_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        admin_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(admin_title)

        # Navigation Buttons
        self.user_management_btn = QPushButton("User Management")
        self.user_management_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        self.user_management_btn.clicked.connect(self.show_user_management)
        sidebar_layout.addWidget(self.user_management_btn)

        self.reports_btn = QPushButton("Reports (Admin)")
        self.reports_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        self.reports_btn.clicked.connect(self.show_admin_reports)
        sidebar_layout.addWidget(self.reports_btn)

        # self.config_btn = QPushButton("System Configuration") # Commented out
        # self.config_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #555555;
        #         color: white;
        #         border: none;
        #         padding: 10px;
        #         text-align: left;
        #     }
        #     QPushButton:hover {
        #         background-color: #777777;
        #     }
        # """)
        # self.config_btn.clicked.connect(self.show_admin_config) # Commented out
        # sidebar_layout.addWidget(self.config_btn) # Commented out

        # self.audit_log_btn = QPushButton("Audit Log") # Commented out
        # self.audit_log_btn.setStyleSheet("""
        #     QPushButton {
        #         background-color: #555555;
        #         color: white;
        #         border: none;
        #         padding: 10px;
        #         text-align: left;
        #     }
        #     QPushButton:hover {
        #         background-color: #777777;
        #     }
        # """)
        # self.audit_log_btn.clicked.connect(self.show_audit_log) # Commented out
        # sidebar_layout.addWidget(self.audit_log_btn) # Commented out

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar)

        # Content Area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1) # Add stretch

        self.setLayout(main_layout)

        # Content pages
        self.user_management_page = UserManagementPage(self.current_user)
        self.content_stack.addWidget(self.user_management_page)

        self.admin_reports_page = AdminReportsPage()
        self.content_stack.addWidget(self.admin_reports_page)

        # Set initial page
        self.content_stack.setCurrentWidget(self.user_management_page)

    def init_user_management_page(self):
        # This method is no longer needed as UserManagementPage has its own init_ui
        pass

    def init_admin_reports_page(self):
        # This method is no longer needed as AdminReportsPage has its own init_ui
        pass

    def show_user_management(self):
        self.content_stack.setCurrentWidget(self.user_management_page)

    def show_admin_reports(self):
        self.content_stack.setCurrentWidget(self.admin_reports_page)

    def show_admin_config(self):
        # This method is no longer needed as AdminConfigPage is removed
        pass

    def show_audit_log(self):
        # This method is no longer needed as AdminAuditLogPage is removed
        pass

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Use Factory Pattern to create database connection
        db_factory = DatabaseFactory()
        self.db = db_factory.create_database()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Payroll Management System - Login")
        # Apply basic main window style
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial;
                background-color: #F0F0F0; /* Light grey background */
            }
        """)
        
        # Main layout with background color
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Background frame
        bg_frame = QFrame()
        # No specific background frame style for basic UI, rely on main window bgcolor
        bg_layout = QVBoxLayout()
        bg_layout.setContentsMargins(40, 60, 40, 40)
        bg_layout.setSpacing(30)
        
        # Logo/Title
        self.title = QLabel("PMS")
        # Basic title style
        self.title.setStyleSheet("""
            QLabel {
                color: #333333; /* Dark grey color */
                font-size: 30px;
                font-weight: bold;
            }
        """)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(self.title)
        
        self.subtitle = QLabel("Payroll Management System")
        # Basic subtitle style
        self.subtitle.setStyleSheet("""
            QLabel {
                color: #555555; /* Medium grey color */
                font-size: 14px;
            }
        """)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(self.subtitle)
        
        # Login Form
        self.form_frame = QFrame()
        # Basic form frame style
        self.form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(25)
        
        # Username
        self.username_label = QLabel("Username")
        # Basic label style
        self.username_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333333;
            }
        """)
        self.username_input = QLineEdit() # Use standard QLineEdit
        self.username_input.setPlaceholderText("Enter your username")
        # Basic input style
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
        """)
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        
        # Password
        self.password_label = QLabel("Password")
        # Basic label style
        self.password_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #333333;
            }
        """)
        self.password_input = QLineEdit() # Use standard QLineEdit
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        # Basic input style
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
        """)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        
        # Login Button
        self.login_btn = QPushButton("Sign In") # Use standard QPushButton
        self.login_btn.clicked.connect(self.login)
        # Basic button style
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #5CB85C; /* Green color */
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4CAE4C;
            }
        """)
        form_layout.addWidget(self.login_btn)
        
        self.form_frame.setLayout(form_layout)
        bg_layout.addWidget(self.form_frame)
        
        # Footer
        self.footer = QLabel("© 2024 Payroll Management System")
        # Basic footer style
        self.footer.setStyleSheet("""
            QLabel {
                color: #777777; /* Grey color */
                font-size: 10px;
            }
        """)
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(self.footer)
        
        bg_frame.setLayout(bg_layout)
        main_layout.addWidget(bg_frame)
        self.setLayout(main_layout)
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password!")
            return
            
        try:
            query = "SELECT role, username FROM Users WHERE username = ? AND password = ?"
            params = [username, password]
            result = self.db.fetch_all(query, params)
            
            if result:
                user_role = result[0][0]
                logged_in_username = result[0][1]
                print(f"Logged in as {logged_in_username} with role {user_role}") # Debug print
                if user_role == 'admin':
                    # Use Factory Pattern to create admin window
                    window_factory = WindowFactory()
                    self.admin_main_window = window_factory.create_admin_window(self.db, logged_in_username)
                    self.admin_main_window.show()
                    self.close()
                elif user_role == 'hr':
                     # Use Factory Pattern to create main window
                     window_factory = WindowFactory()
                     styles_config = {
                         'base_font_size': styles.BASE_FONT_SIZE,
                         'base_padding': styles.BASE_PADDING,
                         'base_radius': styles.BASE_RADIUS,
                         'base_height': styles.BASE_HEIGHT
                     }
                     self.main_window = window_factory.create_main_window(self.db, logged_in_username, styles_config)
                     self.main_window.show()
                     self.close()
                else:
                     QMessageBox.warning(self, "Error", "Unknown user role.")
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    styles.update_screen_sizes()  # Initialize screen sizes after QApplication is created
    window = RoleSelectionWindow() # Start with the role selection window
    window.show()
    sys.exit(app.exec()) 