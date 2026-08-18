#!/usr/local/python3.10/bin/python3.10
# -*- coding: utf-8 -*-
"""从 .env.instreet 读取 key，批量替换 scripts/*.py 中硬编码的 instreet API_KEY"""
import os
import re
import glob

WS = "/home/admin/.openclaw/workspace"

KEY = ""
env_path = os.path.join(WS, ".env.instreet")
with open(env_path, encoding="utf-8") as f:
    for line in f:
        if line.startswith("INSTREET_API_KEY="):
            KEY = line[17:].strip()

if len(KEY) < 20:
    raise SystemExit("key not loaded, abort")

LOADER = (
    'API_KEY = os.environ.get("INSTREET_API_KEY", "")\n'
    "if not API_KEY:\n"
    "    try:\n"
    '        _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env.instreet")\n'
    "        with open(_env_path) as _f:\n"
    "            for _line in _f:\n"
    '                if _line.startswith("INSTREET_API_KEY="):\n'
    '                    API_KEY = _line[17:].strip()\n'
    "    except Exception:\n"
    "        pass"
)

pat = re.compile(r"""API_KEY\s*=\s*['"]sk_inst_[0-9a-f]+['"]""")

patched = []
for path in glob.glob(os.path.join(WS, "scripts", "*.py")):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if KEY not in src:
        continue
    new = pat.sub(LOADER, src)
    if "import os" not in new:
        new = re.sub(r"^(import\s+\w+)", "import os\n\\1", new, count=1, flags=re.M)
    if new != src:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        patched.append(os.path.basename(path))

print("patched %d files" % len(patched))
for p in patched:
    print(" -", p)
