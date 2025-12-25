"""
UI Style module - Theme management and color palettes
"""

from autoxium.ui.style.theme_manager import theme_manager, ThemeManager
from autoxium.ui.style.colors import PALETTES

# Backwards compatibility
COLORS = theme_manager.colors

__all__ = ['theme_manager', 'ThemeManager', 'PALETTES', 'COLORS']
