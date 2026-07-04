from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

MISSING_FILE = "missing.txt"          # Input file
SEARCH_FOLDER = "../"         # Folder to search recursively
OUTPUT_FILE = "found_images.txt"      # Output file

# ==========================================================
# Read missing image names
# ==========================================================

with open(MISSING_FILE, "r", encoding="utf-8") as f:
    missing_images = [line.strip() for line in f if line.strip()]

# Convert to a set for fast lookup
missing_set = set(missing_images)

# ==========================================================
# Search recursively
# ==========================================================

results = {}

for filepath in Path(SEARCH_FOLDER).rglob("*"):

    if filepath.is_file():

        filename = filepath.name

        if filename in missing_set:
            results.setdefault(filename, []).append(filepath.resolve())

# ==========================================================
# Write output
# ==========================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for filename in sorted(missing_images):

        if filename in results:

            for path in results[filename]:
                f.write(f"{filename}\t{path}\n")

        else:
            f.write(f"{filename}\tNOT FOUND\n")

print(f"Finished. Results written to '{OUTPUT_FILE}'.")
print(f"Found {len(results)} out of {len(missing_set)} images.")