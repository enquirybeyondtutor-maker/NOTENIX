r"""Practice Test 3, Reading and Writing: Module 1 (mixed) and Module 2 easier. Original questions."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
WIC, TSP, CTC = "Words in Context", "Text Structure and Purpose", "Cross-Text Connections"
CID, COET, COEQ, INF = "Central Ideas and Details", "Command of Evidence: Textual", "Command of Evidence: Quantitative", "Inferences"
BND, FSS, TR, RS = "Boundaries", "Form, Structure, and Sense", "Transitions", "Rhetorical Synthesis"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"

RW1 = [
    rw(CS, WIC, 1, r"""After weeks of rehearsal, the choir's performance was ______: every singer came in on time, and the harmonies were perfectly balanced.""",
       Q_WIC, ["flawless", "hesitant", "disorganised", "brief"], "A",
       r"""Every singer on time and perfectly balanced harmonies describe a performance with no mistakes: "flawless"."""),
    rw(CS, WIC, 1, r"""The new park quickly became ______ with local families, who filled its playgrounds and picnic areas every weekend.""",
       Q_WIC, ["popular", "unknown", "unsafe", "expensive"], "A",
       r"""Families filling it every weekend shows it was well liked: "popular"."""),
    rw(CS, WIC, 2, r"""The author's prose is ______; she rarely uses a long word where a short one will do, and her sentences seldom run past a single line.""",
       Q_WIC, ["economical", "ornate", "obscure", "repetitive"], "A",
       r"""Short words and short sentences describe writing that uses no more than it needs: "economical". "Ornate" means highly decorated, the opposite."""),
    rw(CS, WIC, 3, r"""Although the two scientists disagreed sharply in public, their private letters reveal a surprisingly ______ relationship, full of shared jokes and requests for advice.""",
       Q_WIC, ["cordial", "hostile", "formal", "fleeting"], "A",
       r""""Although" contrasts their public disagreement with their private letters, which are full of jokes and requests for advice: a friendly, "cordial" relationship."""),
    rw(CS, TSP, 1, r"""Honeyguides are African birds that lead people to wild bees' nests. The birds call and flutter from tree to tree until the people find the nest and open it. The people take the honey, and the birds eat the leftover wax.""",
       "Which choice best states the main purpose of the text?",
       ["To describe a partnership between a bird and people", "To argue that bees should be protected",
        "To explain how bees build their nests", "To compare honeyguides with other African birds"], "A",
       r"""The text describes birds guiding people to nests, the people taking honey and the birds eating the wax: a partnership that benefits both."""),
    rw(CS, TSP, 2, r"""Early maps of the world often included imaginary islands. Some appeared because sailors mistook fog banks or icebergs for land; others were copied from older maps without being checked. A few such islands stayed on official charts into the twentieth century.""",
       "Which choice best describes the overall structure of the text?",
       ["It describes a feature of early maps, explains how it arose and notes how long it lasted.",
        "It argues that early mapmakers were careless and should not be trusted.",
        "It compares early maps with modern satellite images.",
        "It tells the story of a single explorer who discovered an island."], "A",
       r"""The text introduces imaginary islands, gives two reasons they appeared, and ends by noting some lasted into the twentieth century."""),
    rw(CS, TSP, 3, r"""The following text is adapted from a 1910 novel. Edith is waiting for a letter.

Every morning Edith met the postman at the gate, and every morning he shook his head before she could ask. By the second week she had stopped asking; she simply stood there until he passed, and then went back inside to sit by the window, where she could see the road.""",
       "Which choice best describes the function of the second sentence in the text as a whole?",
       ["It shows how Edith's hope continues even as she stops expecting an answer from the postman.",
        "It explains why the postman dislikes Edith.",
        "It reveals what the letter Edith is waiting for will say.",
        "It suggests that Edith has decided to leave home."], "A",
       r"""She stops asking yet still waits at the gate and watches the road, which shows her continued, quieter hope. Nothing reveals the letter's contents or any plan to leave."""),
    rw(CS, CTC, 2, r"""Text 1
Many people believe that multitasking, such as checking messages while studying, lets them get more done.

Text 2
In experiments, people who switched between tasks made more mistakes and took longer to finish than people who completed one task before starting another. Researchers say the brain loses time every time it switches focus.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the belief in Text 1?",
       ["By arguing that multitasking usually makes people slower and less accurate", "By agreeing that multitasking helps people finish more work",
        "By claiming that checking messages improves concentration", "By suggesting that the brain never switches focus"], "A",
       r"""Their experiments found switching between tasks caused more mistakes and slower finishing, which contradicts the belief."""),
    rw(II, CID, 1, r"""The Sahara has not always been a desert. Rock paintings found deep in it show giraffes, hippos and herds of cattle, and scientists have found the remains of ancient lakes. About 6,000 years ago, changes in Earth's orbit shifted rain patterns, and the region slowly dried out.""",
       "Which choice best states the main idea of the text?",
       ["Evidence shows the Sahara was once much wetter before it became a desert.", "Hippos still live in parts of the Sahara.",
        "Rock paintings are the oldest form of art.", "Earth's orbit has never changed."], "A",
       r"""The paintings of water-loving animals and ancient lakes show the Sahara was once wetter, and the text explains how it dried out."""),
    rw(II, CID, 2, r"""The following text is adapted from a 1904 short story.

Old Mr. Okafor was known in the village for two things: the tallest mango tree for miles around, and his refusal to sell a single mango. Every season he gave the fruit away, a basket to each house, and when people offered to pay he only laughed and asked them to bring the seeds back.""",
       "According to the text, what does Mr. Okafor do with his mangoes?",
       ["He gives them away to the people of the village.", "He sells them at the market.",
        "He keeps them for his own family.", "He trades them for seeds from other farmers."], "A",
       r"""He gives "a basket to each house" and laughs when people offer to pay. He only asks for the seeds back; he is not trading for other farmers' seeds."""),
    rw(II, COET, 2, r"""A researcher claims that working in a room with plants improves people's mood.""",
       "Which finding, if true, would most directly support the researcher's claim?",
       ["Office workers randomly assigned to rooms with plants reported better moods over a month than workers assigned to identical rooms without plants.",
        "Many offices now include plants in their design.", "Plants need regular watering to stay healthy.",
        "Some people are allergic to certain plants."], "A",
       r"""Random assignment to otherwise identical rooms, with better moods in the rooms with plants, directly supports the claim."""),
    rw(II, COET, 3, r"""Anthropologist Laila Haddad argues that an ancient settlement was abandoned gradually over several generations, rather than suddenly after a disaster.""",
       "Which finding, if true, would most directly support Haddad's argument?",
       ["Houses in the settlement were emptied of tools and pottery one by one over about eighty years, while the others stayed in use.",
        "The settlement was built near a river.", "Archaeologists found a layer of ash covering the whole settlement.",
        "Other settlements in the region were larger."], "A",
       r"""Houses being emptied one by one over eighty years shows a slow departure. A layer of ash over everything would instead suggest a sudden disaster."""),
    rw(II, COEQ, 1, r"""A town recorded the number of library books borrowed each month.

| Month | Books borrowed |
|---|---|
| January | 1,840 |
| February | 1,620 |
| March | 2,150 |
| April | 1,970 |

The month in which the most books were borrowed was ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["March.", "January.", "February.", "April."], "A", r"""March has the highest number in the table: 2,150."""),
    rw(II, COEQ, 3, r"""Researchers compared the average yearly cost of running two kinds of car.

| Cost | Petrol car | Electric car |
|---|---|---|
| Fuel or charging | $1,900 | $650 |
| Maintenance | $900 | $500 |
| Insurance | $1,100 | $1,300 |

The researchers conclude that although insurance costs more for the electric car, its total yearly running cost is still lower.""",
       "Which choice best describes data from the table that support the researchers' conclusion?",
       ["The electric car's total of $2,450 is lower than the petrol car's $3,900, despite its higher insurance.",
        "Insurance cost $1,300 for the electric car.", "Fuel was the largest cost for the petrol car.",
        "Maintenance cost less for the electric car than for the petrol car."], "A",
       r"""The conclusion compares totals: 650 + 500 + 1,300 = 2,450 for the electric car against 1,900 + 900 + 1,100 = 3,900 for the petrol car, even with higher insurance."""),
    rw(II, INF, 2, r"""In some deserts, beetles stand on sand dunes at dawn with their backs tilted into the wind. Fog drifting in from the sea condenses into droplets on their bumpy shells, and the droplets run down toward their mouths. This suggests that the beetles' behaviour helps them ______""",
       "Which choice most logically completes the text?",
       ["collect drinking water in a dry environment.", "stay cool during the hottest part of the day.",
        "hide from predators on the dunes.", "find food buried in the sand."], "A",
       r"""Fog condenses on their shells and runs to their mouths, so the behaviour lets them drink in the desert."""),
    rw(II, INF, 3, r"""A study compared two groups of patients recovering from the same operation. One group had a window view of trees; the other faced a brick wall. The tree-view group needed fewer painkillers and left hospital earlier on average. The patients were assigned to rooms based only on which beds were free. If the study's findings hold, hospitals designing new wards might ______""",
       "Which choice most logically completes the text?",
       ["consider giving patients views of nature to support recovery.", "replace painkillers with pictures of trees.",
        "build all new wards facing brick walls.", "conclude that room assignment affects which operation patients need."], "A",
       r"""Patients with a tree view recovered better, and rooms were assigned by chance, which strengthens the link. So the practical step is to give patients views of nature. Replacing painkillers goes far beyond the evidence."""),
    rw(SEC, BND, 1, r"""The volunteers planted two hundred ______ by the end of the day, the hillside was green again.""",
       Q_SEC, ["trees;", "trees,", "trees", "trees, and,"], "A",
       r"""Both parts are complete sentences, so a semicolon is needed between them."""),
    rw(SEC, BND, 2, r"""The guide pointed out three kinds of ______ oak, beech and hornbeam.""",
       Q_SEC, ["trees:", "trees;", "trees,", "trees"], "A",
       r"""A complete sentence introduces a list, so a colon fits."""),
    rw(SEC, BND, 2, r"""Ada Lovelace, often described as the first computer ______ wrote notes on a calculating machine that was never built in her lifetime.""",
       Q_SEC, ["programmer,", "programmer", "programmer;", "programmer:"], "A",
       r"""The phrase "often described as the first computer programmer" interrupts the sentence after a comma, so it closes with a comma before "wrote"."""),
    rw(SEC, BND, 3, r"""The experiment did not go as ______ the unexpected result led the team to a far more interesting discovery.""",
       Q_SEC, ["planned; still,", "planned, still,", "planned still", "planned; still"], "A",
       r""""Still" begins a new complete sentence, so a semicolon goes before it and a comma after it."""),
    rw(SEC, FSS, 1, r"""The flowers in the window box ______ in the morning sun.""",
       Q_SEC, ["open", "opens", "is opening", "has opened"], "A",
       r"""The subject is "flowers", which is plural, so the plural verb "open" is needed."""),
    rw(SEC, FSS, 2, r"""Last year, the museum ______ more visitors than in any year since it opened.""",
       Q_SEC, ["welcomed", "welcomes", "will welcome", "is welcoming"], "A",
       r""""Last year" is in the past, so the past tense "welcomed" is needed."""),
    rw(SEC, FSS, 3, r"""Each of the runners, along with their coaches, ______ given a map of the course before the race began.""",
       Q_SEC, ["was", "were", "are", "have been"], "A",
       r"""The subject is "Each", which is singular; "along with their coaches" does not change it. "Was" also matches the past "began"."""),
    rw(EI, TR, 1, r"""The café is small and has only six tables. ______, it is often full by noon.""",
       Q_TR, ["As a result", "However", "In contrast", "For instance"], "A",
       r"""Having few tables is the reason it fills up quickly, so a result transition fits."""),
    rw(EI, TR, 2, r"""Some scientists believe that dinosaurs were cold-blooded, like modern reptiles. ______, recent studies of bone growth suggest that many dinosaurs grew quickly, as warm-blooded animals do.""",
       Q_TR, ["However", "Therefore", "Similarly", "In other words"], "A",
       r"""Evidence of fast, warm-blooded-style growth contrasts with the cold-blooded view, so "However" fits."""),
    rw(EI, RS, 2, r"""While researching a topic, a student has taken the following notes:
• The Silk Road was a network of trade routes.
• It linked China with the Mediterranean.
• Merchants traded silk, spices and paper.
• Ideas and religions also spread along it.""",
       "The student wants to emphasise that the Silk Road spread more than goods. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Along with silk, spices and paper, ideas and religions also spread along the Silk Road.",
        "The Silk Road linked China with the Mediterranean.", "Merchants traded silk on the Silk Road.",
        "The Silk Road was a network of trade routes."], "A",
       r"""Only the sentence mentioning ideas and religions, beyond goods, meets the goal."""),
    rw(EI, RS, 3, r"""While researching a topic, a student has taken the following notes:
• Tardigrades are tiny animals about 0.5 mm long.
• They can survive being frozen, dried out and exposed to radiation.
• In 2007, tardigrades survived ten days in open space.
• They do this by entering a state where their metabolism almost stops.""",
       "The student wants to explain how tardigrades survive extreme conditions. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Tardigrades survive extreme conditions by entering a state in which their metabolism almost stops.",
        "In 2007, tardigrades survived ten days in open space.", "Tardigrades are tiny animals about 0.5 mm long.",
        "Tardigrades can survive being frozen and dried out."], "A",
       r"""The goal is how they survive; only the sentence describing the near-stopped metabolism explains the mechanism."""),
]

RW2E = [
    rw(CS, WIC, 1, r"""The puppy was so ______ that it fell asleep in the middle of its dinner.""",
       Q_WIC, ["tired", "hungry", "excited", "noisy"], "A", r"""Falling asleep mid-meal shows the puppy was very "tired"."""),
    rw(CS, WIC, 1, r"""The bridge is ______ enough for two lorries to pass each other easily.""",
       Q_WIC, ["wide", "narrow", "old", "short"], "A", r"""Two lorries passing easily needs a bridge that is "wide"."""),
    rw(CS, WIC, 2, r"""The team's victory was ______: no one had expected them to win a single match all season.""",
       Q_WIC, ["surprising", "predictable", "disappointing", "routine"], "A",
       r"""No one expected them to win, so the victory was "surprising"."""),
    rw(CS, WIC, 2, r"""The teacher asked students to ______ their essays, cutting each one down to a single page.""",
       Q_WIC, ["shorten", "lengthen", "translate", "decorate"], "A", r"""Cutting essays to one page means making them shorter: "shorten"."""),
    rw(CS, TSP, 1, r"""Kangaroos cannot walk backwards. Their large tail and powerful back legs push them forwards, which is why the kangaroo appears on Australia's coat of arms as a symbol of a country moving forwards.""",
       "Which choice best states the main purpose of the text?",
       ["To describe a fact about kangaroos and link it to a national symbol", "To argue that kangaroos should be protected",
        "To explain how kangaroos find food", "To compare kangaroos with other Australian animals"], "A",
       r"""The text explains that kangaroos only move forwards and links that to their place on the coat of arms."""),
    rw(CS, TSP, 2, r"""Most of the world's chocolate begins with cacao beans grown in West Africa. Farmers dry and ferment the beans, which are then shipped abroad. In factories, the beans are roasted, ground and mixed with sugar to make chocolate.""",
       "Which choice best describes the overall structure of the text?",
       ["It follows cacao beans through the steps that turn them into chocolate.", "It compares chocolate from different countries.",
        "It argues that farmers should be paid more for cacao.", "It explains why chocolate is unhealthy."], "A",
       r"""The text moves step by step from growing beans to drying, shipping, roasting and mixing: the process of making chocolate."""),
    rw(CS, TSP, 2, r"""Most snakes lay eggs. Some species, however, give birth to live young. These species often live in cold places, where eggs left on the ground might not stay warm enough to hatch.""",
       "Which choice best describes the function of the third sentence in the text as a whole?",
       ["It suggests a reason why some snakes give birth to live young.", "It describes how snake eggs hatch.",
        "It argues that cold places are dangerous for snakes.", "It gives a second example of egg-laying snakes."], "A",
       r"""After noting that some snakes give live birth, the third sentence explains why: eggs might not stay warm enough in cold places."""),
    rw(CS, CTC, 2, r"""Text 1
Some people think that eating carrots greatly improves eyesight.

Text 2
Carrots contain vitamin A, which the eyes need to work properly, so people who lack vitamin A can see better after eating them. But for people who already get enough vitamin A, eating more carrots does not make their eyesight sharper.""",
       "Based on the texts, how would the author of Text 2 most likely respond to the belief in Text 1?",
       ["By explaining that carrots help eyesight mainly for people lacking vitamin A", "By agreeing that carrots improve everyone's eyesight",
        "By claiming that carrots harm eyesight", "By arguing that vitamin A has nothing to do with eyes"], "A",
       r"""Text 2 says carrots help only people short of vitamin A, so it would limit the belief rather than accept or reject it entirely."""),
    rw(II, CID, 1, r"""Lightning is extremely hot. A single bolt can heat the air around it to about 30,000 degrees Celsius, roughly five times hotter than the surface of the Sun. This sudden heating makes the air expand so fast that it creates the boom we hear as thunder.""",
       "Which choice best states the main idea of the text?",
       ["Lightning heats the air so much that it causes thunder.", "The Sun is the hottest thing in the universe.",
        "Thunder can be heard from very far away.", "Lightning strikes the same place many times."], "A",
       r"""The text explains lightning's extreme heat and how the sudden heating creates thunder."""),
    rw(II, CID, 2, r"""Priya had always been afraid of deep water. That summer she joined a swimming class, practising a little more each week. By August she swam across the lake with her cousins, and she laughed the whole way.""",
       "According to the text, how did Priya's feelings about deep water change?",
       ["She went from fearing it to enjoying swimming in it.", "She became more afraid of it over the summer.",
        "She never learned to swim.", "She stopped visiting the lake."], "A",
       r"""She began afraid but by August swam across the lake laughing, so her fear turned to enjoyment."""),
    rw(II, COET, 1, r"""A student claims that the school's new reading corner has encouraged students to read more.""",
       "Which finding, if true, would most directly support the student's claim?",
       ["The number of books students borrowed doubled in the term after the reading corner opened.",
        "The reading corner has comfortable chairs.", "Some students prefer reading at home.", "The reading corner was built by parents."], "A",
       r"""More books borrowed after the corner opened directly supports the claim that students read more."""),
    rw(II, COET, 2, r"""A biologist claims that a type of seaweed grows faster in warmer water.""",
       "Which finding, if true, would most directly support the biologist's claim?",
       ["In tanks kept at different temperatures, the seaweed grew fastest in the warmest tank and slowest in the coolest.",
        "The seaweed is found along many coasts.", "Fish often hide among the seaweed.", "The seaweed is green."], "A",
       r"""Growth increasing with temperature across tanks directly supports the claim."""),
    rw(II, COEQ, 1, r"""A class recorded the weather for a month.

| Weather | Days |
|---|---|
| Sunny | 12 |
| Cloudy | 9 |
| Rainy | 7 |
| Snowy | 2 |

According to the table, the most common weather that month was ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["sunny.", "cloudy.", "rainy.", "snowy."], "A", r"""Sunny has the most days in the table: 12."""),
    rw(II, COEQ, 2, r"""A shop compared sales of two drinks over a hot week and a cold week.

| Week | Iced tea | Hot chocolate |
|---|---|---|
| Hot week | 340 | 60 |
| Cold week | 90 | 280 |

The owner says that customers choose drinks to suit the weather.""",
       "Which choice best describes data from the table that support the owner's statement?",
       ["Iced tea sold far more in the hot week, and hot chocolate sold far more in the cold week.",
        "The shop sold 340 iced teas in the hot week.", "Hot chocolate sold 60 cups in the hot week.", "The shop sold two kinds of drink."], "A",
       r"""Each drink sold best in the matching weather, which supports the statement."""),
    rw(II, INF, 1, r"""A plant on a windowsill bends towards the window. When the pot is turned around, within a few days the plant bends towards the window again. This suggests that the plant grows towards ______""",
       "Which choice most logically completes the text?",
       ["light.", "the wall.", "the floor.", "darkness."], "A",
       r"""Whichever way the pot faces, the plant turns to the window, where light comes in."""),
    rw(II, INF, 2, r"""A school started a breakfast club before lessons. Teachers noticed that students who came to the club were more alert in morning lessons. However, the students who came were also those whose parents dropped them off early. Therefore, it is possible that ______""",
       "Which choice most logically completes the text?",
       ["something other than breakfast, such as arriving early, helped the students be more alert.",
        "the breakfast club made students less alert.", "parents did not want their children to eat breakfast.",
        "all students came to the breakfast club."], "A",
       r"""The club students also arrived early, so arriving early, not just breakfast, could explain their alertness."""),
    rw(SEC, BND, 1, r"""My grandmother grows tomatoes in her ______ every summer she gives jars of sauce to the neighbours.""",
       Q_SEC, ["garden;", "garden,", "garden", "garden and,"], "A", r"""Two complete sentences need a semicolon between them."""),
    rw(SEC, BND, 1, r"""The bus was ______ so we decided to walk.""",
       Q_SEC, ["late,", "late", "late;", "late:"], "A", r"""Two complete clauses joined by "so" need a comma before "so"."""),
    rw(SEC, BND, 2, r"""Please bring the following ______ a pencil, a ruler and a calculator.""",
       Q_SEC, ["items:", "items;", "items", "items, and"], "A", r"""A complete sentence introduces a list, so a colon fits."""),
    rw(SEC, BND, 2, r"""The castle, built in the twelfth ______ still has its original walls.""",
       Q_SEC, ["century,", "century", "century;", "century:"], "A",
       r""""Built in the twelfth century" is set off by commas; it opens with a comma after "castle" and must close with one."""),
    rw(SEC, FSS, 1, r"""My brother and I ______ to the cinema every Friday.""",
       Q_SEC, ["go", "goes", "is going", "has gone"], "A", r"""The compound subject "My brother and I" is plural, so "go" is needed."""),
    rw(SEC, FSS, 1, r"""Next week, the class ______ a trip to the zoo.""",
       Q_SEC, ["will take", "took", "has taken", "was taking"], "A", r""""Next week" is in the future, so "will take" is needed."""),
    rw(SEC, FSS, 2, r"""The cat licked ______ paws after eating.""",
       Q_SEC, ["its", "it's", "its'", "their's"], "A", r"""The paws belong to the cat, so the possessive "its" is used. "It's" means "it is"."""),
    rw(EI, TR, 1, r"""The library is closed today. ______, the reading room will open tomorrow at nine.""",
       Q_TR, ["However", "For example", "Similarly", "As a result"], "A", r"""Opening tomorrow contrasts with being closed today, so "However" fits."""),
    rw(EI, TR, 2, r"""Bees collect nectar from flowers. ______, they carry pollen from plant to plant, which helps plants make seeds.""",
       Q_TR, ["At the same time", "In contrast", "Instead", "Nevertheless"], "A",
       r"""Carrying pollen happens while bees collect nectar, so "At the same time" fits."""),
    rw(EI, RS, 1, r"""While researching a topic, a student has taken the following notes:
• The Nile is a river in Africa.
• It flows north into the Mediterranean Sea.
• It is about 6,650 km long.""",
       "The student wants to state where the Nile ends. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["The Nile flows north into the Mediterranean Sea.", "The Nile is a river in Africa.",
        "The Nile is about 6,650 km long.", "The Nile is one of the world's rivers."], "A",
       r"""Only the sentence naming the Mediterranean Sea states where the river ends."""),
    rw(EI, RS, 2, r"""While researching a topic, a student has taken the following notes:
• Polar bears have black skin under their fur.
• Their fur is not actually white; each hair is clear and hollow.
• The hairs scatter light, so the fur looks white.""",
       "The student wants to explain why polar bears look white. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Polar bears look white because their clear, hollow hairs scatter light.", "Polar bears have black skin under their fur.",
        "Polar bear fur is not actually white.", "Polar bears live in the Arctic."], "A",
       r"""Only the sentence linking the clear, hollow hairs scattering light to the white look explains it."""),
]
