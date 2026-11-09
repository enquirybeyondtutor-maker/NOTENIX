r"""Practice Test 3, Reading and Writing: Module 2 harder. Original questions."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
WIC, TSP, CTC = "Words in Context", "Text Structure and Purpose", "Cross-Text Connections"
CID, COET, COEQ, INF = "Central Ideas and Details", "Command of Evidence: Textual", "Command of Evidence: Quantitative", "Inferences"
BND, FSS, TR, RS = "Boundaries", "Form, Structure, and Sense", "Transitions", "Rhetorical Synthesis"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"

RW2H = [
    rw(CS, WIC, 2, r"""The biography is unusually ______: rather than praising its subject, the author records the inventor's failures and cruelties as carefully as his achievements.""",
       Q_WIC, ["candid", "flattering", "speculative", "abridged"], "A",
       r"""Recording failures and cruelties as carefully as achievements is frank and honest: "candid". "Flattering" is the opposite."""),
    rw(CS, WIC, 3, r"""Far from being ______, the town's ban on cars in the old centre was the result of fifteen years of public meetings, traffic studies and trial closures.""",
       Q_WIC, ["impulsive", "deliberate", "permanent", "controversial"], "A",
       r""""Far from" signals the opposite of the evidence that follows. Fifteen years of meetings and studies show careful planning, so the ban was far from "impulsive"."""),
    rw(CS, WIC, 3, r"""Early reviewers found the composer's harmonies ______, but audiences a generation later heard in them a beauty that the critics had been too unsettled to notice.""",
       Q_WIC, ["jarring", "soothing", "conventional", "imitative"], "A",
       r"""The critics were "unsettled", so they found the harmonies harsh: "jarring". "Soothing" and "conventional" would not unsettle anyone."""),
    rw(CS, WIC, 3, r"""The diplomat's reply was a model of ______: in three short sentences, she declined the proposal, thanked its authors and left the door open to future talks.""",
       Q_WIC, ["tact", "bluntness", "verbosity", "indecision"], "A",
       r"""Declining, thanking and keeping talks possible, all briefly and politely, shows skill in handling a delicate situation: "tact". "Verbosity" contradicts "three short sentences"."""),
    rw(CS, TSP, 2, r"""The following text is from a 1917 poem.

The river does not hurry, yet it reaches
The sea it never saw, and never sought;
It finds its way through stones and sand and beaches
By going on, and not by any thought.""",
       "Which choice best describes the overall structure of the text?",
       ["It describes a river's steady progress and suggests that persistence, not planning, carries it to its goal.",
        "It contrasts a calm river with a stormy sea.",
        "It tells the story of a journey made by the speaker along a river.",
        "It describes the plants and animals found along a river."], "A",
       r"""The river reaches the sea "by going on, and not by any thought": the poem shows steady movement succeeding without a plan."""),
    rw(CS, TSP, 3, r"""Scholars have long read the explorer's journals as a record of a lonely journey through empty land. Historian Ruth Banda argues that this reading overlooks the dozens of local guides, interpreters and porters whom the explorer mentions only in passing, often without names. Without them, she contends, the expedition would not have survived its first month.""",
       "Which choice best states the main purpose of the text?",
       ["To present an argument that the explorer's journey depended on people his journals largely ignored",
        "To describe the landscape the explorer crossed",
        "To show that the explorer's journals were written by someone else",
        "To argue that the expedition failed in its first month"], "A",
       r"""The text introduces Banda's challenge to the "lonely journey" reading: the guides and porters, barely mentioned, were essential. It does not say the expedition failed or the journals were faked."""),
    rw(CS, TSP, 3, r"""Many birds sing complex songs, and for decades researchers assumed that only males sang. Then a survey of over a thousand songbird species found that females sing in most of them. The early assumption, it turned out, reflected where researchers had looked: mostly in Europe and North America, where female song is relatively rare.""",
       "Which choice best describes the function of the third sentence in the text as a whole?",
       ["It explains why researchers had held a mistaken assumption.", "It describes the songs that female birds sing.",
        "It questions the results of the survey mentioned in the second sentence.", "It argues that European birds sing more than others."], "A",
       r"""The first two sentences give the old assumption and the evidence against it; the third explains where the mistake came from."""),
    rw(CS, CTC, 3, r"""Text 1
Proponents of "learning styles" claim that students learn best when lessons match their preferred style, such as visual or auditory. Teachers, they argue, should identify each student's style and teach accordingly.

Text 2
When researchers taught students in either their preferred style or a different one, test results did not differ. What helped most was matching the method to the content: diagrams for maps, for instance, and spoken examples for pronunciation.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the proponents in Text 1?",
       ["By arguing that the type of content matters more than a student's preferred style",
        "By agreeing that teachers should identify each student's learning style",
        "By claiming that visual lessons are always best",
        "By suggesting that students should choose what they study"], "A",
       r"""The study found matching students' preferred styles made no difference, while matching method to content helped, so the researchers would put content ahead of learning styles."""),
    rw(II, CID, 2, r"""The following text is adapted from Elizabeth Gaskell's 1855 novel North and South.

Margaret had been accustomed to the quiet, sunny lanes of the south. In the northern town, the sky was low and grey with smoke, and the streets were crowded with workers hurrying to the mills. She felt the change as a heaviness she could not at first explain.""",
       "Which choice best describes Margaret's response to the northern town?",
       ["She feels weighed down by how different it is from the south she knew.", "She is delighted by the busy streets and mills.",
        "She is eager to work in one of the mills.", "She finds the town quieter than she expected."], "A",
       r"""Used to quiet, sunny lanes, she feels "a heaviness" in the smoky, crowded town, a response to the contrast."""),
    rw(II, CID, 3, r"""Economists studying a city's new minimum wage expected restaurants to cut jobs. Instead, employment in restaurants stayed steady. Many owners reported that higher pay reduced how often workers quit, which cut the costs of hiring and training new staff. The economists suggest that for some businesses, lower staff turnover can partly offset the cost of higher wages.""",
       "Which choice best states the main idea of the text?",
       ["A higher minimum wage did not reduce restaurant jobs, partly because it lowered staff turnover costs.",
        "Restaurants in the city closed because of higher wages.", "Economists always predict job losses correctly.",
        "Training new staff costs nothing for most restaurants."], "A",
       r"""Jobs held steady against expectations, and owners linked higher pay to fewer resignations and lower hiring costs, which the economists say partly offsets wages."""),
    rw(II, COET, 2, r"""The following text is from a 1909 novel. The narrator describes her brother.

Thomas could never sit still. At dinner he tapped the table; in church he counted the windows; and on the long train journey to the coast he walked the length of the carriage so often that the guard began to greet him by name.""",
       "Which quotation from the text most effectively illustrates the narrator's claim about Thomas?",
       ["\"he walked the length of the carriage so often that the guard began to greet him by name\"",
        "\"on the long train journey to the coast\"", "\"The narrator describes her brother\"", "\"in church\""], "A",
       r"""The claim is that he could never sit still; walking the carriage so often that the guard knew him illustrates it. The other quotations only give places or the introduction."""),
    rw(II, COET, 3, r"""Neuroscientist Hana Mori hypothesises that a nap after learning helps people remember new information, because during sleep the brain replays recently learned material.""",
       "Which finding, if true, would most directly support Mori's hypothesis?",
       ["Volunteers who napped after learning word pairs remembered more of them than volunteers who stayed awake, and brain scans showed patterns from the learning session recurring during their naps.",
        "Many people feel more refreshed after a short nap.", "Some people find it hard to nap during the day.",
        "Volunteers remembered more words in the morning than in the evening."], "A",
       r"""The hypothesis has two parts: naps improve memory, and the brain replays the material. Better recall after napping plus learning-session patterns recurring during sleep supports both."""),
    rw(II, COEQ, 3, r"""A city compared commuting before and after opening a new tram line.

| Mode | Share of commuters before | Share after |
|---|---|---|
| Car | 52% | 41% |
| Bus | 22% | 18% |
| Tram | 0% | 17% |
| Walk or cycle | 26% | 24% |

A planner claims that most new tram riders switched from cars rather than from other ways of travelling.""",
       "Which choice best describes data from the table that support the planner's claim?",
       ["The car share fell by 11 percentage points, while the bus and walk-or-cycle shares fell by only 4 and 2.",
        "The tram carried 17% of commuters after it opened.", "Cars were the most common mode both before and after.",
        "Walking and cycling made up about a quarter of commuting."], "A",
       r"""The tram took 17 points. Of the losses, cars fell 11 points, buses 4 and walking or cycling 2, so most of the tram's share came from cars."""),
    rw(II, COEQ, 3, r"""Researchers tracked a lake's water clarity, measured as how deep a white disc stays visible.

| Year | Visibility (m) | Farms using a new fertiliser rule |
|---|---|---|
| 2016 | 2.1 | 10% |
| 2018 | 2.4 | 35% |
| 2020 | 3.0 | 60% |
| 2022 | 3.6 | 85% |

The researchers suggest that the fertiliser rule, which reduces nutrients washing into the lake, may have helped clear the water. ______""",
       "Which choice most effectively uses data from the table to support the researchers' suggestion?",
       ["As the share of farms following the rule rose from 10% to 85%, visibility increased from 2.1 m to 3.6 m.",
        "Visibility was 3.6 m in 2022.", "In 2018, 35% of farms followed the rule.", "Visibility was lowest in 2016."], "A",
       r"""The suggestion links the rule to clearer water. Only the statement showing visibility rising alongside wider use of the rule supports that link."""),
    rw(II, INF, 3, r"""Some mountain plants flower only once in their lives, often after decades of growth, and then die. One such plant stores sugars in its thick roots for many years before producing a single tall flower spike. Researchers found that plants growing in richer soil flowered several years earlier than plants in poorer soil. This suggests that the timing of flowering may depend on ______""",
       "Which choice most logically completes the text?",
       ["how quickly the plant can build up enough stored energy.", "how tall the plant's flower spike will be.",
        "how many other plants grow nearby.", "the age of the oldest plant in the area."], "A",
       r"""The plant stores sugars for years before flowering, and plants in richer soil (which could build reserves faster) flowered earlier. So timing likely depends on reaching enough stored energy."""),
    rw(II, INF, 3, r"""In a trial, a supermarket moved fruit from the back of the store to the entrance. Fruit sales rose by a third, while sales of sweets, which were not moved, stayed the same. Shoppers' total spending did not change. The trial suggests that the new layout ______""",
       "Which choice most logically completes the text?",
       ["shifted some spending toward fruit without making shoppers spend more overall.",
        "persuaded shoppers to stop buying sweets.", "increased the amount shoppers spent on every visit.",
        "had no effect on what shoppers bought."], "A",
       r"""Fruit sales rose but total spending did not, so money moved to fruit from other items (not sweets, which stayed the same). Shoppers did not spend more overall."""),
    rw(SEC, BND, 2, r"""The archive contains three kinds of ______ handwritten letters, printed pamphlets and early photographs.""",
       Q_SEC, ["material:", "material;", "material", "material, which"], "A",
       r"""A complete sentence introduces the list, so a colon is correct."""),
    rw(SEC, BND, 3, r"""The software update fixed the security ______ it also made the app noticeably slower on older phones.""",
       Q_SEC, ["flaw; however,", "flaw, however,", "flaw however", "flaw; however"], "A",
       r""""However" begins a new complete sentence, so a semicolon goes before it and a comma after it."""),
    rw(SEC, BND, 3, r"""In 1953, Tenzing Norgay and Edmund Hillary reached the summit of ______ a climb that made them famous around the world.""",
       Q_SEC, ["Everest,", "Everest;", "Everest.", "Everest"], "A",
       r""""A climb that made them famous" is not a complete sentence; it describes the event and attaches with a comma."""),
    rw(SEC, BND, 3, r"""The engineers who designed the original ______ never imagined that it would one day carry four times as much traffic.""",
       Q_SEC, ["bridge", "bridge,", "bridge;", "bridge:"], "A",
       r""""Who designed the original bridge" identifies which engineers, and "engineers" is followed by its verb "imagined". No punctuation belongs between them."""),
    rw(SEC, FSS, 2, r"""The collection of fossils, which includes several complete skeletons, ______ attracted researchers from around the world.""",
       Q_SEC, ["has", "have", "are", "were"], "A",
       r"""The subject is "collection", which is singular; "of fossils" and the "which" clause describe it. So "has" is needed."""),
    rw(SEC, FSS, 3, r"""Exhausted after the long climb, ______""",
       Q_SEC, ["the hikers rested beside the lake before starting down.", "the lake was where the hikers rested before starting down.",
               "a rest beside the lake was taken before starting down.", "resting beside the lake came before the hikers started down."], "A",
       r""""Exhausted after the long climb" must describe the hikers, so "the hikers" must come right after the comma."""),
    rw(SEC, FSS, 3, r"""Neither the manager nor her assistants ______ aware of the problem until a customer pointed it out.""",
       Q_SEC, ["were", "was", "is", "has been"], "A",
       r"""With "neither... nor", the verb agrees with the nearer subject, "assistants", which is plural, so "were" is needed."""),
    rw(EI, TR, 2, r"""The first vaccines were developed against smallpox in the late 1700s. ______, it took almost two centuries of vaccination campaigns before the disease was finally eliminated worldwide in 1980.""",
       Q_TR, ["Even so", "As a result", "For example", "Similarly"], "A",
       r"""Despite an early vaccine, elimination took two centuries: a contrast that "Even so" signals."""),
    rw(EI, TR, 3, r"""Some economists argue that cities should charge drivers to enter congested centres. Such charges, ______, have reduced traffic in several cities, though critics say they fall hardest on people with lower incomes.""",
       Q_TR, ["in practice", "by contrast", "instead", "nonetheless"], "A",
       r"""The sentence moves from the economists' argument to what charges have done in real cities, so "in practice" fits."""),
    rw(EI, RS, 3, r"""While researching a topic, a student has taken the following notes:
• Hedy Lamarr was a film star of the 1930s and 1940s.
• During the Second World War, she co-invented a radio system that switched frequencies to stop signals being jammed.
• The navy did not use it at the time.
• Its principle was later used in technologies such as Wi-Fi and Bluetooth.""",
       "The student wants to emphasise the long-term importance of Lamarr's invention. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Although the navy did not use it at first, the frequency-switching principle Lamarr co-invented was later used in Wi-Fi and Bluetooth.",
        "Hedy Lamarr was a film star of the 1930s and 1940s.", "During the Second World War, Lamarr co-invented a radio system.",
        "The navy did not use Lamarr's invention at the time."], "A",
       r"""Long-term importance means its later use. Only the sentence linking the principle to Wi-Fi and Bluetooth shows that."""),
    rw(EI, RS, 3, r"""While researching a topic, a student has taken the following notes:
• Coral reefs cover less than 1% of the ocean floor.
• They are home to about 25% of all marine species.
• Rising sea temperatures can cause coral bleaching.
• Bleached corals can recover if temperatures drop quickly.""",
       "The student wants to emphasise how important coral reefs are for ocean life relative to their size. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Although coral reefs cover less than 1% of the ocean floor, they are home to about a quarter of all marine species.",
        "Rising sea temperatures can cause coral bleaching.", "Bleached corals can recover if temperatures drop quickly.",
        "Coral reefs are found in the ocean."], "A",
       r"""Only the sentence comparing their small area with the share of species they support meets the goal."""),
]
