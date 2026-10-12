#!/usr/bin/env python3
"""Idempotent, Windows-friendly SDC desktop navbar dock installer."""
from pathlib import Path
import shutil
import sys

root = Path.cwd()
navbar = root / 'src/components/layout/navbar.tsx'
css = root / 'src/app/globals.css'
dest = root / 'src/components/layout/magnification-dock.tsx'
script_dir = Path(__file__).resolve().parent

for path in (navbar, css, script_dir / 'magnification-dock.tsx', script_dir / 'dock.css'):
    if not path.is_file():
        sys.exit(f'Missing {path}; run from the SDC website root with all ZIP files next to apply_dock.py.')

source = navbar.read_text(encoding='utf-8')
if 'import { MagnificationDock }' not in source:
    marker = 'import { Brand } from "@/components/layout/brand";'
    if marker not in source:
        sys.exit('Cannot find Brand import in navbar.tsx. No changes made.')
    source = source.replace(marker, marker + '\nimport { MagnificationDock } from "@/components/layout/magnification-dock";', 1)

if '<MagnificationDock links={navLinks} pathname={pathname} />' not in source:
    start = source.find('<ul className="hidden items-center gap-1 lg:flex">')
    end = source.find('</ul>', start)
    if start < 0 or end < 0:
        sys.exit('Cannot locate desktop nav list; no changes saved. Your navbar may differ from the GitHub version.')
    original_list = source[start:end + len('</ul>')]
    if 'navLinks.map' not in original_list:
        sys.exit('The matched list is not the standard desktop nav; no changes saved.')
    source = source[:start] + '<MagnificationDock links={navLinks} pathname={pathname} />' + source[end + len('</ul>'):]

# Make room above the desktop dock for its tooltip without changing mobile header height.
source = source.replace('flex h-16 w-full max-w-7xl', 'flex h-16 lg:h-28 w-full max-w-7xl', 1)

if navbar.read_text(encoding='utf-8') != source:
    backup = navbar.with_suffix('.tsx.before-dock.bak')
    if not backup.exists():
        shutil.copy2(navbar, backup)
    navbar.write_text(source, encoding='utf-8')
    print('Updated', navbar)
else:
    print('Navbar already patched')

new_component = (script_dir / 'magnification-dock.tsx').read_text(encoding='utf-8')
if not dest.exists() or dest.read_text(encoding='utf-8') != new_component:
    dest.write_text(new_component, encoding='utf-8')
    print('Created', dest)

css_source = css.read_text(encoding='utf-8')
if '.sdc-dock-link {' not in css_source:
    css.write_text(css_source.rstrip() + '\n\n' + (script_dir / 'dock.css').read_text(encoding='utf-8'), encoding='utf-8')
    print('Updated', css)
else:
    print('Dock styles already installed')
print('Dock patch complete. Run npm run lint and npm run build.')
