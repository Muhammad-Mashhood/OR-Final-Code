# Script to remove full-line # comments from final_code.py
from pathlib import Path
p = Path(r"d:\OR Final Code\final_code.py")
text = p.read_text(encoding='utf-8')
lines = text.splitlines(keepends=True)
new_lines = [ln for ln in lines if not ln.lstrip().startswith('#')]
p.write_text(''.join(new_lines), encoding='utf-8')
print(f"Processed {p} — removed {len(lines)-len(new_lines)} full-line comments.")
