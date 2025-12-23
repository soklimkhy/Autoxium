# Modern Dark Theme Palette
COLORS = {
    "background": "#1e1e1e",
    "surface": "#252526",
    "surface_hover": "#2a2d2e",
    "primary": "#007acc",
    "primary_hover": "#0098ff",
    "text": "#ffffff",
    "text_secondary": "#cccccc",
    "border": "#3e3e42",
    "success": "#4caf50",
    "error": "#f44336",
    "scrollbar": "#424242",
}

STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["background"]};
    color: {COLORS["text"]};
}}

QWidget {{
    background-color: {COLORS["background"]};
    color: {COLORS["text"]};
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}}

/* Header Label */
QLabel#Header {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS["text"]};
    padding: 10px 0;
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS["primary"]};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {COLORS["primary_hover"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["primary"]};
}}

QPushButton:disabled {{
    background-color: {COLORS["surface"]};
    color: {COLORS["text_secondary"]};
}}

/* Table Widget */
QTableWidget {{
    background-color: {COLORS["surface"]};
    border: 1px solid {COLORS["border"]};
    gridline-color: {COLORS["border"]};
    selection-background-color: {COLORS["primary"]};
    selection-color: white;
    border-radius: 4px;
}}

QTableWidget::item {{
    padding: 5px;
}}

QHeaderView::section {{
    background-color: {COLORS["surface_hover"]};
    padding: 6px;
    border: none;
    border-bottom: 2px solid {COLORS["border"]};
    font-weight: bold;
    color: {COLORS["text"]};
}}

QTableWidget QTableCornerButton::section {{
    background-color: {COLORS["surface_hover"]};
    border: none;
}}

/* Scrollbar */
QScrollBar:vertical {{
    border: none;
    background: {COLORS["background"]};
    width: 10px;
    margin: 0px 0px 0px 0px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS["scrollbar"]};
    min-height: 20px;
    border-radius: 5px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}
"""
