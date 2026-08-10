#!/usr/bin/env python3
"""修复7个文件的旧编号链接，替换为正确的新编号和相关文献。"""
import os

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 00049_法集論注：I编号 -> 新编号
fix_49 = {
    "I01_法集論": "29762_法集論",
    "I02_分別論": "29763_分別論",
    "I03_清淨道論": "00138_清淨道論",
    "I04_界論": "00068_界論",
}

# 律藏文件00050-00055：错误的论藏链接 -> 正确的律藏链接
old_law_links = """- [I17_巴利論藏七論](I17_巴利論藏七論.md) — 上座部阿毗達磨核心
- [I20_大毗婆沙論](I20_大毗婆沙論.md) — 阿毗達磨百科全書"""

# 根据每个律藏文件定制相关文献
law_links = {
    "00050_四分律": """- [巴利律藏](00005_巴利律藏/原文.md) — 上座部律藏根本
- [四分律行事鈔](00266_四分律行事鈔/原文.md) — 道宣律師四分律疏
- [十誦律](00052_十誦律/原文.md) — 說一切有部律典
- [摩訶僧祇律](00053_摩訶僧祇律/原文.md) — 大眾部律典""",
    "00051_五分律": """- [巴利律藏](00005_巴利律藏/原文.md) — 上座部律藏根本
- [四分律](00050_四分律/原文.md) — 法藏部律典
- [十誦律](00052_十誦律/原文.md) — 說一切有部律典
- [摩訶僧祇律](00053_摩訶僧祇律/原文.md) — 大眾部律典""",
    "00052_十誦律": """- [巴利律藏](00005_巴利律藏/原文.md) — 上座部律藏根本
- [四分律](00050_四分律/原文.md) — 法藏部律典
- [根本說一切有部律](00054_根本說一切有部律/原文.md) — 有部律根本
- [摩訶僧祇律](00053_摩訶僧祇律/原文.md) — 大眾部律典""",
    "00053_摩訶僧祇律": """- [巴利律藏](00005_巴利律藏/原文.md) — 上座部律藏根本
- [四分律](00050_四分律/原文.md) — 法藏部律典
- [十誦律](00052_十誦律/原文.md) — 說一切有部律典
- [五分律](00051_五分律/原文.md) — 化地部律典""",
    "00054_根本說一切有部律": """- [巴利律藏](00005_巴利律藏/原文.md) — 上座部律藏根本
- [十誦律](00052_十誦律/原文.md) — 說一切有部律典舊譯
- [四分律](00050_四分律/原文.md) — 法藏部律典
- [摩訶僧祇律](00053_摩訶僧祇律/原文.md) — 大眾部律典""",
    "00055_巴利律藏大品與小品": """- [巴利律藏](00005_巴利律藏/原文.md) — 巴利律藏全文
- [四分律](00050_四分律/原文.md) — 法藏部律典
- [清淨道論](00138_清淨道論/原文.md) — 戒定慧三學修學次第
- [攝阿毗達磨義論](00069_攝阿毗達磨義論/原文.md) — 上座部阿毗達磨綱要""",
}

count = 0

# 修复00049
fp = os.path.join(BASE, "00049_法集論注", "原文.md")
if os.path.exists(fp):
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in fix_49.items():
        old_name = old.split("_", 1)[1]
        new_num = new.split("_", 1)[0]
        new_name = new.split("_", 1)[1]
        content = content.replace(
            f"[{old.split('_',1)[0]} · {old_name}]({old}.md)",
            f"[{new_num}_{new_name}]({new}/原文.md)"
        )
        # Also handle plain format
        content = content.replace(
            f"[{old}]({old}.md)",
            f"[{new}]({new}/原文.md)"
        )
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
    print(f"[修复] 00049_法集論注")

# 修复00050-00055
for dirname, new_links in law_links.items():
    fp = os.path.join(BASE, dirname, "原文.md")
    if not os.path.exists(fp):
        print(f"[跳過] {dirname} 不存在")
        continue
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(old_law_links, new_links)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
    print(f"[修复] {dirname}")

print(f"\n共修复 {count} 个文件")
