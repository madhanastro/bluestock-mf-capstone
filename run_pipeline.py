"""
run_pipeline.py
Bluestock Fintech — Mutual Fund Analytics Capstone
Master pipeline script — runs all Day 1-6 scripts in order

Author: Madhankumar V
Intern, Bluestock Fintech Pvt. Ltd.
Date: June 2026
"""

import subprocess
import sys
import os

PYTHON = sys.executable

def run_script(script_path, description):
    """Run a Python script and print status"""
    print(f"\n{'='*55}")
    print(f"Running: {description}")
    print(f"{'='*55}")
    result = subprocess.run([PYTHON, script_path], capture_output=False)
    if result.returncode == 0:
        print(f"✅ {description} — Complete!")
    else:
        print(f"❌ {description} — Failed!")
    return result.returncode

if __name__ == "__main__":
    print("="*55)
    print("BLUESTOCK FINTECH — MF ANALYTICS PIPELINE")
    print("="*55)

    scripts = [
        ("scripts/data_ingestion.py",        "Day 1: Data Ingestion"),
        ("scripts/data_cleaning.py",         "Day 2: Data Cleaning"),
        ("scripts/load_database.py",         "Day 2: Load Database"),
        ("scripts/eda_analysis.py",          "Day 3: EDA Analysis"),
        ("scripts/performance_analytics.py", "Day 4: Performance Analytics"),
        ("scripts/advanced_analytics.py",    "Day 6: Advanced Analytics"),
    ]

    for script, desc in scripts:
        run_script(script, desc)

    print("\n" + "="*55)
    print("🎉 FULL PIPELINE COMPLETE!")
    print("="*55)