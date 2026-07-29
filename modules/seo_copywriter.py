import json
import time
import re
import sys
import io
from pathlib import Path

# UTF-8 stdout fix
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def generate_pin_seo_data(product_title: str, price: str = "", category: str = "") -> dict:
    """
    Generates High-Reach Pinterest SEO titles, viral problem-solving descriptions,
    image hooks, feature callouts, and 5 targeted Pinterest hashtags for maximum search visibility & CTR.
    """
    t_lower = product_title.lower()

    # 1. Diffusers / Flame Atmosphere
    if "diffuser" in t_lower or "flame" in t_lower or "volcano" in t_lower:
        clean_name = "Flame Aroma Essential Oil Diffuser"
        pin_title = "Say Goodbye To Harsh Overhead Lights 🕯️ Flame Aroma Diffuser"
        subtitle_hook = ""
        badge_hook = "COZY NIGHT VIBES"
        features = ["VOLCANO FLAME MIST", "WARM AMBER GLOW", "AUTO SHUT OFF", "ESSENTIAL OIL READY"]
        theme_style = "dark_obsidian_neon"
        description = (
            "Tired of stressful overhead lighting? Transform your bedroom into a soothing cozy sanctuary with this viral Flame Aroma Essential Oil Diffuser. "
            "Features realistic volcano flame mist, warm amber LED ambient lighting, and ultra-quiet humidification. "
            "Tap link to check live price on Amazon! #cozyroomdecor #flamediffuser #aestheticdecor #amazonfinds #bedroomvibes"
        )
        keywords = ["flame aroma diffuser", "cozy room decor", "aesthetic bedroom lighting", "essential oil diffuser", "amazon room finds"]

    # 2. Donut Vases / Boho Ceramics
    elif "vase" in t_lower or "donut" in t_lower or "pampas" in t_lower:
        clean_name = "White Ceramic Donut Vases"
        pin_title = "Elevate Your Table Vibe 🌿 White Ceramic Donut Vase Set"
        subtitle_hook = ""
        badge_hook = "VANITY GOALS"
        features = ["MATTE CERAMIC FINISH", "SET OF 2 VASES", "PAMPAS GRASS READY", "HANDCRAFTED BOHO"]
        theme_style = "floating_cream"
        description = (
            "Transform your coffee table or nightstand with this viral White Ceramic Donut Vase Set! "
            "Features hollow matte ceramic craftsmanship designed for pampas grass and modern minimalist room transformations. "
            "Tap link to check price on Amazon! #cozyroomdecor #donutvase #bohodecor #aestheticroom #amazonfinds"
        )
        keywords = ["white ceramic vase", "donut vase set", "boho room decor", "aesthetic table decor", "amazon home finds"]

    # 3. Mirrors / Vanity Decor
    elif "mirror" in t_lower or "wavy" in t_lower or "vanity" in t_lower:
        clean_name = "White Wavy Wall Vanity Mirror"
        pin_title = "Upgrade Your Vanity Vibe ✨ White Wavy Wall Mirror"
        subtitle_hook = ""
        badge_hook = "VANITY GOALS"
        features = ["CREAM WAVY FRAME", "HIGH CLARITY GLASS", "CUTE SQUIGGLE DESIGN", "WALL & VANITY MOUNT"]
        theme_style = "floating_cream"
        description = (
            "Tired of plain boring mirrors? Give your bedroom the ultimate aesthetic upgrade with this viral White Wavy Wall Vanity Mirror. "
            "Features solid cream curvy framing and high-definition glass that illuminates your space. "
            "Tap link to shop now on Amazon! #wavymirror #vanitydecor #aestheticroom #cozyroomdecor #amazonfinds"
        )
        keywords = ["wavy wall mirror", "vanity mirror decor", "aesthetic bedroom mirror", "squiggle mirror", "amazon room finds"]

    # 4. Suncatchers / Crystals
    elif "suncatcher" in t_lower or "prism" in t_lower or "crystal" in t_lower:
        clean_name = "Crystal Prism Window Suncatcher"
        pin_title = "Fill Your Room With Rainbows 🌈 Crystal Prism Window Suncatcher"
        subtitle_hook = ""
        badge_hook = "RAINBOW MAKER"
        features = ["K9 CRYSTAL PRISM", "RAINBOW REFLECTIONS", "WINDOW HANGING CHAIN", "SUNLIGHT SPECTRUM"]
        theme_style = "sunlight_crystal"
        description = (
            "Transform plain morning sunlight into magical room rainbows! This viral Crystal Prism Window Suncatcher "
            "catches natural sunlight and projects dazzling color spectrums across your walls and ceiling. "
            "Tap link to check price on Amazon! #suncatcher #crystalprism #cozyroomdecor #rainbowmaker #amazonfinds"
        )
        keywords = ["crystal suncatcher", "window prism rainbow maker", "cozy room decor", "sunlight decor", "amazon home finds"]

    # 5. Sunset Projection Lamp
    elif "sunset" in t_lower:
        clean_name = "Tsrarey Sunset Projection Lamp"
        pin_title = "Golden Hour Vibes Anytime 🌅 21-Color Sunset Projector Lamp"
        subtitle_hook = ""
        badge_hook = "VIRAL ROOM FIND"
        features = ["21 COLOR MODES", "180 DEGREE ROTATION", "APP & BUTTON CONTROL", "GOLDEN HOUR GLOW"]
        theme_style = "dark_obsidian_neon"
        description = (
            "Bring eternal golden hour into your room! This viral Tsrarey Sunset Projection Lamp "
            "projects warm 21-color sunset halos across your walls, perfect for cozy reading nights and photo aesthetics. "
            "Tap link to shop now on Amazon! #sunsetlamp #goldenhourvibes #cozyroomdecor #aestheticlighting #amazonfinds"
        )
        keywords = ["sunset projection lamp", "golden hour light", "cozy room decor", "aesthetic projector", "amazon room finds"]

    # 6. LED Note Board
    elif "note board" in t_lower or "glowing" in t_lower or "acrylic" in t_lower:
        clean_name = "LED Acrylic Glowing Desktop Note Board"
        pin_title = "Light Up Your Daily Goals ✨ Glowing Acrylic Note Board"
        subtitle_hook = ""
        badge_hook = "DESK GOALS"
        features = ["7 LIGHT COLORS", "DRY ERASE ACRYLIC", "WOODEN LED BASE", "7 COLOR PENS INCL"]
        theme_style = "dark_obsidian_neon"
        description = (
            "Tired of forgotten notes and sticky pads? Upgrade your workspace with this viral LED Acrylic Glowing Desktop Note Board! "
            "Draw, write daily goals, and watch your notes illuminate in 7 glowing neon colors on a solid wooden base. "
            "Tap link to check price on Amazon! #noteboard #desksetup #cozyroomdecor #aestheticdesk #amazonfinds"
        )
        keywords = ["led acrylic note board", "glowing desk memo", "cozy desk decor", "aesthetic workspace", "amazon finds"]

    # 7. Mushroom Lamp
    elif "mushroom" in t_lower:
        clean_name = "Dawnwake Mushroom Touch Table Lamp"
        pin_title = "Cozy Bedroom Essential 🍄 Dawnwake Mushroom Touch Lamp"
        subtitle_hook = ""
        badge_hook = "COZY NIGHT VIBES"
        features = ["TOUCH SENSOR DIMMER", "WARM AMBIENT GLOW", "GLASS DOME SHADE", "BEDSIDE ELEGANCE"]
        theme_style = "floating_luxury"
        description = (
            "Tired of harsh bedroom lighting? Elevate your nightstand aesthetic with this viral Dawnwake Mushroom Touch Table Lamp! "
            "Features smooth dimmable touch controls and warm ambient glow for cozy reading nights. "
            "Tap link to shop now on Amazon! #mushroomlamp #bedside lamp #cozyroomdecor #aestheticroom #amazonfinds"
        )
        keywords = ["mushroom touch lamp", "bedside table lamp", "cozy room decor", "aesthetic nightstand", "amazon room finds"]

    # 8. Flower / Lily Lamp
    elif "flower" in t_lower or "lily" in t_lower:
        clean_name = "Lily of the Valley Flower Lamp"
        pin_title = "Fairy Tale Room Vibe 🌸 Lily of the Valley Flower Lamp"
        subtitle_hook = "FLORAL AMBIENT ELEGANCE"
        badge_hook = "ROOM TRANSFORMATION"
        features = ["HANDCRAFTED GLASS PETALS", "WARM FLORAL GLOW", "VINTAGE GREEN STEM", "NIGHTSTAND ACCENT"]
        theme_style = "floating_luxury"
        description = (
            "Transform your nightstand into a botanical fairy tale sanctuary! This viral Lily of the Valley Flower Lamp "
            "emits a delicate warm glow through handcrafted floral glass petals. "
            "Tap link to check price on Amazon! #flowerlamp #lilyofthevalley #cozyroomdecor #aestheticlamp #amazonfinds"
        )
        keywords = ["lily of the valley lamp", "flower table lamp", "cozy room decor", "floral nightstand light", "amazon home finds"]

    # 9. Bird Lamp
    elif "bird" in t_lower:
        clean_name = "Cute Bird Dimmable Touch Night Lamp"
        pin_title = "Aesthetic Nightstand Find 🐦 Cute Bird Touch Night Lamp"
        subtitle_hook = "CHARMING BIRD ILLUMINATION"
        badge_hook = "BEDSIDE FAVORITE"
        features = ["TOUCH SENSOR CONTROL", "DIMMABLE NIGHT LIGHT", "RECHARGEABLE BATTERY", "CHARMING BIRD SHAPE"]
        theme_style = "floating_luxury"
        description = (
            "Add a touch of whimsical warmth to your bedtime routine! This viral Cute Bird Dimmable Touch Night Lamp "
            "features smooth touch dimming and a soft golden glow perfect for late night reading. "
            "Tap link to shop now on Amazon! #birdlamp #nightlight #cozyroomdecor #bedroomideas #amazonfinds"
        )
        keywords = ["bird touch lamp", "cute nightstand light", "cozy room decor", "dimmable night light", "amazon finds"]

    # 10. Fenmzee Bedside Touch Lamp (Default Touch Lamp)
    else:
        clean_name = "Fenmzee Bedside Table Touch Lamp"
        pin_title = "Say Goodbye To Overhead Lights 🕯️ Fenmzee Touch Bedside Lamp"
        subtitle_hook = "WARM BEDTIME AMBIANCE"
        badge_hook = "BEDSIDE FAVORITE"
        features = ["3 WAY TOUCH DIMMER", "WARM AMBER GLOW", "USB CHARGING PORT", "FABRIC SHADE FINISH"]
        theme_style = "floating_luxury"
        description = (
            "Say goodbye to harsh bedroom lights! Transform your nightstand into a calming sanctuary with the Fenmzee Bedside Touch Lamp. "
            "Features 3-way touch dimming and warm ambient lighting tailored for bedtime reading and cozy room vibes. "
            "Tap link to shop now on Amazon! #cozyroomdecor #bedsidelamp #nightstandlighting #bedroomvibes #amazonfinds"
        )
        keywords = ["bedside touch lamp", "cozy room decor", "nightstand lighting", "bedroom transformation", "amazon room finds"]

    return {
        "pin_title": pin_title,
        "image_hook": clean_name,
        "subtitle_hook": subtitle_hook,
        "badge_hook": badge_hook,
        "features": features,
        "theme_style": theme_style,
        "description": description,
        "suggested_board": "Cozy Room & Desk Decor",
        "keywords": keywords
    }
