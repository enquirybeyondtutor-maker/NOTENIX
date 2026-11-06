"""Year 9: baseline tests (20 questions, 30 minutes) and notes. Bridges KS3 into GCSE."""
from _q import Q, save_test, save_note


def R(passage, topic, stem, options, correct, explanation):
    return Q(topic, f"Read the passage.\n\n{passage}\n\n{stem}", options, correct, explanation)


MATHS = [
    Q("Indices", r"Simplify $x^5 \times x^3$.", [r"$x^{15}$", r"$x^8$", r"$x^2$", r"$2x^8$"], 1, r"Multiplying: add the powers, $5 + 3 = 8$."),
    Q("Indices", r"Simplify $\dfrac{y^9}{y^4}$.", [r"$y^{13}$", r"$y^{36}$", r"$y^5$", r"$y^{2.25}$"], 2, r"Dividing: subtract the powers, $9 - 4 = 5$."),
    Q("Indices", r"Work out $5^0 + 2^{-1}$.", ["0.5", "1.5", "5.5", "$-2$"], 1, r"$5^0 = 1$ and $2^{-1} = \dfrac{1}{2}$, so the total is 1.5."),
    Q("Standard form", "Write 46 000 000 in standard form.", [r"$46 \times 10^6$", r"$4.6 \times 10^7$", r"$4.6 \times 10^6$", r"$0.46 \times 10^8$"], 1, r"The first number must be between 1 and 10: $4.6 \times 10^7$."),
    Q("Standard form", r"Write $3.2 \times 10^{-4}$ as an ordinary number.", ["0.0032", "0.00032", "32 000", "0.000032"], 1, "Move the decimal point 4 places to the left: 0.00032."),
    Q("Expanding", r"Expand and simplify $(x + 3)(x + 5)$.", [r"$x^2 + 8x + 15$", r"$x^2 + 15x + 8$", r"$x^2 + 8x + 8$", r"$2x + 8$"], 0, r"$x^2 + 5x + 3x + 15 = x^2 + 8x + 15$."),
    Q("Factorising", r"Factorise $x^2 + 7x + 12$.", [r"$(x + 3)(x + 4)$", r"$(x + 2)(x + 6)$", r"$(x + 12)(x + 1)$", r"$(x - 3)(x - 4)$"], 0, "Two numbers that multiply to 12 and add to 7: 3 and 4."),
    Q("Equations", r"Solve $\dfrac{2x + 1}{3} = 5$.", ["$x = 2$", "$x = 7$", "$x = 8$", "$x = 14$"], 1, r"Multiply by 3: $2x + 1 = 15$, so $2x = 14$ and $x = 7$."),
    Q("Inequalities", r"Solve $3x - 4 < 11$.", ["$x < 5$", "$x > 5$", r"$x < \dfrac{7}{3}$", "$x < 15$"], 0, r"Add 4: $3x < 15$, divide by 3: $x < 5$."),
    Q("Straight-line graphs", r"What is the gradient of the line $y = 4x - 7$?", ["$-7$", "4", "$-4$", "7"], 1, r"In $y = mx + c$, the gradient is $m = 4$."),
    Q("Straight-line graphs", "A line passes through (1, 3) and (4, 12). What is its gradient?", ["3", "4", r"$\dfrac{1}{3}$", "9"], 0, r"Gradient = change in $y$ ÷ change in $x$ = $9 \div 3 = 3$."),
    Q("Simultaneous equations", r"Solve $x + y = 10$ and $x - y = 4$.", ["$x = 6, y = 4$", "$x = 7, y = 3$", "$x = 5, y = 5$", "$x = 8, y = 2$"], 1, r"Add the equations: $2x = 14$, so $x = 7$ and $y = 3$."),
    Q("Pythagoras", "A right-angled triangle has shorter sides 6 cm and 8 cm. How long is the hypotenuse?", ["10 cm", "12 cm", "14 cm", "48 cm"], 0, r"$6^2 + 8^2 = 36 + 64 = 100$, and $\sqrt{100} = 10$."),
    Q("Pythagoras", "A ladder 13 m long reaches 12 m up a wall. How far is its foot from the wall?", ["1 m", "5 m", "17.7 m", "25 m"], 1, r"$13^2 - 12^2 = 169 - 144 = 25$, and $\sqrt{25} = 5$ m."),
    Q("Volume", r"Find the volume of a cylinder with radius 3 cm and height 10 cm. Use $\pi \approx 3.14$.", ["94.2 cm³", "188.4 cm³", "282.6 cm³", "942 cm³"], 2, r"$V = \pi r^2 h = 3.14 \times 9 \times 10 = 282.6$ cm³."),
    Q("Percentages", "After a 20% increase, a price is £60. What was the original price?", ["£48", "£50", "£72", "£40"], 1, r"£60 is 120% of the original, so original = $60 \div 1.2 = $ £50."),
    Q("Compound interest", "£1000 is invested at 10% compound interest per year. What is it worth after 2 years?", ["£1200", "£1210", "£1100", "£1020"], 1, r"$1000 \times 1.1^2 = 1210$."),
    Q("Probability", "Two fair coins are flipped. What is the probability of two heads?", [r"$\dfrac{1}{2}$", r"$\dfrac{1}{3}$", r"$\dfrac{1}{4}$", r"$\dfrac{3}{4}$"], 2, r"$\dfrac{1}{2} \times \dfrac{1}{2} = \dfrac{1}{4}$."),
    Q("Ratio", "Two numbers are in the ratio 3 : 7 and their difference is 20. What is the larger number?", ["15", "28", "35", "50"], 2, r"The difference is 4 parts = 20, so 1 part = 5. Larger = $7 \times 5 = 35$."),
    Q("Angles", "What is each interior angle of a regular hexagon?", ["60°", "108°", "120°", "135°"], 2, r"Exterior angle = $360 \div 6 = 60$°, so interior = $180 - 60 = 120$°."),
]

SCIENCE = [
    Q("Atomic structure", "Which particles are found in the nucleus of an atom?", ["Electrons only", "Protons and neutrons", "Protons and electrons", "Neutrons and electrons"], 1, "The nucleus holds protons and neutrons; electrons orbit in shells."),
    Q("Atomic structure", "What is the charge on an electron?", ["+1", "0", "$-1$", "+2"], 2, "Protons are +1, neutrons 0, electrons −1."),
    Q("Atomic structure", "An atom has 11 protons. How many electrons does a neutral atom of it have?", ["0", "11", "12", "23"], 1, "Neutral atoms have equal numbers of protons and electrons."),
    Q("Periodic table", "Group 1 metals (e.g. sodium) are stored in oil. Why?", ["They are too heavy", "They react quickly with air and water", "They melt easily", "They are radioactive"], 1, "Alkali metals react vigorously with oxygen and water."),
    Q("Equations", r"Which equation is balanced?", [r"$\text{H}_2 + \text{O}_2 \rightarrow \text{H}_2\text{O}$", r"$2\text{H}_2 + \text{O}_2 \rightarrow 2\text{H}_2\text{O}$", r"$\text{H}_2 + 2\text{O}_2 \rightarrow \text{H}_2\text{O}$", r"$2\text{H} + \text{O} \rightarrow \text{H}_2\text{O}_2$"], 1, "4 hydrogen and 2 oxygen atoms on each side."),
    Q("Reactivity", "Which metal is most reactive?", ["Gold", "Copper", "Iron", "Potassium"], 3, "Potassium is near the top of the reactivity series; gold is at the bottom."),
    Q("Earth and atmosphere", "Which gas makes up about 78% of the air?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Argon"], 1, "Air is about 78% nitrogen and 21% oxygen."),
    Q("Climate", "Why does increasing carbon dioxide cause global warming?", ["It blocks sunlight", "It absorbs heat radiated from the Earth and traps it", "It makes the Sun hotter", "It destroys ozone"], 1, "Greenhouse gases absorb infrared radiation from the Earth's surface."),
    Q("Genetics", "Where is DNA found in a cell?", ["Cell membrane", "Nucleus", "Cytoplasm only", "Cell wall"], 1, "DNA is found in the chromosomes inside the nucleus."),
    Q("Genetics", "How many chromosomes are in a normal human body cell?", ["23", "46", "44", "92"], 1, "Body cells have 46 chromosomes (23 pairs); sex cells have 23."),
    Q("Variation", "Which of these is caused only by genes (inherited)?", ["A scar", "Natural eye colour", "Language spoken", "Hair length"], 1, "Natural eye colour is inherited; the others depend on the environment."),
    Q("Evolution", "What does 'natural selection' mean?", ["Animals choose their food", "Individuals best suited to their environment survive and pass on their genes", "Humans breed animals", "All organisms survive equally"], 1, "Better-adapted individuals are more likely to survive and reproduce."),
    Q("Health", "What is the job of white blood cells?", ["Carry oxygen", "Fight infection", "Help blood clot", "Carry glucose"], 1, "White blood cells defend the body against pathogens."),
    Q("Energy", r"A 2 kW heater is on for 3 hours. How much energy does it transfer in kWh?", ["0.67 kWh", "5 kWh", "6 kWh", "1.5 kWh"], 2, r"Energy = power × time = $2 \times 3 = 6$ kWh."),
    Q("Energy", "A motor is given 500 J and transfers 400 J usefully. What is its efficiency?", ["40%", "80%", "100%", "125%"], 1, r"Efficiency = useful ÷ total = $400 \div 500 = 0.8 = 80\%$."),
    Q("Waves", "Which type of wave is sound?", ["Transverse", "Longitudinal", "Electromagnetic", "It is not a wave"], 1, "Sound vibrations are parallel to the direction the wave travels: longitudinal."),
    Q("Waves", "Which part of the electromagnetic spectrum is used for night-vision cameras?", ["Ultraviolet", "Infrared", "X-rays", "Gamma rays"], 1, "Warm objects give off infrared radiation."),
    Q("Density", "A block has mass 600 g and volume 200 cm³. What is its density?", ["0.33 g/cm³", "3 g/cm³", "400 g/cm³", "120 000 g/cm³"], 1, r"Density = mass ÷ volume = $600 \div 200 = 3$ g/cm³."),
    Q("Forces", "A 1200 kg car accelerates at 2 m/s². What resultant force acts on it?", ["600 N", "1202 N", "2400 N", "24 000 N"], 2, r"$F = m \times a = 1200 \times 2 = 2400$ N."),
    Q("Electricity", "What is the power of a device with current 5 A and potential difference 230 V?", ["46 W", "235 W", "1150 W", "11.5 W"], 2, r"$P = I \times V = 5 \times 230 = 1150$ W."),
]

P9 = ('"They told us the war would be over by Christmas. Christmas came, and then another, and the letters home '
      'grew shorter. My brother had once filled four pages with jokes about army food. His last letter was a '
      'single line: \'Still here. Don\'t worry.\' Mother read it eleven times. I counted."')
ENGLISH = [
    R(P9, "Reading inference", 'What does "the letters home grew shorter" suggest?', ["The brother was busy with jokes", "The war was taking a heavy toll on the brother", "Paper was cheap", "The family moved house"], 1, "Shorter letters suggest exhaustion and that he has less he can or wants to say."),
    R(P9, "Structure", "How does the writer use contrast in the passage?", ["Between four pages of jokes and a single line", "Between summer and winter", "Between two different families", "Between the past and the future tense only"], 0, "The cheerful long letters contrast with the brief last one, showing how he has changed."),
    R(P9, "Language", '"Still here. Don\'t worry." Why is this letter so effective?', ["It is long and detailed", "Its brevity hints at what is left unsaid, which is more worrying", "It is funny", "It explains the battle"], 1, "Telling the family not to worry, in so few words, makes the reader worry more."),
    R(P9, "Reading inference", '"Mother read it eleven times. I counted." What does this reveal?', ["The mother cannot read well", "The family's anxiety and how closely the narrator watches her", "The letter was hard to read", "The narrator was bored"], 1, "Rereading shows desperate worry; counting shows the narrator's own anxiety."),
    R(P9, "Irony", 'Why is "the war would be over by Christmas" ironic?', ["It came true", "The war lasted much longer, so the confident promise was wrong", "Christmas was cancelled", "It was a joke"], 1, "The optimistic prediction is shown to be badly wrong."),
    R(P9, "Narrative voice", "What is the effect of the first-person narrator?", ["It makes the story feel distant", "It makes the family's experience feel personal and close", "It shows the brother's thoughts directly", "It is a news report"], 1, "Seeing events through a family member's eyes makes them intimate."),
    Q("Grammar", "Which sentence contains a relative clause?", ["The book that I borrowed was brilliant.", "I borrowed a book.", "Borrow the book!", "Was the book good?"], 0, "'That I borrowed' adds information about the book."),
    Q("Grammar", "Which sentence uses the subjunctive mood?", ["If I were you, I would apologise.", "If I was going, I'd tell you.", "I am you.", "You were late."], 0, "'If I were' is the subjunctive, used for hypothetical situations."),
    Q("Punctuation", "Which sentence is correctly punctuated?", ["However, the plan failed.", "However the plan, failed.", "However; the plan failed.", "However: the plan failed"], 0, "A comma follows 'However' when it starts a sentence."),
    Q("Vocabulary", 'What does "ambiguous" mean?', ["Very clear", "Having more than one possible meaning", "Angry", "Old-fashioned"], 1, "Ambiguous means open to more than one interpretation."),
    Q("Vocabulary", 'What does "juxtaposition" mean?', ["Placing contrasting things side by side for effect", "Repeating a word", "A type of rhyme", "Exaggeration"], 0, "e.g. placing wealth next to poverty to highlight the difference."),
    Q("Language techniques", "What is a motif?", ["A recurring image or idea in a text", "The first line of a poem", "A type of punctuation", "The narrator's name"], 0, "e.g. repeated images of light and dark."),
    Q("Language techniques", "Which is an example of a rhetorical question?", ["What time is it?", "How can we sit back while this injustice continues?", "Where is the station?", "Did you finish?"], 1, "It is asked for effect, not to get an answer."),
    Q("Poetry", "What is enjambment?", ["A rhyme at the end of each line", "A sentence running over the end of a line into the next", "A pause in the middle of a line", "A poem with 14 lines"], 1, "Enjambment lets a sentence flow across line breaks."),
    Q("Poetry", "What is a caesura?", ["A pause in the middle of a line of poetry", "A rhyming couplet", "The last stanza", "A type of metaphor"], 0, "A caesura is a break mid-line, often shown by punctuation."),
    Q("Context", "Why might knowing when a text was written help you understand it?", ["It never helps", "Attitudes and events of the time shape what the writer says", "It tells you the ending", "It gives you the word count"], 1, "Context explains the values and events behind a text."),
    Q("Writing", "Which sentence best shows a varied, ambitious opening?", ["I went outside.", "Trembling, she reached for the handle.", "It was a day.", "The thing happened."], 1, "Starting with a verb ending -ing (a participle) is varied and vivid."),
    Q("Writing", "In an argument essay, what is a counter-argument?", ["Your main point", "An opposing view that you then respond to", "A list of facts", "The conclusion"], 1, "Acknowledging and rebutting the other side strengthens your argument."),
    Q("Spelling", "Which is spelt correctly?", ["Embarrass", "Embarass", "Embbarass", "Emberrass"], 0, "Double r and double s: embarrass."),
    Q("Shakespeare", "In 'Romeo and Juliet', the two families are...", ["The Montagues and the Capulets", "The Macbeths and the Duncans", "The Bennets and the Darcys", "The Lears and the Gloucesters"], 0, "The feud between the Montagues and Capulets drives the tragedy."),
]

save_test("y9-baseline", "Maths", "Year 9 Maths Baseline", 30, MATHS)
save_test("y9-baseline", "Science", "Year 9 Science Baseline", 30, SCIENCE)
save_test("y9-baseline", "English", "Year 9 English Baseline", 30, ENGLISH)

save_note("y9-maths-algebra", 9, "Maths", "Indices, standard form and algebra", r"""INDEX LAWS
$x^a \times x^b = x^{a+b}$     $x^a \div x^b = x^{a-b}$     $(x^a)^b = x^{ab}$
$x^0 = 1$     $x^{-1} = \dfrac{1}{x}$

STANDARD FORM: $A \times 10^n$ with $1 \le A < 10$
46 000 000 = $4.6 \times 10^7$     0.00032 = $3.2 \times 10^{-4}$

DOUBLE BRACKETS (multiply every term by every term)
$(x + 3)(x + 5) = x^2 + 5x + 3x + 15 = x^2 + 8x + 15$

FACTORISING QUADRATICS
$x^2 + 7x + 12$: find two numbers that multiply to 12 and add to 7 → 3 and 4
$= (x + 3)(x + 4)$

INEQUALITIES
Solve like equations: $3x - 4 < 11$ → $3x < 15$ → $x < 5$
(If you multiply or divide by a negative number, flip the sign.)

SIMULTANEOUS EQUATIONS
$x + y = 10$ and $x - y = 4$: add them → $2x = 14$ → $x = 7$, then $y = 3$""")

save_note("y9-maths-geometry", 9, "Maths", "Graphs, Pythagoras and percentages", r"""STRAIGHT-LINE GRAPHS: $y = mx + c$
$m$ = gradient (steepness), $c$ = where it crosses the $y$-axis.
Gradient from two points = change in $y$ ÷ change in $x$
(1, 3) to (4, 12): $9 \div 3 = 3$

PYTHAGORAS (right-angled triangles only)
$a^2 + b^2 = c^2$, where $c$ is the hypotenuse (longest side, opposite the right angle)
Finding $c$: square, ADD, square root.  6 and 8 → $\sqrt{100} = 10$
Finding a shorter side: square, SUBTRACT, square root.  13 and 12 → $\sqrt{25} = 5$

VOLUME OF A PRISM / CYLINDER
Volume = area of cross-section × length.  Cylinder: $\pi r^2 h$

REVERSE PERCENTAGES
After a 20% increase the price is £60. £60 = 120%, so 100% = $60 \div 1.2 = $ £50

COMPOUND INTEREST
original × (multiplier)$^{\text{years}}$:  $1000 \times 1.1^2 = 1210$""")

save_note("y9-science-chemistry", 9, "Science", "Atomic structure and equations", r"""INSIDE THE ATOM
Nucleus: protons (+1) and neutrons (0). Shells: electrons (−1).
Atomic number = number of protons. Neutral atom: protons = electrons.

THE PERIODIC TABLE
Group 1 (alkali metals): very reactive, react with water to make hydrogen. More reactive going DOWN.
Group 7 (halogens): reactive non-metals. Less reactive going down.
Group 0 (noble gases): unreactive, full outer shells.

BALANCING EQUATIONS
Same number of each atom on both sides; change only the big numbers in front.
$2\text{H}_2 + \text{O}_2 \rightarrow 2\text{H}_2\text{O}$  (4 H and 2 O each side)

REACTIVITY SERIES (most → least)
potassium, sodium, calcium, magnesium, aluminium, (carbon), zinc, iron, copper, silver, gold

THE ATMOSPHERE
78% nitrogen, 21% oxygen, about 1% argon, about 0.04% carbon dioxide.
More $\text{CO}_2$ traps more heat → global warming.""")

save_note("y9-science-bio-physics", 9, "Science", "Genetics, energy and forces", r"""DNA AND GENES
DNA is in the chromosomes inside the nucleus. A gene is a section of DNA that codes for a characteristic.
Body cells: 46 chromosomes (23 pairs). Sex cells: 23.

VARIATION AND EVOLUTION
Inherited (eye colour) vs environmental (scars, language).
Natural selection: the best-adapted individuals survive, reproduce and pass on their genes.

ENERGY
Energy (kWh) = power (kW) × time (h)
Efficiency = useful energy out ÷ total energy in  (500 J in, 400 J useful → 80%)

ELECTRICITY
$P = I \times V$  (power = current × potential difference)

FORCES AND MOTION
$F = m \times a$  (force = mass × acceleration)
Density = mass ÷ volume

WAVES
Sound: longitudinal. Light and all EM waves: transverse.
EM spectrum: radio, microwave, infrared, visible, ultraviolet, X-ray, gamma""")

save_note("y9-english-analysis", 9, "English", "Analysing texts like a GCSE student", r"""WHAT EXAMINERS WANT
Not just WHAT a technique is, but WHY the writer uses it and its EFFECT on the reader.

ADVANCED TERMS
• Juxtaposition: contrasting ideas side by side (four pages of jokes vs one line)
• Irony: the opposite of what's expected ("over by Christmas")
• Motif: a repeated image or idea
• Enjambment: a sentence running over a line break; Caesura: a pause mid-line

CONTEXT
When and why was it written? What did people believe then? Link it to the writer's message.

A STRONG PARAGRAPH (What, How, Why)
What: The writer shows the war slowly breaking the brother.
How: The contrast between "four pages of jokes" and a "single line" ...
Why: ... makes the reader feel the family's growing fear, which reflects how many families experienced the war.

EMBED SHORT QUOTES
Better: the "single line" letter suggests ...  Worse: copying a whole sentence.""")

save_note("y9-english-writing", 9, "English", "Writing with control and range", r"""SENTENCE VARIETY
• Start with a participle: Trembling, she reached for the handle.
• Short sentence for impact. Then a longer one that builds detail and rhythm.
• Relative clauses add detail: The book that I borrowed was brilliant.

PUNCTUATION RANGE
Semicolon; colon: dash - brackets ( ) - used deliberately, not just for decoration.

ARGUMENT WRITING
Introduction with a clear view → points with evidence → counter-argument and rebuttal → strong conclusion.
Use discourse markers: Furthermore, However, Consequently, Ultimately.

DESCRIPTIVE / NARRATIVE WRITING
Zoom in on small details. Use all five senses. Show feelings through actions, not labels.
Plan a structure: hook → build → turning point → resolution.

GRAMMAR FOR GCSE
If I were you (subjunctive for hypotheticals). Fewer (countable) vs less (uncountable).
Who (subject) vs whom (object).""")
print("Year 9 notes written")
