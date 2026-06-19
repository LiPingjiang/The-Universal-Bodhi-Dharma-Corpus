#!/usr/bin/env python3
import openpyxl, os, glob, re

wb = openpyxl.load_workbook('佛教佛法文献古籍大全.xlsx')
ws = wb['文献大全']
rows = list(ws.iter_rows(min_row=2, values_only=True))

excel_entries = []
for r in rows:
    num = r[0]
    period = r[1] if len(r) > 1 else ''
    name = r[2] if len(r) > 2 else ''
    era = r[3] if len(r) > 3 else ''
    excel_entries.append((num, period, name, era))

md_files = glob.glob('文献档案/*.md')
md_names = []
for f in md_files:
    if 'README' in f:
        continue
    md_names.append(os.path.basename(f).replace('.md', ''))

# 更精确的匹配函数
def match_entry(name, md_names):
    """检查Excel名称是否匹配任何文件名"""
    name_clean = name.strip()
    
    for md in md_names:
        md_clean = md.replace('_', '').strip()
        
        # 直接包含检查
        if name_clean in md_clean or md_clean in name_clean:
            return True
        
        # 去除常见后缀的检查
        name_no_suffix = re.sub(r'[经论集]$', '', name_clean)
        md_no_suffix = re.sub(r'[经论集]$', '', md_clean)
        if name_no_suffix in md_no_suffix or md_no_suffix in name_no_suffix:
            return True
        
        # 检查核心名称（去除"大乘"、"小乘"等前缀）
        name_core = re.sub(r'^大乘|^小乘|^藏传佛教|^日本|^朝鲜|^越南|^东南亚', '', name_clean)
        md_core = re.sub(r'^大乘|^小乘|^藏传佛教|^日本|^朝鲜|^越南|^东南亚', '', md_clean)
        if name_core in md_core or md_core in name_core:
            return True
    
    return False

print('=== Excel条目没有对应.md文件 ===')
missing = []
for num, period, name, era in excel_entries:
    if not match_entry(name, md_names):
        missing.append((num, period, name, era))
        print(f'{num} | {period} | {name}')

print(f'\n总计缺失: {len(missing)}个')

# 也检查反向：哪些文件名没有对应Excel条目
print('\n=== .md文件没有对应Excel条目 ===')
md_missing = []
for md in md_names:
    found = False
    for num, period, name, era in excel_entries:
        if match_entry(name, [md]):
            found = True
            break
    if not found:
        md_missing.append(md)
        print(md)

print(f'\n总计多余: {len(md_missing)}个')
