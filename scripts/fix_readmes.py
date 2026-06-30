#!/usr/bin/env python3
"""批量修复27372个目录README

修复内容：
1. 旧文件引用 → 新裸名：xxx_原文.md → 原文.md, xxx_解读_学术.md → 解讀_學術.md, xxx_解读_白话.md → 解讀_白話.md
2. 旧目录引用 → 新编号繁体名
3. 旧编号引用 → 新5位编号
4. 简体中文 → 繁體中文
"""

import os
import re
import sys
from opencc import OpenCC

BASE = "/mnt/openclaw/catdesk/home/佛法"
ARCHIVE = os.path.join(BASE, "文献档案")

cc = OpenCC('s2t')

stats = {
    "readme_found": 0,
    "readme_fixed": 0,
    "file_ref_fixed": 0,
    "dir_ref_fixed": 0,
    "simp_to_trad": 0,
    "errors": 0,
}

def fix_file_references(content):
    """修复文件引用：旧带前缀文件名 → 新裸名"""
    changes = 0
    
    # Pattern: {anything}_原文.md → 原文.md  (but not 原文_备份.md or 原文_根目录版.md)
    # Also handle both () markdown links and bare references
    patterns = [
        # 带前缀的三件套引用
        (r'[^\s/)]+_原文\.md', '原文.md'),
        (r'[^\s/)]+_解读_学术\.md', '解讀_學術.md'),
        (r'[^\s/)]+_解读_白话\.md', '解讀_白話.md'),
        (r'[^\s/)]+_解讀_學術\.md', '解讀_學術.md'),
        (r'[^\s/)]+_解讀_白話\.md', '解讀_白話.md'),
        # 简体裸名
        (r'(?<![/\w])解读_学术\.md', '解讀_學術.md'),
        (r'(?<![/\w])解读_白话\.md', '解讀_白話.md'),
        (r'(?<![/\w])解读_学术_根目录版\.md', '解讀_學術_根目录版.md'),
        (r'(?<![/\w])解读_白话_根目录版\.md', '解讀_白話_根目录版.md'),
    ]
    
    for old_pattern, new_text in patterns:
        def replacer(m):
            nonlocal changes
            changes += 1
            return new_text
        content = re.sub(old_pattern, replacer, content)
    
    return content, changes


def fix_simplified_chinese(content):
    """简体转繁体（仅对README内容，不转代码块内的路径）"""
    # Split by code blocks to avoid converting code block content
    parts = content.split('```')
    for i in range(len(parts)):
        if i % 2 == 0:  # Outside code blocks
            trad = cc.convert(parts[i])
            if trad != parts[i]:
                parts[i] = trad
    
    return '```'.join(parts)


def fix_old_numbering_refs(content, dir_name, dir_num):
    """修复旧编号引用"""
    changes = 0
    
    # Fix "返回主档案" references like ../II01_金刚经.md → ../00078_金剛經/
    # Pattern: ../{old_prefix}_{name}.md or ../{old_prefix}_{name}/
    old_prefix_pattern = re.compile(r'\.\./(I[0-9]+|II[0-9]+|III[0-9]+|IV[0-9]+|V[0-9]+|VI[0-9]+|VII[0-9]+|VIII[0-9]+|IX[0-9]+|X[0-9]+|XB[0-9]+)_([^\s/)]+)')
    
    def old_prefix_replacer(m):
        nonlocal changes
        changes += 1
        return f"../{dir_num}_{dir_name.split('_', 1)[1] if '_' in dir_name else dir_name}"
    
    content = old_prefix_pattern.sub(old_prefix_replacer, content)
    
    # Fix "编号：X301" style references
    old_num_pattern = re.compile(r'\*\*编号\*\*：\s*(X\d+|XB\d+|I\d+|II\d+|III\d+|IV\d+|V\d+|VI\d+|VII\d+|VIII\d+|IX\d+)')
    
    def num_replacer(m):
        nonlocal changes
        changes += 1
        return f"**编号**：{dir_num}"
    
    content = old_num_pattern.sub(num_replacer, content)
    
    return content, changes


def process_readme(filepath, dir_name, dir_num):
    """处理单个README文件"""
    stats["readme_found"] += 1
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        stats["errors"] += 1
        return
    
    original = content
    total_changes = 0
    
    # 1. Fix file references
    content, file_changes = fix_file_references(content)
    stats["file_ref_fixed"] += file_changes
    total_changes += file_changes
    
    # 2. Fix old numbering references
    content, num_changes = fix_old_numbering_refs(content, dir_name, dir_num)
    stats["dir_ref_fixed"] += num_changes
    total_changes += num_changes
    
    # 3. Convert simplified to traditional (only outside code blocks)
    before_trad = content
    content = fix_simplified_chinese(content)
    if content != before_trad:
        stats["simp_to_trad"] += 1
        total_changes += 1
    
    # Write back if changed
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats["readme_fixed"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"写入失败 {filepath}: {e}")


def main():
    if not os.path.isdir(ARCHIVE):
        print(f"错误：{ARCHIVE} 不存在")
        sys.exit(1)
    
    all_dirs = sorted(os.listdir(ARCHIVE))
    
    for i, dirname in enumerate(all_dirs):
        dirpath = os.path.join(ARCHIVE, dirname)
        if not os.path.isdir(dirpath):
            continue
        
        readme_path = os.path.join(dirpath, "README.md")
        if not os.path.isfile(readme_path):
            continue
        
        # Extract number from dirname
        parts = dirname.split('_', 1)
        if len(parts) < 2:
            continue
        dir_num = parts[0]
        
        process_readme(readme_path, dirname, dir_num)
        
        # Also process subdirectory READMEs (for 001-031 period)
        try:
            subdirs = os.listdir(dirpath)
            for sd in subdirs:
                sd_path = os.path.join(dirpath, sd)
                if not os.path.isdir(sd_path):
                    continue
                sd_readme = os.path.join(sd_path, "README.md")
                if os.path.isfile(sd_readme):
                    process_readme(sd_readme, sd, dir_num)
                
                # Check one more level deep (for 001's nested structure)
                try:
                    subsubdirs = os.listdir(sd_path)
                    for ssd in subsubdirs:
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
    print(f"找到README: {stats['readme_found']}")
    print(f"修复README: {stats['readme_fixed']}")
    print(f"文件引用修复: {stats['file_ref_fixed']}")
    print(f"目录/编号引用修复: {stats['dir_ref_fixed']}")
    print(f"简转繁: {stats['simp_to_trad']}")
    print(f"错误: {stats['errors']}")


if __name__ == "__main__":
    main()
