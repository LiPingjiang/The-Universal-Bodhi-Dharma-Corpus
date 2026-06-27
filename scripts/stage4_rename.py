#!/usr/bin/env python3
"""阶段四：I-IX期文件名统一为繁体裸名

重命名规则：
  {文献名}_原文.md        → 原文.md
  {文献名}_解读_学术.md    → 解讀_學術.md
  {文献名}_解读_白话.md    → 解讀_白話.md
  解读_学术.md             → 解讀_學術.md        (已裸名但简体)
  解读_白话.md             → 解讀_白話.md        (已裸名但简体)
  解读_学术_根目录版.md    → 解讀_學術_根目录版.md
  解读_白话_根目录版.md    → 解讀_白話_根目录版.md

不动的文件：原文.md, 原文_根目录版.md, README.md, 索引卡.md, VII06_*.md 等
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(BASE, "文献档案")

# 期数前缀
PERIODS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

# 统计
stats = {
    "prefixed_yuanwen": 0,      # {name}_原文.md → 原文.md
    "prefixed_xueshu": 0,       # {name}_解读_学术.md → 解讀_學術.md
    "prefixed_baihua": 0,       # {name}_解读_白话.md → 解讀_白話.md
    "bare_xueshu": 0,           # 解读_学术.md → 解讀_學術.md
    "bare_baihua": 0,           # 解读_白话.md → 解讀_白話.md
    "root_xueshu": 0,           # 解读_学术_根目录版.md → 解讀_學術_根目录版.md
    "root_baihua": 0,           # 解读_白话_根目录版.md → 解讀_白話_根目录版.md
    "conflicts": 0,
    "dirs_scanned": 0,
}
conflicts = []
errors = []


def is_period_dir(dirname, period):
    """检查目录名是否属于该期数"""
    return dirname.startswith(period + "_") or dirname.startswith(period + "0") or \
           dirname.startswith(period + "1") or dirname.startswith(period + "2") or \
           dirname.startswith(period + "3") or dirname.startswith(period + "4") or \
           dirname.startswith(period + "5") or dirname.startswith(period + "6") or \
           dirname.startswith(period + "7") or dirname.startswith(period + "8") or \
           dirname.startswith(period + "9")


def process_dir(dirpath):
    """处理单个目录的文件重命名"""
    stats["dirs_scanned"] += 1
    
    try:
        files = os.listdir(dirpath)
    except OSError as e:
        errors.append(f"无法读取目录 {dirpath}: {e}")
        return
    
    # 分类文件
    prefixed_yuanwen = []    # {name}_原文.md
    prefixed_xueshu = []     # {name}_解读_学术.md
    prefixed_baihua = []     # {name}_解读_白话.md
    bare_xueshu = False      # 解读_学术.md
    bare_baihua = False      # 解读_白话.md
    root_xueshu = False      # 解读_学术_根目录版.md
    root_baihua = False      # 解读_白话_根目录版.md
    has_yuanwen = False      # 原文.md 已存在
    has_xueshu_trad = False  # 解讀_學術.md 已存在
    has_baihua_trad = False  # 解讀_白話.md 已存在
    
    for f in files:
        fpath = os.path.join(dirpath, f)
        if not os.path.isfile(fpath):
            continue
        
        if f == "原文.md":
            has_yuanwen = True
        elif f == "解讀_學術.md":
            has_xueshu_trad = True
        elif f == "解讀_白話.md":
            has_baihua_trad = True
        elif f == "解读_学术.md":
            bare_xueshu = True
        elif f == "解读_白话.md":
            bare_baihua = True
        elif f == "解读_学术_根目录版.md":
            root_xueshu = True
        elif f == "解读_白话_根目录版.md":
            root_baihua = True
        elif f.endswith("_原文.md") and not f.endswith("_根目录版.md"):
            prefixed_yuanwen.append(f)
        elif f.endswith("_解读_学术.md") and not f.endswith("_根目录版.md"):
            prefixed_xueshu.append(f)
        elif f.endswith("_解读_白话.md") and not f.endswith("_根目录版.md"):
            prefixed_baihua.append(f)
    
    # 1. 先处理裸名简体→繁体（因为这些文件已经存在，不会与带前缀的重命名冲突）
    if bare_xueshu and not has_xueshu_trad:
        src = os.path.join(dirpath, "解读_学术.md")
        dst = os.path.join(dirpath, "解讀_學術.md")
        try:
            os.rename(src, dst)
            stats["bare_xueshu"] += 1
            has_xueshu_trad = True
        except OSError as e:
            errors.append(f"重命名失败 {src} → {dst}: {e}")
    
    if bare_baihua and not has_baihua_trad:
        src = os.path.join(dirpath, "解读_白话.md")
        dst = os.path.join(dirpath, "解讀_白話.md")
        try:
            os.rename(src, dst)
            stats["bare_baihua"] += 1
            has_baihua_trad = True
        except OSError as e:
            errors.append(f"重命名失败 {src} → {dst}: {e}")
    
    if root_xueshu:
        src = os.path.join(dirpath, "解读_学术_根目录版.md")
        dst = os.path.join(dirpath, "解讀_學術_根目录版.md")
        if not os.path.exists(dst):
            try:
                os.rename(src, dst)
                stats["root_xueshu"] += 1
            except OSError as e:
                errors.append(f"重命名失败 {src} → {dst}: {e}")
    
    if root_baihua:
        src = os.path.join(dirpath, "解读_白话_根目录版.md")
        dst = os.path.join(dirpath, "解讀_白話_根目录版.md")
        if not os.path.exists(dst):
            try:
                os.rename(src, dst)
                stats["root_baihua"] += 1
            except OSError as e:
                errors.append(f"重命名失败 {src} → {dst}: {e}")
    
    # 2. 处理带前缀的文件 → 裸名
    for f in prefixed_yuanwen:
        if has_yuanwen:
            conflicts.append(f"目录 {dirpath} 已有 原文.md，跳过 {f}")
            stats["conflicts"] += 1
            continue
        src = os.path.join(dirpath, f)
        dst = os.path.join(dirpath, "原文.md")
        try:
            os.rename(src, dst)
            stats["prefixed_yuanwen"] += 1
            has_yuanwen = True
        except OSError as e:
            errors.append(f"重命名失败 {src} → {dst}: {e}")
    
    for f in prefixed_xueshu:
        if has_xueshu_trad:
            conflicts.append(f"目录 {dirpath} 已有 解讀_學術.md，跳过 {f}")
            stats["conflicts"] += 1
            continue
        src = os.path.join(dirpath, f)
        dst = os.path.join(dirpath, "解讀_學術.md")
        try:
            os.rename(src, dst)
            stats["prefixed_xueshu"] += 1
            has_xueshu_trad = True
        except OSError as e:
            errors.append(f"重命名失败 {src} → {dst}: {e}")
    
    for f in prefixed_baihua:
        if has_baihua_trad:
            conflicts.append(f"目录 {dirpath} 已有 解讀_白話.md，跳过 {f}")
            stats["conflicts"] += 1
            continue
        src = os.path.join(dirpath, f)
        dst = os.path.join(dirpath, "解讀_白話.md")
        try:
            os.rename(src, dst)
            stats["prefixed_baihua"] += 1
            has_baihua_trad = True
        except OSError as e:
            errors.append(f"重命名失败 {src} → {dst}: {e}")


def main():
    if not os.path.isdir(ARCHIVE):
        print(f"错误：文献档案目录不存在: {ARCHIVE}")
        sys.exit(1)
    
    all_dirs = sorted(os.listdir(ARCHIVE))
    
    for period in PERIODS:
        period_dirs = []
        for d in all_dirs:
            dirpath = os.path.join(ARCHIVE, d)
            if not os.path.isdir(dirpath):
                continue
            # 匹配期数前缀：I06_, II01_, VII100_ 等
            # 需要确保 I 不匹配 II, III 等
            if d.startswith(period + "_"):
                period_dirs.append(dirpath)
            elif d.startswith(period) and len(d) > len(period):
                # 检查 period 后面是否跟数字
                next_char = d[len(period)]
                if next_char.isdigit():
                    period_dirs.append(dirpath)
        
        print(f"{period}期: {len(period_dirs)} 个目录")
        for dirpath in period_dirs:
            process_dir(dirpath)
    
    print("\n=== 统计 ===")
    print(f"扫描目录数: {stats['dirs_scanned']}")
    print(f"带前缀_原文 → 原文.md: {stats['prefixed_yuanwen']}")
    print(f"带前缀_解读_学术 → 解讀_學術.md: {stats['prefixed_xueshu']}")
    print(f"带前缀_解读_白话 → 解讀_白話.md: {stats['prefixed_baihua']}")
    print(f"裸名_解读_学术 → 解讀_學術.md: {stats['bare_xueshu']}")
    print(f"裸名_解读_白话 → 解讀_白話.md: {stats['bare_baihua']}")
    print(f"根目录版_学术 → 解讀_學術_根目录版.md: {stats['root_xueshu']}")
    print(f"根目录版_白话 → 解讀_白話_根目录版.md: {stats['root_baihua']}")
    print(f"冲突: {stats['conflicts']}")
    print(f"错误: {len(errors)}")
    
    if conflicts:
        print("\n=== 冲突详情 ===")
        for c in conflicts[:20]:
            print(f"  {c}")
        if len(conflicts) > 20:
            print(f"  ... 还有 {len(conflicts) - 20} 个")
    
    if errors:
        print("\n=== 错误详情 ===")
        for e in errors[:20]:
            print(f"  {e}")
        if len(errors) > 20:
            print(f"  ... 还有 {len(errors) - 20} 个")


if __name__ == "__main__":
    main()
