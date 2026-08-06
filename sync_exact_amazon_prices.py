import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent

print("=========================================================================")
print("⏰ AUTOMATED DAILY MULTI-REGION PRICE SYNC (TASK SCHEDULER ENTRYPOINT)")
print("=========================================================================\n")

registry_path = repo / "product_price_registry.json"
if not registry_path.exists():
    print("⚠️ Registry missing. Aborting sync.")
    sys.exit(0)

# Delegate directly to master sequential sync suite which uses Playwright + contamination guards
master_script = repo / "sync_all_regional_prices_master.py"

res = subprocess.run([sys.executable, str(master_script)], cwd=str(repo), check=False)
if res.returncode == 0:
    print("\n✅ Daily Price Sync Completed Successfully.")
else:
    print(f"\n⚠️ Daily Price Sync completed with return code {res.returncode}.")

