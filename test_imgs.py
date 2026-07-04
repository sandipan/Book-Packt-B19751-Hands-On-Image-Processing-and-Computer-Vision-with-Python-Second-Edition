import json
import re
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

NOTEBOOK = "Chapter13/Chapter13.ipynb"
IMAGE_FOLDER = Path("Chapter13/images")

# ==========================================================
# Supported image extensions
# ==========================================================

IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
    ".svg",
)

# ==========================================================
# Regular expressions
# ==========================================================

patterns = [

    # Markdown: ![](image.png)
    r'!\[[^\]]*\]\(([^)]+)\)',

    # HTML: <img src="image.png">
    r'<img[^>]+src=["\']([^"\']+)["\']',

    # cv2.imread(...)
    r'cv2\.imread\(\s*[frbuFRBU]*["\']([^"\']+)["\']',

    # PIL.Image.open(...)
    r'Image\.open\(\s*[frbuFRBU]*["\']([^"\']+)["\']',

    # plt.imread(...)
    r'plt\.imread\(\s*[frbuFRBU]*["\']([^"\']+)["\']',

    # mpimg.imread(...)
    r'mpimg\.imread\(\s*[frbuFRBU]*["\']([^"\']+)["\']',

    # display(Image(...))
    r'Image\(\s*[frbuFRBU]*["\']([^"\']+)["\']',

    # General string ending with image extension
    r'["\']([^"\']+\.(?:png|jpg|jpeg|gif|bmp|tif|tiff|webp|svg))["\']',
]

# ==========================================================
# Read notebook
# ==========================================================

with open(NOTEBOOK, encoding="utf-8") as f:
    nb = json.load(f)

referenced = set()

# ==========================================================
# Scan all cells
# ==========================================================

for cell in nb["cells"]:

    text = "".join(cell.get("source", []))

    for pattern in patterns:

        for match in re.findall(pattern, text, flags=re.IGNORECASE):

            img = match.split("?")[0]          # remove URL query
            img = img.replace("\\", "/")

            if img.lower().endswith(IMAGE_EXTENSIONS):
                referenced.add(img)

# ==========================================================
# Print referenced images
# ==========================================================

print("=" * 60)
print("Images referenced in notebook")
print("=" * 60)

for img in sorted(referenced):
    print(img)

print(f"\nTotal images referenced : {len(referenced)}")

# ==========================================================
# Check existence
# ==========================================================

missing = []

for img in sorted(referenced):

    filename = Path(img).name

    if not (IMAGE_FOLDER / filename).exists():
        missing.append(filename)

print("\n" + "=" * 60)
print("Missing images")
print("=" * 60)

if missing:

    for m in sorted(set(missing)):
        print(m)

    print(f"\nMissing: {len(set(missing))}")

else:
    print("All images are present.")