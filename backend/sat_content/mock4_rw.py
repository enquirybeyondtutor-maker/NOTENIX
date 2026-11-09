r"""Practice Test 4, Reading and Writing: Module 1 (mixed) and Module 2 easier. Original questions."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
WIC, TSP, CTC = "Words in Context", "Text Structure and Purpose", "Cross-Text Connections"
CID, COET, COEQ, INF = "Central Ideas and Details", "Command of Evidence: Textual", "Command of Evidence: Quantitative", "Inferences"
BND, FSS, TR, RS = "Boundaries", "Form, Structure, and Sense", "Transitions", "Rhetorical Synthesis"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"
NOTES = "While researching a topic, a student has taken the following notes:"

RW1 = [
    rw(CS, WIC, 1, r"""The bakery's sourdough is famously ______: loaves bought on a Monday are often still soft on Friday.""",
       Q_WIC, ["long-lasting", "fragile", "expensive", "rare"], "A",
       r"""Bread that stays soft from Monday to Friday keeps well for a long time, so "long-lasting" fits."""),
    rw(CS, WIC, 1, r"""Although the volcano had been ______ for centuries, scientists continued to monitor it, knowing that it could erupt again.""",
       Q_WIC, ["dormant", "active", "famous", "visible"], "A",
       r""""Although" and "could erupt again" show that the volcano had been quiet but not finished: "dormant". An "active" volcano would obviously need watching."""),
    rw(CS, WIC, 2, r"""The mayor's plan was ______ by the council, which voted unanimously to adopt it without changes.""",
       Q_WIC, ["endorsed", "rejected", "postponed", "amended"], "A",
       r"""A unanimous vote to adopt the plan without changes means the council approved it: "endorsed". "Amended" contradicts "without changes"."""),
    rw(CS, WIC, 3, r"""Historian Li Wei argues that the treaty's importance has been ______: although textbooks present it as a turning point, it changed little about how the two countries actually traded.""",
       Q_WIC, ["overstated", "underestimated", "ignored", "disputed"], "A",
       r"""Textbooks call it a turning point, but Li says it changed little, so its importance has been exaggerated: "overstated"."""),
    rw(CS, TSP, 1, r"""Octopuses can change the colour of their skin in less than a second. They do this using thousands of cells called chromatophores, each filled with pigment. Muscles around each cell stretch it open to show the colour or squeeze it shut to hide it.""",
       "Which choice best states the main purpose of the text?",
       ["To explain how octopuses are able to change colour so quickly", "To argue that octopuses are the most intelligent sea animals",
        "To compare octopuses with other animals that change colour", "To describe where octopuses live"], "A",
       r"""The text names the ability and then explains the cells and muscles that make it possible. It makes no comparison or argument about intelligence."""),
    rw(CS, TSP, 2, r"""The following text is from a short story.

The house had stood empty for years. Its windows were grey with dust, and nettles had swallowed the garden path. Yet when Clara pushed open the gate, she noticed a single rose blooming beside the door, as bright as if someone had tended it that morning.""",
       "Which choice best describes the function of the final sentence in the text as a whole?",
       ["It introduces a detail that contrasts with the neglect described earlier.", "It explains why the house had been left empty.",
        "It describes Clara's memories of living in the house.", "It suggests that Clara plans to repair the garden."], "A",
       r"""The first sentences describe dust and nettles; "Yet" introduces a fresh, carefully kept rose, which contrasts with that neglect."""),
    rw(CS, TSP, 3, r"""Some economists claim that working from home reduces productivity. A 2023 study of a travel company, however, found that employees allowed to work from home two days a week were just as productive as those in the office and were less likely to leave the company. The study's authors caution that the results may differ in jobs that require close teamwork.""",
       "Which choice best describes the overall structure of the text?",
       ["It presents a claim, describes a study that challenges it, and then notes a limitation of the study.",
        "It describes a study and then explains why its results are wrong.",
        "It compares two companies' policies on working from home.",
        "It presents a claim and then gives several examples that support it."], "A",
       r"""The text moves from the economists' claim, to the study that contradicts it ("however"), to the authors' warning about where the result may not apply."""),
    rw(CS, CTC, 3, r"""Text 1
Many people assume that young children learn to speak mainly by imitating the adults around them. On this view, a child's grammar is simply a copy of the grammar the child hears.

Text 2
Linguist Ana Duarte points out that young English speakers often say forms such as "goed" and "mouses", which adults almost never say. Such errors, she argues, show that children work out general rules, like adding "-ed" for the past, and then apply them too widely.""",
       "Based on the texts, how would Duarte (Text 2) most likely respond to the view described in Text 1?",
       ["By arguing that imitation cannot explain errors showing that children apply grammatical rules of their own",
        "By agreeing that children copy exactly what adults say",
        "By claiming that children learn to speak only from books",
        "By suggesting that adults should correct children's errors more often"], "A",
       r"""Children produce forms they never hear, such as "goed", so imitation alone cannot explain them; Duarte says children build and overapply rules."""),
    rw(II, CID, 1, r"""Monarch butterflies travel up to 4,000 kilometres each autumn, from Canada and the northern United States to forests in central Mexico. No single butterfly makes the round trip, however. The journey north in spring is completed by several generations, each of which lives only a few weeks.""",
       "Which choice best states the main idea of the text?",
       ["The monarch migration is so long that the return journey takes several generations to complete.",
        "Monarch butterflies live longer than most other insects.", "Monarch butterflies spend the whole year in Mexico.",
        "Monarch butterflies travel only short distances."], "A",
       r"""The text gives the long autumn journey and explains that the return trip north is finished by several short-lived generations."""),
    rw(II, CID, 2, r"""The following text is from a short story.

Grandfather kept every letter he had ever received in a tin box beneath his bed. As far as anyone knew, he never reread them. But when the river flooded the house, it was the tin box he carried upstairs first, before his coat or his shoes.""",
       "Based on the text, what is most strongly suggested about Grandfather?",
       ["He valued the letters deeply, even though he did not reread them.", "He had forgotten that the letters were under his bed.",
        "He was more worried about his coat than about the letters.", "He planned to throw the letters away after the flood."], "A",
       r"""Saving the box before his coat or shoes shows how much the letters mattered to him, whatever his reading habits."""),
    rw(II, COET, 3, r"""Ecologist Marta Ruiz claims that planting community gardens increases the number of bee species found in a city neighbourhood.""",
       "Which finding, if true, would most directly support Ruiz's claim?",
       ["Neighbourhoods had more bee species after gardens were planted than before, while similar neighbourhoods without new gardens showed no change.",
        "Bees visit many kinds of flowers during a single day.",
        "Some city residents are afraid of being stung by bees.",
        "Community gardens often grow vegetables as well as flowers."], "A",
       r"""The claim is that gardens increase bee species. A rise after planting, with no change in comparable areas without gardens, links the increase to the gardens."""),
    rw(II, COET, 2, r"""In the poem "The Lighthouse Keeper", the speaker conveys the keeper's loneliness.""",
       "Which quotation from the poem most effectively illustrates this claim?",
       ["\"No voice but the gulls' has spoken to me in a year\"", "\"The lamp turns, bright and steady, through the night\"",
        "\"The sea is calm and silver in the evening\"", "\"The ships pass safely by the rocks below\""], "A",
       r"""Hearing no voice but the gulls' for a year shows isolation. The other lines describe the lamp, the sea and the ships, not the keeper's feelings."""),
    rw(II, COEQ, 1, r"""Researchers measured the reaction times of students who had slept for different lengths of time the night before.

| Hours of sleep | Average reaction time (milliseconds) |
|---|---|
| 5 | 320 |
| 6 | 295 |
| 7 | 270 |
| 8 | 255 |
| 9 | 250 |

The researchers found that more sleep was associated with faster reactions: ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["students who slept 9 hours reacted in 250 milliseconds on average, compared with 320 milliseconds for those who slept 5 hours.",
        "students who slept 7 hours reacted in 270 milliseconds on average.",
        "the slowest average reaction time was 320 milliseconds.",
        "some students slept for 8 hours."], "A",
       r"""A shorter reaction time is faster. Comparing the most and least sleep shows more sleep going with a faster average reaction; the other choices give single values."""),
    rw(II, COEQ, 3, r"""A publisher recorded its book sales, in thousands of copies, by format.

| Format | 2019 | 2023 |
|---|---|---|
| Print | 640 | 600 |
| E-book | 180 | 150 |
| Audiobook | 60 | 150 |

A manager claims that audiobooks were the only format whose sales grew between 2019 and 2023.""",
       "Which choice best describes data from the table that support the manager's claim?",
       ["Audiobook sales rose from 60,000 to 150,000 copies, while print and e-book sales both fell.",
        "Print sold the most copies in both years.", "E-book and audiobook sales were equal in 2023.",
        "Print sales fell by 40,000 copies."], "A",
       r"""To support "the only format that grew", the data must show audiobooks rising and the other formats not rising. Only one choice shows both."""),
    rw(II, INF, 2, r"""In a study, plants grown with recordings of birdsong grew no differently from plants grown in silence. Plants placed near a fan that gently shook their stems, however, grew shorter but sturdier stems. The researchers concluded that the plants were responding to ______""",
       "Which choice most logically completes the text?",
       ["physical movement rather than to sound.", "the songs of particular birds.",
        "the noise made by the fan.", "how much water they received."], "A",
       r"""Sound alone (birdsong) made no difference, but shaking did, so the plants responded to movement. The fan's noise is ruled out because sound had no effect."""),
    rw(II, INF, 3, r"""Archaeologists studying a village from about 800 BCE found that some of its pottery was made from clay dug from a riverbank 200 kilometres away, even though good clay was available nearby. Pots made with the distant clay were more elaborately decorated and were found mainly in burials, not in homes. This suggests that the distant clay ______""",
       "Which choice most logically completes the text?",
       ["was reserved for objects with special, possibly ceremonial, importance.", "was cheaper than the clay found near the village.",
        "was used for most of the pots found in homes.", "made pots that were stronger for everyday cooking."], "A",
       r"""The distant clay was used despite nearby clay, for finely decorated pots found mainly in burials. That points to special or ceremonial use, not everyday or cheaper use."""),
    rw(SEC, BND, 1, r"""The museum first opened in ______ since then, it has welcomed more than a million visitors.""",
       Q_SEC, ["1998;", "1998,", "1998", "1998 and,"], "A",
       r"""Both parts are complete sentences, so they need a semicolon. A comma alone, or nothing, would join them incorrectly."""),
    rw(SEC, BND, 2, r"""Marine biologist Sylvia ______ known for her deep-sea explorations, has spent more than 7,000 hours underwater.""",
       Q_SEC, ["Earle,", "Earle", "Earle;", "Earle:"], "A",
       r""""Known for her deep-sea explorations" is extra information set off by commas; the closing comma after "explorations" needs an opening comma after "Earle"."""),
    rw(SEC, BND, 2, r"""Researchers compared two groups of ______ those living in cities and those living in forests.""",
       Q_SEC, ["blackbirds:", "blackbirds", "blackbirds;", "blackbirds."], "A",
       r"""A complete sentence introduces an explanation of the two groups, so a colon is correct. A semicolon or full stop would leave a fragment."""),
    rw(SEC, BND, 3, r"""The bridge, which took six years to ______ finally opened to traffic in 1937.""",
       Q_SEC, ["build,", "build", "build;", "build—"], "A",
       r"""The "which" clause opens with a comma after "bridge", so it must close with a comma before the main verb "opened". A dash would not match the opening comma."""),
    rw(SEC, FSS, 1, r"""Every morning, the twins ______ their dog along the beach.""",
       Q_SEC, ["walk", "walks", "has walked", "is walking"], "A",
       r"""The subject "twins" is plural and the action is a daily habit, so the plural present tense "walk" is needed."""),
    rw(SEC, FSS, 2, r"""The results of the experiment, published last month in a leading journal, ______ surprised many scientists.""",
       Q_SEC, ["have", "has", "was", "is"], "A",
       r"""The subject is "results", which is plural; "of the experiment" and the description between the commas do not change it. So "have" is needed."""),
    rw(SEC, FSS, 3, r"""By the time the rescue boat arrived, the stranded sailors ______ on the island for three days.""",
       Q_SEC, ["had been", "have been", "are", "will be"], "A",
       r"""The waiting happened before a past event (the boat arrived), so the past perfect "had been" is needed."""),
    rw(EI, TR, 1, r"""Penguins are birds. ______, they cannot fly; instead, they use their wings to swim.""",
       Q_TR, ["However", "Therefore", "For example", "Similarly"], "A",
       r"""Most birds fly, so a bird that cannot fly is a contrast with what is expected: "However"."""),
    rw(EI, TR, 2, r"""The city's first underground railway line opened in 1904 with 28 stations. ______, the network had grown to more than 400 stations by the 1940s.""",
       Q_TR, ["Over the following decades", "In contrast", "For instance", "Even so"], "A",
       r"""The second sentence describes growth over the years after 1904, so a time transition, "Over the following decades", fits."""),
    rw(EI, RS, 2, NOTES + r"""
• The Atacama Desert in Chile is one of the driest places on Earth.
• Some weather stations there have never recorded rain.
• Its skies are unusually clear and dark.
• Several major observatories have been built there.""",
       "The student wants to explain why astronomers build observatories in the Atacama Desert. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Because its skies are unusually clear and dark, the Atacama Desert has become home to several major observatories.",
        "The Atacama Desert in Chile is one of the driest places on Earth.",
        "Some weather stations in the Atacama Desert have never recorded rain.",
        "Several major observatories have been built in Chile."], "A",
       r"""Only one choice gives a reason (clear, dark skies) and connects it to the observatories."""),
    rw(EI, RS, 2, NOTES + r"""
• Maria Tallchief (1925–2013) was a member of the Osage Nation.
• She was America's first major prima ballerina.
• She danced with the New York City Ballet.
• Choreographer George Balanchine created roles for her, including in The Firebird (1949).""",
       "The student wants to introduce Maria Tallchief to an audience unfamiliar with her. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Maria Tallchief, a member of the Osage Nation, was America's first major prima ballerina.",
        "George Balanchine created roles for Tallchief.", "The Firebird was performed in 1949.",
        "Tallchief danced with the New York City Ballet."], "A",
       r"""An audience new to Tallchief needs to know who she was. Only one choice says who she was and why she is notable."""),
]

RW2E = [
    rw(CS, WIC, 1, r"""The hikers were ______ after walking twenty miles, so they fell asleep as soon as they reached the cabin.""",
       Q_WIC, ["exhausted", "energetic", "curious", "lost"], "A",
       r"""Falling asleep at once after a twenty-mile walk shows they were very tired: "exhausted"."""),
    rw(CS, WIC, 1, r"""The new library is far more ______ than the old one: it has ramps, wide doors and lifts to every floor.""",
       Q_WIC, ["accessible", "crowded", "ancient", "distant"], "A",
       r"""Ramps, wide doors and lifts make a building easy for everyone to enter and use: "accessible"."""),
    rw(CS, WIC, 2, r"""The scientist was ______ about the early results, warning reporters that a larger study was needed before anyone could draw conclusions.""",
       Q_WIC, ["cautious", "thrilled", "dismissive", "certain"], "A",
       r"""Warning that more study is needed before drawing conclusions shows care, not certainty: "cautious"."""),
    rw(CS, WIC, 2, r"""Rather than ______ the old factory, the town converted it into flats and artists' studios.""",
       Q_WIC, ["demolishing", "admiring", "visiting", "designing"], "A",
       r""""Rather than" sets up an alternative to converting the building. The natural alternative is knocking it down: "demolishing"."""),
    rw(CS, TSP, 1, r"""Honeybees share the location of food through a "waggle dance". The angle of the dance shows the direction of the food relative to the sun, and the length of each waggle shows how far away it is.""",
       "Which choice best states the main purpose of the text?",
       ["To describe how honeybees use a dance to show other bees where food is", "To argue that honeybees are endangered",
        "To explain how honeybees make honey", "To compare honeybees with other insects"], "A",
       r"""Both sentences explain what the waggle dance shows: the food's direction and distance."""),
    rw(CS, TSP, 2, r"""Many people assume that deserts are always hot. Yet the largest desert on Earth is Antarctica: it receives very little precipitation, which is what defines a desert, even though it is extremely cold.""",
       "Which choice best describes the function of the second sentence in the text as a whole?",
       ["It gives an example that challenges a common assumption.", "It explains why deserts are hot.",
        "It describes the animals that live in Antarctica.", "It supports the assumption stated in the first sentence."], "A",
       r"""The first sentence states the assumption that deserts are hot; the second gives a cold desert, Antarctica, that contradicts it."""),
    rw(CS, TSP, 2, r"""The following text is from a short story.

The train pulled away, and Amir watched the platform slide past. His mother's waving figure grew smaller and smaller until it was only a speck, and then nothing at all. He kept looking long after there was nothing left to see.""",
       "Which choice best states the main purpose of the text?",
       ["To show a character's reluctance to let go of a farewell", "To describe the route the train will take",
        "To explain why Amir is leaving home", "To introduce Amir's mother as the main character"], "A",
       r"""Amir keeps watching "long after there was nothing left to see", which shows he does not want the goodbye to end. The route and his reasons are not given."""),
    rw(CS, CTC, 2, r"""Text 1
Some nutritionists recommend eating breakfast every day, arguing that it helps people control their weight.

Text 2
A review of randomised trials found that adults who were asked to eat breakfast did not lose more weight than those asked to skip it. In fact, the breakfast eaters consumed slightly more calories in total each day.""",
       "Based on the texts, how would the authors of the review in Text 2 most likely respond to the nutritionists in Text 1?",
       ["By pointing out that the evidence does not show breakfast helping people control their weight",
        "By agreeing that everyone should eat breakfast", "By arguing that breakfast should be the largest meal of the day",
        "By claiming that skipping breakfast causes weight gain"], "A",
       r"""The trials found no extra weight loss from eating breakfast, which contradicts the nutritionists' reason for recommending it."""),
    rw(II, CID, 1, r"""The Great Barrier Reef, off the coast of Australia, is the largest coral reef system in the world. It stretches for about 2,300 kilometres and can be seen from space. It is home to thousands of species of fish, molluscs and corals.""",
       "Which choice best states the main idea of the text?",
       ["The Great Barrier Reef is an enormous reef system that supports many species.", "The Great Barrier Reef is shrinking quickly.",
        "Coral reefs are found only in Australia.", "Fish are the most common animals on coral reefs."], "A",
       r"""The text describes the reef's size and the many species living there. It says nothing about shrinking or about which animals are most common."""),
    rw(II, CID, 1, r"""The following text is from a short story.

Sofia had practised the piece every evening for a month. When she finally played it at the concert, her hands, which had trembled backstage, moved steadily across the keys, and she smiled as the last note faded.""",
       "Which choice best describes what happens in the text?",
       ["Sofia overcomes her nerves and plays well at a concert.", "Sofia decides to stop playing the piano.",
        "Sofia forgets the piece in the middle of the concert.", "Sofia watches another pianist perform."], "A",
       r"""Her hands trembled backstage but moved steadily on stage, and she smiled at the end: she overcame her nerves."""),
    rw(II, COET, 1, r"""A student claims that the city's new bike lanes have made cycling more popular.""",
       "Which finding, if true, would most directly support the student's claim?",
       ["The number of cyclists counted on main roads doubled in the year after the lanes opened.",
        "The bike lanes are painted green.", "Some drivers complained about the new lanes.",
        "Bicycles were invented in the 1800s."], "A",
       r"""More cyclists after the lanes opened directly shows cycling becoming more popular. The other findings do not measure how many people cycle."""),
    rw(II, COET, 2, r"""In a novel, the narrator describes her aunt as extremely generous.""",
       "Which quotation from the novel most effectively illustrates this description?",
       ["\"She gave her winter coat to a stranger at the bus stop and walked home through the snow, laughing.\"",
        "\"She lived in a narrow house at the end of Mill Street.\"", "\"She liked to read in the evenings.\"",
        "\"She had worked as a teacher for thirty years.\""], "A",
       r"""Giving away her own coat in the snow is a clear act of generosity. The other quotations describe where she lived, her hobby and her job."""),
    rw(II, COEQ, 1, r"""A school asked 200 students to name their favourite season.

| Season | Number of students |
|---|---|
| Spring | 38 |
| Summer | 92 |
| Autumn | 44 |
| Winter | 26 |

A student claims that summer was the most popular season.""",
       "Which choice best describes data from the table that support the student's claim?",
       ["92 students chose summer, more than chose any other season.", "26 students chose winter.",
        "Autumn was chosen by 44 students.", "Spring and autumn together were chosen by 82 students."], "A",
       r"""To show summer was most popular, its count must be compared with the others. Only one choice does that."""),
    rw(II, COEQ, 2, r"""The table shows the average rainfall in a city in four months.

| Month | Average rainfall (mm) |
|---|---|
| January | 80 |
| April | 50 |
| July | 20 |
| October | 90 |

Of the months shown, the city is driest in ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["July, which has an average of 20 mm of rain.", "October, which has an average of 90 mm of rain.",
        "January, which has an average of 80 mm of rain.", "April, which has an average of 50 mm of rain."], "A",
       r"""The driest month has the least rain. July's 20 mm is the lowest value in the table."""),
    rw(II, INF, 1, r"""Foxes living in cities have often been seen eating food left in parks and taken from bins. Foxes in the nearby countryside mostly eat small animals and berries. This suggests that city foxes ______""",
       "Which choice most logically completes the text?",
       ["have adapted their diet to the food available in cities.", "no longer hunt at night.",
        "are larger than countryside foxes.", "will soon move back to the countryside."], "A",
       r"""The two groups eat different foods matching what is around them, so city foxes have adjusted their diet to city food."""),
    rw(II, INF, 2, r"""A school found that students who walked or cycled to school arrived on time more often than students who were driven. On rainy days, when many more students were driven, late arrivals rose sharply. One likely explanation is that ______""",
       "Which choice most logically completes the text?",
       ["traffic near the school was heavier when more families drove.", "students who walk never arrive late.",
        "rain makes students less interested in school.", "the school day started later on rainy days."], "A",
       r"""Lateness rose when more students were driven, which points to more cars and so heavier traffic."""),
    rw(SEC, BND, 1, r"""The concert was ______ the band played for more than three hours.""",
       Q_SEC, ["incredible;", "incredible,", "incredible", "incredible, and,"], "A",
       r"""Both parts are complete sentences, so a semicolon joins them. A comma alone, or no punctuation, is incorrect."""),
    rw(SEC, BND, 1, r"""The lighthouse, built in ______ still guides ships along the rocky coast.""",
       Q_SEC, ["1870,", "1870", "1870;", "1870:"], "A",
       r""""Built in 1870" is extra information that opens with a comma after "lighthouse", so it must close with a comma too."""),
    rw(SEC, BND, 2, r"""Hurricanes form over warm ocean ______ they weaken quickly once they move over land.""",
       Q_SEC, ["water, but", "water but,", "water, but,", "water but"], "A",
       r"""Two complete sentences joined by "but" need a comma before "but" and none after it."""),
    rw(SEC, BND, 2, r"""The guide pointed out the castle's oldest ______ a tower built in the twelfth century.""",
       Q_SEC, ["feature:", "feature;", "feature.", "feature, it is"], "A",
       r"""A complete sentence is followed by a phrase naming the feature, so a colon fits. A semicolon or full stop would leave the phrase as a fragment."""),
    rw(SEC, FSS, 1, r"""Yesterday, the students ______ a trip to the science museum.""",
       Q_SEC, ["took", "take", "will take", "are taking"], "A",
       r""""Yesterday" places the action in the past, so the past tense "took" is needed."""),
    rw(SEC, FSS, 2, r"""Each of the paintings in the gallery ______ a small label giving the artist's name.""",
       Q_SEC, ["has", "have", "are having", "were having"], "A",
       r"""The subject is "Each", which is singular; "of the paintings" does not change it. So the singular "has" is needed."""),
    rw(SEC, FSS, 2, r"""The museum reopened after a year of repairs, and visitors praised ______ new lighting.""",
       Q_SEC, ["its", "it's", "its'", "they're"], "A",
       r"""The lighting belongs to the museum, so the possessive "its" is needed. "It's" means "it is", and "its'" is not a word."""),
    rw(EI, TR, 1, r"""Tomatoes need plenty of sunlight. ______, gardeners usually plant them in the brightest part of the garden.""",
       Q_TR, ["For this reason", "However", "In contrast", "Meanwhile"], "A",
       r"""Planting in the brightest spot is a result of the plants' need for sunlight, so a cause-and-effect transition fits."""),
    rw(EI, TR, 2, r"""Early telephones had to be connected by human operators. ______, automatic exchanges allowed callers to dial numbers themselves.""",
       Q_TR, ["Later", "For example", "Similarly", "In other words"], "A",
       r"""Automatic exchanges came after operator-connected phones, so a time transition, "Later", fits."""),
    rw(EI, RS, 1, NOTES + r"""
• The Nile is about 6,650 kilometres long.
• It flows through eleven countries.
• It ends in the Mediterranean Sea.""",
       "The student wants to emphasise the length of the Nile. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["The Nile stretches for about 6,650 kilometres.", "The Nile flows through eleven countries.",
        "The Nile ends in the Mediterranean Sea.", "The Nile is a river in Africa."], "A",
       r"""Only one choice gives the river's length, which is the student's goal."""),
    rw(EI, RS, 2, NOTES + r"""
• Mae Jemison is an American engineer and physician.
• In 1992, she flew aboard the space shuttle Endeavour.
• She was the first African American woman to travel to space.
• She later founded a technology company.""",
       "The student wants to present Jemison's historic achievement. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["In 1992, aboard the shuttle Endeavour, Mae Jemison became the first African American woman to travel to space.",
        "Mae Jemison is an American engineer and physician.", "Mae Jemison founded a technology company.",
        "The space shuttle Endeavour flew in 1992."], "A",
       r"""Her historic achievement is being the first African American woman in space, and only one choice states it."""),
]
