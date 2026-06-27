#!/usr/bin/env python3
"""修复XB编号冲突：两个脚本都从XB01开始，导致重复。
第一个脚本创建了XB01-XB09(X151-X159) + XB50(X200)。
fix脚本创建了XB01-XB40(X160-X199)，与XB01-XB09冲突。
需要把fix脚本创建的XB01-XB40重命名为XB11-XB50。
"""
import os
import shutil

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 第一个脚本创建的XB目录（正确编号）：
first_script_xbs = {
    "XB01_大智度論", "XB02_十地經論", "XB03_大乘寶性論", "XB04_大乘集菩薩學論",
    "XB05_入菩薩行論", "XB06_菩提道燈論", "XB07_密宗道次第論", "XB08_現觀莊嚴論",
    "XB09_辨法法性論", "XB50_因明正理門論",
}

# 获取所有XB目录
all_xb = sorted([d for d in os.listdir(BASE) if d.startswith("XB") and os.path.isdir(os.path.join(BASE, d))])

# 找出需要重命名的（fix脚本创建的）
to_rename = []
for d in all_xb:
    if d not in first_script_xbs:
        to_rename.append(d)

print(f"第一个脚本创建的XB目录: {len(first_script_xbs)}")
print(f"需要重命名的fix脚本XB目录: {len(to_rename)}")
print()

# 按当前XB编号排序，重新分配XB11-XB49（跳过XB50）
# fix脚本处理的是X160-X199，共40个，应为XB10-XB49
# 但XB10和XB50已被第一个脚本占用（XB10_釋量論不存在，XB50_因明正理門論存在）
# 实际上第一个脚本没有创建XB10（因为X160的文件名不匹配）
# 所以fix脚本的XB01-XB40 → XB10-XB49

new_num = 10
renamed = 0
for d in sorted(to_rename, key=lambda x: (int(x[2:4]), x)):
    old_path = os.path.join(BASE, d)
    # 提取文献名
    name = d[5:]  # 去掉 "XB{nn}_"
    new_dir = f"XB{new_num:02d}_{name}"
    new_path = os.path.join(BASE, new_dir)
    
    if os.path.exists(new_path):
        print(f"⚠️ 目标已存在: {new_dir}，跳过")
    else:
        os.rename(old_path, new_path)
        renamed += 1
    
    new_num += 1

print(f"\n已重命名 {renamed} 个XB目录")
print(f"新编号范围: XB10 - XB{new_num-1:02d}")

# 验证最终XB目录
final_xb = sorted([d for d in os.listdir(BASE) if d.startswith("XB") and os.path.isdir(os.path.join(BASE, d))])
print(f"\n最终XB目录总数: {len(final_xb)}")
for d in final_xb:
    files = os.listdir(os.path.join(BASE, d))
    print(f"  {d}: {len(files)} files")
