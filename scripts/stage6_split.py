#!/usr/bin/env python3
"""阶段六：002-009+001+010-031文献拆分为独立子目录

将平铺的多文献三件套拆分为独立子目录：
  {文献名}_原文.md       → {文献名}/原文.md
  {文献名}_解读_学术.md   → {文献名}/解讀_學術.md
  {文献名}_解读_白话.md   → {文献名}/解讀_白話.md
  {文献名}_解讀_學術.md   → {文献名}/解讀_學術.md  (繁体变体)
  {文献名}_解讀_白話.md   → {文献名}/解讀_白話.md  (繁体变体)

处理范围：
  - 001_口传法藏/01-08子目录内文献拆分
  - 002-031期目录内文献拆分

保留在期目录顶层的文件：README.md, 索引卡.md, 解讀_學術.md, 解讀_白話.md,
  {期编号}_{期名}.md, {期名}.xlsx, 以及其他非三件套文件
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(BASE, "文献档案")

# 三件套后缀（按长度降序排列，避免短后缀误匹配）
SUFFIXES = [
    ("_解读_学术.md", "解讀_學術.md"),
    ("_解读_白话.md", "解讀_白話.md"),
    ("_解讀_學術.md", "解讀_學術.md"),
    ("_解讀_白話.md", "解讀_白話.md"),
    ("_原文.md", "原文.md"),
]

# 顶层保留文件名（不参与拆分）
KEEP_FILES = {"README.md", "索引卡.md", "解讀_學術.md", "解讀_白話.md"}

stats = {
    "dirs_created": 0,
    "files_moved": 0,
    "skipped": 0,
    "errors": 0,
}
errors = []


def extract_lit_name(filename):
    """从文件名中提取文献名和目标文件名
    
    返回 (文献名, 目标文件名) 或 None
    """
    for suffix, target in SUFFIXES:
        if filename.endswith(suffix):
            lit_name = filename[:-len(suffix)]
            if lit_name:  # 确保文献名非空
                return (lit_name, target)
    return None


def process_directory(dirpath):
    """处理一个目录，将三件套文件拆分为子目录
    
    返回创建的子目录数
    """
    try:
        files = os.listdir(dirpath)
    except OSError as e:
        errors.append(f"无法读取 {dirpath}: {e}")
        stats["errors"] += 1
        return 0
    
    # 按文献名分组文件
    lit_files = {}  # {文献名: {目标文件名: 源文件路径}}
    
    for f in files:
        fpath = os.path.join(dirpath, f)
        if not os.path.isfile(fpath):
            continue
        
        # 跳过保留文件
        if f in KEEP_FILES:
            continue
        
        # 跳过备份和根目录版文件
        if f.endswith("_根目录版.md") or f.endswith("_备份.md"):
            continue
        
        result = extract_lit_name(f)
        if result:
            lit_name, target_name = result
            if lit_name not in lit_files:
                lit_files[lit_name] = {}
            lit_files[lit_name][target_name] = fpath
    
    # 为每个文献创建子目录并移动文件
    created = 0
    for lit_name, file_map in lit_files.items():
        lit_dir = os.path.join(dirpath, lit_name)
        
        # 如果目录已存在（可能是之前运行过），不重复创建
        if os.path.exists(lit_dir):
            stats["skipped"] += 1
            # 但仍然尝试移动文件
        else:
            try:
                os.makedirs(lit_dir, exist_ok=True)
                created += 1
                stats["dirs_created"] += 1
            except OSError as e:
                errors.append(f"创建目录失败 {lit_dir}: {e}")
                stats["errors"] += 1
                continue
        
        # 移动文件
        for target_name, src_path in file_map.items():
            dst_path = os.path.join(lit_dir, target_name)
            if os.path.exists(dst_path):
                # 目标已存在，跳过（可能是之前运行过）
                stats["skipped"] += 1
                continue
            try:
                os.rename(src_path, dst_path)
                stats["files_moved"] += 1
            except OSError as e:
                errors.append(f"移动文件失败 {src_path} → {dst_path}: {e}")
                stats["errors"] += 1
    
    return created


def main():
    if not os.path.isdir(ARCHIVE):
        print(f"错误：{ARCHIVE} 不存在")
        sys.exit(1)
    
    # 1. 处理001期子目录
    print("=== 处理001期子目录 ===")
    dir_001 = os.path.join(ARCHIVE, "001_口传法藏")
    if os.path.isdir(dir_001):
        subdirs = sorted([d for d in os.listdir(dir_001) if os.path.isdir(os.path.join(dir_001, d))])
        for sd in subdirs:
            sd_path = os.path.join(dir_001, sd)
            created = process_directory(sd_path)
            print(f"  {sd}: 创建 {created} 个文献目录")
    
    # 2. 处理002-031期
    print("\n=== 处理002-031期 ===")
    all_entries = sorted(os.listdir(ARCHIVE))
    for entry in all_entries:
        dirpath = os.path.join(ARCHIVE, entry)
        if not os.path.isdir(dirpath):
            continue
        # 匹配 002-031
        if entry.startswith("0") and len(entry) >= 3:
            num_part = entry[:3]
            if num_part.isdigit() and 2 <= int(num_part) <= 31:
                created = process_directory(dirpath)
                print(f"  {entry}: 创建 {created} 个文献目录")
    
    print(f"\n=== 统计 ===")
    print(f"创建文献目录: {stats['dirs_created']}")
    print(f"移动文件: {stats['files_moved']}")
    print(f"跳过(已存在): {stats['skipped']}")
    print(f"错误: {stats['errors']}")
    
    if errors:
        print(f"\n=== 错误详情 (前20条) ===")
        for e in errors[:20]:
            print(f"  {e}")


if __name__ == "__main__":
    main()
