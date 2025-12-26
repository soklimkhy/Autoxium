# 🚀 Frameless Window Enhancements - Autoxium

## Overview
The `main_window.py` has been enhanced with **PyQt6-Frameless-Window** to provide a modern, premium user experience with custom window controls and visual effects.

---

## ✨ What's New

### 1. **Frameless Window Design**
- ✅ Removed default Windows title bar
- ✅ Custom title bar with app branding ("🚀 Autoxium")
- ✅ Modern, clean aesthetic that matches your app's design language

### 2. **Custom Window Controls**
The title bar now includes three custom buttons:

| Button | Symbol | Function | Styling |
|--------|--------|----------|---------|
| **Minimize** | `−` | Minimizes window | Gray with hover effect |
| **Maximize** | `□` / `❐` | Toggles maximize/restore | Gray with hover effect |
| **Close** | `✕` | Closes application | **Red hover** for emphasis |

### 3. **Windows 11 Mica Effect**
- 🎨 **Mica blur effect** for modern Windows 11 appearance
- 🌓 **Theme-aware**: Automatically switches between light/dark mode
- ✨ **Translucent background** with system accent colors

### 4. **Enhanced User Experience**
- **Draggable**: Click and drag anywhere on the title bar to move the window
- **Resizable**: Drag from window edges to resize (built-in to FramelessMainWindow)
- **Window shadow**: Native OS shadow for depth
- **Smooth animations**: Maximize/restore animations

---

## 🔧 Technical Implementation

### Dependencies Added
```toml
dependencies = [
    "PyQt6",
    "PyQt6-Frameless-Window",  # NEW: Modern frameless window support
    "psutil",
]
```

### Key Changes to `main_window.py`

#### 1. **Inheritance Change**
```python
# Before
class MainWindow(QMainWindow):

# After
class MainWindow(FramelessMainWindow):
```

#### 2. **Custom Title Bar Setup**
```python
def _setup_title_bar(self):
    """Setup custom title bar with window controls"""
    # Creates a 40px height title bar with:
    # - App icon and title (left)
    # - Window controls: minimize, maximize, close (right)
```

#### 3. **Mica Effect Integration**
```python
# Enable Windows 11 Mica effect
self.windowEffect.setMicaEffect(
    self.winId(), 
    isDarkMode=theme_manager.theme == "dark"
)
```

#### 4. **Window Control Methods**
```python
def toggle_maximize(self):
    """Toggle between maximized and normal window state"""
    # Updates button icon based on state
```

---

## 🎨 Visual Enhancements

### Title Bar Styling
- **Height**: 40px (compact and modern)
- **Background**: Transparent with theme colors
- **Title**: Bold, indigo color (`#6366f1`)
- **Buttons**: 
  - Transparent background
  - Gray text (`#9ca3af`)
  - Hover: Semi-transparent white overlay
  - Close button: **Red hover** (`#ef4444`)

### Window Effects
- **Shadow**: Native OS shadow (automatically handled)
- **Blur**: Mica effect on Windows 11
- **Border**: Frameless design with smooth edges

---

## 📋 Features Comparison

| Feature | Before | After |
|---------|--------|-------|
| **Title Bar** | Default Windows | Custom branded |
| **Window Controls** | Standard | Styled buttons |
| **Dragging** | Title bar only | Custom title bar |
| **Resizing** | Standard | Enhanced with shadow |
| **Visual Effects** | None | Mica blur (Win11) |
| **Theme Support** | Yes | Yes + Mica updates |
| **Maximize Animation** | Standard | Smooth transition |

---

## 🚀 Usage

### Running the Enhanced Application
```bash
# Install dependencies (if not already installed)
pip install PyQt6-Frameless-Window

# Run the application
python -m autoxium
```

### Window Controls
- **Move**: Click and drag the title bar
- **Resize**: Drag from any window edge
- **Minimize**: Click the `−` button
- **Maximize/Restore**: Click the `□` / `❐` button
- **Close**: Click the `✕` button

### Theme Switching
- The Mica effect automatically updates when you switch themes
- Use the theme toggle button (☀️/🌙) in the TopBar

---

## 🔍 Code Structure

### New Methods in `MainWindow`

```python
class MainWindow(FramelessMainWindow):
    def __init__(self):
        # ... initialization
        self._setup_title_bar()  # NEW
    
    def _setup_title_bar(self):  # NEW
        """Creates custom title bar with window controls"""
    
    def _create_title_bar_button(self, text, callback):  # NEW
        """Factory method for title bar buttons"""
    
    def toggle_maximize(self):  # NEW
        """Handles maximize/restore toggle"""
    
    def update_theme(self, theme_name=None):  # ENHANCED
        # Now includes Mica effect updates
```

---

## 🎯 Benefits

### For Users
1. **Modern Appearance**: Matches Windows 11 design language
2. **Consistent Branding**: Custom title bar with app identity
3. **Better UX**: Smooth animations and visual feedback
4. **Premium Feel**: Mica blur and shadow effects

### For Developers
1. **Maintainable**: Library handles complex window management
2. **Cross-platform**: Works on Windows, Linux, macOS
3. **Extensible**: Easy to add more title bar widgets
4. **Theme-aware**: Automatically adapts to theme changes

---

## ⚠️ Important Notes

### Windows Version Support
- **Windows 11**: Full Mica effect support
- **Windows 10**: Acrylic blur fallback
- **Windows 7**: Aero blur fallback
- **Linux/macOS**: Basic frameless window (no blur)

### Known Limitations
1. **Mica effect**: Only on Windows 11
2. **Screen capture**: Can be disabled via library settings
3. **Win11 snap layout**: Not enabled by default (can be enabled)

### Future Enhancements
- [ ] Add snap layout support for Windows 11
- [ ] Add custom icon to title bar
- [ ] Add breadcrumb navigation to title bar
- [ ] Add quick action buttons to title bar

---

## 🐛 Troubleshooting

### Issue: Window won't drag
**Solution**: Make sure you're clicking on the title bar area (top 40px)

### Issue: Mica effect not showing
**Solution**: 
- Verify you're on Windows 11
- Check if transparency is enabled in Windows settings
- Ensure theme is set correctly

### Issue: Close button not red on hover
**Solution**: Check if custom stylesheet is being overridden by theme

---

## 📚 References

- [PyQt6-Frameless-Window GitHub](https://github.com/zhiyiYo/PyQt-Frameless-Window)
- [PyQt6-Frameless-Window Documentation](https://pyqt-frameless-window.readthedocs.io/)
- [Windows 11 Mica Material](https://learn.microsoft.com/en-us/windows/apps/design/style/mica)

---

## 📝 Changelog

### Version 0.2.0 (2025-12-26)
- ✅ Added PyQt6-Frameless-Window dependency
- ✅ Implemented custom title bar with window controls
- ✅ Added Windows 11 Mica effect support
- ✅ Enhanced theme switching with Mica updates
- ✅ Improved window dragging and resizing
- ✅ Added custom styling for window control buttons

---

**Note**: This enhancement only affects `main_window.py`. The `MirrorWindow` remains unchanged to avoid conflicts with scrcpy embedding.
