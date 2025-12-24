from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QGroupBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
)
from autoxium.ui.style import COLORS


class ProfilePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header
        title = QLabel("User Profile")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {COLORS["text"]};
        """)
        layout.addWidget(title)

        # Profile Info Group
        profile_group = QGroupBox("Profile Information")
        profile_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: 600;
                color: {COLORS["text"]};
                border: 2px solid {COLORS["border"]};
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)

        profile_layout = QFormLayout(profile_group)
        profile_layout.setSpacing(15)

        # User fields
        input_style = f"""
            QLineEdit {{
                background-color: {COLORS["background"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 5px;
                padding: 8px;
                color: {COLORS["text"]};
                font-size: 14px;
            }}
        """

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet(input_style)
        profile_layout.addRow("Username:", self.username_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        self.email_input.setStyleSheet(input_style)
        profile_layout.addRow("Email:", self.email_input)

        layout.addWidget(profile_group)

        # Save button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("💾 Save Profile")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["primary"]};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS["primary_hover"]};
            }}
        """)
        save_btn.clicked.connect(self.save_profile)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def save_profile(self):
        # TODO: Implement profile saving
        pass
