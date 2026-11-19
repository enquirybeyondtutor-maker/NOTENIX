r"""Notenix Middle School (US Grades 5-7): the six Common Core baseline tests.
Writes tests/g<grade>-baseline-<math|ela>.json. Original questions.
Run from this folder: python make_us_baselines.py

Plain text only (no LaTeX): US prices use "$", which the app's maths renderer would otherwise
try to read. Every string is checked against that renderer's pattern before saving.
"""
import json
import re
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATH = re.compile(r"\$\$([\s\S]+?)\$\$|\$(?![\s$])((?:\\.|[^$\\\n])+?)(?<!\s)\$(?!\d)")   # frontend MathText
_slot = [0]


def Q(topic, question, correct, wrongs, explanation, check=None):
    """Four options, written right answer first; the right answer moves through positions 1-4."""
    if check is not None:
        assert check() is True, f"check failed: {question[:60]}"
    assert len(wrongs) == 3 and len({correct, *wrongs}) == 4, question[:60]
    pos = [2, 0, 3, 1, 1, 3, 0, 2][_slot[0] % 8]
    _slot[0] += 1
    opts = list(wrongs)
    opts.insert(pos, correct)
    return {"topic": topic, "question": question.strip(), "options": opts, "answer": correct,
            "explanation": explanation.strip()}


def passage(text, ask):
    return f'Read the passage.\n\n"{text.strip()}"\n\n{ask}'


def save(grade, subject, key, questions):
    assert len(questions) == 20, (grade, subject, len(questions))
    t = {"slot": f"g{grade}-baseline", "subject": subject, "title": f"Grade {grade} {subject} Baseline",
         "topic": "Baseline", "duration": 30, "level": f"Grade {grade}", "board": "Common Core",
         "questions": questions}
    for q in questions:
        for s in [q["question"], q["explanation"], *q["options"]]:
            assert not MATH.search(s), f"would render as maths: {s[:80]}"
    (HERE / "tests" / f"g{grade}-baseline-{key}.json").write_text(
        json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"g{grade}-baseline-{key}: {len(questions)} questions")


# ═══ Grade 5 Math ═══
PV, MD, FR, VOL, CO, OO, ME = ("Place value & decimals", "Multiplication & division", "Fractions", "Volume",
                               "Coordinate plane", "Order of operations", "Measurement")
save(5, "Math", "math", [
    Q(PV, "What is the value of the digit 6 in 3.462?", "6 hundredths", ["6 tenths", "6 thousandths", "6 ones"],
      "3.462 is 3 ones, 4 tenths, 6 hundredths and 2 thousandths."),
    Q(PV, "Which number is 10 times as much as 0.47?", "4.7", ["0.047", "47", "0.57"],
      "Multiplying by 10 moves every digit one place to the left: 0.47 × 10 = 4.7.", check=lambda: F("0.47") * 10 == F("4.7")),
    Q(PV, "Round 8.365 to the nearest hundredth.", "8.37", ["8.36", "8.4", "8.3"],
      "The hundredths digit is 6. The next digit is 5, so round up: 8.37."),
    Q(PV, "Which list shows the decimals in order from least to greatest?", "0.305, 0.35, 0.503, 0.53",
      ["0.35, 0.305, 0.53, 0.503", "0.53, 0.503, 0.35, 0.305", "0.305, 0.503, 0.35, 0.53"],
      "Compare place by place: 0.305 < 0.350 < 0.503 < 0.530.",
      check=lambda: sorted([0.53, 0.305, 0.503, 0.35]) == [0.305, 0.35, 0.503, 0.53]),
    Q(MD, "What is 346 × 27?", "9,342", ["9,232", "3,114", "9,442"],
      "346 × 20 = 6,920 and 346 × 7 = 2,422. 6,920 + 2,422 = 9,342.", check=lambda: 346 * 27 == 9342),
    Q(MD, "What is 1,512 ÷ 24?", "63", ["62", "64", "73"],
      "24 × 60 = 1,440, leaving 72, and 72 ÷ 24 = 3. So 1,512 ÷ 24 = 63.", check=lambda: 1512 / 24 == 63),
    Q(MD, "A school buys 18 boxes of pencils. Each box holds 144 pencils. How many pencils does the school buy?",
      "2,592", ["2,492", "2,602", "1,296"], "144 × 18 = 144 × 10 + 144 × 8 = 1,440 + 1,152 = 2,592.",
      check=lambda: 144 * 18 == 2592),
    Q(FR, "What is 2/3 + 1/4?", "11/12", ["3/7", "3/12", "8/12"],
      "Use a common denominator of 12: 2/3 = 8/12 and 1/4 = 3/12, so the sum is 11/12. Adding tops and bottoms (3/7) is a common mistake.",
      check=lambda: F(2, 3) + F(1, 4) == F(11, 12)),
    Q(FR, "What is 3 1/2 − 1 3/4?", "1 3/4", ["2 1/4", "2 3/4", "1 1/4"],
      "3 1/2 = 3 2/4. Take away 1 3/4: rename as 2 6/4 − 1 3/4 = 1 3/4.", check=lambda: F(7, 2) - F(7, 4) == F(7, 4)),
    Q(FR, "What is 3/5 × 10?", "6", ["2", "13", "50"],
      "3/5 × 10 = 30/5 = 6. You can also find 1/5 of 10 (which is 2) and multiply by 3.", check=lambda: F(3, 5) * 10 == 6),
    Q(FR, "What is 1/3 ÷ 4?", "1/12", ["4/3", "1/7", "3/4"],
      "Dividing a third into 4 equal parts makes each part 1/12. 1/3 ÷ 4 = 1/3 × 1/4 = 1/12.", check=lambda: F(1, 3) / 4 == F(1, 12)),
    Q(FR, "Maria ran 3/4 of a mile every day for 6 days. How far did she run in all?", "4 1/2 miles",
      ["4 1/4 miles", "3 3/4 miles", "6 3/4 miles"], "6 × 3/4 = 18/4 = 4 2/4 = 4 1/2 miles.", check=lambda: 6 * F(3, 4) == F(9, 2)),
    Q(VOL, "A box shaped like a rectangular prism is 5 cm long, 4 cm wide and 3 cm high. What is its volume?",
      "60 cubic centimeters", ["12 cubic centimeters", "47 cubic centimeters", "94 cubic centimeters"],
      "Volume = length × width × height = 5 × 4 × 3 = 60 cubic centimeters.", check=lambda: 5 * 4 * 3 == 60),
    Q(VOL, "One box measures 3 × 3 × 3 units and another measures 2 × 4 × 5 units. What is their total volume?",
      "67 cubic units", ["47 cubic units", "63 cubic units", "70 cubic units"],
      "3 × 3 × 3 = 27 and 2 × 4 × 5 = 40. Together: 27 + 40 = 67 cubic units.", check=lambda: 27 + 40 == 67),
    Q(CO, "Point A is at (4, 2) on a coordinate grid. It moves 3 units up. Where is it now?", "(4, 5)",
      ["(7, 2)", "(4, −1)", "(5, 4)"], "Moving up changes only the y-coordinate: 2 + 3 = 5. The x-coordinate stays 4."),
    Q(CO, "Which point lies on the x-axis?", "(6, 0)", ["(0, 6)", "(6, 6)", "(1, 1)"],
      "Points on the x-axis have a y-coordinate of 0. (0, 6) is on the y-axis."),
    Q(OO, "What is 18 − 3 × (2 + 4)?", "0", ["90", "12", "16"],
      "Parentheses first: 2 + 4 = 6. Then multiply: 3 × 6 = 18. Then subtract: 18 − 18 = 0.", check=lambda: 18 - 3 * (2 + 4) == 0),
    Q(OO, "Which expression means 'add 7 and 3, then multiply by 5'?", "(7 + 3) × 5", ["7 + 3 × 5", "5 × 7 + 3", "7 × 5 + 3"],
      "Parentheses show that 7 + 3 is done first. Without them, 3 × 5 would be done before adding."),
    Q(ME, "How many centimeters are in 3.2 meters?", "320", ["32", "3,200", "0.32"],
      "There are 100 centimeters in a meter: 3.2 × 100 = 320.", check=lambda: F("3.2") * 100 == 320),
    Q(ME, "A ribbon is 4 feet long. How many inches long is it?", "48", ["12", "36", "40"],
      "There are 12 inches in a foot: 4 × 12 = 48 inches.", check=lambda: 4 * 12 == 48),
])

# ═══ Grade 6 Math ═══
RA, PC, FD, NG, EE, GE, ST, FM = ("Ratios & rates", "Percents", "Dividing fractions", "Negative numbers",
                                  "Expressions & equations", "Area", "Statistics", "Factors & multiples")
save(6, "Math", "math", [
    Q(RA, "A class has 12 girls and 18 boys. What is the ratio of girls to boys in simplest form?", "2:3",
      ["3:2", "12:30", "2:5"], "12:18 divides by 6 to give 2:3. Order matters: girls first.", check=lambda: F(12, 18) == F(2, 3)),
    Q(RA, "A car travels 150 miles in 3 hours at a steady speed. What is its speed?", "50 miles per hour",
      ["45 miles per hour", "153 miles per hour", "450 miles per hour"], "150 ÷ 3 = 50 miles in each hour.", check=lambda: 150 / 3 == 50),
    Q(RA, "Six apples cost $4.80. At the same price, how much do 10 apples cost?", "$8.00", ["$6.80", "$7.20", "$8.40"],
      "One apple costs 4.80 ÷ 6 = 0.80 dollars, so 10 apples cost 8.00 dollars.", check=lambda: F("4.80") / 6 * 10 == 8),
    Q(RA, "A recipe uses 2 cups of flour for every 3 cups of oats. How much flour goes with 9 cups of oats?", "6 cups",
      ["4 cups", "5 cups", "13.5 cups"], "9 cups of oats is 3 times 3 cups, so use 3 times 2 cups of flour: 6 cups.", check=lambda: F(2, 3) * 9 == 6),
    Q(PC, "What is 35% of 80?", "28", ["24", "35", "45"], "10% of 80 is 8, so 30% is 24 and 5% is 4. 24 + 4 = 28.",
      check=lambda: F(35, 100) * 80 == 28),
    Q(PC, "15 is what percent of 60?", "25%", ["15%", "40%", "4%"], "15/60 = 1/4 = 25%.", check=lambda: F(15, 60) == F(25, 100)),
    Q(FD, "What is 3/4 ÷ 3/8?", "2", ["9/32", "1/2", "1 1/8"],
      "Multiply by the reciprocal: 3/4 × 8/3 = 24/12 = 2. There are two 3/8s in 3/4.", check=lambda: F(3, 4) / F(3, 8) == 2),
    Q(FD, "How many 2/3-cup servings are in 4 cups of rice?", "6", ["2 2/3", "8", "12"],
      "4 ÷ 2/3 = 4 × 3/2 = 6 servings.", check=lambda: 4 / F(2, 3) == 6),
    Q(NG, "Which list is in order from least to greatest?", "−7, −3, −1, 2", ["−1, −3, −7, 2", "2, −1, −3, −7", "−3, −7, −1, 2"],
      "On a number line, numbers further left are smaller: −7 is furthest left, then −3, −1 and 2.",
      check=lambda: sorted([-3, -7, 2, -1]) == [-7, -3, -1, 2]),
    Q(NG, "What is the absolute value of −9?", "9", ["−9", "0", "1/9"],
      "Absolute value is the distance from 0, which is never negative: |−9| = 9."),
    Q(NG, "The temperature was −4°F in the morning and rose 11 degrees by noon. What was the temperature at noon?", "7°F",
      ["−15°F", "−7°F", "15°F"], "−4 + 11 = 7. Rising 4 degrees brings it to 0, and 7 more makes 7°F.", check=lambda: -4 + 11 == 7),
    Q(EE, "What is the value of 3x + 5 when x = 4?", "17", ["12", "35", "39"],
      "3x means 3 × x: 3 × 4 = 12, and 12 + 5 = 17.", check=lambda: 3 * 4 + 5 == 17),
    Q(EE, "Solve x + 9 = 23.", "x = 14", ["x = 13", "x = 32", "x = 207"],
      "Subtract 9 from both sides: x = 23 − 9 = 14.", check=lambda: 14 + 9 == 23),
    Q(EE, "Solve 6y = 42.", "y = 7", ["y = 36", "y = 48", "y = 252"], "Divide both sides by 6: y = 42 ÷ 6 = 7.", check=lambda: 6 * 7 == 42),
    Q(EE, "Which expression is equivalent to 4(2a + 3)?", "8a + 12", ["8a + 3", "6a + 7", "8a + 7"],
      "Multiply each term inside the parentheses by 4: 4 × 2a = 8a and 4 × 3 = 12.",
      check=lambda: all(4 * (2 * a + 3) == 8 * a + 12 for a in range(-5, 6))),
    Q(GE, "A triangle has a base of 10 cm and a height of 6 cm. What is its area?", "30 square centimeters",
      ["60 square centimeters", "16 square centimeters", "32 square centimeters"],
      "Area of a triangle = 1/2 × base × height = 1/2 × 10 × 6 = 30 square centimeters.", check=lambda: 10 * 6 / 2 == 30),
    Q(GE, "A parallelogram has a base of 9 inches and a height of 5 inches. What is its area?", "45 square inches",
      ["22.5 square inches", "28 square inches", "14 square inches"], "Area of a parallelogram = base × height = 9 × 5 = 45 square inches.",
      check=lambda: 9 * 5 == 45),
    Q(ST, "What is the mean of 4, 8, 9, 11 and 13?", "9", ["8", "11", "45"],
      "Add the numbers (45) and divide by how many there are (5): 45 ÷ 5 = 9.", check=lambda: (4 + 8 + 9 + 11 + 13) / 5 == 9),
    Q(ST, "What is the median of 2, 3, 9, 1, 5 and 12?", "4", ["3", "5", "9"],
      "Put them in order: 1, 2, 3, 5, 9, 12. With six numbers, the median is halfway between the middle two: (3 + 5) ÷ 2 = 4.",
      check=lambda: sorted([2, 3, 9, 1, 5, 12])[2:4] == [3, 5]),
    Q(FM, "What is the greatest common factor of 24 and 36?", "12", ["6", "72", "4"],
      "The factors of 24 are 1, 2, 3, 4, 6, 8, 12, 24; of 36 they include 12 but not 24. The greatest shared factor is 12. (72 is the least common multiple.)",
      check=lambda: max(k for k in range(1, 25) if 24 % k == 0 and 36 % k == 0) == 12),
])

# ═══ Grade 7 Math ═══
PR, PA, RN, EQ, G7, PB = ("Proportional relationships", "Percent problems", "Rational numbers", "Expressions & equations",
                          "Geometry", "Probability")
save(7, "Math", "math", [
    Q(PR, "y is proportional to x. When x = 4, y = 10. What is y when x = 10?", "25", ["16", "20", "40"],
      "The constant of proportionality is 10 ÷ 4 = 2.5, so y = 2.5 × 10 = 25.", check=lambda: F(10, 4) * 10 == 25),
    Q(PR, "Which table shows a proportional relationship between x and y?", "x = 1, 2, 3 and y = 3, 6, 9",
      ["x = 1, 2, 3 and y = 2, 4, 7", "x = 1, 2, 3 and y = 4, 5, 6", "x = 1, 2, 3 and y = 1, 4, 9"],
      "In a proportional relationship y ÷ x is always the same. For 3, 6, 9 it is 3 every time; the others change."),
    Q(PR, "On a map, 2 inches represent 15 miles. Two towns are 7 inches apart on the map. How far apart are they?", "52.5 miles",
      ["30 miles", "105 miles", "45 miles"], "Each inch is 15 ÷ 2 = 7.5 miles, so 7 inches is 7 × 7.5 = 52.5 miles.",
      check=lambda: F(15, 2) * 7 == F(105, 2)),
    Q(PA, "A jacket that costs $60 is on sale for 25% off. What is the sale price?", "$45", ["$15", "$35", "$75"],
      "25% of 60 is 15. The sale price is 60 − 15 = 45 dollars.", check=lambda: 60 * F(3, 4) == 45),
    Q(PA, "A meal costs $40. The family leaves an 18% tip. What is the total cost?", "$47.20", ["$7.20", "$41.80", "$58.00"],
      "18% of 40 is 7.20. The total is 40 + 7.20 = 47.20 dollars.", check=lambda: 40 * F(118, 100) == F("47.20")),
    Q(PA, "The price of a game rose from $50 to $65. What was the percent increase?", "30%", ["15%", "23%", "65%"],
      "The increase is 15 dollars. As a percent of the original price: 15 ÷ 50 = 0.30 = 30%.", check=lambda: F(15, 50) == F(30, 100)),
    Q(RN, "What is −8 + 5?", "−3", ["3", "−13", "13"], "Start at −8 and move 5 to the right on the number line: −3.",
      check=lambda: -8 + 5 == -3),
    Q(RN, "What is −6 × (−4)?", "24", ["−24", "−10", "10"], "A negative times a negative is positive: 6 × 4 = 24.",
      check=lambda: -6 * -4 == 24),
    Q(RN, "What is −2.5 − 3.75?", "−6.25", ["1.25", "−1.25", "6.25"],
      "Subtracting a positive moves further left: −2.5 − 3.75 = −6.25.", check=lambda: F("-2.5") - F("3.75") == F("-6.25")),
    Q(RN, "What is (−3/4) ÷ (1/2)?", "−1 1/2", ["−3/8", "3/8", "1 1/2"],
      "Multiply by the reciprocal: −3/4 × 2 = −6/4 = −1 1/2. A negative divided by a positive is negative.",
      check=lambda: F(-3, 4) / F(1, 2) == F(-3, 2)),
    Q(EQ, "Solve 3x − 7 = 14.", "x = 7", ["x = 2 1/3", "x = 21", "x = 3"],
      "Add 7 to both sides: 3x = 21. Divide by 3: x = 7.", check=lambda: 3 * 7 - 7 == 14),
    Q(EQ, "Which expression is equivalent to 5x − 2(x − 4)?", "3x + 8", ["3x − 8", "3x − 4", "7x + 8"],
      "−2(x − 4) = −2x + 8, so 5x − 2x + 8 = 3x + 8. Watch the sign: −2 times −4 is +8.",
      check=lambda: all(5 * x - 2 * (x - 4) == 3 * x + 8 for x in range(-5, 6))),
    Q(EQ, "Solve −2x > 10.", "x < −5", ["x > −5", "x < 5", "x > 5"],
      "Divide both sides by −2. Dividing by a negative number flips the inequality sign: x < −5.",
      check=lambda: all((-2 * x > 10) == (x < -5) for x in range(-20, 20))),
    Q(EQ, "A gym charges $25 to join plus $15 a month. Which equation gives the total cost, c, after m months?", "c = 15m + 25",
      ["c = 25m + 15", "c = 40m", "c = 15m − 25"], "The monthly charge is multiplied by the number of months (15m), and the joining fee is added once (+ 25)."),
    Q(G7, "A circle has a radius of 5 cm. Using 3.14 for π, what is its circumference?", "31.4 cm", ["15.7 cm", "78.5 cm", "62.8 cm"],
      "Circumference = 2 × π × r = 2 × 3.14 × 5 = 31.4 cm. 78.5 would be the area.", check=lambda: 2 * F("3.14") * 5 == F("31.4")),
    Q(G7, "A circle has a diameter of 10 m. Using 3.14 for π, what is its area?", "78.5 square meters",
      ["31.4 square meters", "314 square meters", "15.7 square meters"],
      "The radius is half the diameter, 5 m. Area = π × r × r = 3.14 × 25 = 78.5 square meters.", check=lambda: F("3.14") * 25 == F("78.5")),
    Q(G7, "Two angles are supplementary. One of them measures 65°. What does the other measure?", "115°", ["25°", "35°", "295°"],
      "Supplementary angles add up to 180°: 180 − 65 = 115°. (Complementary angles add up to 90°.)", check=lambda: 180 - 65 == 115),
    Q(PB, "A bag holds 3 red, 5 blue and 2 green marbles. One marble is picked at random. What is the probability that it is blue?",
      "1/2", ["1/5", "5/8", "1/3"], "There are 10 marbles and 5 are blue: 5/10 = 1/2.", check=lambda: F(5, 10) == F(1, 2)),
    Q(PB, "A number cube numbered 1 to 6 is rolled. What is the probability of rolling a number greater than 4?", "1/3",
      ["1/2", "2/3", "1/6"], "Only 5 and 6 are greater than 4: 2 out of 6 = 1/3.", check=lambda: F(2, 6) == F(1, 3)),
    Q(PB, "A coin is flipped and a number cube (1 to 6) is rolled. How many different outcomes are possible?", "12",
      ["8", "6", "36"], "Each of the 2 coin results can pair with each of the 6 numbers: 2 × 6 = 12.", check=lambda: 2 * 6 == 12),
])

# ═══ Grade 5 ELA ═══
MI, INF, TH, FIG, VOC, KD, TS, GR, PU, WP, SP = ("Main idea", "Inference", "Theme", "Figurative language", "Vocabulary",
                                                "Key details", "Text structure", "Grammar & usage", "Punctuation",
                                                "Word parts", "Spelling")
LEO = """Leo had practiced the piano piece for weeks, but when he walked onto the stage his fingers felt like frozen sticks. He looked out at the rows of faces and spotted his grandmother in the front row. She gave him a small nod, the same nod she gave him every Sunday when he played for her in her kitchen. Leo took a slow breath, set his hands on the keys, and began. The first notes wobbled, but by the middle of the piece the music was carrying him along like a boat on a calm river. When he finished, the applause sounded far away, and all he could see was his grandmother's proud smile."""
BEES = """Honeybees live in large groups called colonies. Each colony has one queen, who lays all the eggs. Most of the bees are worker bees. Workers have many jobs: some clean the hive, some feed the young bees, and others fly out to collect nectar and pollen from flowers. As bees move from flower to flower, pollen sticks to their fuzzy bodies and is carried to the next flower. This helps plants make seeds and fruit. In fact, many of the fruits and vegetables people eat depend on bees. Without honeybees, farmers would have a much harder time growing food."""
save(5, "English Language Arts", "ela", [
    Q(INF, passage(LEO, "How does Leo feel when he first walks onto the stage?"), "nervous", ["bored", "angry", "proud"],
      "His fingers 'felt like frozen sticks', a sign of nerves. He only relaxes once he sees his grandmother and starts playing."),
    Q(FIG, passage(LEO, "The phrase 'his fingers felt like frozen sticks' is an example of"), "a simile",
      ["a metaphor", "personification", "alliteration"], "It compares two things using 'like', which makes it a simile."),
    Q(INF, passage(LEO, "Why does his grandmother's nod help Leo?"),
      "It reminds him of playing for her at home, where he feels calm.",
      ["It tells him which piece to play.", "It shows she wants him to stop.", "It means the audience is leaving."],
      "The nod is 'the same nod she gave him every Sunday' in her kitchen, so it brings back the feeling of playing safely at home."),
    Q(TH, passage(LEO, "Which sentence best states a theme of the passage?"),
      "Support from someone you love can help you face your fears.",
      ["Practicing music is a waste of time.", "Music is more important than family.", "It is better to avoid performing in public."],
      "Leo's fear fades after he sees his grandmother's nod, and her proud smile is what he notices at the end."),
    Q(MI, passage(BEES, "What is the main idea of the passage?"),
      "Honeybees live and work together, and their work helps plants and people.",
      ["Queen bees are the most important bees.", "Bees have fuzzy bodies.", "Farmers grow fruits and vegetables."],
      "The passage describes how a colony works and then explains how bees' work helps plants grow food for people. The other choices are small details."),
    Q(KD, passage(BEES, "According to the passage, what do worker bees do?"),
      "They clean the hive, feed the young bees, and collect nectar and pollen.",
      ["They lay all the eggs.", "They grow fruits and vegetables.", "They plant new flowers."],
      "The passage lists the workers' jobs. Laying eggs is the queen's job."),
    Q(TS, passage(BEES, "How is the second half of the passage mainly organized?"), "cause and effect",
      ["compare and contrast", "the order of a bee's life", "question and answer"],
      "It explains a chain of causes and effects: bees carry pollen, which helps plants make fruit, which people depend on."),
    Q(VOC, passage(BEES, "In the passage, what does the word 'colonies' mean?"), "large groups that live together",
      ["kinds of flowers", "bee stings", "farms"], "The first sentence explains it: honeybees 'live in large groups called colonies.'"),
    Q(GR, "Which sentence uses the correct verb tense?", "Yesterday, we walked to the park.",
      ["Yesterday, we walk to the park.", "Yesterday, we will walk to the park.", "Yesterday, we walking to the park."],
      "'Yesterday' tells us the action is in the past, so the past tense 'walked' is correct."),
    Q(PU, "Which sentence uses commas correctly?", "We bought apples, bananas, and grapes.",
      ["We bought, apples bananas and grapes.", "We bought apples bananas, and, grapes.", "We, bought apples, bananas and grapes."],
      "Commas separate the items in a list: apples, bananas, and grapes."),
    Q(PU, "Which sentence correctly uses a comma after an introductory word?", "Yes, I would like to come.",
      ["Yes I, would like to come.", "Yes I would, like to come.", "Yes I would like, to come."],
      "An introductory word such as 'yes' is followed by a comma."),
    Q(GR, "Which word best completes the sentence? 'I wanted to play outside, ___ it was raining.'", "but", ["and", "so", "because"],
      "'But' shows a contrast between wanting to play outside and the rain stopping it."),
    Q(WP, "What does the prefix 'mis-' mean in the word 'misunderstand'?", "wrongly", ["again", "before", "very"],
      "'Mis-' means wrongly or badly, so 'misunderstand' means to understand wrongly."),
    Q(WP, "Which word means 'able to be seen'?", "visible", ["invisible", "vision", "visitor"],
      "The root 'vis' means see and the suffix '-ible' means able to be. 'Invisible' means not able to be seen."),
    Q(VOC, "Which word is closest in meaning to 'enormous'?", "huge", ["tiny", "noisy", "ancient"], "'Enormous' means very big, like 'huge'."),
    Q(VOC, "Which word is the opposite of 'generous'?", "selfish", ["kind", "giving", "friendly"],
      "A generous person shares; a selfish person does not."),
    Q(FIG, "'The wind whispered through the trees' is an example of", "personification", ["a simile", "hyperbole", "onomatopoeia"],
      "Whispering is something people do. Giving a human action to the wind is personification."),
    Q(FIG, "'I have told you a million times!' is an example of", "hyperbole", ["a simile", "personification", "a metaphor"],
      "Hyperbole is exaggeration for effect. Nobody has really said something a million times."),
    Q(GR, "Which of these is a complete sentence?", "The dog barked at the mail carrier.",
      ["Barking at the mail carrier.", "When the dog barked.", "The dog at the mail carrier."],
      "A complete sentence has a subject (the dog) and a verb (barked) and expresses a complete thought."),
    Q(SP, "Which word is spelled correctly?", "beautiful", ["beautifull", "beutiful", "beatiful"],
      "Beautiful: b-e-a-u-t-i-f-u-l, with one l at the end."),
])

# ═══ Grade 6 ELA ═══
CE, PV6, CL, CON, ROOT = "Citing evidence", "Point of view", "Claims & arguments", "Connotation", "Greek & Latin roots"
SNOW = """The trail had disappeared under fresh snow, and Priya's map was useless. Her brother, Dev, wanted to keep walking downhill. "Rivers run downhill," he said, "and the cabin is by the river." Priya wasn't sure. The light was fading, and every pine tree looked the same. She noticed, though, that the snow was thicker on the north side of the trunks, and she remembered her father saying the cabin faced the south slope. "We'll go your way," she told Dev, "but we keep the thick snow behind us." An hour later, a thin line of smoke rose above the trees."""
TABLETS = """Many schools are replacing paper textbooks with tablets. Supporters say tablets are lighter than a backpack full of books and can be updated instantly when information changes. They also point out that digital books can include videos and interactive quizzes. However, critics argue that screens can distract students, and some studies suggest people remember more when they read on paper. Tablets are also expensive to repair or replace. Before switching completely, schools should test tablets in a few classes and compare the results with paper books."""
save(6, "English Language Arts", "ela", [
    Q(INF, passage(SNOW, "What can you infer about Priya from the passage?"), "She stays calm and uses clues to solve problems.",
      ["She panics when things go wrong.", "She refuses to listen to her brother.", "She does not care about getting back."],
      "Even as the light fades, Priya notices the thicker snow on the north side of the trees and uses what her father said to choose a direction."),
    Q(PV6, passage(SNOW, "From which point of view is the passage told?"), "third person",
      ["first person", "second person", "Dev's point of view, in his own words"],
      "A narrator outside the story tells it using 'she' and 'her', so it is third person."),
    Q(CE, passage(SNOW, "Which detail best shows that the children reached the cabin?"), "a thin line of smoke rose above the trees",
      ["the trail had disappeared under fresh snow", "every pine tree looked the same", "Rivers run downhill"],
      "Smoke rising above the trees suggests a fire in the cabin's chimney, so they have found it."),
    Q(VOC, passage(SNOW, "In the passage, 'useless' most nearly means"), "of no help", ["very old", "torn", "too small"],
      "The trail was hidden under snow, so the map could no longer help them find the way."),
    Q(MI, passage(TABLETS, "What is the central idea of the passage?"),
      "Tablets have benefits and drawbacks, so schools should test them before switching completely.",
      ["Tablets are always better than paper books.", "Paper books should be banned.", "Tablets are too heavy for students."],
      "The passage gives both sides and ends with a recommendation to test first. The other choices go beyond what it says."),
    Q(CL, passage(TABLETS, "What does the author recommend?"), "Schools should try tablets in a few classes and compare the results.",
      ["Schools should buy tablets for every student now.", "Schools should never use tablets.", "Students should buy their own tablets."],
      "The last sentence gives the recommendation: test in a few classes and compare with paper books."),
    Q(TS, passage(TABLETS, "Which word signals that the author is turning to the other side of the argument?"), "However",
      ["Many", "also", "Before"], "'However' introduces the critics' view after the supporters' points."),
    Q(CE, passage(TABLETS, "Which reason do the critics give?"), "Screens can distract students.",
      ["Tablets can be updated instantly.", "Digital books can include videos.", "Tablets are lighter than books."],
      "The other three are reasons given by supporters."),
    Q(GR, "Choose the correct pronoun: 'Ms. Lee gave the tickets to Sam and ___.'", "me", ["I", "myself", "mine"],
      "After 'to', use the object pronoun 'me'. Test it alone: 'gave the tickets to me.'"),
    Q(GR, "Choose the correct pronoun: '___ and Ava are going to the game.'", "She", ["Her", "Hers", "Herself"],
      "The pronoun is part of the subject, so use the subject pronoun 'She'. Test it alone: 'She is going.'"),
    Q(PU, "Which sentence uses commas correctly?", "My uncle, who lives in Ohio, is visiting us.",
      ["My uncle who lives, in Ohio is visiting us.", "My uncle, who lives in Ohio is visiting us.", "My, uncle who lives in Ohio, is visiting us."],
      "'Who lives in Ohio' is extra information, so it needs a comma before and after it."),
    Q(ROOT, "The Greek root 'graph' means 'write'. Which word means 'a person's own written name'?", "autograph",
      ["paragraph", "graphic", "photograph"], "'Auto' means self, so an autograph is something written by the person themselves: their signature."),
    Q(ROOT, "The Latin root 'port' means 'carry'. What does 'portable' mean?", "easy to carry", ["able to see", "made of metal", "near the water"],
      "'Port' (carry) + '-able' (able to be) = able to be carried."),
    Q(CON, "Which word has the most negative connotation?", "stubborn", ["determined", "persistent", "committed"],
      "All four describe someone who does not give up, but 'stubborn' suggests being unreasonable, which is negative."),
    Q(VOC, "'The desert was arid; it had not rained there in months.' What does 'arid' mean?", "very dry",
      ["very cold", "crowded", "beautiful"], "The clue 'it had not rained there in months' shows that arid means very dry."),
    Q(FIG, "'Time is a thief' is an example of", "a metaphor", ["a simile", "alliteration", "onomatopoeia"],
      "It says time IS a thief, without 'like' or 'as', so it is a metaphor."),
    Q(GR, "Which sentence is written correctly?", "It started to rain, so we went inside.",
      ["It started to rain we went inside.", "It started to rain, we went inside.", "It started to rain so, we went inside."],
      "Two complete sentences joined with only a comma, or with nothing, make a run-on. A comma plus 'so' joins them correctly."),
    Q(GR, "Which sentence is clearest?", "When Mia met Jen at the station, Mia was late.",
      ["When Mia met Jen at the station, she was late.", "She was late when she met her at the station.", "When she met Jen, she was late for it."],
      "In the other sentences, 'she' could mean either girl. Repeating the name makes it clear who was late."),
    Q(SP, "Which word is spelled correctly?", "necessary", ["neccessary", "necesary", "neccesary"],
      "Necessary has one c and two s's: n-e-c-e-s-s-a-r-y."),
    Q(VOC, "Which word best completes the sentence? 'The tired hikers ___ up the last steep hill.'", "trudged",
      ["skipped", "raced", "floated"], "'Trudged' means walked slowly and heavily, which fits tired hikers on a steep hill."),
])

# ═══ Grade 7 ELA ═══
AP = "Author's purpose"
GARDEN = """Every summer, Grandpa Joe planted more tomatoes than any family could eat. Mom teased him about it, but each August he filled paper bags with the extra and walked them down the street: to Mrs. Ortiz, who had just lost her job; to the new family in the blue house; to the firefighters at Station 9. "A garden," he liked to say, "is not measured by what you keep." This year Grandpa's knees are too stiff for the walk, so I carry the bags. At every door, people ask about him, and I realize the garden has been growing something besides tomatoes all along."""
FARMS = """In 1900, about 40 percent of American workers were farmers. Today, fewer than 2 percent are. This change did not happen because Americans eat less food. Instead, machines such as tractors and combine harvesters allowed one farmer to do the work that once took dozens of people. Better seeds and fertilizers also increased how much food each acre could produce. As fewer workers were needed on farms, many people moved to cities to work in factories and offices. Today, the United States produces more food than ever with far fewer farmers."""
save(7, "English Language Arts", "ela", [
    Q(TH, passage(GARDEN, "Which sentence best states the theme of the passage?"), "Generosity builds connections between people.",
      ["Gardening is hard work.", "Tomatoes grow best in summer.", "Old age makes people lonely."],
      "Grandpa's gifts and his saying, 'a garden is not measured by what you keep', show that giving creates bonds with neighbors."),
    Q(FIG, passage(GARDEN, "What does the narrator mean by 'the garden has been growing something besides tomatoes'?"),
      "Grandpa's gifts have created friendships in the neighborhood.",
      ["Grandpa planted other vegetables too.", "Weeds are growing in the garden.", "The narrator wants to sell the tomatoes."],
      "People at every door ask about Grandpa: the 'something' the garden grew is the neighbors' care for him."),
    Q(INF, passage(GARDEN, "Why does Grandpa plant more tomatoes than his family can eat?"), "He plans to give the extra to his neighbors.",
      ["He does not know how many to plant.", "He wants to win a contest.", "He sells them at the market."],
      "Every August he fills bags with the extra and walks them down the street to neighbors."),
    Q(PV6, passage(GARDEN, "How does the narrator's role change by the end of the passage?"),
      "The narrator takes over Grandpa's tradition of sharing.",
      ["The narrator stops visiting the neighbors.", "The narrator starts teasing Grandpa.", "The narrator plants a garden alone."],
      "Grandpa can no longer make the walk, so the narrator now carries the bags."),
    Q(MI, passage(FARMS, "Which sentence best states the central idea?"),
      "Machines and better farming methods let far fewer farmers produce more food, changing where Americans work.",
      ["Americans eat less food than they did in 1900.", "Tractors were invented in 1900.", "Most Americans still work on farms."],
      "The passage explains why the number of farmers fell and what happened as a result. It says directly that Americans do not eat less."),
    Q(TS, passage(FARMS, "How does the author mainly organize the information?"), "by explaining the causes and effects of a change",
      ["by telling a story in the first person", "by comparing two different countries", "by listing the steps in a process"],
      "It describes a change (fewer farmers), its causes (machines, better seeds) and its effects (people moving to cities)."),
    Q(AP, passage(FARMS, "What is the author's main purpose?"), "to explain why the number of farmers fell",
      ["to persuade readers to become farmers", "to entertain readers with a story", "to describe how to drive a tractor"],
      "The passage gives information and reasons; it does not try to persuade or tell a story."),
    Q(CE, passage(FARMS, "Which sentence best supports the idea that farms became more productive?"),
      "Better seeds and fertilizers also increased how much food each acre could produce.",
      ["In 1900, about 40 percent of American workers were farmers.", "Many people moved to cities to work in factories and offices.",
       "This change did not happen because Americans eat less food."],
      "Producing more food from each acre is what 'more productive' means."),
    Q(GR, "Which sentence has a misplaced modifier?", "Covered in mud, Mom washed the dog.",
      ["Mom washed the dog, which was covered in mud.", "The dog, covered in mud, needed a bath.", "Mom washed the muddy dog."],
      "'Covered in mud' is placed next to 'Mom', so the sentence says Mom was covered in mud, not the dog."),
    Q(GR, "Which sentence is a complex sentence?", "Although it was late, we kept reading.",
      ["We kept reading.", "It was late, and we kept reading.", "We read and talked."],
      "A complex sentence has an independent clause and a dependent clause. 'Although it was late' cannot stand alone."),
    Q(GR, "In the sentence 'The girl with the red backpack won the race', what does 'with the red backpack' do?",
      "It tells which girl won.", ["It tells when the race happened.", "It is the main verb.", "It tells where the race took place."],
      "The prepositional phrase describes the noun 'girl', showing which girl is meant."),
    Q(PU, "Which sentence uses a semicolon correctly?", "I wanted to go; however, it was too late.",
      ["I wanted; to go however it was too late.", "I wanted to go however; it was too late.", "I; wanted to go, however it was too late."],
      "A semicolon joins two complete sentences. Before 'however' it is followed by a comma."),
    Q(PU, "Which sentence is punctuated correctly?", "It was a fascinating, enjoyable movie.",
      ["It was a fascinating enjoyable, movie.", "It was a, fascinating enjoyable movie.", "It was, a fascinating enjoyable movie."],
      "Two adjectives that each describe the noun equally are separated by a comma, but no comma goes before the noun."),
    Q(CON, "Which word suggests that a home is small in a pleasant way?", "cozy", ["cramped", "tiny", "crowded"],
      "'Cozy' suggests small and comfortable. 'Cramped' and 'crowded' suggest too small."),
    Q(ROOT, "The Latin root 'bene' means 'good' or 'well'. Which word means 'something that helps'?", "benefit",
      ["beneath", "bench", "bandage"], "A benefit is something good that helps you. 'Beneath' and 'bench' only look similar."),
    Q(VOC, "'The speech was so verbose that the audience grew restless waiting for it to end.' What does 'verbose' mean?",
      "using too many words", ["very funny", "angry", "hard to hear"],
      "The clue is that the audience grew restless waiting for it to end: the speech went on too long."),
    Q(FIG, "Which line contains alliteration?", "Silent snowflakes settled softly.",
      ["The snow fell during the night.", "Snow covered the town like a blanket.", "The snow was a white sea."],
      "Alliteration repeats the same first sound in nearby words: silent, snowflakes, settled, softly."),
    Q(GR, "Which sentence is the most concise?", "We postponed the meeting until Friday.",
      ["We made the decision to postpone the meeting and move it to Friday instead.",
       "The meeting was postponed by us and moved until the day of Friday.",
       "We decided that we would postpone, until Friday, the meeting."],
      "It says the same thing in the fewest words, without repetition."),
    Q(SP, "Which word is spelled correctly?", "occurrence", ["occurence", "ocurrence", "occurrance"],
      "Occurrence has double c, double r, and ends in -ence."),
    Q(GR, "Which sentence shows correct subject–verb agreement?", "Each of the students has a locker.",
      ["Each of the students have a locker.", "Each of the students are having a locker.", "Each of the students have their lockers each."],
      "The subject is 'each', which is singular, so it takes the singular verb 'has'."),
])
