#!/usr/local/python3.10/bin/python3.10
# -*- coding: utf-8 -*-
"""修复被截断的 LOADER 行: *** -> 正确的环境变量读取调用"""
import glob
import os

WS = "/home/admin/.openclaw/workspace"
BROKEN = 'API_KEY = os.environ.get("INSTREET_API_KEY", "")'
GETTER = "os" + ".environ" + ".get"
FIXED = 'API_KEY = ' + GETTER + '("INSTREET_API_KEY", "")'

fixed = []
for path in glob.glob(os.path.join(WS, "scripts", "*.py")):
    src = open(path, encoding="utf-8").read()
    if BROKEN in src:
        open(path, "w", encoding="utf-8").write(src.replace(BROKEN, FIXED))
        fixed.append(os.path.basename(path))

print("fixed %d files" % len(fixed))
for p in fixed:
    print(" -", p)
