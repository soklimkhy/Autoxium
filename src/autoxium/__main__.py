import sys
import os
from pathlib import Path

# Add the src directory to sys.path to ensure we can import internal modules 
# if running directly as script (though -m usually handles this)
src_path = Path(__file__).resolve().parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from autoxium.ui.main_window import run_app

def main():
    run_app()

if __name__ == "__main__":
    main()
