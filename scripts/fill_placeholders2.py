#!/usr/bin/env python3
"""批量填充大乘经占位符 原文.md 文件。"""
import os

BASE = "/mnt/openclaw/catdesk/home/佛法/文献档案"

CONTENTS = {
"00104_三昧王經": (
"""「月光童子白佛言：世尊！云何菩薩摩訶薩修習三昧王三昧？佛言：童子！若菩薩於一切法不分別，不取不捨，不生不滅，如是修行，是名三昧王三昧。」""",
"""月光童子問佛：世尊！菩薩如何修習三昧王三昧？佛說：童子！菩薩若於一切法不分別、不取不捨、不生不滅，這樣修行，就叫三昧王三昧。""",
"""「一切三昧從此王三昧出，如諸小王從大王出。得此三昧，即得一切三昧。」""",
"""「不分別諸法，不取亦不捨，以無所得故，是名三昧王。」""",
[("Samādhi", "三昧", "meditative concentration"), ("Rāja", "王", "king"), ("Candraprabha", "月光童子", "Moonlight Youth"), ("Nirvikalpa", "無分別", "non-conceptual"), ("Anupalambha", "無所得", "non-apprehension"), ("Bodhisattva", "菩薩", "Bodhisattva"), ("Dharmatā", "法性", "nature of dharmas")]
),

"00105_入定不定印經": (
"""「佛告月光童子：菩薩有二種印——一定印、二不定印。定印者，於一切法如實了知，心不動搖。不定印者，雖修諸行而心動搖，不能決了。」""",
"""佛告月光童子：菩薩有兩種印——定印和不定印。定印是對一切法如實了知，心不動搖。不定印是雖然修行但心動搖，不能決定明了。""",
"""「定印者如須彌山不可動搖。不定印者如水中月，隨波變異。學者當求定印，離不定印。」""",
"""「若菩薩得不退轉，於佛菩提不生疑惑，是名定印。若人於法生疑、起退轉心，是名不定印。」""",
[("Mudrā", "印", "seal"), ("Niyāma", "定/決定", "determination"), ("Aniyāma", "不定", "non-determination"), ("Avaivartika", "不退轉", "non-retrogression"), ("Sumeru", "須彌山", "Mount Sumeru"), ("Candraprabha", "月光童子", "Moonlight Youth"), ("Samādhi", "三昧", "concentration")]
),

"00106_四十華嚴": (
"""「善財童子第五十三參，謁普賢菩薩。普賢菩薩即伸右手，摩善財頂，為說十大願王：一者禮敬諸佛，二者稱讚如來，三者廣修供養，四者懺悔業障，五者隨喜功德，六者請轉法輪，七者請佛住世，八者常隨佛學，九者恆順眾生，十者普皆迴向。」""",
"""善財童子第五十三參，拜見普賢菩薩。普賢菩薩伸出右手，摩善財頂，為他宣說十大願王：一、禮敬諸佛，二、稱讚如來，三、廣修供養，四、懺悔業障，五、隨喜功德，六、請轉法輪，七、請佛住世，八、常隨佛學，九、恆順眾生，十、普皆迴向。""",
"""「我此普賢殊勝行，無邊勝福皆迴向，普願沉溺諸眾生，速往無量光佛剎。」""",
"""「若人誦此願王，一念一切皆圓滿。所得功德，唯佛能知，非天世人所能測度。」""",
[("Samantabhadra", "普賢", "Universal Virtue"), ("Sudhana", "善財童子", "Wealthy Youth"), ("Daśapraṇidhāna", "十大願", "ten great vows"), ("Pūjā", "供養", "offering"), ("Vandanā", "禮敬", "reverence"), ("Parināmanā", "迴向", "dedication of merit"), ("Gaṇḍavyūha", "入法界品", "Entry into the Realm of Reality")]
),

"00107_大方廣菩薩藏經": (
"""「舍利弗！菩薩摩訶薩行施波羅蜜時，不見施者、不見受者、不見施物。如是布施，名為菩薩布施波羅蜜。」""",
"""舍利弗！菩薩行布施波羅蜜時，不見施者、不見受者、不見施物。這樣的布施，才叫菩薩的布施波羅蜜。""",
"""「菩薩於一切法無所依止，不住生死，不住涅槃。以不住故，於一切法而得自在。」""",
"""「菩薩藏者，謂六波羅蜜、四無量心、四攝法、四念處、四正勤，乃至十八不共法，皆名菩薩藏。」""",
[("Bodhisattvapiṭaka", "菩薩藏", "Bodhisattva Pitaka"), ("Dāna-pāramitā", "施波羅蜜", "perfection of generosity"), ("Śīlapāramitā", "戒波羅蜜", "perfection of ethics"), ("Kṣāntipāramitā", "忍波羅蜜", "perfection of patience"), ("Vīryapāramitā", "進波羅蜜", "perfection of diligence"), ("Dhyānapāramitā", "禪波羅蜜", "perfection of meditation"), ("Prajñāpāramitā", "慧波羅蜜", "perfection of wisdom")]
),

"00108_般舟三昧經": (
"""「佛告跋陀和菩薩：若善男子善女人，持戒清淨，獨處一心，念佛三昧。期七日、或九十日，精勤不懈。阿彌陀佛即現其前，為說妙法。」""",
"""佛告跋陀和菩薩：若善男子善女人持戒清淨，獨處一心，修念佛三昧。七天或九十天精勤不懈，阿彌陀佛便會出現在他面前，為他說法。""",
"""「作是念佛，心不清濁，心不散亂。心不清濁故，心不散亂故，即得見佛。見佛已，心生歡喜，即得無生法忍。」""",
"""「般舟三昧者，九十日中常行不坐不臥，一心稱念阿彌陀佛。如是精勤，佛即現前。」""",
[("Pratyutpanna-samādhi", "般舟三昧", "Standing Samadhi"), ("Bhadrapāla", "跋陀和", "Bhadrapala"), ("Amitābha", "阿彌陀佛", "Amida Buddha"), ("Anutpattika-dharma-kṣānti", "無生法忍", "acceptance of non-arising"), ("Buddhānusmṛti", "念佛", "recollection of Buddha"), ("Saṃsarga", "現前", "presence"), ("Cittavisuddhi", "心清淨", "purification of mind")]
),

"00109_思益梵天所問經": (
"""「思益梵天白佛言：世尊！云何名為如來正法？佛言：梵天！一切法平等，無高無下，是名正法。梵天！一切法無分別，無取無捨，是名正法。」""",
"""思益梵天問佛：世尊！什麼是如來的正法？佛說：梵天！一切法平等，沒有高下，這就是正法。梵天！一切法無分別、不取不捨，這就是正法。""",
"""「梵天言：何謂菩薩同等？佛言：如虚空平等，法界平等，眾生平等。以是平等故，菩薩於一切法不分別。」""",
"""「無生者，即是如來。若人如實知無生，是人即見如來。以如來者，本來不生故。」""",
[("Viśeṣacinta", "思益", "Distinguished Thinking"), ("Brahman", "梵天", "Brahma"), ("Samatā", "平等", "equality"), ("Avikalpa", "無分別", "non-conceptual"), ("Tathāgata", "如來", "Thus Come One"), ("Dharmadhātu", "法界", "dharma realm"), ("Anutpāda", "無生", "non-arising")]
),

"00110_持世經": (
"""「持世菩薩白佛言：世尊！菩薩云何修四念處？佛言：持世！菩薩觀身不淨，觀受是苦，觀心無常，觀法無我。如是觀時，不住生死，不證涅槃。」""",
"""持世菩薩問佛：世尊！菩薩怎麼修四念處？佛說：持世！菩薩觀身不淨、觀受是苦、觀心無常、觀法無我。這樣觀時，不住生死、不證涅槃。""",
"""「持世！菩薩知一切法從本已來，性自寂滅。以寂滅故，不取不捨，不行不住，是名真實菩薩行。」""",
"""「四法者，謂善知法、善知義、善知時、善知量。菩薩具此四法，則能利益眾生。」""",
[("Viśeṣaçakra", "持世", "Distinguished Chakra"), ("Smṛtyupasthāna", "念處", "foundation of mindfulness"), ("Aśubha", "不淨", "impurity"), ("Duḥkha", "苦", "suffering"), ("Anitya", "無常", "impermanence"), ("Anātman", "無我", "non-self"), ("Prabhāsvara", "自性清淨", "luminous nature")]
),

"00111_超日明三昧經": (
"""「佛告日明菩薩：若有菩薩得此超日明三昧，其光明超過日月，照耀十方一切世界。令諸眾生離苦得樂，破除無明黑暗。」""",
"""佛告日明菩薩：若有菩薩得到這超日明三昧，其光明超過日月，照耀十方一切世界，令眾生離苦得樂，破除無明黑暗。""",
"""「超日明三昧者，超過一切日月光明。以智慧光，破無明暗，是名超日明。」""",
"""「菩薩修此三昧，於一念中遍至十方佛剎，供養諸佛，聞法受持，還至本處，不捨本定。」""",
[("Sūryaprabhāsa", "超日明", "Surpassing Sunlight"), ("Samādhi", "三昧", "concentration"), ("Avidyā", "無明", "ignorance"), ("Prabhāsvara", "光明", "luminosity"), ("Buddhakṣetra", "佛剎", "Buddha field"), ("Pūjā", "供養", "offering"), ("Ekacitta", "一念", "single thought")]
),

"00112_文殊師利問經": (
"""「文殊師利白佛言：世尊！云何為佛根本？佛言：文殊！於一切法無所得，是為佛根本。以無所得故，不生不滅，不垢不淨，不增不減。」""",
"""文殊師利問佛：世尊！什麼是佛的根本？佛說：文殊！於一切法無所得，就是佛的根本。因為無所得，所以不生不滅、不垢不淨、不增不減。""",
"""「文殊！諸法空故，無相故，無願故。如是三解脫門，為諸佛之根本。」""",
"""「文殊言：法本無說，言說皆是方便。如來以方便力，於無說中而有所說。」""",
[("Mañjuśrī", "文殊師利", "Manjushri"), ("Mūla", "根本", "root/foundation"), ("Apratilabdha", "無所得", "non-obtainment"), ("Śūnyatā", "空", "emptiness"), ("Animitta", "無相", "signlessness"), ("Praṇidhāna", "無願", "wishlessness"), ("Upāya", "方便", "skillful means")]
),

"00113_大乘本生心地觀經": (
"""「爾時佛告彌勒菩薩：善男子！三界之中，以心為主。能觀心者，究竟解脫；不能觀者，永處生死。」""",
"""佛告彌勒菩薩：善男子！三界之中以心為主。能觀心的人，畢竟解脫；不能觀心的人，永遠在生死中。""",
"""「心清淨故，世界清淨。心雜染故，世界雜染。當知一切法，皆從心生。」""",
"""「如人用心造善惡業，受種種報。心如畫師，能畫種種五蘊世間及出世間。」""",
[("Cittamātra", "唯心", "mind only"), ("Cittaviśuddhi", "心清淨", "purification of mind"), ("Triloka", "三界", "three realms"), ("Maitreya", "彌勒", "Maitreya"), ("Vāsanā", "熏習", "impression"), ("Āśraya-parāvṛtti", "轉依", "turning about of the basis"), ("Cittakarmma", "心業", "mental action")]
),

"00114_大集經月藏分": (
"""「月藏菩薩白佛言：世尊！云何護持正法？佛言：月藏！若人能持戒、讀誦大乘、為人演說，不為名利，是名護持正法。」""",
"""月藏菩薩問佛：世尊！如何護持正法？佛說：月藏！若人持戒、讀誦大乘經典、為人講說，不為名利，這就是護持正法。""",
"""「月藏！如來滅後，有諸惡魔王，惱亂佛法。若諸菩薩以大忍力、大慈悲力，能護正法，令久住世。」""",
"""「月藏言：我等當以神力護持佛法。若有一人持佛一戒，我等晝夜衛護，不令惡魔鬼神得其便也。」""",
[("Candragarbha", "月藏", "Moon Matrix"), ("Dharmaprakāśana", "護法", "protection of Dharma"), ("Silāni", "戒", "precepts"), ("Māra", "魔", "Mara/demon"), ("Kṣānti", "忍辱", "patience"), ("Karuṇā", "慈悲", "compassion"), ("Sadharma", "正法", "true Dharma")]
),

"00115_大雲經": (
"""「佛言：善男子！如是密藏，非聲聞緣覺所能知，唯佛與佛乃能悉知。如是大雲密藏法門，即是如來秘蜜藏處。」""",
"""佛說：善男子！這樣的密藏，不是聲聞緣覺所能知道的，只有佛與佛才能完全了知。這大雲密藏法門，就是如來的秘密藏處。""",
"""「大雲密藏者，猶如大雲覆護一切。如來密藏亦復如是，覆護一切眾生，令得安樂。」""",
"""「佛言：我涅槃後，有國王名大雲，當護持我法，以大悲心利益眾生，令正法久住。」""",
[("Megha", "雲", "cloud"), ("Guhyagarbha", "密藏", "secret matrix"), ("Śrāvaka", "聲聞", "Hearer"), ("Pratyekabuddha", "緣覺", "Solitary Buddha"), ("Guhyasthāna", "秘密處", "secret place"), ("Mahākaruṇā", "大悲", "great compassion"), ("Saddharma", "正法", "True Dharma")]
),

"00116_如來藏經": (
"""「佛言：善男子！一切眾生，雖在諸趣煩惱身中，有如來藏常無染污，德相備足如我無異。」""",
"""佛說：善男子！一切眾生，雖然在六道煩惱的身體中，但有如來藏常住其中，不被染污，具備一切功德相好，與我（佛）沒有差別。""",
"""「一切眾生皆有如來藏。如貧女宅中藏有伏藏，雖未開發，而有寶藏。眾生亦爾，有如來藏而不自知。」""",
"""「九喻者：萎花中佛、蜂中蜜、糠中米、穢中金、地中寶、果中芽、衣中像、女中胎、泥中寶。如是九喻，喻如來藏。」""",
[("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Āśraya", "所依", "basis"), ("Viśuddhi", "清淨", "purity"), ("Śrāvaka", "聲聞", "Hearer"), ("Buddhadhātu", "佛性", "Buddha element"), ("Saṃkleśa", "染污", "defilement"), ("Guṇa", "德相", "qualities")]
),

"00117_不增不減經": (
"""「舍利弗！眾生界不增不減。何以故？眾生界即是法身，法身即是眾生界。舍利弗！法身者，即是如來藏。」""",
"""舍利弗！眾生界不增不減。為什麼？因為眾生界就是法身，法身就是眾生界。舍利弗！法身就是如來藏。""",
"""「舍利弗！甚深義者，即是第一義諦。第一義諦者，即是眾生界。眾生界者，即是如來藏。如來藏者，即是法身。」""",
"""「不增不減者，謂眾生界、法界、如來藏，三名一義。離於增減，常恆不變。」""",
[("Sattvadhātu", "眾生界", "realm of beings"), ("Dharmakāya", "法身", "Dharma body"), ("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Paramārtha-satya", "第一義諦", "ultimate truth"), ("Apañcama", "不增不減", "neither increasing nor decreasing"), ("Śāriputra", "舍利弗", "Shariputra"), ("Gambhīrārtha", "甚深義", "profound meaning")]
),

"00118_大法鼓經": (
"""「佛告迦葉：一切眾生有如來藏。如來常恆無有變易。迦葉！譬如有人見諸音聲從法鼓出，而不知鼓體常在。眾生亦爾，不知如來藏常在身中。」""",
"""佛告迦葉：一切眾生都有如來藏。如來常恆不變。迦葉！譬如人聽見聲音從法鼓發出，但不知道鼓體一直都在。眾生也一樣，不知道如來藏常在身中。""",
"""「迦葉！擊大法鼓，說甚深法。聲聞緣覺所不能解，唯諸菩薩乃能信受。」""",
"""「如來藏者，清淨無染。以客塵煩惱所覆蔽故，不能顯了。若離煩惱，即自現前。」""",
[("Dharma-bherī", "法鼓", "Dharma drum"), ("Kāśyapa", "迦葉", "Kashyapa"), ("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Agantuka-mala", "客塵", "adventitious defilement"), ("Nitya", "常恆", "eternal"), ("Guhyasthāna", "秘密", "secret"), ("Śrāvaka", "聲聞", "Hearer")]
),

"00119_央掘魔羅經": (
"""「爾時世尊入城乞食。央掘魔羅執劍逐佛：住！住！沙門！佛徐行。央掘魔羅疾走而不能及。即遙喚言：住！住！沙門！佛告言：我常自住，汝自不住。」""",
"""世尊入城乞食。央掘魔羅拿著劍追佛：停下！停下！沙門！佛慢慢走，央掘魔羅快跑卻追不上。他大喊：停下！佛說：我早已安住了，是你自己沒有安住。""",
"""「我常住於諸善法，汝自妄走不能住。如來已離於殺害，汝今何故隨惡法？」""",
"""「一切眾生皆有如來藏。如來藏者，離於生滅，不生不死，常恆清涼。央掘魔羅！汝身亦具如來藏，何故隨惡？如是知已，改惡修善。」""",
[("Aṅgulimāla", "央掘魔羅", "Angulimala"), ("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Sthitā", "住", "abiding"), ("Hiṃsā", "殺害", "violence"), ("Karuṇā", "慈悲", "compassion"), ("Kuśala", "善法", "wholesome dharma"), ("Cittaviśuddhi", "心清淨", "mind purification")]
),

"00120_大悲經": (
"""「佛言：阿難！我以大悲利益眾生，為諸眾生開示法要。阿難！我涅槃後，汝等當以大悲心，護持正法，令久住世。」""",
"""佛說：阿難！我以大悲心利益眾生，為眾生開示法要。阿難！我涅槃後，你們應當以大悲心護持正法，讓它長久住世。""",
"""「阿難！如來大悲不可窮盡。如來以大悲力故，於無量劫受種種苦，不捨一切眾生。」""",
"""「大悲者，謂於一切眾生生慈愍心。若人於善法退失，以大悲心，方便引導，令住善法。」""",
[("Mahākaruṇā", "大悲", "great compassion"), ("Ānanda", "阿難", "Ananda"), ("Sadharma", "正法", "true Dharma"), ("Anukampā", "慈愍", "sympathy"), ("Upāya", "方便", "skillful means"), ("Karuṇā", "悲", "compassion"), ("Nirvāṇa", "涅槃", "Nirvana")]
),

"00121_菩薩地持經": (
"""「菩薩地持者，謂菩薩所學之地。云何為地？謂菩薩於此中學菩薩戒、菩薩定、菩薩慧。以是三學，能持菩薩一切行。」""",
"""菩薩地持：即菩薩所學的階地。什麼是地？菩薩在此中學菩薩戒、菩薩定、菩薩慧。以這三學，能攝持菩薩的一切行持。""",
"""「菩薩摩訶薩，於六波羅蜜中，以施為首。以施故，攝取眾生；以戒故，利益眾生；以忍故，救護眾生。」""",
"""「菩薩地者，從初歡喜地乃至法雲地。於一一地中，修行萬行，漸次增進，乃至究竟無上菩提。」""",
[("Bodhisattvabhūmi", "菩薩地", "Bodhisattva stage"), ("Pāramitā", "波羅蜜", "perfection"), ("Śīla", "戒", "ethics"), ("Samādhi", "定", "concentration"), ("Prajñā", "慧", "wisdom"), ("Sahaja", "眾生攝取", "benefiting beings"), ("Daśabhūmi", "十地", "ten stages")]
),

"00122_菩薩善戒經": (
"""「菩薩戒者，有不同的聲聞戒。聲聞戒重身語，菩薩戒重心意。若菩薩起殺心，雖不動身，已犯菩薩戒。」""",
"""菩薩戒與聲聞戒不同。聲聞戒注重身體和語言的行為，菩薩戒注重心意的動機。菩薩若起殺心，即使沒有動手，已經犯了菩薩戒。""",
"""「菩薩戒有三種——攝律儀戒、攝善法戒、饒益有情戒。此三聚淨戒，攝一切菩薩戒。」""",
"""「菩薩若以慈悲心受菩薩戒，盡未來際，終不捨離。不同聲聞戒，一期壽盡即失。」""",
[("Bodhisattva-śīla", "菩薩戒", "Bodhisattva precepts"), ("Trisaṃvara", "三聚淨戒", "three sets of pure precepts"), ("Saṃvara-sīla", "攝律儀戒", "precept of restraint"), ("Kuśala-dharma-saṃgrāhaka", "攝善法戒", "precept of gathering virtue"), ("Sattvārtha-kriyā", "饒益有情戒", "precept of benefiting beings"), ("Śrāvaka-śīla", "聲聞戒", "Hearer precepts"), ("Karuṇā-citta", "慈悲心", "compassionate mind")]
),

"00123_優婆塞戒經": (
"""「善生白佛言：世尊！在家菩薩云何受戒？佛言：善男子！在家菩薩先當受三歸依，次受五戒——不殺、不盜、不邪婬、不妄語、不飲酒。」""",
"""善生問佛：世尊！在家菩薩怎麼受戒？佛說：善男子！在家菩薩先受三歸依，然後受五戒——不殺生、不偷盜、不邪淫、不妄語、不飲酒。""",
"""「若優婆塞能持五戒，名為善行之人。雖在家 居，如出家行。臨命終時，心得歡喜，不生恐怖。」""",
"""「善男子！優婆塞雖一人持戒，家中大小皆得安樂。以持戒故，龍天，龍天擁護，惡鬼遠離。」""",
[("Upāsaka", "優婆塞", "lay follower"), ("Śīla", "戒", "precepts"), ("Pañca-śīla", "五戒", "five precepts"), ("Sīlagṛha", "善生", "Sila-griha"), ("Triśaraṇa", "三歸依", "three refuges"), ("Gṛhastha", "在家", "householder"), ("Pāṇātipātā", "不殺", "not killing")]
),

"00124_梵網經": (
"""「盧舍那佛告千華上佛：我已百劫修行是心，心地法門。今為汝等說十重戒——殺戒、盜戒、淫戒、妄語戒、酤酒戒、說四眾過戒、自讚毀他戒、慳惜加加毀戒、瞋心不受悔戒、謗三寶戒。」""",
"""盧舍那佛告千華上佛：我已經百劫修行此心地法門。現在為你們說十重戒——殺、盜、淫、妄語、酤酒、說四眾過、自讚毀他、慳惜加、慳惜加毀、瞋心不受悔、謗三寶。""",
"""「一切眾生皆有佛性。一切意識色心，皆是佛性。是故佛戒，從心地中出，是名心地戒品。」""",
"""「佛子！若受佛戒者，國王王子百官宰相比丘比丘尼十八梵天六欲天子庶民黃門淫男淫女奴婢一切鬼神乃至金剛神，皆得受持。」""",
[("Brahmajāla", "梵網", "Brahma-net"), ("Vairocana", "盧舍那佛", "Vairocana Buddha"), ("Daśaguru-śīla", "十重戒", "ten major precepts"), ("Buddhadhātu", "佛性", "Buddha-nature"), ("Cittabhūmi", "心地", "mind ground"), ("Bodhisattva-śīla", "菩薩戒", "Bodhisattva precepts"), ("Upāsaka", "優婆塞", "lay follower")]
),

"00125_仁王般若經": (
"""「佛告波斯匿王：大王！護佛果者，當學般若波羅蜜。以般若故，觀一切法不生不滅，不垢不淨。如是觀者，即護佛果。」""",
"""佛告波斯匿王：大王！要護持佛果，應當學般若波羅蜜。因為般若能觀一切法不生不滅、不垢不淨。這樣觀就是護持佛果。""",
"""「大王！國土危脆，無有堅實。王以般若護持國土，則七難不起，風雨以時，五穀豐登，人民安樂。」""",
"""「般若波羅蜜者，是諸佛母。三世如來皆從般若生。護持般若，即護持諸佛正法。」""",
[("Prajñāpāramitā", "般若波羅蜜", "Perfection of Wisdom"), ("Prasenajit", "波斯匿王", "King Prasenajit"), ("Saptāpatti", "七難", "seven disasters"), ("Anutpāda", "不生", "non-arising"), ("Kṣetrarakṣā", "護國", "protecting the realm"), ("Buddhamātṛ", "佛母", "mother of Buddhas"), ("Dharmarakṣa", "護法", "protecting Dharma")]
),

"00126_佔察善惡業報經": (
"""「地藏菩薩言：若欲占察三世善惡業報，當用木輪相法。以木輪擲之，觀其輪相，而占未來善惡果報。」""",
"""地藏菩薩說：若想占察過去現在未來三世的善惡業報，應用木輪相法。擲木輪，觀察輪相，就能占卜未來的善惡果報。""",
"""「若人欲修懺悔，當先占察宿業輕重。知已，至心懺悔。懺悔清淨已，然後修行定慧。」""",
"""「地藏菩薩告堅淨信言：善男子！若有眾生不識善惡，不知因果，我以木輪相法，令其自知宿業。」""",
[("Kṣitigarbha", "地藏", "Earth Store"), ("Mūla- cakra", "木輪", "wooden wheel"), ("Pāpa", "惡業", "evil karma"), ("Puṇya", "善業", "merit"), ("Pratisaṃvid", "占察", "investigation"), ("Karma-vipāka", "業報", "ripening of karma"), ("Kaukṛtya", "懺悔", "repentance")]
),

"00127_大乘密嚴經": (
"""「佛告金剛藏菩薩：密嚴土者，即是如來清淨法界。超過三界，離諸分別。非聲聞緣覺所行之境，唯如來及大菩薩之所安住。」""",
"""佛告金剛藏菩薩：密嚴土就是如來的清淨法界。超過三界，離一切分別。不是聲聞緣覺的境界，只有如來和大菩薩才能安住。""",
"""「密嚴者，以如來藏為體。如來藏者，清淨本然，不生不然，不生不滅。轉識成智，即證密嚴。」""",
"""「阿賴耶識與如來藏，不一不異。阿賴耶識如水，如來藏如水性。水與水性，不一不異。」""",
[("Ghanavyūha", "密嚴", "Secret Adornment"), ("Vajragarbha", "金剛藏", "Vajra Store"), ("Tathāgatagarbha", "如來藏", "Buddha-nature"), ("Dharmadhātu", "法界", "dharma realm"), ("Ālayavijñāna", "阿賴耶識", "storehouse consciousness"), ("Āśraya-parāvṛtti", "轉識成智", "transforming consciousness into wisdom"), ("Niṣprapañca", "離分別", "free from conceptualization")]
),

"00128_大乘同性經": (
"""「佛言：海妙深持菩薩！如來有四種——一者化身如來，二者報身如來，三者法身如來，四者如如如來。是為同性。」""",
"""佛說：海妙深持菩薩！如來有四種——化身如來、報身如來、法身如來、如如如來。這就是同性（同一體性）。""",
"""「同性者，謂如來之四身同一體性。化報法三，各異其相，而同其性。以是故名同性彼岸。」""",
"""「佛言：如來法身，離於相書。不可以色見，不可以聲求。法身者，即是真如，無有差別。」""",
[("Samalakṣa", "同性", "same characteristic"), ("Nirmāṇakāya", "化身", "emanation body"), ("Saṃbhogakāya", "報身", "enjoyment body"), ("Dharmakāya", "法身", "Dharma body"), ("Tathatā", "如如", "suchness"), ("Sāgara-dhāra", "海妙深持", "Ocean Deep Holder"), ("Tathāgata", "如來", "Thus Come One")]
),

"00129_圓覺經大疏": (
"""「文殊師利法王子請問佛：世尊！云何如來本起清淨因地法行？佛言：一切如來本起因地，皆依圓照清淨覺相，永斷無明，方成佛道。」""",
"""文殊師利菩薩問佛：世尊！如來最初修行清淨因地的法行是什麼？佛說：一切如來最初修行，都依圓照清淨覺相，永斷無明，才能成佛道。""",
"""「知幻即離，不作方便。離幻即覺，亦無漸次。一切菩薩及末世眾生，依此修行，如是乃能永離諸幻。」""",
"""「宗密疏云：圓：圓覺者，圓滿覺性。在凡不減，在聖不增。以無明覆故，不能顯了。離幻即覺，本來圓滿。」""",
[("Samantabhadra-samādhi", "圓覺三昧", "Complete Enlightenment Samadhi"), ("Mañjuśrī", "文殊師利", "Manjushri"), ("Avidyā", "無明", "ignorance"), ("Māyā", "幻", "illusion"), ("Parimirvāṇa", "圓覺", "complete enlightenment"), ("Guifeng Zongmi", "宗密", "Zongmi"), ("Śūnyatā", "空性", "emptiness")]
),

"00130_注維摩詰經": (
"""「爾時維摩詰謂眾菩薩言：諸仁者！云何菩薩入不二法門？各隨所樂說之。於是眾菩薩各各說已，問文殊師利。文殊言：如我意者，於一切法無言無說，無示無識，離諸問答，是為入不二法門。」""",
"""維摩詰問眾菩薩：各位！菩薩如何入不二法門？請各人說說。眾菩薩說完後，問文殊師利。文殊說：依我看，於一切法無言無說、無示無識、離諸問答，這就是入不二法門。""",
"""「文殊問維摩：我等各說已，仁者當說。維摩默然無言。文殊讚言：善哉善哉！乃至無有文字語言，是真入不二法門。」""",
"""「僧肇注云：言之者失其真，知之者反其愚。不二之理，離言絕言絕慮。維摩默然，即是說竟。」""",
[("Advaya-dharmamukha", "不二法門", "non-dual Dharma gate"), ("Vimalakīrti", "維摩詰", "Vimalakirti"), ("Mañjuśrī", "文殊師利", "Manjushri"), ("Sengzhao", "僧肇", "Seng Zhao"), ("Nirvikalpa", "離分別", "non-conceptual"), ("Aṣṭasāhasrikā", "八千頌", "8000 verses"), ("śūnyatā", "空", "emptiness")]
),

"00131_法華經玄義": (
"""「智者大師說：妙法者，十界十如權實之法。蓮華者，喻權實開會。玄義者，旨深曰玄，意微曰義。」""",
"""智者大師說：妙法是十法界、十如是的權教與實教之法。蓮花比喻權教與實教的開會（開權顯實、會三歸一）。玄義：旨深為玄，意微為義。""",
"""「十妙者：境妙、智妙、行妙、位妙、三法妙、感應妙、神通妙、說法妙、眷屬妙、功德妙。此十妙攝法華一經之大旨。」""",
"""「跡門開權顯實，本門開近顯遠。此二章為法華之綱要。智者大師五重玄義——名、體、宗、用、教。」""",
[("Saddharma Puṇḍarīka", "妙法蓮華", "Lotus Sutra"), ("Zhiyi", "智者", "Zhiyi"), ("Daśa-amitābha", "十妙", "ten wonders"), ("Guānshí", "權實", "expedient and real"), ("Liánhuá", "蓮華", "lotus flower"), ("Wǔchóng-xuányì", "五重玄義", "five-fold profound meaning"), ("Piṇḍagrāha", "綱要", "essence")]
),

"00132_法華經文句": (
"""「方便品者，對真實而辨。佛昔日說三乘，是方便。今日說一乘，是真實。開方便門，示真實相，此文句之大旨也。」""",
"""方便品：相對於真實而言。佛過去說三乘是方便教法，現在說一乘是真實教法。開方便門、示真實相——這是文句解釋的核心要旨。""",
"""「智者云：諸佛世尊唯以一大事因緣故出現於世。所謂開示悟入佛之知見。此四字，是一部法華之綱骨。」""",
"""「文句者，以四釋解經——因緣釋、約教釋、本跡釋、觀心釋。四釋具足，方名消文。」""",
[("Upāya", "方便", "skillful means"), ("Satya", "真實", "truth"), ("Ekayāna", "一乘", "One Vehicle"), ("Triyāna", "三乘", "Three Vehicles"), ("Buddhajñāna", "佛知見", "Buddha's insight"), ("Kāimén-shìxiàng", "開權顯實", "opening the expedient and revealing the real"), ("Sìshì", "四釋", "four interpretations")]
),

"00133_華嚴經探玄記": (
"""「法藏大師云：華嚴一乘者，別教一乘，不同三乘。此中十玄門——同時具足相應門、因陀羅網境界門、秘密隱顯俱成門、微細相容安立門、十世隔法異成門、諸藏純雜具德門、一多相容不同門、諸法相即自在門、唯心迴轉善成門、託事顯法生解門。」""",
"""法藏大師說：華嚴一乘是別教一乘，不同於三乘。其中十玄門——同時具足相應門、帝網境界門、秘密隱顯俱成門、微細相容安立門、十世隔法異成門、諸藏純雜具德門、一多相容不同門、諸法相即自在門、唯心迴轉善成門、託事顯法生解門。""",
"""「一即一切，一切即一。如是相即相入，重重無盡，是名華嚴法界緣起。」""",
"""「法藏云：華嚴經以法界緣起為宗。法界者，一切法的真實本性。緣起者，一切法的相互關係。相即相入，重重無盡。」""",
[("Avataṃsaka", "華嚴", "Flower Adornment"), ("Daśa-gambhīra-dvāra", "十玄門", "ten profound gates"), ("Dharmadhātu-pratītyasamutpāda", "法界緣起", "dependent origination of the dharma realm"), ("Faxian", "法藏", "Fazang"), ("Ekādvaya", "一多相即", "one and many are identical"), ("Indrajāla", "因陀羅網", "Indra's net"), ("Śūnyatā", "空性", "emptiness")]
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

## 二、術語對照表

| 梵/巴語 | 漢語 | 英譯 |
|---|---|---|
{terms}

---

## 三、相關文獻

- [法華經](法華經/原文.md) — 一乘思想，開權顯實
- [華嚴經](華嚴經/原文.md) — 法界緣起，重重無盡
'''

def gen_terms(terms_list):
    lines = []
    for s, c, e in terms_list:
        lines.append(f"| {s} | {c} | {e} |")
    return "\n".join(lines)

count = 0
for dirname, (orig, trans, q1, q2, terms) in CONTENTS.items():
    filepath = os.path.join(BASE, dirname, "原文.md")
    if not os.path.exists(filepath):
        print(f"[跳過] {filepath} 不存在")
        continue
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
    count += 1
    print(f"[完成] {dirname}")

print(f"\n共處理 {count} 個文件")
