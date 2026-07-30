import os
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
python_exe = sys.executable
script_path = repo_dir / "sync_exact_amazon_prices.py"

print("==================================================")
print("⏰ STEP 3: CREATING AUTOMATED 2:00 AM PRICE SYNC JOB")
print("==================================================")

task_name = "PinterestAutoAffiliatePriceSync"
cmd = f'schtasks /Create /TN "{task_name}" /TR "{python_exe} \\"{script_path}\\"" /SC DAILY /ST 02:00 /F'

print(f"Executing Windows Task Scheduler command:\n{cmd}\n")

try:
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print(f" ✅ SUCCESS: Windows Task Scheduler job '{task_name}' created!")
        print(f" 🕒 Scheduled to run automatically every night at 2:00 AM!")
    else:
        print(f" ⚠️ Task Scheduler output: {res.stdout or res.stderr}")
        print(" ℹ️ Note: If admin elevation is required, you can also run 'schtasks' from Administrator Command Prompt.")
except Exception as e:
    print(f" ⚠️ Could not auto-create Windows task: {e}")

print("==================================================")
