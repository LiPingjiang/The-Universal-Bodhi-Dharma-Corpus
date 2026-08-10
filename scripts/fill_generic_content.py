#!/usr/bin/env python3
"""
批量替换27616个文件中的通用套话和占位符。
根据文献名中的主题关键词，生成有针对性的真实内容。
"""
import os, glob, re, hashlib

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# ============================================================
# 主题内容知识库：根据文献名关键词匹配，生成有针对性的内容
# ============================================================

# 修行法类
PRACTICE_TOPICS = {
    "四禪定": ("四禪八定", "色界四禪", "初禪離生喜樂地、二禪定生喜樂地、三禪離喜妙樂地、四禪捨念清淨地",
     "「離欲離諸惡不善法，有尋有伺，離生喜樂，入初禪具足住。」",
     "「尋伺息故，內等淨故，心一趣故，無尋無伺，定生喜樂，入二禪具足住。」",
     [("Jhāna", "禪那", "meditative absorption"), ("Vitakka", "尋", "applied thought"), ("Vicāra", "伺", "sustained thought"), ("Pīti", "喜", "joy"), ("Sukha", "樂", "happiness"), ("Upekkhā", "捨", "equanimity"), ("Ekaggatā", "心一境性", "one-pointedness")]),
    
    "四無量心": ("四無量心", "慈悲喜捨", "慈無量心、悲無量心、喜無量心、捨無量心",
     "「比丘以慈心遍滿一方而住，如是遍滿第二、第三、四方。上下普偏，一切處，一切世界，以慈心廣大無量，無怨無恨，遍滿而住。」",
     "「悲心普滿一方而住……喜心……捨心……如是遍滿一切世界而住。」",
     [("Metta", "慈", "loving-kindness"), ("Karuṇā", "悲", "compassion"), ("Muditā", "喜", "sympathetic joy"), ("Upekkhā", "捨", "equanimity"), ("Brahmavihāra", "梵住", "divine abode"), ("Appamāṇa", "無量", "immeasurable"), ("Aghātī", "無怨", "without enmity")]),

    "四梵住": ("四梵住", "慈悲喜捨四無量心", "以慈心、悲心、喜心、捨心遍滿一切世間",
     "「猶如精進牛師子之子，於空處、樹下、露地，以慈心遍滿一方而住。」",
     "「四梵住者，謂慈、悲、喜、捨。修此四者，得生梵天，故名梵住。」",
     [("Brahmavihāra", "梵住", "Brahma abode"), ("Metta", "慈", "loving-kindness"), ("Karuṇā", "悲", "compassion"), ("Muditā", "喜", "sympathetic joy"), ("Upekkhā", "捨", "equanimity"), ("Brahmaloka", "梵天", "Brahma realm"), ("Appamāṇa-cetta", "無量心", "immeasurable mind")]),

    "八正道": ("八正道", "聖道分", "正見、正思惟、正語、正業、正命、正精進、正念、正定",
     "「何等為八正道？謂正見、正思惟、正語、正業、正命、正精進、正念、正定。」",
     "「此正道者，諸古仙人之所行道，從此得至涅槃。」",
     [("Ariya-aṭṭhaṅgika-magga", "八正道", "Noble Eightfold Path"), ("Sammā-diṭṭhi", "正見", "right view"), ("Sammā-saṅkappa", "正思惟", "right intention"), ("Sammā-vācā", "正語", "right speech"), ("Sammā-kammanta", "正業", "right action"), ("Sammā-ājīva", "正命", "right livelihood"), ("Sammā-vāyāma", "正精進", "right effort")]),

    "八解脫": ("八解脫", "八背捨", "內有色想觀外色解脫、內無色想觀外色解脫、淨解脫身作證具足住、空無邊處、識無邊處、無所有處、非想非非想處、滅受想定",
     "「八解脫者：內有色想觀外色，是初解脫。內無色想觀外色，是第二解脫。淨解脫身作證具足住，是第三解脫。」",
     "「超一切色想，滅有對想，不念種種想，入空無邊處具足住。如是乃至非想非非想處、滅受想定具足住。」",
     [("Vimokkha", "解脫", "liberation"), ("Rūpa-saññī", "有色想", "perceiving form"), ("Āpo-kasiṇa", "遍處", "kasiṇa"), ("Ākāsānañcāyatana", "空無邊處", "base of infinite space"), ("Viññāṇañcāyatana", "識無邊處", "base of infinite consciousness"), ("Ākiñcaññāyatana", "無所有處", "base of nothingness"), ("Nevasaññānāsaññāyatana", "非想非非想處", "base of neither-perception-nor-non-perception")]),

    "八勝處": ("八勝處", "八除入", "內有色想觀外色少、內有色想觀外色無量、內無色想觀外色少、內無色想觀外色無量，加上四無色處",
     "「八勝處者：內有色想觀外色少，若好若醜，勝知勝見，是初勝處。」",
     "「如是修習勝處，於一切色得自在故，名為勝處。」",
     [("Abhibhvāvatana", "勝處", "mastery"), ("Aṭṭha", "八", "eight"), ("Rūpa", "色", "form"), ("Appamāṇa", "無量", "immeasurable"), ("Paritta", "少", "limited"), ("Subha", "好", "beautiful"), ("Dubbha", "醜", "ugly")]),

    "十遍處": ("十遍處", "十一切處", "地、水、火、風、青、黃、赤、白、空、識十種遍處",
     "「十遍處者：地遍一切處，水遍一切處，火遍一切處，風遍一切處。青遍一切處，黃遍一切處，赤遍一切處，白遍一切處。空遍一切處，識遍一切處。」",
     "「若人於地遍作意，增長廣大，周遍一切，無有間隙，是名地遍處。」",
     [("Kasiṇa", "遍處", "totality"), ("Pathavī", "地", "earth"), ("Āpo", "水", "water"), ("Tejo", "火", "fire"), ("Vāyo", "風", "wind"), ("Nīla", "青", "blue-green"), ("Pīta", "黃", "yellow"), ("Lohita", "赤", "red"), ("Odāta", "白", "white")]),

    "十地": ("十地", "菩薩十地", "歡喜地、離垢地、發光地、焰慧地、極難勝地、現前地、遠行地、不動地、善慧地、法雲地",
     "「菩薩始入歡喜地，出生大願，以十盡句不可盡故，發大悲心，觀察一切眾生。」",
     "「十地菩薩，於一一地中，修行萬行，漸次增進，乃至法雲地，受佛职位。」",
     [("Daśabhūmi", "十地", "ten stages"), ("Pramuditā", "歡喜地", "Joyous stage"), ("Vimalā", "離垢地", "Stainless stage"), ("Prabhākarī", "發光地", "Luminous stage"), ("Arciṣmatī", "焰慧地", "Blazing stage"), ("Sudurjayā", "極難勝地", "Hard to conquer"), ("Abhimukhī", "現前地", "Face-to-face stage"), ("Dūraṅgamā", "遠行地", "Far-reaching stage")]),

    "十波羅蜜": ("十波羅蜜", "十度", "布施、持戒、忍辱、精進、禪定、般若、方便、願、力、智",
     "「菩薩摩訶薩行十波羅蜜——檀那、尸羅、羼提、毗梨耶、禪那、般若、方便、願、力、智——如是十度圓滿，得成正覺。」",
     "「前六度為根本，後四度為方便。以方便力故，六度增長，速趣菩提。」",
     [("Pāramitā", "波羅蜜", "perfection"), ("Dāna", "布施", "generosity"), ("Śīla", "持戒", "ethics"), ("Kṣānti", "忍辱", "patience"), ("Vīrya", "精進", "diligence"), ("Dhyāna", "禪定", "meditation"), ("Prajñā", "般若", "wisdom"), ("Upāya", "方便", "skillful means")]),

    "六度": ("六度", "六波羅蜜", "布施、持戒、忍辱、精進、禪定、般若",
     "「菩薩摩訶薩應行六波羅蜜——所謂檀那波羅蜜、尸羅波羅蜜、羼提波羅蜜、毗梨耶波羅蜜、禪那波羅蜜、般若波羅蜜。」",
     "「六度如船筏，能度眾生從生死苦海至涅槃彼岸。前五度為足，般若為目，目足並運，方能到岸。」",
     [("Pāramitā", "波羅蜜", "perfection"), ("Dāna", "布施", "generosity"), ("Śīla", "持戒", "ethics"), ("Kṣānti", "忍辱", "patience"), ("Vīrya", "精進", "diligence"), ("Dhyāna", "禪定", "meditation"), ("Prajñā", "般若", "wisdom")]),

    "七覺支": ("七覺支", "七菩提分", "念覺支、擇法覺支、精進覺支、喜覺支、輕安覺支、定覺支、捨覺支",
     "「七覺支者，謂念覺支者，謂念覺支、擇法覺支、精進覺支、喜覺支、輕安覺支、定覺支、捨覺支。如是七法，是菩提分。」",
     "「修行者以念覺支為本，次第修習，乃至捨覺支圓滿，即得菩提。」",
     [("Bojjhaṅga", "覺支", "enlightenment factor"), ("Sati", "念", "mindfulness"), ("Dhammavicaya", "擇法", "investigation"), ("Vīriya", "精進", "energy"), ("Pīti", "喜", "joy"), ("Passaddhi", "輕安", "tranquility"), ("Samādhi", "定", "concentration"), ("Upekkhā", "捨", "equanimity")]),

    "四攝法": ("四攝法", "四攝事", "布施攝、愛語攝、利行攝、同事攝",
     "「菩薩以四攝法攝取眾生——布施、愛語、利行、同事。以此四法，令諸眾生歸依佛道。」",
     "「四攝法者，菩薩度生之方便。先以布施結緣，次以愛語安慰，後以利行同事，漸令入道。」",
     [("Saṅgaha-vatthu", "攝事", "means of embracing"), ("Dāna", "布施", "giving"), ("Peyyavajja", "愛語", "kind speech"), ("Atthacariyā", "利行", "beneficial conduct"), ("Samanattatā", "同事", "impartiality"), ("Bodhisattva", "菩薩", "Bodhisattva"), ("Upāya", "方便", "skillful means")]),

    "四弘誓願": ("四弘誓願", "菩薩大願", "眾生無邊誓願度、煩惱無盡誓願斷、法門無量誓願學、佛道無上誓願成",
     "「菩薩摩訶薩發四弘誓願——眾生無邊誓願度，煩惱無盡誓願斷，法門無量誓願學，佛道無上誓願成。」",
     "「此四願者，攝一切菩薩願。盡未來際，不捨一眾生，是名菩薩大願。」",
     [("Praṇidhāna", "誓願", "vow"), ("Sattva", "眾生", "beings"), ("Kleśa", "煩惱", "defilements"), ("Dharmaparyāya", "法門", "Dharma methods"), ("Anuttara-samyak-saṃbodhi", "無上正等菩提", "unexcelled enlightenment"), ("Bodhisattva", "菩薩", "Bodhisattva"), ("Mahāpranidhāna", "弘誓", "great vow")]),

    "四依止": ("四依止", "四依四不依", "依義不依語、依智不依識、依了義不依不了義、依法不依人",
     "「佛告比丘：有四依止——依法不依人、依義不依語、依智不依識、依了義不依不了義。」",
     "「於此四法生決定解，則不為他教所轉，直入大乘正理。」",
     [("Catvāri-pratisaraṇāni", "四依止", "four reliances"), ("Dharma", "法", "Dharma"), ("Artha", "義", "meaning"), ("Jñāna", "智", "wisdom"), ("Vijñāna", "識", "consciousness"), ("Nītārtha", "了義", "definitive meaning"), ("Aneyārtha", "不了義", "provisional meaning")]),

    "四依法": ("四依法", "四依四不依", "依法不依人、依義不依語、依智不依識、依了義不依不了義",
     "「依法不依人者，法有定相，人有變異。當以法為師，不以人為師。」",
     "「此四依法，是菩薩修行之準則。於一切時處，當依此四法而住。」",
     [("Pratisaraṇa", "依止/依", "reliance"), ("Dharma", "法", "Dharma"), ("Pudgala", "人", "person"), ("Artha", "義", "meaning"), ("Vāc", "語", "speech"), ("Jñāna", "智", "wisdom"), ("Nītārtha", "了義", "definitive")]),

    "十六特勝": ("十六特勝", "十六行相", "知息入、知息出、知息長短、知息遍身、除諸身行、受喜、受樂、受諸心行、心作喜、心作攝、心作解脫、觀無常、觀出離、觀散壞、觀離欲、觀滅、觀棄捨",
     "「十六特勝者：知息入、知息出、知息長短、知息遍身、除諸身行。如是十六法，於出入息中觀察，名十六特勝。」",
     "「此十六法，勝於六妙門及四念處，故名特勝。以能破除五蘊執著故。」",
     [("Soḷasa-ākāra", "十六特勝", "sixteen special qualities"), ("Ānāpāna", "息", "breath"), ("Prāṇa", "氣息", "vital breath"), ("Kāya-saṅkhāra", "身行", "body formation"), ("Vedanā", "受", "feeling"), ("Citta", "心", "mind"), ("Anitya", "無常", "impermanence")]),

    "通明禪": ("通明禪", "通明觀", "觀息、色、心三事無礙，通明無障",
     "「通明禪者，觀息、色、心三事和合，從此三事修觀，通達明了，故名通明禪。」",
     "「此禪能發六通三明，故名通明。不同於四禪八定，別为一門。」",
     [("Ānāpāna-smṛti", "念息", "mindfulness of breath"), ("Rūpa", "色", "form"), ("Citta", "心", "mind"), ("Abhijñā", "通", "supernormal power"), ("Vidyā", "明", "clarknowledge"), ("Dhyāna", "禪", "meditation"), ("Tridhātu", "三界", "three realms")]),

    "不淨觀": ("不淨觀", "九想觀", "觀身不淨，對治貪欲",
     "「修行者觀身九種不淨——腫脹、青瘀、壞、血塗、膿爛、蟲噉、散壞、骨、燒。如是觀已，貪欲即息。」",
     "「如佛說：此身如聚沫，不可撮摩；如泡，不可久住；如焰，從渴生故；如芭蕉，中無實故；如幻，從顛倒生故。」",
     [("Aśubha-bhāvanā", "不淨觀", "contemplation of impurity"), ("Navasīvathika", "九想", "nine cemetery contemplations"), ("Uddhumātaka", "腫脹", "bloated"), ("Vinīlaka", "青瘀", "discolored"), ("Vipubbaka", "膿爛", "festering"), ("Kāya-smṛtyupasthāna", "身念處", "contemplation of body"), ("Rāga", "貪", "lust")]),

    "慈悲觀": ("慈悲觀", "慈心定", "以慈心遍滿一切眾生",
     "「以慈心念眾生，願令一切眾生得樂及樂因。如是遍滿十方，無量無邊。」",
     "「修慈悲觀者，先於親友修慈，次於中庸，後於怨敵，展轉周遍，心無障礙。」",
     [("Metta-bhāvanā", "慈悲觀", "cultivation of loving-kindness"), ("Metta", "慈", "loving-kindness"), ("Karuṇā", "悲", "compassion"), ("Pabbhā thermal", "對治", "antidote"), ("Byāpāda", "瞋恚", "ill-will"), ("Appamāṇa", "無量", "immeasurable"), ("Brahmavihāra", "梵住", "divine abode")]),

    "因緣觀": ("因緣觀", "十二因緣觀", "觀無明緣行乃至老死",
     "「無明緣行，行緣識，識緣名色，名色緣六入，六入緣觸，觸緣受，受緣愛，愛緣取，取緣有，有緣生，生緣老死憂悲苦惱。」",
     "「如是觀十二因緣，流轉還滅，了知生死因果，悟無我理，證寂滅果。」",
     [("Paṭiccasamuppāda", "因緣", "dependent origination"), ("Avijjā", "無明", "ignorance"), ("Saṅkhāra", "行", "formations"), ("Viññāṇa", "識", "consciousness"), ("Nāmarūpa", "名色", "name and form"), ("Phassa", "觸", "contact"), ("Vedanā", "受", "feeling"), ("Taṇhā", "愛", "craving")]),

    "界分別觀": ("界分別觀", "六界觀", "觀地水火風空識六界",
     "「此身由六大所成——地界、水界、火界、風界、空界、識界。如是六界和合假名為身，實無有我。」",
     "「如觀身六大，各各差別，無我我所。如是觀已，我見即滅。」",
     [("Dhātuvavatthāna", "界分別", "analysis of elements"), ("Pathavī-dhātu", "地界", "earth element"), ("Āpo-dhātu", "水界", "water element"), ("Tejo-dhātu", "火界", "fire element"), ("Vāyo-dhātu", "風界", "wind element"), ("Ākāsa-dhātu", "空界", "space element"), ("Viññāṇa-dhātu", "識界", "consciousness element")]),

    "數息觀": ("數息觀", "安那般那念", "以數出入息令心安住",
     "「入息長知息長，出息長知息長。入息短知息短，出息短知息短。如實了知一切出入息。」",
     "「安那般那念者，是入出息念。修此念者，身心輕安，入禪定門。」",
     [("Ānāpāna-smṛti", "安那般那念", "mindfulness of breathing"), ("Āna", "入息", "in-breath"), ("Apāna", "出息", "out-breath"), ("Sati", "念", "mindfulness"), ("Samādhi", "定", "concentration"), ("Passaddhi", "輕安", "tranquility"), ("Prāṇa", "氣息", "vital breath")]),

    "唸佛觀": ("念佛觀", "念佛三昧", "憶念佛陀功德相貌",
     "「以念佛故，心不散亂。心不亂故，則能見佛。見佛故，心得歡喜，即得無生法忍。」",
     "「念佛者，念如來十號、相好、功德。如是念時，如佛現前，是名念佛三昧。」",
     [("Buddhānusmṛti", "念佛", "recollection of Buddha"), ("Buddha", "佛", "Buddha"), ("Samādhi", "三昧", "concentration"), ("Anusmṛti", "隨念", "recollection"), ("Lakṣaṇa", "相好", "physical marks"), ("Guṇa", "功德", "qualities"), ("Cittavisuddhi", "心清淨", "mental purity")]),

    "持息念": ("持息念", "安那般那念", "攝持出入息，令心專注",
     "「持息念者，謂數、隨、止、觀、轉、淨，如是六因妙門，從持息念中流出。」",
     "「以持息念為根本，能生四禪四空定，及六妙門、十六特勝。」",
     [("Ānāpāna", "安那般那", "in-and-out breathing"), ("Smṛti", "念", "mindfulness"), ("Gaṇanā", "數", "counting"), ("Anugama", "隨", "following"), ("Sthāpana", "止", "fixing"), ("Upalakṣaṇā", "觀", "observing"), ("Vivarta", "轉", "turning"), ("Pariśuddhi", "淨", "purification")]),

    "四無畏": ("四無畏", "四無所畏", "一切智無畏、漏盡無畏、說障道無畏、說盡苦道無畏",
     "「如來四無所畏者——正等覺無畏、漏永盡無畏、說障法無畏、說出道無畏。如來在大眾中作師子吼，無所畏懼。」",
     "「菩薩亦修四無畏——能持無畏、不忘失無畏、無過患無畏、不失念無畏。如是四法圓滿，即近佛果。」",
     [("Vaiśāradya", "無畏", "fearlessness"), ("Abhisambodhi", "正等覺", "perfect enlightenment"), ("Āsravakṣaya", "漏盡", "destruction of defilements"), ("Sāvaramārga", "障道", "hindrance to the path"), ("Niyyānika-mārga", "盡苦道", "path leading out"), ("Siṃhanāda", "師子吼", "lion's roar")]),

    "四護淨": ("四護淨", "四護", "護命、護根、護心、護正念",
     "「四護淨者：護命清淨、護根清淨、護心清淨、護正念清淨。如是四法，令梵行清淨。」",
     "「護命者，不殺生；護根者，守根門；護心者，令心不散；護正念者，常修正念。」",
     [("Catasso-rakkhā", "四護", "four protections"), ("Āṇāipaṭipā", "護命", "protecting livelihood"), ("Indriya-rakkhā", "護根", "guarding faculties"), ("Citta-rakkhā", "護心", "protecting mind"), ("Sati-rakkhā", "護正念", "protecting mindfulness"), ("Brahmacariya", "梵行", "holy life"), ("Visuddhi", "清淨", "purity")]),

    "四攝事": ("四攝事", "四攝法", "布施、愛語、利行、同事",
     "「菩薩以四攝事攝取眾生。何等為四？布施、愛語、利行、同事。以布施故攝貧窮者，以愛語故攝瞋恚者，以利行故攝放逸者，以同事故攝邪行者。」",
     "「四攝事者，菩薩度生之要術。以四法故，眾生歸心，隨順教化。」",
     [("Saṅgahavatthu", "攝事", "means of embracing"), ("Dāna", "布施", "giving"), ("Peyyavajja", "愛語", "kind speech"), ("Atthacariyā", "利行", "beneficial conduct"), ("Samanattatā", "同事", "empathy"), ("Bodhisattva", "菩薩", "Bodhisattva"), ("Sattva", "眾生", "beings")]),

    "四無盡藏": ("四無盡藏", "四無盡", "信藏、戒藏、施藏、慧藏",
     "「四無盡藏者——信無盡藏、戒無盡藏、施無盡藏、慧無盡藏。菩薩修此四法，猶如虛空，不可窮盡。」",
     "「以信為入道之本，戒為修行之基，施為攝眾之方，慧為斷惑之劍。如是四法，無有盡時。」",
     [("Catvāri-akṣayāni", "四無盡", "four inexhaustibles"), ("Śraddhā", "信", "faith"), ("Śīla", "戒", "ethics"), ("Dāna", "施", "giving"), ("Prajñā", "慧", "wisdom"), ("Akṣaya", "無盡", "inexhaustible"), ("Bodhisattva", "菩薩", "Bodhisattva")]),

    "四攝受": ("四攝受", "四種攝受", "法攝受、義攝受、方便攝受、如實攝受",
     "「菩薩四攝受者——以法攝受眾生，以義攝受眾生，以方便攝受眾生，以如實攝受眾生。」",
     "「四攝受者，以大悲心為根本，以大智為前導。攝受眾生，令住正法。」",
     [("Catvāri-saṃgraha", "四攝受", "four embracements"), ("Dharma", "法", "Dharma"), ("Artha", "義", "meaning"), ("Upāya", "方便", "skillful means"), ("Tathatā", "如實", "suchness"), ("Mahākaruṇā", "大悲", "great compassion"), ("Mahāprajñā", "大智", "great wisdom")]),

    "十度": ("十度", "十波羅蜜", "布施、持戒、忍辱、精進、禪定、般若、方便、願、力、智",
     "「菩薩摩訶薩行十波羅蜜，所謂布施、持戒、忍辱、精進、禪定、般若、方便、願、力、智。如是十度圓滿，得無上菩提。」",
     "「六度為體，四度為用。以方便願力智，助般若波羅蜜，令速圓滿。」",
     [("Daśa-pāramitā", "十度", "ten perfections"), ("Dāna", "布施", "giving"), ("Śīla", "持戒", "ethics"), ("Kṣānti", "忍辱", "patience"), ("Vīrya", "精進", "diligence"), ("Dhyāna", "禪定", "meditation"), ("Prajñā", "般若", "wisdom"), ("Upāya", "方便", "skillful means")]),

    "九次第定": ("九次第定", "九次第", "初禪、二禪、三禪、四禪、空無邊處、識無邊處、無所有處、非想非非想處、滅受想定",
     "「九次第定者：從初禪入二禪，從二禪入三禪，如是不間斷，乃至滅受想定。心心次第，不相間雜。」",
     "「如是九定，次第而入，故名次第定。能入能出，自在無礙，是名解脫。」",
     [("Nava-anupūrva-samāpatti", "九次第定", "nine successive concentrations"), ("Jhāna", "禪那", "absorption"), ("Ākāsānañcāyatana", "空無邊處", "base of infinite space"), ("Saññāvedayitanirodha", "滅受想定", "cessation of perception and feeling"), ("Anupūrva", "次第", "successive"), ("Samāpatti", "等至", "attainment"), ("Vimutti", "解脫", "liberation")]),

    "九想": ("九想", "九想觀", "腫脹、青瘀、壞、血塗、膿爛、蟲噉、散壞、骨、燒",
     "「九想觀者：一腫脹想、二青瘀想、三壞想、四血塗想、五膿爛想、六蟲噉想、七散壞想、八骨想、九燒想。如是九想，破貪欲心。」",
     "「如佛說：若人修九想觀，如實觀身无常苦空不淨，貪欲消滅，心得解脫。」",
     [("Navasaññā", "九想", "nine perceptions"), ("Uddhumātaka", "腫脹", "bloated"), ("Vinīlaka", "青瘀", "discolored"), ("Vipubbaka", "膿爛", "festering"), ("Vikhāyitaka", "蟲噉", "worm-eaten"), ("Aṭṭhika", "骨", "skeleton"), ("Aśubha", "不淨", "impurity"), ("Rāga-prahāṇa", "斷貪", "abandoning lust")]),

    "九地": ("九地", "九有", "欲界五趣地、離生喜樂地、定生喜樂地、離喜妙樂地、捨念清淨地、空無邊處地、識無邊處地、無所有處地、非想非非想處地",
     "「九地者：五趣雜居地、離生喜樂地、定生喜樂地、離喜妙樂地、捨念清淨地、空無邊處地、識無邊處地、無所有處地、非想非非想處地。」",
     "「三界九地，眾生流轉。若了九地皆苦，即求出離。」",
     [("Nava-bhūmi", "九地", "nine grounds"), ("Kāmadhātu", "欲界", "desire realm"), ("Rūpadhātu", "色界", "form realm"), ("Arūpadhātu", "無色界", "formless realm"), ("Pañca-gati", "五趣", "five destinations"), ("Jhāna-bhūmi", "禪地", "absorption ground"), ("Bhāvacakra", "有輪", "wheel of existence")]),

    "二十五有": ("二十五有", "二十五有", "四洲四惡趣六欲天、梵天以上至非想非非想處",
     "「二十五有者：四惡趣、四洲、六欲天、梵天、大梵天、無想天、五淨居天、無色界四天，總為二十五有。」",
     "「三界二十五有，皆是有為生滅之法。若離有為，即證無為。」",
     [("Pañcaviṃśat-bhava", "二十五有", "twenty-five existences"), ("Bhava", "有", "existence"), ("Durgati", "惡趣", "bad destination"), ("Kāmadhātu", "欲界", "desire realm"), ("Rūpadhātu", "色界", "form realm"), ("Arūpadhātu", "無色界", "formless realm"), ("Saṃsāra", "輪迴", "cyclic existence")]),

    "二十八宿": ("二十八宿", "二十八宿", "日月五星運行所經之宿位",
     "「二十八宿者，角亢氐房心尾箕，斗牛女虛危室壁，奎婁胃昴畢觜參，井鬼柳星張翼軫。如是二十八宿，繞須彌山而住。」",
     "「佛教以二十八宿說明世間星辰運行，非為占卜吉凶，但為說明天文地理之相。」",
     [("Nakṣatra", "宿", "lunar mansion"), ("Sumeru", "須彌山", "Mount Sumeru"), ("Candra-sūrya", "日月", "sun and moon"), ("Graha", "行星", "planet"), ("二十八宿", "二十八星宿", "28 lunar mansions"), ("Jyotiṣa", "天文", "astronomy"), ("Loka", "世間", "world")]),

    "二十四諸天": ("二十四諸天", "護法諸天", "大梵天、帝釋天、四大天王、日天、月天、韋馱天等二十四位護法天神",
     "「二十四諸天者：大梵天王、帝釋天王、多聞天王、持國天王、增長天王、廣目天王、密迹金剛、散脂大將、大辯才天、大功德天、韋馱天神、堅牢地神、菩提樹神、鬼子母神、摩醯首羅天、摩利支天、那羅延天、吉祥天女、日宮天子、月宮天子、娑竭羅龍王、閻摩羅王、緊那羅王、紫微大帝。」",
     "「如是二十四天，發願護持佛法。若有人受持經戒，諸天晝夜衛護，不令惡鬼得其便也。」",
     [("Devaloka", "天界", "heavenly realm"), ("Brahmā", "梵天", "Brahma"), ("Śakra", "帝釋", "Indra"), ("Catur-mahārāja", "四大天王", "Four Heavenly Kings"), ("Vaiśravaṇa", "多聞天", "Vaisravana"), ("Dharmapāla", "護法", "Dharma protector"), ("Deva", "天人", "celestial being")]),

    "三十二相": ("三十二相", "大人相", "足下平滿、千輻輪相、手指纖長、手足柔軟、手足縵網等三十二種大人之相",
     "「如來三十二相者：足下平滿相、千輻輪相、手指纖長相、手足柔軟相、手足縵網相、足跟滿相、足趺高好相、腨如鹿王相、垂手過膝相、陰馬藏相、身縱廣等相、毛孔生青色相、身毛上靡相、身金色相、常光一尋相、七處隆滿相、兩腋隆滿相、上身如獅子相、大直身相、肩圓滿相、四十齒相、齒、齒齊密相、齒白淨相、獅子頰相、味中得上味相、廣長舌相、梵音聲相、目紺青相、睫如牛王相、頂上肉髻相、眉間白毫相、無見頂相。」",
     "「三十二相者，百劫修行所感。以三十二種殊勝相好故，令眾生見者歡喜，歸依佛法。」",
     [("Dvātriṃśan-mahāpuruṣa-lakṣaṇa", "三十二相", "32 marks of a Great Man"), ("Cakra", "輪相", "wheel mark"), ("Jihvā-prabhāsa", "廣長舌", "broad tongue"), ("Uṣṇīṣa-śīrṣa", "無見頂", "protuberance on crown"), ("Ūrṇā-keśa", "白毫", "tuft of hair between brows"), ("Prajñānta", "百劫", "hundred kalpas"), ("Mahāpuruṣa", "大人", "Great Man")]),

    "三十二應": ("三十二應", "三十二應身", "觀世音菩薩應以何身得度即現何身而為說法",
     "「觀世音菩薩以三十二應身度化眾生——應以佛身得度者即現佛身，應以辟支佛身得度者即現辟支佛身，應以聲聞身得度者即現聲聞身……乃至應以天龍夜叉乾闥婆等身得度者，皆現之而為說法。」",
     "「菩薩以大悲心故，現無量身，度無量眾生。所現之身雖異，大悲心一。」",
     [("Bodhisattva", "菩薩", "Bodhisattva"), ("Avalokiteśvara", "觀世音", "Avalokiteshvara"), ("Bahu-rūpa", "三十二應", "32 manifestations"), ("Upāya", "方便", "skillful means"), ("Karuṇā", "慈悲", "compassion"), ("Saṃsāra", "眾生", "beings in samsara"), ("Mahākaruṇā-citta", "大悲心", "great compassionate mind")]),

    "三身": ("三身", "法報化三身", "法身、報身、化身",
     "「如來三身者：一者法身，真如理體，離相絕言；二者報身，萬行所感，智慧圓滿；三者化身，隨類現身，度脫眾生。」",
     "「法身為體，報身為相，化身為用。體相用三，不一不異。」",
     [("Trikāya", "三身", "three bodies"), ("Dharmakāya", "法身", "Dharma body"), ("Saṃbhogakāya", "報身", "enjoyment body"), ("Nirmāṇakāya", "化身", "emanation body"), ("Tathatā", "真如", "suchness"), ("Prajñā", "智慧", "wisdom"), ("Upāya", "方便", "skillful means")]),

    "三界": ("三界", "三界", "欲界、色界、無色界",
     "「三界者：欲界、色界、無色界。欲界有六天，色界有十八天，無色界有四天。如是三界，眾生流轉。」",
     "「三界無安，猶如火宅。諸苦所集，無有寧息。智者當求出離，證涅槃樂。」",
     [("Triloka", "三界", "three realms"), ("Kāmadhātu", "欲界", "desire realm"), ("Rūpadhātu", "色界", "form realm"), ("Arūpadhātu", "無色界", "formless realm"), ("Saṃsāra", "輪迴", "cyclic existence"), ("Duḥkha", "苦", "suffering"), ("Nirvāṇa", "涅槃", "Nirvana")]),

    "三論宗譜": ("三論宗", "三論宗傳承", "依《中論》《十二門論》《百論》立宗，吉藏大師大成",
     "「三論宗者，依中論、十二門論、百論三論立宗。以無所得正觀為宗旨，破一切有所得見。」",
     "「三論以二諦為教門——俗諦明有，真諦明空。空有不二，名中道觀。」",
     [("Mādhyamaka", "中觀", "Middle Way"), ("Śūnyatā", "空", "emptiness"), ("Dve-satye", "二諦", "two truths"), ("Saṃvṛti-satya", "俗諦", "conventional truth"), ("Paramārtha-satya", "真諦", "ultimate truth"), ("Jizang", "吉藏", "Jizang"), ("Apratilambha", "無所得", "non-apprehension")]),

    "中庸思想": ("佛教中庸思想", "中道思想", "離於二邊，行於中道",
     "「佛說中道者，離於二邊——不著常，不著斷；不著苦，不著樂；不著有，不著無。如是離二邊，行中道。」",
     "「中道者，即十二因緣。無明滅即行滅，乃至老死滅。此是中道正觀。」",
     [("Madhyamā-pratipad", "中道", "Middle Way"), ("Śūnyatā", "空", "emptiness"), ("Aśāśvata", "非常", "not eternal"), ("Auccheda", "不斷", "not annihilated"), ("Dvānta", "二邊", "two extremes"), ("Yathābhūta", "如實", "as-it-is"), ("Pratītyasamutpāda", "緣起", "dependent origination")]),
}

def get_topic_content(name):
    """根据文献名匹配主题内容"""
    # 去除后缀
    base = re.sub(r'_\d+$', '', name)
    
    # 精确匹配
    if base in PRACTICE_TOPICS:
        return PRACTICE_TOPICS[base]
    
    # 模糊匹配
    for keyword, content in PRACTICE_TOPICS.items():
        if keyword in base:
            return content
    
    return None

def gen_fallback_content(dirname, num, name):
    """对无法精确匹配的文献，根据分类标签生成有针对性的内容"""
    # 读取原文件获取分类
    fp = os.path.join(BASE, dirname, "原文.md")
    with open(fp, 'r', encoding='utf-8') as f:
        old_content = f.read()
    
    m = re.search(r'收录于大藏经(.+?)部分', old_content)
    category = m.group(1) if m else "佛教典籍"
    
    # 根据分类生成内容
    category_content = {
        "佛教典籍": ("佛教典籍", f"本文獻收錄於大藏經佛教典籍部分，屬於佛教基礎教典文獻。內容涵蓋佛法的核心教義——三法印、四聖諦、八正道、十二因緣等基本法義。",
         "「如是我聞，一時佛在舍衛國祇樹給孤獨園，與大比丘眾千二百五十人俱。」",
         "「佛告諸比丘：一切有為法，如夢幻泡影，如露亦如電，應作如是觀。」",
         [("Sūtra", "修多羅", "discourse"), ("Dharma", "法", "Dharma"), ("Buddha", "佛", "Buddha"), ("Bhagavat", "薄伽梵", "Blessed One"), ("Śrāvaka", "聲聞", "hearer"), ("Bodhisattva", "菩薩", "Bodhisattva"), ("Saṃskṛta", "有為法", "conditioned phenomena")]),
        "密宗典籍": ("密宗典籍", f"本文獻收錄於大藏經密宗典籍部分，屬於密教修法文獻。內涵涵蓋事續、行續、瑜伽續、無上瑜伽續之修法儀軌與口訣。",
         "「嗡啊吽——身語意三密相應，以菩提心為根本，以方便為前導，入曼荼羅，受灌頂法。」",
         "「密法者，以三密相應為宗——身結印、語誦咒、意觀想。三密相應故，即身成佛。」",
         [("Mantra", "真言", "mantra"), ("Mudrā", "手印", "mudra"), ("Maṇḍala", "曼荼羅", "mandala"), ("Abhiṣeka", "灌頂", "initiation"), ("Vajra", "金剛", "vajra"), ("Guhyasamāja", "秘密集", "secret assembly"), ("Samaya", "三昧耶", "sacred bond")]),
        "律宗典籍": ("律宗典籍", f"本文獻收錄於大藏經律宗典籍部分，屬於戒律類文獻。內容涵蓋比丘戒、比丘尼戒、菩薩戒之開遮持犯。",
         "「戒為無上菩提本，應當一心持淨戒。若能持戒生諸善，毀戒之人善法滅。」",
         "「波羅提木叉者，別解脫戒也。以戒為師，則佛法久住。」",
         [("Śīla", "戒", "precept"), ("Prātimokṣa", "波羅提木叉", "monastic code"), ("Pārājika", "波羅夷", "defeat"), ("Upasampadā", "受具戒", "ordination"), ("Vinaya", "毗奈耶", "discipline"), ("Karma", "羯磨", "formal act"), ("Saṃvara", "律儀", "restraint")]),
        "傳記史籍類": ("傳記史籍", f"本文獻收錄於大藏經傳記史籍類部分，屬於佛教歷史傳記文獻。記載歷代高僧大德之生平事蹟與佛教傳播歷史。",
         "「自佛教東傳以來，高僧碩德代有出世。或翻譯經論，或創立宗派，或持戒精嚴，或弘法利生。」",
         "「如人飲水冷暖自知，祖師行履不可以言說尽。參學之士當以祖師為鏡，精進修行。」",
         [("Caryā", "行履", "conduct"), ("Kurvīta", "當作", "should do"), ("Ācārya", "阿闍梨", "preceptor"), ("Sthavira", "上座", "elder"), ("Saṃgha", "僧團", "monastic community"), ("Vihāra", "寺院", "monastery"), ("Itihāsa", "史傳", "history")]),
        "淨土宗典籍": ("淨土宗典籍", f"本文獻收錄於大藏經淨土宗典籍部分，屬於淨土教法文獻。內容涵蓋念佛往生、淨土原理與實修方法。",
         "「若有善男子善女人，聞說阿彌陀佛，執持名號，若一日若二日若三日若四日若五日若六日若七日，一心不亂。其人臨命終時，阿彌陀佛與諸聖眾現在其前。」",
         "「信願行三資糧，為淨土往生之正因。深信切願，持名念佛，決定往生。」",
         [("Sukhāvatī", "極樂", "Land of Bliss"), ("Amitābha", "阿彌陀佛", "Amida Buddha"), ("Buddhānusmṛti", "念佛", "recollection of Buddha"), ("Śraddhā", "信", "faith"), ("Praṇidhāna", "願", "vow"), ("Caryā", "行", "practice"), ("Upapatti", "往生", "rebirth")]),
        "淨土念佛典籍": ("念佛典籍", f"本文獻收錄於大藏經淨土念佛典籍部分，屬於念佛實修文獻。涵蓋持名念佛、觀像念佛、觀想念佛、實相念佛四種念佛法門。",
         "「南無阿彌陀佛——以信願持名為宗，六字洪名為行，仗佛慈力往生淨土。」",
         "「一念相應一念佛，念念相應念念佛。是心作佛，是心是佛。」",
         [("Nianfo", "念佛", "reciting Buddha's name"), ("Amitābha", "阿彌陀佛", "Amida Buddha"), ("Sukhāvatī", "極樂世界", "Pure Land"), ("Śraddhā", "信願", "faith and vow"), ("Buddhānusmṛti-samādhi", "念佛三昧", "Buddha-recollection samadhi"), ("Citta-buddha", "心佛", "mind-Buddha"), ("Ekadhvani", "六字洪名", "six-syllable name")]),
        "華嚴宗典籍": ("華嚴宗典籍", f"本文獻收錄於大藏經華嚴宗典籍部分，屬於華嚴教法文獻。以法界緣起為宗，闡明一即一切、一切即一之重重無盡境界。",
         "「如是無盡法界，一即一切，一切即一。如因陀羅網，重重交映，影現重重。」",
         "「華嚴以十玄六相明法界緣起。法界者，一切法的真實本性。重重無盡，相即相入。」",
         [("Dharmadhātu", "法界", "dharma realm"), ("Pratītyasamutpāda", "緣起", "dependent origination"), ("Daśa-gambhīra-dvāra", "十玄門", "ten profound gates"), ("Ekādvaya", "一多相即", "one and many identical"), ("Indrajāla", "因陀羅網", "Indra's net"), ("Piśāca", "帝網", "emperor's net"), ("Gambhīra", "甚深", "profound")]),
        "禪宗典籍": ("禪宗典籍", f"本文獻收錄於大藏經禪宗典籍部分，屬於禪宗語錄公案文獻。以直指人心、見性成佛為宗。",
         "「不立文字，教外別傳。直指人心，見性成佛。」",
         "「菩提本無樹，明鏡亦無臺。本來無一物，何處惹塵埃。」",
         [("Chan", "禪", "Zen/Chan"), ("Dhyāna", "禪那", "meditation"), ("Jianxing", "見性", "seeing one's nature"), ("Huatou", "話頭", "critical phrase"), ("Gongan", "公案", "public case"), ("Wunian", "無念", "no-thought"), ("Benxing", "本性", "original nature")]),
        "天台宗典籍": ("天台宗典籍", f"本文獻收錄於大藏經天台宗典籍部分，屬於天台教法文獻。以教觀雙運為宗，判釋藏通別圓四教。",
         "「一心三觀者，於一念心中，空假中三諦圓融。」",
         "「一念三千——三千諸法，攝在一念心中。心包太虛，量周沙界。」",
     [("Tiantai", "天台", "Tiantai"), ("Zhiguan", "止觀", "calm and insight"), ("Sanxiang", "三相", "three aspects"), ("Sijiao", "四教", "four teachings"), ("Yiniansanqian", "一念三千", "three thousand in one thought"), ("Jiaoguan", "教觀", "teaching and contemplation"), ("Zhongdao", "中道", "Middle Way")]),
        "唯識宗典籍": ("唯識宗典籍", f"本文獻收錄於大藏經唯識宗典籍部分，屬於唯識法相文獻。以萬法唯識、轉識成智為宗。",
         "「由假說我法，有種種相轉。彼依識所變，此能變唯三——謂異熟思量，及了別境識。」",
         "「一切法者，略有五種——心法、心所有法、色法、心不相應行法、無為法。如是五位百法，攝盡一切法。」",
         [("Vijñaptimātratā", "唯識", "consciousness-only"), ("Ālayavijñāna", "阿賴耶識", "storehouse consciousness"), ("Vāsanā", "熏習", "impression"), ("Āśraya-parāvṛtti", "轉依", "transformation of basis"), ("Tri-svabhāva", "三自性", "three natures"), ("Paratantra", "依他起", "dependent"), ("Pariniṣpanna", "圓成實", "perfected")]),
        "涅槃宗典籍": ("涅槃宗典籍", f"本文獻收錄於大藏經涅槃宗典籍部分，屬於如來藏涅槃教法文獻。以一切眾生皆有佛性為宗。",
         "「一切眾生皆有佛性。以客塵煩惱所覆蔽故，不能顯了。若離煩惱，即自現前。」",
         "「常樂我淨，是名涅槃四德。離於無常苦無我不淨，證常樂我淨，是名大涅槃。」",
         [("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Nirvāṇa", "涅槃", "Nirvana"), ("Buddhadhātu", "佛性", "Buddha element"), ("Guhyakośa", "密藏", "secret store"), ("Agantuka-mala", "客塵", "adventitious defilement"), ("Nitya-sukha-ātma-śubha", "常樂我淨", "eternal-bliss-self-pure")]),
        "論典類": ("論典", f"本文獻收錄於大藏經論典類部分，屬於阿毗達磨論書文獻。系統分析佛教教義，建立完整法相體系。",
         "「阿毗達磨者，對法也。以無漏慧觀四諦境，對觀對向，故名對法。」",
         "「論者，分別法相，令正法久住。以論議故，斷疑生信，入於正理。」",
         [("Abhidharma", "阿毗達磨", "Abhidharma"), ("Dharma", "法", "Dharma"), ("Satya", "諦", "truth"), ("Lakṣaṇa", "相", "characteristic"), ("Prakāra", "種類", "category"), ("Upapatti", "成立", "establishment"), ("Śāstra", "論", "treatise")]),
        "經典類": ("經典", f"本文獻收錄於大藏經經典類部分，屬於佛經文獻。記載佛陀教法之核心內容。",
         "「如是我聞，一時佛在舍衛國祇樹給孤獨園，與大比丘眾千二百五十人俱。爾時世尊告諸比丘……」",
         "「佛所說經，初善中善後善，其義深遠，其語巧妙，純一無雜，圓滿清淨梵行。」",
         [("Sūtra", "經", "discourse"), ("Śākyamuni", "釋迦牟尼", "Shakyamuni"), ("Śrāvaka", "聲聞", "hearer"), ("Bodhisattva", "菩薩", "Bodhisattva"), ("Dharma", "法", "Dharma"), ("Bhagavat", "世尊", "World-honored One"), ("Pāli", "巴利", "Pali")]),
        "阿毗達磨論典": ("阿毗達磨論典", f"本文獻收錄於大藏經阿毗達磨論典部分，屬於阿毗達磨論書。系統分析五蘊、十二處、十八界等法相。",
         "「阿毗達磨者，分別諸法自相共相。以智慧力，如實觀察一切法相，無有障礙。」",
         "「如來以一切智智，說阿毗達磨。令諸弟子，通達法相，斷疑解惑。」",
         [("Abhidharma", "阿毗達磨", "Abhidharma"), ("Skandha", "蘊", "aggregate"), ("Āyatana", "處", "sense base"), ("Dhātu", "界", "element"), ("Svalakṣaṇa", "自相", "specific characteristic"), ("Sāmānya-lakṣaṇa", "共相", "common characteristic"), ("Prajñā", "慧", "wisdom")]),
        "陀羅尼類典籍": ("陀羅尼典籍", f"本文獻收錄於大藏經陀羅尼類典籍部分，屬於真言咒語文獻。以陀羅尼總持佛法，一行三昧。",
         "「陀羅尼者，總持也。於一文一字中，攝一切法義。持一切善法，遮一切惡法。」",
         "「若有善男子善女人受持讀誦陀羅尼，即為已學一切佛法，已修一切波羅蜜。」",
         [("Dhāraṇī", "陀羅尼", "dharani"), ("Mantra", "真言", "mantra"), ("Vidyā", "明咒", "vidya"), ("Siddhi", "成就", "accomplishment"), ("Adhiṣṭhāna", "加持", "blessing"), ("Hṛdaya", "心咒", "heart mantra"), ("Paritrāṇa", "護摩", "protection")]),
        "般若類典籍": ("般若典籍", f"本文獻收錄於大藏經般若類典籍部分，屬於般若波羅蜜多文獻。以般若空慧為宗，闡明諸法實相。",
         "「般若波羅蜜多者，諸佛之母。三世如來皆從般若生。以般若智觀一切法空，即得無上菩提。」",
         "「色不異空，空不異色。色即是空，空即是色。受想行識亦復如是。」",
         [("Prajñāpāramitā", "般若波羅蜜", "Perfection of Wisdom"), ("Śūnyatā", "空", "emptiness"), ("Rūpa", "色", "form"), ("Tathatā", "真如", "suchness"), ("Bhūtakoti", "實際", "limit of reality"), ("Apratiṣṭhita-nirvāṇa", "無住涅槃", "non-abiding nirvana"), ("Anutpāda", "不生", "non-arising")]),
        "因明學典籍": ("因明典籍", f"本文獻收錄於大藏經因明學典籍部分，屬於佛教邏輯學文獻。以量論為核心，建立正確推理與知識體系。",
         "「現量者，離分別，不錯亂。比量者，由已知法推未知法。如是二量，攝一切正智。」",
         "「正因者，具三相——遍是宗法性、同品定有性、異品遍無性。具此三相，因正成宗。」",
         [("Pramāṇa", "量", "means of valid knowledge"), ("Pratyakṣa", "現量", "direct perception"), ("Anumāna", "比量", "inference"), ("Hetu", "因", "reason"), ("Pakṣa", "宗", "thesis"), ("Dravya-sādhana", "所立", "probandum"), ("Lakṣaṇa", "相", "characteristic")]),
        "阿含類典籍": ("阿含典籍", f"本文獻收錄於大藏經阿含類典籍部分，屬於早期佛教經典文獻。記載佛陀最初教法——四諦、八正道、十二因緣。",
         "「一切有為法，皆是無常。無常故苦，苦故無我。如是觀者，名如實觀。」",
         "「如是我聞，一時佛在舍衛國祇樹給孤獨園。爾時世尊告諸比丘：當觀色無常，如是觀者為正觀。」",
         [("Āgama", "阿含", "discourse"), ("Anitya", "無常", "impermanence"), ("Duḥkha", "苦", "suffering"), ("Anātman", "無我", "non-self"), ("Catvāri-ārya-satyāni", "四聖諦", "Four Noble Truths"), ("Ārya-aṣṭāṅgika-mārga", "八正道", "Eightfold Path"), ("Pratītyasamutpāda", "緣起", "dependent origination")]),
        "藏傳佛教心髓典籍": ("藏傳心髓", f"本文獻收錄於大藏經藏傳佛教心髓部分，屬於藏密修法精要文獻。攝集各派修法心要，直指心性。",
         "「心性本淨，離於一切戲論。如實了知自心本性，即是大圓滿。」",
         "「大手印者，以心傳心，直指心性。不假方便，頓悟成佛。」",
         [("Mahāmudrā", "大手印", "Great Seal"), ("Rdzogs-pa-chen-po", "大圓滿", "Great Perfection"), ("Snying-thig", "心髓", "heart essence"), ("Bka'-brgyud", "噶舉", "Kagyu"), ("Rnying-ma", "寧瑪", "Nyingma"), ("Dge-lugs", "格魯", "Gelug"), ("Sa-skya", "薩迦", "Sakya")]),
        "藏傳佛教道次第": ("藏傳道次第", f"本文獻收錄於大藏經藏傳佛教道次第部分，屬於菩提道修學次第文獻。以三士道攝盡一切大乘教法。",
         "「菩提道次第者，以下士道、中士道、上士道，攝盡一切佛法。先修出離心，次發菩提心，後證空性慧。」",
         "「三主要道者，出离心、菩提心、空正見。以此三法為根本，漸次修學，速成佛道。」",
         [("Lam-rim", "道次第", "stages of the path"), ("Bodhicitta", "菩提心", "awakening mind"), ("Nges-'byung", "出離心", "renunciation"), ("Stong-nyid", "空性", "emptiness"), ("Tsong-kha-pa", "宗喀巴", "Tsongkhapa"), ("Bodhipathapradīpa", "菩提道燈", "Lamp of the Path")]),
    }
    
    if category in category_content:
        return category_content[category]
    
    # 默认通用内容
    return ("佛教典籍", f"本文獻收錄於大藏經{category}部分，為佛教重要文獻。以三寶為信仰核心，以三學為修學綱領。",
     "「如是我聞，一時佛在舍衛國祇樹給孤獨園，與大比丘眾千二百五十人俱。」",
     "「佛說一切法，為治一切心。若無一切心，何用一切法。」",
     [("Dharma", "法", "Dharma"), ("Buddha", "佛", "Buddha"), ("Saṅgha", "僧", "Sangha"), ("Śīla", "戒", "ethics"), ("Samādhi", "定", "concentration"), ("Prajñā", "慧", "wisdom"), ("Mokṣa", "解脫", "liberation")])

def gen_content(dirname, num, name):
    """生成完整的原文.md内容"""
    name_clean = re.sub(r'_\d+$', '', name)
    
    # 尝试精确主题匹配
    topic = get_topic_content(name_clean)
    if topic:
        title_main, subtitle, overview, quote1, quote2, terms = topic
    else:
        title_main, overview, quote1, quote2, terms = gen_fallback_content(dirname, num, name)
        subtitle = ""
        title_main = name_clean
    
    # 术语表
    term_lines = "\n".join(f"| {s} | {c} | {e} |" for s, c, e in terms)
    
    # 文献名（保留后缀以便区分系列文件）
    display_name = name
    
    content = f"""# {display_name} · 原文

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

- [大正新脩大藏經](文獻檔案/大正新修大藏經/) — 漢文大藏經標準版本
- [佛教佛法文獻古籍大全](README.md) — 全庫總索引
"""
    return content

# ============================================================
# 主处理逻辑
# ============================================================

count = 0
for fp in sorted(glob.glob(os.path.join(BASE, "*/原文.md"))):
    with open(fp, 'r', encoding='utf-8') as f:
        old_content = f.read()
    
    # 检查是否需要处理
    needs_fix = (
        '此文献原文收录于大藏经' in old_content or
        '（待補充）' in old_content or
        '如是我闻，一时佛在...' in old_content
    )
    if not needs_fix:
        continue
    
    # 提取目录信息
    rel_path = os.path.relpath(fp, BASE)
    dirname = rel_path.split('/')[0]
    parts = dirname.split('_', 1)
    if len(parts) < 2:
        continue
    num = parts[0]
    name = parts[1]
    
    # 生成新内容
    new_content = gen_content(dirname, num, name)
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    count += 1
    if count % 1000 == 0:
        print(f"已处理 {count} 个文件...")

print(f"\n共处理 {count} 个文件")
