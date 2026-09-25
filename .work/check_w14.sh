#!/bin/bash
# 校验：净汉字数 + 禁用句式 + 反引号目录名存在性
BANNED=('本文獻' '教義精要：' '詳細考證成書年代' '[漢譯信息]')
for d in $(cat /mnt/openclaw/catdesk/home/佛法/.work/w14_d.txt); do
  base="/mnt/openclaw/catdesk/home/佛法/文献档案/$d"
  for f in 解讀_學術.md 解讀_白話.md; do
    file="$base/$f"
    n=$(grep -oP '[\x{4e00}-\x{9fff}]' "$file" | wc -l)
    bad=""
    for b in "${BANNED[@]}"; do grep -qF "$b" "$file" && bad="$bad [$b]"; done
    # 反引号目录名校验
    miss=$(grep -oP '(?<=`)`?' "$file" >/dev/null; grep -oP '`[^`]+`' "$file" | sed 's/`//g' | while read t; do [ -d "/mnt/openclaw/catdesk/home/佛法/文献档案/$t" ] || echo "$t"; done | tr '\n' ' ')
    flag=""
    [ "$n" -lt 1000 ] && flag="${flag} 少于1000"
    [ -n "$bad" ] && flag="${flag} 禁语:$bad"
    [ -n "$miss" ] && flag="${flag} 目录不存在:$miss"
    [ -z "$flag" ] && st="OK" || st="FAIL:$flag"
    echo "$d/$f 净汉字=$n $st"
  done
done
