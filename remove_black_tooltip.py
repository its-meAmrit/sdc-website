from pathlib import Path
import re
import shutil
import sys

root = Path.cwd()
file = root / 'src/components/layout/magnification-dock.tsx'
if not file.is_file():
    sys.exit('Cannot find src/components/layout/magnification-dock.tsx. Run in the project folder.')
source = file.read_text(encoding='utf-8')
# Remove only the tooltip that is rendered above each navigation link.
pattern = r'\n\s*<span\s+role="tooltip"[\s\S]*?</span>(?=\s*</li>)'
modified, count = re.subn(pattern, '', source)
if count:
    modified = re.sub(r'\n\s*const \[hovered, setHovered\] = useState<string \| null>\(null\);', '', modified)
    modified = modified.replace('setScales([]); setHovered(null);', 'setScales([]);')
    modified = re.sub(r'\n\s*onPointerEnter=\{\(\) => setHovered\(link.href\)\}', '', modified)
    modified = re.sub(r'\n\s*onPointerLeave=\{\(\) => setHovered\(null\)\}', '', modified)
    modified = re.sub(r'\n\s*onFocus=\{\(\) => setHovered\(link.href\)\}', '', modified)
    modified = re.sub(r'\n\s*onBlur=\{\(\) => setHovered\(null\)\}', '', modified)
    backup = file.with_name(file.name + '.before-tooltip-removal.bak')
    if not backup.exists():
        shutil.copy2(file, backup)
    file.write_text(modified, encoding='utf-8')
    print(f'Removed {count} tooltip element(s) from {file}.')
elif 'role="tooltip"' not in source:
    print('No tooltip found; patch already applied.')
else:
    sys.exit('Tooltip structure differs from expected; no edits made. Share your magnification-dock.tsx file.')
print('Run npm run lint and npm run build to verify.')
