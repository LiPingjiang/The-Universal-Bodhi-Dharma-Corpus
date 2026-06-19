#!/usr/bin/env python3
import os, glob

dirs = [d for d in glob.glob('文献档案/*') if os.path.isdir(d)]
print(f'子目录总数: {len(dirs)}')

complete = 0
incomplete = 0
incomplete_list = []

for d in dirs:
    basename = os.path.basename(d)
    files = glob.glob(d + '/*.md')
    
    # 001_口传法藏是特殊情况，有子分类目录，不在根目录放三件套
    if basename == '001_口传法藏':
        complete += 1
        continue
    
    has_readme = any('README' in f for f in files)
    has_original = any('原文' in f for f in files)
    has_academic = any('学术' in f for f in files)
    has_plain = any('白话' in f for f in files)
    
    if has_readme and has_original and has_academic and has_plain:
        complete += 1
    else:
        incomplete += 1
        missing = []
        if not has_readme: missing.append('README')
        if not has_original: missing.append('原文')
        if not has_academic: missing.append('学术')
        if not has_plain: missing.append('白话')
        incomplete_list.append((os.path.basename(d), missing))

print(f'完整三件套: {complete}')
print(f'不完整: {incomplete}')

if incomplete_list:
    print('\n=== 不完整的子目录 ===')
    for name, missing in incomplete_list:
        print(f'  {name}: 缺少 {missing}')
