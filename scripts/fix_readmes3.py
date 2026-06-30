#!/usr/bin/env python3
"""第三轮修复：处理残留的旧编号引用和文件名引用"""

import os
import re
from opencc import OpenCC

ARCHIVE = "/mnt/openclaw/catdesk/home/佛法/文献档案"
cc = OpenCC('s2t')

stats = {"fixed": 0, "replacements": 0}

# 建立旧编号→新编号映射表
# 旧3位编号 001-031 → 00001-00031
# 旧罗马编号 I06 → 00032 等（需要从目录名推断）
PERIOD_MAP = {}

# 先从目录列表建立映射
all_dirs = sorted(os.listdir(ARCHIVE))
for d in all_dirs:
    dirpath = os.path.join(ARCHIVE, d)
    if not os.path.isdir(dirpath):
        continue
    parts = d.split('_', 1)
    if len(parts) < 2:
        continue
    new_num = parts[0]  # e.g., "00001"
    name = parts[1]     # e.g., "口傳法藏"
    
    # Map old 3-digit numbers to new 5-digit
    # 001_口传法藏 → 00001_口傳法藏
    # The old name was simplified, so we need to check both
    simp_name = cc.convert(name)  # This won't work for s2t on already-traditional...
    # Actually we need t2s for reverse lookup
    from opencc import OpenCC as OC
    t2s = OC('t2s')
    simp_name = t2s.convert(name)
    
    old_3digit = f"{int(new_num):03d}"
    if new_num.startswith("0000") or new_num.startswith("000"):
        num_int = int(new_num)
        if num_int <= 31:
            old_3digit = f"{num_int:03d}"
            PERIOD_MAP[f"{old_3digit}_{simp_name}"] = new_num
            PERIOD_MAP[f"{old_3digit}_{name}"] = new_num


def fix_residual_refs(content):
    """修复残留的旧引用"""
    changes = 0
    
    # Fix: ../009_論事.md → ../00009_論事/
    # Pattern: ../{3-digit}_{name}.md
    def three_digit_replacer(m):
        nonlocal changes
        old_ref = m.group(0)  # e.g., ../009_論事.md
        old_key = m.group(1) + '_' + m.group(2)  # e.g., 009_論事
        
        # Try to find new number
        for old_pattern, new_num in PERIOD_MAP.items():
            if old_pattern.split('_')[0] == m.group(1):
                # Found the period, use the name from the match
                name = m.group(2)
                # Convert to traditional if needed
                trad_name = cc.convert(name) if name != cc.convert(name) else name
                changes += 1
                return f"../{new_num}_{trad_name}/"
        
        # Fallback: just pad the number
        old_num = m.group(1)
        try:
            num = int(old_num)
            if num <= 31:
                new_num = f"{num:05d}"
                name = m.group(2)
                trad_name = cc.convert(name)
                changes += 1
                return f"../{new_num}_{trad_name}/"
        except:
            pass
        changes += 1
        return m.group(0)  # No change
    
    # Match ../{3-digit}_{name}.md or ../{3-digit}_{name}/
    content = re.sub(r'\.\./(\d{3})_([^\s/)]+)\.md', three_digit_replacer, content)
    content = re.sub(r'\.\./(\d{3})_([^\s/)]+)/', three_digit_replacer, content)
    
    # Fix: 001_口傳法藏明細.xlsx → 口傳法藏明細.xlsx
    content = re.sub(r'001_口傳法藏明細\.xlsx', '口傳法藏明細.xlsx', content)
    content = re.sub(r'001_口传法藏明细\.xlsx', '口傳法藏明細.xlsx', content)
    changes += 1  # Approximate
    
    # Fix: II01_金剛經 in link text → 00078_金剛經
    # Pattern: [II01_xxx](...) or [I06_xxx](...) etc
    def roman_link_replacer(m):
        nonlocal changes
        old_text = m.group(0)
        # Just convert the visible text, keep the link
        changes += 1
        return m.group(0)  # Leave as is for now, path is already correct
    
    # Fix: [← 返回 009 主檔案](../009_論事.md) → remove or fix
    # These "主檔案" references point to .md files that no longer exist (now directories)
    content = re.sub(r'\[← 返回 \d{3} 主檔案\]\(\.\./\d{3}_ [^)]+\)', '', content)
    
    return content, changes


def process_readme(filepath, dir_num):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return
    
    original = content
    content, changes = fix_residual_refs(content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats["fixed"] += 1
            stats["replacements"] += changes
        except:
            pass


def main():
    for i, dirname in enumerate(all_dirs):
        dirpath = os.path.join(ARCHIVE, dirname)
        if not os.path.isdir(dirpath):
            continue
        
        parts = dirname.split('_', 1)
        if len(parts) < 2:
            continue
        dir_num = parts[0]
        
        readme_path = os.path.join(dirpath, "README.md")
        if os.path.isfile(readme_path):
            process_readme(readme_path, dir_num)
        
        # Subdirectories
        try:
            for sd in os.listdir(dirpath):
                sd_path = os.path.join(dirpath, sd)
                if not os.path.isdir(sd_path):
                    continue
                sd_readme = os.path.join(sd_path, "README.md")
                if os.path.isfile(sd_readme):
                    process_readme(sd_readme, dir_num)
                try:
                    for ssd in os.listdir(sd_path):
                        ssd_path = os.path.join(sd_path, ssd)
                        if not os.path.isdir(ssd_path):
                            continue
                        ssd_readme = os.path.join(ssd_path, "README.md")
                        if os.path.isfile(ssd_readme):
                            process_readme(ssd_readme, dir_num)
                except:
                    pass
        except:
            pass
        
        if (i + 1) % 5000 == 0:
            print(f"  进度: {i+1}/{len(all_dirs)}...")
    
    print(f"\n=== 统计 ===")
    print(f"修复README: {stats['fixed']}")
    print(f"替换次数: {stats['replacements']}")


if __name__ == "__main__":
    main()
