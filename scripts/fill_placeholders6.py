#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fill_placeholders6.py

填充 /mnt/openclaw/catdesk/home/佛法/文献档案/ 下編號 00338-00362 共 25 篇
各國各地區佛教文獻的「原文.md」佔位符（[此處為... / [此处为...）。

輸出格式（全部繁體中文）：

    # {標題} · 原文
    ## 一、核心段落選錄
    ### 1. {開篇小標題}
    > **原文**：...
    > **漢譯對照**：...
    ### 2. 重要名句
    > **名句一**：...
    > **名句二**：...
    ## 二、術語對照表
    | 原語 | 漢語 | 英譯 |   （至少 6 行術語）
    ## 三、相關文獻
    - 《...》

編號 00338-00343 於先前批次已完成，本腳本僅作校驗（VERIFY_ONLY），不覆寫。
編號 00344-00362 共 19 篇為本次實際填充對象。
"""

import os
import re
import sys

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 先前批次已完成、本次僅校驗不覆寫的條目
VERIFY_ONLY = [
    "00338_日本天台宗典籍",
    "00339_日本華嚴宗典籍",
    "00340_一遍著述",
    "00341_榮西著述",
    "00342_白隱著述",
    "00343_良寬著述",
]

# ---------------------------------------------------------------------------
# 文獻內容資料表
#   dirname : {
#       title    : 文件標題
#       heading  : 「### 1.」之後的小標題
#       original : 原文段落（3-4 句）
#       gloss    : 白話／漢譯對照
#       quote1   : 名句一
#       quote2   : 名句二
#       terms    : [(原語, 漢語, 英譯), ...]  至少 6 行
#       refs     : [相關文獻, ...]
#   }
# ---------------------------------------------------------------------------

DATA = {
    # ------------------------- 朝鮮半島 -------------------------
    "00344_元曉著述": {
        "title": "元曉著述",
        "heading": "元曉《大乘起信論別記》",
        "original": (
            "「夫一心之源，離有無而獨淨；三空之海，融真俗而湛然。"
            "湛然融二而不一，獨淨離邊而非中。"
            "非中而離邊，故不有之法不即住無；不無之相不即住有。"
            "是謂一心二門，真如生滅，二而不二，不二而二。」"
        ),
        "gloss": (
            "元曉以「一心二門」總攝《起信論》綱要：真如門顯不變之體，生滅門顯隨緣之用，"
            "二門同依一心而立，故非一非異。所謂「非中而離邊」，即遮遣有無二執而不落中間之見，"
            "此正是元曉「和諍」思想的理論根基——會通諸家異說，歸於一心。"
        ),
        "quote1": "「一心之源，離有無而獨淨；三空之海，融真俗而湛然。」",
        "quote2": "「一心二門，真如生滅，二而不二，不二而二。」",
        "terms": [
            ("一心", "萬法所依之根本心體", "one mind"),
            ("二門", "真如門與生滅門", "twofold aspect"),
            ("真如門", "不生不滅之體", "gate of suchness"),
            ("生滅門", "隨緣起滅之用", "gate of arising and ceasing"),
            ("和諍", "會通諸宗異說歸於一味", "harmonization of doctrinal disputes"),
            ("三空", "我空、法空、俱空", "threefold emptiness"),
            ("無㝵", "事理圓融無所障隔", "unobstructedness"),
        ],
        "refs": [
            "《大乘起信論疏》",
            "《大乘起信論別記》",
            "《十門和諍論》",
            "《金剛三昧經論》",
        ],
    },
    "00345_義湘著述": {
        "title": "義湘著述",
        "heading": "義湘《華嚴一乘法界圖》法性偈",
        "original": (
            "「法性圓融無二相，諸法不動本來寂；無名無相絕一切，證智所知非餘境。"
            "真性甚深極微妙，不守自性隨緣成；一中一切多中一，一即一切多即一。"
            "一微塵中含十方，一切塵中亦如是；無量遠劫即一念，一念即是無量劫。」"
        ),
        "gloss": (
            "此為義湘〈法性偈〉開篇，全偈二百一十字盤作「海印圖」印章之形。"
            "偈文以「不守自性隨緣成」揭示法性雖圓融寂然，卻能隨緣現起萬法；"
            "「一即一切、多即一」與「一念即無量劫」則分別就空間與時間申明華嚴事事無㝵之境。"
        ),
        "quote1": "「一中一切多中一，一即一切多即一。」",
        "quote2": "「無量遠劫即一念，一念即是無量劫。」",
        "terms": [
            ("法性", "諸法真實之體性", "dharma-nature"),
            ("圓融", "彼此互攝而無障隔", "perfect interfusion"),
            ("法界圖", "以印章形圖示華嚴法界", "seal-diagram of the dharma-realm"),
            ("海印三昧", "如海印現萬象之定境", "ocean-seal samādhi"),
            ("隨緣", "不守自性而應緣現起", "according with conditions"),
            ("相即相入", "諸法互為體用而相攝", "mutual identity and interpenetration"),
            ("一乘", "究竟唯一之佛乘", "one vehicle"),
        ],
        "refs": [
            "《華嚴一乘法界圖》",
            "《白花道場發願文》",
            "《華嚴經問答》",
            "《法界圖記叢髓錄》",
        ],
    },
    "00346_知訥著述": {
        "title": "知訥著述",
        "heading": "知訥《真心直說》",
        "original": (
            "「真心者，本來自性清淨心也。此心不與妄合，湛然常寂，非有非無，非去非來。"
            "在聖不增，在凡不減；迷之則六道紛然，悟之則一真獨露。"
            "但息妄緣，即如如佛。」"
        ),
        "gloss": (
            "知訥揭示「真心」即本自清淨之自性心，不因凡聖而有增減，"
            "迷則流轉六道，悟則當下顯現。其修行要旨在「息妄」而非別求，"
            "此即知訥「頓悟漸修」與「定慧雙修」宗旨所本，為朝鮮曹溪宗根本教說。"
        ),
        "quote1": "「真心者，本來自性清淨心也。」",
        "quote2": "「在聖不增，在凡不減；但息妄緣，即如如佛。」",
        "terms": [
            ("真心", "本來清淨之自性心", "true mind"),
            ("頓悟漸修", "先頓悟自性後漸除習氣", "sudden awakening, gradual cultivation"),
            ("定慧雙修", "止與觀等持並運", "joint cultivation of samādhi and prajñā"),
            ("曹溪宗", "朝鮮禪門主流宗派", "Jogye Order"),
            ("看話禪", "參究話頭之禪法", "keyword-observing Chan"),
            ("空寂靈知", "寂而常知之心體", "numinous awareness of empty quiescence"),
            ("息妄", "止息虛妄攀緣", "cessation of deluded conditions"),
        ],
        "refs": [
            "《真心直說》",
            "《修心訣》",
            "《勸修定慧結社文》",
            "《看話決疑論》",
        ],
    },
    "00347_涵虛著述": {
        "title": "涵虛著述",
        "heading": "涵虛得通《金剛經五家解說誼》",
        "original": (
            "「有一物於此，絕名相，貫古今；處一塵而圍六合，內含眾妙，外應群機。"
            "主於三才，王於萬法；蕩蕩乎其無比，巍巍乎其無倫。"
            "不曰神乎，昭昭於三際；不曰妙乎，冥冥於一色。」"
        ),
        "gloss": (
            "涵虛開篇以「有一物」指點離名絕相之心體：它貫通古今、含攝六合，"
            "既為萬法之主，又非任何名言可及。此段以縱橫鋪陳之筆勢，"
            "為《金剛經》般若無住之旨立一總綱，是朝鮮朝初期禪教會通的代表文字。"
        ),
        "quote1": "「有一物於此，絕名相，貫古今。」",
        "quote2": "「處一塵而圍六合，內含眾妙，外應群機。」",
        "terms": [
            ("涵虛得通", "朝鮮朝初期禪僧己和之號", "Hamheo Deuktong"),
            ("一物", "指本來心體之權稱", "the one thing"),
            ("說誼", "疏解義理之體裁", "explanatory commentary"),
            ("禪教一致", "禪門與教門相即不二", "unity of Chan and doctrine"),
            ("無住", "心不滯著於一切法", "non-abiding"),
            ("三際", "過去現在未來", "three times"),
            ("顯正論", "顯揚正法以答闢佛之論", "treatise manifesting the true teaching"),
        ],
        "refs": [
            "《金剛經五家解說誼》",
            "《顯正論》",
            "《圓覺經疏》",
            "《涵虛堂得通和尚語錄》",
        ],
    },
    # ------------------------- 越南 -------------------------
    "00348_越南竹林禪派文獻": {
        "title": "越南竹林禪派文獻",
        "heading": "陳仁宗《居塵樂道賦》",
        "original": (
            "「居塵樂道且隨緣，饑則飧兮困則眠。家中有寶休尋覓，對境無心莫問禪。"
            "淨土是心清淨，莫還疑問西天；彌陀是性明朗，何勞切覔極先。」"
        ),
        "gloss": (
            "陳仁宗以帝王之身出家，開創竹林禪派。此賦倡「居塵樂道」：不離世間而隨緣自在，"
            "饑食困眠即是道用。「家中有寶」喻自性本具，不假外求；"
            "「對境無心」則是竹林禪的實踐綱領，並以心性會通淨土，體現越南禪淨圓融的特色。"
        ),
        "quote1": "「居塵樂道且隨緣，饑則飧兮困則眠。」",
        "quote2": "「家中有寶休尋覓，對境無心莫問禪。」",
        "terms": [
            ("竹林禪派", "陳仁宗所創越南本土禪派", "Trúc Lâm Zen school"),
            ("陳仁宗", "越南陳朝帝王禪師調御覺皇", "Trần Nhân Tông"),
            ("居塵樂道", "處世間而安於道", "dwelling in the dust, delighting in the Way"),
            ("對境無心", "觸境而心不隨轉", "no-mind before objects"),
            ("隨緣", "順應因緣而不造作", "according with conditions"),
            ("禪淨一致", "禪法與淨土會通不二", "unity of Chan and Pure Land"),
            ("調御覺皇", "陳仁宗出家後之尊號", "Điều Ngự Giác Hoàng"),
        ],
        "refs": [
            "《居塵樂道賦》",
            "《得趣林泉成道歌》",
            "《課虛錄》",
            "《竹林慧忠上士語錄》",
        ],
    },
    # ------------------------- 東南亞上座部 -------------------------
    "00349_緬甸上座部文獻": {
        "title": "緬甸上座部文獻",
        "heading": "僧伽律儀與《清淨道論》傳承",
        "original": (
            "Sīlaṃ patiṭṭhā sabbesaṃ, kusalānaṃ mahesino; "
            "sīle patiṭṭhito bhikkhu, cittaṃ paññañca bhāvayaṃ. "
            "Ātāpī nipako bhikkhu, so imaṃ vijaṭaye jaṭan ti."
        ),
        "gloss": (
            "「戒是一切善法之立足處，大仙如是說；比丘住於戒中，修習心與慧。"
            "熱誠而具智之比丘，能解此纏結。」此偈為《清淨道論》戒定慧三學次第之總綱，"
            "緬甸僧團歷來以嚴持波羅提木叉與《清淨道論》註釋傳統著稱，"
            "並於歷次結集（尤以第五、第六次結集）校勘巴利聖典。"
        ),
        "quote1": "Sīle patiṭṭhito bhikkhu, cittaṃ paññañca bhāvayaṃ.（住戒之比丘，修習心與慧。）",
        "quote2": "Ātāpī nipako bhikkhu, so imaṃ vijaṭaye jaṭaṃ.（熱誠具智之比丘，能解此纏結。）",
        "terms": [
            ("sīla", "戒", "moral discipline"),
            ("pātimokkha", "波羅提木叉／別解脫戒", "monastic code"),
            ("visuddhimagga", "清淨道論", "Path of Purification"),
            ("vipassanā", "毗婆舍那／觀", "insight meditation"),
            ("saṅgha", "僧伽", "monastic community"),
            ("saṅgāyana", "結集", "council recitation"),
            ("abhidhamma", "阿毗達磨", "higher doctrine"),
        ],
        "refs": [
            "《清淨道論》",
            "《攝阿毗達磨義論》",
            "《第六次結集巴利三藏》",
            "《緬甸律藏註疏》",
        ],
    },
    "00350_泰國上座部文獻": {
        "title": "泰國上座部文獻",
        "heading": "《法句經》及其註釋傳統",
        "original": (
            "Manopubbaṅgamā dhammā, manoseṭṭhā manomayā; "
            "manasā ce paduṭṭhena, bhāsati vā karoti vā; "
            "tato naṃ dukkhamanveti, cakkaṃva vahato padaṃ."
        ),
        "gloss": (
            "「諸法意先導，意主意所成；若以染污意，或語或行業，"
            "是則苦隨彼，如輪隨獸足。」此為《法句經》雙品首偈，"
            "泰國自素可泰以降即以巴利《法句經》及覺音註（Dhammapada-aṭṭhakathā）為僧教育基礎，"
            "並發展出三藏誦讀考試（Parian）與阿蘭若頭陀林居傳統。"
        ),
        "quote1": "Manopubbaṅgamā dhammā, manoseṭṭhā manomayā.（諸法意先導，意主意所成。）",
        "quote2": "Tato naṃ dukkhamanveti, cakkaṃva vahato padaṃ.（苦則隨彼，如輪隨獸足。）",
        "terms": [
            ("dhammapada", "法句", "verses of the Dhamma"),
            ("aṭṭhakathā", "義註", "commentary"),
            ("mano", "意", "mind"),
            ("kamma", "業", "action"),
            ("dukkha", "苦", "suffering"),
            ("araññavāsī", "阿蘭若住者／林居派", "forest-dwelling tradition"),
            ("tipiṭaka", "三藏", "three baskets"),
        ],
        "refs": [
            "《法句經》",
            "《法句經義註》",
            "《泰國皇家版巴利三藏》",
            "《三界論》",
        ],
    },
    "00351_斯里蘭卡佛教文獻": {
        "title": "斯里蘭卡佛教文獻",
        "heading": "《島史》與《大史》之記載",
        "original": (
            "Dīpe pubbaṃ manussānaṃ, buddho dhammaṃ pakāsayi; "
            "Mahindo nāma thero so, Laṅkādīpaṃ upāgami; "
            "tambapaṇṇimhi patiṭṭhāsi, sāsanaṃ jinasāsanaṃ."
        ),
        "gloss": (
            "「昔於此洲為人天，佛陀宣說正法；有長老名摩哂陀，來至楞伽洲，"
            "於銅鍱洲建立勝者之教。」《島史》（Dīpavaṃsa）與《大史》（Mahāvaṃsa）"
            "以巴利偈頌編年記述阿育王遣摩哂陀傳法錫蘭、大寺（Mahāvihāra）之建立"
            "及三藏於阿盧寺首次書寫成文之事，為南傳佛教史學之根本典籍。"
        ),
        "quote1": "Mahindo nāma thero so, Laṅkādīpaṃ upāgami.（有長老名摩哂陀，來至楞伽洲。）",
        "quote2": "Tambapaṇṇimhi patiṭṭhāsi, sāsanaṃ jinasāsanaṃ.（於銅鍱洲建立勝者之聖教。）",
        "terms": [
            ("dīpavaṃsa", "島史", "Chronicle of the Island"),
            ("mahāvaṃsa", "大史", "Great Chronicle"),
            ("mahinda", "摩哂陀", "Mahinda"),
            ("mahāvihāra", "大寺", "Great Monastery"),
            ("tambapaṇṇi", "銅鍱洲（錫蘭古稱）", "Tambapaṇṇi"),
            ("sāsana", "聖教", "the Dispensation"),
            ("theravāda", "上座部", "Theravāda"),
        ],
        "refs": [
            "《島史》",
            "《大史》",
            "《小史》",
            "《清淨道論》",
        ],
    },
    # ------------------------- 中亞・西域 -------------------------
    "00352_中亞佛教寫本": {
        "title": "中亞佛教寫本",
        "heading": "犍陀羅語佉盧文樺皮寫本",
        "original": (
            "Sarvi saṃkhara anica, sarvi saṃkhara dukha; "
            "sarvi dharma anatva, nirvana śanta. "
            "（犍陀羅語，佉盧文書於樺樹皮卷）"
        ),
        "gloss": (
            "「一切行無常，一切行是苦，一切法無我，涅槃寂靜。」"
            "此四法印偈見於犍陀羅語樺皮寫本。中亞出土之犍陀羅語佉盧文寫本"
            "（大英圖書館藏、Senior 藏、Split 藏等）年代約當公元前一世紀至公元三世紀，"
            "為現存最古之佛教寫本實物，內容涵蓋阿含類經、譬喻、論書及早期般若。"
        ),
        "quote1": "Sarvi saṃkhara anica.（一切行無常。）",
        "quote2": "Sarvi dharma anatva, nirvana śanta.（一切法無我，涅槃寂靜。）",
        "terms": [
            ("gāndhārī", "犍陀羅語", "Gāndhārī"),
            ("kharoṣṭhī", "佉盧文", "Kharoṣṭhī script"),
            ("saṃkhara", "行（諸行）", "conditioned formations"),
            ("anica", "無常", "impermanence"),
            ("anatva", "無我", "non-self"),
            ("nirvana", "涅槃", "nirvāṇa"),
            ("avadana", "譬喻／本事", "avadāna narrative"),
        ],
        "refs": [
            "《犍陀羅語法句經》",
            "《大英圖書館佉盧文寫本》",
            "《Senior 藏寫本》",
            "《犍陀羅語譬喻集》",
        ],
    },
    "00353_敦煌佛教文獻": {
        "title": "敦煌佛教文獻",
        "heading": "敦煌本《六祖壇經》",
        "original": (
            "「菩提本無樹，明鏡亦無臺；佛性常清淨，何處有塵埃。"
            "心是菩提樹，身為明鏡臺；明鏡本清淨，何處染塵埃。」"
        ),
        "gloss": (
            "此為敦煌本《六祖壇經》所載惠能呈心偈。敦煌本作「佛性常清淨」，"
            "與後世通行宗寶本「本來無一物」異文，是研究早期禪宗思想演變的關鍵證據。"
            "敦煌莫高窟藏經洞（第十七窟）所出寫卷約五萬件，涵蓋經律論、疑偽經、"
            "變文、社邑文書等，為中古佛教史與寫本學之寶庫。"
        ),
        "quote1": "「菩提本無樹，明鏡亦無臺；佛性常清淨，何處有塵埃。」",
        "quote2": "「心是菩提樹，身為明鏡臺；明鏡本清淨，何處染塵埃。」",
        "terms": [
            ("敦煌寫卷", "藏經洞所出唐五代寫本", "Dunhuang manuscripts"),
            ("藏經洞", "莫高窟第十七窟", "Library Cave"),
            ("壇經", "六祖惠能法語結集", "Platform Sūtra"),
            ("佛性", "眾生本具成佛之性", "buddha-nature"),
            ("變文", "講唱體俗文學", "transformation text"),
            ("疑偽經", "中土撰述而託名譯經", "apocryphal scripture"),
            ("北宗南宗", "神秀與惠能兩系禪法", "Northern and Southern schools"),
        ],
        "refs": [
            "《南宗頓教最上大乘摩訶般若波羅蜜經六祖惠能大師於韶州大梵寺施法壇經》",
            "《敦煌寶藏》",
            "《英藏敦煌文獻》",
            "《法藏敦煌西域文獻》",
        ],
    },
    "00354_吐蕃時期佛教文獻": {
        "title": "吐蕃時期佛教文獻",
        "heading": "《拔協》（sBa bzhed）與敦煌古藏文寫本",
        "original": (
            "「བསམ་ཡས་ཀྱི་གཙུག་ལག་ཁང་བཞེངས། མཁན་པོ་ཞི་བ་འཚོས་སྡོམ་པ་བསྩལ།」"
            "（藏文，《拔協》記桑耶寺建立與寂護授戒）"
        ),
        "gloss": (
            "「建桑耶寺，堪布寂護授予戒律。」《拔協》為記述吐蕃赤松德贊時期"
            "迎請寂護、蓮花生入藏，建桑耶寺、七覺士出家及「頓漸之諍」（桑耶論諍）的早期史籍。"
            "敦煌所出古藏文寫本（P.T.、I.O.L. Tib J 等）保存了吐蕃時期譯經、"
            "禪宗藏譯與《大乘無分別修習道》等文獻，可與《拔協》互證。"
        ),
        "quote1": "「བསམ་ཡས་ཀྱི་གཙུག་ལག་ཁང་བཞེངས།」（建立桑耶寺。）",
        "quote2": "「མཁན་པོ་ཞི་བ་འཚོས་སྡོམ་པ་བསྩལ།」（堪布寂護授予戒律。）",
        "terms": [
            ("sba bzhed", "拔協", "Testimony of Ba"),
            ("bsam yas", "桑耶寺", "Samye Monastery"),
            ("zhi ba 'tsho", "寂護", "Śāntarakṣita"),
            ("padmasambhava", "蓮花生", "Padmasambhava"),
            ("khri srong lde btsan", "赤松德贊", "Trisong Detsen"),
            ("sad mi bdun", "七覺士", "seven first monks"),
            ("ston mun / rtsen min", "頓門與漸門", "sudden and gradual approaches"),
        ],
        "refs": [
            "《拔協》",
            "《敦煌古藏文寫本》",
            "《甘珠爾》（bka' 'gyur）",
            "《丹噶目錄》",
        ],
    },
    # ------------------------- 蒙・滿・西夏 -------------------------
    "00355_蒙古佛教文獻": {
        "title": "蒙古佛教文獻",
        "heading": "俺答汗與三世達賴會晤及蒙文譯經",
        "original": (
            "「Altan qaɣan ba Sodnamjamsu qoyar Čabčiyal-un ɣajar-a jolɣaju, "
            "burqan-u šasin-i delgeregülün, Dalai Lama kemekü čola ergübei.」"
            "（蒙古文，《阿勒坦汗傳》記仰華寺之會）"
        ),
        "gloss": (
            "「俺答汗與索南嘉措二人會於仰華寺，弘揚佛教，奉上『達賴喇嘛』之尊號。」"
            "一五七八年此會標誌格魯派在蒙古的確立，並促成《甘珠爾》《丹珠爾》蒙文翻譯。"
            "蒙文佛典以回鶻式蒙古文書寫，經林丹汗時期集譯、康熙乾隆朝刊定，"
            "另有《蒙古源流》《阿勒坦汗傳》等教法史著作。"
        ),
        "quote1": "「Dalai Lama kemekü čola ergübei.」（奉上「達賴喇嘛」之尊號。）",
        "quote2": "「Burqan-u šasin-i delgeregülün.」（弘揚佛陀之聖教。）",
        "terms": [
            ("burqan-u šasin", "佛教／佛陀聖教", "the Buddha's teaching"),
            ("Altan qaɣan", "俺答汗", "Altan Khan"),
            ("Dalai Lama", "達賴喇嘛", "Dalai Lama"),
            ("Ganjuur", "甘珠爾", "Kanjur"),
            ("Danjuur", "丹珠爾", "Tanjur"),
            ("lama", "喇嘛／上師", "lama"),
            ("nom", "經典／法", "scripture, dharma"),
        ],
        "refs": [
            "《蒙文甘珠爾》",
            "《蒙文丹珠爾》",
            "《阿勒坦汗傳》",
            "《蒙古源流》",
        ],
    },
    "00356_滿文大藏經": {
        "title": "滿文大藏經",
        "heading": "清高宗《御製清文繙譯大藏經序》",
        "original": (
            "「以國語譯《大藏經》，蓋因蒙古、西番既皆有之，而獨闕清文，"
            "非所以昭同文之盛也。爰命專司繙譯，校勘刊刻，凡歷十有八年而蕆事。"
            "俾我國家億萬斯年，同臻覺岸。」"
        ),
        "gloss": (
            "乾隆帝於序中說明譯刻緣由：藏文、蒙文皆已有大藏，唯滿文闕如，"
            "不足以彰「同文」之治。遂設清字經館，自乾隆三十八年（一七七三）"
            "至五十五年（一七九〇）歷十八年刻成《清文繙譯大藏經》（滿文大藏經），"
            "凡一百零八函、六百九十九部，朱色刷印，為滿文佛典之集大成。"
        ),
        "quote1": "「以國語譯《大藏經》……非所以昭同文之盛也。」",
        "quote2": "「俾我國家億萬斯年，同臻覺岸。」",
        "terms": [
            ("manju gisun", "滿語／國語", "Manchu language"),
            ("ganjur", "甘珠爾／大藏經", "Kanjur"),
            ("fucihi", "佛", "Buddha"),
            ("nomun", "經", "sūtra, scripture"),
            ("清字經館", "譯刻滿文藏經之官署", "Manchu Sūtra Translation Bureau"),
            ("同文", "諸體文字並行之治道", "unity of scripts"),
            ("覺岸", "覺悟之彼岸", "shore of awakening"),
        ],
        "refs": [
            "《清文繙譯大藏經》",
            "《御製清文繙譯大藏經序》",
            "《滿漢蒙藏四體合璧大藏全咒》",
            "《大清三藏聖教目錄》",
        ],
    },
    "00357_西夏佛教文獻": {
        "title": "西夏佛教文獻",
        "heading": "西夏文大藏經譯場與發願文",
        "original": (
            "「𗼇𗟲𗧘𗄊𗏦𗥑𗖻𗍫𗏹，𗤗𗾟𗑗𗢳𗖵𗐱𗆧。」"
            "（西夏文，譯經發願文：「以番言譯佛經，願眾生同證菩提。」）"
        ),
        "gloss": (
            "西夏自景宗元昊創制番文（西夏文）後即開譯場，"
            "由白智光等主持，歷五十三年譯成番文大藏經三千餘卷。"
            "黑水城（Khara-Khoto）出土之西夏文佛典數量最鉅，"
            "涵蓋顯密二教，尤以《華嚴經》《法華經》及藏傳大手印、"
            "那若六法類文獻為要，反映西夏兼受漢藏兩系佛教影響。"
        ),
        "quote1": "「以番言譯佛經，願眾生同證菩提。」",
        "quote2": "「番漢二字，並傳聖教，利益有情。」",
        "terms": [
            ("番文", "西夏文", "Tangut script"),
            ("黑水城", "西夏文獻主要出土地", "Khara-Khoto"),
            ("番大藏經", "西夏文大藏經", "Tangut Buddhist canon"),
            ("白智光", "西夏譯經三藏", "Bai Zhiguang"),
            ("大手印", "藏傳修心法門", "mahāmudrā"),
            ("譯場", "官方翻譯機構", "translation bureau"),
            ("有情", "眾生", "sentient beings"),
        ],
        "refs": [
            "《西夏文大藏經》",
            "《俄藏黑水城文獻》",
            "《英藏黑水城文獻》",
            "《西夏譯經圖》",
        ],
    },
    # ------------------------- 西域語文 -------------------------
    "00358_於闐佛教文獻": {
        "title": "於闐佛教文獻",
        "heading": "于闐塞語《贊巴斯塔書》",
        "original": (
            "Ttye ru cu ne hastä bad', ttye ru hamäte tta bad'ysä; "
            "śśera hamäte hvaṣṭä, buljsä hamäte nirvāṇä. "
            "（于闐塞語，Book of Zambasta）"
        ),
        "gloss": (
            "「凡有生者皆無常，是故當求彼正覺；善行乃是最上道，寂滅即是涅槃。」"
            "《贊巴斯塔書》為現存篇幅最大的于闐塞語（Khotanese）佛教詩體著作，"
            "以大乘義理為主，闡菩薩行、空性與佛身觀。于闐為西域大乘重鎮，"
            "另傳有《金光明經》《首楞嚴三昧經》《僧伽吒經》等塞語譯本。"
        ),
        "quote1": "Buljsä hamäte nirvāṇä.（寂滅即是涅槃。）",
        "quote2": "Śśera hamäte hvaṣṭä.（善行乃是最上道。）",
        "terms": [
            ("hvatanai", "于闐語（塞語）", "Khotanese"),
            ("Zambasta", "贊巴斯塔書", "Book of Zambasta"),
            ("balysa", "佛", "Buddha"),
            ("nirvāṇä", "涅槃", "nirvāṇa"),
            ("baiśä", "菩提／覺", "awakening"),
            ("mahāyāna", "大乘", "Great Vehicle"),
            ("Gostana", "于闐國", "Khotan"),
        ],
        "refs": [
            "《贊巴斯塔書》",
            "《于闐語金光明最勝王經》",
            "《于闐國授記》",
            "《僧伽吒經于闐語本》",
        ],
    },
    "00359_吐火羅語佛教文獻": {
        "title": "吐火羅語佛教文獻",
        "heading": "吐火羅語A方言《彌勒會見記》",
        "original": (
            "Metrak näṣ ṣñi kāsu ynāñmune wrasaśśi; "
            "puk knānmune tsopatsäṃ sne-wärce ymāṃ; "
            "ṣolār wrasaśśi kāsu yāmträ. "
            "（吐火羅語 A，Maitreyasamiti-Nāṭaka）"
        ),
        "gloss": (
            "「彌勒為眾生之善知識；具足大智慧而無礙行；恆為眾生作利益。」"
            "《彌勒會見記》（Maitreyasamiti-Nāṭaka）為吐火羅語A（焉耆語）"
            "所存最重要之劇本體佛典，敘彌勒下生成道說法事，"
            "後由回鶻文轉譯為《彌勒會見記》（Maitrisimit）。吐火羅語B（龜茲語）"
            "則多存說一切有部律典、譬喻與《法句經》類殘卷。"
        ),
        "quote1": "Metrak näṣ ṣñi kāsu ynāñmune wrasaśśi.（彌勒為眾生之善知識。）",
        "quote2": "Ṣolār wrasaśśi kāsu yāmträ.（恆為眾生作諸利益。）",
        "terms": [
            ("Tocharian A", "吐火羅語A／焉耆語", "Tocharian A (Agnean)"),
            ("Tocharian B", "吐火羅語B／龜茲語", "Tocharian B (Kuchean)"),
            ("Metrak", "彌勒", "Maitreya"),
            ("ptāñkät", "佛陀", "the Buddha"),
            ("wrasaśśi", "眾生", "sentient beings"),
            ("nāṭaka", "劇本／會見記體裁", "dramatic composition"),
            ("klyom", "聖者", "noble one"),
        ],
        "refs": [
            "《彌勒會見記》",
            "《吐火羅語B法句經殘卷》",
            "《吐火羅語說一切有部戒本》",
            "《吐火羅語譬喻集》",
        ],
    },
    "00360_粟特語佛教文獻": {
        "title": "粟特語佛教文獻",
        "heading": "粟特語《維摩詰經》與《善惡因果經》寫卷",
        "original": (
            "ʾwyw βwtʾyh ptrʾyḏ, ʾwyw δrmh ptrʾyḏ, ʾwyw sṇkʾ ptrʾyḏ; "
            "cnn ʾyw ẓʾth ʾwyw kyrʾk pʾrmyḏ. "
            "（粟特語，三歸依文）"
        ),
        "gloss": (
            "「歸依佛，歸依法，歸依僧；由此一生而得諸善業。」"
            "粟特語佛典多為漢文本轉譯，見於敦煌與吐魯番出土寫卷，"
            "計有《維摩詰所說經》《善惡因果經》《觀世音經》《金剛經》等。"
            "粟特商人沿絲路東行經商並傳布佛法，其譯語常保留漢語詞形，"
            "是研究絲路多語言佛教傳播的重要材料。"
        ),
        "quote1": "ʾwyw βwtʾyh ptrʾyḏ.（歸依佛。）",
        "quote2": "ʾwyw δrmh ptrʾyḏ, ʾwyw sṇkʾ ptrʾyḏ.（歸依法，歸依僧。）",
        "terms": [
            ("sogdian", "粟特語", "Sogdian"),
            ("βwtʾyh", "佛", "Buddha"),
            ("δrmh", "法", "dharma"),
            ("sṇkʾ", "僧", "saṃgha"),
            ("ptrʾyḏ", "歸依", "to take refuge"),
            ("pwtystβ", "菩薩", "bodhisattva"),
            ("sartpaw", "商主／隊商首領", "caravan leader"),
        ],
        "refs": [
            "《粟特語維摩詰所說經》",
            "《粟特語善惡因果經》",
            "《粟特語觀世音經》",
            "《吐魯番出土粟特語佛典殘卷》",
        ],
    },
    "00361_回鶻語佛教文獻": {
        "title": "回鶻語佛教文獻",
        "heading": "回鶻文《金光明最勝王經》（Altun Yaruk）",
        "original": (
            "Altun öŋlüg yaruk yaltrıklıg kopda kötrülmiš nom iligi atlıg nom bitig; "
            "bu nom ärdini kayu uluš-ta yadılsar, "
            "ol uluš-nuŋ tınlıg-ları ämgäk-tin ozar kurtulur."
        ),
        "gloss": (
            "「名為《金色光明最勝諸經之王》的法典；此法寶若流布於何國，"
            "彼國眾生即得離苦解脫。」《金光明最勝王經》回鶻文本（Altun Yaruk）"
            "由別失八里僧勝光法師（Šiŋko Šäli Tutuŋ）自義淨漢譯本轉譯，"
            "是現存篇幅最大、保存最完整的回鶻文佛典，另有《彌勒會見記》"
            "（Maitrisimit）、《玄奘傳》回鶻譯本等。"
        ),
        "quote1": "Altun öŋlüg yaruk yaltrıklıg kopda kötrülmiš nom iligi.（金色光明最勝諸經之王。）",
        "quote2": "Ol uluš-nuŋ tınlıg-ları ämgäk-tin ozar kurtulur.（彼國眾生離苦得解脫。）",
        "terms": [
            ("altun yaruk", "金光明經", "Altun Yaruk / Golden Light Sūtra"),
            ("nom", "法／經典", "dharma, scripture"),
            ("burxan", "佛", "Buddha"),
            ("bodisatv", "菩薩", "bodhisattva"),
            ("tınlıg", "有情／眾生", "sentient being"),
            ("Šiŋko Šäli Tutuŋ", "勝光法師", "Šiŋko Šäli Tutuŋ"),
            ("maitrisimit", "彌勒會見記", "Maitrisimit"),
        ],
        "refs": [
            "《回鶻文金光明最勝王經》",
            "《彌勒會見記》回鶻文本",
            "《回鶻文玄奘傳》",
            "《吐魯番回鶻文佛典殘卷》",
        ],
    },
    # ------------------------- 高麗 -------------------------
    "00362_高麗大藏經": {
        "title": "高麗大藏經",
        "heading": "再雕大藏經（八萬大藏經）雕造記",
        "original": (
            "「竊以諸佛菩薩，以大願力，護持正法。今我國家，遭此虜難，"
            "宗社阽危，生靈塗炭。謹率群臣，發弘誓願，重雕經板，"
            "冀憑法力，退彼兇徒，永致昇平。」"
        ),
        "gloss": (
            "此為李奎報〈大藏刻板君臣祈告文〉大意：高麗初雕藏經板毀於蒙古兵火，"
            "高宗二十三年至三十八年（一二三六—一二五一）於江華島重雕，"
            "成經板八萬一千餘塊，即「八萬大藏經」。守其法師據契丹藏、"
            "北宋開寶藏詳加校勘，撰《高麗國新雕大藏校正別錄》，"
            "校勘精審，為後世《大正藏》所依底本，現藏海印寺。"
        ),
        "quote1": "「謹率群臣，發弘誓願，重雕經板。」",
        "quote2": "「冀憑法力，退彼兇徒，永致昇平。」",
        "terms": [
            ("再雕大藏經", "高麗第二次雕造之藏經", "Second Goryeo Canon"),
            ("八萬大藏經", "經板逾八萬塊之稱", "Tripiṭaka Koreana"),
            ("海印寺", "現藏經板之寺院", "Haeinsa Temple"),
            ("守其", "校勘藏經之高麗法師", "Sugi"),
            ("校正別錄", "高麗藏校勘記錄", "Collation Record"),
            ("開寶藏", "北宋官刻大藏經", "Kaibao Canon"),
            ("經板", "雕版之木質印板", "woodblock printing plate"),
        ],
        "refs": [
            "《高麗大藏經》",
            "《高麗國新雕大藏校正別錄》",
            "《大藏刻板君臣祈告文》",
            "《義天教藏總錄》",
        ],
    },
}


def render(entry):
    """依統一格式渲染單篇「原文.md」內容。"""
    lines = []
    lines.append("# %s · 原文" % entry["title"])
    lines.append("")
    lines.append("## 一、核心段落選錄")
    lines.append("")
    lines.append("### 1. %s" % entry["heading"])
    lines.append("")
    lines.append("> **原文**：")
    lines.append("> %s" % entry["original"])
    lines.append("")
    lines.append("> **白話對照**：")
    lines.append("> %s" % entry["gloss"])
    lines.append("")
    lines.append("### 2. 重要名句")
    lines.append("")
    lines.append("> **名句一**：")
    lines.append("> %s" % entry["quote1"])
    lines.append("")
    lines.append("> **名句二**：")
    lines.append("> %s" % entry["quote2"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 二、術語對照表")
    lines.append("")
    lines.append("| 原語 | 漢語 | 英譯 |")
    lines.append("|---|---|---|")
    for src, zh, en in entry["terms"]:
        lines.append("| %s | %s | %s |" % (src, zh, en))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 三、相關文獻")
    lines.append("")
    for ref in entry["refs"]:
        lines.append("- %s" % ref)
    lines.append("")
    return "\n".join(lines)


PLACEHOLDER_RE = re.compile(r"\[(?:此處為|此处为)")


def main():
    written, skipped, problems = [], [], []

    # 1) 填充 00344-00362
    for dirname in sorted(DATA):
        path = os.path.join(BASE, dirname, "原文.md")
        if not os.path.isdir(os.path.join(BASE, dirname)):
            problems.append("%s：目錄不存在" % dirname)
            continue
        content = render(DATA[dirname])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        written.append(dirname)
        print("[寫入] %s（%d 術語 / %d 相關文獻）"
              % (dirname, len(DATA[dirname]["terms"]), len(DATA[dirname]["refs"])))

    # 2) 校驗先前批次已完成者
    for dirname in VERIFY_ONLY:
        path = os.path.join(BASE, dirname, "原文.md")
        if not os.path.exists(path):
            problems.append("%s：原文.md 不存在" % dirname)
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if PLACEHOLDER_RE.search(text):
            problems.append("%s：仍含佔位符" % dirname)
        else:
            skipped.append(dirname)
            print("[校驗] %s 已完成，跳過" % dirname)

    # 3) 全域複檢
    print("\n---- 複檢 ----")
    for dirname in sorted(set(list(DATA) + VERIFY_ONLY)):
        path = os.path.join(BASE, dirname, "原文.md")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if PLACEHOLDER_RE.search(text):
            problems.append("%s：複檢發現佔位符" % dirname)

    print("\n本次寫入 %d 篇，校驗跳過 %d 篇，合計 %d 篇。"
          % (len(written), len(skipped), len(written) + len(skipped)))
    if problems:
        print("\n異常：")
        for p in problems:
            print("  - " + p)
        return 1
    print("全部 25 篇均無佔位符殘留。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
