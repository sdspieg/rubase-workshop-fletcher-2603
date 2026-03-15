#!/usr/bin/env python3
"""Check all HTML files for Home button navigation"""

import os
import glob

def check_home_button(file_path):
    """Check if file has Home button"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            has_home = '🏠 Home' in content
            has_module = 'Module' in content and ('onclick' in content or 'href' in content)
            return has_home, has_module
    except:
        return False, False

print("=== COMPLETE HOME BUTTON CHECK ===\n")

# Define modules for each day
days = {
    "DAY 1": {
        "Welcome": "modules/welcome/*.html",
        "Bibliometrics": "modules/bibliometrics/*.html"
    },
    "DAY 2": {
        "OpenAlex": "modules/openalex/*.html",
        "Corpus": "modules/corpus/*.html"
    },
    "DAY 3": {
        "Analyze": "modules/analyze/*.html"
    }
}

base_path = "/mnt/c/Users/Stephan/Dropbox/Presentations/2603 - Boston_instructors/rubase-workshop-fletcher-2603"

for day, modules in days.items():
    print(f"\n📚 {day}:")
    for module_name, pattern in modules.items():
        full_pattern = os.path.join(base_path, pattern)
        files = glob.glob(full_pattern)

        if not files:
            print(f"  {module_name}: No HTML files found")
            continue

        print(f"  {module_name}:")
        for file_path in sorted(files):
            if 'backup' in file_path or 'old' in file_path:
                continue  # Skip backup files

            filename = os.path.basename(file_path)
            has_home, has_module = check_home_button(file_path)

            status = ""
            if has_home and has_module:
                status = "✅ Home + Module buttons"
            elif has_home:
                status = "✅ Home button only"
            elif has_module:
                status = "⚠️  Module button only (NO HOME)"
            else:
                status = "❌ NO NAVIGATION"

            print(f"    {filename:<35} {status}")

print("\n" + "="*60)
print("SUMMARY:")
print("✅ = Has Home button")
print("⚠️  = Missing Home button")
print("❌ = No navigation at all")