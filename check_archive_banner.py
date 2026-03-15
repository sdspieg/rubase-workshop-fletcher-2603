from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    
    # Navigate to Fletcher archive site
    page.goto('https://sdspieg.github.io/rubase-workshop-fletcher-2603/')
    page.wait_for_load_state('networkidle')
    time.sleep(2)
    
    # Take screenshot focused on the banner
    banner = page.locator('div:has-text("This is an archived workshop")').first
    if banner:
        # Get banner properties
        banner_box = banner.bounding_box()
        if banner_box:
            print(f"Banner found at: {banner_box}")
            
            # Take full screenshot
            page.screenshot(path='Screenshots/archive_banner_full.png')
            
            # Take banner-only screenshot
            page.screenshot(path='Screenshots/archive_banner_only.png', clip={
                'x': 0,
                'y': 0,
                'width': 1920,
                'height': 100
            })
            
            # Get computed styles
            bg_color = page.evaluate('''() => {
                const banner = document.querySelector('div[style*="background: linear-gradient"]');
                return window.getComputedStyle(banner).background;
            }''')
            
            text_color = page.evaluate('''() => {
                const banner = document.querySelector('div[style*="background: linear-gradient"]');
                return window.getComputedStyle(banner).color;
            }''')
            
            print(f"Background: {bg_color}")
            print(f"Text color: {text_color}")
            
            # Check if text is visible
            is_visible = page.is_visible('text=This is an archived workshop')
            print(f"Archive text visible: {is_visible}")
            
            link_visible = page.is_visible('text=View Latest Version')
            print(f"Link visible: {link_visible}")
            
        else:
            print("Could not get banner bounding box")
    else:
        print("Banner not found!")
    
    browser.close()

print("\nScreenshots saved to Screenshots folder")
