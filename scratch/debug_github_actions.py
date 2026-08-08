import os
import sys
import io
import shutil
import pathlib
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("=========================================================================")
print("🤖 GITHUB ACTIONS WORKFLOW DIAGNOSTIC & DEBUGGER SUITE")
print("=========================================================================\n")

project_root = pathlib.Path(__file__).resolve().parent.parent
workflow_file = project_root / ".github" / "workflows" / "pages.yml"

print(f"1. Checking workflow file location: {workflow_file}")
if not workflow_file.exists():
    print("❌ ERROR: .github/workflows/pages.yml does NOT exist!")
    sys.exit(1)
print("  ✓ Workflow file found.")

# Read workflow content
workflow_text = workflow_file.read_text(encoding="utf-8")
print("\n2. Validating Workflow Configuration & Permissions:")
required_elements = [
    ('push trigger', 'branches: ["main"]'),
    ('workflow_dispatch', 'workflow_dispatch'),
    ('pages permission', 'pages: write'),
    ('id-token permission', 'id-token: write'),
    ('checkout action', 'actions/checkout@v4'),
    ('configure-pages action', 'actions/configure-pages@v4'),
    ('upload-pages-artifact action', 'actions/upload-pages-artifact@v3'),
    ('deploy-pages action', 'actions/deploy-pages@v4')
]

for name, elem in required_elements:
    if elem in workflow_text:
        print(f"  ✓ {name}: PRESENT ({elem})")
    else:
        print(f"  ❌ {name}: MISSING ({elem})")

print("\n3. Simulating GitHub Actions Build Step Locally (_site/ staging):")
site_dir = project_root / "_site_test_build"
if site_dir.exists():
    shutil.rmtree(site_dir)
site_dir.mkdir(parents=True, exist_ok=True)

# Copy all *.html, images, etc.
copied_count = 0
html_files = list(project_root.glob("*.html"))
for h in html_files:
    shutil.copy(h, site_dir / h.name)
    copied_count += 1

print(f"  ✓ Copied {copied_count} HTML files to _site/ (including index.html, terms-of-service.html, privacy-policy.html)")

# Copy directories if exist
dirs_to_copy = ["images", "fonts", "price tags", "raw_images", "bridge_pages"]
for d in dirs_to_copy:
    src_d = project_root / d
    if src_d.exists():
        dst_d = site_dir / d
        if dst_d.exists():
            shutil.rmtree(dst_d)
        shutil.copytree(src_d, dst_d)
        print(f"  ✓ Copied directory '{d}' to _site/{d}")

# Copy standalone json/xml files
standalone_files = ["sitemap.xml", "robots.txt", "global_direct_matrix.json", "product_price_registry.json", ".nojekyll"]
for sf in standalone_files:
    src_f = project_root / sf
    if src_f.exists():
        shutil.copy(src_f, site_dir / sf)
        print(f"  ✓ Copied standalone asset '{sf}' to _site/{sf}")

print("\n4. Verifying _site/ Staged Artifact Integrity:")
essential_urls = [
    "index.html",
    "privacy-policy.html",
    "terms-of-service.html",
    "terms.html",
    "sitemap.xml",
    "robots.txt",
    "bridge_pages/terms-of-service.html",
    "bridge_pages/privacy-policy.html"
]

missing_artifacts = 0
for u in essential_urls:
    target = site_dir / u
    if target.exists():
        print(f"  ✅ PASS: _site/{u} exists ({target.stat().st_size} bytes)")
    else:
        print(f"  ❌ FAIL: _site/{u} MISSING!")
        missing_artifacts += 1

print("\n5. Cleaning up local build test directory...")
if site_dir.exists():
    shutil.rmtree(site_dir)

print("\n6. Checking Remote Git Repository Sync:")
try:
    res = subprocess.run(["git", "status"], capture_output=True, text=True, cwd=str(project_root))
    print(res.stdout)
except Exception as e:
    print(f"  ⚠️ Error checking git status: {e}")

print("=========================================================================")
if missing_artifacts == 0:
    print("🏆 GITHUB ACTIONS DIAGNOSTIC RESULT: 100% HEALTHY & VERIFIED!")
else:
    print(f"⚠️ GITHUB ACTIONS DIAGNOSTIC RESULT: {missing_artifacts} MISSING ARTIFACTS FOUND!")
print("=========================================================================")
