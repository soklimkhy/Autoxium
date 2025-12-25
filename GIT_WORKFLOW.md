# Git Workflow Guide - Managing Your Autoxium Changes

## Current Situation
You cloned the Autoxium repository and made significant improvements:
- ✅ Added theme support (Light/Dark mode)
- ✅ Fixed device name detection (Product Name & Model Name)
- ✅ Reorganized UI folder structure
- ✅ Added device name mapping database
- ✅ Improved table styling

## Option 1: Commit to Your Own Fork (Recommended)

### Step 1: Create Your Own Fork on GitHub
1. Go to the original repository on GitHub
2. Click "Fork" button (top right)
3. This creates a copy under your GitHub account

### Step 2: Update Remote URL
```bash
# Check current remote
git remote -v

# Add your fork as origin (replace YOUR_USERNAME)
git remote set-url origin https://github.com/YOUR_USERNAME/Autoxium.git

# Or add it as a new remote
git remote add myfork https://github.com/YOUR_USERNAME/Autoxium.git
```

### Step 3: Stage Your Changes
```bash
# Add all modified files
git add -A

# Or add specific files/folders
git add src/autoxium/ui/
git add src/autoxium/core/adb_wrapper.py
git add src/autoxium/utils/device_names.py
git add pyproject.toml
```

### Step 4: Commit Your Changes
```bash
# Create a meaningful commit message
git commit -m "feat: Add theme support, improve device detection, and reorganize UI

- Added Light/Dark theme switching with ThemeManager
- Fixed device name detection using manufacturer-specific properties
- Created device name mapping database for Samsung, Google, Xiaomi, OnePlus
- Reorganized UI folder: layouts/ for sidebars/topbar, style/ for theming
- Updated table to show Product Name and Model Name correctly
- Removed alternating row colors and added outline: none
- Added psutil dependency for system metrics"
```

### Step 5: Push to Your Fork
```bash
# Push to your fork
git push origin main

# Or if you created a new remote
git push myfork main
```

## Option 2: Create a New Branch (For Pull Request)

If you want to contribute back to the original repository:

```bash
# Create a new feature branch
git checkout -b feature/theme-and-device-improvements

# Stage and commit (same as above)
git add -A
git commit -m "feat: Add theme support and improve device detection"

# Push to your fork
git push origin feature/theme-and-device-improvements
```

Then create a Pull Request on GitHub from your fork to the original repo.

## Option 3: Keep Local Changes Only

If you just want to keep your changes locally without pushing:

```bash
# Commit locally
git add -A
git commit -m "Local improvements: themes, device detection, UI reorganization"

# Don't push - keep it local
```

## Useful Git Commands

### Check what changed
```bash
# See all changes
git status

# See detailed diff
git diff

# See what files were renamed/moved
git status -v
```

### Undo changes (if needed)
```bash
# Unstage files
git reset HEAD <file>

# Discard changes to a file
git restore <file>

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### Clean up test files
```bash
# Remove test files from tracking
git rm --cached test_device_props.py
git rm --cached test_current_detection.py
git rm --cached check_device_info.bat

# Add to .gitignore
echo "test_*.py" >> .gitignore
echo "*.bat" >> .gitignore
```

## Recommended Next Steps

1. **Create a .gitignore** (if not exists) to exclude:
   ```
   __pycache__/
   *.pyc
   *.pyo
   test_*.py
   check_device_info.bat
   .vscode/
   .idea/
   ```

2. **Stage your changes**:
   ```bash
   git add -A
   ```

3. **Commit with a good message**:
   ```bash
   git commit -m "feat: Major UI and device detection improvements"
   ```

4. **Push to your repository**:
   ```bash
   git push origin main
   ```

## Summary of Your Changes

**Modified Files:**
- `pyproject.toml` - Added psutil dependency
- `src/autoxium/core/adb_wrapper.py` - Improved device detection
- `src/autoxium/ui/components/device_table.py` - Updated table styling
- `src/autoxium/ui/main_window.py` - Updated imports
- `src/autoxium/ui/pages/*.py` - Updated style imports

**Deleted Files:**
- `src/autoxium/ui/components/sidebar.py` → moved to layouts/
- `src/autoxium/ui/components/top_bar.py` → moved to layouts/
- `src/autoxium/ui/mirror_window.py` → moved to components/
- `src/autoxium/ui/styles.py` → split into style/ module

**New Files:**
- `src/autoxium/ui/layouts/` - New folder for layout components
- `src/autoxium/ui/style/` - New modular styling system
- `src/autoxium/ui/components/mirror_window.py` - Moved here
- `src/autoxium/utils/device_names.py` - Device mapping database

Need help with any specific Git operation? Let me know!
