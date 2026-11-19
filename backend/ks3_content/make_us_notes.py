r"""Notenix Middle School (US Grades 5-7): one set of review notes per grade and subject.
Writes notes/g<grade>-<math|ela>.json with "track": "us". Run from this folder: python make_us_notes.py
Plain text (no LaTeX), same style as the KS3 notes: CAPITAL headings, short worked examples."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

NOTES = {
    (5, "Math"): ("Grade 5 Math: the key ideas", """PLACE VALUE AND DECIMALS
Each place is 10 times the place to its right: ones, tenths, hundredths, thousandths.
• In 3.462 the 6 is 6 hundredths.
• × 10 moves every digit one place left: 0.47 × 10 = 4.7. ÷ 10 moves them right.
• Compare decimals place by place: 0.305 < 0.35 because 3 tenths 0 hundredths < 3 tenths 5 hundredths.

MULTIPLYING AND DIVIDING
• Break the multiplier apart: 346 × 27 = 346 × 20 + 346 × 7 = 6,920 + 2,422 = 9,342.
• Divide using chunks: 1,512 ÷ 24 → 24 × 60 = 1,440, 72 left, 24 × 3 = 72, so 63.

FRACTIONS
• To add or subtract, make the denominators the same: 2/3 + 1/4 = 8/12 + 3/12 = 11/12.
• Fraction × whole number: 3/5 × 10 = 30/5 = 6.
• Unit fraction ÷ whole number: 1/3 ÷ 4 = 1/12 (a third split into 4 parts).

VOLUME
Volume of a rectangular prism = length × width × height, in cubic units.
5 cm × 4 cm × 3 cm = 60 cubic centimeters.

THE COORDINATE PLANE
(x, y): go across x, then up y. Points on the x-axis have y = 0.

ORDER OF OPERATIONS
Parentheses first, then × and ÷ (left to right), then + and − (left to right).
18 − 3 × (2 + 4) = 18 − 3 × 6 = 18 − 18 = 0."""),
    (6, "Math"): ("Grade 6 Math: the key ideas", """RATIOS AND RATES
• A ratio compares two amounts: 12 girls to 18 boys is 12:18 = 2:3.
• A unit rate is "per 1": 150 miles in 3 hours is 50 miles per hour.
• Scale up with a table or by multiplying both parts: 2 cups flour : 3 cups oats = 6 : 9.

PERCENTS
Percent means "out of 100". 35% of 80 = 0.35 × 80 = 28.
To find what percent: part ÷ whole × 100. 15 out of 60 = 0.25 = 25%.

DIVIDING FRACTIONS
Multiply by the reciprocal (flip the second fraction): 3/4 ÷ 3/8 = 3/4 × 8/3 = 2.
Ask "how many 3/8s fit in 3/4?" to check the answer makes sense.

NEGATIVE NUMBERS
• On a number line, further left is smaller: −7 < −3 < −1 < 2.
• Absolute value is the distance from 0: |−9| = 9.

EXPRESSIONS AND EQUATIONS
• 3x means 3 × x. If x = 4, 3x + 5 = 17.
• Distribute: 4(2a + 3) = 8a + 12.
• Solve by doing the same to both sides: x + 9 = 23 → x = 14; 6y = 42 → y = 7.

AREA
Triangle = 1/2 × base × height. Parallelogram = base × height.

STATISTICS
Mean: add the values and divide by how many. Median: the middle value once they are in order
(with an even number of values, halfway between the middle two)."""),
    (7, "Math"): ("Grade 7 Math: the key ideas", """PROPORTIONAL RELATIONSHIPS
y is proportional to x when y = kx; k is the constant of proportionality (y ÷ x, always the same).
If y = 10 when x = 4, then k = 2.5 and y = 25 when x = 10.

PERCENT PROBLEMS
• Discount: 25% off 60 dollars → 60 × 0.75 = 45 dollars.
• Tip or tax: 18% on 40 dollars → 40 × 1.18 = 47.20 dollars.
• Percent change = change ÷ original × 100. From 50 to 65: 15 ÷ 50 = 30% increase.

RATIONAL NUMBERS
• Adding a negative moves left: −8 + 5 = −3.
• Same signs multiply or divide to give a positive; different signs give a negative:
  −6 × (−4) = 24, (−3/4) ÷ (1/2) = −1 1/2.

EXPRESSIONS, EQUATIONS AND INEQUALITIES
• Simplify carefully with negatives: 5x − 2(x − 4) = 5x − 2x + 8 = 3x + 8.
• Two-step equations: 3x − 7 = 14 → 3x = 21 → x = 7.
• Multiplying or dividing an inequality by a negative number flips the sign: −2x > 10 → x < −5.

CIRCLES AND ANGLES
• Circumference = 2 × π × r. Area = π × r × r. (Use 3.14 for π.)
• Supplementary angles add to 180°; complementary angles add to 90°.

PROBABILITY
Probability = favorable outcomes ÷ total outcomes, from 0 (impossible) to 1 (certain).
For two events, multiply the number of outcomes: a coin and a number cube give 2 × 6 = 12."""),
    (5, "English Language Arts"): ("Grade 5 ELA: reading and language", """READING: MAIN IDEA AND DETAILS
The main idea is what the whole passage is mostly about. Details support it.
Test a choice: does the whole passage support it, or only one sentence?

INFERENCE
An inference is a smart guess using clues from the text plus what you know.
"His fingers felt like frozen sticks" → he is nervous.

THEME
The theme is the lesson or message about life, e.g. "Support from someone you love can help you face fears."
Look at how the character changes and what they learn.

FIGURATIVE LANGUAGE
• Simile: compares using like or as ("like a boat on a calm river").
• Metaphor: says one thing IS another ("Time is a thief").
• Personification: gives human actions to things ("the wind whispered").
• Hyperbole: huge exaggeration ("I've told you a million times").

GRAMMAR AND PUNCTUATION
• Keep verb tense consistent: "Yesterday we walked."
• Commas separate items in a list and follow introductory words: "Yes, I'd like that."
• Conjunctions join ideas: and (adds), but (contrasts), so (result), because (reason).

WORD PARTS
mis- = wrongly · re- = again · pre- = before · un-/in- = not · -ible/-able = able to be."""),
    (6, "English Language Arts"): ("Grade 6 ELA: reading and language", """CENTRAL IDEA AND EVIDENCE
The central idea is the main point the author develops. When a question asks for evidence,
pick the quotation that proves the answer most directly.

POINT OF VIEW
• First person: the narrator is in the story ("I", "we").
• Third person: a narrator outside the story ("he", "she", "they").

ARGUMENTS
A claim is the author's position. Reasons and evidence support it. Words such as "however",
"on the other hand" and "critics argue" signal the other side.

PRONOUNS
• Subject pronouns (I, she, he, we, they) do the action: "She and Ava are going."
• Object pronouns (me, her, him, us, them) receive it: "to Sam and me."
• Make sure every pronoun clearly refers to one person.

PUNCTUATION
Put commas around extra (nonessential) information: "My uncle, who lives in Ohio, is visiting."
Avoid run-ons: join two sentences with a comma + and/but/so, or a period.

GREEK AND LATIN ROOTS
graph = write (autograph) · port = carry (portable) · tele = far · bio = life · aud = hear.

CONNOTATION
Words can have the same meaning but different feelings: determined (positive) vs. stubborn (negative)."""),
    (7, "English Language Arts"): ("Grade 7 ELA: reading and language", """THEME AND CHARACTER
A theme is developed over the whole story: look at what characters do, say and learn.
"A garden is not measured by what you keep" → generosity builds connections.

AUTHOR'S PURPOSE AND TEXT STRUCTURE
• Purpose: to inform/explain, to persuade, or to entertain.
• Structures: cause and effect, compare and contrast, problem and solution, chronological order.

SUPPORTING EVIDENCE
Choose the sentence that proves the exact point in the question, not just a related fact.

SENTENCES AND CLAUSES
• Simple: one independent clause. Compound: two joined by and/but/so.
• Complex: an independent clause + a dependent clause ("Although it was late, we kept reading").
• Place modifiers next to what they describe: "Mom washed the dog, which was covered in mud."

PUNCTUATION
• A semicolon joins two complete sentences: "I wanted to go; however, it was too late."
• Separate equal adjectives with a comma: "a fascinating, enjoyable movie".

WORD CHOICE
• Be concise: cut words that repeat the same idea.
• Connotation matters: cozy (pleasant) vs. cramped (unpleasant).
• Latin root bene = good (benefit). Use context clues for words like "verbose" (too wordy)."""),
}

for (grade, subject), (title, body) in NOTES.items():
    key = f"g{grade}-{'math' if subject == 'Math' else 'ela'}"
    note = {"key": key, "year": grade, "subject": subject, "title": title, "body": body, "track": "us"}
    (HERE / "notes" / f"{key}.json").write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8")
    print(key, len(body))
