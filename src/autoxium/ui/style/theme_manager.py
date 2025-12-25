"""
Theme Manager - Handles theme switching and stylesheet generation
"""

from PyQt6.QtCore import QObject, pyqtSignal
from autoxium.ui.style.colors import PALETTES


class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._current_theme = "dark"
        self._colors = PALETTES[self._current_theme]

    @property
    def theme(self):
        return self._current_theme

    @property
    def colors(self):
        return self._colors

    def set_theme(self, theme_name):
        if theme_name in PALETTES and theme_name != self._current_theme:
            self._current_theme = theme_name
            self._colors = PALETTES[theme_name]
            self.theme_changed.emit(theme_name)

    def get_stylesheet(self):
        c = self._colors
        return f"""
        QMainWindow {{
            background-color: {c["background"]};
            color: {c["text"]};
        }}

        QWidget {{
            background-color: {c["background"]};
            color: {c["text"]};
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }}

        /* Header Label */
        QLabel#Header {{
            font-size: 24px;
            font-weight: bold;
            color: {c["text"]};
            padding: 10px 0;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {c["primary"]};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}

        QPushButton:hover {{
            background-color: {c["primary_hover"]};
        }}

        QPushButton:pressed {{
            background-color: {c["primary"]};
        }}

        QPushButton:disabled {{
            background-color: {c["surface"]};
            color: {c["text_secondary"]};
        }}

        /* Table Widget */
        QTableWidget {{
            background-color: {c["surface"]};
            border: 1px solid {c["border"]};
            gridline-color: {c["border"]};
            selection-background-color: {c["primary"]};
            selection-color: white;
            border-radius: 4px;
        }}

        QTableWidget::item {{
            padding: 5px;
        }}

        QHeaderView::section {{
            background-color: {c["surface_hover"]};
            padding: 6px;
            border: none;
            border-bottom: 2px solid {c["border"]};
            font-weight: bold;
            color: {c["text"]};
        }}

        QTableWidget QTableCornerButton::section {{
            background-color: {c["surface_hover"]};
            border: none;
        }}

        /* Scrollbar */
        QScrollBar:vertical {{
            border: none;
            background: {c["background"]};
            width: 10px;
            margin: 0px 0px 0px 0px;
        }}

        QScrollBar::handle:vertical {{
            background: {c["scrollbar"]};
            min-height: 20px;
            border-radius: 5px;
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        """


# Singleton instance
theme_manager = ThemeManager()
