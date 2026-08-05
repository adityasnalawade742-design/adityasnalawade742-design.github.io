import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path('.').resolve()

print("=========================================================================")
print("🚀 DEPLOYMENT & GITHUB REMOTE SYNC AUDIT")
print("=========================================================================\n")

# 1. Local Working Tree Status
res_stat = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd=str(repo))
clean = (res_stat.stdout.strip() == "")
print(f"1. 🌳 Local Working Tree: {'✅ CLEAN (100% Committed)' if clean else '⚠️ UNCOMMITTED CHANGES PRESENT'}")
if not clean:
    print("   Uncommitted files:\n", res_stat.stdout.strip())

# 2. Recent Git Commit History
res_log = subprocess.run(['git', 'log', '-n', '6', '--oneline'], capture_output=True, text=True, cwd=str(repo))
print(f"\n2. 📜 Recent Git Commit History:\n{res_log.stdout.strip()}")

# 3. Branch & Remote Sync Status
res_branch = subprocess.run(['git', 'status', '-uno'], capture_output=True, text=True, cwd=str(repo))
print(f"\n3. 🌐 Branch & GitHub Pages Remote Sync:\n{res_branch.stdout.strip()}")

print("\n=========================================================================")
print("🏆 DEPLOYMENT VERIFICATION COMPLETE!")
print("=========================================================================\n")
