from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from database import Database # Assuming database connection is available

class AdminAuditLogPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
        self.load_audit_logs()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("Audit Log")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Audit Log Table
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(4) # Columns for Timestamp, User, Action, Details
        self.log_table.setHorizontalHeaderLabels(["Timestamp", "User", "Action", "Details"])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.log_table)

        layout.addStretch()
        self.setLayout(layout)

    def load_audit_logs(self):
        self.log_table.setRowCount(0) # Clear existing rows
        # Assumes an 'AuditLogs' table with columns timestamp, user, action, details
        query = "SELECT timestamp, user, action, details FROM AuditLogs ORDER BY timestamp DESC"
        logs = self.db.fetch_all(query)

        for row_num, log_entry in enumerate(logs):
            self.log_table.insertRow(row_num)
            self.log_table.setItem(row_num, 0, QTableWidgetItem(str(log_entry[0])))
            self.log_table.setItem(row_num, 1, QTableWidgetItem(str(log_entry[1])))
            self.log_table.setItem(row_num, 2, QTableWidgetItem(str(log_entry[2])))
            self.log_table.setItem(row_num, 3, QTableWidgetItem(str(log_entry[3]))) 