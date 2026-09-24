#!/usr/bin/env python3
# 统计解读书净汉字数（[\u4e00-\u9fff]）
import re, sys, glob, os
paths = sys.argv[1:]
if not paths:
    paths = sorted(glob.glob('/mnt/openclaw/catdesk/home/佛法/文献档案/*_*/解讀_*.md'))
for p in paths:
    t = open(p, encoding='utf-8').read()
    n = len(re.findall(r'[\u4e00-\u9fff]', t))
    print(f"{n}\t{p}")
