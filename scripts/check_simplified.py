#!/usr/bin/env python3
"""检查是否还有简体目录名"""
import os
from opencc import OpenCC

cc = OpenCC('s2t')
archive = "/mnt/openclaw/catdesk/home/佛法/文献档案"

dirs = sorted(os.listdir(archive))
simp_count = 0
simp_samples = []
for d in dirs:
    dirpath = os.path.join(archive, d)
    if not os.path.isdir(dirpath):
        continue
    parts = d.split('_', 1)
    if len(parts) < 2:
        continue
    name = parts[1]
    trad = cc.convert(name)
    if trad != name:
        simp_count += 1
        if len(simp_samples) < 20:
            simp_samples.append((d, trad))

print(f"简体目录名数量: {simp_count}")
for old, new in simp_samples:
    print(f"  {old} → 应为: {new}")
