r"""Practice Test 4, Reading and Writing: Module 2 harder. Original questions."""
from _sat import rw

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
WIC, TSP, CTC = "Words in Context", "Text Structure and Purpose", "Cross-Text Connections"
CID, COET, COEQ, INF = "Central Ideas and Details", "Command of Evidence: Textual", "Command of Evidence: Quantitative", "Inferences"
BND, FSS, TR, RS = "Boundaries", "Form, Structure, and Sense", "Transitions", "Rhetorical Synthesis"
Q_WIC = "Which choice completes the text with the most logical and precise word or phrase?"
Q_SEC = "Which choice completes the text so that it conforms to the conventions of Standard English?"
Q_TR = "Which choice completes the text with the most logical transition?"
NOTES = "While researching a topic, a student has taken the following notes:"

RW2H = [
    rw(CS, WIC, 2, r"""Critics praised the documentary for its ______ approach: it presented the views of farmers, scientists and government officials without favouring any of them.""",
       Q_WIC, ["even-handed", "partisan", "sensational", "technical"], "A",
       r"""Presenting every group's views without favouring any is fair and balanced: "even-handed". "Partisan" means taking one side."""),
    rw(CS, WIC, 3, r"""The committee's report was deliberately ______, leaving each member free to interpret its recommendations as they wished.""",
       Q_WIC, ["ambiguous", "precise", "lengthy", "confidential"], "A",
       r"""A report that lets each reader interpret it differently is open to more than one meaning: "ambiguous". A "precise" report would allow only one reading."""),
    rw(CS, WIC, 3, r"""Once dismissed as a ______ fad, the electric bicycle has become a fixture of commuting in many cities.""",
       Q_WIC, ["passing", "lasting", "costly", "practical"], "A",
       r"""The sentence contrasts how the bike was once seen with what it has become: a permanent fixture. The contrast needs a word meaning short-lived: "passing"."""),
    rw(CS, WIC, 3, r"""Although the explorer's account of the voyage was later shown to contain errors, historians still consider it ______ on matters such as the weather and the crew's daily routine.""",
       Q_WIC, ["reliable", "fictional", "irrelevant", "incomplete"], "A",
       r""""Although... errors" sets up a contrast: despite mistakes, the account can still be trusted on some matters: "reliable"."""),
    rw(CS, TSP, 2, r"""The following text is from a poem.

The city sleeps, but not the bakers' lights;
Their ovens glow through all the quiet nights,
So that, when dawn comes slowly up the street,
The town will find its bread still warm to eat.""",
       "Which choice best describes the overall structure of the text?",
       ["It describes bakers working through the night and then the result that the town enjoys in the morning.",
        "It contrasts a noisy city with a quiet village.", "It describes a baker's memories of childhood.",
        "It explains how bread is made, step by step."], "A",
       r"""The first two lines show the bakers working while the city sleeps; "So that" leads to the result, warm bread for the town at dawn."""),
    rw(CS, TSP, 3, r"""For centuries, Roman harbour walls puzzled engineers: modern concrete can crumble in seawater within decades, yet Roman structures have lasted two thousand years. A 2017 study traced the difference to the volcanic ash the Romans mixed into their concrete. Seawater seeping into the walls reacts with the ash to grow new minerals that strengthen the concrete over time.""",
       "Which choice best describes the function of the final sentence in the text as a whole?",
       ["It explains the process responsible for the durability described earlier.",
        "It questions whether the 2017 study was accurate.", "It describes how modern concrete is made.",
        "It suggests that Roman walls are now crumbling."], "A",
       r"""The text sets up a puzzle (why Roman concrete lasts), names the ash as the cause, and the final sentence explains how the ash and seawater make it stronger."""),
    rw(CS, TSP, 3, r"""Biologist Tomas Reyes notes that crows can solve puzzles that require several steps in the right order. He cautions, though, against concluding from this that crows reason as humans do. Similar results, he points out, have been produced by animals following simple learned rules, and the experiments so far cannot tell the two explanations apart.""",
       "Which choice best states the main purpose of the text?",
       ["To present a researcher's warning against drawing too strong a conclusion from crows' puzzle-solving",
        "To argue that crows are more intelligent than humans", "To describe the steps of a puzzle that crows solve",
        "To show that crows cannot solve puzzles"], "A",
       r"""Reyes accepts that crows solve the puzzles but warns that the results do not show human-like reasoning, because simpler explanations have not been ruled out."""),
    rw(CS, CTC, 3, r"""Text 1
For decades, many urban planners held that adding lanes to busy roads was the most direct way to reduce traffic congestion. More space for cars, they argued, would mean fewer cars per lane.

Text 2
Economists studying cities in the United States found that when road capacity increased, the total distance driven rose almost in proportion, leaving congestion largely unchanged. New lanes, they concluded, attract new trips, an effect they call "induced demand".""",
       "Based on the texts, how would the economists in Text 2 most likely respond to the planners' view in Text 1?",
       ["By arguing that extra lanes encourage more driving, so congestion does not fall as the planners expect",
        "By agreeing that adding lanes is the best way to reduce congestion", "By claiming that cities should build no new roads at all",
        "By suggesting that congestion is caused mainly by road repairs"], "A",
       r"""The economists found driving rose with capacity, so congestion stayed the same: the opposite of the planners' prediction. They do not say no roads should ever be built."""),
    rw(II, CID, 2, r"""The following text is from a short story.

Mrs. Hale had lived on the street for forty years and had an opinion about all of it. She disliked the new streetlights, which she said kept her awake, and the new neighbours, who she said were far too loud. Yet every afternoon at four o'clock, she set out two cups of tea on her front step, in case anyone should stop to talk.""",
       "Which choice best describes Mrs. Hale as she is presented in the text?",
       ["Although she complains about her surroundings, she hopes for company.", "She plans to move away from the street.",
        "She enjoys the noise made by her neighbours.", "She has no interest in talking to anyone."], "A",
       r"""She criticises the lights and the neighbours, but "Yet" introduces the second cup of tea set out for visitors, which shows she wants company."""),
    rw(II, CID, 3, r"""Glaciers are often described as slow-moving ice, but their movement is far from uniform. Some glaciers periodically "surge", advancing ten to a hundred times faster than usual for months or even years before slowing again. Researchers think that surges begin when meltwater builds up beneath a glacier, lifting it slightly off its bed and reducing friction.""",
       "Which choice best states the main idea of the text?",
       ["Some glaciers periodically move much faster than normal, probably because meltwater reduces friction beneath them.",
        "All glaciers move at the same slow, steady speed.", "Glaciers are melting faster than ever before.",
        "Meltwater causes glaciers to stop moving entirely."], "A",
       r"""The text says glacier movement is not uniform, describes surges, and gives the likely cause, meltwater lowering friction."""),
    rw(II, COET, 3, r"""Psychologist Ines Navarro hypothesises that people give more to charity when they are shown a photograph of a single person in need than when they are shown statistics about many people in need.""",
       "Which finding, if true, would most directly support Navarro's hypothesis?",
       ["Participants shown a photograph of one child donated about twice as much, on average, as participants shown figures about millions of children.",
        "Most participants said that they gave to charity at least once a year.",
        "Participants shown statistics remembered more numbers than participants shown a photograph.",
        "Charities often use both photographs and statistics in their advertising."], "A",
       r"""The hypothesis compares giving after a single photo with giving after statistics. Only the finding showing higher donations after the photo makes that comparison."""),
    rw(II, COET, 3, r"""Some biologists hypothesise that the bright feathers of a certain bird species evolved mainly to help males attract mates.""",
       "Which finding, if true, would most directly weaken this hypothesis?",
       ["Males and females of the species have equally bright feathers, and brightness has no effect on which birds pair up.",
        "Males with the brightest feathers are chosen by females more often than other males.",
        "The species lives in forests with many other brightly coloured birds.",
        "Bright feathers take a lot of energy for birds to grow."], "A",
       r"""If brightness does not affect pairing, and females are just as bright as males, attracting mates is unlikely to be the main reason for the feathers. One choice supports the hypothesis instead."""),
    rw(II, COEQ, 3, r"""Researchers recorded the share of households with solar panels in four regions.

| Region | 2015 | 2022 |
|---|---|---|
| North | 4% | 9% |
| South | 6% | 18% |
| East | 5% | 11% |
| West | 7% | 12% |

The researchers claim that the South saw the largest increase in solar panel use between 2015 and 2022.""",
       "Which choice best describes data from the table that support the researchers' claim?",
       ["The South's share rose by 12 percentage points, while the other regions' shares rose by 5 or 6 points.",
        "The West had the highest share in 2015.", "The North had the lowest share in both years.",
        "The East's share more than doubled."], "A",
       r"""The claim is about the size of the increase. The South rose 12 points; the North and West rose 5 and the East 6."""),
    rw(II, COEQ, 3, r"""An agricultural scientist tested how much fertiliser to add to plots of beans.

| Fertiliser per plot (g) | Average yield (kg) |
|---|---|
| 0 | 4.0 |
| 10 | 5.5 |
| 20 | 6.2 |
| 30 | 6.3 |

The scientist concludes that beyond a certain amount, extra fertiliser adds little to the yield. ______""",
       "Which choice most effectively uses data from the table to support the scientist's conclusion?",
       ["Increasing the fertiliser from 20 g to 30 g raised the yield by only 0.1 kg, compared with 1.5 kg from 0 g to 10 g.",
        "The plots with 30 g of fertiliser had the highest yield.", "Plots with no fertiliser had a yield of 4.0 kg.",
        "The yield with 10 g of fertiliser was 5.5 kg."], "A",
       r"""The conclusion is about shrinking gains. Comparing the large gain from the first 10 g with the tiny gain from the last 10 g shows it."""),
    rw(II, INF, 3, r"""Linguists have found that languages spoken in high mountain regions are more likely than others to include ejective consonants, sounds made with a sharp burst of air from the throat. One proposed explanation is that these sounds take less effort to produce where air pressure is lower. If this explanation is correct, then, all else being equal, ejective consonants should be ______""",
       "Which choice most logically completes the text?",
       ["less common in languages spoken at low altitudes.", "found only in languages spoken in mountains.",
        "harder to produce at high altitudes than at low altitudes.", "unrelated to the altitude at which a language is spoken."], "A",
       r"""If low air pressure makes ejectives easier, they should be rarer where air pressure is higher, at low altitudes. "Only in mountains" goes further than the explanation."""),
    rw(II, INF, 2, r"""A city replaced its parking meters with an app that charged higher prices on its busiest streets. Within a year, the number of drivers circling those streets in search of a space fell by a third, while the city's total income from parking stayed about the same. The results suggest that the higher prices ______""",
       "Which choice most logically completes the text?",
       ["led some drivers to park elsewhere or at other times, freeing up spaces without reducing the city's income.",
        "made the busiest streets completely empty of cars.", "caused the city to lose most of its parking income.",
        "had no effect on where drivers chose to park."], "A",
       r"""Fewer drivers circling means spaces became easier to find, so some drivers changed where or when they parked; income stayed level, so it did not fall."""),
    rw(SEC, BND, 2, r"""The Rosetta Stone, discovered in ______ allowed scholars to decipher Egyptian hieroglyphs for the first time.""",
       Q_SEC, ["1799,", "1799", "1799;", "1799:"], "A",
       r""""Discovered in 1799" is extra information that opens with a comma after "Stone", so it must close with a comma before the verb "allowed"."""),
    rw(SEC, BND, 3, r"""The festival offers something for everyone: concerts for music lovers; workshops for ______ and, for the youngest visitors, a puppet theatre.""",
       Q_SEC, ["artists;", "artists,", "artists:", "artists"], "A",
       r"""The list items contain commas, so they are separated by semicolons, as after "music lovers". A semicolon is needed after "artists" too."""),
    rw(SEC, BND, 3, r"""Physicist Chien-Shiung Wu's 1956 experiment overturned a long-held ______ that nature does not distinguish between left and right.""",
       Q_SEC, ["assumption", "assumption,", "assumption;", "assumption:"], "A",
       r"""The "that" clause states what the assumption was and is essential to the sentence, so no punctuation separates it from "assumption"."""),
    rw(SEC, BND, 3, r"""Some of the world's oldest living trees are bristlecone ______ one of them, in California, is more than 4,800 years old.""",
       Q_SEC, ["pines;", "pines,", "pines", "pines that"], "A",
       r"""Both parts are complete sentences, so a semicolon is needed. A comma alone, or nothing, would join them incorrectly."""),
    rw(SEC, FSS, 3, r"""The number of students taking the exam ______ risen every year since 2015.""",
       Q_SEC, ["has", "have", "are", "were"], "A",
       r"""The subject is "The number", which is singular; "of students" describes it. So the singular "has" is needed."""),
    rw(SEC, FSS, 3, r"""The prize for the best science project was shared by my sister and ______""",
       Q_SEC, ["me.", "I.", "myself.", "mine."], "A",
       r"""After the preposition "by", the object pronoun is needed. Removing "my sister and" gives "shared by me", so "me" is correct."""),
    rw(SEC, FSS, 2, r"""Of the two proposals, the council chose the ______ expensive one.""",
       Q_SEC, ["less", "least", "lesser", "lessest"], "A",
       r"""When comparing exactly two things, the comparative "less" is used; "least" is for three or more."""),
    rw(EI, TR, 3, r"""Many early critics dismissed photography as a mechanical process with no claim to be art. ______, by the early twentieth century, photographs were being shown in major galleries alongside paintings.""",
       Q_TR, ["Nevertheless", "Accordingly", "For instance", "Likewise"], "A",
       r"""Galleries showing photographs goes against the critics' dismissal, so a contrast transition, "Nevertheless", fits."""),
    rw(EI, TR, 3, r"""The drug lowered blood pressure in nearly every patient in the trial. ______, a small number of patients experienced dizziness severe enough that they stopped taking it.""",
       Q_TR, ["That said", "Therefore", "In other words", "For example"], "A",
       r"""The second sentence adds a drawback that qualifies the success described first, so "That said" fits. The dizziness is not a restatement or an example of lower blood pressure."""),
    rw(EI, RS, 2, NOTES + r"""
• The okapi lives in the rainforests of the Democratic Republic of the Congo.
• It has striped legs that resemble a zebra's.
• Its closest living relative is the giraffe.
• Scientists outside Africa first described it in 1901.""",
       "The student wants to emphasise a surprising fact about the okapi's relatives. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Although its striped legs resemble a zebra's, the okapi's closest living relative is the giraffe.",
        "The okapi lives in the rainforests of the Democratic Republic of the Congo.",
        "Scientists outside Africa first described the okapi in 1901.", "The okapi has striped legs."], "A",
       r"""The surprise is the contrast between zebra-like stripes and its true relative, the giraffe. Only one choice makes that contrast."""),
    rw(EI, RS, 3, NOTES + r"""
• A 2010 study of 300 adults linked drinking coffee to a lower risk of liver disease.
• A 2018 study of 9,000 adults found the same link.
• Both were observational studies, not experiments.
• Observational studies can show links but cannot show that one thing causes another.""",
       "The student wants to present the studies' findings while acknowledging a limitation. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Two studies, one of 9,000 adults, linked coffee to a lower risk of liver disease, though as observational studies they cannot show that coffee causes the lower risk.",
        "Drinking coffee prevents liver disease, according to two studies.", "A 2018 study included 9,000 adults.",
        "Observational studies are different from experiments."], "A",
       r"""The goal has two parts: the finding and its limitation. Only one choice gives both; another overstates the finding as proof that coffee prevents disease."""),
]
