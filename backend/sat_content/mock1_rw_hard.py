r"""Practice Test 1, Reading and Writing: Module 2 harder. Original questions."""
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
       r"""The committee's report was notably ______: rather than recommending a single course of action, it laid out the strengths and weaknesses of each option and left the final decision to the council.""",
       Q_WIC, ["partisan", "even-handed", "dismissive", "hasty"], "B",
       r"""Setting out strengths and weaknesses of every option without pushing one is balanced, or "even-handed". "Partisan" means taking a side, the opposite."""),
    rw(CS, WIC, 3,
       r"""Critics initially praised the documentary for its candour, but later investigations revealed that several of its most striking scenes had been staged. In retrospect, the film's apparent honesty was largely ______.""",
       Q_WIC, ["illusory", "inadvertent", "redundant", "unassailable"], "A",
       r"""Staged scenes mean the honesty only seemed real, so it was "illusory". "Unassailable" means beyond challenge, which the investigations contradict."""),
    rw(CS, WIC, 3,
       r"""Rather than abandoning traditional techniques, the ceramicist ______ them, adapting centuries-old glazing methods to work with materials that were unavailable to earlier potters.""",
       Q_WIC, ["repudiated", "reinvented", "imitated", "neglected"], "B",
       r"""She did not abandon the techniques but adapted them for new materials, so she "reinvented" them. "Repudiated" and "neglected" mean rejecting or ignoring them, and "imitated" misses the adaptation."""),
    rw(CS, WIC, 3,
       r"""The senator's speech was so ______ that reporters struggled to identify a single concrete proposal among its many appeals to unity, progress and shared values.""",
       Q_WIC, ["incisive", "nebulous", "succinct", "inflammatory"], "B",
       r"""A speech with no concrete proposal, only broad appeals, is vague: "nebulous". "Incisive" and "succinct" suggest sharpness and brevity, the opposite."""),
    rw(CS, TSP, 2,
       r"""The following text is from a 1920 poem. The speaker describes an old house.

The rooms are full of clocks that do not run,
Of chairs that wait for guests who never come;
The windows hold the colour of the sun
But let no warmth inside this patient home.""",
       "Which choice best describes the overall structure of the text?",
       ["It lists details of the house that together suggest stillness and absence.",
        "It describes the house's history from its building to the present.",
        "It contrasts the house's cheerful past with its gloomy present.",
        "It explains why the house's owners left."], "A",
       r"""Stopped clocks, chairs waiting for guests who never come and windows that let in no warmth are a list of details creating a mood of stillness and absence. No history, past or explanation is given."""),
    rw(CS, TSP, 3,
       r"""It is tempting to credit the printing press alone with the spread of literacy in early modern Europe. Yet in several regions, literacy rates rose sharply only decades after printing arrived, once schooling expanded and books became cheap enough for ordinary households. The press, in other words, made widespread literacy possible; it did not by itself make it happen.""",
       "Which choice best states the main purpose of the text?",
       ["To argue that the printing press's role in spreading literacy has been overstated",
        "To show that the printing press slowed the spread of literacy",
        "To describe how early printing presses worked",
        "To explain why books in early modern Europe were expensive"], "A",
       r"""The text calls crediting the press "alone" tempting, then shows literacy rose only when other factors appeared, concluding the press made literacy possible but did not cause it alone. That qualifies the press's role; it never says the press slowed literacy."""),
    rw(CS, TSP, 3,
       r"""Biologists once classified fungi as plants because both are rooted in place and grow from the ground. Genetic studies have since shown that fungi are more closely related to animals than to plants. Like animals, fungi cannot make their own food and must absorb nutrients from other organisms, and their cell walls contain chitin, a substance also found in insect shells.""",
       "Which choice best describes the function of the third sentence in the text as a whole?",
       ["It gives features that fungi share with animals, supporting the finding described in the second sentence.",
        "It explains why biologists first classified fungi as plants.",
        "It challenges the genetic studies mentioned in the second sentence.",
        "It describes how insects use chitin to build their shells."], "A",
       r"""The second sentence says fungi are closer to animals; the third lists shared features (absorbing food, chitin) that back this up. The insect detail is only an example of chitin."""),
    rw(CS, CTC, 3,
       r"""Text 1
The decline of honeybee colonies is often blamed on a single cause, such as a particular pesticide. But beekeepers' records suggest that colonies rarely fail for one reason. Parasites, poor nutrition and pesticide exposure each weaken bees, and colonies collapse when several stresses occur together.

Text 2
In a controlled experiment, researchers exposed colonies to low doses of a common pesticide. Exposed colonies that were also infested with mites suffered heavy losses, while exposed colonies without mites did about as well as unexposed ones.""",
       "Based on the texts, how would the author of Text 1 most likely view the results of the experiment in Text 2?",
       ["As evidence that the pesticide is the single main cause of colony decline",
        "As consistent with the view that colonies collapse when several stresses combine",
        "As proof that mites are harmless to honeybees",
        "As irrelevant, because experiments cannot show what happens to real colonies"], "B",
       r"""In Text 2, the pesticide hurt colonies only when mites were also present: two stresses together caused losses. That matches Text 1's view that collapse comes from combined stresses, not a single cause."""),
    rw(II, CID, 2,
       r"""The following text is adapted from Jane Austen's 1813 novel Pride and Prejudice.

Mr. Bennet was so odd a mixture of quick parts, sarcastic humour, reserve and caprice, that the experience of three-and-twenty years had been insufficient to make his wife understand his character.""",
       "Which choice best describes Mr. Bennet's character as presented in the text?",
       ["He is complicated enough that even his wife has not understood him after many years.",
        "He is honest and straightforward with his family.",
        "He is unhappy because his wife does not respect him.",
        "He has only recently married."], "A",
       r"""His "odd mixture" of traits means twenty-three years have not been enough for his wife to understand him, so he is complicated and hard to read. "Three-and-twenty years" also shows the marriage is long."""),
    rw(II, CID, 3,
       r"""Sociologist Dalia Haddad studied neighbourhood libraries in three cities. She found that libraries offering services beyond lending books, such as job-search help, language classes and spaces for community meetings, had more visitors than libraries that focused on books alone. Haddad argues that libraries are increasingly valued less as storehouses of books than as public spaces where people can gain skills and connect with one another.""",
       "Which choice best states the main idea of the text?",
       ["Libraries that offer community services attract more visitors, suggesting people value libraries as public spaces.",
        "Most people no longer read books from libraries.",
        "Libraries should stop lending books and offer only classes.",
        "Haddad's study included more cities than earlier studies of libraries."], "A",
       r"""The text presents Haddad's finding (more visitors to libraries with extra services) and her argument (libraries valued as public spaces). It never says people stopped reading or that lending should end."""),
    rw(II, COET, 2,
       r"""The following text is from a 1919 short story. The narrator describes his grandmother.

She kept the best garden on the street and baked bread every Saturday, but what people remembered about her was something else. She had a way of listening that made you feel you were the only person in the world who had ever said anything interesting. Visitors who came to call for ten minutes often stayed for two hours, and left looking surprised at the time.""",
       "The narrator claims that the grandmother's way of listening made people feel interesting. Which quotation from the text most effectively illustrates this claim?",
       ["\"Visitors who came to call for ten minutes often stayed for two hours, and left looking surprised at the time.\"",
        "\"She kept the best garden on the street\"",
        "\"baked bread every Saturday\"",
        "\"what people remembered about her was something else\""], "A",
       r"""Visitors staying two hours instead of ten minutes shows the effect of her listening: people kept talking because she made them feel interesting. The garden and the bread are about other things, and "something else" does not say what."""),
    rw(II, COET, 3,
       r"""Linguist Tomás Reyes hypothesises that children learning two languages at once do not become confused between them, as some parents fear, but instead learn early to keep the languages separate, using each with the people who speak it.""",
       "Which finding, if true, would most directly support Reyes's hypothesis?",
       ["Two-year-olds raised with two languages consistently used each language with the parent who spoke it to them.",
        "Children raised with two languages sometimes mix words from both in a single sentence.",
        "Parents who speak two languages often worry about confusing their children.",
        "Children raised with one language learn a second language more slowly as teenagers."], "A",
       r"""The hypothesis is that young bilingual children keep the languages apart, using each with its speakers. Two-year-olds matching each language to the parent who speaks it is exactly that. Mixing words points the other way."""),
    rw(II, COEQ, 2,
       r"""A researcher compared four kinds of light bulb.

| Bulb | Power (watts) | Light (lumens) | Lifespan (hours) |
|---|---|---|---|
| Incandescent | 60 | 800 | 1,000 |
| Halogen | 43 | 750 | 2,000 |
| CFL | 13 | 800 | 8,000 |
| LED | 9 | 800 | 25,000 |

The researcher concludes that the LED bulb is the best choice for a household that wants bright light while using little electricity.""",
       "Which choice best describes data from the table that support the researcher's conclusion?",
       ["The LED bulb gives as much light as the incandescent bulb while using the least power of the four.",
        "The LED bulb lasts 25,000 hours, the longest of the four.",
        "The halogen bulb uses less power than the incandescent bulb.",
        "The CFL bulb gives 800 lumens of light."], "A",
       r"""The conclusion is about bright light and little electricity. The LED gives 800 lumens (as bright as the brightest) using only 9 watts (the least). Lifespan, though impressive, is not part of the conclusion."""),
    rw(II, COEQ, 3,
       r"""Economists tracked average weekly hours worked and average output per hour in one industry.

| Year | Weekly hours | Output per hour (units) |
|---|---|---|
| 2000 | 44 | 20 |
| 2005 | 42 | 23 |
| 2010 | 40 | 26 |
| 2015 | 38 | 30 |

Some managers in the industry worried that shorter working weeks would lead to less total output per worker. The data, however, suggest that this concern may be unfounded, since ______""",
       "Which choice most effectively uses data from the table to complete the statement?",
       ["output per hour rose enough that weekly output per worker increased from 880 units in 2000 to 1,140 units in 2015.",
        "weekly hours fell from 44 in 2000 to 38 in 2015.",
        "output per hour was highest in 2015.",
        "weekly hours fell by the same amount every five years."], "A",
       r"""The worry is about total output per worker. Weekly output is hours times output per hour: 44 × 20 = 880 in 2000 and 38 × 30 = 1,140 in 2015, so total output rose despite shorter weeks. Hours falling alone would support the worry, not answer it."""),
    rw(II, INF, 3,
       r"""When the ancient city of Pompeii was buried by volcanic ash in 79 CE, many everyday objects were preserved, including graffiti scratched into walls. Much of this graffiti consists of jokes, election slogans and messages between friends, written in an informal Latin that differs in spelling and grammar from the polished Latin of surviving literary works. Because most of the Latin that survives from the period was written by educated authors, the Pompeii graffiti is especially valuable to historians because it ______""",
       "Which choice most logically completes the text?",
       ["offers evidence of how ordinary people in the city actually wrote.",
        "shows that most people in Pompeii could not read.",
        "proves that literary Latin was never spoken.",
        "contains the oldest surviving examples of Latin poetry."], "A",
       r"""Surviving Latin mostly comes from educated authors, while the graffiti is everyday, informal writing. So its value lies in showing how ordinary people wrote. It does not show who could read or prove anything about speech."""),
    rw(II, INF, 3,
       r"""Some trees in dry regions shed their leaves during the hottest months rather than in winter. Leaves lose water through tiny pores as they take in carbon dioxide for photosynthesis. Without leaves, a tree loses much less water, but it also cannot photosynthesise. Researchers studying these trees should therefore expect that during the hottest months, the trees ______""",
       "Which choice most logically completes the text?",
       ["grow little, if at all, while conserving water.",
        "photosynthesise more than at any other time of year.",
        "lose more water than trees that keep their leaves.",
        "take in more carbon dioxide than in winter."], "A",
       r"""In the hottest months the trees are leafless, so they lose little water but cannot photosynthesise. With no photosynthesis there is little energy to grow. The other options contradict the text."""),
    rw(SEC, BND, 2,
       r"""The documentary covers three ______ the building of the canal, the epidemic that halted its construction, and the engineer who finally completed it.""",
       Q_SEC, ["topics:", "topics;", "topics", "topics, which are"], "A",
       r"""A complete sentence ("The documentary covers three topics") introduces a list, so a colon is right. A semicolon would need a complete sentence after it."""),
    rw(SEC, BND, 3,
       r"""The novelist rarely gave ______ when she did, she spoke at length about the farmers and miners whose stories had shaped her books.""",
       Q_SEC, ["interviews, but", "interviews but,", "interviews, but,", "interviews but"], "A",
       r"""Two complete sentences joined by "but" need a comma before "but" and nothing after it, since "when she did" belongs to the second clause."""),
    rw(SEC, BND, 3,
       r"""The researchers at the ______ led by astrophysicist Kenji Watanabe, detected the faint signal after months of observations.""",
       Q_SEC, ["observatory,", "observatory", "observatory;", "observatory:"], "A",
       r"""The phrase "led by astrophysicist Kenji Watanabe" is extra information about the researchers, and it is closed by the comma after "Watanabe". So it must open with a comma too. A semicolon or colon would cut the subject off from its verb, "detected"."""),
    rw(SEC, BND, 3,
       r"""Many of the artist's early paintings were lost in a ______ the few that survived now hang in museums on three continents.""",
       Q_SEC, ["fire; however,", "fire, however,", "fire however", "fire; however"], "A",
       r""""However" begins a new complete sentence here, so it needs a semicolon before it (between the two sentences) and a comma after it."""),
    rw(SEC, FSS, 2,
       r"""Neither the coach nor the players ______ expected the team to reach the final.""",
       Q_SEC, ["had", "has", "was", "is"], "A",
       r"""With "neither... nor", the verb agrees with the nearer subject, "players", which is plural. "Had expected" works for a plural subject; "has" and "was" are singular, and "is expected" changes the meaning."""),
    rw(SEC, FSS, 3,
       r"""The collection of letters, which includes correspondence from three generations of the family, ______ donated to the archive last spring.""",
       Q_SEC, ["was", "were", "have been", "are"], "A",
       r"""The subject is "collection", which is singular; "of letters" and the "which" clause only describe it. So the singular "was" is needed."""),
    rw(SEC, FSS, 3,
       r"""Unlike the city's older bridges, whose stone arches required decades to build, ______""",
       Q_SEC,
       ["the new bridge was assembled from prefabricated steel sections in under two years.",
        "engineers assembled the new bridge from prefabricated steel sections in under two years.",
        "prefabricated steel sections allowed the new bridge to be assembled in under two years.",
        "it took less than two years to assemble the new bridge from prefabricated steel sections."], "A",
       r""""Unlike the city's older bridges" compares bridges, so a bridge must follow the comma. Only "the new bridge was assembled..." makes the comparison bridge to bridge."""),
    rw(EI, TR, 2,
       r"""Early weather forecasts relied mainly on observations from a few weather stations. ______, forecasters can draw on data from satellites, radar and thousands of automated sensors.""",
       Q_TR, ["Today", "Similarly", "As a result", "In conclusion"], "A",
       r"""The text contrasts early forecasting with how it works now, so a time transition, "Today", fits. Nothing in the second sentence results from the first."""),
    rw(EI, TR, 3,
       r"""The playwright's early comedies were commercial successes, filling theatres for months. Critics, ______, dismissed them as light entertainment, and it was not until her later, darker plays that she won serious critical attention.""",
       Q_TR, ["however", "therefore", "for example", "likewise"], "A",
       r"""Critics dismissing the plays contrasts with their commercial success, so "however" fits. "Therefore" would wrongly make the dismissal a result of the success."""),
    rw(EI, RS, 3,
       r"""While researching a topic, a student has taken the following notes:
• The Svalbard Global Seed Vault is in Norway, inside a mountain on an Arctic island.
• It stores more than one million seed samples from almost every country.
• Its purpose is to protect crop diversity against disasters, wars and climate change.
• In 2015, researchers in Syria withdrew seeds to replace a seed bank damaged by war.""",
       "The student wants to give an example showing that the vault has fulfilled its purpose. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["In 2015, Syrian researchers withdrew seeds from the Svalbard vault to replace a seed bank damaged by war, just as the vault was designed to allow.",
        "The Svalbard Global Seed Vault stores more than one million seed samples from almost every country.",
        "The Svalbard Global Seed Vault is inside a mountain on an Arctic island in Norway.",
        "The vault's purpose is to protect crop diversity against disasters, wars and climate change."], "A",
       r"""The goal is an example of the vault doing its job. Only the Syrian withdrawal after a war-damaged seed bank shows that happening; the others describe the vault or its purpose without an example."""),
    rw(EI, RS, 3,
       r"""While researching a topic, a student has taken the following notes:
• Rosalind Franklin was a British chemist.
• In 1952, she produced Photo 51, an X-ray image of DNA.
• The image was key evidence for DNA's double-helix structure.
• James Watson and Francis Crick published the double-helix model in 1953 after seeing her image, without her knowledge.""",
       "The student wants to emphasise Franklin's contribution to the discovery of DNA's structure. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["Franklin's 1952 X-ray image, Photo 51, provided key evidence for the double-helix structure that Watson and Crick published in 1953.",
        "Watson and Crick published the double-helix model of DNA in 1953.",
        "Rosalind Franklin was a British chemist who worked with X-rays.",
        "DNA has a double-helix structure, as shown by research in the 1950s."], "A",
       r"""Only the sentence centred on Franklin's image as "key evidence" for the model highlights her contribution. The others leave her out or do not link her to the discovery."""),
]
