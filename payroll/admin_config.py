from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QComboBox, QCheckBox, QScrollArea, QFrame, QAbstractSpinBox, QDoubleSpinBox
from PyQt6.QtCore import Qt
from database import Database # Assuming database connection is available
from styles import get_button_style, get_input_style, get_table_style, get_form_frame_style, BASE_FONT_SIZE, BASE_PADDING, BASE_RADIUS, BASE_HEIGHT, BASE_MARGIN

class AddDeductionTypeDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add Deduction Type")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(get_form_frame_style(BASE_RADIUS, BASE_PADDING, BASE_MARGIN))
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Deduction Name")
        self.name_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.name_input)

        self.is_percentage_checkbox = QCheckBox("Is Percentage?")
        layout.addWidget(self.is_percentage_checkbox)

        self.default_value_input = QDoubleSpinBox()
        self.default_value_input.setRange(0.0, 999999.99)
        self.default_value_input.setPrefix("Default Value: ")
        self.default_value_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        layout.addWidget(self.default_value_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.save_button.clicked.connect(self.save_deduction_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_deduction_type(self):
        name = self.name_input.text().strip()
        is_percentage = self.is_percentage_checkbox.isChecked()
        default_value = self.default_value_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Deduction name cannot be empty.")
            return

        try:
            self.db.add_deduction_type(name, is_percentage, default_value)
            self.db.log_action(self.parent().current_user, f"Added deduction type: {name}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not add deduction type: {e}")

class EditDeductionTypeDialog(QDialog):
    def __init__(self, db: Database, deduction_type_data, parent=None):
        super().__init__(parent)
        self.db = db
        self.deduction_type_data = deduction_type_data
        self.setWindowTitle(f"Edit Deduction Type: {deduction_type_data['name']}")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(get_form_frame_style(BASE_RADIUS, BASE_PADDING, BASE_MARGIN))
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(deduction_type_data['name'])
        self.name_input.setPlaceholderText("Deduction Name")
        self.name_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.name_input)

        self.is_percentage_checkbox = QCheckBox("Is Percentage?")
        self.is_percentage_checkbox.setChecked(bool(deduction_type_data['is_percentage']))
        layout.addWidget(self.is_percentage_checkbox)

        self.default_value_input = QDoubleSpinBox()
        self.default_value_input.setRange(0.0, 999999.99)
        self.default_value_input.setPrefix("Default Value: ")
        self.default_value_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.default_value_input.setValue(deduction_type_data['default_value'])
        layout.addWidget(self.default_value_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.save_button.clicked.connect(self.save_deduction_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_deduction_type(self):
        name = self.name_input.text().strip()
        is_percentage = self.is_percentage_checkbox.isChecked()
        default_value = self.default_value_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Deduction name cannot be empty.")
            return

        try:
            self.db.update_deduction_type(self.deduction_type_data['deduction_type_id'], name, is_percentage, default_value)
            self.db.log_action(self.parent().current_user, f"Updated deduction type ID {self.deduction_type_data['deduction_type_id']}: {name}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not update deduction type: {e}")

class AddEarningTypeDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add Earning Type")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(get_form_frame_style(BASE_RADIUS, BASE_PADDING, BASE_MARGIN))
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Earning Name")
        self.name_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.name_input)

        self.is_percentage_checkbox = QCheckBox("Is Percentage?")
        layout.addWidget(self.is_percentage_checkbox)

        self.default_value_input = QDoubleSpinBox()
        self.default_value_input.setRange(0.0, 999999.99)
        self.default_value_input.setPrefix("Default Value: ")
        self.default_value_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        layout.addWidget(self.default_value_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.save_button.clicked.connect(self.save_earning_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_earning_type(self):
        name = self.name_input.text().strip()
        is_percentage = self.is_percentage_checkbox.isChecked()
        default_value = self.default_value_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Earning name cannot be empty.")
            return

        try:
            self.db.add_earning_type(name, is_percentage, default_value)
            self.db.log_action(self.parent().current_user, f"Added earning type: {name}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not add earning type: {e}")

class EditEarningTypeDialog(QDialog):
    def __init__(self, db: Database, earning_type_data, parent=None):
        super().__init__(parent)
        self.db = db
        self.earning_type_data = earning_type_data
        self.setWindowTitle(f"Edit Earning Type: {earning_type_data['name']}")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet(get_form_frame_style(BASE_RADIUS, BASE_PADDING, BASE_MARGIN))
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(earning_type_data['name'])
        self.name_input.setPlaceholderText("Earning Name")
        self.name_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.name_input)

        self.is_percentage_checkbox = QCheckBox("Is Percentage?")
        self.is_percentage_checkbox.setChecked(bool(earning_type_data['is_percentage']))
        layout.addWidget(self.is_percentage_checkbox)

        self.default_value_input = QDoubleSpinBox()
        self.default_value_input.setRange(0.0, 999999.99)
        self.default_value_input.setPrefix("Default Value: ")
        self.default_value_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.default_value_input.setValue(earning_type_data['default_value'])
        layout.addWidget(self.default_value_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.save_button.clicked.connect(self.save_earning_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_earning_type(self):
        name = self.name_input.text().strip()
        is_percentage = self.is_percentage_checkbox.isChecked()
        default_value = self.default_value_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Earning name cannot be empty.")
            return

        try:
            self.db.update_earning_type(self.earning_type_data['earning_type_id'], name, is_percentage, default_value)
            self.db.log_action(self.parent().current_user, f"Updated earning type ID {self.earning_type_data['earning_type_id']}: {name}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not update earning type: {e}")


class AddBenefitTypeDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Add Benefit Type")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet(get_form_frame_style(BASE_RADIUS, BASE_PADDING, BASE_MARGIN))
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Benefit Name")
        self.name_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.name_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.description_input)

        self.default_employer_contribution_input = QDoubleSpinBox()
        self.default_employer_contribution_input.setRange(0.0, 999999.99)
        self.default_employer_contribution_input.setPrefix("Default Employer Contribution: ")
        self.default_employer_contribution_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        layout.addWidget(self.default_employer_contribution_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.save_button.clicked.connect(self.save_benefit_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_benefit_type(self):
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()
        default_employer_contribution = self.default_employer_contribution_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Benefit name cannot be empty.")
            return

        try:
            self.db.add_benefit_type(name, description, default_employer_contribution)
            self.db.log_action(self.parent().current_user, f"Added benefit type: {name}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not add benefit type: {e}")


class EditBenefitTypeDialog(QDialog):
    def __init__(self, db: Database, benefit_type_data, parent=None):
        super().__init__(parent)
        self.db = db
        self.benefit_type_data = benefit_type_data
        self.setWindowTitle(f"Edit Benefit Type: {benefit_type_data['name']}")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet(get_form_frame_style(BASE_RADIUS, BASE_PADDING, BASE_MARGIN))
        self.setModal(True)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(benefit_type_data['name'])
        self.name_input.setPlaceholderText("Benefit Name")
        self.name_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.name_input)

        self.description_input = QLineEdit(benefit_type_data['description'])
        self.description_input.setPlaceholderText("Description")
        self.description_input.setStyleSheet(get_input_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        layout.addWidget(self.description_input)

        self.default_employer_contribution_input = QDoubleSpinBox()
        self.default_employer_contribution_input.setRange(0.0, 999999.99)
        self.default_employer_contribution_input.setPrefix("Default Employer Contribution: ")
        self.default_employer_contribution_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.default_employer_contribution_input.setValue(benefit_type_data['default_employer_contribution'])
        layout.addWidget(self.default_employer_contribution_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.save_button.clicked.connect(self.save_benefit_type)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_benefit_type(self):
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()
        default_employer_contribution = self.default_employer_contribution_input.value()

        if not name:
            QMessageBox.warning(self, "Input Error", "Benefit name cannot be empty.")
            return

        try:
            self.db.update_benefit_type(self.benefit_type_data['benefit_type_id'], name, description, default_employer_contribution)
            self.db.log_action(self.parent().current_user, f"Updated benefit type ID {self.benefit_type_data['benefit_type_id']}: {name}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not update benefit type: {e}")


class AdminConfigPage(QScrollArea):
    def __init__(self, db: Database, current_user: str, parent=None):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: #f0f0f0;")

        content_widget = QFrame()
        self.setWidget(content_widget)
        self.layout = QVBoxLayout(content_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setup_deduction_types_section()
        self.setup_earning_types_section()
        self.setup_benefit_types_section()


    def setup_deduction_types_section(self):
        deduction_label = QLabel("Deduction Types")
        deduction_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #333;")
        self.layout.addWidget(deduction_label)

        self.deduction_types_table = QTableWidget()
        self.deduction_types_table.setColumnCount(4)
        self.deduction_types_table.setHorizontalHeaderLabels(["ID", "Name", "Is Percentage", "Default Value"])
        self.deduction_types_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.deduction_types_table.setStyleSheet(get_table_style(BASE_RADIUS, BASE_PADDING, BASE_FONT_SIZE, BASE_HEIGHT))
        self.layout.addWidget(self.deduction_types_table)

        deduction_button_layout = QHBoxLayout()
        self.add_deduction_button = QPushButton("Add Deduction Type")
        self.add_deduction_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.add_deduction_button.clicked.connect(self.add_deduction_type)
        deduction_button_layout.addWidget(self.add_deduction_button)

        self.edit_deduction_button = QPushButton("Edit Deduction Type")
        self.edit_deduction_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.edit_deduction_button.clicked.connect(self.edit_deduction_type)
        deduction_button_layout.addWidget(self.edit_deduction_button)

        self.delete_deduction_button = QPushButton("Delete Deduction Type")
        self.delete_deduction_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.delete_deduction_button.clicked.connect(self.delete_deduction_type)
        deduction_button_layout.addWidget(self.delete_deduction_button)

        self.layout.addLayout(deduction_button_layout)
        self.load_deduction_types()

    def load_deduction_types(self):
        self.deduction_types_table.setRowCount(0)
        deduction_types = self.db.get_deduction_types()
        for row_num, deduction_type in enumerate(deduction_types):
            self.deduction_types_table.insertRow(row_num)
            self.deduction_types_table.setItem(row_num, 0, QTableWidgetItem(str(deduction_type['deduction_type_id'])))
            self.deduction_types_table.setItem(row_num, 1, QTableWidgetItem(deduction_type['name']))
            self.deduction_types_table.setItem(row_num, 2, QTableWidgetItem("Yes" if deduction_type['is_percentage'] else "No"))
            self.deduction_types_table.setItem(row_num, 3, QTableWidgetItem(str(deduction_type['default_value'])))

    def add_deduction_type(self):
        dialog = AddDeductionTypeDialog(self.db, self)
        if dialog.exec():
            self.load_deduction_types()

    def edit_deduction_type(self):
        selected_row = self.deduction_types_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a deduction type to edit.")
            return

        deduction_type_id = int(self.deduction_types_table.item(selected_row, 0).text())
        deduction_types = self.db.get_deduction_types()
        selected_deduction_type = next((dt for dt in deduction_types if dt['deduction_type_id'] == deduction_type_id), None)

        if selected_deduction_type:
            dialog = EditDeductionTypeDialog(self.db, selected_deduction_type, self)
            if dialog.exec():
                self.load_deduction_types()
        else:
             QMessageBox.critical(self, "Error", "Could not retrieve deduction type data.")


    def delete_deduction_type(self):
        selected_row = self.deduction_types_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a deduction type to delete.")
            return

        deduction_type_id = int(self.deduction_types_table.item(selected_row, 0).text())
        name = self.deduction_types_table.item(selected_row, 1).text()

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete deduction type: {name}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_deduction_type(deduction_type_id)
                self.db.log_action(self.current_user, f"Deleted deduction type ID {deduction_type_id}: {name}")
                self.load_deduction_types()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not delete deduction type: {e}")

    def setup_earning_types_section(self):
        earning_label = QLabel("Earning Types")
        earning_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #333;")
        self.layout.addWidget(earning_label)

        self.earning_types_table = QTableWidget()
        self.earning_types_table.setColumnCount(4)
        self.earning_types_table.setHorizontalHeaderLabels(["ID", "Name", "Is Percentage", "Default Value"])
        self.earning_types_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.earning_types_table.setStyleSheet(get_table_style(BASE_RADIUS, BASE_PADDING, BASE_FONT_SIZE, BASE_HEIGHT))
        self.layout.addWidget(self.earning_types_table)

        earning_button_layout = QHBoxLayout()
        self.add_earning_button = QPushButton("Add Earning Type")
        self.add_earning_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.add_earning_button.clicked.connect(self.add_earning_type)
        earning_button_layout.addWidget(self.add_earning_button)

        self.edit_earning_button = QPushButton("Edit Earning Type")
        self.edit_earning_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.edit_earning_button.clicked.connect(self.edit_earning_type)
        earning_button_layout.addWidget(self.edit_earning_button)

        self.delete_earning_button = QPushButton("Delete Earning Type")
        self.delete_earning_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.delete_earning_button.clicked.connect(self.delete_earning_type)
        earning_button_layout.addWidget(self.delete_earning_button)

        self.layout.addLayout(earning_button_layout)
        self.load_earning_types()

    def load_earning_types(self):
        self.earning_types_table.setRowCount(0)
        earning_types = self.db.get_earning_types()
        for row_num, earning_type in enumerate(earning_types):
            self.earning_types_table.insertRow(row_num)
            self.earning_types_table.setItem(row_num, 0, QTableWidgetItem(str(earning_type['earning_type_id'])))
            self.earning_types_table.setItem(row_num, 1, QTableWidgetItem(earning_type['name']))
            self.earning_types_table.setItem(row_num, 2, QTableWidgetItem("Yes" if earning_type['is_percentage'] else "No"))
            self.earning_types_table.setItem(row_num, 3, QTableWidgetItem(str(earning_type['default_value'])))

    def add_earning_type(self):
        dialog = AddEarningTypeDialog(self.db, self)
        if dialog.exec():
            self.load_earning_types()

    def edit_earning_type(self):
        selected_row = self.earning_types_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an earning type to edit.")
            return

        earning_type_id = int(self.earning_types_table.item(selected_row, 0).text())
        earning_types = self.db.get_earning_types()
        selected_earning_type = next((et for et in earning_types if et['earning_type_id'] == earning_type_id), None)

        if selected_earning_type:
            dialog = EditEarningTypeDialog(self.db, selected_earning_type, self)
            if dialog.exec():
                self.load_earning_types()
        else:
            QMessageBox.critical(self, "Error", "Could not retrieve earning type data.")


    def delete_earning_type(self):
        selected_row = self.earning_types_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an earning type to delete.")
            return

        earning_type_id = int(self.earning_types_table.item(selected_row, 0).text())
        name = self.earning_types_table.item(selected_row, 1).text()

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete earning type: {name}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_earning_type(earning_type_id)
                self.db.log_action(self.current_user, f"Deleted earning type ID {earning_type_id}: {name}")
                self.load_earning_types()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not delete earning type: {e}")


    # New section for Benefit Types
    def setup_benefit_types_section(self):
        benefit_label = QLabel("Benefit Types")
        benefit_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; color: #333;")
        self.layout.addWidget(benefit_label)

        self.benefit_types_table = QTableWidget()
        self.benefit_types_table.setColumnCount(4)
        self.benefit_types_table.setHorizontalHeaderLabels(["ID", "Name", "Description", "Default Employer Contribution"])
        self.benefit_types_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.benefit_types_table.setStyleSheet(get_table_style(BASE_RADIUS, BASE_PADDING, BASE_FONT_SIZE, BASE_HEIGHT))
        self.layout.addWidget(self.benefit_types_table)

        benefit_button_layout = QHBoxLayout()
        self.add_benefit_button = QPushButton("Add Benefit Type")
        self.add_benefit_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.add_benefit_button.clicked.connect(self.add_benefit_type)
        benefit_button_layout.addWidget(self.add_benefit_button)

        self.edit_benefit_button = QPushButton("Edit Benefit Type")
        self.edit_benefit_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.edit_benefit_button.clicked.connect(self.edit_benefit_type)
        benefit_button_layout.addWidget(self.edit_benefit_button)

        self.delete_benefit_button = QPushButton("Delete Benefit Type")
        self.delete_benefit_button.setStyleSheet(get_button_style(BASE_PADDING, BASE_RADIUS, BASE_FONT_SIZE, BASE_HEIGHT))
        self.delete_benefit_button.clicked.connect(self.delete_benefit_type)
        benefit_button_layout.addWidget(self.delete_benefit_button)

        self.layout.addLayout(benefit_button_layout)
        self.load_benefit_types()

    def load_benefit_types(self):
        self.benefit_types_table.setRowCount(0)
        benefit_types = self.db.get_benefit_types()
        for row_num, benefit_type in enumerate(benefit_types):
            self.benefit_types_table.insertRow(row_num)
            self.benefit_types_table.setItem(row_num, 0, QTableWidgetItem(str(benefit_type['benefit_type_id'])))
            self.benefit_types_table.setItem(row_num, 1, QTableWidgetItem(benefit_type['name']))
            self.benefit_types_table.setItem(row_num, 2, QTableWidgetItem(benefit_type['description']))
            self.benefit_types_table.setItem(row_num, 3, QTableWidgetItem(str(benefit_type['default_employer_contribution'])))

    def add_benefit_type(self):
        dialog = AddBenefitTypeDialog(self.db, self)
        if dialog.exec():
            self.load_benefit_types()

    def edit_benefit_type(self):
        selected_row = self.benefit_types_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a benefit type to edit.")
            return

        benefit_type_id = int(self.benefit_types_table.item(selected_row, 0).text())
        benefit_types = self.db.get_benefit_types()
        selected_benefit_type = next((bt for bt in benefit_types if bt['benefit_type_id'] == benefit_type_id), None)

        if selected_benefit_type:
            dialog = EditBenefitTypeDialog(self.db, selected_benefit_type, self)
            if dialog.exec():
                self.load_benefit_types()
        else:
            QMessageBox.critical(self, "Error", "Could not retrieve benefit type data.")

    def delete_benefit_type(self):
        selected_row = self.benefit_types_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a benefit type to delete.")
            return

        benefit_type_id = int(self.benefit_types_table.item(selected_row, 0).text())
        name = self.benefit_types_table.item(selected_row, 1).text()

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete benefit type: {name}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_benefit_type(benefit_type_id)
                self.db.log_action(self.current_user, f"Deleted benefit type ID {benefit_type_id}: {name}")
                self.load_benefit_types()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", f"Could not delete benefit type: {e}")