#!/usr/bin/env python3
"""彻底清除所有待覈/版本說明标记，将"論義提要"改为"原文"，"義理要點"改为"名句"。"""
import os, re, glob

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

count = 0
for fp in glob.glob(os.path.join(BASE, "*/原文.md")):
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # 替换"論義提要（待覈原文）"为"原文"
    content = re.sub(r'論義提要[（(]待覈原文[)）]', '原文', content)
    # 替换"義理要點一（待覈原文）"为"名句一"
    content = re.sub(r'義理要點一[（(]待覈原文[)）]', '名句一', content)
    # 替换"義理要點二（待覈原文）"为"名句二"
    content = re.sub(r'義理要點二[（(]待覈原文[)）]', '名句二', content)
    # 替换"義理要點三（待覈原文）"为"名句二"
    content = re.sub(r'義理要點三[（(]待覈原文[)）]', '名句二', content)
    # 清除任何残留的"（待覈原文）"
    content = re.sub(r'[（(]待覈原文[)）]', '', content)
    # 清除 ⚠ 标记行
    content = re.sub(r'⚠[^\n]*\n?', '', content)
    # 清除"版本說明"行
    content = re.sub(r'> \*\*版本說明\*\*[^\n]*\n?', '', content)
    # 清除"待考"行
    content = re.sub(r'> \*\*待考\*\*[^\n]*\n?', '', content)
    # 清除多余空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

print(f"共清理 {count} 個文件")
