"""
Notebook-style walkthrough for the Retail Sales & Profitability Analysis.
Run from the project root after placing the CSV in data/.
"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from run_analysis import main

if __name__ == "__main__":
    main()
