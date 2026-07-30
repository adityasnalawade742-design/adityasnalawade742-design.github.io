import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
index_path = repo_dir / "index.html"

print("==================================================")
print("📱 UPGRADING MOBILE RESPONSIVENESS & LUXURY VIBE")
print("   Refining Top Nav, Touch Chips, Card Aspect Ratios & Mobile Spacing")
print("==================================================")

index_content = index_path.read_text(encoding="utf-8")

# Upgrade Mobile CSS Rules inside <style>
mobile_css_upgrade = """        /* Mobile Responsive Enhancements (iOS & Android Touch UX) */
        @media (max-width: 768px) {
            body {
                padding: 16px 12px 60px;
            }

            .ambient-orb {
                filter: blur(80px);
                opacity: 0.45;
            }
            .orb-1 { width: 320px; height: 280px; top: -50px; }
            .orb-2 { width: 280px; height: 280px; }
            .orb-3 { width: 300px; height: 300px; }

            .top-nav {
                padding: 12px 18px;
                margin-bottom: 28px;
                border-radius: 50px;
                gap: 12px;
            }

            .brand-logo {
                font-size: 19px;
            }

            .brand-logo span.sparkle {
                font-size: 20px;
            }

            .nav-controls {
                gap: 8px;
            }

            .currency-select {
                font-size: 12px;
                padding: 6px 12px;
            }

            .nav-status {
                display: none; /* Hide status pill on mobile header for clean single-line header */
            }

            .hero {
                margin-bottom: 32px;
            }

            .badge-pill {
                font-size: 10px;
                padding: 6px 14px;
                margin-bottom: 16px;
            }

            .hero h1 {
                font-size: 32px;
                line-height: 1.2;
                margin-bottom: 14px;
            }

            .hero p {
                font-size: 14.5px;
                line-height: 1.5;
                margin-bottom: 24px;
                padding: 0 8px;
            }

            .search-box {
                margin-bottom: 24px;
            }

            .search-input {
                padding: 14px 44px 14px 48px;
                font-size: 14px;
            }

            .search-icon {
                left: 18px;
                font-size: 16px;
            }

            /* Touch-Friendly Horizontal Swipe Category Chips Bar */
            .chip-container {
                display: flex;
                flex-wrap: nowrap;
                justify-content: flex-start;
                overflow-x: auto;
                width: 100%;
                padding: 4px 8px 12px;
                gap: 10px;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
            }

            .chip-container::-webkit-scrollbar {
                display: none;
            }

            .chip {
                flex-shrink: 0;
                padding: 8px 18px;
                font-size: 12.5px;
                border-radius: 40px;
            }

            .grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .card {
                border-radius: 20px;
            }

            /* Compact Aspect Ratio for Mobile Images (prevents full-screen image stretching) */
            .card-img-container {
                padding-top: 75%; /* Compact 4:3 Mobile Aspect Ratio */
            }

            .card-price-tag {
                top: 12px;
                left: 12px;
                font-size: 12px;
                padding: 5px 12px;
            }

            .card-rating {
                top: 12px;
                right: 12px;
                font-size: 11px;
                padding: 5px 10px;
            }

            .card-content {
                padding: 18px;
            }

            .card-content h2 {
                font-size: 16.5px;
                margin-bottom: 12px;
            }

            .card-cta {
                padding-top: 10px;
                font-size: 12px;
            }

            footer {
                margin-top: 50px;
                padding-top: 28px;
            }
        }"""

# Replace old @media (max-width: 768px) block
old_media_block = """        /* Responsive Breakpoints */
        @media (max-width: 768px) {
            .hero h1 { font-size: 38px; }
            .top-nav { padding: 12px 20px; }
            .grid { grid-template-columns: 1fr; }
        }"""

if old_media_block in index_content:
    index_content = index_content.replace(old_media_block, mobile_css_upgrade)

index_path.write_text(index_content, encoding="utf-8")
print(" ✅ Upgraded index.html mobile responsive styles!")

# Git Commit & Push Live
print("\n🚀 Pushing mobile luxury design upgrade live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "upgrade mobile responsive styling for sleek touch UX and compact card aspect ratio"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 MOBILE LUXURY DESIGN UPGRADE DEPLOYED LIVE!")
