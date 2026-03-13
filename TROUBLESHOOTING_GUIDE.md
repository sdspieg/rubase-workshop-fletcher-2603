# Troubleshooting Guide & Common Issues

## Critical Reminders for Claude

### 1. ALWAYS VERIFY FIRST!
- **Problem**: Claiming changes work without testing
- **Solution**: Use Playwright to verify on live GitHub Pages site
- **Example**:
```python
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://sdspieg.github.io/rubase-workshop-fletcher-2603/...')
    # Verify changes are live
"
```

### 2. Iterate Until 100% Correct
- Don't stop at "good enough"
- If user says something isn't right, verify and fix immediately
- Keep working until exactly as requested

## GitHub Pages Issues

### .nojekyll File
- **Problem**: GitHub Pages doesn't serve directories starting with underscore (_)
- **Solution**: Add `.nojekyll` file to repository root
```bash
touch .nojekyll
git add .nojekyll
git commit -m "Add .nojekyll for GitHub Pages"
```

### 404 Errors After Push
- **Problem**: Files show 404 even after pushing to GitHub
- **Solution**:
  1. Wait 1-2 minutes for GitHub Pages to update
  2. Ensure `.nojekyll` file exists
  3. Check file paths are correct (case-sensitive!)

## File Handling Errors

### Glob Pattern Errors
- **Problem**: `ls *.html` fails with "cannot access 'glob': No such file or directory"
- **Solution**: Quote the pattern or use proper escaping
```bash
# Wrong
ls /path/*.html

# Right
ls /path/ | grep "\.html$"
# Or
find /path -name "*.html"
```

### Converting PowerPoint to Individual PNG Slides
- **Problem**: LibreOffice creates one combined image instead of individual slides
- **Solution**: Convert to PDF first, then use pdf2image
```python
# Step 1: Convert to PDF
soffice --headless --convert-to pdf --outdir /tmp "presentation.pptx"

# Step 2: Convert PDF to PNGs
from pdf2image import convert_from_path
images = convert_from_path('/tmp/presentation.pdf')
for i, image in enumerate(images, 1):
    image.save(f'slide-{i}.png', 'PNG')
```

## Project Structure

### Application Architecture
```
rubase-workshop-fletcher-2603/
├── index.html                 # Main landing page with module grid
├── modules/
│   ├── workshop-overview/     # Overview module
│   │   └── index.html        # Navigation hub with schedule cards
│   ├── build/                # Day 1 module
│   ├── collect/              # Day 2 module
│   │   └── openalex/        # OpenAlex presentations
│   └── analyze/              # Day 3 module
│       ├── index.html        # Module hub with sidebar + resources
│       └── *.html           # Individual presentations
└── Day3_Workshop_Package/     # Workshop materials and scripts
```

### Key UI Components

#### Module Schedule Cards (workshop-overview/index.html)
- Located in the center content area
- Each day has its own card with schedule details
- Cards link to respective module pages

#### Module Index Pages
- **Left Sidebar**: Navigation within module
- **Center Content**: Main content area
- **Right Resources Panel**: Related materials and links

#### Slide Presentations
- Full-screen slides with navigation
- Dark blue gradient backgrounds
- Cyan/green/yellow/orange color scheme
- Navigation: Previous/Next buttons + keyboard arrows

## CSS/Styling Issues

### Split-Pane Display Problem
- **Problem**: Slides showing side-by-side instead of individual
- **Solution**: Fix CSS display properties
```css
/* Wrong */
.slide { display: none; }
.slide.title-slide { display: flex; }  /* Overrides active state! */

/* Right */
.slide { display: none; }
.slide.active { display: block; }
.slide.title-slide.active { display: flex; }
```

### Dark Theme Not Applying
- **Problem**: Dark background not showing after push
- **Solution**:
  1. Clear browser cache
  2. Wait for GitHub Pages to update
  3. Verify CSS gradient syntax is correct

## Git Issues

### Large File Errors
- **Problem**: Files over 100MB can't be pushed to GitHub
- **Solution**:
  1. Remove large files from git
  2. Add to .gitignore
```bash
git rm --cached large_file.json
echo "large_file.json" >> .gitignore
```

### Permission Errors on Push
- **Problem**: "unable to unlink" warnings
- **Solution**: Usually harmless if push succeeds (check commit hash)

## Python/Library Issues

### python-pptx Shape Iteration
- **Problem**: `for shape in slide.shapes[:3]` causes AttributeError
- **Solution**: Iterate directly without slicing
```python
# Wrong
for shape in slide.shapes[:3]:

# Right
for i, shape in enumerate(slide.shapes):
    if i >= 3: break
```

### Playwright Timeout Errors
- **Problem**: Element not found within timeout
- **Solution**:
  1. Check if page loaded correctly
  2. Verify selector is correct
  3. Add wait conditions
```python
page.wait_for_load_state('networkidle')
page.wait_for_selector('.slide', timeout=10000)
```

## Common Workflow Mistakes

### Not Using Project Root
- **Problem**: Running commands from wrong directory
- **Solution**: Always `cd` to project root first
```bash
cd /mnt/c/Users/Stephan/Dropbox/Presentations/2603\ -\ Boston_instructors/rubase-workshop-fletcher-2603
```

### Forgetting to Add Files to Git
- **Problem**: Changes not appearing on GitHub Pages
- **Solution**: Always check `git status` and add all needed files
```bash
git add -A  # Add all files
git status  # Verify what will be committed
```

### Not Checking File Paths
- **Problem**: Links broken due to incorrect paths
- **Solution**:
  1. Use relative paths in HTML
  2. Verify paths are case-sensitive
  3. Test locally before pushing

## Slide Presentation Guidelines

### Visual Consistency
- Dark blue gradient backgrounds (#0a192f → #1e3c72 → #2a5298)
- Bright accent colors:
  - Cyan (#00ffff) for primary highlights
  - Green (#00ff7f) for success/positive
  - Yellow (#ffff00) for attention
  - Orange (#ffa500) for warnings
- Glowing text shadows for neon effect
- 92% width, 88vh height for slides

### Semantic Emojis (Not Excited!)
- 📊 for data/statistics
- 🔬 for research
- 📅 for dates/timeline
- 🌍/🌎/🌏 for global/geographic
- 🎯 for goals/targets
- ⚠️ for warnings
- ✅ for completed/success
- 🚫 for limitations/cannot do

## Testing Commands

### Verify Slides Work
```bash
python verify_final.py     # Full verification
python verify_buttons.py   # Button verification
```

### Quick GitHub Pages Check
```python
# Check if a page is live
import requests
response = requests.get('https://sdspieg.github.io/rubase-workshop-fletcher-2603/page.html')
print(f"Status: {response.status_code}")
```

## Remember: The Three Golden Rules

1. **ALWAYS VERIFY** - Test on live site, not just local files
2. **ITERATE TO 100%** - Don't stop until exactly right
3. **CHECK GITHUB PAGES** - Wait for updates, ensure .nojekyll exists