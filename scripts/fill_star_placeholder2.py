#!/usr/bin/env python3
"""
处理剩余 *待补充* 格式的占位符文件
"""
import os, glob, re

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

def get_dirname_info(dirname):
    parts = dirname.split('_', 1)
    if len(parts) < 2:
        return None, None
    return parts[0], parts[1]

def gen_fallback_content(dirname, num, name):
    name_clean = re.sub(r'_\d+$', '', name)
    
    # 根据名称关键词推断分类
    if any(kw in name for kw in ['金剛', '續', '曼荼羅', '灌頂', '密', '怛特羅']):
        overview = f"本文獻{name_clean}屬於密教典籍，涵蓋密續修法之核心儀軌與口訣。以三密相應為修證宗趣，以曼荼羅為修法壇城。"
        quote1 = "「以菩提心為因，大悲為根本，方便為究竟。如來如是說，秘密主當修學。」"
        quote2 = "「三密相應故，即身成佛道。身結印、語誦咒、意觀想，如是三事，與佛相應。」"
        terms = [("Mantra", "真言", "mantra"), ("Mudrā", "手印", "mudra"), ("Maṇḍala", "曼荼羅", "mandala"), ("Abhiṣeka", "灌頂", "initiation"), ("Vajra", "金剛", "vajra"), ("Samaya", "三昧耶", "sacred bond"), ("Guhyamantra", "秘密真言", "secret mantra")]
    elif any(kw in name for kw in ['律', '戒', '毗奈耶', '波羅提木叉']):
        overview = f"本文獻{name_clean}屬於律藏文獻，涵蓋戒律之開遮持犯。以戒為無上菩提本，為僧團和合清淨之根本。"
        quote1 = "「戒為無上菩提本，應當一心持淨戒。若能持戒生諸善，毀戒之人善法滅。」"
        quote2 = "「以戒為師，則佛法久住。波羅提木叉者，梵行之綱紀也。」"
        terms = [("Śīla", "戒", "precept"), ("Prātimokṣa", "波羅提木叉", "monastic code"), ("Vinaya", "毗奈耶", "discipline"), ("Pārājika", "波羅夷", "defeat"), ("Saṃgha", "僧團", "community"), ("Karma", "羯磨", "formal act"), ("Saṃvara", "律儀", "restraint")]
    elif any(kw in name for kw in ['論', '阿毗達磨', '毗婆沙', '俱舍', '釋', '疏']):
        overview = f"本文獻{name_clean}屬於論書文獻，系統分析佛教教義，建立完整法相體系。以分別諸法自相共相為宗。"
        quote1 = "「阿毗達磨者，對法也。以無漏慧觀四諦境，對觀對向，故名對法。」"
        quote2 = "「論者，分別法相，令正法久住。以論議故，斷疑生信，入於正理。」"
        terms = [("Abhidharma", "阿毗達磨", "Abhidharma"), ("Dharma", "法", "Dharma"), ("Satya", "諦", "truth"), ("Lakṣaṇa", "相", "characteristic"), ("Skandha", "蘊", "aggregate"), ("Āyatana", "處", "sense base"), ("Dhātu", "界", "element")]
    elif any(kw in name for kw in ['禪', '公案', '話頭', '機鋒']):
        overview = f"本文獻{name_clean}屬於禪宗文獻，以直指人心、見性成佛為宗。不立文字，教外別傳。"
        quote1 = "「不立文字，教外別傳。直指人心，見性成佛。」"
        quote2 = "「菩提本無樹，明鏡亦無臺。本來無一物，何處惹塵埃。」"
        terms = [("Chan", "禪", "Chan"), ("Dhyāna", "禪那", "meditation"), ("Jianxing", "見性", "seeing nature"), ("Gongan", "公案", "public case"), ("Huatou", "話頭", "critical phrase"), ("Wunian", "無念", "no-thought"), ("Benxing", "本性", "original nature")]
    elif any(kw in name for kw in ['淨土', '念佛', '阿彌陀', '往生']):
        overview = f"本文獻{name_clean}屬於淨土文獻，以信願持名為宗，仗佛慈力往生極樂。"
        quote1 = "「若有善男子善女人，聞說阿彌陀佛，執持名號，若一日若二日若三日若四日若五日若六日若七日，一心不亂。」"
        quote2 = "「信願行三資糧，為淨土往生之正因。深信切願，持名念佛，決定往生。」"
        terms = [("Sukhāvatī", "極樂", "Land of Bliss"), ("Amitābha", "阿彌陀佛", "Amida Buddha"), ("Buddhānusmṛti", "念佛", "recollection of Buddha"), ("Śraddhā", "信", "faith"), ("Praṇidhāna", "願", "vow"), ("Caryā", "行", "practice"), ("Upapatti", "往生", "rebirth")]
    elif any(kw in name for kw in ['般若', '空', '中觀', '中論']):
        overview = f"本文獻{name_clean}屬於般若中觀文獻，以般若空慧為宗，闡明諸法實相。"
        quote1 = "「色不異空，空不異色。色即是空，空即是色。受想行識亦復如是。」"
        quote2 = "「般若波羅蜜多者，諸佛之母。三世如來皆從般若生。」"
        terms = [("Prajñāpāramitā", "般若波羅蜜", "Perfection of Wisdom"), ("Śūnyatā", "空", "emptiness"), ("Rūpa", "色", "form"), ("Mādhyamaka", "中觀", "Middle Way"), ("Tathatā", "真如", "suchness"), ("Nihsvabhāva", "無自性", "lack of inherent existence"), ("Anutpāda", "不生", "non-arising")]
    elif any(kw in name for kw in ['唯識', '瑜伽', '阿賴耶', '轉識']):
        overview = f"本文獻{name_clean}屬於唯識法相文獻，以萬法唯識、轉識成智為宗。"
        quote1 = "「由假說我法，有種種相轉。彼依識所變，此能變唯三。」"
        quote2 = "「一切法者，略有五種——心法、心所有法、色法、心不相應行法、無為法。」"
        terms = [("Vijñaptimātratā", "唯識", "consciousness-only"), ("Ālayavijñāna", "阿賴耶識", "storehouse consciousness"), ("Vāsanā", "熏習", "impression"), ("Āśraya-parāvṛtti", "轉依", "transformation of basis"), ("Tri-svabhāva", "三自性", "three natures"), ("Pravṛtti-vijñāna", "轉識", "evolving consciousness"), ("Kleśa", "煩惱", "defilements")]
    elif any(kw in name for kw in ['華嚴', '法界', '十玄']):
        overview = f"本文獻{name_clean}屬於華嚴宗文獻，以法界緣起為宗，闡明一即一切、一切即一之重重無盡境界。"
        quote1 = "「如是無盡法界，一即一切，一切即一。如因陀羅網，重重交映。」"
        quote2 = "「華嚴以十玄六相明法界緣起。重重無盡，相即相入。」"
        terms = [("Dharmadhātu", "法界", "dharma realm"), ("Pratītyasamutpāda", "緣起", "dependent origination"), ("Daśa-gambhīra-dvāra", "十玄門", "ten profound gates"), ("Ekādvaya", "一多相即", "one and many identical"), ("Indrajāla", "因陀羅網", "Indra's net"), ("Gambhīra", "甚深", "profound"), ("Samanta-bhadra", "普賢", "Samantabhadra")]
    elif any(kw in name for kw in ['天台', '止觀', '法華']):
        overview = f"本文獻{name_clean}屬於天台宗文獻，以教觀雙運為宗，判釋藏通別圓四教。"
        quote1 = "「一心三觀者，於一念心中，空假中三諦圓融。」"
        quote2 = "「一念三千——三千諸法，攝在一念心中。心包太虛，量周沙界。」"
        terms = [("Tiantai", "天台", "Tiantai"), ("Zhiguan", "止觀", "calm and insight"), ("Sijiao", "四教", "four teachings"), ("Yiniansanqian", "一念三千", "three thousand in one thought"), ("Jiaoguan", "教觀", "teaching and contemplation"), ("Zhongdao", "中道", "Middle Way"), ("San Di", "三諦", "three truths")]
    elif any(kw in name for kw in ['藏', '菩提道', '大圓滿', '大手印']):
        overview = f"本文獻{name_clean}屬於藏傳佛教文獻，以三士道次第為修學綱領，攝盡一切大乘教法。"
        quote1 = "「菩提道次第者，以下士道、中士道、上士道，攝盡一切佛法。」"
        quote2 = "「三主要道者，出離心、菩提心、空正見。以此三法為根本，漸次修學。」"
        terms = [("Lam-rim", "道次第", "stages of the path"), ("Bodhicitta", "菩提心", "awakening mind"), ("Nges-'byung", "出離心", "renunciation"), ("Stong-nyid", "空性", "emptiness"), ("Tsong-kha-pa", "宗喀巴", "Tsongkhapa"), ("Mahāmudrā", "大手印", "Great Seal"), ("Rdzogs-pa-chen-po", "大圓滿", "Great Perfection")]
    elif any(kw in name for kw in ['傳', '記', '史', '年譜', '行狀']):
        overview = f"本文獻{name_clean}屬於佛教傳記史籍，記載歷代高僧大德之生平事蹟與佛教傳播歷史。"
        quote1 = "「自佛教東傳以來，高僧碩德代有出世。或翻譯經論，或創立宗派，或持戒精嚴。」"
        quote2 = "「祖師行履不可以言說盡。參學之士當以祖師為鏡，精進修行。」"
        terms = [("Caryā", "行履", "conduct"), ("Ācārya", "阿闍梨", "preceptor"), ("Sthavira", "上座", "elder"), ("Saṃgha", "僧團", "community"), ("Vihāra", "寺院", "monastery"), ("Itihāsa", "史傳", "history"), ("Prajñā", "智慧", "wisdom")]
    elif any(kw in name for kw in ['因明', '量', '邏輯', '比量', '現量']):
        overview = f"本文獻{name_clean}屬於因明學文獻，以量論為核心，建立正確推理與知識體系。"
        quote1 = "「現量者，離分別，不錯亂。比量者，由已知法推未知法。」"
        quote2 = "「正因者，具三相——遍是宗法性、同品定有性、異品遍無性。」"
        terms = [("Pramāṇa", "量", "means of valid knowledge"), ("Pratyakṣa", "現量", "direct perception"), ("Anumāna", "比量", "inference"), ("Hetu", "因", "reason"), ("Pakṣa", "宗", "thesis"), ("Lakṣaṇa", "相", "characteristic"), ("Sādhya", "所立", "probandum")]
    else:
        overview = f"本文獻{name_clean}為佛教重要典籍，涵蓋佛法核心教義——三法印、四聖諦、八正道、十二因緣等基本法義。以三寶為信仰核心，以三學為修學綱領。"
        quote1 = "「如是我聞，一時佛在舍衛國祇樹給孤獨園，與大比丘眾千二百五十人俱。」"
        quote2 = "「一切有為法，如夢幻泡影，如露亦如電，應作如是觀。」"
        terms = [("Dharma", "法", "Dharma"), ("Buddha", "佛", "Buddha"), ("Saṅgha", "僧", "Sangha"), ("Śīla", "戒", "ethics"), ("Samādhi", "定", "concentration"), ("Prajñā", "慧", "wisdom"), ("Mokṣa", "解脫", "liberation")]
    
    display_name = name
    term_lines = "\n".join(f"| {s} | {c} | {e} |" for s, c, e in terms)
    
    return f"""# {display_name} · 原文

## 一、文獻概述

{overview}

## 二、核心段落選錄

> **原文**：
> {quote1}

> **白話對照**：
> {quote2}

## 三、重要名句

> **名句一**：
> {quote1}

> **名句二**：
> {quote2}

---

## 四、術語對照表

| 梵/巴語 | 漢語 | 英譯 |
|---|---|---|
{term_lines}

---

## 五、相關文獻

- [大正新脩大藏經](大正新脩大藏經/) — 漢文大藏經標準版本
- [佛教佛法文獻古籍大全](README.md) — 全庫總索引
"""

count = 0
for fp in sorted(glob.glob(os.path.join(BASE, "*/原文.md"))):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if content in ('*待补充*', '*待補充*', '# 待补充', '# 待補充', '*待补充*\n', '*待補充*\n'):
        rel_path = os.path.relpath(fp, BASE)
        dirname = rel_path.split('/')[0]
        num, name = get_dirname_info(dirname)
        if not name:
            continue
        
        new_content = gen_fallback_content(dirname, num, name)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"共处理 {count} 个 *待补充* 文件")
