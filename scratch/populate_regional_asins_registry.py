import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
registry_file = repo / "product_price_registry.json"

print("=== 📌 POPULATING REGIONAL ASIN VARIANT MAPPER IN REGISTRY ===")

regional_asins_master = {
    "B07HP22QTZ": {"US": "B07HP22QTZ", "IN": "B07HP22QTZ", "UK": "B07HP22QTZ", "DE": "B07HP22QTZ", "CA": "B07HP22QTZ", "AU": "B07HP22QTZ", "JP": "B07HP22QTZ"},
    "B0BZXNSW5K": {"US": "B0BZXNSW5K", "IN": "B0BZXNSW5K", "UK": "B0BZXNSW5K", "DE": "B0BZXNSW5K", "CA": "B0BZXNSW5K", "AU": "B0BZXNSW5K", "JP": "B0BZXNSW5K"},
    "B0C2YLN3H4": {"US": "B0C2YLN3H4", "IN": "B0C2YLN3H4", "UK": "B0C2YLN3H4", "DE": "B0C2YLN3H4", "CA": "B0C2YLN3H4", "AU": "B0C2YLN3H4", "JP": "B0C2YLN3H4"},
    "B0D1FRDFFX": {"US": "B0D1FRDFFX", "IN": "B0D1FRDFFX", "UK": "B0D1FRDFFX", "DE": "B0D1FRDFFX", "CA": "B0D1FRDFFX", "AU": "B0D1FRDFFX", "JP": "B0D1FRDFFX"},
    "B0D8P8CSYP": {"US": "B0D8P8CSYP", "IN": "B0D8P8CSYP", "UK": "B0D8P8CSYP", "DE": "B0D8P8CSYP", "CA": "B0D8P8CSYP", "AU": "B0D8P8CSYP", "JP": "B0D8P8CSYP"},
    "B0FXLYXM32": {"US": "B0FXLYXM32", "IN": "B0FXLYXM32", "UK": "B0FXLYXM32", "DE": "B0FXLYXM32", "CA": "B0FXLYXM32", "AU": "B0FXLYXM32", "JP": "B0FXLYXM32"},
    "B0DZD1X83N": {"US": "B0DZD1X83N", "IN": "B0DZD1X83N", "UK": "B0DZD1X83N", "DE": "B0DZD1X83N", "CA": "B0DZD1X83N", "AU": "B0DZD1X83N", "JP": "B0DZD1X83N"},
    "B0DXKGL1T2": {"US": "B0DDTPCDLB", "IN": "B0DDTPCDLB", "UK": "B0DDTPCDLB", "DE": "B0DDTPCDLB", "CA": "B0DDTPCDLB", "AU": "B0DDTPCDLB", "JP": "B0DDTPCDLB"},
    "B0GYDXHF4G": {"US": "B0GYDXHF4G"}
}

registry = json.loads(registry_file.read_text(encoding="utf-8"))

for asin, asins_dict in regional_asins_master.items():
    if asin in registry:
        registry[asin]["regional_asins"] = asins_dict
        print(f"  • Product [{asin}]: Added regional_asins -> {asins_dict}")

registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅ product_price_registry.json updated with regional_asins for all 9 products!")
