from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from autoxium.ui.style import theme_manager


class Sidebar(QWidget):
    page_changed = pyqtSignal(str)  # Emits page name when clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 10)
        layout.setSpacing(5)

        # Menu items
        self.buttons = {}
        self.active_button = None

        # Add menu buttons
        menu_items = [
            ("home", "🏠 Home"),
            ("logs", "📋 Logs"),
            ("settings", "⚙️ Settings"),
            ("profile", "👤 Profile"),
        ]

        for page_id, label in menu_items:
            btn = self._create_menu_button(label, page_id)
            layout.addWidget(btn)
            self.buttons[page_id] = btn

        layout.addStretch()

        # Connect to theme manager
        theme_manager.theme_changed.connect(self._on_theme_changed)

        # Set default active
        self.set_active_page("home")

        # Initial style application
        self.update_styles()

    def _on_theme_changed(self, _):
        """Handle theme change signal from theme manager"""
        self.update_styles()
    
    def update_styles(self):
        c = theme_manager.colors
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {c["surface"]};
                border-right: 1px solid {c["border"]};
            }}
        """)
        
        # Refresh current button states
        if self.active_button:
            self.set_active_page(self.active_button)

    def _create_menu_button(self, text, page_id):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # Style will be set by set_active_page called in init or update_styles
        btn.clicked.connect(lambda: self._on_button_clicked(page_id))
        return btn

    def _on_button_clicked(self, page_id):
        self.set_active_page(page_id)
        self.page_changed.emit(page_id)

    def set_active_page(self, page_id):
        # Reset all buttons
        for pid, btn in self.buttons.items():
            is_active = pid == page_id
            btn.setStyleSheet(self._get_button_style(is_active))

        self.active_button = page_id

    def _get_button_style(self, active):
        c = theme_manager.colors
        if active:
            return f"""
                QPushButton {{
                    background-color: {c["primary"]};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 15px;
                    text-align: left;
                    font-size: 14px;
                    font-weight: 600;
                }}
            """
        else:
            return f"""
                QPushButton {{
                    background-color: transparent;
                    color: {c["text"]};
                    border: none;
                    border-radius: 8px;
                    padding: 12px 15px;
                    text-align: left;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {c["surface_hover"]};
                }}
            """
