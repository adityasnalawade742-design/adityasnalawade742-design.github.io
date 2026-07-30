import sys, io
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.amazon_extractor import has_text_annotation, select_clean_photo_or_skip

sample_photos = [
    "https://m.media-amazon.com/images/I/81E5p8uvtWL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71MfShfsWyL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/710HFWtubIL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/817JiwgvYTL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81n5zERXHSL._AC_SL1500_.jpg"
]

print("🔍 Testing Enhanced High-Frequency Text & Glyph Detector on B0GGHJ1J4L Photos...\n")
clean_photo, should_skip = select_clean_photo_or_skip(sample_photos)

if should_skip:
    print("\n⚠️ RESULT: Product SKIPPED because ALL listing photos contain text/glyph annotations.")
else:
    print(f"\n✅ RESULT: Found Clean Text-Free Photo -> {clean_photo}")
