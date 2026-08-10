#!/usr/bin/env python3
"""
处理剩余 *待补充* 格式的占位符文件
"""
import os, glob, re

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 导入主脚本的内容生成函数
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from fill_generic_content import gen_content

count = 0
for fp in sorted(glob.glob(os.path.join(BASE, "*/原文.md"))):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # 检查是否仅为 *待补充*
    if content in ('*待补充*', '*待補充*', '# 待补充', '# 待補充'):
        rel_path = os.path.relpath(fp, BASE)
        dirname = rel_path.split('/')[0]
        parts = dirname.split('_', 1)
        if len(parts) < 2:
            continue
        num, name = parts[0], parts[1]
        
        new_content = gen_content(dirname, num, name)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"共处理 {count} 个 *待补充* 文件")
