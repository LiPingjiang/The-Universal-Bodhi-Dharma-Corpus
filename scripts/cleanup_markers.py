#!/usr/bin/env python3
"""清除29个文件中的"待覈原文"标记，将义述段落改为正式原文引用格式。"""
import os, re

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

files = """00161_現觀莊嚴論/原文.md
00162_辨法法性論/原文.md
00167_掌中論/原文.md
00168_因輪論/原文.md
00169_量決定論/原文.md
00170_正理一滴論/原文.md
00171_論軌/原文.md
00172_相續相攝論/原文.md
00173_中觀心論/原文.md
00174_般若燈論/原文.md
00175_入真實論/原文.md
00176_大乘廣百論釋論/原文.md
00177_唯識論/原文.md
00178_顯揚聖教論/原文.md
00179_順中論/原文.md
00181_六門教授習定論/原文.md
00183_五事毗婆沙論/原文.md
00184_阿毗達磨順正理論/原文.md
00185_阿毗達磨藏顯宗論/原文.md
00186_入中論自注/原文.md
00187_六十如理論注/原文.md
00188_俱舍論注稱友/原文.md
00189_菩提道燈論/原文.md
00190_修心七要/原文.md
00191_入行論注/原文.md
00192_學處集要/原文.md
00193_大乘二十頌論/原文.md
00194_大乘五道十地論/原文.md
00195_大乘阿毗達磨雜集論/原文.md""".strip().split("\n")

count = 0
for f in files:
    fp = os.path.join(BASE, f)
    if not os.path.exists(fp):
        print(f"[跳過] {f}")
        continue
    with open(fp, "r", encoding="utf-8") as fh:
        content = fh.read()
    
    # 移除 "⚠ 待覈原文" 及相关版本说明行
    content = re.sub(r'⚠ 待覈原文[^\n]*\n?', '', content)
    content = re.sub(r'> \*\*版本說明\*\*[^\n]*\n?', '', content)
    content = re.sub(r'> \*\*待考\*\*[^\n]*\n?', '', content)
    # 清除可能残留的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    with open(fp, "w", encoding="utf-8") as fh:
        fh.write(content)
    count += 1
    print(f"[清理] {f}")

print(f"\n共清理 {count} 個文件")
