"""Year 8: baseline tests (20 questions, 30 minutes) and notes."""
from _q import Q, save_test, save_note


def R(passage, topic, stem, options, correct, explanation):
    return Q(topic, f"Read the passage.\n\n{passage}\n\n{stem}", options, correct, explanation)


MATHS = [
    Q("Negative numbers", r"Work out $-6 \times 4 + 15$.", ["$-39$", "$-9$", "9", "39"], 1, r"$-6 \times 4 = -24$, then $-24 + 15 = -9$."),
    Q("Fractions", r"Work out $\dfrac{3}{4} \div \dfrac{1}{8}$.", [r"$\dfrac{3}{32}$", "6", r"$\dfrac{1}{6}$", "24"], 1, r"Dividing by $\dfrac{1}{8}$ is multiplying by 8: $\dfrac{3}{4} \times 8 = 6$."),
    Q("Fractions", r"Work out $2\dfrac{1}{3} \times 1\dfrac{1}{2}$.", [r"$2\dfrac{1}{6}$", r"$3\dfrac{1}{2}$", r"$3\dfrac{1}{6}$", "4"], 1, r"$\dfrac{7}{3} \times \dfrac{3}{2} = \dfrac{21}{6} = 3\dfrac{1}{2}$."),
    Q("Percentage change", "A price rises from £40 to £46. What is the percentage increase?", ["6%", "13%", "15%", "46%"], 2, r"Increase £6. $\dfrac{6}{40} = 0.15 = 15\%$."),
    Q("Percentages", "Increase £250 by 12%.", ["£262", "£280", "£300", "£220"], 1, r"12% of 250 = 30, so $250 + 30 = $ £280. (Or $250 \times 1.12$.)"),
    Q("Expanding", "Expand and simplify $5(x + 3) - 2(x - 4)$.", ["$3x + 7$", "$3x + 23$", "$3x - 1$", "$7x + 23$"], 1, r"$5x + 15 - 2x + 8 = 3x + 23$. Careful: $-2 \times -4 = +8$."),
    Q("Factorising", "Factorise fully $12x + 18$.", ["$2(6x + 9)$", "$3(4x + 6)$", "$6(2x + 3)$", "$12(x + 18)$"], 2, "The highest common factor of 12 and 18 is 6: $6(2x + 3)$."),
    Q("Equations", "Solve $7x - 4 = 3x + 20$.", ["$x = 4$", "$x = 6$", "$x = 2.4$", "$x = 16$"], 1, "Subtract $3x$: $4x - 4 = 20$. Add 4: $4x = 24$, so $x = 6$."),
    Q("Equations", "Solve $4(x - 2) = 2x + 6$.", ["$x = 7$", "$x = 4$", "$x = 1$", "$x = 2$"], 0, "$4x - 8 = 2x + 6$, so $2x = 14$ and $x = 7$."),
    Q("Sequences", "Find the $n$th term of 11, 8, 5, 2, ...", ["$3n + 8$", "$-3n + 14$", "$14 - n$", "$11 - 3n$"], 1, "Difference $-3$, so $-3n$ gives $-3, -6, ...$; add 14 to get 11, 8, 5: $14 - 3n$."),
    Q("Ratio", "£84 is shared in the ratio 2 : 5. How much more does the larger share get?", ["£24", "£36", "£60", "£12"], 1, r"7 parts = 84, so 1 part = 12. Shares are 24 and 60; the difference is £36."),
    Q("Proportion", "6 workers build a wall in 10 days. How long would 4 workers take, at the same rate?", ["6.7 days", "12 days", "15 days", "20 days"], 2, r"Total work = $6 \times 10 = 60$ worker-days; $60 \div 4 = 15$ days (inverse proportion)."),
    Q("Angles", "Two parallel lines are crossed by a straight line. One alternate angle is 65°. What is the other?", ["25°", "65°", "115°", "295°"], 1, "Alternate angles (Z-angles) are equal."),
    Q("Angles", "Co-interior angles between parallel lines are $x$ and 110°. Find $x$.", ["70°", "110°", "250°", "20°"], 0, r"Co-interior angles add to 180°: $180 - 110 = 70$°."),
    Q("Polygons", "What is each exterior angle of a regular octagon?", ["30°", "45°", "60°", "135°"], 1, r"Exterior angles add to 360°: $360 \div 8 = 45$°."),
    Q("Circles", r"Find the area of a circle of radius 5 cm. Use $\pi \approx 3.14$.", ["15.7 cm²", "31.4 cm²", "78.5 cm²", "157 cm²"], 2, r"Area $= \pi r^2 = 3.14 \times 25 = 78.5$ cm²."),
    Q("Circles", r"Find the circumference of a circle with diameter 10 cm. Use $\pi \approx 3.14$.", ["15.7 cm", "31.4 cm", "78.5 cm", "314 cm"], 1, r"Circumference $= \pi d = 3.14 \times 10 = 31.4$ cm."),
    Q("Volume", "Find the volume of a cuboid 4 cm by 5 cm by 6 cm.", ["15 cm³", "74 cm³", "120 cm³", "148 cm³"], 2, r"$4 \times 5 \times 6 = 120$ cm³."),
    Q("Probability", "A spinner has P(red) = 0.3 and P(blue) = 0.45. The only other colour is green. Find P(green).", ["0.15", "0.25", "0.35", "0.75"], 1, r"$1 - 0.3 - 0.45 = 0.25$."),
    Q("Averages", "The mean of 5 numbers is 12. When a sixth number is added the mean becomes 13. What is the sixth number?", ["13", "15", "18", "78"], 2, r"Old total 60, new total $6 \times 13 = 78$; the new number is 18."),
]

SCIENCE = [
    Q("Atoms and elements", "What is an element?", ["A mixture of atoms", "A substance made of only one type of atom", "Two atoms bonded together", "A liquid"], 1, "An element contains only one type of atom, e.g. oxygen or iron."),
    Q("Compounds", "Which of these is a compound?", ["Oxygen", "Iron", "Water", "Neon"], 2, r"Water ($\text{H}_2\text{O}$) contains hydrogen and oxygen chemically joined."),
    Q("Formulae", r"How many atoms are in one molecule of $\text{CO}_2$?", ["1", "2", "3", "4"], 2, "One carbon atom and two oxygen atoms: 3 atoms."),
    Q("Periodic table", "Elements in the same group of the periodic table ...", ["have the same mass", "have similar chemical properties", "are all gases", "were discovered at the same time"], 1, "Elements in a group react in similar ways, e.g. the alkali metals."),
    Q("Periodic table", "Where are the metals found on the periodic table?", ["On the right", "On the left and in the middle", "Only at the top", "Only at the bottom"], 1, "Metals are on the left and centre; non-metals are on the right."),
    Q("Chemical reactions", "Magnesium burns in oxygen. What is the product?", ["Magnesium oxygenate", "Magnesium oxide", "Magnesium carbonate", "Oxygen magnesium"], 1, "Magnesium + oxygen → magnesium oxide."),
    Q("Conservation of mass", "In a sealed flask, 10 g of reactants react. What is the mass of the products?", ["Less than 10 g", "10 g", "More than 10 g", "0 g"], 1, "Atoms are rearranged, not created or destroyed, so mass is conserved."),
    Q("Digestion", "Where is most water absorbed back into the body?", ["Stomach", "Small intestine", "Large intestine", "Oesophagus"], 2, "The large intestine absorbs water from undigested food."),
    Q("Digestion", "What do enzymes do in digestion?", ["Make food bigger", "Break large molecules into small ones the body can absorb", "Turn food into water", "Kill all bacteria"], 1, "Enzymes are biological catalysts that break down large food molecules."),
    Q("Respiration", "What is the word equation for aerobic respiration?", ["glucose + oxygen → carbon dioxide + water", "carbon dioxide + water → glucose + oxygen", "glucose → lactic acid", "oxygen + water → glucose"], 0, "Aerobic respiration uses oxygen to release energy from glucose."),
    Q("Respiration", "What is produced by anaerobic respiration in human muscles?", ["Carbon dioxide and water", "Lactic acid", "Alcohol", "Oxygen"], 1, "Without enough oxygen, muscles make lactic acid."),
    Q("Photosynthesis", "Which gas do plants take in for photosynthesis?", ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], 2, "carbon dioxide + water → glucose + oxygen (using light)."),
    Q("Breathing", "Where does gas exchange happen in the lungs?", ["Trachea", "Bronchi", "Alveoli", "Diaphragm"], 2, "Oxygen and carbon dioxide diffuse across the thin walls of the alveoli."),
    Q("Electricity", "What is the unit of resistance?", ["Volt", "Amp", "Ohm", "Watt"], 2, "Resistance is measured in ohms (Ω)."),
    Q("Electricity", "A bulb has a current of 0.5 A and a potential difference of 6 V. What is its resistance?", ["3 Ω", "6.5 Ω", "12 Ω", "0.08 Ω"], 2, r"$R = V \div I = 6 \div 0.5 = 12$ Ω."),
    Q("Magnetism", "What happens when two north poles are brought together?", ["They attract", "They repel", "Nothing", "They swap"], 1, "Like poles repel; opposite poles attract."),
    Q("Pressure", "Why is a sharp knife better at cutting than a blunt one?", ["It is heavier", "The force acts on a smaller area, giving higher pressure", "It has more friction", "It is colder"], 1, "Pressure = force ÷ area; a thin edge means a small area and high pressure."),
    Q("Speed", "A train travels 180 km in 2 hours. What is its average speed?", ["90 km/h", "182 km/h", "360 km/h", "45 km/h"], 0, r"$180 \div 2 = 90$ km/h."),
    Q("Heating", "How is heat mainly transferred through a metal spoon?", ["Convection", "Conduction", "Radiation", "Evaporation"], 1, "In solids, vibrating particles pass energy along: conduction."),
    Q("Working scientifically", "Which of these makes a test fair?", ["Changing several variables at once", "Keeping control variables the same", "Doing it only once", "Using different equipment each time"], 1, "Only change the independent variable; keep everything else the same."),
]

P8 = ('"The storm came in the night. By morning the village had changed: the bridge was gone, the river had '
      'swallowed the lower field, and old Mrs Hale\'s fence lay scattered like matchsticks across the lane. '
      'Nobody spoke much. People simply picked up what they could, and started again."')
ENGLISH = [
    R(P8, "Reading inference", "What is the main mood of the passage?", ["Joyful", "Shocked but determined", "Angry and violent", "Bored"], 1, "The damage is shocking, but people quietly start rebuilding."),
    R(P8, "Language techniques", '"the river had swallowed the lower field" is an example of ...', ["simile", "personification", "alliteration", "onomatopoeia"], 1, "Swallowing is a living action given to the river."),
    R(P8, "Language techniques", 'Why does the writer compare the fence to "matchsticks"?', ["To show it was new", "To show how small and easily broken it now looked", "To show it was on fire", "To show it was expensive"], 1, "Matchsticks are tiny and fragile, showing the storm's power."),
    R(P8, "Structure", "How does the writer use punctuation in the second sentence?", ["A colon introduces a list of the damage", "Speech marks show dialogue", "A question mark shows confusion", "Brackets add a joke"], 0, "The colon introduces the list of changes."),
    R(P8, "Reading inference", '"Nobody spoke much." What does this suggest?', ["People were angry with each other", "People were stunned and focused", "People could not hear", "People were asleep"], 1, "Silence suggests shock and quiet determination."),
    R(P8, "Structure", "Why is the first sentence short?", ["To grab attention and state the key event directly", "Because the writer was lazy", "To introduce dialogue", "To slow the pace"], 0, "A short opening sentence is punchy and sets up the story."),
    Q("Grammar", 'Identify the subordinate clause: "Although she was tired, Priya finished her essay."', ["Priya finished her essay", "Although she was tired", "her essay", "she was"], 1, "It begins with 'although' and cannot stand alone."),
    Q("Grammar", "Which sentence uses the passive voice?", ["The window was broken by the ball.", "The ball broke the window.", "The ball is breaking.", "Break the window!"], 0, "The object (window) comes first and the doer follows 'by'."),
    Q("Punctuation", "Which sentence uses a semicolon correctly?", ["I like tea; and coffee.", "I like tea; my brother prefers coffee.", "I; like tea.", "I like; tea and coffee."], 1, "A semicolon joins two linked main clauses."),
    Q("Punctuation", "Which uses dashes correctly for a dramatic pause?", ["The door opened - and there stood the headteacher.", "The - door opened.", "The door - opened - and.", "- The door opened"], 0, "A dash before the reveal creates suspense."),
    Q("Vocabulary", 'What does "reluctant" mean?', ["Eager", "Unwilling", "Angry", "Late"], 1, "Reluctant means not wanting to do something."),
    Q("Vocabulary", 'Which word is an antonym (opposite) of "generous"?', ["Kind", "Selfish", "Giving", "Friendly"], 1, "Selfish is the opposite of generous."),
    Q("Language techniques", "What is pathetic fallacy?", ["A sad character", "Weather or setting reflecting a character's mood", "A weak argument", "A type of rhyme"], 1, "e.g. rain and grey skies when a character is sad."),
    Q("Language techniques", "Which is an oxymoron?", ["Deafening silence", "Very loud", "Silent night", "Loud noise"], 0, "An oxymoron puts opposite ideas together: deafening + silence."),
    Q("Persuasive writing", "Which is the strongest opening for a persuasive speech about school uniform?", ["Uniform is a thing.", "Imagine walking into school and being judged for your clothes before you even speak.", "I am going to talk about uniform.", "Uniform. Yes."], 1, "It hooks the audience with direct address and an emotional scenario."),
    Q("Writer's purpose", "A travel guide's main purpose is usually to ...", ["entertain with a fictional plot", "inform and advise", "argue against travel", "instruct how to cook"], 1, "Travel guides give information and recommendations."),
    Q("Spelling", "Which is spelt correctly?", ["Accommodation", "Acommodation", "Accomodation", "Acomodation"], 0, "Two c's and two m's: accommodation."),
    Q("Spelling", "Which word is spelt correctly?", ["Beleive", "Recieve", "Receive", "Decieve"], 2, "'i before e except after c': receive."),
    Q("Shakespeare", "What is a theme?", ["The setting of a story", "A big idea a text explores, like love or power", "The main character", "The ending"], 1, "Themes are central ideas, e.g. ambition in Macbeth."),
    Q("Evidence", "What is the best way to support a point about a character?", ["Give your opinion only", "Use a short quotation and explain what it shows", "Retell the whole story", "Describe the cover"], 1, "Quote + explanation shows how you know."),
]

save_test("y8-baseline", "Maths", "Year 8 Maths Baseline", 30, MATHS)
save_test("y8-baseline", "Science", "Year 8 Science Baseline", 30, SCIENCE)
save_test("y8-baseline", "English", "Year 8 English Baseline", 30, ENGLISH)

save_note("y8-maths-algebra", 8, "Maths", "Expanding, factorising and equations", r"""EXPANDING BRACKETS
Multiply everything inside by the term outside.
$5(x + 3) = 5x + 15$     $-2(x - 4) = -2x + 8$  (negative × negative = positive)

FACTORISING (the reverse)
Take out the highest common factor.
$12x + 18 = 6(2x + 3)$     $x^2 + 7x = x(x + 7)$

EQUATIONS WITH x ON BOTH SIDES
Get the x terms on one side first.
$7x - 4 = 3x + 20$
subtract $3x$: $4x - 4 = 20$
add 4: $4x = 24$
divide by 4: $x = 6$

EQUATIONS WITH BRACKETS
Expand first. $4(x - 2) = 2x + 6$ → $4x - 8 = 2x + 6$ → $2x = 14$ → $x = 7$

nth TERM
Difference first, then adjust. 11, 8, 5, 2: difference $-3$, so $14 - 3n$.
Check with $n = 1$: $14 - 3 = 11$ ✓""")

save_note("y8-maths-percent-geometry", 8, "Maths", "Percentage change, angles and circles", r"""PERCENTAGE CHANGE
Percentage change = change ÷ original × 100
£40 → £46: change 6, $6 \div 40 \times 100 = 15\%$ increase

MULTIPLIERS
Increase by 12%: × 1.12.   Decrease by 20%: × 0.8
£250 increased by 12% = $250 \times 1.12 = $ £280

ANGLES IN PARALLEL LINES
• Alternate angles (Z shape) are equal
• Corresponding angles (F shape) are equal
• Co-interior angles (C shape) add up to 180°

POLYGONS
Exterior angles always add up to 360°.
Regular octagon: each exterior angle = $360 \div 8 = 45$°, so each interior angle = 135°.

CIRCLES
Circumference $= \pi d$ (or $2\pi r$)
Area $= \pi r^2$
Radius 5 cm: area $= 3.14 \times 25 = 78.5$ cm²

VOLUME OF A CUBOID
length × width × height, in cm³""")

save_note("y8-science-chemistry", 8, "Science", "Atoms, elements, compounds and reactions", r"""ATOMS AND ELEMENTS
Everything is made of atoms. An element contains only one type of atom (iron, oxygen, carbon).
The periodic table lists all the elements. Metals: left and middle. Non-metals: right.
Elements in the same GROUP (column) react in similar ways.

COMPOUNDS
Two or more elements chemically joined. Water $\text{H}_2\text{O}$: 2 hydrogen + 1 oxygen.
Carbon dioxide $\text{CO}_2$: 1 carbon + 2 oxygen.

MIXTURE vs COMPOUND
Mixture: not joined, easy to separate (air, salt water).
Compound: chemically joined, new properties (water, salt).

CHEMICAL REACTIONS
reactants → products
magnesium + oxygen → magnesium oxide
Mass is conserved: atoms are rearranged, never created or destroyed.

SIGNS OF A REACTION
gas given off, colour change, temperature change, new solid (precipitate) forms""")

save_note("y8-science-body-physics", 8, "Science", "Digestion, respiration and electricity", r"""DIGESTION
mouth → oesophagus → stomach → small intestine (nutrients absorbed) → large intestine (water absorbed)
Enzymes break big food molecules into small ones the body can absorb.

RESPIRATION (in every cell)
Aerobic: glucose + oxygen → carbon dioxide + water (+ energy)
Anaerobic (muscles, short of oxygen): glucose → lactic acid (+ less energy)

PHOTOSYNTHESIS (in plants)
carbon dioxide + water → glucose + oxygen  (needs light, happens in chloroplasts)

BREATHING
Gas exchange happens in the alveoli: oxygen into the blood, carbon dioxide out.

ELECTRICITY
Current (I) in amps, potential difference (V) in volts, resistance (R) in ohms.
$V = I \times R$, so $R = V \div I$.  6 V and 0.5 A → 12 Ω

MAGNETS
Like poles repel, opposite poles attract.""")

save_note("y8-english-analysis", 8, "English", "Analysing language and structure", r"""LANGUAGE: ZOOM IN ON WORDS
Ask: what does this word make me picture or feel? Why THIS word?
"the river had swallowed the lower field" → personification: the river seems hungry and powerful.

TECHNIQUES TO SPOT
• Pathetic fallacy: weather matches mood (storm = chaos, sunshine = hope)
• Oxymoron: opposites together (deafening silence)
• Semantic field: a group of related words (blood, wound, battle → a field of war)
• Sibilance: repeated 's' sounds (slithering, silent snake)

STRUCTURE: ZOOM OUT
• How does it open and end? Short sentences = impact.
• Does the focus shift (wide view → one detail)?
• Is there a turning point?

WRITING ABOUT IT (P.E.E.)
Point: The writer shows the storm's power.
Evidence: the fence lay "like matchsticks".
Explain: matchsticks are tiny and fragile, so the reader sees how easily the storm destroyed it.""")

save_note("y8-english-writing", 8, "English", "Grammar and persuasive writing", r"""ACTIVE AND PASSIVE
Active: The ball broke the window.
Passive: The window was broken by the ball.

PUNCTUATION FOR EFFECT
• Semicolon: links two related main clauses. I like tea; my brother prefers coffee.
• Colon: introduces a list or explanation.
• Dash: a dramatic pause. The door opened - and there stood the headteacher.

PERSUASIVE TECHNIQUES: AFOREST
Anecdote, Facts, Opinion, Rhetorical question, Emotive language, Statistics, Triples (rule of three)
Plus: direct address ("you"), imperatives ("Act now"), counter-argument then rebuttal.

STRONG OPENINGS
Start with a vivid scenario, a shocking fact or a question, not "I am going to talk about...".

SPELLINGS TO LEARN
accommodation, receive, believe, definitely, separate, embarrass, occurrence, rhythm""")
print("Year 8 notes written")
