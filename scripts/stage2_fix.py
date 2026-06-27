#!/usr/bin/env python3
"""阶段二修复：扫描实际散落文件，动态创建XB目录"""
import os
import re
import shutil

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 扫描所有 X{num}_{name}_原文.md 格式的散落文件
pattern = re.compile(r'^(X\d+)_(.+?)_原文\.md$')
pattern2 = re.compile(r'^(X\d+)_(.+?)_解讀_學術\.md$')
pattern3 = re.compile(r'^(X\d+)_(.+?)_解讀_白話\.md$')

# 收集所有繁体前缀散落文件
files_a = {}  # {X编号: {文献名: {原文, 学术, 白话}}}

for entry in os.listdir(BASE):
    filepath = os.path.join(BASE, entry)
    if not os.path.isfile(filepath):
        continue
    
    for pat, key in [(pattern, "原文"), (pattern2, "學術"), (pattern3, "白話")]:
        m = pat.match(entry)
        if m:
            xid = m.group(1)
            name = m.group(2)
            if xid not in files_a:
                files_a[xid] = {}
            if name not in files_a[xid]:
                files_a[xid][name] = {}
            files_a[xid][name][key] = entry
            break

# 也查找对应的简体裸名索引卡（文献B的）
# 格式: X{num}_{name_b}.md (没有_原文/解讀后缀)
all_x_md = set()
for entry in os.listdir(BASE):
    if entry.startswith("X") and entry.endswith(".md"):
        filepath = os.path.join(BASE, entry)
        if os.path.isfile(filepath):
            # 排除已知的三件套文件
            if "_原文.md" in entry or "_解讀_學術.md" in entry or "_解讀_白話.md" in entry:
                continue
            all_x_md.add(entry)

count_a = 0
count_b = 0
errors = []

# 处理文献A
# 按X编号排序
sorted_xids = sorted(files_a.keys(), key=lambda x: int(x[1:]))
xb_num = 1

for xid in sorted_xids:
    for name_a, files in files_a[xid].items():
        xb_id = f"XB{xb_num:02d}"
        xb_dir = os.path.join(BASE, f"{xb_id}_{name_a}")
        os.makedirs(xb_dir, exist_ok=True)
        
        for key, std_name in [("原文", "原文.md"), ("學術", "解讀_學術.md"), ("白話", "解讀_白話.md")]:
            if key in files:
                src = os.path.join(BASE, files[key])
                dst = os.path.join(xb_dir, std_name)
                if os.path.exists(dst):
                    dst = os.path.join(xb_dir, files[key])  # 保留原名
                shutil.move(src, dst)
                count_a += 1
        
        # 同时查找对应的简体索引卡
        # 索引卡格式: X{num}_{name_b}.md
        xnum = xid[1:]
        for md_file in list(all_x_md):
            if md_file.startswith(f"X{xnum}_"):
                # 这是文献B的索引卡
                # 找到文献B的目录
                b_name = md_file[len(f"X{xnum}_"):-3]  # 去掉X{num}_前缀和.md后缀
                b_dirs = [d for d in os.listdir(BASE) if d.startswith(f"X{xnum}_") and os.path.isdir(os.path.join(BASE, d)) and b_name in d]
                if b_dirs:
                    b_dir = os.path.join(BASE, b_dirs[0])
                    b_dst = os.path.join(b_dir, "索引卡.md")
                    if os.path.exists(b_dst):
                        b_dst = os.path.join(b_dir, md_file.replace(".md", "_索引卡.md"))
                    shutil.move(os.path.join(BASE, md_file), b_dst)
                    all_x_md.remove(md_file)
                    count_b += 1
        
        xb_num += 1

print(f"文献A: 移动 {count_a} 个文件到XB目录 (共{xb_num-1}个XB目录)")
print(f"文献B: 移动 {count_b} 个索引卡到已有目录")

# 检查剩余散落md
if all_x_md:
    print(f"\n剩余散落md ({len(all_x_md)}):")
    for f in sorted(all_x_md)[:20]:
        print(f"  {f}")
