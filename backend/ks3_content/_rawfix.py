"""Make every "..." literal that contains a backslash a raw string, in the given content files."""
import re
import sys

pat = re.compile(r'(?<![rR\w])"((?:[^"\\\n]|\\.)*\\(?:[^"\\\n]|\\.)*)"')
for path in sys.argv[1:]:
    src = open(path, encoding="utf-8").read()
    out, n = pat.subn(lambda m: 'r"' + m.group(1) + '"', src)
    open(path, "w", encoding="utf-8").write(out)
    print(f"{path}: {n} strings made raw")
