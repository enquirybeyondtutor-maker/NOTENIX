r"""SAT skill drills, Reading and Writing: 6 original questions per skill (11 skills), mixed difficulty.
Imported by drills.py. Explanations never name options by letter (answers are spread automatically)."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"

D = {}

D["Words in Context"] = [
    rw(CS, "Words in Context", 1, r"""The hiking trail is so ______ that families with young children can complete it in under an hour.""",
       Q_WIC, ["gentle", "treacherous", "remote", "lengthy"], "A",
       r"""A trail young children finish quickly must be easy: "gentle". "Treacherous" and "lengthy" contradict this."""),
    rw(CS, "Words in Context", 1, r"""Because the meeting ran so long, several members left ______, before the final vote had been taken.""",
       Q_WIC, ["early", "late", "together", "happily"], "A",
       r"""Leaving before the final vote means leaving before the end: "early"."""),
    rw(CS, "Words in Context", 2, r"""The documentary's narrator remains ______ throughout, presenting the arguments of both sides without revealing which she finds more convincing.""",
       Q_WIC, ["impartial", "enthusiastic", "sarcastic", "uncertain"], "A",
       r"""Presenting both sides without showing a preference is being "impartial". "Uncertain" suggests confusion, which the text does not describe."""),
    rw(CS, "Words in Context", 2, r"""Rather than replacing the old wooden floors, the builders chose to ______ them, sanding away the damage and sealing the original boards.""",
       Q_WIC, ["restore", "demolish", "conceal", "measure"], "A",
       r"""Sanding away damage and sealing the original boards brings them back to good condition: "restore"."""),
    rw(CS, "Words in Context", 3, r"""The scientist's early papers were cautious, but her later work grew increasingly ______, advancing bold theories that many colleagues considered premature.""",
       Q_WIC, ["audacious", "tentative", "derivative", "meticulous"], "A",
       r"""Bold theories that others think premature contrast with "cautious" early work, so the later work was "audacious". "Tentative" means hesitant, the opposite."""),
    rw(CS, "Words in Context", 3, r"""Though the treaty was hailed as a breakthrough, its terms were so ______ that each side later claimed the agreement supported its own, contradictory position.""",
       Q_WIC, ["ambiguous", "explicit", "punitive", "concise"], "A",
       r"""Terms that let each side claim opposite meanings are open to more than one reading: "ambiguous". "Explicit" means clear, the opposite."""),
]

D["Text Structure and Purpose"] = [
    rw(CS, "Text Structure and Purpose", 1, r"""Camels can go for days without drinking. When they do find water, they can drink over 100 litres in about ten minutes, and their bodies are built to absorb it quickly without harm.""",
       "Which choice best states the main purpose of the text?",
       ["To describe how camels cope with long periods without water", "To argue that camels should be protected",
        "To compare camels with horses", "To explain where camels find water in the desert"], "A",
       r"""The text describes camels going days without water and drinking large amounts quickly: how they cope with scarce water."""),
    rw(CS, "Text Structure and Purpose", 2, r"""Many people think tomatoes have always been part of Italian cooking. In fact, tomatoes came from the Americas and were not widely eaten in Italy until the 1800s. Before then, many Europeans grew them only as decorative plants.""",
       "Which choice best describes the overall structure of the text?",
       ["It presents a common belief and then corrects it with historical facts.", "It gives a recipe and explains its origins.",
        "It compares Italian and American cooking.", "It argues that tomatoes are healthier than other vegetables."], "A",
       r"""The first sentence gives a belief; "In fact" introduces facts that correct it."""),
    rw(CS, "Text Structure and Purpose", 2, r"""Most stars appear to twinkle at night. Planets, however, usually shine with a steady light. The difference arises because stars are so far away that they appear as single points, which are easily disturbed by Earth's moving air, while planets appear as tiny discs.""",
       "Which choice best describes the function of the third sentence in the text as a whole?",
       ["It explains the cause of the difference described in the first two sentences.", "It gives a new example of a twinkling star.",
        "It questions whether planets really shine steadily.", "It describes how astronomers measure distances."], "A",
       r"""The first two sentences describe a difference (stars twinkle, planets don't); the third explains why."""),
    rw(CS, "Text Structure and Purpose", 3, r"""The following text is from a 1920 novel. The narrator describes her aunt.

My aunt never raised her voice. When she disapproved of something, she simply became very still and very polite, and her politeness was more terrible than any shouting could have been.""",
       "Which choice best states the main purpose of the text?",
       ["To show that the aunt expressed disapproval in a quiet but powerful way", "To explain why the narrator moved away from her aunt",
        "To describe the aunt's physical appearance", "To suggest that the aunt was rarely polite"], "A",
       r"""The aunt never shouts; her stillness and politeness are "more terrible than any shouting", so the text shows her quiet but powerful disapproval."""),
    rw(CS, "Text Structure and Purpose", 3, r"""Economists long assumed that people make financial choices by carefully weighing costs and benefits. Experiments in behavioural economics have challenged this view, showing that people often choose differently depending on how options are described, even when the options are identical. Such findings have led many economists to build psychology into their models.""",
       "Which choice best describes the overall structure of the text?",
       ["It describes an assumption, presents evidence against it, and notes how the field has responded.",
        "It lists several economic theories without favouring any of them.",
        "It describes an experiment and then explains why its results were wrong.",
        "It argues that psychology is more important than economics."], "A",
       r"""Sentence one gives the assumption, sentence two the challenging evidence, and sentence three the field's response (building in psychology)."""),
    rw(CS, "Text Structure and Purpose", 2, r"""Some birds in cities sing at a higher pitch than birds of the same species in the countryside. Researchers think this helps their songs be heard over the low rumble of traffic.""",
       "Which choice best describes the function of the second sentence in the text as a whole?",
       ["It offers a possible explanation for the observation in the first sentence.", "It describes a second species of city bird.",
        "It contradicts the observation in the first sentence.", "It explains how researchers recorded the birds."], "A",
       r"""The first sentence observes higher-pitched songs in cities; the second suggests why (to be heard over traffic)."""),
]

D["Cross-Text Connections"] = [
    rw(CS, "Cross-Text Connections", 2, r"""Text 1
Some nutritionists say that eating late at night causes weight gain.

Text 2
A study found that people who ate the same total number of calories gained the same amount of weight whether they ate in the evening or earlier in the day. What mattered was how much they ate, not when.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the nutritionists in Text 1?",
       ["By arguing that the total amount eaten, not the time of eating, affects weight", "By agreeing that evening meals cause weight gain",
        "By claiming that eating late helps people lose weight", "By suggesting that nutritionists should study only breakfast"], "A",
       r"""The study found timing made no difference when calories were equal, so the researchers would say amount, not timing, matters."""),
    rw(CS, "Cross-Text Connections", 2, r"""Text 1
Electric cars are often described as having zero emissions.

Text 2
Electric cars produce no exhaust while driving. However, if the electricity that charges them comes from burning coal, the emissions are simply moved from the car to the power station.""",
       "Based on the texts, how would the author of Text 2 most likely respond to the description in Text 1?",
       ["By pointing out that it ignores emissions that may occur where the electricity is produced", "By agreeing that electric cars cause no pollution of any kind",
        "By arguing that petrol cars are cleaner than electric cars", "By claiming that power stations no longer burn coal"], "A",
       r"""Text 2 accepts there is no exhaust but notes emissions can move to the power station, so "zero emissions" leaves something out."""),
    rw(CS, "Cross-Text Connections", 3, r"""Text 1
Historians have often portrayed medieval peasants as almost never travelling more than a few miles from their villages.

Text 2
Records of pilgrimages, markets and seasonal work show that many medieval peasants travelled considerable distances, sometimes hundreds of miles, at least occasionally in their lives.""",
       "Based on the texts, how would the author of Text 2 most likely respond to the portrayal in Text 1?",
       ["By arguing that it underestimates how far many peasants travelled", "By agreeing that peasants rarely left their villages",
        "By claiming that peasants travelled more than modern people do", "By suggesting that pilgrimage records are unreliable"], "A",
       r"""Text 2 uses records to show many peasants travelled far at least sometimes, which challenges the "few miles" portrayal."""),
    rw(CS, "Cross-Text Connections", 3, r"""Text 1
Some educators claim that students learn more from reading on paper than on screens, because screens encourage skimming.

Text 2
In a study, students who read long texts on screens understood them less well than students reading on paper, but for short texts there was no difference. The researchers suggest the screen effect appears mainly with longer, more demanding reading.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the claim in Text 1?",
       ["By suggesting that the claim holds mainly for longer texts rather than all reading", "By rejecting the claim entirely",
        "By agreeing that screens harm understanding of every kind of text", "By arguing that paper encourages skimming"], "A",
       r"""The study found a screen disadvantage only for long texts, so the researchers would limit the claim to longer reading."""),
    rw(CS, "Cross-Text Connections", 2, r"""Text 1
Many gardeners believe that talking to plants makes them grow faster.

Text 2
In one experiment, plants exposed to recordings of human voices grew slightly taller than plants kept in silence. The researchers caution that vibration from sound, not the meaning of words, may be responsible.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the gardeners' belief in Text 1?",
       ["By noting that sound may affect growth, but not necessarily because of what is said", "By agreeing that plants understand human speech",
        "By claiming that silence helps plants grow faster", "By arguing that their experiment shows sound has no effect"], "A",
       r"""The plants grew slightly more with voices, but the researchers credit vibration, not meaning. So they partly support the belief while doubting the reason."""),
    rw(CS, "Cross-Text Connections", 3, r"""Text 1
The decline in bee populations is often blamed on pesticides alone.

Text 2
Studies show that bees exposed to low levels of pesticides cope well when they have plenty of varied flowers to feed on, but suffer serious losses when their diet is poor. Habitat loss, which reduces flower variety, may therefore make pesticides far more harmful.""",
       "Based on the texts, how would the author of Text 2 most likely respond to the view in Text 1?",
       ["By arguing that pesticides interact with other factors, such as habitat loss, rather than acting alone", "By agreeing that pesticides are the only cause of bee decline",
        "By claiming that pesticides are harmless to bees", "By suggesting that bees prefer a poor diet"], "A",
       r"""Text 2 shows pesticides do the most harm when combined with poor diet from habitat loss, so it would reject "pesticides alone"."""),
]

D["Central Ideas and Details"] = [
    rw(II, "Central Ideas and Details", 1, r"""Owls can turn their heads about 270 degrees. Because their eyes are fixed in their sockets and cannot move, turning the head is how owls look around.""",
       "Which choice best states the main idea of the text?",
       ["Owls turn their heads so far because their eyes cannot move.", "Owls have the largest eyes of any bird.",
        "Owls hunt only at night.", "Owls cannot see to the side."], "A",
       r"""The text links the wide head turn to eyes that cannot move in their sockets."""),
    rw(II, "Central Ideas and Details", 1, r"""The town's new library has a café, a recording studio and rooms people can book for meetings. On weekends, it runs free coding classes for children.""",
       "According to the text, what does the library offer on weekends?",
       ["Free coding classes for children", "Discounts at its café", "Concerts in its studio", "Longer opening hours"], "A",
       r"""The text says "On weekends, it runs free coding classes for children"."""),
    rw(II, "Central Ideas and Details", 2, r"""When the ship's engine failed, the crew did not panic. They rationed the drinking water, rigged a sail from spare canvas and steered by the stars. Eleven days later, they reached a fishing village, tired but unharmed.""",
       "Which choice best states the main idea of the text?",
       ["The crew survived a dangerous situation through calm, practical action.", "The ship's engine had never been reliable.",
        "Fishing villages often help stranded sailors.", "Steering by the stars is easier than using an engine."], "A",
       r"""The crew stayed calm, rationed water, made a sail and navigated, and reached safety: they survived through calm, practical action."""),
    rw(II, "Central Ideas and Details", 2, r"""The following text is adapted from a 1906 novel.

Mrs. Hale had lived in the house for thirty years and knew every creak of its stairs. She could tell, without looking, which of her children was coming down by the sound of their steps.""",
       "According to the text, what is true about Mrs. Hale?",
       ["She knows the house and her family so well that she can recognise footsteps.", "She has recently moved into the house.",
        "She dislikes the noise her children make.", "She has trouble hearing."], "A",
       r"""After thirty years she knows every creak and can tell which child is coming from their steps."""),
    rw(II, "Central Ideas and Details", 3, r"""Researchers studying a remote island found that its lizards had longer legs than lizards of the same species on the mainland. On the island, the lizards spend most of their time running across open ground, while mainland lizards mostly climb thin branches, where shorter legs give better balance. The researchers concluded that each population's leg length suits the surfaces it moves across.""",
       "Which choice best states the main idea of the text?",
       ["Differences in lizards' leg length appear to match the surfaces they live on.", "Island lizards are faster than all mainland animals.",
        "Mainland lizards are in danger of extinction.", "Lizards with long legs cannot climb at all."], "A",
       r"""The researchers link longer legs to running on open ground and shorter legs to climbing branches: leg length suits the surface."""),
    rw(II, "Central Ideas and Details", 3, r"""For centuries, the city's canals were its main roads, carrying goods and people. As railways and roads spread in the twentieth century, many canals were filled in. Recently, the city has begun reopening some of them, not for transport, but to provide green space, reduce summer heat and attract visitors.""",
       "Which choice best states the main idea of the text?",
       ["The city's canals have changed from transport routes to spaces valued for other reasons.", "Railways were the most important invention of the twentieth century.",
        "The city plans to fill in all of its remaining canals.", "Canals are a cheaper way to move goods than roads."], "A",
       r"""The text traces canals from main roads, to being filled in, to reopening for green space and visitors: a change in their purpose."""),
]

D["Command of Evidence: Textual"] = [
    rw(II, "Command of Evidence: Textual", 1, r"""A student claims that the school's recycling programme has reduced the amount of rubbish the school throws away.""",
       "Which finding, if true, would most directly support the student's claim?",
       ["The weight of rubbish collected from the school each month fell by a third after the programme began.", "The recycling bins are painted green.",
        "Most students know what recycling means.", "The programme was started by a student club."], "A",
       r"""A fall in rubbish collected after the programme began directly supports the claim. The other facts say nothing about the amount of rubbish."""),
    rw(II, "Command of Evidence: Textual", 2, r"""A researcher claims that reading aloud to young children improves their vocabulary.""",
       "Which finding, if true, would most directly support the researcher's claim?",
       ["Children whose parents were randomly assigned to read aloud daily learned more new words over a year than children whose parents were not.",
        "Many children enjoy being read to at bedtime.", "Picture books are popular gifts.", "Some parents read silently to themselves every evening."], "A",
       r"""Random assignment plus a vocabulary gain links reading aloud to vocabulary growth, which is the claim."""),
    rw(II, "Command of Evidence: Textual", 2, r"""The following text is from a 1913 short story. The narrator describes his neighbour.

Mr. Reyes was the most generous man on our street. Whenever a family fell on hard times, a basket of vegetables from his garden would appear on their doorstep before anyone had asked.""",
       "Which quotation from the text most effectively illustrates the narrator's claim about Mr. Reyes?",
       ["\"a basket of vegetables from his garden would appear on their doorstep before anyone had asked\"", "\"Mr. Reyes was the most generous man\"",
        "\"on our street\"", "\"Whenever a family fell\""], "A",
       r"""The claim is that he was generous; leaving vegetables for struggling families unasked is the example that shows it. Repeating the claim does not illustrate it."""),
    rw(II, "Command of Evidence: Textual", 3, r"""Biologist Ana Ruiz hypothesises that a species of frog avoids ponds containing predatory fish by detecting chemicals the fish release into the water, rather than by seeing the fish.""",
       "Which finding, if true, would most directly support Ruiz's hypothesis?",
       ["Frogs avoided laying eggs in ponds that contained water taken from fish tanks, even though no fish were present.", "Frogs often lay eggs in ponds that have no fish.",
        "Predatory fish eat frog eggs and tadpoles.", "Frogs can see well in dim light."], "A",
       r"""Avoiding ponds with fish water but no visible fish shows the frogs respond to chemicals, not sight."""),
    rw(II, "Command of Evidence: Textual", 3, r"""Historian Kofi Mensah argues that a set of letters long thought to have been written in 1840 were actually written decades later, by someone imitating the earlier style.""",
       "Which finding, if true, would most directly support Mensah's argument?",
       ["The letters mention a railway line that was not built until 1871.", "The letters are written in elegant handwriting.",
        "Many letters from the 1840s have been lost.", "The letters were kept in a family archive."], "A",
       r"""Mentioning a railway built in 1871 means the letters could not date from 1840. Handwriting and storage do not date them."""),
    rw(II, "Command of Evidence: Textual", 2, r"""A city official claims that the new bus lanes have made bus journeys faster.""",
       "Which finding, if true, would most directly support the official's claim?",
       ["Average bus journey times on routes with the new lanes fell by eight minutes, while times on routes without them stayed the same.",
        "Buses are now painted in brighter colours.", "More people say they like buses.", "The bus lanes were built in the summer."], "A",
       r"""Faster journeys only on routes with the new lanes, compared with routes without them, directly support the claim."""),
]

D["Command of Evidence: Quantitative"] = [
    rw(II, "Command of Evidence: Quantitative", 1, r"""A school recorded students' favourite subjects.

| Subject | Students |
|---|---|
| Art | 64 |
| Maths | 52 |
| Science | 71 |
| History | 38 |

The most popular subject was ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["science.", "art.", "maths.", "history."], "A", r"""Science has the highest number of students: 71."""),
    rw(II, "Command of Evidence: Quantitative", 2, r"""A shop tracked umbrella sales and rainfall.

| Month | Rainfall (mm) | Umbrellas sold |
|---|---|---|
| June | 20 | 15 |
| July | 45 | 32 |
| August | 90 | 70 |

The manager suggests that umbrella sales rise when there is more rain.""",
       "Which choice best describes data from the table that support the manager's suggestion?",
       ["As rainfall increased from June to August, umbrella sales also increased.", "The shop sold 15 umbrellas in June.",
        "August had 90 mm of rain.", "The shop sold umbrellas in all three months."], "A",
       r"""The suggestion is that more rain goes with more sales. Only the statement linking rising rainfall to rising sales across the months supports it."""),
    rw(II, "Command of Evidence: Quantitative", 2, r"""Researchers measured how long four kinds of battery lasted.

| Battery | Hours |
|---|---|
| Brand P | 12 |
| Brand Q | 18 |
| Brand R | 9 |
| Brand S | 15 |

A reviewer claims that Brand Q lasts at least twice as long as Brand R. ______""",
       "Which choice most effectively uses data from the table to complete the text?",
       ["Brand Q lasted 18 hours and Brand R 9 hours, so the claim is correct.", "Brand Q lasted longer than Brand S.",
        "Brand R lasted the shortest time of the four.", "Brand P lasted 12 hours."], "A",
       r"""The claim compares Q and R: 18 hours is exactly twice 9 hours, so Q lasts at least twice as long."""),
    rw(II, "Command of Evidence: Quantitative", 3, r"""A survey asked adults in two age groups how they usually get news.

| Source | Ages 18–29 | Ages 60+ |
|---|---|---|
| Social media | 58% | 14% |
| Television | 16% | 61% |
| News websites | 22% | 18% |
| Print | 4% | 7% |

A researcher concludes that the two age groups differ most in their use of social media and television.""",
       "Which choice best describes data from the table that support the researcher's conclusion?",
       ["The gaps between the groups were largest for social media (44 points) and television (45 points).", "Both groups rarely used print.",
        "The youngest group used news websites more than television.", "Television was the most common source for adults aged 60+."], "A",
       r"""The conclusion is about where the groups differ most. The gaps are 44 points for social media and 45 for television, far larger than for websites (4) or print (3)."""),
    rw(II, "Command of Evidence: Quantitative", 3, r"""A farm tested three fertilisers on wheat.

| Fertiliser | Yield (tonnes per hectare) | Cost per hectare |
|---|---|---|
| None | 5.0 | $0 |
| X | 6.5 | $90 |
| Y | 6.8 | $240 |

The farmer argues that fertiliser X gives better value than fertiliser Y, even though Y produces a higher yield.""",
       "Which choice best describes data from the table that support the farmer's argument?",
       ["Y adds only 0.3 tonnes more than X per hectare but costs $150 more.", "Y produced the highest yield of the three options.",
        "Using no fertiliser cost nothing.", "X increased the yield by 1.5 tonnes compared with no fertiliser."], "A",
       r"""Value compares extra yield with extra cost. Y gives just 0.3 more tonnes than X for $150 more, which supports X as better value."""),
    rw(II, "Command of Evidence: Quantitative", 2, r"""A library counted visitors on different days.

| Day | Visitors |
|---|---|
| Monday | 210 |
| Wednesday | 190 |
| Saturday | 480 |

The librarian claims that the library is busiest at the weekend.""",
       "Which choice best describes data from the table that support the librarian's claim?",
       ["Saturday had more than twice as many visitors as either weekday.", "Monday had 210 visitors.",
        "Wednesday had the fewest visitors.", "The library was open on three days."], "A",
       r"""Saturday's 480 is more than double Monday's 210 and Wednesday's 190, supporting the weekend as busiest."""),
]

D["Inferences"] = [
    rw(II, "Inferences", 1, r"""Most cacti have spines instead of broad leaves. Broad leaves lose a lot of water through evaporation. This suggests that spines help cacti ______""",
       "Which choice most logically completes the text?",
       ["lose less water than they would with broad leaves.", "grow faster than other plants.", "attract more insects.", "survive in cold climates."], "A",
       r"""Broad leaves lose water, and cacti have spines instead, so spines likely help them save water."""),
    rw(II, "Inferences", 2, r"""In a survey, students who used the school's online homework help scored higher on tests than students who did not. However, the students who used it were also more likely to do extra reading at home. Therefore, the survey alone cannot show that ______""",
       "Which choice most logically completes the text?",
       ["the online homework help caused the higher scores.", "students used the online homework help.",
        "some students did extra reading at home.", "test scores varied between students."], "A",
       r"""The users also did more extra reading, which could explain their scores, so the survey cannot show the homework help caused them."""),
    rw(II, "Inferences", 2, r"""Arctic foxes have brown fur in summer and white fur in winter. Their summer coat blends in with rocks and soil, while their winter coat blends in with snow. This suggests that the fox's changing coat ______""",
       "Which choice most logically completes the text?",
       ["helps it stay hidden as its surroundings change through the year.", "makes it warmer in summer.",
        "attracts mates in winter.", "is a sign that the fox is ill."], "A",
       r"""Each coat matches the season's surroundings, so the change keeps the fox camouflaged all year."""),
    rw(II, "Inferences", 3, r"""Archaeologists found tools made of a type of volcanic glass at a site hundreds of kilometres from the nearest source of that glass. There is no evidence that the people at the site ever travelled that far. This suggests that the glass ______""",
       "Which choice most logically completes the text?",
       ["may have reached the site through trade with other groups.", "formed naturally near the site.",
        "was too fragile to be useful for tools.", "was brought by the archaeologists themselves."], "A",
       r"""The glass came from far away, but the people did not travel there, so it most likely arrived through others, such as trade."""),
    rw(II, "Inferences", 3, r"""A company tested a new four-day working week in one of its offices. Employees there completed the same amount of work as before and took fewer sick days. However, the office chosen for the trial was the company's smallest, and its staff had volunteered for the trial. Before introducing the change everywhere, the company should therefore consider that ______""",
       "Which choice most logically completes the text?",
       ["the results may not be the same in larger offices or with staff who did not volunteer.", "the four-day week reduced the amount of work completed.",
        "employees took more sick days during the trial.", "small offices always perform better than large ones."], "A",
       r"""A small office of volunteers may not represent the whole company, so results elsewhere could differ. The other options contradict the text."""),
    rw(II, "Inferences", 2, r"""Some trees in a forest were found to have far fewer insects on their leaves than neighbouring trees of the same species. Researchers discovered that these trees were growing next to wild garlic, whose strong smell is known to repel many insects. This suggests that ______""",
       "Which choice most logically completes the text?",
       ["the garlic's smell may protect nearby trees from insects.", "the trees produce garlic themselves.",
        "insects prefer trees that grow near garlic.", "wild garlic needs trees to grow."], "A",
       r"""The trees with fewer insects grow beside garlic, whose smell repels insects, so the garlic likely protects them."""),
]

D["Boundaries"] = [
    rw(SEC, "Boundaries", 1, r"""The bakery opens at six every ______ its first loaves sell out within an hour.""",
       Q_SEC, ["morning;", "morning,", "morning", "morning, and,"], "A",
       r"""Two complete sentences are joined, so a semicolon is needed. A comma alone is a comma splice."""),
    rw(SEC, "Boundaries", 1, r"""For the camping trip, we packed three ______ a tent, a stove and a first-aid kit.""",
       Q_SEC, ["essentials:", "essentials;", "essentials", "essentials, which"], "A",
       r"""A complete sentence introduces the list, so a colon fits."""),
    rw(SEC, "Boundaries", 2, r"""Dr. Mei ______ a leading expert on volcanoes, will give the opening lecture.""",
       Q_SEC, ["Lin,", "Lin", "Lin;", "Lin:"], "A",
       r""""A leading expert on volcanoes" renames Dr. Mei Lin and closes with a comma, so it must open with one."""),
    rw(SEC, "Boundaries", 2, r"""The river flooded the lower ______ the families who lived there were moved to the school hall.""",
       Q_SEC, ["streets, and", "streets and,", "streets", "streets,"], "A",
       r"""Two complete sentences joined by "and" need a comma before "and"."""),
    rw(SEC, "Boundaries", 3, r"""The museum's most famous ______ a jade carving more than two thousand years old, was found by a farmer ploughing his field.""",
       Q_SEC, ["object,", "object", "object;", "object:"], "A",
       r"""The phrase "a jade carving more than two thousand years old" renames the object and closes with a comma before "was", so it must open with a comma."""),
    rw(SEC, "Boundaries", 3, r"""The team's first prototype failed every ______ the second, built with lighter materials, passed all of them.""",
       Q_SEC, ["test; however,", "test, however,", "test however", "test; however"], "A",
       r""""However" starts a new complete sentence, so it needs a semicolon before it and a comma after it."""),
]

D["Form, Structure, and Sense"] = [
    rw(SEC, "Form, Structure, and Sense", 1, r"""The keys to the classroom ______ on the teacher's desk.""",
       Q_SEC, ["are", "is", "was", "has been"], "A",
       r"""The subject is "keys", which is plural ("to the classroom" describes them), so "are" is needed."""),
    rw(SEC, "Form, Structure, and Sense", 1, r"""Tomorrow, the students ______ their science projects to the judges.""",
       Q_SEC, ["will present", "presented", "have presented", "were presenting"], "A",
       r""""Tomorrow" refers to the future, so "will present" is needed."""),
    rw(SEC, "Form, Structure, and Sense", 2, r"""Neither of the paintings ______ been cleaned since it arrived at the gallery.""",
       Q_SEC, ["has", "have", "are", "were"], "A",
       r"""The subject "Neither" is singular (and "it arrived" confirms it), so "has" is needed."""),
    rw(SEC, "Form, Structure, and Sense", 2, r"""When the guests arrived, the host greeted each of them and offered ______ a drink.""",
       Q_SEC, ["them", "him", "it", "their"], "A",
       r"""The pronoun refers back to "the guests" (each of them), so the plural object pronoun "them" is correct."""),
    rw(SEC, "Form, Structure, and Sense", 3, r"""Covered in moss and half hidden by ferns, ______""",
       Q_SEC, ["the ancient stone wall was easy to miss.", "hikers easily missed the ancient stone wall.",
               "it was easy for hikers to miss the ancient stone wall.", "missing the ancient stone wall was easy."], "A",
       r"""The opening phrase describes something covered in moss, so the wall must follow the comma. The other options make the hikers (or "it") the thing covered in moss."""),
    rw(SEC, "Form, Structure, and Sense", 3, r"""The list of volunteers, which grows longer every year, ______ posted on the community noticeboard each spring.""",
       Q_SEC, ["is", "are", "were", "have been"], "A",
       r"""The subject is "list", which is singular; "of volunteers" and the "which" clause describe it. So the singular "is" is needed."""),
]

D["Transitions"] = [
    rw(EI, "Transitions", 1, r"""The test was difficult. ______, most students passed.""",
       Q_TR, ["Still", "Therefore", "For example", "Similarly"], "A",
       r"""Students passing despite a difficult test is a contrast, so "Still" fits."""),
    rw(EI, "Transitions", 1, r"""Bananas are rich in potassium. ______, they are a popular snack for athletes.""",
       Q_TR, ["For this reason", "However", "In contrast", "Nonetheless"], "A",
       r"""Being rich in potassium is a reason athletes eat bananas, so a cause-and-effect transition fits."""),
    rw(EI, "Transitions", 2, r"""The first part of the novel is set in a busy city. ______, the second part takes place on a quiet, isolated farm.""",
       Q_TR, ["By contrast", "As a result", "For instance", "In addition"], "A",
       r"""A quiet farm is the opposite of a busy city, so a contrast transition fits."""),
    rw(EI, "Transitions", 2, r"""To make bread, first mix the flour, water and yeast. ______, knead the dough for ten minutes.""",
       Q_TR, ["Next", "However", "In conclusion", "For example"], "A",
       r"""The text gives steps in order, so a sequence word, "Next", fits."""),
    rw(EI, "Transitions", 3, r"""Early telephones were expensive and few people owned them. Telephone companies, ______, saw them mainly as a tool for businesses rather than for chatting with friends.""",
       Q_TR, ["accordingly", "nevertheless", "for example", "by contrast"], "A",
       r"""Because few people owned telephones, companies saw them as business tools: a consequence, so "accordingly" fits."""),
    rw(EI, "Transitions", 3, r"""The new drug reduced symptoms in most patients. It did, ______, cause headaches in about one in ten of them.""",
       Q_TR, ["however", "therefore", "similarly", "in other words"], "A",
       r"""Headaches are a drawback that contrasts with the drug's benefits, so "however" fits."""),
]

D["Rhetorical Synthesis"] = [
    rw(EI, "Rhetorical Synthesis", 1, r"""While researching a topic, a student has taken the following notes:
• Mount Everest is the highest mountain on Earth.
• Its summit is 8,849 metres above sea level.
• It lies on the border between Nepal and China.""",
       "The student wants to state the height of Mount Everest. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Mount Everest's summit is 8,849 metres above sea level.", "Mount Everest lies on the border between Nepal and China.",
        "Mount Everest is a famous mountain.", "Many climbers try to reach Mount Everest."], "A",
       r"""Only the sentence giving 8,849 metres states the height."""),
    rw(EI, "Rhetorical Synthesis", 2, r"""While researching a topic, a student has taken the following notes:
• Penicillin was discovered by Alexander Fleming in 1928.
• It was the first widely used antibiotic.
• Mass production began during the Second World War.
• It saved many soldiers from infected wounds.""",
       "The student wants to emphasise penicillin's impact during the Second World War. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Mass-produced during the Second World War, penicillin saved many soldiers from infected wounds.", "Penicillin was discovered by Alexander Fleming in 1928.",
        "Penicillin was the first widely used antibiotic.", "Alexander Fleming was a scientist."], "A",
       r"""Only the sentence linking wartime production to saving soldiers shows its impact during the war."""),
    rw(EI, "Rhetorical Synthesis", 2, r"""While researching a topic, a student has taken the following notes:
• The cheetah is the fastest land animal.
• It can reach about 110 km/h.
• It can keep this speed for only about 20 to 30 seconds.""",
       "The student wants to emphasise a limit on the cheetah's speed. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Although the cheetah can reach about 110 km/h, it can keep that speed for only 20 to 30 seconds.", "The cheetah is the fastest land animal.",
        "The cheetah can reach about 110 km/h.", "Cheetahs are fast animals that live on land."], "A",
       r"""The limit is how briefly it can sprint; only the sentence including the 20–30 second limit emphasises it."""),
    rw(EI, "Rhetorical Synthesis", 3, r"""While researching a topic, a student has taken the following notes:
• Katherine Johnson was a NASA mathematician.
• She calculated flight paths for early space missions.
• In 1962, astronaut John Glenn asked her to check the computer's calculations before his orbital flight.
• She received the Presidential Medal of Freedom in 2015.""",
       "The student wants to show how much astronauts trusted Johnson's work. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Before his 1962 orbital flight, John Glenn asked Katherine Johnson to check the computer's calculations himself.", "Katherine Johnson received the Presidential Medal of Freedom in 2015.",
        "Katherine Johnson was a mathematician at NASA.", "Katherine Johnson calculated flight paths for space missions."], "A",
       r"""Glenn asking her to check the computer's work before his flight shows his trust in her; the others do not involve astronauts' trust."""),
    rw(EI, "Rhetorical Synthesis", 3, r"""While researching a topic, a student has taken the following notes:
• Reykjavík, Iceland, heats most of its buildings using geothermal energy.
• Hot water is piped from underground into homes.
• This has greatly reduced the city's use of fossil fuels.
• Iceland has many active volcanoes.""",
       "The student wants to explain an environmental benefit of Reykjavík's heating system. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["By heating buildings with underground hot water, Reykjavík has greatly reduced its use of fossil fuels.", "Iceland has many active volcanoes.",
        "Reykjavík is the capital of Iceland.", "Hot water is piped from underground into homes in Reykjavík."], "A",
       r"""The environmental benefit is reduced fossil-fuel use; only the sentence connecting the heating system to that reduction explains it."""),
    rw(EI, "Rhetorical Synthesis", 2, r"""While researching a topic, a student has taken the following notes:
• The Nile is about 6,650 km long.
• The Amazon is about 6,400 km long.
• Some researchers argue the Amazon is longer, depending on where its source is measured from.""",
       "The student wants to show that the rivers' ranking is disputed. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["The Nile is usually listed as longer than the Amazon, but some researchers argue the Amazon is longer, depending on where its source is measured from.",
        "The Nile is about 6,650 km long.", "The Amazon is about 6,400 km long.", "The Nile and the Amazon are both very long rivers."], "A",
       r"""Only the sentence setting the usual ranking against the researchers' disagreement shows that it is disputed."""),
]
