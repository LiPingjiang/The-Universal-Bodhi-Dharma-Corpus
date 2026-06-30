#!/usr/bin/env python3
"""修复README中的markdown链接问题

上一轮脚本过于激进，把markdown链接的文本部分也吃掉了。
这个脚本修复：[原文](原文.md) 格式的链接，确保链接文本和路径都正确。
"""

import os
import re
from opencc import OpenCC

ARCHIVE = "/mnt/openclaw/catdesk/home/佛法/文献档案"
cc = OpenCC('s2t')

stats = {"fixed": 0, "links_fixed": 0, "errors": 0}

def fix_markdown_links(content):
    """修复被破坏的markdown链接
    
    问题模式：原文.md) 或 解讀_學術.md) （缺少链接文本和开括号）
    期望结果：[原文](原文.md) 或 [解讀_學術](解讀_學術.md)
    
    也修复：[旧文本](路径) 中旧文本仍为简体的情况
    """
    # Fix broken links: "- 原文.md)" → "- [原文](原文.md)"
    broken_patterns = [
        (r'(?<![\[\w])- (原文\.md)\)', r'- [原文](\1)'),
        (r'(?<![\[\w])- (解讀_學術\.md)\)', r'- [解讀_學術](\1)'),
        (r'(?<![\[\w])- (解讀_白話\.md)\)', r'- [解讀_白話](\1)'),
    ]
    
    for pattern, replacement in broken_patterns:
        content, n = re.subn(pattern, replacement, content)
        stats["links_fixed"] += n
    
    # Fix link text: [金刚经_原文](原文.md) → [原文](原文.md)
    # Pattern: [something_原文](原文.md) → [原文](原文.md)
    link_text_patterns = [
        (r'\[[^\]]+_原文\](\(原文\.md\))', r'[原文]\1'),
        (r'\[[^\]]+_解读_学术\](\(解讀_學術\.md\))', r'[解讀_學術]\1'),
        (r'\[[^\]]+_解读_白话\](\(解讀_白話\.md\))', r'[解讀_白話]\1'),
        (r'\[[^\]]+_解讀_學術\](\(解讀_學術\.md\))', r'[解讀_學術]\1'),
        (r'\[[^\]]+_解讀_白話\](\(解讀_白話\.md\))', r'[解讀_白話]\1'),
        # Also fix simplified link text
        (r'\[解读_学术\](\(解讀_學術\.md\))', r'[解讀_學術]\1'),
        (r'\[解读_白话\](\(解讀_白話\.md\))', r'[解讀_白話]\1'),
    ]
    
    for pattern, replacement in link_text_patterns:
        content, n = re.subn(pattern, replacement, content)
        stats["links_fixed"] += n
    
    # Fix remaining old-style file references in tables:
    # | [原文](./01_xxx/xxx_原文.md) | → | [原文](./01_xxx/原文.md) |
    # This handles patterns inside () where path has subdirectory
    table_patterns = [
        (r'\(\./([^)]+)/[^)]+_原文\.md\)', r'(\1/原文.md)'),
        (r'\(\./([^)]+)/[^)]+_解读_学术\.md\)', r'(\1/解讀_學術.md)'),
        (r'\(\./([^)]+)/[^)]+_解读_白话\.md\)', r'(\1/解讀_白話.md)'),
        (r'\(\./([^)]+)/[^)]+_解讀_學術\.md\)', r'(\1/解讀_學術.md)'),
        (r'\(\./([^)]+)/[^)]+_解讀_白話\.md\)', r'(\1/解讀_白話.md)'),
    ]
    
    for pattern, replacement in table_patterns:
        content, n = re.subn(pattern, replacement, content)
        stats["links_fixed"] += n
    
    return content


def fix_xlsx_refs(content):
    """修复xlsx文件引用"""
    # 001_口传法藏明细.xlsx → 口傳法藏明細.xlsx
    content = re.sub(r'001_口传法藏明细\.xlsx', '口傳法藏明細.xlsx', content)
    return content


def fix_title_numbering(content, dir_num):
    """修复标题中的旧编号"""
    # "# 001 · 佛陀口傳法藏" → "# 00001 · 佛陀口傳法藏"
    # Only fix if the title starts with a short number that matches old scheme
    content = re.sub(r'^# (\d{1,3})\s', f'# {dir_num} ', content, count=1, flags=re.MULTILINE)
    return content


def process_readme(filepath, dir_name, dir_num):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        stats["errors"] += 1
        return
    
    original = content
    content = fix_markdown_links(content)
    content = fix_xlsx_refs(content)
    content = fix_title_numbering(content, dir_num)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats["fixed"] += 1
        except:
            stats["errors"] += 1


def main():
    all_dirs = sorted(os.listdir(ARCHIVE))
    
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
            process_readme(readme_path, dirname, dir_num)
        
        # Process subdirectory READMEs
        try:
            for sd in os.listdir(dirpath):
                sd_path = os.path.join(dirpath, sd)
                if not os.path.isdir(sd_path):
                    continue
                sd_readme = os.path.join(sd_path, "README.md")
                if os.path.isfile(sd_readme):
                    process_readme(sd_readme, sd, dir_num)
                # One more level
                try:
                    for ssd in os.listdir(sd_path):
                        ssd_path = os.path.join(sd_path, ssd)
                        if not os.path.isdir(ssd_path):
                            continue
                        ssd_readme = os.path.join(ssd_path, "README.md")
                        if os.path.isfile(ssd_readme):
                            process_readme(ssd_readme, ssd, dir_num)
                except:
                    pass
        except:
            pass
        
        if (i + 1) % 5000 == 0:
            print(f"  进度: {i+1}/{len(all_dirs)}...")
    
    print(f"\n=== 统计 ===")
    print(f"修复README: {stats['fixed']}")
    print(f"链接修复: {stats['links_fixed']}")
    print(f"错误: {stats['errors']}")


if __name__ == "__main__":
    main()
