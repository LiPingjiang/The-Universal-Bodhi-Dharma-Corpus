#!/usr/bin/env python3
"""
修复索引卡.md和README.md中的旧格式链接。
旧格式使用I/III/VII前缀，需要映射到新的5位阿拉伯数字格式。
"""
import os, glob, re

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 旧编号→新编号映射（基于之前的修复工作中建立的对应关系）
# I前缀 = 印度部派/上座部典籍 (00001-00100区间)
I_MAP = {
    'I01': '00001', 'I02': '00002', 'I03': '00003', 'I04': '00004',
    'I05': '00005', 'I06': '00006', 'I07': '00007', 'I08': '00008',
    'I09': '00009', 'I10': '00010', 'I11': '00011', 'I12': '00012',
    'I13': '00013', 'I14': '00014', 'I15': '00015', 'I16': '00016',
    'I17': '00043', 'I18': '00044', 'I19': '00045', 'I20': '00046',
    'I21': '00047', 'I22': '00048', 'I23': '00049', 'I24': '00003',
    'I25': '00050', 'I26': '00051', 'I27': '00052', 'I28': '00053',
    'I29': '00054', 'I30': '00055', 'I31': '00056', 'I32': '00057',
    'I33': '00058', 'I34': '00059', 'I35': '00060', 'I36': '00061',
    'I37': '00062', 'I38': '00063', 'I39': '00064', 'I40': '00065',
    'I41': '00066', 'I42': '00067', 'I43': '00068', 'I44': '00069',
    'I45': '00070', 'I46': '00071', 'I47': '00072', 'I48': '00073',
    'I49': '00074', 'I50': '00075', 'I51': '00076', 'I52': '00077',
    'I53': '00078', 'I54': '00079', 'I55': '00080', 'I56': '00081',
    'I57': '00082', 'I58': '00083', 'I59': '00084', 'I60': '00085',
    'I61': '00086', 'I62': '00087', 'I63': '00088', 'I64': '00089',
    'I65': '00090', 'I66': '00091', 'I67': '00092', 'I68': '00093',
    'I69': '00094', 'I70': '00095', 'I71': '00096', 'I72': '00097',
    'I73': '00098', 'I74': '00099', 'I75': '00100',
}

# III前缀 = 印度大乘/论书 (00138区间)
III_MAP = {
    'III01': '00138', 'III02': '00139', 'III03': '00140', 'III04': '00141',
    'III05': '00142', 'III06': '00143', 'III07': '00144', 'III08': '00145',
    'III09': '00146', 'III10': '00147', 'III11': '00148', 'III12': '00149',
    'III13': '00150', 'III14': '00151', 'III15': '00152', 'III16': '00153',
    'III17': '00154', 'III18': '00155', 'III19': '00156', 'III20': '00157',
}

# VII前缀 = 藏传典籍 (00300区间)  
VII_MAP = {
    'VII01': '00300', 'VII02': '00301', 'VII03': '00302', 'VII04': '00303',
    'VII05': '00304', 'VII06': '00305', 'VII07': '00306', 'VII08': '00307',
    'VII09': '00308', 'VII10': '00309',
}

# 合并所有映射
ALL_MAPS = {**I_MAP, **III_MAP, **VII_MAP}

# 律藏相关文献正确链接（替换错误的阿毗达磨链接）
VINAYA_RELATED_LINKS = """## 相關文獻

- [00005_巴利律藏](00005_巴利律藏/原文.md) — 上座部律藏根本
- [00266_四分律行事鈔](00266_四分律行事鈔/原文.md) — 漢傳律宗要典
- [00068_界論](00068_界論/原文.md) — 阿毗達磨論書
"""

ABHIDHARMA_RELATED_LINKS = """## 相關文獻

- [00043_巴利論藏七論](00043_巴利論藏七論/原文.md) — 上座部阿毗達磨核心
- [00046_大毗婆沙論](00046_大毗婆沙論/原文.md) — 阿毗達磨百科全書
- [00141_俱舍論](00141_俱舍論/原文.md) — 世親綜合阿毗達磨
"""

# 文献类型→正确相关链接映射
def get_correct_related_links(dirname):
    """根据文献类型返回正确的相关文献链接"""
    num = int(dirname.split('_')[0])
    
    # 律藏类 (00005-00056区间)
    if any(kw in dirname for kw in ['律', '戒', '波羅提木叉', '毗奈耶', 'Vinaya', 'pratimokṣa']):
        return VINAYA_RELATED_LINKS
    
    # 论书类
    if any(kw in dirname for kw in ['論', '阿毗達磨', 'Abhidharma', '毗婆沙', '俱舍', '品類足', '界論', '發趣']):
        return ABHIDHARMA_RELATED_LINKS
    
    # 默认：通用佛教典籍链接
    return """## 相關文獻

- [大正新脩大藏經](大正新脩大藏經/) — 漢文大藏經標準版本
- [佛教佛法文獻古籍大全](README.md) — 全庫總索引
"""

def fix_old_links(content, dirname):
    """修复旧格式链接"""
    # 替换 I/III/VII 编号引用
    for old_prefix, new_num in sorted(ALL_MAPS.items(), key=lambda x: -len(x[0])):
        # [I17_巴利论藏七论](I17_巴利论藏七论.md)
        pattern = rf'\[{re.escape(old_prefix)}_[^\]]+\]\({re.escape(old_prefix)}_[^\)]+\.md\)'
        # 查找匹配
        matches = list(re.finditer(pattern, content))
        if matches:
            # 需要找到对应的新目录名
            for m in matches:
                old_link = m.group(0)
                # 提取文献名
                name_match = re.search(rf'{re.escape(old_prefix)}_(.+?)\]', old_link)
                if name_match:
                    old_name = name_match.group(1)
                    # 尝试查找以新编号开头的目录
                    new_dir_pattern = os.path.join(BASE, f"{new_num}_*")
                    matching_dirs = glob.glob(new_dir_pattern)
                    if matching_dirs:
                        new_dirname = os.path.basename(matching_dirs[0])
                        # 使用新目录名替换
                        new_link = f"[{new_dirname}]({new_dirname}/原文.md)"
                        content = content.replace(old_link, new_link)
    
    # 替换编号表格中的旧编号
    for old_prefix, new_num in sorted(ALL_MAPS.items(), key=lambda x: -len(x[0])):
        content = content.replace(f'| 编号 | {old_prefix} |', f'| 编号 | {new_num} |')
        content = content.replace(f'编号 {old_prefix}', f'编号 {new_num}')
    
    # 替换底部旧编号引用
    for old_prefix, new_num in sorted(ALL_MAPS.items(), key=lambda x: -len(x[0])):
        content = content.replace(f'编号 {old_prefix}', f'编号 {new_num}')
    
    return content

def is_vinaya_wrong_link(content):
    """检查律藏文献是否有错误的论书链接"""
    if not any(kw in content for kw in ['律', '戒', 'Vinaya', '波羅提木叉']):
        return False
    return 'I17_巴利论藏七论' in content or 'I20_大毗婆沙论' in content

count = 0
for fp in sorted(glob.glob(os.path.join(BASE, "*/索引卡.md")) + glob.glob(os.path.join(BASE, "*/README.md"))):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    dirname = os.path.basename(os.path.dirname(fp))
    
    # 先修正律藏文献中错误的论书链接
    if is_vinaya_wrong_link(content):
        # 替换整个"相关文献"部分
        related_start = content.find('## 相關文献')
        if related_start == -1:
            related_start = content.find('## 相关文献')
        if related_start == -1:
            related_start = content.find('## 相關文獻')
        if related_start >= 0:
            # 找到下一个 --- 或文件结尾
            related_end = content.find('\n---', related_start)
            if related_end == -1:
                related_end = len(content)
            old_related = content[related_start:related_end]
            new_related = get_correct_related_links(dirname).strip()
            content = content[:related_start] + new_related + content[related_end:]
    
    # 修复旧格式链接
    original = content
    content = fix_old_links(content, dirname)
    
    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"共修复 {count} 个文件")
