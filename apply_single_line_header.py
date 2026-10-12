#!/usr/bin/env python3
"""Update previously installed SDC magnification dock to one horizontal row."""
from pathlib import Path
import shutil
import sys

root = Path.cwd()
assets = Path(__file__).resolve().parent
navbar = root / "src/components/layout/navbar.tsx"
dock = root / "src/components/layout/magnification-dock.tsx"
css_file = root / "src/app/globals.css"

for path in (navbar, dock, css_file, assets / "magnification-dock.tsx", assets / "dock.css"):
    if not path.is_file():
        sys.exit(f"Missing file: {path}. Run from your website root after installing the dock patch.")

navbar_text = navbar.read_text(encoding="utf-8")
if "<MagnificationDock links={navLinks} pathname={pathname} />" not in navbar_text:
    sys.exit("Existing dock not found in navbar.tsx. No files were changed.")

# Existing Brand component already renders full Student Development Council name
# and IISER Bhopal subtitle. Preserve it and the auth/theme controls unchanged.
updated_nav = navbar_text
for tall in ("flex h-16 lg:h-28 w-full max-w-7xl", "flex h-16 lg:h-20 w-full max-w-7xl"):
    updated_nav = updated_nav.replace(tall, "flex h-16 lg:h-20 w-full max-w-7xl")

new_dock = (assets / "magnification-dock.tsx").read_text(encoding="utf-8")
new_css = (assets / "dock.css").read_text(encoding="utf-8")
old_css = css_file.read_text(encoding="utf-8")
marker = "/* SDC header magnification dock"
if marker in old_css:
    css_updated = old_css[:old_css.index(marker)].rstrip() + "\n\n" + new_css
else:
    css_updated = old_css.rstrip() + "\n\n" + new_css

for path, new_content in ((navbar, updated_nav), (dock, new_dock), (css_file, css_updated)):
    previous = path.read_text(encoding="utf-8")
    if previous == new_content:
        print("Already updated:", path.relative_to(root))
        continue
    backup = path.with_name(path.name + ".before-single-line.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(new_content, encoding="utf-8")
    print("Updated:", path.relative_to(root))

print("Finished. Run npm run lint, npm run build, and npm run dev.")
