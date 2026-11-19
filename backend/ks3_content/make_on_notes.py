r"""Notenix Ontario (Grades 5-7): review notes per grade and subject (Math, Language).
Writes notes/on<grade>-<math|language>.json with "track": "on". Run from this folder: python make_on_notes.py
Plain text (no LaTeX), Canadian spelling, metric units."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

NOTES = {
    (5, "Math"): ("Grade 5 Math: the key ideas", """NUMBER
• Place value to 100 000: in 54 312 the 4 is worth 4 000. Round by looking at the digit to the right.
• Tenths and hundredths: 7/10 = 0.7, 25/100 = 0.25. Line up decimal points to add: 3.45 + 2.70 = 6.15.
• Equivalent fractions: multiply or divide the top and bottom by the same number. 3/4 = 6/8 = 9/12.
• Multiply by breaking numbers apart: 245 × 6 = 200 × 6 + 40 × 6 + 5 × 6 = 1 470.
• Remainders: 150 bars in boxes of 12 → 12 boxes and 6 left over, so 13 boxes are needed.

ALGEBRA AND CODING
• Patterns: 4, 9, 14, 19 adds 5 each time. Term 10 = 4 + 9 × 5 = 49.
• Equations: find the value that makes both sides equal. 6 × n = 42 → n = 7.
• Code runs in order; a loop repeats steps. Track the variable each time round.

DATA AND PROBABILITY
Mode = most common value. Median = middle value in order. Mean = total ÷ number of values.
Probability = favourable outcomes ÷ equally likely outcomes. 4 blue sections out of 8 → 1/2.

SPATIAL SENSE
Parallelogram area = base × height. Triangle area = base × height ÷ 2.
1 L = 1 000 mL · 1 m = 100 cm · 1 km = 1 000 m.

FINANCIAL LITERACY
Total the cost of every item, then subtract from the amount paid to find the change."""),
    (6, "Math"): ("Grade 6 Math: the key ideas", """NUMBER
• Decimals to thousandths: compare place by place. 0.407 < 0.45 < 0.457 < 0.46.
• Percents: 25% = 1/4, 3/8 = 0.375 = 37.5%.
• Ratios and rates: 2 parts concentrate : 5 parts water = 6 : 15. 6 L per 100 km → 21 L for 350 km.
• Integers: on a number line, further right is greater. −3 > −5 > −8.
• Multiply or divide decimals: 7.2 ÷ 0.9 = 72 ÷ 9 = 8.

ALGEBRA AND CODING
• 5a means 5 × a. Substitute: 5(6) − 4 = 26.
• Solve by doing the same to both sides: 3k = 27 → k = 9.
• Inequalities have many solutions: y + 4 < 10 means y < 6.
• Loops: a value doubled 4 times is multiplied by 2 × 2 × 2 × 2 = 16.

DATA AND PROBABILITY
Mean, median and mode can be different for the same data. Expected results: P(4 on a number cube) = 1/6,
so in 60 rolls expect about 10 fours.

SPATIAL SENSE
Composite shapes: split into rectangles and add. Volume of a rectangular prism = length × width × height.
Angles on a straight line add to 180°.

FINANCIAL LITERACY
Simple interest = amount × rate × years: 500 dollars at 3% for 2 years earns 30 dollars.
Best buy: compare the price per unit (per litre, per 100 g)."""),
    (7, "Math"): ("Grade 7 Math: the key ideas", """NUMBER
• Integers: adding a negative moves left (−7 + (−5) = −12). Same signs multiply/divide to a positive,
  different signs to a negative (−24 ÷ 6 = −4).
• Fractions: multiply tops and bottoms, then simplify: 2/3 × 9/10 = 18/30 = 3/5.
• Squares and square roots: 5² = 25, √144 = 12.
• Proportions: find the unit rate first. 4 tickets for 58 dollars → 14.50 dollars each.

FINANCIAL LITERACY
• HST in Ontario is 13%: a price × 1.13 gives the total with tax.
• A discount of 20% means paying 80%: 45 dollars × 0.8 = 36 dollars.

ALGEBRA
• Two-step equations: 4x + 9 = 37 → 4x = 28 → x = 7.
• Simplify: 3(2y − 5) + 4y = 6y − 15 + 4y = 10y − 15.
• Inequalities: 2n + 1 > 11 → n > 5.

SPATIAL SENSE
Circumference = π × diameter. Area of a circle = π × radius × radius (use 3.14 for π).
Angles in a triangle add to 180°. Scale: multiply the drawing length by the scale factor.

DATA AND PROBABILITY
Independent events: multiply the probabilities. P(heads and 6) = 1/2 × 1/6 = 1/12.
Experimental probability = results ÷ trials (22 heads in 50 flips = 11/25)."""),
    (5, "Language"): ("Grade 5 Language: reading and writing", """COMPREHENSION
• Main idea: what the whole text is mostly about. Details support it.
• Inference: use clues from the text plus what you know. A character who volunteers to steer has grown confident.
• Theme: the message or lesson, such as "with patience and good advice, a new skill can be learned."

TEXT FEATURES AND ORGANIZATION
Information texts are often organized past → present, cause → effect, or problem → solution.

FIGURATIVE LANGUAGE
Simile (like/as) · metaphor (says one thing is another) · personification (human actions for things:
"the thunder grumbled") · hyperbole (exaggeration).

GRAMMAR AND PUNCTUATION
• Keep verb tense consistent with time words: "Last winter, we skated."
• Commas separate items in a list. Question marks go inside quotation marks: "Can we go now?" asked Mia.
• their (belongs to them) · there (a place) · they're (they are).
• A compound sentence joins two sentences with and, but or so.

WORD PARTS AND SPELLING
re- = again · -less = without · -ful = full of. Canadian spelling: colour, neighbour, favourite, centre, metre."""),
    (6, "Language"): ("Grade 6 Language: reading and writing", """COMPREHENSION
• Character change: compare how a character acts at the start and at the end, and what caused the change.
• Evidence: choose the quotation that proves the exact point you are making.
• Point of view: first person (I) or third person (he, she, they).

ARGUMENTS
A claim is the writer's position. Look for each side's reasons and the writer's recommendation.

GRAMMAR
• Pronouns: subject (I, she, he) and object (me, her, him). "The coach gave Amir and me a ride."
• Subject–verb agreement: find the real subject. "The box of crayons is on the shelf."
• Fix run-ons with a period, a semicolon, or a comma + and/but/so.

PUNCTUATION
• Commas around extra information: "My cousin, a nurse in Ottawa, is visiting."
• Plural possessives: the dogs' leashes (more than one dog).

WORD KNOWLEDGE
Roots: aqua = water (aquarium) · tele = far (telescope) · graph = write · port = carry.
Connotation: thrifty (positive) vs. stingy (negative). Use context clues for new words (placid = calm)."""),
    (7, "Language"): ("Grade 7 Language: reading and writing", """COMPREHENSION
• Theme: what the story suggests about life, built through what characters do and feel.
• Symbols: an object can stand for something bigger (plants passed between sisters = connection, responsibility).
• Author's purpose: to inform, persuade or entertain. Structure: cause and effect, compare, sequence.

SENTENCES
• Complex sentence: independent clause + dependent clause ("When the bell rang, the students lined up").
• Dangling modifier: the opening phrase must describe the subject. Not "Running for the bus, my backpack fell open."
• Active voice (the goalie stopped the puck) is usually clearer than passive (the puck was stopped by the goalie).
• Be concise: cut words that repeat an idea.

PUNCTUATION
• Semicolon: joins two related sentences. Colon: after a complete sentence, introduces a list.

AGREEMENT
With either/or and neither/nor, the verb agrees with the nearer subject: "Neither the players nor the coach was happy."

WORD KNOWLEDGE
chron = time (chronological) · Connotation: confident vs. arrogant · Context clues: succinct = brief and clear.
Spelling: accommodate, occurrence, necessary."""),
}

for (grade, subject), (title, body) in NOTES.items():
    key = f"on{grade}-{subject.lower()}"
    note = {"key": key, "year": grade, "subject": subject, "title": title, "body": body, "track": "on"}
    (HERE / "notes" / f"{key}.json").write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8")
    print(key, len(body))
