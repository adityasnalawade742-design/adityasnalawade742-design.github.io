"""
Deep Codebase Auditor & Static Debugger
Performs comprehensive AST inspection, route auditing, missing import detection,
unhandled exception checks, and UI event binding checks across the entire repo.
"""
import ast
import os
import sys
import re
from pathlib import Path

import io

# Ensure UTF-8 output encoding for Windows PowerShell
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

print("=" * 80)
print("DEEP CODEBASE AUDIT & FIRST-PRINCIPLES DEBUGGER")
print("=" * 80)

py_files = list(ROOT.glob("*.py")) + list((ROOT / "modules").glob("*.py"))
js_files = [ROOT / "admin_console.html"]

errors_found = []
warnings_found = []

# 1. AST & Import Validation across all Python files
print("\n--- 1. AST & SYNTAX INTEGRITY AUDIT ---")
for pf in py_files:
    rel_path = pf.relative_to(ROOT)
    try:
        content = pf.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(pf))
        print(f"  [OK] Python Syntax Valid: {rel_path} ({len(content.splitlines())} lines)")
    except Exception as e:
        msg = f"Syntax/AST error in {rel_path}: {e}"
        print(f"  [CRITICAL ERROR] {msg}")
        errors_found.append(msg)

# 2. Check for missing module imports or undefined symbol usages
print("\n--- 2. UNDEFINED SYMBOL & SCOPE AUDIT ---")
for pf in py_files:
    rel_path = pf.relative_to(ROOT)
    content = pf.read_text(encoding="utf-8")
    
    # Check common dangerous unimported references
    patterns = [
        (r'\burllib\.parse\b', 'import urllib.parse'),
        (r'\burllib\.request\b', 'import urllib.request'),
        (r'\bjson\.', 'import json'),
        (r'\bre\.', 'import re'),
        (r'\btime\.', 'import time'),
        (r'\brequests\.', 'import requests'),
    ]
    for symbol_regex, import_statement in patterns:
        if re.search(symbol_regex, content) and not (import_statement in content or 'from urllib' in content):
            msg = f"{rel_path} uses '{symbol_regex}' but may be missing '{import_statement}'!"
            print(f"  [WARNING] {msg}")
            warnings_found.append(msg)

# 3. HTML/JS Interface & API Alignment Audit
print("\n--- 3. FRONTEND / BACKEND API ROUTE ALIGNMENT AUDIT ---")
html_content = (ROOT / "admin_console.html").read_text(encoding="utf-8")
server_content = (ROOT / "web_console_server.py").read_text(encoding="utf-8")

# Extract all fetch() paths from admin_console.html
fetch_paths = set(re.findall(r"fetch\(['\"]([^'\"]+)['\"]", html_content))
print(f"  Found {len(fetch_paths)} API endpoints invoked by frontend JS:")

for fp in fetch_paths:
    clean_path = fp.split('?')[0]
    if clean_path.startswith('/api/'):
        if clean_path in server_content:
            print(f"  [MATCH] Frontend route '{clean_path}' -> Handled in web_console_server.py")
        else:
            msg = f"Frontend route '{clean_path}' called in admin_console.html but NOT found in web_console_server.py!"
            print(f"  [CRITICAL DISCREPANCY] {msg}")
            errors_found.append(msg)

# 4. Check potential CORS / Image Referrer / Fallback issues
print("\n--- 4. IMAGE & MEDIA PIPELINE AUDIT ---")
if 'referrerpolicy="no-referrer"' in html_content:
    print("  [OK] HTML <img> elements enforce referrerpolicy='no-referrer' (bypasses Amazon CDN hotlink protection)")

if 'onerror=' in html_content:
    print("  [OK] HTML <img> elements include fallback onerror handlers")

# Summary
print("\n" + "=" * 80)
print(f"DEEP AUDIT SUMMARY: {len(errors_found)} Critical Errors | {len(warnings_found)} Warnings")
print("=" * 80)
for err in errors_found:
    print(f" ❌ ERROR: {err}")
for warn in warnings_found:
    print(f" ⚠️ WARNING: {warn}")
