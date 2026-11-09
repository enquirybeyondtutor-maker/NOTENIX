r"""Practice Test 1, Reading and Writing: Module 1 (mixed) and Module 2 easier. Original questions."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
WIC, TSP, CTC = "Words in Context", "Text Structure and Purpose", "Cross-Text Connections"
CID, COET, COEQ, INF = "Central Ideas and Details", "Command of Evidence: Textual", "Command of Evidence: Quantitative", "Inferences"
BND, FSS, TR, RS = "Boundaries", "Form, Structure, and Sense", "Transitions", "Rhetorical Synthesis"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"

RW1 = [
    rw(CS, WIC, 1,
       r"""The chef's new menu was deliberately ______: instead of the dozens of dishes the restaurant once offered, it listed only six, each made with ingredients from nearby farms.""",
       Q_WIC, ["extensive", "concise", "expensive", "traditional"], "B",
       r"""The colon explains the blank: the menu went from dozens of dishes to six. A short, focused menu is "concise"."""),
    rw(CS, WIC, 1,
       r"""Although the bridge looked fragile, engineers found it remarkably ______: it had survived two major floods and decades of heavy traffic with only minor repairs.""",
       Q_WIC, ["durable", "ornate", "temporary", "crowded"], "A",
       r""""Although" sets up a contrast with "fragile", and the evidence (surviving floods and traffic) shows the bridge lasts. "Durable" means able to withstand wear."""),
    rw(CS, WIC, 2,
       r"""Historians have long ______ the role of women in the early printing trade. Recent research in guild records shows that widows frequently ran print shops and trained apprentices, a contribution earlier accounts barely mention.""",
       Q_WIC, ["exaggerated", "celebrated", "overlooked", "documented"], "C",
       r"""The second sentence says earlier accounts "barely mention" women's contribution, so historians have "overlooked" it. "Celebrated" and "documented" contradict this, and "exaggerated" means the opposite."""),
    rw(CS, WIC, 3,
       r"""The economist's forecast was ______: it predicted modest growth but surrounded that prediction with so many qualifications and alternative scenarios that almost any outcome could be said to fit it.""",
       Q_WIC, ["equivocal", "pessimistic", "erroneous", "unprecedented"], "A",
       r"""A forecast hedged with so many qualifications that almost any outcome fits it is "equivocal" (open to more than one interpretation). Nothing suggests it was gloomy, wrong or unprecedented."""),
    rw(CS, TSP, 1,
       r"""Sea otters often float on their backs and use a flat rock resting on their chests as an anvil, striking shellfish against it until the shells crack. Some otters keep a favourite rock tucked in a fold of skin under their forelegs, carrying it from one meal to the next.""",
       "Which choice best states the main purpose of the text?",
       ["To describe how sea otters use rocks to open their food",
        "To compare sea otters with other tool-using animals",
        "To explain why sea otters float on their backs",
        "To argue that sea otters are the most intelligent marine mammals"], "A",
       r"""Both sentences describe otters using rocks as anvils to crack shellfish, including carrying a favourite rock. No other animals are compared and no argument about intelligence is made."""),
    rw(CS, TSP, 2,
       r"""For years, city planners assumed that adding lanes to a congested road would reduce traffic. Studies of dozens of expansions have found the opposite: within a few years, the new lanes fill with drivers who previously took other routes or travelled at other times. Planners call this effect "induced demand."
""",
       "Which choice best describes the overall structure of the text?",
       ["It presents a common assumption, then describes evidence that contradicts it and names the effect.",
        "It describes a problem, then proposes several possible solutions.",
        "It explains a scientific term, then gives its history.",
        "It compares two cities' approaches to reducing traffic."], "A",
       r"""The text states what planners assumed, gives studies showing "the opposite", and ends by naming the effect ("induced demand")."""),
    rw(CS, TSP, 3,
       r"""In her 1962 memoir, the architect describes her first commission, a small library in a mountain town, in loving detail: the creak of its floorboards, the smell of pine, the way afternoon light fell across the reading tables. Yet she devotes only a single sentence to the vast government building that made her famous.""",
       "Which choice best describes the function of the second sentence in the text as a whole?",
       ["It explains why the architect stopped designing libraries.",
        "It provides a contrast that highlights how much more attention the architect gives to her first commission.",
        "It suggests that the government building was poorly designed.",
        "It introduces a criticism of the memoir made by other architects."], "B",
       r""""Yet" signals a contrast: the small library gets loving detail, while her most famous building gets one sentence. The contrast emphasises the attention she gives the library. Nothing is said about quality or critics."""),
    rw(CS, CTC, 2,
       r"""Text 1
Many nutritionists recommend eating breakfast every day, arguing that a morning meal improves concentration and helps people avoid overeating later.

Text 2
In a large study, adults who were randomly assigned to skip breakfast did not eat more at lunch or dinner than those who ate breakfast, and their performance on attention tests was the same. The study's authors suggest that the benefits of breakfast may depend more on the individual than on any general rule.""",
       "Based on the texts, how would the authors of the study in Text 2 most likely respond to the nutritionists' recommendation in Text 1?",
       ["They would agree that breakfast improves concentration for most adults.",
        "They would argue that the recommendation may not apply to everyone, since their results did not show the claimed benefits.",
        "They would claim that skipping breakfast is healthier than eating it.",
        "They would suggest that nutritionists should study children instead of adults."], "B",
       r"""The study found no difference in later eating or attention, and its authors say benefits "may depend more on the individual than on any general rule". So they would question a recommendation for everyone, without claiming skipping breakfast is better."""),
    rw(II, CID, 1,
       r"""Before refrigerators, many households kept food cold in an "icebox", a wooden cabinet lined with tin or zinc and packed with a large block of ice. Ice was cut from frozen lakes in winter, stored in insulated ice houses, and delivered door to door through the summer. The trade employed tens of thousands of workers until electric refrigerators became affordable in the 1930s.""",
       "Which choice best states the main idea of the text?",
       ["Electric refrigerators were invented in the 1930s.",
        "Before electric refrigerators, a large industry supplied ice so households could keep food cold.",
        "Ice houses were the most important buildings in early towns.",
        "Wooden cabinets were better at keeping food cold than electric refrigerators."], "B",
       r"""The text describes iceboxes, how ice was harvested, stored and delivered, and how many people the trade employed until refrigerators replaced it. Together that is the ice industry that kept food cold before refrigerators."""),
    rw(II, CID, 2,
       r"""The following text is adapted from a 1913 short story. Maria has just arrived in a city for the first time.

Everything was taller than she had imagined and louder than she had feared. She stood at the corner with her single suitcase, letting the crowd part around her like water around a stone, and for a long moment she could not decide whether she wanted to laugh or to go straight back to the station.""",
       "According to the text, what is true about Maria?",
       ["She is unsure how she feels about the city.",
        "She has visited the city many times before.",
        "She is waiting for a friend to meet her.",
        "She is angry that people are ignoring her."], "A",
       r"""She "could not decide whether she wanted to laugh or to go straight back to the station", which shows mixed, uncertain feelings. The text says this is her first time in a city."""),
    rw(II, COET, 2,
       r"""A historian claims that the spread of public libraries in the late nineteenth century increased reading among working-class adults, not just among the wealthy.""",
       "Which finding, if true, would most directly support the historian's claim?",
       ["Library membership records from the period show that most new members listed factory, dock or domestic work as their occupation.",
        "Many public libraries built in the period had grand entrances and marble floors.",
        "Wealthy families in the period often owned large private libraries.",
        "Some public libraries charged a small fee to borrow new novels."], "A",
       r"""The claim is about working-class adults reading more thanks to public libraries. Records showing that most new members had working-class jobs connect the libraries directly to that group."""),
    rw(II, COET, 3,
       r"""Ecologist Rosa Delgado studied a meadow where a non-native plant had spread. She hypothesised that the plant was reducing the number of native bee species, not because bees avoided it, but because it crowded out the native flowers those bees depend on.""",
       "Which finding, if true, would most strongly support Delgado's hypothesis?",
       ["Native bees were frequently observed visiting the non-native plant's flowers.",
        "Areas of the meadow where the non-native plant was removed and native flowers regrew saw native bee species return.",
        "The non-native plant flowers earlier in spring than most native plants.",
        "Non-native bees in other regions prefer native flowers to non-native ones."], "B",
       r"""The hypothesis links bee decline to the loss of native flowers. If bees return when native flowers regrow after the plant is removed, the loss of those flowers is the likely cause. Bees visiting the plant does not show what drives the decline."""),
    rw(II, COEQ, 1,
       r"""A school surveyed students about how they usually get to school.

| Method | Percentage of students |
|---|---|
| Walk | 35% |
| Bus | 40% |
| Car | 18% |
| Bicycle | 7% |

The survey found that the most common way students get to school is ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["by bus.", "on foot.", "by car.", "by bicycle."], "A",
       r"""The bus has the highest percentage in the table (40%), so it is the most common method."""),
    rw(II, COEQ, 3,
       r"""Researchers measured average daily screen time and average nightly sleep for teenagers in four groups.

| Group | Screen time (hours) | Sleep (hours) |
|---|---|---|
| 1 | 2.1 | 8.4 |
| 2 | 3.8 | 7.9 |
| 3 | 5.2 | 7.1 |
| 4 | 6.9 | 6.6 |

The researchers argue that their data are consistent with the idea that more screen time is associated with less sleep, but they caution that the data alone cannot show that screens cause the loss of sleep.""",
       "Which choice best describes data from the table that support the researchers' argument?",
       ["Group 1 had the least screen time and the most sleep.",
        "As average screen time increased from group to group, average sleep decreased.",
        "Group 4's screen time was more than three times group 1's.",
        "Every group averaged more than six hours of sleep."], "B",
       r"""The argument is about an association: more screen time going with less sleep. Only the statement describing the pattern across all four groups (screen time rising as sleep falls) supports it. The others describe single groups."""),
    rw(II, INF, 2,
       r"""Glass frogs have transparent skin on their undersides. Researchers recently discovered that when a glass frog sleeps, it stores most of its red blood cells in its liver, making its body almost completely see-through. Because predators in the frogs' forest habitat often hunt by sight, this suggests that ______""",
       "Which choice most logically completes the text?",
       ["hiding red blood cells may help glass frogs avoid being seen while they sleep.",
        "glass frogs are more active at night than during the day.",
        "the liver is the largest organ in a glass frog's body.",
        "predators in the forest cannot see the colour red."], "A",
       r"""Predators hunt by sight, and storing blood in the liver makes a sleeping frog nearly invisible. The logical conclusion is that this helps it avoid predators while asleep."""),
    rw(II, INF, 3,
       r"""Medieval manuscripts were often written on parchment made from animal skin, which was expensive. Scribes sometimes scraped old texts off parchment and wrote new ones over them. Using special imaging, researchers can now read the faint traces of the erased writing. Because the erased texts were usually ones that scribes no longer considered valuable, the recovered writing is likely to include ______""",
       "Which choice most logically completes the text?",
       ["works that were widely copied and read at the time.",
        "texts that did not survive anywhere else.",
        "only religious texts.",
        "writing that the scribes themselves had composed."], "B",
       r"""Texts scribes no longer valued were scraped off rather than copied, so they are the ones least likely to survive elsewhere. Widely copied works are the opposite."""),
    rw(SEC, BND, 1,
       r"""The museum's newest exhibit features over two hundred ______ many of which have never been shown to the public.""",
       Q_SEC, ["photographs,", "photographs;", "photographs.", "photographs"], "A",
       r""""Many of which have never been shown" is not a complete sentence, so it cannot follow a semicolon or full stop. It adds detail to "photographs" and is joined with a comma."""),
    rw(SEC, BND, 2,
       r"""The first public demonstration of television took place in London in ______ the inventor, John Logie Baird, showed moving images of a ventriloquist's dummy to a group of scientists.""",
       Q_SEC, ["1926, and", "1926", "1926 and", "1926,"], "A",
       r"""Two complete sentences are being joined, so they need a comma plus a conjunction ("1926, and"). A comma alone is a comma splice; no punctuation is a run-on."""),
    rw(SEC, BND, 2,
       r"""The recipe calls for three ______ flour, sugar and cocoa powder.""",
       Q_SEC, ["ingredients:", "ingredients;", "ingredients,", "ingredients"], "A",
       r"""A colon introduces a list after a complete sentence ("The recipe calls for three ingredients"). A semicolon needs complete sentences on both sides."""),
    rw(SEC, BND, 3,
       r"""Marine biologist Asha ______ who has spent fifteen years tracking whale sharks off the coast of Mozambique, believes the animals return to the same feeding grounds each year.""",
       Q_SEC, ["Nkemelu,", "Nkemelu", "Nkemelu;", "Nkemelu:"], "A",
       r"""The clause "who has spent fifteen years..." is extra information about Nkemelu and ends with a comma before "believes", so it must also start with a comma."""),
    rw(SEC, FSS, 1,
       r"""The team of volunteers ______ every weekend to clear litter from the riverbank.""",
       Q_SEC, ["meet", "meets", "are meeting", "have met"], "B",
       r"""The subject is "team", a singular noun ("of volunteers" describes it), so it takes the singular verb "meets"."""),
    rw(SEC, FSS, 2,
       r"""By the time the rescue boat arrived, the stranded hikers ______ on the small island for nearly two days.""",
       Q_SEC, ["wait", "will wait", "had been waiting", "are waiting"], "C",
       r"""The waiting happened before another past event (the boat arriving), so the past perfect continuous "had been waiting" is needed."""),
    rw(SEC, FSS, 3,
       r"""Walking through the market at dawn, ______""",
       Q_SEC,
       ["the smell of fresh bread drew the tourists toward a small bakery.",
        "a small bakery drew the tourists in with the smell of fresh bread.",
        "the tourists were drawn toward a small bakery by the smell of fresh bread.",
        "fresh bread was smelled by the tourists near a small bakery."], "C",
       r""""Walking through the market at dawn" must describe whoever is walking, so the tourists must come right after the comma. In the other options the smell, the bakery or the bread would be doing the walking."""),
    rw(EI, TR, 1,
       r"""The first part of the hike follows a wide, gently sloping path. ______, the final kilometre is steep and rocky, and hikers often need to use their hands.""",
       Q_TR, ["By contrast", "Similarly", "For instance", "Therefore"], "A",
       r"""The final kilometre (steep, rocky) is the opposite of the first part (wide, gentle), so a contrast transition fits."""),
    rw(EI, TR, 2,
       r"""Honey found in ancient Egyptian tombs has been tasted by archaeologists and found to be perfectly edible. Honey's low moisture and natural acidity make it hostile to bacteria. ______, it can last for thousands of years if sealed properly.""",
       Q_TR, ["Nevertheless", "As a result", "In other words", "Meanwhile"], "B",
       r"""Honey being hostile to bacteria is the reason it can last so long, so the third sentence is a result of the second."""),
    rw(EI, RS, 2,
       r"""While researching a topic, a student has taken the following notes:
• The Atacama Desert in Chile is one of the driest places on Earth.
• Some weather stations there have never recorded rain.
• Its clear, dry skies make it ideal for astronomy.
• Several of the world's largest telescopes are built there.""",
       "The student wants to explain why the Atacama Desert attracts astronomers. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["The Atacama Desert in Chile is one of the driest places on Earth.",
        "Because its skies are so clear and dry, the Atacama Desert is home to several of the world's largest telescopes.",
        "Some weather stations in the Atacama Desert have never recorded rain.",
        "Chile is home to the Atacama Desert, where it rarely rains."], "B",
       r"""The goal is to explain the attraction for astronomers. Only the sentence linking clear, dry skies to the telescopes built there does that."""),
    rw(EI, RS, 3,
       r"""While researching a topic, a student has taken the following notes:
• Bioluminescence is light produced by living organisms.
• Fireflies use it to attract mates.
• The anglerfish uses a glowing lure to attract prey.
• Some squid use it to match light from above and hide their shadows from predators.""",
       "The student wants to emphasise that organisms use bioluminescence for different purposes. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Bioluminescence, light produced by living organisms, is found in fireflies and anglerfish.",
        "Organisms use bioluminescence in different ways: fireflies to attract mates, anglerfish to lure prey and some squid to hide from predators.",
        "The anglerfish has a glowing lure that it uses to attract prey.",
        "Some squid use bioluminescence to hide their shadows."], "B",
       r"""The goal is several different purposes. Only the sentence naming three uses (attracting mates, luring prey, hiding) shows that variety."""),
]

RW2E = [
    rw(CS, WIC, 1,
       r"""The library's new reading room is so ______ that visitors often whisper even when no one else is there.""",
       Q_WIC, ["noisy", "quiet", "colourful", "crowded"], "B",
       r"""Visitors whisper even when alone, which suggests the room is very "quiet"."""),
    rw(CS, WIC, 1,
       r"""The young pianist practised for hours every day, and her ______ paid off when she won the national competition.""",
       Q_WIC, ["dedication", "boredom", "confusion", "reluctance"], "A",
       r"""Practising for hours every day shows commitment, or "dedication", which "paid off" with the win."""),
    rw(CS, WIC, 1,
       r"""The instructions were so ______ that even first-time users could assemble the desk in under twenty minutes.""",
       Q_WIC, ["complicated", "clear", "short-lived", "unusual"], "B",
       r"""First-time users assembling the desk quickly shows the instructions were easy to follow: "clear"."""),
    rw(CS, WIC, 2,
       r"""The scientist was careful not to ______ her results; she reported only what the experiment had shown, even though she had hoped for a more dramatic finding.""",
       Q_WIC, ["overstate", "publish", "repeat", "understand"], "A",
       r"""She reported only what the experiment showed despite hoping for something more dramatic, so she avoided making the results sound bigger than they were: she did not "overstate" them."""),
    rw(CS, TSP, 1,
       r"""Every spring, volunteers in the village carry hundreds of toads across a busy road in buckets. The toads are migrating to the pond where they were born to lay their eggs, and without help, many would be hit by cars.""",
       "Which choice best states the main purpose of the text?",
       ["To describe a local effort to help toads reach their breeding pond safely",
        "To argue that the road should be closed every spring",
        "To explain how toads find the pond where they were born",
        "To compare toads with other migrating animals"], "A",
       r"""The text describes volunteers carrying toads across a road so they can reach their pond without being hit. It makes no argument and compares nothing."""),
    rw(CS, TSP, 2,
       r"""Most people picture deserts as hot. But the largest desert on Earth is Antarctica. A desert is defined by how little precipitation it receives, not by its temperature, and Antarctica's interior receives less than 5 centimetres of snow a year.""",
       "Which choice best describes the function of the third sentence in the text as a whole?",
       ["It explains the definition that makes the surprising claim in the second sentence true.",
        "It describes the wildlife that lives in Antarctica.",
        "It gives a second example of a hot desert.",
        "It questions whether Antarctica should be called a desert."], "A",
       r"""The second sentence makes a surprising claim (Antarctica is the largest desert). The third explains why: deserts are defined by precipitation, and Antarctica gets very little."""),
    rw(CS, TSP, 2,
       r"""The following text is adapted from a 1908 novel. Anne, a young orphan, has just arrived at a farm.

Anne looked around the kitchen with shining eyes. "Oh, I'm so glad I'm going to stay here," she said, although no one had yet told her that she would. "I've never had a real home before, and this looks exactly like the sort of place I always imagined."
""",
       "Which choice best describes the overall structure of the text?",
       ["A character reacts with joy to a new place and explains why it matters to her.",
        "A character argues with another character about where she will live.",
        "A narrator describes a farm in detail and then explains its history.",
        "A character remembers a home she lived in long ago."], "A",
       r"""Anne looks around "with shining eyes", says she is glad to stay, and explains she has never had a real home, so the passage shows her joy and the reason for it."""),
    rw(CS, CTC, 2,
       r"""Text 1
Some teachers argue that students learn best when classrooms are silent, because noise makes it harder to concentrate.

Text 2
A study of primary school pupils found that low background noise, like quiet chatter, did not reduce test scores, while loud noise, such as traffic, did. The researchers concluded that it is the volume of noise, rather than any noise at all, that matters.""",
       "Based on the texts, how would the researchers in Text 2 most likely respond to the teachers in Text 1?",
       ["By agreeing that any noise at all harms learning",
        "By suggesting that only loud noise, not all noise, makes concentration harder",
        "By arguing that classrooms should be as loud as possible",
        "By claiming that noise has no effect on learning"], "B",
       r"""The study found quiet noise did not lower scores but loud noise did, so the researchers would qualify the teachers' view: only loud noise is the problem."""),
    rw(II, CID, 1,
       r"""The Great Barrier Reef, off the coast of Australia, is the largest coral reef system in the world. It stretches for more than 2,300 kilometres and is home to thousands of species of fish, coral and other animals. It is so large that it can be seen from space.""",
       "Which choice best states the main idea of the text?",
       ["The Great Barrier Reef is enormous and full of life.",
        "Coral reefs are found only in Australia.",
        "Most fish species live on the Great Barrier Reef.",
        "Scientists use space photographs to study coral reefs."], "A",
       r"""Each detail (largest reef system, over 2,300 km, thousands of species, visible from space) shows how large and full of life the reef is."""),
    rw(II, CID, 2,
       r"""Some apartment buildings now grow vegetables on their roofs. The gardens give residents fresh food and shade the roof, which keeps the floors below cooler in summer. They also absorb rainwater that would otherwise rush into city drains.""",
       "According to the text, which is one benefit of rooftop gardens?",
       ["They help keep buildings cooler in summer.",
        "They make apartments cheaper to rent.",
        "They replace the need for city drains.",
        "They are easier to look after than ground gardens."], "A",
       r"""The text says the gardens shade the roof, "which keeps the floors below cooler in summer". The other benefits are not stated."""),
    rw(II, COET, 1,
       r"""A student claims that the town's new bike lanes have made cycling more popular.""",
       "Which finding, if true, would most directly support the student's claim?",
       ["The number of cyclists counted on the town's main roads doubled in the year after the bike lanes opened.",
        "The bike lanes were painted green.",
        "Bicycles have become more expensive in recent years.",
        "Some drivers complained about the new bike lanes."], "A",
       r"""The claim is that cycling became more popular after the lanes. A doubling in cyclists after the lanes opened directly supports it."""),
    rw(II, COET, 2,
       r"""A researcher argues that dogs can tell whether a person is smiling or frowning from a photograph.""",
       "Which finding, if true, would most directly support the researcher's argument?",
       ["Dogs trained to choose photos of smiling faces kept choosing smiling faces when shown photos of people they had never seen.",
        "Dogs spend more time looking at people than at other dogs.",
        "Many dog owners believe their dogs understand their moods.",
        "Dogs can recognise their owners' voices."], "A",
       r"""Picking smiling faces of unfamiliar people shows dogs are telling expressions apart from photos alone, which is the argument. Owners' beliefs and voices are not evidence about photographs."""),
    rw(II, COEQ, 1,
       r"""A bakery recorded how many loaves of each bread it sold in one week.

| Bread | Loaves sold |
|---|---|
| White | 420 |
| Wholemeal | 310 |
| Sourdough | 515 |
| Rye | 145 |

According to the table, the bakery sold the most loaves of ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["sourdough.", "white bread.", "wholemeal.", "rye."], "A",
       r"""Sourdough has the highest number in the table: 515 loaves."""),
    rw(II, COEQ, 2,
       r"""A park recorded the number of visitors each season.

| Season | Visitors |
|---|---|
| Spring | 18,000 |
| Summer | 42,000 |
| Autumn | 21,000 |
| Winter | 6,000 |

The park manager claims that summer is by far the park's busiest season.""",
       "Which choice best describes data from the table that support the manager's claim?",
       ["Summer had about twice as many visitors as any other season.",
        "Winter had the fewest visitors.",
        "Spring and autumn had similar numbers of visitors.",
        "The park had 87,000 visitors in total."], "A",
       r"""Summer's 42,000 is about twice autumn's 21,000, the next highest, which shows summer is "by far" the busiest."""),
    rw(II, INF, 1,
       r"""Penguins cannot fly, but they are excellent swimmers. Their wings have evolved into stiff flippers, and their bodies are shaped like torpedoes. These features suggest that penguins' bodies are suited to ______""",
       "Which choice most logically completes the text?",
       ["moving quickly through water.", "flying long distances.", "climbing trees.", "living in hot deserts."], "A",
       r"""Flippers and a torpedo shape are features for swimming, so the bodies suit moving through water. The text says penguins cannot fly."""),
    rw(II, INF, 2,
       r"""A town replaced its old orange streetlights with bright white LED lights. Afterwards, residents noticed that the night sky looked less starry, and astronomers recorded that faint stars had become harder to see. This suggests that ______""",
       "Which choice most logically completes the text?",
       ["the new lights increased the amount of light in the night sky.",
        "the stars had moved further from Earth.",
        "LED lights use more electricity than orange lights.",
        "residents preferred the old streetlights."], "A",
       r"""After brighter lights were installed, faint stars became harder to see, which suggests the lights brightened the sky. The text says nothing about electricity use or residents' preferences."""),
    rw(SEC, BND, 1,
       r"""Our school's chess club meets every ______ new members are always welcome.""",
       Q_SEC, ["Tuesday,", "Tuesday", "Tuesday;", "Tuesday, and,"], "C",
       r"""Two complete sentences are joined, so a semicolon is needed. A comma alone is a comma splice, and no punctuation is a run-on."""),
    rw(SEC, BND, 1,
       r"""Before the storm arrived, the farmers moved their ______ into the barn.""",
       Q_SEC, ["sheep", "sheep,", "sheep;", "sheep:"], "A",
       r""""The farmers moved their sheep into the barn" is one clause with nothing to separate, so no punctuation is needed."""),
    rw(SEC, BND, 2,
       r"""The author's first ______ a mystery set in a lighthouse, was rejected by six publishers before it became a bestseller.""",
       Q_SEC, ["novel,", "novel", "novel;", "novel:"], "A",
       r""""A mystery set in a lighthouse" renames "novel" and is closed by a comma after "lighthouse", so it must open with a comma too."""),
    rw(SEC, BND, 2,
       r"""The volcano's last eruption, in ______ covered nearby villages in ash.""",
       Q_SEC, ["1902,", "1902", "1902;", "1902:"], "A",
       r""""In 1902" is extra information set off by commas; the comma after "eruption" opens it, so a comma must close it."""),
    rw(SEC, FSS, 1,
       r"""Each of the students ______ a short presentation at the end of the term.""",
       Q_SEC, ["give", "gives", "are giving", "have given"], "B",
       r"""The subject is "Each", which is singular, so the verb is "gives"."""),
    rw(SEC, FSS, 1,
       r"""Last summer, my family ______ a week camping in the mountains.""",
       Q_SEC, ["spends", "spend", "spent", "will spend"], "C",
       r""""Last summer" is in the past, so the past tense "spent" is needed."""),
    rw(SEC, FSS, 2,
       r"""The orchestra tuned ______ instruments before the conductor walked onto the stage.""",
       Q_SEC, ["its", "it's", "their's", "they're"], "A",
       r"""The instruments belong to "the orchestra", treated here as a single group, so the possessive "its" is used. "It's" means "it is"."""),
    rw(EI, TR, 1,
       r"""The museum is closed on Mondays. ______, it stays open late on Thursdays.""",
       Q_TR, ["However", "For example", "As a result", "Similarly"], "A",
       r"""Being closed one day and open late another are contrasting facts about the opening hours, so "However" fits."""),
    rw(EI, TR, 2,
       r"""Cacti store water in their thick stems. ______, they can survive long periods without rain.""",
       Q_TR, ["As a result", "In contrast", "For instance", "Nonetheless"], "A",
       r"""Storing water is the reason cacti survive without rain, so the second sentence is a result."""),
    rw(EI, RS, 1,
       r"""While researching a topic, a student has taken the following notes:
• The Eiffel Tower is in Paris, France.
• It was completed in 1889.
• It is about 330 metres tall.""",
       "The student wants to state when the Eiffel Tower was completed. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["The Eiffel Tower, in Paris, was completed in 1889.",
        "The Eiffel Tower is about 330 metres tall.",
        "The Eiffel Tower is in Paris, France.",
        "Paris is home to a tall tower."], "A",
       r"""Only the sentence giving the year, 1889, states when the tower was completed."""),
    rw(EI, RS, 2,
       r"""While researching a topic, a student has taken the following notes:
• Hummingbirds can hover in place.
• They beat their wings up to 80 times per second.
• They feed on flower nectar.
• The bee hummingbird is the smallest bird in the world.""",
       "The student wants to explain how hummingbirds are able to hover. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Hummingbirds can hover in place by beating their wings up to 80 times per second.",
        "The bee hummingbird is the smallest bird in the world.",
        "Hummingbirds feed on flower nectar.",
        "There are many kinds of hummingbirds, including the bee hummingbird."], "A",
       r"""Only the sentence linking hovering to very fast wingbeats explains how they do it."""),
]
