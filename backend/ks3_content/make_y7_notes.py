"""Writes the Year 7 KS3 notes to notes/*.json. Edit here, run, deploy.
Bodies are plain text (line breaks kept) with maths in $...$."""
import json
from pathlib import Path

OUT = Path(__file__).parent / "notes"
OUT.mkdir(exist_ok=True)

NOTES = [
("y7-maths-fdp", "Maths", "Fractions, decimals and percentages", r"""KEY IDEA
Fractions, decimals and percentages are three ways of writing the same amount.
$\dfrac{1}{2} = 0.5 = 50\%$     $\dfrac{1}{4} = 0.25 = 25\%$     $\dfrac{3}{4} = 0.75 = 75\%$     $\dfrac{1}{10} = 0.1 = 10\%$     $\dfrac{1}{5} = 0.2 = 20\%$

CONVERTING
• Fraction → decimal: divide the top by the bottom. $\dfrac{3}{8} = 3 \div 8 = 0.375$
• Decimal → percentage: multiply by 100. $0.375 = 37.5\%$
• Percentage → fraction: put it over 100 and simplify. $35\% = \dfrac{35}{100} = \dfrac{7}{20}$

ADDING FRACTIONS
Make the denominators the same first.
$\dfrac{2}{3} + \dfrac{1}{4} = \dfrac{8}{12} + \dfrac{3}{12} = \dfrac{11}{12}$

FRACTION OF AN AMOUNT
Divide by the bottom, multiply by the top.
$\dfrac{3}{5}$ of 40: $40 \div 5 = 8$, then $8 \times 3 = 24$

PERCENTAGE OF AN AMOUNT (no calculator)
Build it from 10% and 5%.
15% of 60: 10% = 6, 5% = 3, so 15% = 9

COMMON MISTAKE
Adding the tops and the bottoms: $\dfrac{1}{2} + \dfrac{1}{3}$ is NOT $\dfrac{2}{5}$. It is $\dfrac{3}{6} + \dfrac{2}{6} = \dfrac{5}{6}$."""),

("y7-maths-negatives", "Maths", "Negative numbers", r"""ON THE NUMBER LINE
Numbers to the left are smaller: $-7 < -2 < 0 < 3$.
Think of temperatures: $-7$°C is colder than $-2$°C.

ADDING AND SUBTRACTING
• Adding a positive: move right. $-4 + 9 = 5$
• Subtracting a positive: move left. $3 - 8 = -5$
• Two signs next to each other:
  $+\,-$ or $-\,+$ → minus.  $6 + (-2) = 6 - 2 = 4$
  $-\,-$ → plus.  $5 - (-3) = 5 + 3 = 8$

MULTIPLYING AND DIVIDING
Same signs → positive. Different signs → negative.
$-3 \times -6 = 18$     $-20 \div 4 = -5$     $7 \times -2 = -14$

CHECK YOURSELF
$-2 - 5 = ?$   (answer: $-7$)
$-12 \div -3 = ?$   (answer: 4)"""),

("y7-maths-algebra", "Maths", "Algebra basics", r"""WORDS TO KNOW
• Term: $3a$, $5$, $-2b$
• Expression: terms added or subtracted, e.g. $3a + 5b - 2$ (no equals sign)
• Equation: has an equals sign and can be solved, e.g. $2x + 5 = 17$

SIMPLIFYING (collect like terms)
Only combine terms with the same letter.
$3a + 5b - a + 2b = 2a + 7b$

SUBSTITUTION
Swap the letter for the number, then follow BIDMAS.
If $x = 4$: $3x^2 = 3 \times 16 = 48$  (square first, then multiply)

SOLVING ONE- AND TWO-STEP EQUATIONS
Do the same thing to both sides, undoing in reverse order.
$2x + 5 = 17$
subtract 5: $2x = 12$
divide by 2: $x = 6$
Check: $2 \times 6 + 5 = 17$ ✓

SEQUENCES
3, 7, 11, 15, … goes up by 4 each time.
$n$th term: $4n - 1$  (the times-table of the difference, then adjust)"""),

("y7-maths-angles-area", "Maths", "Angles, area and perimeter", r"""ANGLE FACTS
• Angles on a straight line add up to 180°
• Angles around a point add up to 360°
• Angles in a triangle add up to 180°
• Vertically opposite angles are equal

Example: a triangle has angles 48° and 75°. Third angle = $180 - 48 - 75 = 57$°

TYPES OF ANGLE
acute: less than 90°   right: 90°   obtuse: between 90° and 180°   reflex: more than 180°

PERIMETER
The distance all the way around. Add every side.

AREA
• Rectangle: length × width
• Triangle: $\dfrac{1}{2} \times$ base × perpendicular height
• Parallelogram: base × perpendicular height

Example: triangle, base 10 cm, height 6 cm → $\dfrac{1}{2} \times 10 \times 6 = 30$ cm²

UNITS
Perimeter is in cm; area is in cm² (squared units)."""),

("y7-science-cells", "Science", "Cells", r"""ALL LIVING THINGS ARE MADE OF CELLS

ANIMAL AND PLANT CELLS BOTH HAVE
• Nucleus: contains DNA, controls the cell
• Cell membrane: controls what goes in and out
• Cytoplasm: jelly where chemical reactions happen
• Mitochondria: where respiration releases energy

ONLY PLANT CELLS HAVE
• Cell wall: made of cellulose, keeps the cell rigid
• Chloroplasts: where photosynthesis happens (contain green chlorophyll)
• Permanent vacuole: filled with cell sap, keeps the cell firm

LEVELS OF ORGANISATION
cell → tissue → organ → organ system → organism
e.g. muscle cell → muscle tissue → heart → circulatory system → you

SPECIALISED CELLS
• Red blood cell: no nucleus, more room to carry oxygen
• Root hair cell: long and thin to absorb water
• Sperm cell: tail to swim

USING A MICROSCOPE
Start on the lowest power, focus with the coarse knob, then the fine knob."""),

("y7-science-particles", "Science", "Particles and states of matter", r"""THE PARTICLE MODEL
Everything is made of tiny particles. How they are arranged decides the state.

SOLID: particles touching, in a regular pattern, vibrate on the spot. Fixed shape, cannot be squashed.
LIQUID: particles touching but arranged randomly, can slide past each other. Flows, takes the shape of its container, cannot be squashed.
GAS: particles far apart, moving quickly in all directions. Fills its container, can be squashed.

CHANGES OF STATE
solid → liquid: melting
liquid → gas: boiling / evaporating
gas → liquid: condensing
liquid → solid: freezing
solid → gas: subliming

DIFFUSION
Particles spread out from where there are lots to where there are few. It is faster in gases and when hotter.

MIXTURES
• Filtration: separates an insoluble solid from a liquid (sand and water)
• Evaporation: gets a dissolved solid back (salt from salty water)
• Chromatography: separates coloured dyes in ink"""),

("y7-science-forces", "Science", "Forces and energy", r"""FORCES
A force is a push or a pull, measured in newtons (N).
Contact forces: friction, air resistance, tension, normal (support) force
Non-contact forces: gravity (weight), magnetism, static electricity

RESULTANT FORCE
• Same direction: add.  Opposite directions: subtract.
10 N right and 4 N left → resultant 6 N to the right.
• Balanced forces (resultant 0): the object stays still or keeps moving at the same speed.

MASS AND WEIGHT
Mass is the amount of matter (kg) and does not change.
Weight is the force of gravity (N): weight = mass × gravitational field strength
On Earth $g \approx 10$ N/kg, so a 50 kg pupil weighs 500 N. On the Moon they weigh about one sixth as much.

ENERGY STORES
kinetic (moving), gravitational (high up), elastic (stretched), chemical (food, fuel, batteries), thermal (hot), nuclear
Energy is never used up; it is transferred between stores.

RENEWABLE vs NON-RENEWABLE
Renewable: wind, solar, tidal, hydroelectric, geothermal
Non-renewable: coal, oil, natural gas, nuclear"""),

("y7-english-grammar", "English", "Word classes and sentences", r"""WORD CLASSES
• Noun: a person, place or thing (Maya, school, courage)
• Verb: an action or state (run, is, decided)
• Adjective: describes a noun (tired dog, steep hill)
• Adverb: describes a verb, often ends in -ly (slowly, quietly, soon)
• Pronoun: replaces a noun (she, it, they)
• Preposition: shows where or when (under, after, through)
• Conjunction: joins clauses (and, but, because, although)

SENTENCE TYPES
• Simple: one main clause. "The cat slept."
• Compound: two main clauses joined by and/but/or. "The cat slept and the dog barked."
• Complex: a main clause + a subordinate clause. "Although it was late, the cat refused to sleep."

ACTIVE AND PASSIVE
Active: The chef cooked the meal.
Passive: The meal was cooked by the chef.
Use the passive to put the focus on what happened, not who did it.

WRITE BETTER SENTENCES
Vary how you start: with an adverb (Slowly, …), a subordinate clause (When the bell rang, …) or a verb ending in -ing (Clutching her bag, …)."""),

("y7-english-punctuation", "English", "Punctuation and spelling", r"""APOSTROPHES
• Missing letters: do not → don't, it is → it's
• Belonging: the girl's bag (one girl), the girls' bags (more than one)
• its = belonging to it (no apostrophe). it's = it is / it has.

SPEECH MARKS
"Where are you going?" asked Tom.
• Punctuation goes inside the speech marks
• New speaker, new line

COMMAS
• In lists: eggs, flour, sugar and butter
• After a fronted adverbial: After lunch, we went outside.
• Around extra information: My brother, who is twelve, loves football.

SEMICOLONS AND COLONS
• Semicolon joins two linked main clauses: It was getting dark; we headed home.
• Colon introduces a list or explanation: You need three things: a pen, a ruler and a calculator.

TRICKY SPELLINGS
definitely (de-FINITE-ly), separate (there's A RAT in sepARATe), necessary (one Collar, two Sleeves), their / there / they're, your / you're"""),

("y7-english-reading", "English", "Reading: inference and language", r"""INFERENCE = READING BETWEEN THE LINES
Writers often SHOW feelings instead of telling you.
"She clutched her bag so tightly her knuckles turned white." → she is nervous.
Ask: what does this detail suggest? How do I know?

ANSWERING READING QUESTIONS (P.E.E.)
• Point: Maya feels nervous at first.
• Evidence: "clutching the straps … so tightly that her knuckles turned white"
• Explain: the tight grip shows she is tense and anxious about starting school.

LANGUAGE TECHNIQUES
• Simile: compares using like/as. "as fast as a cheetah"
• Metaphor: says something IS something else. "a river of blazers"
• Personification: gives human qualities to objects. "the wind howled"
• Alliteration: same starting sound. "silent, silver stars"
• Onomatopoeia: words that sound like the noise. crash, shriek, buzz

WHY WORD CHOICE MATTERS
Ask why the writer chose THIS word. "Shrieked" (not "rang") makes the bell sound loud and alarming.

PURPOSE: PIE
Persuade (offers, exclamations, "you"), Inform (facts, headings), Entertain (stories, description). Instructions use commands: "Mix the flour."
"""),
]

for i, (key, subject, title, body) in enumerate(NOTES, 1):
    (OUT / f"{key}.json").write_text(json.dumps(
        {"key": key, "year": 7, "subject": subject, "title": f"Year 7 {subject}: {title}", "body": body.strip()},
        ensure_ascii=False, indent=2), encoding="utf-8")
print(f"wrote {len(NOTES)} notes to {OUT}")
