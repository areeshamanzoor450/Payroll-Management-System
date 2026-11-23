import hashlib # Import hashlib for password hashing
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QFormLayout, QMessageBox, QHeaderView
from PyQt6.QtCore import Qt
from database import Database # Assuming database connection is available

def hash_password(password):
    """Hashes a password using SHA-256."""
    # In a real application, use a stronger, salt-based hashing algorithm like bcrypt
    return hashlib.sha256(password.encode()).hexdigest()

class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New User")
        self.init_ui()
        self.db = Database()

    def init_ui(self):
        layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "hr"]) # Assuming roles are 'admin' and 'hr'

        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Role:", self.role_combo)

        button_box = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_box.addWidget(self.save_button)
        button_box.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_box)

        self.setLayout(main_layout)

    def get_user_data(self):
        return {
            "username": self.username_input.text(),
            "password": self.password_input.text(), # Remember to hash this in production!
            "role": self.role_combo.currentText()
        }

class EditUserDialog(QDialog):
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit User")
        self.user_data = user_data
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.username_label = QLabel(f"Username: {self.user_data['username']}")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter new password (leave blank to keep current)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["admin", "hr"])
        self.role_combo.setCurrentText(self.user_data['role'])

        layout.addRow(self.username_label)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Role:", self.role_combo)

        button_box = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_box.addWidget(self.save_button)
        button_box.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(button_box)

        self.setLayout(main_layout)

    def get_user_data(self):
        return {
            "username": self.user_data['username'], # Username cannot be changed
            "password": self.password_input.text(), # Remember to hash this!
            "role": self.role_combo.currentText()
        }


class UserManagementPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.db = Database()
        self.current_user = current_user # Store the current user's username
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("User Management")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # User Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(3) # Columns for Username, Role, and Actions
        self.user_table.setHorizontalHeaderLabels(["Username", "Role", "Actions"])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.user_table)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("Add User")
        self.edit_user_btn = QPushButton("Edit User")
        self.delete_user_btn = QPushButton("Delete User")

        self.add_user_btn.clicked.connect(self.add_user)
        self.edit_user_btn.clicked.connect(lambda: self.edit_user(self.user_table.currentRow()))
        self.delete_user_btn.clicked.connect(lambda: self.delete_user(self.user_table.currentRow()))

        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_users(self):
        self.user_table.setRowCount(0) # Clear existing rows
        query = "SELECT username, role FROM Users"
        users = self.db.fetch_all(query)

        for row_num, user in enumerate(users):
            self.user_table.insertRow(row_num)
            self.user_table.setItem(row_num, 0, QTableWidgetItem(user[0]))
            self.user_table.setItem(row_num, 1, QTableWidgetItem(user[1]))

            # Add action buttons (Edit/Delete)
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")

            # Connect buttons to methods with row number
            edit_button.clicked.connect(lambda _, r=row_num: self.edit_user(r))
            delete_button.clicked.connect(lambda _, r=row_num: self.delete_user(r))

            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)
            action_widget.setLayout(action_layout)
            self.user_table.setCellWidget(row_num, 2, action_widget)

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec() == QDialog.accepted:
            user_data = dialog.get_user_data()
            if user_data["username"] and user_data["password"]:
                # Check if username already exists
                existing_user = self.db.fetch_one("SELECT username FROM Users WHERE username = ?", [user_data["username"]])
                if existing_user:
                    QMessageBox.warning(self, "Input Error", "Username already exists.")
                else:
                    hashed_password = hash_password(user_data["password"])
                    self.save_new_user(user_data["username"], hashed_password, user_data["role"])
            else:
                QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")

    def save_new_user(self, username, hashed_password, role):
        query = "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)"
        params = [username, hashed_password, role]
        try:
            if self.db.execute_query(query, params):
                # Log the action
                self.db.log_action(self.current_user, "Added User", f"Username: {username}, Role: {role}")
                QMessageBox.information(self, "Success", "User added successfully.")
                self.load_users() # Refresh the table
            else:
                QMessageBox.critical(self, "Database Error", "Failed to add user to the database.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error adding user: {str(e)}")

    def edit_user(self, row_num=None):
        # Check if a row is selected (for main edit button)
        if row_num is None or row_num < 0:
             selected_row = self.user_table.currentRow()
             if selected_row < 0:
                  QMessageBox.warning(self, "Select User", "Please select a user to edit.")
                  return
             row_num = selected_row

        # Get user data from the selected row
        username = self.user_table.item(row_num, 0).text()
        role = self.user_table.item(row_num, 1).text()
        user_data = {"username": username, "role": role}

        dialog = EditUserDialog(user_data, self)
        if dialog.exec() == QDialog.accepted:
            updated_data = dialog.get_user_data()
            self.update_user(updated_data["username"], updated_data["password"], updated_data["role"])

    def update_user(self, username, new_password, new_role):
        # Only update password if a new one is provided
        if new_password:
             hashed_password = hash_password(new_password)
             query = "UPDATE Users SET password = ?, role = ? WHERE username = ?"
             params = [hashed_password, new_role, username]
             details = f"Updated user {username}. Changed password and role to {new_role}."
        else:
             query = "UPDATE Users SET role = ? WHERE username = ?"
             params = [new_role, username]
             details = f"Updated user {username}. Changed role to {new_role}."

        try:
            self.db.execute_query(query, params)
            # Log the action
            self.db.log_action(self.current_user, "Updated User", details)
            QMessageBox.information(self, "Success", "User updated successfully.")
            self.load_users() # Refresh the table
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error updating user: {str(e)}")

    def delete_user(self, row_num=None):
        # Check if a row is selected (for main delete button)
        if row_num is None or row_num < 0:
             selected_row = self.user_table.currentRow()
             if selected_row < 0:
                  QMessageBox.warning(self, "Select User", "Please select a user to delete.")
                  return
             row_num = selected_row

        # Get user data from the selected row
        username = self.user_table.item(row_num, 0).text()
        reply = QMessageBox.question(self, "Delete User", f"Are you sure you want to delete user {username}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.execute_delete_user(username)

    def execute_delete_user(self, username):
        query = "DELETE FROM Users WHERE username = ?"
        params = [username]
        try:
            # Prevent deleting the last admin user
            admin_count_query = "SELECT COUNT(*) FROM Users WHERE role = 'admin'"
            admin_count = self.db.fetch_one(admin_count_query)[0]

            user_role_query = "SELECT role FROM Users WHERE username = ?"
            user_role = self.db.fetch_one(user_role_query, [username])[0]

            if user_role == 'admin' and admin_count <= 1:
                 QMessageBox.warning(self, "Deletion Error", "Cannot delete the last admin user.")
                 return

            self.db.execute_query(query, params)
            # Log the action
            self.db.log_action(self.current_user, "Deleted User", f"Username: {username}")
            QMessageBox.information(self, "Success", "User deleted successfully.")
            self.load_users() # Refresh the table
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error deleting user: {str(e)}") 