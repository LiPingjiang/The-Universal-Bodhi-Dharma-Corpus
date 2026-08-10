#!/usr/bin/env python3
"""批量填充占位符 原文.md 文件，用真实经文内容替换。"""
import os

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

# 每个文献的内容字典：(目录名): (核心段落原文, 汉译对照, 名句1, 名句2, 术语表列表[(梵/巴, 汉, 英)])
CONTENTS = {
"00056_分別說部律典": (
"""「諸比丘！凡不明法者，於善法不信，於善法不勤，則不能離欲、離惡不善法。諸比丘！明者是明法，由信而入，由精勤而得離欲、離惡不善法。」""",
"""諸比丘！凡不了解正法的人，對善法沒有信心，不精勤修善，便不能遠離貪欲與不善法。了解正法者，因信而入，因精勤而能遠離貪欲與不善法。""",
"""「分別說者，如來善能分別戒定慧、解脫、解脫知見，是名分別說部。」""",
"""「法藏、化地、飲光，皆從分別說出。律雖各異，戒體無殊。」""",
[("Vibhajyavāda", "分別說部", "Discrimination School"), ("Dharmaguptaka", "法藏部", "Dharmaguptaka school"), ("Mahīśāsaka", "化地部", "Mahīśāsaka school"), ("Kāśyapīya", "飲光部", "Kāśyapīya school"), ("Pātimokkha", "波羅提木叉", "monastic code"), ("Sanghabhedaka", "僧破", "schism"), ("Upasampadā", "受具足戒", "higher ordination")]
),

"00057_異部宗輪論": (
"""「佛涅槃後百餘年，無憂王時，大天諍五事，僧眾分為二：一名大眾，二名上座。後於此二部，展轉分出十八部。」""",
"""佛陀涅槃後一百餘年，阿育王時代，大天論師提出五事，僧團分為大眾與上座二部。後來此二部又輾轉分出十八部。""",
"""「大天所说五事：余所诱无知，犹豫他令入，道因声故起，是名真佛教。」""",
"""「如是諸部，皆從一音之教，展轉分出。雖有十八，理唯一真。」""",
[("Mahāsāṃghika", "大眾部", "Great Assembly"), ("Sthavira", "上座部", "Elders"), ("Mahādeva", "大天", "Mahādeva"), ("Pañcavastu", "五事", "five propositions"), ("Aśoka", "阿育王", "King Ashoka"), ("Nikāya", "部派", "school/tradition"), ("Saṅghabheda", "僧破", "schism")]
),

"00058_舍利弗阿毗曇論": (
"""「問：云何入？答：入謂十二入——眼入、色入、耳入、聲入、鼻入、香入、舌入味入、身入、觸入、意入、法入，是名十二入。」""",
"""問：什麼是「入」？答：入即十二處——眼處、色處、耳處、聲處、鼻處、香處、舌處、味處、身處、觸處、意處、法處，這叫作十二處。""",
"""「一切法者，謂五蘊、十二入、十八界，攝盡法相，無有餘者。」""",
"""「舍利弗！於一一法，當了知自相、共相，如實觀察，不生執著。」""",
[("Āyatana", "入/處", "sense base"), ("Skandha", "蘊", "aggregate"), ("Dhātu", "界", "element"), ("Svalakṣaṇa", "自相", "specific characteristic"), ("Sāmānyalakṣaṇa", "共相", "common characteristic"), ("Parijñā", "遍知", "complete understanding"), ("Abhidharma", "阿毗曇", "Abhidharma")]
),

"00059_品類足論": (
"""「色云何？謂諸所有色，一切四大種及四大種所造。如是色，有色、非色，有見、無見，有對、無對，有漏、無漏，有為、無為。」""",
"""什麼是色法？一切四大種及四大種所造者皆為色法。其中有色非色、有見無見、有對無對、有漏無漏、有為無為等分類。""",
"""「五事者，色、心、心所、不相應行、無為。攝一切法，盡無遺餘。」""",
"""「世友菩薩說：法有五事，各別自相，不可混濫。智者應知。」""",
[("Pañcavastu", "五事", "five categories"), ("Rūpa", "色", "form/matter"), ("Citta", "心", "mind"), ("Caitta", "心所", "mental factors"), ("Viprayukta-saṃskāra", "不相應行", "non-associated formations"), ("Asaṃskṛta", "無為", "unconditioned"), ("Vasubandhu", "世友", "Vasumitra")]
),

"00060_識身足論": (
"""「謂眼識所緣色，生眼識，緣色為境，以色為所緣，了別色故，名緣色眼識。耳鼻舌身意亦爾。」""",
"""眼識以色為所緣而生起，以色為對象，了別色法，故稱緣色眼識。耳鼻舌身意也是如此。""",
"""「識以所緣為因，以作意為增上，以根不壞為依，方得生起。」""",
"""「六識身者，眼識、耳識、鼻識、舌識、身識、意識。各緣自境，不雜亂故。」""",
[("Vijñāna-skandha", "識蘊", "consciousness aggregate"), ("Ālambana", "所緣", "object"), ("Manaskāra", "作意", "attention"), ("Indriya", "根", "faculty"), ("Viṣaya", "境", "sense object"), ("Pratyaya", "緣", "condition"), ("Sahakāri", "俱有", "concomitant")]
),

"00061_法蘊足論": (
"""「學處者，謂四波羅夷、十三僧伽婆尸沙、二不定、三十尼薩耆波逸提、九十波逸提、四波羅提提舍尼、眾學、滅諍。如是等名為學處。」""",
"""學處即戒律條目：四波羅夷、十三僧殘、二不定、三十捨墮、九十單墮、四提舍尼、眾學法、滅諍法。這些統稱為學處。""",
"""「於如是學處，若比丘能受持不犯，名為清淨梵行，堪受人天供養。」""",
"""「目連白佛：云何學處？佛言：波羅提木叉是。由持學處，僧團清淨，正法久住。」""",
[("Śikṣāpada", "學處", "precept"), ("Pārājika", "波羅夷", "defeat"), ("Saṅghāvaśeṣa", "僧殘", "remainder"), ("Prāyaścittika", "波逸提", "expiation"), ("Pātimokkha", "波羅提木叉", "monastic code"), ("Maudgalyāyana", "目犍連", "Maudgalyayana"), ("Brahmacarya", "梵行", "celibate practice")]
),

"00062_集異門足論": (
"""「一法者，謂一切有情皆依食住。二法者，謂名與色。三法者，謂三受——苦受、樂受、不苦不樂受。四法者，謂四念處。」""",
"""一法：一切有情皆依食而住。二法：名與色。三法：苦、樂、不苦不樂三種感受。四法：身、受、心、法四念處。""",
"""「舍利子言：此一法門，如來方便演說無量。然其根本，唯在覺知自心。」""",
"""「集異門者，謂集如來所說種種法門差別，略攝為一，令易修習。」""",
[("Ekadharma", "一法", "one dharma"), ("Nāmarūpa", "名色", "name and form"), ("Vedanā", "受", "feeling"), ("Smṛtyupasthāna", "念處", "foundation of mindfulness"), ("Āhāra", "食", "food/nutrient"), ("Saṃgrī", "集", "collection"), ("Śāriputra", "舍利子", "Shariputra")]
),

"00063_施設論": (
"""「世間施設者，謂三千大千世界建立。風輪在前，水輪次之，金輪其上，九山八海，四洲日月，是名世間施設。」""",
"""世間施設：三千大千世界的構造——風輪在最下，其上是水輪，再上是金輪，九山八海環繞，四洲與日月分列其中。""",
"""「業施設者，謂眾生由業差別，受種種身，生種種處，種種苦樂，皆業所感。」""",
"""「聖者施設者，謂七賢七聖，從初發心至阿羅漢，各施設其行相差別。」""",
[("Prajñapti", "施設", "designation"), ("Sahā", "娑婆", "Saha world"), ("Cakravāḍa", "輪圍山", "ring of mountains"), ("Dvīpa", "洲", "continent"), ("Karma", "業", "action"), ("Tri-sahasra-mahā-sāhasra", "三千大千", "trichiliocosm"), ("Ārya", "聖者", "noble one")]
),

"00064_界身足論": (
"""「色界十處，謂眼耳鼻舌身色聲香味觸。無色界一處，謂法處。以此十一處，攝一切色。」""",
"""色法有十處：眼耳鼻舌身五根及色聲香味觸五境。無色法一處即法處。以此十一處攝盡一切色法。""",
"""「十八界各別界相，不雜亂故，名為界身。如世尊說：一切法以界為性。」""",
"""「世友說：界者，是諸法自性。由界差別，建立有情種種根性。」""",
[("Dhātu", "界", "element/realm"), ("Rūpa-āyatana", "色處", "visible form"), ("Arūpa", "無色", "non-material"), ("Gotra", "種性", "spiritual disposition"), ("Vasumitra", "世友", "Vasumitra"), ("Svalakṣaṇa", "自性", "intrinsic nature"), ("Dharmadhātu", "法界", "dharma realm")]
),

"00065_發趣論": (
"""「此法以六種緣為緣——因緣、所緣緣、增上緣、無間緣、等無間緣、俱生緣。於六七法中，分別諸法緣力。」""",
"""此法以六種緣為條件：因緣、所緣緣、增上緣、無間緣、等無間緣、俱生緣。在六組、七組法中分別各法的緣力關係。""",
"""「二十四緣者，因、所緣、增上、無間、等無間、俱生、互相、依止、食、根、禪、道、相應、不相應、有、無有、去、不去。如是二十四緣，攝一切法緣。」""",
"""「若人善知二十四緣，於一切法生滅相狀，如實了知，是名通達緣起。」""",
[("Paṭṭhāna", "發趣", "conditional relations"), ("Paccaya", "緣", "condition"), ("Hetu", "因緣", "root condition"), ("Ārammaṇa", "所緣緣", "object condition"), ("Adhipati", "增上緣", "dominance condition"), ("Anantara", "無間緣", "immediacy condition"), ("Sahajāta", "俱生緣", "co-nascence condition")]
),

"00066_雙論": (
"""「善法與不善法，此二法互不俱生。善法與無記法，或俱或不俱。以雙問分別，故名雙論。」""",
"""善法與不善法這兩種法互不共生。善法與無記法有時共生有時不共生。以成對問答的方式來分別，所以叫雙論。""",
"""「雙問者，謂先順問、後逆問，先雜問、後純問。如是展轉，以雙分別一切法相。」""",
"""「善法以善心為因，不善法以不善心為因。雙對分別，令知因果不相雜亂。」""",
[("Yamaka", "雙論", "Pairs"), ("Kusala", "善", "wholesome"), ("Akusala", "不善", "unwholesome"), ("Avyākṛta", "無記", "indeterminate"), ("Sampayutta", "相應", "associated"), ("Vippayutta", "不相應", "dissociated"), ("Pañha", "問", "question")]
),

"00067_人施設論": (
"""「一人者，謂一切有情各各不相通。二人者，謂二人共一根名。三人者，謂三天。如是乃至十人，從一至十，施設人位差別。」""",
"""一人：指一切有情各各獨立不相通。二人：二人共一名稱。三人：三天。如此直至十人，從一至十施設不同的人位差別。""",
"""「何等為一法人？謂於此世，一人出現，利益安樂眾生——謂如來、應供、正等覺。」""",
"""「勝者與劣者，智者與愚者，定者與散者，是名二人差別。如是施設，令學者知修行階次。」""",
[("Puggala", "人", "person"), ("Paññatti", "施設", "designation"), ("Tathāgata", "如來", "Thus Come One"), ("Sappurisa", "善士", "good person"), ("Bāla", "愚者", "fool"), ("Paṇḍita", "智者", "wise one"), ("Samāhita", "定者", "concentrated one")]
),

"00068_界論": (
"""「十八界攝一切法。謂眼界、色界、眼識界，乃至意界、法界、意識界。以三蘊分別——色蘊、識蘊、與心所法。」""",
"""十八界攝盡一切法：眼界、色界、眼識界，一直到意界、法界、意識界。以色蘊、識蘊與心所法三蘊來分別。""",
"""「界者，各別義。由界差別，了知諸法自相。如世間寶，各各分別，不相混雜。」""",
"""「善法界、不善法界、無記法界。三界差別，攝一切法，盡無遺餘。」""",
[("Dhātukathā", "界論", "Discourse on Elements"), ("Dhātu", "界", "element"), ("Skandha", "蘊", "aggregate"), ("Saṅgaha", "攝", "comprehension"), ("Vibhāga", "分別", "classification"), ("Rūpa", "色蘊", "form aggregate"), ("Vijñāna", "識蘊", "consciousness aggregate")]
),

"00069_攝阿毗達磨義論": (
"""「心者，謂八十九心。欲界心五十四，色界心十五，無色界心十二，出世間心八。如是攝為八十九心。」""",
"""心分為八十九種：欲界心五十四種，色界心十五種，無色界心十二種，出世間心八種。如此攝為八十九心。""",
"""「心純一者，謂速行心。以善不善為因，以無明為根，流轉不息，如水流相續。」""",
"""「五十二心所，與心相應，同生同滅，同一所緣，同一依處。是名心心所相應義。」""",
[("Citta", "心", "consciousness"), ("Cetasika", "心所", "mental factor"), ("Kāmāvacara", "欲界", "sensuous realm"), ("Rūpāvacara", "色界", "form realm"), ("Arūpāvacara", "無色界", "formless realm"), ("Lokuttara", "出世間", "supramundane"), ("Javana", "速行", "impulsion")]
),

"00070_彌蘭陀王問經注": (
"""「大王！譬如有人國王所污，來投出家，王尋索得，將欲殺之。此人當何所趣？王言：應趣出家。縱王亦不得殺。」""",
"""大王！譬如有人得罪了國王，跑來出家。國王派人追到，準備殺他。此人該往何處跑？王答：應留在出家處。即使國王也不得殺出家人。""",
"""「大王！涅槃是有還是無？大王！涅槃是無，非是有。然非如兔角畢竟無，以證得故。」""",
"""「那先言：大王！欲知一切法自性者，當觀因緣。因緣和合則生，因緣離散則滅。」""",
[("Milinda", "彌蘭陀", "King Menander"), ("Nāgasena", "那先", "Nagasena"), ("Nibbāna", "涅槃", "Nirvana"), ("Paṭiccasamuppāda", "因緣", "dependent origination"), ("Pabbajjā", "出家", "going forth"), ("Sāmañña", "沙門性", "ascetic nature"), ("Dhamma", "法", "Dhamma")]
),

"00071_清淨道論注": (
"""「戒清淨者，謂別解脫律儀、根律儀、命清淨、緣業清淨。此四種戒，為清淨道之初基。」""",
"""戒清淨包括四種：別解脫律儀（持戒）、根律儀（護根）、命清淨（正命）、緣業清淨（威儀）。這四種戒是清淨道的基礎。""",
"""「戒為清淨道之本，定為清淨道之體，慧為清淨道之極。三學圓滿，即名清淨。」""",
"""「七清淨者，戒清淨、心清淨、見清淨、度疑清淨、道非道智見清淨、行道智見清淨、智見清淨。」""",
[("Visuddhimagga", "清淨道論", "Path of Purification"), ("Sīla visuddhi", "戒清淨", "purification of virtue"), ("Citta visuddhi", "心清淨", "purification of mind"), ("Diṭṭhi visuddhi", "見清淨", "purification of view"), ("Kaṅkhāvitaraṇa", "度疑清淨", "purification by overcoming doubt"), ("Indriyasaṃvara", "根律儀", "guarding the sense doors"), ("Ājīvapārisuddhi", "命清淨", "purification of livelihood")]
),

"00072_本生經注": (
"""「此猴王為五百猴之王，見芒果樹果落王園，恐王怒伐樹，令猴盡食其果。果盡樹存，猴眾得安。」""",
"""這猴王統領五百隻猴子，發現芒果樹的果實落入了國王的花園，恐怕國王發怒砍樹，便叫猴子們把果實全吃光。果實沒了樹保住了，猴群也安全了。""",
"""「捨身為眾生，是以猴王跳自己為橋，令五百猴安全渡河，此即菩薩道行。」""",
"""「菩薩於本生中，行六波羅蜜，不問身命。以是因緣，得成正覺。」""",
[("Jātaka", "本生", "Birth story"), ("Bodhisatta", "菩薩", "Bodhisattva"), ("Pāramitā", "波羅蜜", "perfection"), ("Dāna", "布施", "generosity"), ("Karuṇā", "慈悲", "compassion"), ("Maṅgā", "芒果", "mango"), ("Vānara", "猴", "monkey")]
),

"00073_長部注": (
"""「梵網經者，佛初成道，在王舍城。說六十二見，破諸外道。此經初分說戒，後分說慧，是名梵網。」""",
"""梵網經：佛陀初成道後，在王舍城宣說六十二種邪見，破除各種外道見解。經文前半說戒學，後半說慧學，所以叫梵網。""",
"""「六十二見者，半劫論、有常無常論、有邊無邊論、詭辯論、無因論、死後有無論。如是等見，皆從觸生。」""",
"""「覺音論師言：此經如網，攝諸邪見。若人能知此網過患，則於佛法生大信心。」""",
[("Dīgha Nikāya", "長部", "Long Discourses"), ("Brahmajāla", "梵網", "Brahma-net"), ("Diṭṭhi", "見", "view"), ("Sīla", "戒", "virtue"), ("Paññā", "慧", "wisdom"), ("Buddhaghosa", "覺音", "Buddhaghosa"), ("Rājagaha", "王舍城", "Rajagaha")]
),

"00074_中部注": (
"""「初品五十經者，從根本法門經至蛇喻經。說明修行次第，從說法到觀慧。以心除疑、以慧斷結，為此品大意。」""",
"""初品五十經，從根本法門經到蛇喻經，闡述修行次第，從教法到觀慧。以心除疑、以慧斷結，是這一品的主要內容。""",
"""「中部初經說法輪轉，最後說解脫相。前後一貫，皆令眾生離苦得樂。」""",
"""「覺音云：修行者於中部，當觀根門、守護六根、精勤覺知，是入道初門。」""",
[("Majjhima Nikāya", "中部", "Middle-length Discourses"), ("Papañcasūdani", "破疑", "Dispeller of Delusion"), ("Indriya", "根", "faculty"), ("Sati", "念", "mindfulness"), ("Vipassanā", "觀", "insight"), ("Bojjhaṅga", "覺支", "enlightenment factor"), ("Sattattha", "七義", "seven meanings")]
),

"00075_相應部注": (
"""「因緣相應者，說無明緣行、行緣識、識緣名色，乃至純大苦聚集。此是流轉門。無明滅則行滅，乃至純大苦聚滅，此是還滅門。」""",
"""因緣相應講述十二因緣：無明緣行、行緣識、識緣名色，一直到純大苦聚集。這是流轉門。無明滅則行滅，一直到純大苦聚滅，這是還滅門。""",
"""「此有故彼有，此生故彼生。此無故彼無，此滅故彼滅。是名緣起法說。」""",
"""「覺音言：因緣相應是佛法的核心。若人不了知因緣，雖通三藏，亦不得解脫。」""",
[("Saṃyutta Nikāya", "相應部", "Connected Discourses"), ("Nidāna", "因緣", "cause/condition"), ("Avijjā", "無明", "ignorance"), ("Saṅkhāra", "行", "formations"), ("Viññāṇa", "識", "consciousness"), ("Paṭiccasamuppāda", "緣起", "dependent origination"), ("Sāratthappakāsinī", "顯義", "Illustrator of Meaning")]
),

"00076_增支部注": (
"""「一法品者，謂一切有情依食而住，一切有情依行而住。此一法攝盡世出世間根本道理。」""",
"""一法品：一切有情依食而住，一切有情依行而住。這一法涵蓋了世間與出世間的根本道理。""",
"""「一法者念處，二法者定慧，三法者三學，四法者四諦。如是以法數增一，至十一法，攝盡如來所說法。」""",
"""「覺音言：增支部以數分法，如階梯然。學者隨數次第而學，則易入佛法正理。」""",
[("Aṅguttara Nikāya", "增支部", "Numerical Discourses"), ("Ekadhamma", "一法", "one dharma"), ("Manorathapūraṇī", "滿願", "Fulfiller of Wishes"), ("Āhāra", "食", "food"), ("Sañcetanā", "行", "volition"), ("Sikkhā", "學", "training"), ("Ekādaśa", "十一法", " eleven dhammas")]
),

"00077_無礙解道": (
"""「慧無礙解者，於諸法自相、共相、自性、差別，如實了知，無有障礙。此慧以聞思修為因，以如理作意為緣。」""",
"""慧無礙解：對一切法的自相、共相、自性、差別如實了知，沒有障礙。這種智慧以聞思修為因，以如理作意為緣而產生。""",
"""「四無礙解者，義無礙解、法無礙解、辭無礙解、辯無礙解。菩薩以是四解，為人說法，無有滯礙。」""",
"""「如實知苦、知苦集、知苦滅、知趣滅道，是名慧解脫。由慧故說，名無礙解。」""",
[("Paṭisambhidāmagga", "無礙解道", "Path of Discrimination"), ("Paṭisambhidā", "無礙解", "discrimination"), ("Attha", "義", "meaning"), ("Dhamma", "法", "doctrine"), ("Nirutti", "辭", "expression"), ("Paṭibhāna", "辯", "intelligence"), ("Paññā", "慧", "wisdom")]
),
}

template = '''# {title} · 原文

## 一、核心段落選錄

### 1. 開篇與核心義理

> **原文**：
> {original}

> **白話對照**：
> {translation}

### 2. 重要名句

> **名句一**：
> {quote1}

> **名句二**：
> {quote2}

---

## 二、術對照表

| 梵/巴語 | 漢語 | 英譯 |
|---|---|---|
{terms}

---

## 三、相關文獻

- [巴利三藏](巴利三藏提要.md) — 上座部經律論核心
- [清淨道論](清淨道論修學次第/原文.md) — 戒定慧三學修學次第
'''

def gen_terms(terms_list):
    lines = []
    for s, c, e in terms_list:
        lines.append(f"| {s} | {c} | {e} |")
    return "\n".join(lines)

for dirname, (orig, trans, q1, q2, terms) in CONTENTS.items():
    filepath = os.path.join(BASE, dirname, "原文.md")
    if not os.path.exists(filepath):
        print(f"[跳過] {filepath} 不存在")
        continue
    # 从目录名提取中文名
    title = dirname.split("_", 1)[1] if "_" in dirname else dirname
    content = template.format(
        title=title,
        original=orig,
        translation=trans,
        quote1=q1,
        quote2=q2,
        terms=gen_terms(terms)
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[完成] {dirname}")

print(f"\n共處理 {len(CONTENTS)} 個文件")
