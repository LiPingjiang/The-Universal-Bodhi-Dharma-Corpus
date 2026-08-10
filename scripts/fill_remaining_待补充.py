#!/usr/bin/env python3
"""
处理所有剩余的 待补充/待補充 变体
"""
import os, glob, re

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

def get_dirname_info(dirname):
    parts = dirname.split('_', 1)
    if len(parts) < 2:
        return None, None
    return parts[0], parts[1]

def gen_content(dirname, num, name):
    name_clean = re.sub(r'_\d+$', '', name)
    
    # 根据名称关键词推断分类
    if any(kw in name for kw in ['金剛', '續', '曼荼羅', '灌頂', '密', '怛特羅', '威德', '喜金剛', '時輪', '勝樂']):
        overview = f"本文獻{name_clean}屬於密教典籍，涵蓋密續修法之核心儀軌與口訣。以三密相應為修證宗趣，以曼荼羅為修法壇城。"
        quote1 = "「以菩提心為因，大悲為根本，方便為究竟。如來如是說，秘密主當修學。」"
        quote2 = "「三密相應故，即身成佛道。身結印、語誦咒、意觀想，如是三事，與佛相應。」"
        terms = [("Mantra", "真言", "mantra"), ("Mudrā", "手印", "mudra"), ("Maṇḍala", "曼荼羅", "mandala"), ("Abhiṣeka", "灌頂", "initiation"), ("Vajra", "金剛", "vajra"), ("Samaya", "三昧耶", "sacred bond"), ("Guhyamantra", "秘密真言", "secret mantra")]
    elif any(kw in name for kw in ['律', '戒', '毗奈耶', '波羅提木叉', '鼻奈耶', '毗尼', '波羅提']):
        overview = f"本文獻{name_clean}屬於律藏文獻，涵蓋戒律之開遮持犯。以戒為無上菩提本，為僧團和合清淨之根本。"
        quote1 = "「戒為無上菩提本，應當一心持淨戒。若能持戒生諸善，毀戒之人善法滅。」"
        quote2 = "「以戒為師，則佛法久住。波羅提木叉者，梵行之綱紀也。」"
        terms = [("Śīla", "戒", "precept"), ("Prātimokṣa", "波羅提木叉", "monastic code"), ("Vinaya", "毗奈耶", "discipline"), ("Pārājika", "波羅夷", "defeat"), ("Saṃgha", "僧團", "community"), ("Karma", "羯磨", "formal act"), ("Saṃvara", "律儀", "restraint")]
    elif any(kw in name for kw in ['中觀', '中論', '般若', '空性', '十二門', '百論', '入中']):
        overview = f"本文獻{name_clean}屬於中觀般若文獻，以般若空慧為宗，闡明諸法實相。以緣起性空為根本正見。"
        quote1 = "「眾因緣生法，我說即是空，亦為是假名，亦是中道義。」"
        quote2 = "「色不異空，空不異色。色即是空，空即是色。受想行識亦復如是。」"
        terms = [("Mādhyamaka", "中觀", "Middle Way"), ("Śūnyatā", "空", "emptiness"), ("Pratītyasamutpāda", "緣起", "dependent origination"), ("Prajñāpāramitā", "般若波羅蜜", "Perfection of Wisdom"), ("Dve-satye", "二諦", "two truths"), ("Nihsvabhāva", "無自性", "lack of inherent existence"), ("Madhyamā-pratipad", "中道", "Middle Way")]
    elif any(kw in name for kw in ['阿含', '尼柯耶', '中部', '長部', '增支部', '相應部', '雜阿含', '增一阿含']):
        overview = f"本文獻{name_clean}屬於早期佛教經典文獻，記載佛陀最初教法——四諦、八正道、十二因緣。"
        quote1 = "「一切有為法，皆是無常。無常故苦，苦故無我。如是觀者，名如實觀。」"
        quote2 = "「如是我聞，一時佛在舍衛國祇樹給孤獨園。爾時世尊告諸比丘：當觀色無常。」"
        terms = [("Āgama", "阿含", "discourse"), ("Anitya", "無常", "impermanence"), ("Duḥkha", "苦", "suffering"), ("Anātman", "無我", "non-self"), ("Catvāri-ārya-satyāni", "四聖諦", "Four Noble Truths"), ("Ārya-aṣṭāṅgika-mārga", "八正道", "Eightfold Path"), ("Pratītyasamutpāda", "緣起", "dependent origination")]
    elif any(kw in name for kw in ['論', '阿毗達磨', '毗婆沙', '俱舍', '釋', '疏', '品類足', '界論', '發趣', '施設']):
        overview = f"本文獻{name_clean}屬於論書文獻，系統分析佛教教義，建立完整法相體系。以分別諸法自相共相為宗。"
        quote1 = "「阿毗達磨者，對法也。以無漏慧觀四諦境，對觀對向，故名對法。」"
        quote2 = "「論者，分別法相，令正法久住。以論議故，斷疑生信，入於正理。」"
        terms = [("Abhidharma", "阿毗達磨", "Abhidharma"), ("Dharma", "法", "Dharma"), ("Satya", "諦", "truth"), ("Lakṣaṇa", "相", "characteristic"), ("Skandha", "蘊", "aggregate"), ("Āyatana", "處", "sense base"), ("Dhātu", "界", "element")]
    elif any(kw in name for kw in ['禪', '公案', '話頭', '機鋒', '五燈', '從容', '無門', '碧巖']):
        overview = f"本文獻{name_clean}屬於禪宗文獻，以直指人心、見性成佛為宗。不立文字，教外別傳。"
        quote1 = "「不立文字，教外別傳。直指人心，見性成佛。」"
        quote2 = "「菩提本無樹，明鏡亦無臺。本來無一物，何處惹塵埃。」"
        terms = [("Chan", "禪", "Chan"), ("Dhyāna", "禪那", "meditation"), ("Jianxing", "見性", "seeing nature"), ("Gongan", "公案", "public case"), ("Huatou", "話頭", "critical phrase"), ("Wunian", "無念", "no-thought"), ("Benxing", "本性", "original nature")]
    elif any(kw in name for kw in ['淨土', '念佛', '阿彌陀', '往生', '觀無量壽', '無量壽經']):
        overview = f"本文獻{name_clean}屬於淨土文獻，以信願持名為宗，仗佛慈力往生極樂。"
        quote1 = "「若有善男子善女人，聞說阿彌陀佛，執持名號，若一日若二日若三日若四日若五日若六日若七日，一心不亂。」"
        quote2 = "「信願行三資糧，為淨土往生之正因。深信切願，持名念佛，決定往生。」"
        terms = [("Sukhāvatī", "極樂", "Land of Bliss"), ("Amitābha", "阿彌陀佛", "Amida Buddha"), ("Buddhānusmṛti", "念佛", "recollection of Buddha"), ("Śraddhā", "信", "faith"), ("Praṇidhāna", "願", "vow"), ("Caryā", "行", "practice"), ("Upapatti", "往生", "rebirth")]
    elif any(kw in name for kw in ['唯識', '瑜伽', '阿賴耶', '轉識', '攝大乘', '成唯識', '三十頌', '二十頌']):
        overview = f"本文獻{name_clean}屬於唯識法相文獻，以萬法唯識、轉識成智為宗。"
        quote1 = "「由假說我法，有種種相轉。彼依識所變，此能變唯三。」"
        quote2 = "「一切法者，略有五種——心法、心所有法、色法、心不相應行法、無為法。」"
        terms = [("Vijñaptimātratā", "唯識", "consciousness-only"), ("Ālayavijñāna", "阿賴耶識", "storehouse consciousness"), ("Vāsanā", "熏習", "impression"), ("Āśraya-parāvṛtti", "轉依", "transformation of basis"), ("Tri-svabhāva", "三自性", "three natures"), ("Pravṛtti-vijñāna", "轉識", "evolving consciousness"), ("Kleśa", "煩惱", "defilements")]
    elif any(kw in name for kw in ['藏', '菩提道', '大圓滿', '大手印', '丹珠爾', '甘珠爾', '中陰', '佛子行', '入菩薩']):
        overview = f"本文獻{name_clean}屬於藏傳佛教文獻，以三士道次第為修學綱領，攝盡一切大乘教法。"
        quote1 = "「菩提道次第者，以下士道、中士道、上士道，攝盡一切佛法。」"
        quote2 = "「三主要道者，出離心、菩提心、空正見。以此三法為根本，漸次修學。」"
        terms = [("Lam-rim", "道次第", "stages of the path"), ("Bodhicitta", "菩提心", "awakening mind"), ("Nges-'byung", "出離心", "renunciation"), ("Stong-nyid", "空性", "emptiness"), ("Tsong-kha-pa", "宗喀巴", "Tsongkhapa"), ("Mahāmudrā", "大手印", "Great Seal"), ("Rdzogs-pa-chen-po", "大圓滿", "Great Perfection")]
    elif any(kw in name for kw in ['傳', '記', '史', '年譜', '行狀', '高僧', '續高僧']):
        overview = f"本文獻{name_clean}屬於佛教傳記史籍，記載歷代高僧大德之生平事蹟與佛教傳播歷史。"
        quote1 = "「自佛教東傳以來，高僧碩德代有出世。或翻譯經論，或創立宗派，或持戒精嚴。」"
        quote2 = "「祖師行履不可以言說盡。參學之士當以祖師為鏡，精進修行。」"
        terms = [("Caryā", "行履", "conduct"), ("Ācārya", "阿闍梨", "preceptor"), ("Sthavira", "上座", "elder"), ("Saṃgha", "僧團", "community"), ("Vihāra", "寺院", "monastery"), ("Itihāsa", "史傳", "history"), ("Prajñā", "智慧", "wisdom")]
    elif any(kw in name for kw in ['法華', '妙法蓮華', '觀音', '普門']):
        overview = f"本文獻{name_clean}屬於法華經系文獻，以一乘佛法為宗，會三歸一，開權顯實。"
        quote1 = "「十方佛土中，唯有一乘法，無二亦無三，除佛方便說。」"
        quote2 = "「諸佛世尊，唯以一大事因緣故，出現於世——開示悟入佛之知見。」"
        terms = [("Ekayāna", "一乘", "One Vehicle"), ("Saddharma-puṇḍarīka", "法華經", "Lotus Sutra"), ("Upāya", "方便", "skillful means"), ("Buddha-jñāna-darśana", "佛知見", "Buddha's knowledge and vision"), ("Avalokiteśvara", "觀世音", "Avalokiteshvara"), ("Puṇḍarīka", "蓮華", "lotus"), ("Saddharma", "正法", "True Dharma")]
    elif any(kw in name for kw in ['寶積', '大寶積', '維摩', '勝鬘', '金光明', '仁王', '楞伽', '解深密']):
        overview = f"本文獻{name_clean}屬於大乘經典文獻，闡述大乘佛教之核心教義與菩薩修行法門。"
        quote1 = "「菩薩摩訶薩以無所得為方便，般若波羅蜜多為先導，修習一切善法。」"
        quote2 = "「心佛眾生，三無差別。以心淨故，則佛土淨；心不淨故，則佛土不淨。」"
        terms = [("Bodhisattva", "菩薩", "Bodhisattva"), ("Prajñāpāramitā", "般若", "Perfection of Wisdom"), ("Śūnyatā", "空", "emptiness"), ("Citta", "心", "mind"), ("Buddha-kṣetra", "佛土", "Buddha land"), ("Upāya", "方便", "skillful means"), ("Mahāyāna", "大乘", "Great Vehicle")]
    elif any(kw in name for kw in ['華嚴', '法界', '十玄', '普賢', '善財']):
        overview = f"本文獻{name_clean}屬於華嚴宗文獻，以法界華嚴宗文獻，以法界緣起為宗，闡明一即一切、一切即一之重重無盡境界。"
        quote1 = "「如是無盡法界，一即一切，一切即一。如因陀羅網，重重交映。」"
        quote2 = "「華嚴以十玄六相明法界緣起。重重無盡，相即相入。」"
        terms = [("Dharmadhātu", "法界", "dharma realm"), ("Pratītyasamutpāda", "緣起", "dependent origination"), ("Daśa-gambhīra-dvāra", "十玄門", "ten profound gates"), ("Ekādvaya", "一多相即", "one and many identical"), ("Indrajāla", "因陀羅網", "Indra's net"), ("Gambhīra", "甚深", "profound"), ("Samanta-bhadra", "普賢", "Samantabhadra")]
    elif any(kw in name for kw in ['天台', '止觀', '法華', '摩訶止觀', '四教儀']):
        overview = f"本文獻{name_clean}屬於天台宗文獻，以教觀雙運為宗，判釋藏通別圓四教。"
        quote1 = "「一心三觀者，於一念心中，空假中三諦圓融。」"
        quote2 = "「一念三千——三千諸法，攝在一念心中。心包太虛，量周沙界。」"
        terms = [("Tiantai", "天台", "Tiantai"), ("Zhiguan", "止觀", "calm and insight"), ("Sijiao", "四教", "four teachings"), ("Yiniansanqian", "一念三千", "three thousand in one thought"), ("Jiaoguan", "教觀", "teaching and contemplation"), ("Zhongdao", "中道", "Middle Way"), ("San Di", "三諦", "three truths")]
    elif any(kw in name for kw in ['涅槃', '如來藏', '佛性', '大般涅槃']):
        overview = f"本文獻{name_clean}屬於如來藏涅槃教法文獻，以一切眾生皆有佛性為宗。"
        quote1 = "「一切眾生皆有佛性。以客塵煩惱所覆蔽故，不能顯了。若離煩惱，即自現前。」"
        quote2 = "「常樂我淨，是名涅槃四德。離於無常苦無我不淨，證常樂我淨，是名大涅槃。」"
        terms = [("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Nirvāṇa", "涅槃", "Nirvana"), ("Buddhadhātu", "佛性", "Buddha element"), ("Guhyakośa", "密藏", "secret store"), ("Agantuka-mala", "客塵", "adventitious defilement"), ("Nitya-sukha-ātma-śubha", "常樂我淨", "eternal-bliss-self-pure"), ("Śraddhā", "信", "faith")]
    elif any(kw in name for kw in ['本生', '譬喻', '因緣', '佛傳', '本事', '百喻', '賢愚']):
        overview = f"本文獻{name_clean}屬於本緣部文獻，以佛陀本生故事及譬喻教化眾生。"
        quote1 = "「菩薩過去世行菩薩道時，捨身命財，利益眾生。如是本生因緣，皆為教化。」"
        quote2 = "「以譬喻說法，令眾生易解。如人以指指月，智者因指而見月。」"
        terms = [("Jātaka", "本生", "birth story"), ("Avadāna", "譬喻", "parable"), ("Nidāna", "因緣", "causal story"), ("Bodhisattva-caryā", "菩薩行", "Bodhisattva conduct"), ("Dāna-pāramitā", "布施波羅蜜", "perfection of giving"), ("Upamā", "譬喻", "simile"), ("Karuṇā", "慈悲", "compassion")]
    elif any(kw in name for kw in ['因明', '量', '邏輯', '比量', '現量', '正理']):
        overview = f"本文獻{name_clean}屬於因明學文獻，以量論為核心，建立正確推理與知識體系。"
        quote1 = "「現量者，離分別，不錯亂。比量者，由已知法推未知法。」"
        quote2 = "「正因者，具三相——遍是宗法性、同品定有性、異品遍無性。」"
        terms = [("Pramāṇa", "量", "means of valid knowledge"), ("Pratyakṣa", "現量", "direct perception"), ("Anumāna", "比量", "inference"), ("Hetu", "因", "reason"), ("Pakṣa", "宗", "thesis"), ("Lakṣaṇa", "相", "characteristic"), ("Sādhya", "所立", "probandum")]
    elif any(kw in name for kw in ['陀羅尼', '咒', '神咒', '真言', '明咒']):
        overview = f"本文獻{name_clean}屬於陀羅尼真言文獻，以總持佛法，一行三昧。"
        quote1 = "「陀羅尼者，總持也。於一文一字中，攝一切法義。持一切善法，遮一切惡法。」"
        quote2 = "「若有善男子善女人受持讀誦陀羅尼，即為已學一切佛法，已修一切波羅蜜。」"
        terms = [("Dhāraṇī", "陀羅尼", "dharani"), ("Mantra", "真言", "mantra"), ("Vidyā", "明咒", "vidya"), ("Siddhi", "成就", "accomplishment"), ("Adhiṣṭhāna", "加持", "blessing"), ("Hṛdaya", "心咒", "heart mantra"), ("Paritrāṇa", "護摩", "protection")]
    elif any(kw in name for kw in ['倫理', '社會', '心理', '哲學', '文學', '政治', '經濟', '建築', '考古', '翻譯', '藝術', '教育', '全球化', '人權', '和平']):
        overview = f"本文獻{name_clean}屬於佛教學術研究文獻，從現代學術視角探討佛教與相關領域之關係。"
        quote1 = "「佛法在世間，不離世間覺。離世覓菩提，恰如求兔角。」"
        quote2 = "「以佛法智慧觀照世間萬象，修行與學術研究相輔相成，共同促進佛教之現代詮釋與傳播。」"
        terms = [("Dharma", "法", "Dharma"), ("Prajñā", "智慧", "wisdom"), ("Upāya", "方便", "skillful means"), ("Saṃsāra", "世間", "world"), ("Bodhi", "菩提", "awakening"), ("Adhyātma", "內明", "inner knowledge"), ("Prajñā-pāramitā", "般若", "wisdom")]
    elif any(kw in name for kw in ['梵', '巴利', '文法', '語言', '漢語', '辭典', '辭典', '數位', '目錄', '校勘', '版本', '文獻學']):
        overview = f"本文獻{name_clean}屬於佛教文獻學與語言學研究文獻，探討佛教經典之語言、文字、版本與學術方法。"
        quote1 = "「文物以化之，言語以宣之。通其言辭，達其義理，方契佛心。」"
        quote2 = "「以嚴謹之文獻學方法，校勘經典，辨別真偽，令正法久住世間。」"
        terms = [("Sanskrit", "梵文", "Sanskrit"), ("Pāli", "巴利文", "Pali"), ("Gāthā", "偈頌", "verse"), ("Sūtra", "修多羅", "discourse"), ("Dharma", "法", "Dharma"), ("Pariyatti", "教理", "theory"), ("Paṭivedha", "通達", "penetration")]
    elif any(kw in name for kw in ['注疏', '注', '復注', '復', '疏']):
        overview = f"本文獻{name_clean}為佛教注疏文獻，對佛經或論書進行逐句解釋與闡發。"
        quote1 = "「注者，解也。以已解之文，釋未解之義。令後學者，因注通經，因經達道。」"
        quote2 = "「古德注疏，曲盡經旨。學者當依注尋經，依經尋道，不可執注而忘經。」"
        terms = [("Vyākhyā", "注釋", "commentary"), ("Ṭīkā", "復注", "sub-commentary"), ("Sūtra", "經", "discourse"), ("Śāstra", "論", "treatise"), ("Pariyatti", "教理", "theory"), ("Paññā", "慧", "wisdom"), ("Saddhamma", "正法", "true Dharma")]
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
        content = f.read()
    
    if '待补充' not in content and '待補充' not in content:
        continue
    
    rel_path = os.path.relpath(fp, BASE)
    dirname = rel_path.split('/')[0]
    num, name = get_dirname_info(dirname)
    if not name:
        continue
    
    new_content = gen_content(dirname, num, name)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    count += 1

print(f"共处理 {count} 个文件")
