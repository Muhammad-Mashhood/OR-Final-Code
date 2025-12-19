# Remove inline comments (#...) and triple-quoted string literals ('''...''' or """...""")
# Uses the tokenize module to preserve code structure while removing comments
import io, tokenize, re, sys
from pathlib import Path
p = Path(r"d:\OR Final Code\final_code.py")
src = p.read_text(encoding='utf-8')

def is_triple_quoted_string(token_str):
    # Strip possible string prefixes like r, u, f, b, R, FR, etc.
    m = re.match(r"([rubfRUBF]{,3})?(.*)$", token_str, flags=0)
    body = m.group(2) if m else token_str
    return body.startswith('"""') or body.startswith("'''")

out_tokens = []
reader = io.StringIO(src).readline
try:
    for tok in tokenize.generate_tokens(reader):
        ttype = tok.type
        tstring = tok.string
        if ttype == tokenize.COMMENT:
            # skip comments
            continue
        if ttype == tokenize.STRING and is_triple_quoted_string(tstring):
            # skip triple-quoted string tokens
            # but preserve a NEWLINE if the string token spans a line by itself
            # generate_tokens will provide NL/NEWLINE tokens separately, so nothing to add
            continue
        out_tokens.append((ttype, tstring))
except tokenize.TokenError as e:
    print('Tokenization error:', e)
    sys.exit(1)

new_src = tokenize.untokenize(out_tokens)
# Normalize excessive blank lines: collapse >2 consecutive newlines into 2
new_src = re.sub(r"\n{3,}", "\n\n", new_src)

p.write_text(new_src, encoding='utf-8')
print(f"Processed {p} — removed inline comments and triple-quoted strings.")
