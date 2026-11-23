from PyQt6.QtWidgets import QWidget, QSizePolicy, QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

# Default sizes (will be updated when application starts)
BASE_FONT_SIZE = 14
BASE_PADDING = 10
BASE_MARGIN = 8
BASE_HEIGHT = 40
BASE_RADIUS = 4

def update_screen_sizes():
    """Update sizes based on screen dimensions"""
    global BASE_FONT_SIZE, BASE_PADDING, BASE_MARGIN, BASE_HEIGHT, BASE_RADIUS
    
    screen = QApplication.primaryScreen().size()
    SCREEN_WIDTH = screen.width()
    SCREEN_HEIGHT = screen.height()
    
    # Calculate responsive sizes while maintaining proportions
    BASE_FONT_SIZE = max(12, int(SCREEN_WIDTH * 0.008))  # Slightly smaller for better readability
    BASE_PADDING = max(8, int(SCREEN_WIDTH * 0.008))     # Reduced padding
    BASE_MARGIN = max(6, int(SCREEN_WIDTH * 0.006))      # Reduced margin
    BASE_HEIGHT = max(36, int(SCREEN_HEIGHT * 0.04))     # Slightly reduced height
    BASE_RADIUS = max(4, int(SCREEN_WIDTH * 0.003))      # Maintained border radius

# Common styles for the application
def get_main_window_style(base_font_size):
    return f"""
    QWidget {{
        font-family: 'Segoe UI', Arial;
        font-size: {base_font_size}px;
        background-color: #F5F5F5;
    }}
    QMainWindow {{
        background-color: #F5F5F5;
    }}
"""

def get_sidebar_style(base_height, base_font_size, base_padding):
    return f"""
    QFrame {{
        background-color: #1976D2;
        min-width: {base_height * 4}px;
        max-width: {base_height * 5}px;
    }}
    QLabel {{
        color: white;
        font-size: {int(base_font_size * 1.5)}px;
        padding: {base_padding}px;
    }}
    QPushButton {{
        background-color: transparent;
        color: white;
        border: none;
        padding: {base_padding}px;
        text-align: left;
        font-weight: normal;
        font-size: {base_font_size}px;
    }}
    QPushButton:hover {{
        background-color: #2196F3;
    }}
"""

def get_content_area_style(base_padding):
    return f"""
    QWidget {{
        background-color: #F5F5F5;
        padding: {base_padding}px;
    }}
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
"""

def get_form_frame_style(base_radius, base_padding, base_margin):
    return f"""
    QFrame {{
        background-color: white;
        border-radius: {base_radius * 2}px;
        padding: {base_padding * 2}px;
        margin: {base_margin}px;
        border: 1px solid #E0E0E0;
    }}
"""

def get_button_style(base_padding, base_radius, base_font_size, base_height):
    return f"""
    QPushButton {{
        background-color: #2196F3;
        color: white;
        border: none;
        padding: {base_padding}px {base_padding * 2}px;
        border-radius: {base_radius}px;
        font-weight: bold;
        font-size: {base_font_size}px;
        min-height: {base_height}px;
        min-width: {base_height * 2}px;
    }}
    QPushButton:hover {{
        background-color: #1976D2;
    }}
    QPushButton:pressed {{
        background-color: #0D47A1;
    }}
    QPushButton:disabled {{
        background-color: #BDBDBD;
    }}
"""

def get_input_style(base_padding, base_radius, base_font_size, base_height):
    return f"""
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {{
        padding: {base_padding}px;
        border: 1px solid #BDBDBD;
        border-radius: {base_radius}px;
        background-color: white;
        font-size: {base_font_size}px;
        min-height: {base_height}px;
        min-width: {base_height * 3}px;
    }}
    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid #2196F3;
    }}
    QComboBox::drop-down {{
        border: none;
        width: {base_height}px;
    }}
    QComboBox::down-arrow {{
        image: url(down_arrow.png);
        width: {base_font_size}px;
        height: {base_font_size}px;
    }}
    QSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
        width: {base_height}px;
    }}
"""

def get_table_style(base_radius, base_padding, base_font_size, base_height):
    return f"""
    QTableWidget {{
        border: 1px solid #BDBDBD;
        border-radius: {base_radius * 2}px;
        background-color: white;
        gridline-color: #E0E0E0;
        font-size: {base_font_size}px;
    }}
    QTableWidget::item {{
        padding: {base_padding}px;
        min-height: {base_height}px;
    }}
    QTableWidget::item:selected {{
        background-color: #E3F2FD;
        color: black;
    }}
    QHeaderView::section {{
        background-color: #F5F5F5;
        padding: {base_padding}px;
        border: none;
        border-bottom: 1px solid #BDBDBD;
        font-weight: bold;
        font-size: {base_font_size}px;
        min-height: {base_height}px;
    }}
"""

def get_label_style(base_font_size, base_padding):
    return f"""
    QLabel {{
        font-weight: bold;
        color: #424242;
        font-size: {base_font_size}px;
        padding: {base_padding/2}px;
    }}
"""

def apply_modern_style(widget: QWidget):
    """Apply modern style to a widget and its children"""
    widget.setStyleSheet(get_main_window_style(BASE_FONT_SIZE))
    
    # Set minimum sizes for better responsiveness
    if hasattr(widget, 'setMinimumHeight'):
        widget.setMinimumHeight(BASE_HEIGHT)
    
    # Set size policies for better responsiveness
    if hasattr(widget, 'setSizePolicy'):
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    
    # Set font size
    if hasattr(widget, 'setFont'):
        font = widget.font()
        font.setPointSize(BASE_FONT_SIZE)
        widget.setFont(font)
    
    # Apply to all child widgets recursively
    for child in widget.findChildren(QWidget):
        apply_modern_style(child)

# New styles for Login Window
def get_login_title_style(base_font_size):
    return f"""
    QLabel {{
        color: white;
        font-size: {int(base_font_size * 3)}px;
        font-weight: bold;
        letter-spacing: 2px;
    }}
"""

def get_login_subtitle_style(base_font_size):
    return f"""
    QLabel {{
        color: rgba(255, 255, 255, 0.9);
        font-size: {int(base_font_size * 1.2)}px;
        letter-spacing: 1px;
    }}
"""

def get_login_form_frame_style(base_radius, base_padding):
    return f"""
    QFrame {{
        background-color: white;
        border-radius: {int(base_radius * 2)}px;
        padding: {int(base_padding * 3)}px;
        border: 1px solid #E0E0E0;
    }}
"""

def get_login_footer_style(base_font_size):
    return f"""
    QLabel {{
        color: rgba(255, 255, 255, 0.7);
        font-size: {int(base_font_size * 0.9)}px;
        letter-spacing: 0.5px;
    }}
""" 