# Replace all Unicode special characters with ASCII equivalents
from pathlib import Path

p = Path(r"d:\OR Final Code\final_code.py")
text = p.read_text(encoding='utf-8')

# Replace Unicode characters with ASCII equivalents
replacements = {
    '─': '-',  # Box drawing horizontal
    '│': '|',  # Box drawing vertical
    '└': '+',  # Box drawing corner
    '├': '+',  # Box drawing T
    '→': '->',  # Right arrow
    '✓': 'OK',  # Check mark
    '✗': 'X',   # X mark
    '∞': 'INF',  # Infinity
    '×': 'x',   # Multiplication sign
    '\u00a0': ' ',  # Non-breaking space to regular space
}

for unicode_char, ascii_char in replacements.items():
    text = text.replace(unicode_char, ascii_char)

p.write_text(text, encoding='utf-8')
print(f"Replaced Unicode characters in {p}")
print("Replacements made:")
for u, a in replacements.items():
    print(f"  '{u}' -> '{a}'")
