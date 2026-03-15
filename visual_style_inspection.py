#!/usr/bin/env python3
"""Visually inspect all slidedecks for styling consistency"""

from playwright.sync_api import sync_playwright
import time
import os
import glob

def inspect_presentations():
    presentations = [
        # Day 1
        ("modules/welcome/welcome-slides.html", "Day 1 - Welcome Slides"),
        ("modules/welcome/welcome-setup.html", "Day 1 - Welcome Setup"),

        # Day 2
        ("modules/openalex/openalex-explorer.html", "Day 2 - OpenAlex Explorer"),
        ("modules/openalex/dashboard.html", "Day 2 - Dashboard"),

        # Day 3
        ("modules/analyze/welcome-day3.html", "Day 3 - Welcome"),
        ("modules/analyze/llm-selection-guide.html", "Day 3 - LLM Selection"),
        ("modules/analyze/ottoman-bank-case-study.html", "Day 3 - Ottoman Bank"),
        ("modules/analyze/wacko-presentation.html", "Day 3 - Wacko"),
        ("modules/analyze/cli-llms-guide.html", "Day 3 - CLI LLMs"),
        ("modules/analyze/deep-research-guide.html", "Day 3 - Deep Research"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        os.makedirs("style_inspection", exist_ok=True)

        for filepath, name in presentations:
            if not os.path.exists(filepath):
                print(f"❌ {name}: File not found")
                continue

            print(f"\n📊 Inspecting: {name}")
            file_url = f"file:///{os.path.abspath(filepath)}"
            page.goto(file_url)
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            # Capture screenshot
            screenshot_name = f"style_inspection/{name.replace(' - ', '_').replace(' ', '_').lower()}.png"
            page.screenshot(path=screenshot_name)

            # Check for common style elements
            try:
                # Check background
                bg_color = page.evaluate("""
                    () => {
                        const body = document.body;
                        const style = window.getComputedStyle(body);
                        return style.backgroundColor;
                    }
                """)

                # Check if gradient backgrounds exist
                has_gradient = page.evaluate("""
                    () => {
                        const slides = document.querySelectorAll('.slide');
                        if (slides.length === 0) return false;
                        const style = window.getComputedStyle(slides[0]);
                        return style.backgroundImage.includes('gradient');
                    }
                """)

                # Check navigation buttons
                has_nav = page.evaluate("""
                    () => {
                        return document.querySelector('button') !== null ||
                               document.querySelector('.nav-btn') !== null ||
                               document.querySelector('.nav-container') !== null;
                    }
                """)

                # Check fonts
                font_family = page.evaluate("""
                    () => {
                        const body = document.body;
                        const style = window.getComputedStyle(body);
                        return style.fontFamily;
                    }
                """)

                print(f"  Background: {bg_color}")
                print(f"  Has Gradient: {'✅' if has_gradient else '❌'}")
                print(f"  Has Navigation: {'✅' if has_nav else '❌'}")
                print(f"  Font Family: {font_family}")
                print(f"  Screenshot: {screenshot_name}")

            except Exception as e:
                print(f"  ⚠️ Error analyzing: {e}")

        browser.close()
        print("\n\n=== VISUAL INSPECTION COMPLETE ===")
        print("Check 'style_inspection' folder for screenshots")

if __name__ == "__main__":
    inspect_presentations()