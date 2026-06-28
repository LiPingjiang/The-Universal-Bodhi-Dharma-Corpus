#!/usr/bin/env python3
"""统一编号 + 统一繁体名

将文献档案/下所有目录统一为：
  {连续编号}_{繁体文献名}

编号方案：
  001-031 保持不变
  I期 → 032-077
  II期 → 078-133
  ...
  X期 → 1076-29639
  XB期 → 29640-29689

同时将所有目录名（含子目录）转为繁体。

使用两阶段重命名避免冲突：
  Phase 1: 旧名 → _tmp_{编号}
  Phase 2: _tmp_{编号} → 新名
"""

import os
import sys
import re
from opencc import OpenCC

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(BASE, "文献档案")

cc = OpenCC('s2t')

# 期数定义和顺序
PERIOD_ORDER = [
    ("000s", r"^0\d{2}_"),     # 001-031
    ("I",    r"^I[0-9]"),       # I06-I36
    ("II",   r"^II[0-9]"),      # II01-II56
    ("III",  r"^III[0-9]"),     # III01-III62
    ("IV",   r"^IV[0-9]"),      # IV01-IV72
    ("V",    r"^V[0-9]"),       # V01-V52
    ("VI",   r"^VI[0-9]"),      # VI01-VI43
    ("VII",  r"^VII[0-9]"),     # VII01-VII212
    ("VIII", r"^VIII[0-9]"),    # VIII01-VIII301
    ("IX",   r"^IX[0-9]"),      # IX01-IX200
    ("X",    r"^X[0-9]"),       # X01-X28125
    ("XB",   r"^XB[0-9]"),      # XB01-XB50
]


def extract_number(dirname, period_key):
    """从目录名中提取编号数字部分"""
    if period_key == "000s":
        # 001_口传法藏 → 1
        m = re.match(r"^0(\d{2})_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "I":
        m = re.match(r"^I(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "II":
        m = re.match(r"^II(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "III":
        m = re.match(r"^III(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "IV":
        m = re.match(r"^IV(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "V":
        m = re.match(r"^V(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "VI":
        m = re.match(r"^VI(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "VII":
        m = re.match(r"^VII(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "VIII":
        m = re.match(r"^VIII(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "IX":
        m = re.match(r"^IX(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "X":
        m = re.match(r"^X(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    elif period_key == "XB":
        m = re.match(r"^XB(\d+)_", dirname)
        return int(m.group(1)) if m else 0
    return 0


def extract_name(dirname, period_key):
    """从目录名中提取文献名部分（去掉编号前缀）"""
    if period_key == "000s":
        # 001_口传法藏 → 口传法藏
        parts = dirname.split("_", 1)
        return parts[1] if len(parts) > 1 else dirname
    else:
        # I06_波罗提木叉 → 波罗提木叉
        # VII100_瑜伽師地論釋 → 瑜伽師地論釋
        # X01_四分律 → 四分律
        # XB01_大智度論 → 大智度論
        parts = dirname.split("_", 1)
        return parts[1] if len(parts) > 1 else dirname


def classify_period(dirname):
    """判断目录属于哪个期"""
    for period_key, pattern in PERIOD_ORDER:
        if re.match(pattern, dirname):
            return period_key
    return None


def build_rename_plan():
    """构建重命名计划
    
    返回: [(old_path, temp_path, new_path), ...]
    """
    all_dirs = sorted(os.listdir(ARCHIVE))
    
    # 按期分类
    by_period = {}
    for d in all_dirs:
        dirpath = os.path.join(ARCHIVE, d)
        if not os.path.isdir(dirpath):
            continue
        period = classify_period(d)
        if period is None:
            print(f"警告：无法分类目录 {d}")
            continue
        if period not in by_period:
            by_period[period] = []
        num = extract_number(d, period)
        by_period[period].append((num, d, dirpath))
    
    # 按期顺序排列，每期内按编号排序
    ordered = []
    for period_key, _ in PERIOD_ORDER:
        if period_key not in by_period:
            continue
        dirs = sorted(by_period[period_key], key=lambda x: x[0])
        ordered.extend(dirs)
        print(f"{period_key}: {len(dirs)} 个目录")
    
    print(f"总计: {len(ordered)} 个目录")
    
    # 分配新编号
    plan = []
    for i, (old_num, old_name, old_path) in enumerate(ordered):
        new_num = i + 1  # 001-29689
        new_num_str = f"{new_num:05d}"  # 5位补零
        
        # 提取文献名并转繁体
        period = classify_period(old_name)
        lit_name = extract_name(old_name, period)
        trad_name = cc.convert(lit_name)
        
        new_name = f"{new_num_str}_{trad_name}"
        new_path = os.path.join(ARCHIVE, new_name)
        temp_name = f"_tmp_{new_num_str}"
        temp_path = os.path.join(ARCHIVE, temp_name)
        
        plan.append((old_path, temp_path, new_path, old_name, new_name))
    
    return plan


def rename_subdirs_to_traditional(dirpath):
    """将目录内的子目录名转为繁体"""
    try:
        entries = os.listdir(dirpath)
    except OSError:
        return 0
    
    count = 0
    for entry in entries:
        entry_path = os.path.join(dirpath, entry)
        if not os.path.isdir(entry_path):
            continue
        
        # 转繁体
        trad_name = cc.convert(entry)
        if trad_name != entry:
            new_path = os.path.join(dirpath, trad_name)
            if not os.path.exists(new_path):
                try:
                    os.rename(entry_path, new_path)
                    count += 1
                except OSError as e:
                    print(f"  子目录重命名失败: {entry} → {trad_name}: {e}")
        
        # 递归处理子目录的子目录
        count += rename_subdirs_to_traditional(os.path.join(dirpath, trad_name) if trad_name != entry else entry_path)
    
    return count


def main():
    if not os.path.isdir(ARCHIVE):
        print(f"错误：{ARCHIVE} 不存在")
        sys.exit(1)
    
    # 构建计划
    print("=== 构建重命名计划 ===")
    plan = build_rename_plan()
    
    if not plan:
        print("没有需要重命名的目录")
        return
    
    # 显示前10个和后5个映射
    print("\n=== 前10个映射 ===")
    for old_path, temp_path, new_path, old_name, new_name in plan[:10]:
        print(f"  {old_name} → {new_name}")
    
    print("\n=== 后5个映射 ===")
    for old_path, temp_path, new_path, old_name, new_name in plan[-5:]:
        print(f"  {old_name} → {new_name}")
    
    # Phase 1: 旧名 → 临时名
    print(f"\n=== Phase 1: 重命名为临时名 ({len(plan)} 个) ===")
    errors = 0
    for i, (old_path, temp_path, new_path, old_name, _) in enumerate(plan):
        if old_path == temp_path:
            continue
        try:
            os.rename(old_path, temp_path)
        except OSError as e:
            print(f"  错误: {old_name} → {os.path.basename(temp_path)}: {e}")
            errors += 1
        if (i + 1) % 5000 == 0:
            print(f"  进度: {i+1}/{len(plan)}")
    
    print(f"Phase 1 完成，错误: {errors}")
    
    # Phase 2: 临时名 → 新名
    print(f"\n=== Phase 2: 重命名为最终名 ({len(plan)} 个) ===")
    errors = 0
    for i, (old_path, temp_path, new_path, old_name, new_name) in enumerate(plan):
        if temp_path == new_path:
            continue
        try:
            os.rename(temp_path, new_path)
        except OSError as e:
            print(f"  错误: {os.path.basename(temp_path)} → {new_name}: {e}")
            errors += 1
        if (i + 1) % 5000 == 0:
            print(f"  进度: {i+1}/{len(plan)}")
    
    print(f"Phase 2 完成，错误: {errors}")
    
    # Phase 3: 子目录名转繁体
    print(f"\n=== Phase 3: 子目录名转繁体 ===")
    total_subdir_renames = 0
    for i, (_, _, new_path, _, new_name) in enumerate(plan):
        count = rename_subdirs_to_traditional(new_path)
        total_subdir_renames += count
        if (i + 1) % 5000 == 0:
            print(f"  进度: {i+1}/{len(plan)}, 子目录重命名: {total_subdir_renames}")
    
    print(f"Phase 3 完成，子目录重命名: {total_subdir_renames}")
    
    # 统计
    renamed_count = sum(1 for old_path, temp_path, new_path, old_name, new_name in plan if old_name != new_name)
    print(f"\n=== 最终统计 ===")
    print(f"总目录数: {len(plan)}")
    print(f"重命名目录: {renamed_count}")
    print(f"子目录转繁体: {total_subdir_renames}")


if __name__ == "__main__":
    main()
