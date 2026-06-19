#!/usr/bin/env python3
import os, glob

dirs = [d for d in glob.glob('文献档案/*') if os.path.isdir(d) and '001_口传法藏' not in d]

print('=== 检查子目录三件套文件质量 ===\n')

low_quality = []
for d in dirs:
    basename = os.path.basename(d)
    files = glob.glob(d + '/*.md')
    
    for f in files:
        if 'README' in f:
            continue
        size = os.path.getsize(f)
        with open(f, 'r') as file:
            content = file.read()
        
        # 检查质量
        if size < 500:
            low_quality.append((os.path.basename(d), os.path.basename(f), size, '文件过小'))
        elif content.count('待补充') > 3 or content.count('TODO') > 0:
            low_quality.append((os.path.basename(d), os.path.basename(f), size, '包含待补充标记'))
        elif len(content.strip()) < 800:
            low_quality.append((os.path.basename(d), os.path.basename(f), size, '内容过少'))

print(f'子目录总数: {len(dirs)}')
print(f'低质量文件: {len(low_quality)}')

if low_quality:
    print('\n=== 需要完善的文件（前50个）===')
    for dir_name, file_name, size, reason in low_quality[:50]:
        print(f'  {dir_name}/{file_name} ({size} bytes): {reason}')
