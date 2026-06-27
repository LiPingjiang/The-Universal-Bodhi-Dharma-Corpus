#!/usr/bin/env python3
"""阶段五：X期文件名统一+重复文件标记备份

处理规则：
  1. {文献名}_原文.md + 已有 原文.md → 原文_备份.md（重复标记）
  2. {文献名}_原文.md + 无 原文.md  → 原文.md（直接重命名）
  3. {文献名}_解讀_學術.md + 已有 解讀_學術.md → 解讀_學術_备份.md
  4. {文献名}_解讀_學術.md + 无 解讀_學術.md  → 解讀_學術.md
  5. 同理处理 _解讀_白話.md / _解读_学术.md / _解读_白话.md

仅处理 X期（X01-X28125），不处理 XB期（已全部为繁体裸名）。
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(BASE, "文献档案")

stats = {
    "yuanwen_rename": 0,       # 前缀→原文.md
    "yuanwen_backup": 0,       # 前缀→原文_备份.md
    "xueshu_rename": 0,        # 前缀→解讀_學術.md
    "xueshu_backup": 0,        # 前缀→解讀_學術_备份.md
    "baihua_rename": 0,        # 前缀→解讀_白話.md
    "baihua_backup": 0,        # 前缀→解讀_白話_备份.md
    "xueshu_simp_rename": 0,   # 简体前缀→解讀_學術.md
    "baihua_simp_rename": 0,   # 简体前缀→解讀_白話.md
    "dirs_scanned": 0,
    "errors": 0,
}
errors = []


def process_dir(dirpath):
    """处理单个X期目录"""
    stats["dirs_scanned"] += 1
    
    try:
        files = os.listdir(dirpath)
    except OSError as e:
        errors.append(f"无法读取 {dirpath}: {e}")
        stats["errors"] += 1
        return
    
    # 检查已有文件
    has_yuanwen = "原文.md" in files
    has_xueshu = "解讀_學術.md" in files
    has_baihua = "解讀_白話.md" in files
    
    # 分类带前缀文件
    for f in files:
        fpath = os.path.join(dirpath, f)
        if not os.path.isfile(fpath):
            continue
        
        # 跳过裸名文件和已有备份/根目录版
        if f in ("原文.md", "解讀_學術.md", "解讀_白話.md", "索引卡.md", "README.md"):
            continue
        if f.endswith("_根目录版.md") or f.endswith("_备份.md"):
            continue
        
        # 处理 _原文.md
        if f.endswith("_原文.md"):
            if has_yuanwen:
                # 重复，标记为备份
                dst = os.path.join(dirpath, "原文_备份.md")
                if os.path.exists(dst):
                    # 如果已有备份，加数字后缀
                    i = 2
                    while os.path.exists(os.path.join(dirpath, f"原文_备份{i}.md")):
                        i += 1
                    dst = os.path.join(dirpath, f"原文_备份{i}.md")
                try:
                    os.rename(fpath, dst)
                    stats["yuanwen_backup"] += 1
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
            else:
                # 无冲突，直接重命名
                dst = os.path.join(dirpath, "原文.md")
                try:
                    os.rename(fpath, dst)
                    stats["yuanwen_rename"] += 1
                    has_yuanwen = True
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
        
        # 处理 _解讀_學術.md（繁体前缀）
        elif f.endswith("_解讀_學術.md"):
            if has_xueshu:
                dst = os.path.join(dirpath, "解讀_學術_备份.md")
                if os.path.exists(dst):
                    i = 2
                    while os.path.exists(os.path.join(dirpath, f"解讀_學術_备份{i}.md")):
                        i += 1
                    dst = os.path.join(dirpath, f"解讀_學術_备份{i}.md")
                try:
                    os.rename(fpath, dst)
                    stats["xueshu_backup"] += 1
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
            else:
                dst = os.path.join(dirpath, "解讀_學術.md")
                try:
                    os.rename(fpath, dst)
                    stats["xueshu_rename"] += 1
                    has_xueshu = True
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
        
        # 处理 _解读_学术.md（简体前缀）
        elif f.endswith("_解读_学术.md"):
            if has_xueshu:
                dst = os.path.join(dirpath, "解讀_學術_备份.md")
                if os.path.exists(dst):
                    i = 2
                    while os.path.exists(os.path.join(dirpath, f"解讀_學術_备份{i}.md")):
                        i += 1
                    dst = os.path.join(dirpath, f"解讀_學術_备份{i}.md")
                try:
                    os.rename(fpath, dst)
                    stats["xueshu_backup"] += 1
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
            else:
                dst = os.path.join(dirpath, "解讀_學術.md")
                try:
                    os.rename(fpath, dst)
                    stats["xueshu_simp_rename"] += 1
                    has_xueshu = True
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
        
        # 处理 _解讀_白話.md（繁体前缀）
        elif f.endswith("_解讀_白話.md"):
            if has_baihua:
                dst = os.path.join(dirpath, "解讀_白話_备份.md")
                if os.path.exists(dst):
                    i = 2
                    while os.path.exists(os.path.join(dirpath, f"解讀_白話_备份{i}.md")):
                        i += 1
                    dst = os.path.join(dirpath, f"解讀_白話_备份{i}.md")
                try:
                    os.rename(fpath, dst)
                    stats["baihua_backup"] += 1
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
            else:
                dst = os.path.join(dirpath, "解讀_白話.md")
                try:
                    os.rename(fpath, dst)
                    stats["baihua_rename"] += 1
                    has_baihua = True
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
        
        # 处理 _解读_白话.md（简体前缀）
        elif f.endswith("_解读_白话.md"):
            if has_baihua:
                dst = os.path.join(dirpath, "解讀_白話_备份.md")
                if os.path.exists(dst):
                    i = 2
                    while os.path.exists(os.path.join(dirpath, f"解讀_白話_备份{i}.md")):
                        i += 1
                    dst = os.path.join(dirpath, f"解讀_白話_备份{i}.md")
                try:
                    os.rename(fpath, dst)
                    stats["baihua_backup"] += 1
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1
            else:
                dst = os.path.join(dirpath, "解讀_白話.md")
                try:
                    os.rename(fpath, dst)
                    stats["baihua_simp_rename"] += 1
                    has_baihua = True
                except OSError as e:
                    errors.append(f"重命名失败 {fpath}: {e}")
                    stats["errors"] += 1


def main():
    if not os.path.isdir(ARCHIVE):
        print(f"错误：{ARCHIVE} 不存在")
        sys.exit(1)
    
    all_entries = sorted(os.listdir(ARCHIVE))
    
    x_dirs = []
    for entry in all_entries:
        dirpath = os.path.join(ARCHIVE, entry)
        if not os.path.isdir(dirpath):
            continue
        # 匹配 X期：以X开头后跟数字，排除XB期
        if entry.startswith("X") and not entry.startswith("XB"):
            if len(entry) > 1 and entry[1].isdigit():
                x_dirs.append(dirpath)
    
    print(f"X期目录数: {len(x_dirs)}")
    
    for i, dirpath in enumerate(x_dirs):
        process_dir(dirpath)
        if (i + 1) % 5000 == 0:
            print(f"  进度: {i+1}/{len(x_dirs)}...")
    
    print(f"\n=== 统计 ===")
    print(f"扫描目录: {stats['dirs_scanned']}")
    print(f"原文 → 原文.md (直接重命名): {stats['yuanwen_rename']}")
    print(f"原文 → 原文_备份.md (重复标记): {stats['yuanwen_backup']}")
    print(f"解讀_學術 → 解讀_學術.md (直接重命名): {stats['xueshu_rename']}")
    print(f"解讀_學術 → 解讀_學術_备份.md (重复标记): {stats['xueshu_backup']}")
    print(f"解读_学术(简体) → 解讀_學術.md: {stats['xueshu_simp_rename']}")
    print(f"解讀_白話 → 解讀_白話.md (直接重命名): {stats['baihua_rename']}")
    print(f"解讀_白話 → 解讀_白話_备份.md (重复标记): {stats['baihua_backup']}")
    print(f"解读_白话(简体) → 解讀_白話.md: {stats['baihua_simp_rename']}")
    print(f"错误: {stats['errors']}")
    
    total = sum(v for k, v in stats.items() if k not in ("dirs_scanned", "errors"))
    print(f"总重命名文件数: {total}")
    
    if errors:
        print(f"\n=== 错误详情 (前20条) ===")
        for e in errors[:20]:
            print(f"  {e}")


if __name__ == "__main__":
    main()
