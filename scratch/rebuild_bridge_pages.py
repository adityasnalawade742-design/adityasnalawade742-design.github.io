import sys
sys.path.append("G:/CLI/pinterest-auto-affiliate")
import json
from modules.bridge_creator import generate_bridge_page

reg = json.loads(open("product_price_registry.json", encoding="utf-8").read())

# Re-generate bridge_B0BZXNSW5K.html
prod_b0b = reg.get("B0BZXNSW5K", {
    "title": "Bedside Table Lamp for Bedroom - Dimmable Touch, USB A+C, AC Outlet",
    "current_price": "$19.99",
    "rating": "4.8",
    "features": [
        "3-WAY DIMMABLE TOUCH CONTROL",
        "DUAL USB-A & USB-C FAST CHARGING",
        "BUILT-IN AC POWER OUTLET",
        "SOFT GLARE-FREE FABRIC LINEN SHADE",
        "ENERGY-SAVING LED BULB INCLUDED"
    ]
})
seo_b0b = {
    "pin_title": "Bedside Table Lamp for Bedroom (Touch + USB A+C)",
    "description": "Transform your bedroom into a cozy sanctuary with this 3-way dimmable touch control bedside lamp featuring built-in USB A+C charging ports and an AC outlet for your nightstand."
}
generate_bridge_page(prod_b0b, seo_b0b, "B0BZXNSW5K")

# Re-generate bridge_B0D8P8CSYP.html
prod_bird = reg.get("B0D8P8CSYP", {
    "title": "Cute Bird Dimmable Touch Night Lamp",
    "current_price": "$20.56",
    "rating": "4.8",
    "features": [
        "SOFT TOUCH DIMMABLE ILLUMINATION",
        "PORTABLE RECHARGEABLE BATTERY",
        "WARM WOODGRAIN AESTHETIC BASE",
        "PERFECT NIGHTSTAND ACCENT LIGHT"
    ]
})
seo_bird = {
    "pin_title": "Cute Bird Dimmable Touch Night Lamp",
    "description": "Add a touch of whimsical cozy charm to your room with this dimmable touch bird night lamp."
}
generate_bridge_page(prod_bird, seo_bird, "B0D8P8CSYP")

print("🎉 Successfully rebuilt bridge_B0BZXNSW5K.html and bridge_B0D8P8CSYP.html with upgraded text template!")
