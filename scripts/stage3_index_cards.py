#!/usr/bin/env python3
"""阶段三：剩余散落md索引卡归位
将 文献档案/{编号}_{名称}.md 移入对应文献目录，重命名为 索引卡.md
"""
import os
import shutil

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 收集所有散落的md文件（非目录内）
loose_md = []
for entry in os.listdir(BASE):
    filepath = os.path.join(BASE, entry)
    if os.path.isfile(filepath) and entry.endswith(".md"):
        loose_md.append(entry)

print(f"散落md总数: {len(loose_md)}")

moved = 0
not_found = 0
already_has = 0

for md_file in sorted(loose_md):
    # 提取编号前缀（如 X01, I06, 001, III05 等）
    # 格式: {编号}_{名称}.md
    base_name = md_file[:-3]  # 去掉.md
    
    # 尝试匹配目录：以相同编号开头
    # 编号格式：001-009, I01-I99, II01-II99, ..., X01-X28125
    # 用下划线分割第一部分作为编号
    parts = base_name.split("_", 1)
    if len(parts) < 2:
        not_found += 1
        continue
    
    prefix = parts[0]  # 如 X01, I06, 001
    
    # 查找以该编号开头的目录
    matched_dirs = []
    for d in os.listdir(BASE):
        dpath = os.path.join(BASE, d)
        if os.path.isdir(dpath) and d.startswith(prefix + "_"):
            matched_dirs.append(d)
    
    if not matched_dirs:
        not_found += 1
        continue
    elif len(matched_dirs) == 1:
        target_dir = matched_dirs[0]
    else:
        # 多个匹配，选名称最接近的
        md_name = parts[1] if len(parts) > 1 else ""
        best_match = None
        best_score = -1
        for d in matched_dirs:
            d_name = d[len(prefix)+1:]  # 去掉编号_
            # 计算相似度（共同字符数）
            score = len(set(md_name) & set(d_name))
            if score > best_score:
                best_score = score
                best_match = d
        target_dir = best_match
    
    target_path = os.path.join(BASE, target_dir, "索引卡.md")
    src_path = os.path.join(BASE, md_file)
    
    if os.path.exists(target_path):
        # 已有索引卡，用原文件名保留
        target_path = os.path.join(BASE, target_dir, md_file)
        if os.path.exists(target_path):
            # 连原文件名都冲突了，加后缀
            target_path = os.path.join(BASE, target_dir, base_name + "_索引卡.md")
        already_has += 1
    
    shutil.move(src_path, target_path)
    moved += 1

print(f"移入索引卡: {moved}")
print(f"  其中目录已有索引卡(保留原名): {already_has}")
print(f"未找到对应目录: {not_found}")

# 列出未找到的
if not_found > 0:
    print("\n未匹配的散落md:")
    for md_file in sorted(loose_md):
        base_name = md_file[:-3]
        parts = base_name.split("_", 1)
        if len(parts) < 2:
            print(f"  {md_file}")
            continue
        prefix = parts[0]
        matched = any(d.startswith(prefix + "_") for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d)))
        if not matched:
            print(f"  {md_file}")
