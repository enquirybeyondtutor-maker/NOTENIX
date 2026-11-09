r"""Practice Test 2, Reading and Writing: Module 2 harder. Original questions."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
WIC, TSP, CTC = "Words in Context", "Text Structure and Purpose", "Cross-Text Connections"
CID, COET, COEQ, INF = "Central Ideas and Details", "Command of Evidence: Textual", "Command of Evidence: Quantitative", "Inferences"
BND, FSS, TR, RS = "Boundaries", "Form, Structure, and Sense", "Transitions", "Rhetorical Synthesis"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"

RW2H = [
    rw(CS, WIC, 2,
       r"""The historian's account of the trade route is ______: drawing on ship records, merchants' letters and customs ledgers in four languages, it traces the movement of goods across three centuries in remarkable detail.""",
       Q_WIC, ["comprehensive", "speculative", "derivative", "cursory"], "A",
       r"""Using many kinds of sources across centuries "in remarkable detail" makes the account complete: "comprehensive". "Cursory" (hasty) and "speculative" (based on guesses) contradict this."""),
    rw(CS, WIC, 3,
       r"""The negotiator's tone was ______ throughout the talks; even when the other side made provocative demands, she responded calmly and kept the discussion focused on practical details.""",
       Q_WIC, ["measured", "strident", "evasive", "capricious"], "A",
       r"""Responding calmly and staying practical under provocation describes a controlled, "measured" tone. "Strident" (harsh) and "capricious" (unpredictable) are the opposite."""),
    rw(CS, WIC, 3,
       r"""Early critics thought the poet's habit of leaving lines unfinished was careless, but many scholars now see it as ______: a deliberate technique that invites readers to complete the thought themselves.""",
       Q_WIC, ["intentional", "accidental", "outdated", "imitative"], "A",
       r"""The colon explains the blank: "a deliberate technique". So scholars see the unfinished lines as "intentional", in contrast with the early critics' view of carelessness."""),
    rw(CS, WIC, 3,
       r"""The company's claims about its product's environmental benefits proved ______; independent testing found that the product produced nearly as much waste as the competitors it claimed to outperform.""",
       Q_WIC, ["specious", "modest", "verifiable", "prescient"], "A",
       r"""Claims that testing showed to be untrue, though they seemed convincing, are "specious". "Verifiable" and "prescient" (showing foresight) contradict the testing."""),
    rw(CS, TSP, 2,
       r"""The following text is from a 1923 poem.

I kept the letters in a cedar box
And did not read them for a dozen years;
Today I turned the small and rusted locks,
Expecting grief, and found instead no tears,
But only gladness that such words were said,
And gratitude for every line I read.""",
       "Which choice best describes the overall structure of the text?",
       ["The speaker describes avoiding something for years, then reports an unexpected reaction on finally facing it.",
        "The speaker describes writing letters and explains why they were never sent.",
        "The speaker compares two boxes of letters from different times.",
        "The speaker regrets keeping the letters and decides to destroy them."], "A",
       r"""The speaker left the letters unread for twelve years, then opened them "expecting grief" but felt gladness and gratitude instead: avoidance followed by a surprising response."""),
    rw(CS, TSP, 3,
       r"""Conventional accounts treat the Industrial Revolution as a story of inventors and their machines. Economic historian Priya Natarajan argues that this emphasis is misleading. Many of the key machines, she notes, had been invented decades before they were widely used; what changed was the availability of cheap coal and growing markets that made adopting them profitable.""",
       "Which choice best states the main purpose of the text?",
       ["To present an argument that economic conditions, rather than inventions alone, drove industrial change",
        "To describe how the first steam engines were built",
        "To show that inventors played no part in the Industrial Revolution",
        "To compare coal production in different countries"], "A",
       r"""The text introduces Natarajan's view that the usual focus on inventors misleads: machines existed for decades, and cheap coal and markets made using them pay. She qualifies the inventors' role but does not say they played no part."""),
    rw(CS, TSP, 3,
       r"""Octopuses can change the colour and texture of their skin in a fraction of a second, matching rocks, coral or sand. Strangely, most octopuses appear to be colour-blind: their eyes have only one type of light receptor. Researchers have proposed that light-sensitive proteins in the skin itself may help octopuses sense the colours around them.""",
       "Which choice best describes the function of the second sentence in the text as a whole?",
       ["It presents a puzzling fact that the third sentence offers a possible explanation for.",
        "It provides evidence that octopuses cannot change colour.",
        "It explains how octopuses match their surroundings so quickly.",
        "It contradicts the researchers mentioned in the third sentence."], "A",
       r"""Colour-blind animals matching colours is puzzling ("Strangely"); the third sentence proposes how they might sense colour anyway. The second sentence does not deny that octopuses change colour."""),
    rw(CS, CTC, 3,
       r"""Text 1
Some educators argue that handwriting lessons are outdated now that most writing is done on keyboards. Time spent practising handwriting, they say, would be better used teaching typing and digital skills.

Text 2
In a study of young children, those who practised writing letters by hand later recognised those letters more quickly than children who practised typing them. The researchers suggest that forming letters by hand helps children learn their shapes, which supports early reading.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the educators in Text 1?",
       ["By cautioning that handwriting practice may have benefits for young children's reading that typing does not provide",
        "By agreeing that handwriting lessons should be replaced by typing lessons",
        "By arguing that typing harms children's ability to read",
        "By claiming that most writing is still done by hand"], "A",
       r"""The study found handwriting helped children recognise letters, which supports reading. The researchers would warn that dropping handwriting could lose this benefit. They do not claim typing does harm."""),
    rw(II, CID, 2,
       r"""The following text is adapted from Charlotte Brontë's 1847 novel Jane Eyre.

I was glad of it: I never liked long walks, especially on chilly afternoons: dreadful to me was the coming home in the raw twilight, with nipped fingers and toes, and a heart saddened by the chidings of Bessie, the nurse.""",
       "Based on the text, why is the narrator glad?",
       ["Because she will not have to go on a long walk, which she disliked",
        "Because she enjoys chilly afternoons outdoors",
        "Because Bessie has praised her",
        "Because she has finally reached home"], "A",
       r"""She is glad of "it" and immediately explains that she "never liked long walks", especially coming home cold and scolded. So she is glad to avoid a walk."""),
    rw(II, CID, 3,
       r"""Researchers studying city trees found that streets with more trees had lower summer temperatures, fewer reports of heat-related illness and higher property values. However, trees were far more common in wealthier neighbourhoods. The researchers argue that planting trees in poorer neighbourhoods could reduce health risks for the people most exposed to extreme heat.""",
       "Which choice best states the main idea of the text?",
       ["Because trees bring benefits that are unevenly spread, planting more in poorer areas could improve residents' health.",
        "Wealthy neighbourhoods should remove some of their trees.",
        "Property values rise whenever trees are planted.",
        "Extreme heat affects all neighbourhoods equally."], "A",
       r"""The text links trees to cooler streets and better health, notes that trees are concentrated in wealthier areas, and concludes that planting in poorer areas could reduce health risks. Nothing suggests removing trees."""),
    rw(II, COET, 2,
       r"""The following text is from a 1915 novel. Clara is about to give her first public speech.

Clara had rehearsed the speech so many times that she could have recited it in her sleep. Yet as she stepped onto the platform, her hands trembled so badly that the pages rattled, and for a terrible moment the first line would not come.""",
       "Which quotation from the text most effectively illustrates that Clara is nervous?",
       ["\"her hands trembled so badly that the pages rattled\"",
        "\"Clara had rehearsed the speech so many times\"",
        "\"she could have recited it in her sleep\"",
        "\"as she stepped onto the platform\""], "A",
       r"""Trembling hands that rattle the pages are a physical sign of nerves. The other quotations show preparation or simply describe her movement."""),
    rw(II, COET, 3,
       r"""Marine scientist Ibrahim Saleh hypothesises that a coral species survives warm water events better when it lives near seagrass meadows, because the seagrass lowers the acidity of the surrounding water.""",
       "Which finding, if true, would most directly support Saleh's hypothesis?",
       ["During a recent warm event, colonies of the coral growing beside seagrass meadows, where water was measurably less acidic, lost far less coral than colonies of the same species growing away from seagrass.",
        "Seagrass meadows provide shelter for many species of young fish.",
        "The coral species is found in warm waters around the world.",
        "Warm water events have become more frequent in recent decades."], "A",
       r"""The hypothesis links survival near seagrass to lower acidity. Same-species colonies beside seagrass, in less acidic water, surviving better supports both parts of it."""),
    rw(II, COEQ, 3,
       r"""A researcher surveyed adults about how many hours of sleep they usually get and how they rated their own concentration at work.

| Sleep per night | Rated concentration "good" | Rated concentration "poor" |
|---|---|---|
| Less than 6 hours | 28% | 72% |
| 6 to 7 hours | 55% | 45% |
| 7 to 8 hours | 74% | 26% |
| More than 8 hours | 70% | 30% |

The researcher concludes that, in this survey, more sleep was generally associated with better self-rated concentration, but that the benefit appeared to level off beyond a certain amount.""",
       "Which choice best describes data from the table that support the researcher's conclusion?",
       ["The share rating their concentration as good rose from 28% to 74% across the first three groups but was about the same for those sleeping more than 8 hours.",
        "Most adults who slept less than 6 hours rated their concentration as poor.",
        "The share rating their concentration as poor was 26% for those sleeping 7 to 8 hours.",
        "More adults slept 7 to 8 hours than any other amount."], "A",
       r"""The conclusion has two parts: improvement with more sleep, then levelling off. Only the description of the rise across three groups followed by a similar figure (70%) for the longest sleepers covers both. The table does not give how many adults were in each group."""),
    rw(II, COEQ, 3,
       r"""A city tracked the number of bike-share trips and the number of bike-share stations.

| Year | Stations | Trips (thousands) |
|---|---|---|
| 2019 | 120 | 600 |
| 2020 | 150 | 780 |
| 2021 | 200 | 1,000 |
| 2022 | 250 | 1,250 |

A transport official claims that each new station added roughly the same number of yearly trips. ______""",
       "Which choice most effectively uses data from the table to support the official's claim?",
       ["Across the years, trips stayed at about 5,000 per station, rising in step with the number of stations.",
        "The number of stations doubled between 2019 and 2022.",
        "The number of trips was highest in 2022.",
        "The city added 50 stations between 2021 and 2022."], "A",
       r"""Trips divided by stations is 5,000 in 2019 (600,000 ÷ 120), 5,200 in 2020 and 5,000 in 2021 and 2022: roughly constant. That supports each station adding about the same number of trips. The other facts say nothing about trips per station."""),
    rw(II, INF, 3,
       r"""When glaciers melt, the land beneath them, freed of the ice's enormous weight, slowly rises, a process called isostatic rebound. In parts of northern Scandinavia, where thick ice sheets melted thousands of years ago, the land is still rising by up to a centimetre a year. Harbour structures built in some of these towns centuries ago now ______""",
       "Which choice most logically completes the text?",
       ["stand further above the water than they did when they were built.",
        "lie deeper underwater than they did when they were built.",
        "have been crushed by the weight of new glaciers.",
        "show that the ice sheets never covered the region."], "A",
       r"""If the land is still rising, structures built centuries ago have been lifted with it, so they now sit higher relative to the sea."""),
    rw(II, INF, 3,
       r"""Some plants release chemicals into the soil that slow the growth of nearby plants, a strategy called allelopathy. A researcher found that a certain shrub releases such chemicals only when its roots are crowded by roots of other species, not when it grows alone or among shrubs of its own kind. This suggests that the shrub ______""",
       "Which choice most logically completes the text?",
       ["releases the chemicals mainly in response to competition from other species.",
        "cannot grow in soil without the chemicals.",
        "uses the chemicals to help shrubs of its own kind grow faster.",
        "releases the chemicals at all times, whatever plants are nearby."], "A",
       r"""The shrub releases the chemicals only when crowded by other species, not alone or among its own kind, which points to a response to competition from other species."""),
    rw(SEC, BND, 2,
       r"""The expedition faced two main ______ the extreme cold and the difficulty of carrying enough food across the ice.""",
       Q_SEC, ["challenges:", "challenges;", "challenges", "challenges, which"], "A",
       r"""A complete sentence introduces the two challenges, so a colon is used. A semicolon would need a complete sentence after it."""),
    rw(SEC, BND, 3,
       r"""The architect insisted that the museum's walls be made of local ______ she argued that the building should look as though it had grown out of the surrounding hills.""",
       Q_SEC, ["stone;", "stone,", "stone", "stone, and,"], "A",
       r"""Both parts are complete sentences, so a semicolon is needed. A comma alone creates a comma splice."""),
    rw(SEC, BND, 3,
       r"""In 1928, Alexander Fleming noticed that mould growing on one of his culture plates had killed the surrounding ______ a chance observation that led to the development of penicillin.""",
       Q_SEC, ["bacteria,", "bacteria;", "bacteria.", "bacteria"], "A",
       r""""A chance observation that led to..." is not a complete sentence; it describes what Fleming noticed. So it attaches with a comma, not a semicolon or full stop."""),
    rw(SEC, BND, 3,
       r"""The two scientists who first described the ______ worked in separate laboratories on different continents and did not learn of each other's research until both papers had been published.""",
       Q_SEC, ["phenomenon", "phenomenon,", "phenomenon;", "phenomenon:"], "A",
       r""""Who first described the phenomenon" identifies which scientists, and the subject "scientists" is followed directly by its verb "worked". No punctuation belongs between them."""),
    rw(SEC, FSS, 2,
       r"""The results of the survey, which was carried out in twelve countries over three years, ______ that most people now get their news online.""",
       Q_SEC, ["show", "shows", "is showing", "has shown"], "A",
       r"""The subject is "results", which is plural; "of the survey" and the "which" clause only describe it. So the plural verb "show" is needed."""),
    rw(SEC, FSS, 3,
       r"""Having studied the ruins for over a decade, ______""",
       Q_SEC,
       ["the archaeologist was confident that the city had been abandoned after a drought.",
        "the city's abandonment after a drought seemed certain to the archaeologist.",
        "a drought was the archaeologist's explanation for the city's abandonment.",
        "it was clear to the archaeologist that a drought had caused the city's abandonment."], "A",
       r""""Having studied the ruins for over a decade" must describe whoever studied them, so "the archaeologist" must come right after the comma."""),
    rw(SEC, FSS, 3,
       r"""Neither the committee members nor the director ______ willing to approve the budget without further review.""",
       Q_SEC, ["was", "were", "are", "have been"], "A",
       r"""With "neither... nor", the verb agrees with the nearer subject, "the director", which is singular, so "was" is needed."""),
    rw(EI, TR, 2,
       r"""The first version of the software was slow and often crashed. The developers rewrote much of the code. ______, the second version ran twice as fast and rarely failed.""",
       Q_TR, ["Consequently", "Nevertheless", "For example", "Similarly"], "A",
       r"""The faster, more reliable second version resulted from rewriting the code, so "Consequently" fits."""),
    rw(EI, TR, 3,
       r"""Many early photographers saw their work as a scientific tool for recording the world accurately. Others, ______, used the camera to create dreamlike, artistic images that made no attempt at realism.""",
       Q_TR, ["by contrast", "as a result", "in other words", "for instance"], "A",
       r"""Dreamlike, unrealistic images contrast with accurate scientific records, so "by contrast" fits."""),
    rw(EI, RS, 3,
       r"""While researching a topic, a student has taken the following notes:
• Mary Anning (1799–1847) was a British fossil collector.
• She found the first complete plesiosaur skeleton in 1823.
• Because she was a woman, she could not join the Geological Society of London.
• Scientists often used her discoveries without crediting her.""",
       "The student wants to emphasise the obstacles Anning faced despite her achievements. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Although Mary Anning found the first complete plesiosaur skeleton, she was barred from the Geological Society, and scientists often used her finds without credit.",
        "Mary Anning was a British fossil collector who lived from 1799 to 1847.",
        "In 1823, Mary Anning found the first complete plesiosaur skeleton.",
        "The Geological Society of London studies fossils and rocks."], "A",
       r"""The goal pairs her achievement with the obstacles she faced. Only the sentence combining the plesiosaur find with her exclusion and lack of credit does both."""),
    rw(EI, RS, 3,
       r"""While researching a topic, a student has taken the following notes:
• Bamboo is a type of grass.
• Some species can grow up to 90 centimetres in a single day.
• It reaches full height in just a few months.
• Many builders use it because it is strong, light and quick to replace.""",
       "The student wants to explain why bamboo is a practical building material. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Because bamboo is strong and light and grows back quickly, many builders find it a practical material.",
        "Bamboo, a type of grass, can grow up to 90 centimetres in a single day.",
        "Bamboo reaches its full height in just a few months.",
        "There are many species of bamboo around the world."], "A",
       r"""The goal is why builders find bamboo practical. Only the sentence giving its strength, lightness and quick regrowth as the reasons does that."""),
]
