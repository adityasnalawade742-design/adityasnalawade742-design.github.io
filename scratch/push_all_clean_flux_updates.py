import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent

print("==================================================")
print("🚀 PUSHING ALL 21 CLEAN FLUX BADGE OVERLAYS TO GITHUB MAIN")
print("==================================================")

try:
    subprocess.run(["git", "add", "-A"], check=True, cwd=str(repo_dir))
    subprocess.run(["git", "commit", "-m", "Sync 21 clean Flux Dev AI images & price overlay badges to GitHub main"], check=False, cwd=str(repo_dir))
    subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(repo_dir))
    print("🎉 SUCCESS: Synced 21 clean Flux AI images & graphic badges live on GitHub Pages!")
except Exception as e:
    print(f"⚠️ Git push warning: {e}")

print("==================================================")
