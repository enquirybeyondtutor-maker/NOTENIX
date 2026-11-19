r"""Notenix Ontario (Grades 5-7): the six baseline tests, Math (2020 Ontario Mathematics curriculum:
Number, Algebra incl. coding, Data incl. probability, Spatial Sense, Financial Literacy) and Language.
Writes tests/on<grade>-baseline-<math|language>.json. Original questions, Canadian spelling, metric units.
Run from this folder: python make_on_baselines.py

Plain text only (no LaTeX): prices use "$", which the app's maths renderer would otherwise try to read.
"""
import json
import math
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
    pos = [1, 3, 0, 2, 2, 0, 3, 1][_slot[0] % 8]
    _slot[0] += 1
    opts = list(wrongs)
    opts.insert(pos, correct)
    return {"topic": topic, "question": question.strip(), "options": opts, "answer": correct,
            "explanation": explanation.strip()}


def passage(text, ask):
    return f'Read the passage.\n\n"{text.strip()}"\n\n{ask}'


def save(grade, subject, key, questions):
    assert len(questions) == 20, (grade, subject, len(questions))
    t = {"slot": f"on{grade}-baseline", "subject": subject, "title": f"Grade {grade} {subject} Baseline",
         "topic": "Baseline", "duration": 30, "level": f"Grade {grade}", "board": "Ontario curriculum",
         "questions": questions}
    for q in questions:
        for s in [q["question"], q["explanation"], *q["options"]]:
            assert not MATH.search(s), f"would render as maths: {s[:80]}"
    (HERE / "tests" / f"on{grade}-baseline-{key}.json").write_text(
        json.dumps(t, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"on{grade}-baseline-{key}: {len(questions)} questions")


NUM, ALG, COD, DAT, SPA, FIN = "Number", "Algebra", "Coding", "Data & probability", "Spatial sense", "Financial literacy"

# ═══ Grade 5 Math ═══
save(5, "Math", "math", [
    Q(NUM, "What is the value of the digit 4 in 54 312?", "4 000", ["400", "40 000", "40"],
      "54 312 is 5 ten thousands, 4 thousands, 3 hundreds, 1 ten and 2 ones."),
    Q(NUM, "Round 68 471 to the nearest thousand.", "68 000", ["69 000", "68 500", "70 000"],
      "Look at the hundreds digit: 4 is less than 5, so round down to 68 000."),
    Q(NUM, "Which decimal is equal to 7/10?", "0.7", ["0.07", "7.1", "0.17"], "7 tenths is written 0.7. 0.07 is 7 hundredths.",
      check=lambda: F("0.7") == F(7, 10)),
    Q(NUM, "Which fraction is equivalent to 3/4?", "9/12", ["6/12", "3/8", "4/3"],
      "Multiply the top and bottom by 3: 3/4 = 9/12. 6/12 is equal to 1/2.", check=lambda: F(9, 12) == F(3, 4)),
    Q(NUM, "What is 245 × 6?", "1 470", ["1 270", "1 450", "1 520"], "200 × 6 = 1 200, 40 × 6 = 240, 5 × 6 = 30. 1 200 + 240 + 30 = 1 470.",
      check=lambda: 245 * 6 == 1470),
    Q(NUM, "What is 936 ÷ 4?", "234", ["224", "233", "244"], "900 ÷ 4 = 225 and 36 ÷ 4 = 9, so 936 ÷ 4 = 234.", check=lambda: 936 / 4 == 234),
    Q(NUM, "A box holds 12 granola bars. How many boxes are needed to pack 150 granola bars?", "13 boxes",
      ["12 boxes", "15 boxes", "18 boxes"], "150 ÷ 12 = 12 remainder 6. The 6 leftover bars need another box, so 13 boxes.",
      check=lambda: math.ceil(150 / 12) == 13),
    Q(NUM, "What is 3.45 + 2.7?", "6.15", ["5.52", "6.42", "3.72"], "Line up the decimal points: 3.45 + 2.70 = 6.15.",
      check=lambda: F("3.45") + F("2.7") == F("6.15")),
    Q(ALG, "A pattern starts 4, 9, 14, 19, … and keeps adding the same amount. What is the 10th term?", "49", ["44", "50", "54"],
      "The pattern adds 5 each time. The 10th term is 4 + 9 × 5 = 49.", check=lambda: 4 + 9 * 5 == 49),
    Q(ALG, "What value of n makes 6 × n = 42 true?", "7", ["6", "36", "48"], "6 × 7 = 42, so n = 7.", check=lambda: 6 * 7 == 42),
    Q(ALG, "What value of m makes m + 18 = 50 true?", "32", ["68", "22", "34"], "Subtract 18 from 50: m = 32.", check=lambda: 32 + 18 == 50),
    Q(COD, "A program sets x = 3. It then repeats the instruction 'add 4 to x' three times. What is x at the end?", "15",
      ["7", "12", "19"], "x goes 3 → 7 → 11 → 15.", check=lambda: 3 + 3 * 4 == 15),
    Q(DAT, "What is the mode of this data set: 2, 8, 8, 3, 10, 6?", "8", ["7", "6", "10"],
      "The mode is the value that appears most often. 8 appears twice; every other value appears once."),
    Q(DAT, "What is the mean of 12, 15, 9 and 14?", "12.5", ["12", "13", "50"],
      "Add the values (50) and divide by how many there are (4): 50 ÷ 4 = 12.5.", check=lambda: (12 + 15 + 9 + 14) / 4 == 12.5),
    Q(DAT, "A spinner has 8 equal sections: 3 red, 4 blue and 1 yellow. What is the probability of landing on blue?", "1/2",
      ["3/8", "1/8", "1/4"], "4 of the 8 equal sections are blue: 4/8 = 1/2.", check=lambda: F(4, 8) == F(1, 2)),
    Q(SPA, "A parallelogram has a base of 8 cm and a height of 5 cm. What is its area?", "40 cm²", ["20 cm²", "13 cm²", "26 cm²"],
      "Area of a parallelogram = base × height = 8 × 5 = 40 cm².", check=lambda: 8 * 5 == 40),
    Q(SPA, "A triangle has a base of 12 m and a height of 7 m. What is its area?", "42 m²", ["84 m²", "19 m²", "38 m²"],
      "Area of a triangle = base × height ÷ 2 = 12 × 7 ÷ 2 = 42 m².", check=lambda: 12 * 7 / 2 == 42),
    Q(SPA, "What is a triangle with three sides of different lengths called?", "scalene", ["isosceles", "equilateral", "right"],
      "Scalene: no equal sides. Isosceles: at least two equal sides. Equilateral: three equal sides."),
    Q(SPA, "How many millilitres are in 2.5 L?", "2 500", ["250", "25", "25 000"], "1 L = 1 000 mL, so 2.5 L = 2 500 mL.",
      check=lambda: F("2.5") * 1000 == 2500),
    Q(FIN, "Maya buys 3 notebooks at $2.75 each and a pen for $1.40. She pays with a $20 bill. How much change does she get?",
      "$10.35", ["$9.65", "$11.35", "$10.65"], "The notebooks cost 3 × 2.75 = 8.25 dollars. With the pen: 8.25 + 1.40 = 9.65 dollars. Change: 20.00 − 9.65 = 10.35 dollars.",
      check=lambda: 20 - (3 * F("2.75") + F("1.40")) == F("10.35")),
])

# ═══ Grade 6 Math ═══
save(6, "Math", "math", [
    Q(NUM, "Which list is in order from least to greatest?", "0.407, 0.45, 0.457, 0.46",
      ["0.46, 0.457, 0.45, 0.407", "0.45, 0.407, 0.46, 0.457", "0.407, 0.457, 0.45, 0.46"],
      "Compare place by place: 0.407 < 0.450 < 0.457 < 0.460.", check=lambda: sorted([0.46, 0.457, 0.45, 0.407]) == [0.407, 0.45, 0.457, 0.46]),
    Q(NUM, "What is 3/8 written as a percent?", "37.5%", ["38%", "3.8%", "83%"], "3 ÷ 8 = 0.375, which is 37.5%.",
      check=lambda: F(3, 8) == F("0.375")),
    Q(NUM, "What is 25% of 360?", "90", ["36", "72", "120"], "25% is one quarter: 360 ÷ 4 = 90.", check=lambda: 360 / 4 == 90),
    Q(NUM, "A juice mix uses 2 parts concentrate to 5 parts water. How much water goes with 6 cups of concentrate?", "15 cups",
      ["9 cups", "12 cups", "30 cups"], "6 cups is 3 times 2 cups, so use 3 times 5 cups of water: 15 cups.", check=lambda: F(5, 2) * 6 == 15),
    Q(NUM, "A car uses 6 L of fuel to travel 100 km. At the same rate, how much fuel does it use to travel 350 km?", "21 L",
      ["18 L", "24 L", "35 L"], "350 km is 3.5 times 100 km, so the car uses 3.5 × 6 = 21 L.", check=lambda: F(6, 100) * 350 == 21),
    Q(NUM, "Which temperature is the warmest?", "−3°C", ["−8°C", "−12°C", "−5°C"],
      "On a number line, −3 is furthest to the right of these numbers, so it is the greatest (warmest).",
      check=lambda: max([-3, -8, -12, -5]) == -3),
    Q(NUM, "What is 4.8 × 3?", "14.4", ["12.4", "14.8", "1.44"], "4 × 3 = 12 and 0.8 × 3 = 2.4, so the product is 14.4.",
      check=lambda: F("4.8") * 3 == F("14.4")),
    Q(NUM, "What is 7.2 ÷ 0.9?", "8", ["0.8", "6.3", "80"], "Multiply both numbers by 10: 72 ÷ 9 = 8.", check=lambda: F("7.2") / F("0.9") == 8),
    Q(ALG, "What is the value of 5a − 4 when a = 6?", "26", ["2", "30", "52"], "5a means 5 × a = 30, and 30 − 4 = 26.",
      check=lambda: 5 * 6 - 4 == 26),
    Q(ALG, "Solve 3k = 27.", "k = 9", ["k = 24", "k = 30", "k = 81"], "Divide both sides by 3: k = 9.", check=lambda: 3 * 9 == 27),
    Q(ALG, "Which value of y makes y + 4 < 10 true?", "y = 5", ["y = 6", "y = 7", "y = 10"],
      "y + 4 < 10 means y < 6. Of the choices, only 5 is less than 6.", check=lambda: 5 + 4 < 10 and not 6 + 4 < 10),
    Q(COD, "A program sets total = 3. A loop runs 4 times, and each time it doubles total. What is total at the end?", "48",
      ["11", "24", "96"], "3 → 6 → 12 → 24 → 48.", check=lambda: 3 * 2 ** 4 == 48),
    Q(DAT, "What is the median of 14, 9, 25, 9 and 18?", "14", ["9", "15", "25"],
      "In order: 9, 9, 14, 18, 25. The middle value is 14. (The mean is 15 and the mode is 9.)",
      check=lambda: sorted([14, 9, 25, 9, 18])[2] == 14 and sum([14, 9, 25, 9, 18]) / 5 == 15),
    Q(DAT, "A number cube numbered 1 to 6 is rolled 60 times. About how many times would you expect to roll a 4?", "10",
      ["4", "6", "15"], "The probability of a 4 is 1/6, and 1/6 of 60 is 10.", check=lambda: F(1, 6) * 60 == 10),
    Q(SPA, "An L-shaped garden is made of a 6 m by 4 m rectangle joined to a 3 m by 2 m rectangle. What is its total area?",
      "30 m²", ["24 m²", "15 m²", "36 m²"], "6 × 4 = 24 m² and 3 × 2 = 6 m². Together: 30 m².", check=lambda: 6 * 4 + 3 * 2 == 30),
    Q(SPA, "What is the volume of a rectangular prism that measures 6 cm by 5 cm by 2 cm?", "60 cm³", ["13 cm³", "104 cm³", "30 cm³"],
      "Volume = length × width × height = 6 × 5 × 2 = 60 cm³. (104 cm² would be its surface area.)", check=lambda: 6 * 5 * 2 == 60),
    Q(SPA, "Two angles together make a straight line. One of them is 128°. What is the other?", "52°", ["62°", "232°", "38°"],
      "Angles on a straight line add up to 180°: 180 − 128 = 52°.", check=lambda: 180 - 128 == 52),
    Q(SPA, "How many centimetres are in 4.25 m?", "425", ["42.5", "4 250", "4.25"], "1 m = 100 cm, so 4.25 m = 425 cm.",
      check=lambda: F("4.25") * 100 == 425),
    Q(FIN, "Sam puts $500 in a savings account that pays 3% simple interest per year. How much interest does he earn in 2 years?",
      "$30", ["$15", "$3", "$530"], "3% of 500 dollars is 15 dollars a year, so 2 years earn 30 dollars of interest.",
      check=lambda: 500 * F(3, 100) * 2 == 30),
    Q(FIN, "Which of these is the best buy (lowest price per litre)?", "4 L of milk for $8.60",
      ["2 L of milk for $4.40", "1 L of milk for $2.29", "500 mL of milk for $1.15"],
      "Per litre: 8.60 ÷ 4 = 2.15, 4.40 ÷ 2 = 2.20, 2.29, and 1.15 × 2 = 2.30 dollars. The 4 L jug is cheapest per litre.",
      check=lambda: min(F("8.60") / 4, F("4.40") / 2, F("2.29"), F("1.15") * 2) == F("8.60") / 4),
])

# ═══ Grade 7 Math ═══
save(7, "Math", "math", [
    Q(NUM, "What is −7 + (−5)?", "−12", ["2", "−2", "12"], "Adding a negative moves further left: −7 − 5 = −12.", check=lambda: -7 + -5 == -12),
    Q(NUM, "What is −24 ÷ 6?", "−4", ["4", "−18", "−30"], "A negative divided by a positive is negative: −24 ÷ 6 = −4.", check=lambda: -24 / 6 == -4),
    Q(NUM, "What is 2/3 × 9/10?", "3/5", ["11/13", "20/27", "6/5"], "Multiply tops and bottoms: 18/30, which simplifies to 3/5.",
      check=lambda: F(2, 3) * F(9, 10) == F(3, 5)),
    Q(NUM, "What is the square root of 144?", "12", ["72", "14", "24"], "12 × 12 = 144.", check=lambda: 12 * 12 == 144),
    Q(NUM, "What is 5² + 3²?", "34", ["64", "16", "30"], "5² = 25 and 3² = 9, so the sum is 34. (8² = 64 is a common mistake.)",
      check=lambda: 5 ** 2 + 3 ** 2 == 34),
    Q(FIN, "HST in Ontario is 13%. A jacket costs $80 before tax. What is the total cost with HST?", "$90.40",
      ["$10.40", "$93.00", "$81.30"], "13% of 80 dollars is 10.40 dollars, so the total is 80 + 10.40 = 90.40 dollars.",
      check=lambda: 80 * F(113, 100) == F("90.40")),
    Q(FIN, "A shirt that costs $45 is 20% off. What is the sale price?", "$36", ["$9", "$25", "$40"],
      "20% of 45 dollars is 9 dollars, so the sale price is 45 − 9 = 36 dollars.", check=lambda: 45 * F(4, 5) == 36),
    Q(NUM, "Four concert tickets cost $58. At the same price, how much do 7 tickets cost?", "$101.50",
      ["$87.00", "$116.00", "$94.50"], "One ticket costs 58 ÷ 4 = 14.50 dollars, so 7 tickets cost 7 × 14.50 = 101.50 dollars.",
      check=lambda: F(58, 4) * 7 == F("101.50")),
    Q(ALG, "Solve 4x + 9 = 37.", "x = 7", ["x = 6.5", "x = 11.5", "x = 28"], "Subtract 9: 4x = 28. Divide by 4: x = 7.",
      check=lambda: 4 * 7 + 9 == 37),
    Q(ALG, "Which expression is equivalent to 3(2y − 5) + 4y?", "10y − 15", ["10y − 5", "6y − 15", "10y + 15"],
      "3(2y − 5) = 6y − 15, and 6y + 4y = 10y, giving 10y − 15.", check=lambda: all(3 * (2 * y - 5) + 4 * y == 10 * y - 15 for y in range(-5, 6))),
    Q(ALG, "Solve x/3 − 2 = 5.", "x = 21", ["x = 3", "x = 9", "x = 15"], "Add 2: x/3 = 7. Multiply by 3: x = 21.",
      check=lambda: F(21, 3) - 2 == 5),
    Q(ALG, "Which describes all the values of n for which 2n + 1 > 11?", "n > 5", ["n < 5", "n > 6", "n > 11"],
      "Subtract 1: 2n > 10. Divide by 2: n > 5.", check=lambda: all((2 * n + 1 > 11) == (n > 5) for n in range(-10, 20))),
    Q(SPA, "A circle has a diameter of 14 cm. Using 3.14 for π, what is its circumference?", "43.96 cm",
      ["21.98 cm", "153.86 cm", "87.92 cm"], "Circumference = π × diameter = 3.14 × 14 = 43.96 cm.", check=lambda: F("3.14") * 14 == F("43.96")),
    Q(SPA, "A circle has a radius of 3 m. Using 3.14 for π, what is its area?", "28.26 m²", ["18.84 m²", "9.42 m²", "113.04 m²"],
      "Area = π × r × r = 3.14 × 9 = 28.26 m². (18.84 m would be its circumference.)", check=lambda: F("3.14") * 9 == F("28.26")),
    Q(SPA, "What is the surface area of a cube with edges of 4 cm?", "96 cm²", ["64 cm²", "16 cm²", "48 cm²"],
      "Each face is 4 × 4 = 16 cm², and a cube has 6 faces: 6 × 16 = 96 cm². (64 cm³ is its volume.)", check=lambda: 6 * 16 == 96),
    Q(SPA, "Two angles of a triangle measure 47° and 68°. What is the third angle?", "65°", ["115°", "75°", "245°"],
      "The angles of a triangle add up to 180°: 180 − 47 − 68 = 65°.", check=lambda: 180 - 47 - 68 == 65),
    Q(SPA, "On a floor plan, 1 cm represents 2.5 m. A room is 6 cm long on the plan. How long is the real room?", "15 m",
      ["8.5 m", "12 m", "2.4 m"], "Each centimetre stands for 2.5 m: 6 × 2.5 = 15 m.", check=lambda: 6 * F("2.5") == 15),
    Q(DAT, "A coin is flipped and a number cube (1 to 6) is rolled. What is the probability of getting heads and a 6?", "1/12",
      ["1/8", "2/3", "1/6"], "The events are independent: 1/2 × 1/6 = 1/12.", check=lambda: F(1, 2) * F(1, 6) == F(1, 12)),
    Q(DAT, "A coin was flipped 50 times and landed heads 22 times. What is the experimental probability of heads?", "11/25",
      ["1/2", "14/25", "11/50"], "Experimental probability = 22/50, which simplifies to 11/25. (1/2 is the theoretical probability.)",
      check=lambda: F(22, 50) == F(11, 25)),
    Q(NUM, "At 6 a.m. it was −6°C. The temperature rose 4°C, then fell 9°C. What was the final temperature?", "−11°C",
      ["7°C", "−1°C", "−19°C"], "−6 + 4 = −2, and −2 − 9 = −11°C.", check=lambda: -6 + 4 - 9 == -11),
])

# ═══ Language ═══
MI, INF, TH, FIG, VOC, KD, TS, GR, PU, WP, SP, PV, CE, CL, CON, AP = (
    "Main idea", "Inference", "Theme", "Figurative language", "Vocabulary", "Key details", "Text structure",
    "Grammar & usage", "Punctuation", "Word parts", "Spelling", "Point of view", "Citing evidence",
    "Claims & arguments", "Connotation", "Author's purpose")

CANOE = """Noor had never paddled a canoe before the class trip to Algonquin Park. On the first morning, her paddle kept slipping, and the canoe turned in slow circles while the others glided ahead. Her partner, Ben, laughed, but not unkindly. "Watch the water, not your paddle," he said. Noor tried it. She pulled the paddle back in long, steady strokes and felt the canoe straighten like an arrow. By the afternoon, she was the one calling out the rhythm. When the group stopped for lunch on a rocky island, the teacher asked who wanted to steer the next day. Noor's hand shot up before she had time to think."""
TOWER = """The CN Tower in Toronto was finished in 1976. At 553 metres, it was the tallest free-standing structure in the world for more than 30 years. It was built mainly to send television and radio signals, because new skyscrapers in the city were blocking the signals from shorter towers. Today, the tower still broadcasts signals, but it is also one of Canada's most popular tourist attractions. Visitors can ride glass-fronted elevators to a lookout, stand on a glass floor 342 metres above the ground, or even walk around the outside of the tower while attached to a safety harness."""
save(5, "Language", "language", [
    Q(INF, passage(CANOE, "How has Noor changed by the end of the passage?"), "She has become confident in the canoe.",
      ["She wants to go home early.", "She is angry with Ben.", "She has decided she dislikes canoeing."],
      "At first the canoe turns in circles, but by the end she calls out the rhythm and volunteers to steer."),
    Q(FIG, passage(CANOE, "The phrase 'the canoe straighten like an arrow' is an example of"), "a simile",
      ["a metaphor", "personification", "onomatopoeia"], "It compares the canoe's path to an arrow using 'like', so it is a simile."),
    Q(KD, passage(CANOE, "What advice helps Noor paddle better?"), "Watch the water instead of the paddle.",
      ["Paddle as fast as possible.", "Let Ben do all the paddling.", "Stop and rest on the island."],
      "Ben tells her, 'Watch the water, not your paddle,' and then she paddles in long, steady strokes."),
    Q(TH, passage(CANOE, "Which sentence best states a theme of the passage?"), "With patience and good advice, a new skill can be learned.",
      ["Canoe trips are too difficult for beginners.", "It is better to work alone than with a partner.", "Teachers should always choose who steers."],
      "Noor struggles, takes Ben's advice, keeps trying and ends up confident."),
    Q(MI, passage(TOWER, "What is the main idea of the passage?"),
      "The CN Tower was built to broadcast signals and is now also a major tourist attraction.",
      ["The CN Tower has a glass floor.", "Skyscrapers block television signals.", "Toronto has many tall buildings."],
      "The passage explains why the tower was built and what it is used for today. The other choices are single details."),
    Q(KD, passage(TOWER, "According to the passage, why was the CN Tower built?"),
      "New skyscrapers were blocking signals from shorter towers.",
      ["Tourists wanted a place to see the city.", "Toronto needed a new safety harness.", "It was a contest to build the tallest tower."],
      "The passage says it was built mainly to send signals, because new skyscrapers were blocking signals from shorter towers."),
    Q(VOC, passage(TOWER, "In the passage, 'free-standing' most likely means"),
      "standing up by itself, without being held up by other buildings", ["free for visitors to enter", "very old", "made of glass"],
      "A free-standing structure supports itself; it is not attached to or held up by something else."),
    Q(TS, passage(TOWER, "How is the passage mostly organized?"), "It describes the tower's past and then its present.",
      ["It compares the CN Tower with other towers in Canada.", "It gives step-by-step instructions.", "It is a story told by one visitor."],
      "It starts with when and why the tower was built, then moves to how it is used 'today'."),
    Q(SP, "Which word uses Canadian spelling?", "colour", ["color", "coulour", "collor"],
      "Canadian spelling keeps the -our ending in words like colour, neighbour and favourite."),
    Q(GR, "Which sentence uses the correct verb tense?", "Last winter, we skated on the canal.",
      ["Last winter, we skate on the canal.", "Last winter, we will skate on the canal.", "Last winter, we skating on the canal."],
      "'Last winter' tells us the action happened in the past, so use the past tense 'skated'."),
    Q(PU, "Which sentence uses commas correctly?", "Lucas, Priya, and Sam ran to the bus.",
      ["Lucas Priya, and, Sam ran to the bus.", "Lucas, Priya and, Sam ran to the bus.", "Lucas Priya and Sam, ran to the bus."],
      "Commas separate the names in a list. No comma goes between the subject and the verb."),
    Q(PU, "Which sentence is punctuated correctly?", "\"Can we go now?\" asked Mia.",
      ["\"Can we go now\" asked Mia?", "\"Can we go now,\" asked Mia?", "Can we go now? \"asked Mia.\""],
      "The question mark belongs inside the quotation marks, right after the words Mia said."),
    Q(WP, "What does the prefix 're-' mean in the word 'rebuild'?", "again", ["not", "before", "wrongly"],
      "'Re-' means again, so 'rebuild' means to build again."),
    Q(WP, "What does the suffix '-less' mean in the word 'fearless'?", "without", ["full of", "more", "able to"],
      "'-less' means without, so 'fearless' means without fear."),
    Q(VOC, "Which word is closest in meaning to 'rapid'?", "fast", ["calm", "heavy", "careful"], "'Rapid' means very quick, like 'fast'."),
    Q(GR, "Which sentence uses 'their' correctly?", "The students packed their bags.",
      ["Their going to the park.", "Put the books over their.", "Their is a game tonight."],
      "'Their' shows belonging. The others need 'they're' (they are) or 'there' (a place)."),
    Q(FIG, "'The thunder grumbled in the distance' is an example of", "personification", ["a simile", "hyperbole", "alliteration"],
      "Grumbling is something people do. Giving a human action to thunder is personification."),
    Q(GR, "Which of these is a compound sentence?", "It was snowing, but we walked to school.",
      ["We walked to school.", "Walking to school in the snow.", "Because it was snowing."],
      "A compound sentence joins two complete sentences with a joining word such as 'but'."),
    Q(GR, "In the sentence 'The happy dog chased the ball', which word is an adjective?", "happy", ["dog", "chased", "ball"],
      "An adjective describes a noun. 'Happy' describes the dog."),
    Q(SP, "Which word is spelled correctly?", "neighbour", ["neighbur", "nieghbour", "naybour"],
      "Neighbour: n-e-i-g-h-b-o-u-r, with 'ei' and the Canadian -our ending."),
])

STORM = """The power had been out for two days after the ice storm, and Grandma's farmhouse was so cold that Theo could see his breath. At first he complained about everything: no internet, no hot shower, nothing to do. Then Grandma handed him a deck of cards and taught him a game her father used to play. They ate soup heated on the wood stove and told stories by lantern light. On the third evening, when the lights flickered back on and the furnace roared to life, Theo realized he was a little disappointed."""
BLOWERS = """Some people say Canadian cities should ban gas-powered leaf blowers. Supporters point out that the machines are loud, and that their small engines release a surprising amount of pollution for their size. Rakes, they argue, are quiet, cheap and good exercise. Landscaping companies disagree. They say leaf blowers let workers clear large areas quickly, which keeps costs down for homeowners. A sensible approach would be to ban gas-powered blowers in residential areas while still allowing quieter electric models."""
save(6, "Language", "language", [
    Q(INF, passage(STORM, "Why is Theo 'a little disappointed' when the power comes back?"),
      "He has come to enjoy his time with Grandma without electricity.",
      ["He wanted the house to stay cold.", "He is tired of playing on the internet.", "The furnace is too loud for him."],
      "After the cards, soup and stories by lantern light, he no longer minds the outage; the return of power ends that time."),
    Q(TH, passage(STORM, "How does Theo change during the passage?"), "He goes from complaining to appreciating simple activities.",
      ["He goes from happy to angry.", "He stops talking to Grandma.", "He learns how to fix the furnace."],
      "At first he complains about everything, but by the end he is sorry the quiet time is over."),
    Q(CE, passage(STORM, "Which detail best shows how cold the farmhouse was?"), "Theo could see his breath",
      ["They ate soup heated on the wood stove", "Grandma handed him a deck of cards", "they told stories by lantern light"],
      "Seeing your breath indoors shows the air is very cold."),
    Q(PV, passage(STORM, "From which point of view is the passage told?"), "third person",
      ["first person", "second person", "Grandma's point of view, in her own words"],
      "A narrator outside the story uses 'he' and 'Theo', so it is third person."),
    Q(MI, passage(BLOWERS, "What is the central idea of the passage?"),
      "There are arguments on both sides, so cities should ban gas blowers in neighbourhoods but allow electric ones.",
      ["Leaf blowers should be banned everywhere.", "Rakes are better exercise than leaf blowers.", "Landscaping companies charge too much."],
      "The passage gives both sides and ends with a compromise."),
    Q(CL, passage(BLOWERS, "What does the author recommend?"), "Ban gas-powered blowers in residential areas but allow electric ones.",
      ["Ban all leaf blowers, including electric ones.", "Make homeowners rake their own leaves.", "Allow gas-powered blowers everywhere."],
      "The last sentence gives the author's recommendation."),
    Q(CE, passage(BLOWERS, "Which reason do landscaping companies give?"), "Leaf blowers clear large areas quickly, keeping costs down.",
      ["Leaf blowers are quiet.", "Rakes are good exercise.", "Small engines cause a lot of pollution."],
      "The other three are points made by supporters of a ban."),
    Q(VOC, passage(BLOWERS, "In the passage, 'residential areas' are places where"), "people live", ["people work in factories", "farms grow crops", "parks are kept"],
      "'Residential' comes from 'reside', which means to live somewhere."),
    Q(GR, "Choose the correct pronoun: 'The coach gave Amir and ___ a ride home.'", "me", ["I", "myself", "mine"],
      "Test it alone: 'The coach gave me a ride.' Use the object pronoun 'me'."),
    Q(GR, "Choose the correct verb: 'The box of crayons ___ on the shelf.'", "is", ["are", "were", "be"],
      "The subject is 'box', which is singular, so it takes 'is'. 'Of crayons' just describes the box."),
    Q(PU, "Which sentence uses commas correctly?", "My cousin, a nurse in Ottawa, is visiting us.",
      ["My cousin a nurse, in Ottawa is visiting us.", "My cousin, a nurse in Ottawa is visiting us.", "My, cousin a nurse in Ottawa, is visiting us."],
      "'A nurse in Ottawa' renames 'my cousin', so it needs a comma before and after it."),
    Q(WP, "The Latin root 'aqua' means 'water'. Which word means 'a tank where fish are kept'?", "aquarium",
      ["aquatic", "aqueduct", "aquamarine"], "An aquarium is a water tank for fish. Aquatic means living in water; an aqueduct carries water."),
    Q(WP, "The Greek root 'tele' means 'far'. What is a telescope?", "a tool for seeing things that are far away",
      ["a tool for writing", "a kind of telephone", "a machine for measuring heat"], "'Tele' (far) + 'scope' (look at)."),
    Q(CON, "Which word gives the most positive description of someone who is careful with money?", "thrifty",
      ["cheap", "stingy", "miserly"], "All four describe spending little, but 'thrifty' praises it; the others suggest meanness."),
    Q(VOC, "'The lake was so placid that it reflected the trees like a mirror.' What does 'placid' mean?", "calm and still",
      ["deep and cold", "dirty", "crowded"], "A lake can only reflect like a mirror when its surface is calm and still."),
    Q(FIG, "'The classroom was a zoo after the fire drill' is an example of", "a metaphor", ["a simile", "onomatopoeia", "alliteration"],
      "It says the classroom WAS a zoo, without 'like' or 'as', so it is a metaphor."),
    Q(GR, "Which sentence is written correctly?", "The bus was late; we missed the first class.",
      ["The bus was late we missed the first class.", "The bus was late, we missed the first class.", "The bus was late we, missed the first class."],
      "Two complete sentences can be joined with a semicolon. With only a comma or nothing, they make a run-on."),
    Q(PU, "Which shows that leashes belong to more than one dog?", "the dogs' leashes", ["the dog's leashes", "the dogs leashes", "the dogs's leashes"],
      "For a plural noun ending in s, add the apostrophe after the s: dogs'."),
    Q(SP, "Which word is spelled correctly?", "favourite", ["favorit", "favourate", "faverite"],
      "Favourite: f-a-v-o-u-r-i-t-e, with the Canadian -our."),
    Q(VOC, "Which word best completes the sentence? 'The audience ___ when the magician vanished.'", "gasped",
      ["yawned", "slept", "shrugged"], "'Gasped' shows surprise, which fits a magician suddenly vanishing."),
])

ROOM = """My sister Leila left for university in Montreal at the end of August. For years we had shared a bedroom, and I had dreamed of having it to myself. Now the room was mine, and it was too quiet. Her side of the closet held only empty hangers that rattled whenever I opened the door. I moved my desk to the window, where she used to read, and found a note taped underneath it in her handwriting: "Your turn to keep the plants alive." I looked at the three dusty pots on the sill and, for the first time in a week, I laughed. Then I went to find the watering can."""
NORTH = """Canada's three territories cover about 40 percent of the country's land, yet fewer than 130 000 people live there. The climate explains much of this. Winters are long and extremely cold, and in many areas the ground stays frozen all year in a layer called permafrost. Building roads and houses on permafrost is difficult, because heat from buildings can thaw the ground and make it unstable. As the climate warms, however, permafrost is thawing in some places on its own, damaging roads and buildings that were built decades ago."""
save(7, "Language", "language", [
    Q(TH, passage(ROOM, "Which sentence best states the theme of the passage?"),
      "Even when a change is hard, small connections with people we love can help us adjust.",
      ["Having your own room is always better.", "Plants are difficult to keep alive.", "University is too far from home."],
      "The narrator misses Leila, but her note and the plants give the narrator a way to feel close to her and move forward."),
    Q(INF, passage(ROOM, "Why does the narrator say the room was 'too quiet'?"), "The narrator misses having Leila there.",
      ["The neighbours had moved away.", "The narrator's radio was broken.", "The window was always closed."],
      "The narrator had wanted the room alone, but now notices the emptiness Leila left behind."),
    Q(FIG, passage(ROOM, "What do the plants most likely represent in the passage?"),
      "a way for the narrator to stay connected to Leila and take on her role",
      ["the narrator's wish to become a gardener", "the cold weather in Montreal", "the narrator's anger at Leila"],
      "Leila's note hands the job of caring for the plants to the narrator: a link between the sisters."),
    Q(PV, passage(ROOM, "How do the narrator's feelings change by the end?"), "from lonely to comforted",
      ["from happy to angry", "from bored to frightened", "from excited to jealous"],
      "The narrator starts out finding the room too quiet and ends up laughing for the first time in a week."),
    Q(MI, passage(NORTH, "Which sentence best states the central idea?"),
      "The North's harsh climate and permafrost make it hard to build and live there, and a warming climate is creating new problems.",
      ["Most Canadians live in the territories.", "Permafrost is found only in Canada.", "Roads in the North were built recently."],
      "The passage explains why few people live in the territories and how thawing permafrost now causes damage."),
    Q(TS, passage(NORTH, "How does the author mainly organize the information?"), "by explaining causes and effects",
      ["by telling a personal story", "by listing steps in a process", "by comparing two countries"],
      "It explains why few people live there (causes) and what thawing permafrost does (effects)."),
    Q(CE, passage(NORTH, "Which detail best supports the idea that building on permafrost is difficult?"),
      "heat from buildings can thaw the ground and make it unstable",
      ["Canada's three territories cover about 40 percent of the country's land", "Winters are long and extremely cold",
       "fewer than 130 000 people live there"], "This detail directly explains why construction on permafrost causes problems."),
    Q(AP, passage(NORTH, "What is the author's main purpose?"), "to inform readers about life and building in Canada's North",
      ["to persuade readers to move to the territories", "to entertain readers with a story", "to describe how to build a house"],
      "The passage gives facts and explanations; it does not tell a story or argue for an action."),
    Q(GR, "Which sentence contains a dangling modifier?", "Running for the bus, my backpack fell open.",
      ["While I was running for the bus, my backpack fell open.", "My backpack fell open as I ran for the bus.", "I ran for the bus, and my backpack fell open."],
      "'Running for the bus' has nothing to describe except 'my backpack', so the sentence says the backpack was running."),
    Q(GR, "Which sentence is a complex sentence?", "When the bell rang, the students lined up.",
      ["The students lined up.", "The bell rang, and the students lined up.", "The bell rang loudly."],
      "It has a dependent clause ('When the bell rang') and an independent clause."),
    Q(PU, "Which sentence uses a semicolon correctly?", "The game was cancelled; the field was flooded.",
      ["The game; was cancelled the field was flooded.", "The game was; cancelled, the field was flooded.", "The game was cancelled the; field was flooded."],
      "A semicolon joins two closely related complete sentences."),
    Q(PU, "Which sentence uses a colon correctly?", "Bring three things: a pencil, an eraser, and a ruler.",
      ["Bring: three things a pencil, an eraser, and a ruler.", "Bring three: things a pencil, an eraser, and a ruler.", "Bring three things a pencil: an eraser, and a ruler."],
      "A colon comes after a complete sentence to introduce a list."),
    Q(CON, "Which word describes a confident person in a negative way?", "arrogant", ["self-assured", "confident", "bold"],
      "'Arrogant' suggests thinking you are better than others, which is negative."),
    Q(WP, "The Greek root 'chron' means 'time'. What does 'chronological' mean?", "in time order", ["very long", "in alphabetical order", "about clocks only"],
      "Chronological order is the order in which events happened in time."),
    Q(VOC, "'The mayor's speech was so succinct that it lasted barely a minute.' What does 'succinct' mean?", "brief and clear",
      ["angry", "boring and long", "hard to hear"], "The clue 'lasted barely a minute' shows that succinct means short and to the point."),
    Q(FIG, "Which line contains alliteration?", "Big brown bears bounded by the river.",
      ["The bears ran beside the river.", "The river was a ribbon of silver.", "The bears were as quick as lightning."],
      "Alliteration repeats the same first sound: big, brown, bears, bounded, by."),
    Q(GR, "Which sentence is written in the active voice?", "The goalie stopped the puck.",
      ["The puck was stopped by the goalie.", "The puck was stopped.", "The puck had been stopped by the goalie."],
      "In the active voice the subject (the goalie) does the action."),
    Q(GR, "Which sentence is the most concise?", "Please reply by Friday.",
      ["Please make sure that you send us a reply at some point before the day of Friday.",
       "We would like it if you could possibly reply to us by Friday or before.", "Please reply by Friday at the very latest, by Friday."],
      "It gives the same request in the fewest words, without repetition."),
    Q(SP, "Which word is spelled correctly?", "accommodate", ["acommodate", "accomodate", "acomodate"],
      "Accommodate has double c and double m."),
    Q(GR, "Choose the correct verb: 'Neither the players nor the coach ___ happy with the result.'", "was",
      ["were", "are being", "be"], "With 'neither … nor', the verb agrees with the nearer subject, 'the coach', which is singular."),
])
