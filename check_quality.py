#!/usr/bin/env python3
import os, glob

md_files = [f for f in glob.glob('文献档案/*.md') if 'README' not in f]
empty_or_template = []

for f in md_files:
    size = os.path.getsize(f)
    with open(f, 'r') as file:
        content = file.read()
    
    if size < 500:
        empty_or_template.append((os.path.basename(f), size, '文件过小'))
    elif content.count('待补充') > 5 or content.count('TODO') > 0 or content.count('FIXME') > 0:
        empty_or_template.append((os.path.basename(f), size, '包含待补充标记'))
    elif len(content.strip()) < 1000:
        empty_or_template.append((os.path.basename(f), size, '内容过少'))

print(f'主目录.md文件总数: {len(md_files)}')
print(f'需要完善的文件: {len(empty_or_template)}')
if empty_or_template:
    print('\n=== 需要完善的文件 ===')
    for name, size, reason in empty_or_template[:50]:
        print(f'  {name} ({size} bytes): {reason}')
