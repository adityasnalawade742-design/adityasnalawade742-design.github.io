import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")

py_files = []
for p in repo.glob("**/*.py"):
    if ".git" not in str(p) and "__pycache__" not in str(p) and "venv" not in str(p):
        py_files.append(p)

print("==================================================")
print("🐍 PYTHON FILES BREAKDOWN IN REPOSITORY")
print("==================================================")

by_folder = {}
for p in py_files:
    folder = str(p.parent.relative_to(repo))
    if folder == ".":
        folder = "Root Directory"
    if folder not in by_folder:
        by_folder[folder] = []
    by_folder[folder].append(p.name)

for folder, files in sorted(by_folder.items()):
    print(f"\n📂 {folder} ({len(files)} files):")
    for f in sorted(files):
        print(f"   • {f}")

print("\n==================================================")
print(f"📊 TOTAL ACTIVE PYTHON (.py) FILES: {len(py_files)}")
print("==================================================")
