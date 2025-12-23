from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF
from PyQt6.QtCore import Qt, QPointF, QRectF


class SidebarButton(QPushButton):
    def __init__(self, icon_type, tooltip, parent=None):
        super().__init__(parent=parent)
        self.icon_type = icon_type
        self.setToolTip(tooltip)
        self.setFixedSize(28, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # Hand cursor for better feel

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Draw Background based on state
        # We define colors manually here to ensure they match exact "Drawing" style
        # instead of relying purely on stylesheet for the complex interaction,
        # though we could mix both. Let's do manual for full control of the "fire" look.

        bg_color = QColor(0, 0, 0, 0)  # Transparent default
        icon_color = QColor("#cccccc")  # Default text gray

        if self.isDown():
            bg_color = QColor("#007acc")  # Primary Pressed
            icon_color = QColor("white")
        elif self.underMouse():
            bg_color = QColor("#2a2d2e")  # Surface Hover
            icon_color = QColor("#0098ff")  # Primary Hover

        # Draw rounded bg
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)  # 5px radius radius

        # 2. Draw Icon
        painter.setPen(
            QPen(
                icon_color,
                2,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        painter.setBrush(Qt.BrushStyle.NoBrush)

        rect = self.rect()
        center_x = rect.width() / 2
        center_y = rect.height() / 2

        if self.icon_type == "back":
            # Draw < (smaller)
            path = QPolygonF(
                [
                    QPointF(center_x + 2, center_y - 3),
                    QPointF(center_x - 2, center_y),
                    QPointF(center_x + 2, center_y + 3),
                ]
            )
            painter.drawPolyline(path)

        elif self.icon_type == "home":
            # Draw Circle (smaller)
            radius = 3
            painter.drawEllipse(QPointF(center_x, center_y), radius, radius)

        elif self.icon_type == "recent":
            # Draw Square (smaller)
            size = 6
            painter.drawRoundedRect(
                QRectF(center_x - size / 2, center_y - size / 2, size, size), 1, 1
            )

        elif self.icon_type == "vol_up":
            # Cone (smaller)
            painter.drawPolygon(
                QPolygonF(
                    [
                        QPointF(center_x - 3, center_y - 2),
                        QPointF(center_x - 5, center_y - 2),
                        QPointF(center_x - 5, center_y + 2),
                        QPointF(center_x - 3, center_y + 2),
                        QPointF(center_x - 1, center_y + 4),
                        QPointF(center_x - 1, center_y - 4),
                    ]
                )
            )
            # Plus (smaller)
            plus_x = center_x + 4
            painter.drawLine(
                int(plus_x), int(center_y - 2), int(plus_x), int(center_y + 2)
            )
            painter.drawLine(
                int(plus_x - 2), int(center_y), int(plus_x + 2), int(center_y)
            )

        elif self.icon_type == "vol_down":
            # Cone (smaller)
            painter.drawPolygon(
                QPolygonF(
                    [
                        QPointF(center_x - 3, center_y - 2),
                        QPointF(center_x - 5, center_y - 2),
                        QPointF(center_x - 5, center_y + 2),
                        QPointF(center_x - 3, center_y + 2),
                        QPointF(center_x - 1, center_y + 4),
                        QPointF(center_x - 1, center_y - 4),
                    ]
                )
            )
            # Minus (smaller)
            minus_x = center_x + 4
            painter.drawLine(
                int(minus_x - 2), int(center_y), int(minus_x + 2), int(center_y)
            )

        elif self.icon_type == "power":
            # Power symbol (smaller)
            radius = 4
            rect_f = QRectF(
                center_x - radius, center_y - radius, radius * 2, radius * 2
            )
            painter.drawArc(rect_f, 60 * 16, 300 * 16)
            painter.drawLine(
                QPointF(center_x, center_y - radius - 1), QPointF(center_x, center_y)
            )

        elif self.icon_type == "screenshot":
            # Camera Icon (smaller)
            cam_w, cam_h = 12, 9
            cam_rect = QRectF(
                center_x - cam_w / 2, center_y - cam_h / 2 + 1, cam_w, cam_h
            )
            painter.drawRoundedRect(cam_rect, 1, 1)
            # Lens
            painter.drawEllipse(QPointF(center_x, center_y + 1), 2.5, 2.5)
            # Top knob
            painter.drawRect(QRectF(center_x - 2.5, center_y - cam_h / 2 - 1, 5, 2))

        elif self.icon_type == "apk":
            # Install / APK Icon (smaller)
            # Box with arrow down
            # Bottom
            painter.drawLine(
                int(center_x - 4),
                int(center_y + 4),
                int(center_x + 4),
                int(center_y + 4),
            )
            # Sides
            painter.drawLine(
                int(center_x - 4),
                int(center_y + 4),
                int(center_x - 4),
                int(center_y + 1),
            )
            painter.drawLine(
                int(center_x + 4),
                int(center_y + 4),
                int(center_x + 4),
                int(center_y + 1),
            )

            # Arrow
            painter.drawLine(
                int(center_x), int(center_y - 3), int(center_x), int(center_y + 2)
            )
            # Arrow head
            painter.drawLine(
                int(center_x - 2), int(center_y), int(center_x), int(center_y + 2)
            )
            painter.drawLine(
                int(center_x + 2), int(center_y), int(center_x), int(center_y + 2)
            )

        painter.end()
