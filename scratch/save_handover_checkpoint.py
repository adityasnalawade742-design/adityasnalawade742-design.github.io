import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent

print("==================================================")
print("💾 SAVING MASTER HANDOVER DOCUMENTATION & CHECKPOINT TO GITHUB MAIN")
print("==================================================")

try:
    subprocess.run(["git", "add", "-A"], check=True, cwd=str(repo_dir))
    subprocess.run(["git", "commit", "-m", "Save master handover documentation and project progress checkpoint"], check=False, cwd=str(repo_dir))
    subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(repo_dir))
    print("🎉 SUCCESS: Master handover documentation saved & committed live to GitHub main!")
except Exception as e:
    print(f"⚠️ Git push warning: {e}")

print("==================================================")
