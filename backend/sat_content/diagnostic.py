r"""Notenix SAT free diagnostic: 14 Reading & Writing + 12 Math, mixed difficulty, every domain.
Run: python diagnostic.py   (writes diagnostic.json)"""
from fractions import Fraction as F
import math
from _sat import rw, mq, spr, module, save_form

II, CS, EI, SEC = "Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"
ALG, ADV, PSDA, GEO = "Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"

RW = [
    # Craft and Structure
    rw(CS, "Words in Context", 1,
       r"""The town council's decision to close the library on Sundays was met with ______ opposition: within a week, more than two thousand residents had signed a petition asking the council to reconsider.""",
       "Which choice completes the text with the most logical and precise word or phrase?",
       ["negligible", "widespread", "hesitant", "private"], "B",
       r"""The second half of the sentence describes thousands of residents signing a petition, so the opposition was broad: "widespread". "Negligible" and "hesitant" contradict the evidence, and a public petition is not "private"."""),
    rw(CS, "Words in Context", 2,
       r"""Early reviewers dismissed the novelist's first book as slight, but later critics have come to regard its spare, understated style as ______: a deliberate choice that gives its quiet scenes unusual emotional force.""",
       "Which choice completes the text with the most logical and precise word or phrase?",
       ["a weakness", "an accident", "a strength", "a distraction"], "C",
       r"""The colon explains the blank: the style is "a deliberate choice that gives its quiet scenes unusual emotional force", which is praise. So later critics see the style as "a strength", in contrast with the early reviewers."""),
    rw(CS, "Text Structure and Purpose", 2,
       r"""Honeybees communicate the location of food through a "waggle dance." For decades, researchers assumed the dance was entirely instinctive. A 2023 study, however, found that young bees who never watched experienced dancers performed noticeably less precise dances, suggesting that bees refine the behaviour by observing others.""",
       "Which choice best describes the function of the third sentence in the overall structure of the text?",
       ["It presents evidence that challenges a long-held assumption described earlier in the text.",
        "It explains why researchers were first interested in the waggle dance.",
        "It describes a method that later studies have shown to be unreliable.",
        "It summarises the main argument of the researchers mentioned in the second sentence."], "A",
       r"""The second sentence gives the old assumption (the dance is entirely instinctive). The study, introduced with "however", shows learning plays a part, so it challenges that assumption."""),
    rw(CS, "Cross-Text Connections", 3,
       r"""Text 1
Some economists argue that a four-day working week raises productivity: rested employees, they say, accomplish as much in four days as they previously did in five, so output stays level while wellbeing improves.

Text 2
Trials of the four-day week have produced encouraging results, but most took place in office jobs where output is hard to measure. In settings such as hospitals or factories, where a shorter week simply means fewer hours of staffing, it is far less clear that the same amount of work would get done.""",
       "Based on the texts, how would the author of Text 2 most likely respond to the economists' claim in Text 1?",
       ["By arguing that the trials described in Text 1 were poorly designed and their results should be ignored",
        "By suggesting that the claim may hold for some kinds of work but has not been shown to apply to all jobs",
        "By agreeing that productivity rises in every workplace that adopts a four-day week",
        "By claiming that employee wellbeing is more important than productivity"], "B",
       r"""Text 2 calls the results "encouraging" but notes they come mostly from office jobs and that it is "far less clear" for hospitals or factories. So the author accepts the claim may hold in some settings but doubts it applies everywhere."""),
    # Information and Ideas
    rw(II, "Central Ideas and Details", 1,
       r"""Mangrove forests grow along tropical coastlines where few other trees can survive the salty, waterlogged soil. Their tangled roots slow incoming waves, reducing coastal erosion, and shelter young fish that later move out to coral reefs. Because of these roles, scientists describe mangroves as a "nursery" for the ocean and a natural barrier for coastal communities.""",
       "Which choice best states the main idea of the text?",
       ["Mangroves are difficult to grow outside the tropics.",
        "Mangroves provide important benefits to both marine life and coastal areas.",
        "Coral reefs depend more on mangroves than on any other habitat.",
        "Coastal erosion is the most serious threat facing tropical coastlines."], "B",
       r"""The text lists two kinds of benefit (slowing waves to reduce erosion, and sheltering young fish) and sums them up as a "nursery" for the ocean and a "natural barrier" for communities. The other choices are either not stated or too narrow."""),
    rw(II, "Command of Evidence: Textual", 2,
       r"""A researcher claims that children who learn a musical instrument develop stronger working memory, the ability to hold and use information over a few seconds.""",
       "Which finding, if true, would most directly support the researcher's claim?",
       ["Children who learn an instrument often say they enjoy their lessons.",
        "Many professional musicians began learning their instrument before age ten.",
        "Children randomly assigned to two years of instrument lessons improved more on working-memory tests than similar children assigned to art lessons.",
        "Adults who play an instrument tend to listen to more music than adults who do not."], "C",
       r"""Only the finding about randomly assigned lessons links instrument learning to working memory, and with random assignment and a comparison group it suggests the lessons caused the improvement. The others say nothing about working memory."""),
    rw(II, "Command of Evidence: Quantitative", 2,
       r"""A team surveyed visitors to four national parks about how they travelled there. In every park, most visitors arrived by car, but the share arriving by public transport varied widely.

Visitors arriving by public transport
Park P: 4%
Park Q: 21%
Park R: 9%
Park S: 2%

The team concluded that parks with direct train links attract more public-transport visitors. Of the four parks, only Park Q has a direct train link.""",
       "Which choice best describes data from the table that support the team's conclusion?",
       ["Park S had the smallest share of visitors arriving by public transport.",
        "Most visitors to every park arrived by car.",
        "Park Q, the only park with a direct train link, had a far higher share of public-transport visitors than any other park.",
        "Parks P and R together had a larger share of public-transport visitors than Park S."], "C",
       r"""The conclusion is about train links. Park Q is the only park with one, and its 21% is far above the others (2% to 9%), which is the data that supports the conclusion."""),
    rw(II, "Inferences", 3,
       r"""In laboratory tests, a new drought-resistant variety of wheat produced yields similar to standard wheat when watered normally, and much higher yields when water was scarce. However, the new variety needs a soil nutrient that is low in many of the dry regions where it would be planted. Therefore, without ______""",
       "Which choice most logically completes the text?",
       ["more laboratory testing, the variety's yields under normal watering will remain unknown.",
        "added fertiliser, the variety may not deliver its advantage in the places that need it most.",
        "rainfall, standard wheat will always outperform the new variety.",
        "changes to the variety, it cannot be grown in any region at all."], "B",
       r"""The problem raised is that dry regions lack a nutrient the variety needs. So unless the nutrient is supplied (fertiliser), its drought advantage may not appear where droughts happen. The option about laboratory testing contradicts the text, which already reports yields under normal watering."""),
    # Standard English Conventions
    rw(SEC, "Form, Structure, and Sense", 1,
       r"""Each of the paintings in the museum's new gallery ______ by an artist who was born in the city.""",
       "Which choice completes the text so that it conforms to the conventions of Standard English?",
       ["were created", "was created", "are created", "have been created"], "B",
       r"""The subject is "Each", which is singular ("of the paintings" is a phrase in between). The singular verb "was created" agrees with it."""),
    rw(SEC, "Boundaries", 2,
       r"""The bridge was designed to carry 20,000 vehicles a ______ by its tenth year, it was carrying nearly twice that number.""",
       "Which choice completes the text so that it conforms to the conventions of Standard English?",
       ["day,", "day", "day;", "day, and,"], "C",
       r"""Both parts are complete sentences, so they need a semicolon (or a full stop) between them. A comma alone creates a comma splice, and no punctuation creates a run-on."""),
    rw(SEC, "Boundaries", 3,
       r"""The expedition's leader, a geologist who had spent two decades mapping the ______ insisted on checking every rock sample herself.""",
       "Which choice completes the text so that it conforms to the conventions of Standard English?",
       ["region;", "region:", "region", "region,"], "D",
       r"""The phrase "a geologist who had spent two decades mapping the region" interrupts the sentence, so it must be closed with a comma to match the comma after "leader"."""),
    rw(SEC, "Form, Structure, and Sense", 2,
       r"""After months of negotiation, the two companies finally agreed to share ______ research facilities, a move that analysts expect will cut costs for both.""",
       "Which choice completes the text so that it conforms to the conventions of Standard English?",
       ["it's", "its", "their", "they're"], "C",
       r"""The facilities belong to "the two companies", a plural noun, so the plural possessive "their" is needed. "Its" is singular, and "it's" and "they're" are contractions."""),
    # Expression of Ideas
    rw(EI, "Transitions", 1,
       r"""Electric scooters are cheap to rent and easy to park. ______, many cities have struggled with scooters left blocking pavements and doorways.""",
       "Which choice completes the text with the most logical transition?",
       ["Similarly", "For example", "However", "As a result"], "C",
       r"""The second sentence describes a problem that contrasts with the advantages in the first, so a contrast word, "However", fits."""),
    rw(EI, "Rhetorical Synthesis", 3,
       r"""While researching a topic, a student has taken the following notes:
• The Great Green Wall is a project to restore land across Africa's Sahel region.
• It was launched in 2007 by the African Union.
• Its goal is to restore 100 million hectares of degraded land by 2030.
• By 2020, about 4 million hectares (roughly 4% of the goal) had been restored.""",
       "The student wants to emphasise how much work remains for the project to meet its goal. Which choice most effectively uses relevant information from the notes to accomplish this goal?",
       ["The Great Green Wall, launched by the African Union in 2007, aims to restore land across the Sahel region.",
        "By 2020, the Great Green Wall had restored only about 4% of the 100 million hectares it aims to restore by 2030.",
        "The Great Green Wall is a land-restoration project in Africa's Sahel region.",
        "Launched in 2007, the Great Green Wall has a goal for the year 2030."], "B",
       r"""Only the sentence about 2020 sets what has been done (about 4%) against the goal (100 million hectares by 2030), which shows how much remains."""),
]

M = [
    mq(ALG, "Linear equations in one variable", 1,
       r"If $5x - 8 = 3x + 6$, what is the value of $x$?",
       ["$-7$", "$1$", "$7$", "$14$"], "C",
       r"Subtract $3x$ and add $8$ to both sides: $2x = 14$, so $x = 7$.",
       check=lambda: 5 * 7 - 8 == 3 * 7 + 6),
    mq(ALG, "Linear functions", 1,
       r"A gym charges a joining fee plus a fixed amount per month. The total cost, in dollars, of $m$ months of membership is given by $C(m) = 25m + 40$. What does the number $40$ represent?",
       ["The joining fee", "The cost per month", "The total cost of one month", "The number of months"], "A",
       r"When $m = 0$ (no months yet), $C = 40$: the amount paid before any monthly charge, which is the joining fee. $25$ is the cost per month.",
       check=lambda: 25 * 0 + 40 == 40),
    spr(PSDA, "Percentages", 1,
        r"A jacket originally priced at $\$80$ is on sale for $15\%$ off. What is the sale price, in dollars?",
        ["68", "68.00", "68.0"],
        r"$15\%$ of $80$ is $12$, so the sale price is $80 - 12 = 68$ dollars.",
        check=lambda: 80 * (1 - F(15, 100)) == 68),
    mq(PSDA, "Ratios, rates and units", 2,
       r"A printer prints $45$ pages in $3$ minutes. At this rate, how many minutes will it take to print $270$ pages?",
       ["$12$", "$15$", "$18$", "$20$"], "C",
       r"The rate is $45 \div 3 = 15$ pages per minute, so $270$ pages take $270 \div 15 = 18$ minutes.",
       check=lambda: 270 / (45 / 3) == 18),
    mq(ALG, "Systems of linear equations", 2,
       r"""$2x + y = 11$
$x - y = 1$

What is the solution $(x, y)$ to the system of equations above?""",
       ["$(3, 5)$", "$(4, 3)$", "$(5, 1)$", "$(6, 5)$"], "B",
       r"Add the equations: $3x = 12$, so $x = 4$. Then $y = x - 1 = 3$.",
       check=lambda: 2 * 4 + 3 == 11 and 4 - 3 == 1),
    mq(ADV, "Equivalent expressions", 2,
       r"Which expression is equivalent to $(2x + 3)(x - 4)$?",
       ["$2x^2 - 5x - 12$", "$2x^2 + 5x - 12$", "$2x^2 - 8x - 12$", "$2x^2 - 11x + 12$"], "A",
       r"Expand: $2x \cdot x + 2x(-4) + 3x + 3(-4) = 2x^2 - 8x + 3x - 12 = 2x^2 - 5x - 12$.",
       check=lambda: all((2 * x + 3) * (x - 4) == 2 * x * x - 5 * x - 12 for x in range(-5, 6))),
    spr(GEO, "Right triangles and trigonometry", 2,
        r"A right triangle has legs of length $9$ and $12$. What is the length of its hypotenuse?",
        ["15"],
        r"By Pythagoras, the hypotenuse is $\sqrt{9^2 + 12^2} = \sqrt{81 + 144} = \sqrt{225} = 15$.",
        check=lambda: math.isclose(math.hypot(9, 12), 15)),
    mq(PSDA, "One-variable data", 2,
       r"The data set $3, 7, 7, 10, 13$ has a mean of $8$. If the value $13$ is replaced by $23$, which of the following is true?",
       ["Both the mean and the median increase.", "The mean increases and the median stays the same.",
        "The mean stays the same and the median increases.", "Neither the mean nor the median changes."], "B",
       r"The total rises by $10$, so the mean rises to $10$. The middle value is still $7$, so the median does not change.",
       check=lambda: sum([3, 7, 7, 10, 23]) / 5 == 10 and sorted([3, 7, 7, 10, 23])[2] == 7),
    mq(ADV, "Nonlinear functions", 3,
       r"The function $f$ is defined by $f(x) = 2(x - 3)^2 + 5$. What is the minimum value of $f(x)$?",
       ["$-5$", "$2$", "$3$", "$5$"], "D",
       r"$(x - 3)^2 \ge 0$, so $f(x) \ge 5$, with equality when $x = 3$. The minimum value is $5$ (the $y$-coordinate of the vertex $(3, 5)$).",
       check=lambda: min(2 * (x / 10 - 3) ** 2 + 5 for x in range(-100, 100)) == 5),
    mq(GEO, "Circles", 3,
       r"A circle in the $xy$-plane has equation $x^2 + y^2 - 6x + 4y = 12$. What is the radius of the circle?",
       ["$\\sqrt{12}$", "$5$", "$12$", "$25$"], "B",
       r"Complete the square: $(x - 3)^2 - 9 + (y + 2)^2 - 4 = 12$, so $(x - 3)^2 + (y + 2)^2 = 25$. The radius is $\sqrt{25} = 5$.",
       check=lambda: 12 + 9 + 4 == 25),
    spr(ADV, "Nonlinear equations and systems", 3,
        r"What is the positive solution to the equation $x^2 - 2x - 35 = 0$?",
        ["7"],
        r"Factor: $(x - 7)(x + 5) = 0$, so $x = 7$ or $x = -5$. The positive solution is $7$.",
        check=lambda: 7 * 7 - 2 * 7 - 35 == 0 and (-5) ** 2 - 2 * (-5) - 35 == 0),
    mq(PSDA, "Probability", 3,
       r"""A survey asked 200 students whether they walk or take the bus to school.

| | Walk | Bus | Total |
|---|---|---|---|
| Year 10 | 36 | 64 | 100 |
| Year 11 | 54 | 46 | 100 |
| Total | 90 | 110 | 200 |

If a student who walks is chosen at random, what is the probability that the student is in Year 11?""",
       ["$\\dfrac{27}{100}$", "$\\dfrac{9}{20}$", "$\\dfrac{27}{50}$", "$\\dfrac{3}{5}$"], "D",
       r"Only the $90$ walkers count. Of them, $54$ are in Year 11, so the probability is $\frac{54}{90} = \frac{3}{5}$.",
       check=lambda: F(54, 90) == F(3, 5)),
]

save_form("diagnostic", "SAT Diagnostic", "diagnostic", [
    module("rw", "Reading and Writing", "rw", 16, RW),
    module("m", "Math", "math", 18, M),
], summary="A 34-minute check of every SAT skill area: 14 Reading & Writing and 12 Math questions.")
