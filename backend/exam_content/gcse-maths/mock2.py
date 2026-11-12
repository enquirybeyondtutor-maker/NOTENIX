r"""GCSE Maths Practice Paper 2 (Higher, grades 4-9): 12 non-calculator + 12 calculator multiple-choice
questions. Original questions written by the Notenix team. Run: python mock2.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from gcse_maths_common import *  # noqa: E402,F403

A = [
    q(NUM, IND, 2, r"Simplify $\dfrac{5^6 \times 5^{-2}}{5^3}$.", ["$5$", "$25$", r"$\dfrac{1}{5}$", "$125$"], "A",
      r"Add the indices on top: $5^{6 + (-2)} = 5^4$. Subtract the index underneath: $5^{4 - 3} = 5^1 = 5$.",
      check=lambda: Fr(5 ** 6, 5 ** 2) / 5 ** 3 == 5),
    q(NUM, FDP, 2, r"Work out $2\tfrac{1}{4} \times 1\tfrac{1}{3}$.", [r"$2\tfrac{1}{12}$", r"$3\tfrac{7}{12}$", "$3$", "$2$"], "C",
      r"Change to improper fractions: $\frac{9}{4} \times \frac{4}{3} = \frac{36}{12} = 3$.", check=lambda: Fr(9, 4) * Fr(4, 3) == 3),
    q(ALG, EXP, 2, r"Expand and simplify $(x + 5)^2$.", ["$x^2 + 25$", "$x^2 + 10x + 25$", "$x^2 + 5x + 25$", "$2x + 10$"], "B",
      r"$(x + 5)^2 = (x + 5)(x + 5) = x^2 + 5x + 5x + 25 = x^2 + 10x + 25$. Do not forget the middle term.",
      check=lambda: all((x + 5) ** 2 == x * x + 10 * x + 25 for x in R)),
    q(ALG, EQN, 3, r"Solve the simultaneous equations $y = x + 1$ and $x^2 + y^2 = 25$.",
      [r"$(4, 5)$ and $(-5, -4)$", r"$(3, 4)$ only", r"$(5, 0)$ and $(0, 5)$", r"$(3, 4)$ and $(-4, -3)$"], "D",
      r"Substitute: $x^2 + (x + 1)^2 = 25$ gives $2x^2 + 2x - 24 = 0$, so $x^2 + x - 12 = 0$ and $(x + 4)(x - 3) = 0$. $x = 3$ gives $y = 4$; $x = -4$ gives $y = -3$.",
      check=lambda: all(y == x + 1 and x * x + y * y == 25 for x, y in ((3, 4), (-4, -3)))),
    q(NUM, IND, 3, r"Expand and simplify $(\sqrt{5} + 2)(\sqrt{5} - 2)$.", ["$9$", r"$1 + 4\sqrt{5}$", "$3$", "$1$"], "D",
      r"This is a difference of two squares: $(\sqrt{5})^2 - 2^2 = 5 - 4 = 1$. The two surd terms cancel.",
      check=lambda: near((math.sqrt(5) + 2) * (math.sqrt(5) - 2), 1, 1e-9)),
    q(ALG, SEQ, 3, r"What is the $n$th term of the quadratic sequence $2,\ 6,\ 12,\ 20,\ \ldots$?",
      ["$4n - 2$", "$n^2 + n$", "$n^2 + 1$", "$2n^2$"], "B",
      r"The second difference is $2$, so the rule starts $n^2$. Subtracting $n^2$ ($1, 4, 9, 16$) from the terms leaves $1, 2, 3, 4$, which is $n$. So the rule is $n^2 + n$.",
      check=lambda: [n * n + n for n in (1, 2, 3, 4)] == [2, 6, 12, 20]),
    q(ALG, GRA, 3, "What is the equation of the circle with centre the origin and radius 5?",
      ["$x^2 + y^2 = 25$", "$x^2 + y^2 = 5$", "$x + y = 25$", "$y = x^2 + 25$"], "A",
      r"A circle with centre the origin and radius $r$ has equation $x^2 + y^2 = r^2$. Here $r^2 = 25$.", check=lambda: 3 ** 2 + 4 ** 2 == 5 ** 2),
    q(RAT, RP, 3, r"$y$ is directly proportional to $\sqrt{x}$. When $x = 9$, $y = 6$. What is $y$ when $x = 25$?",
      ["$16.7$", "$50$", "$10$", "$30$"], "C",
      r"Write $y = k\sqrt{x}$. Using $x = 9$, $y = 6$: $6 = 3k$, so $k = 2$. When $x = 25$, $y = 2 \times 5 = 10$.",
      check=lambda: 6 / math.sqrt(9) * math.sqrt(25) == 10),
    q(GEO, ANG, 3, r"$AB$ is a diameter of a circle and $C$ is another point on the circumference. What is the size of angle $ACB$?",
      [r"$45^\circ$", r"$90^\circ$", r"$180^\circ$", r"$60^\circ$"], "B",
      r"The angle in a semicircle is always a right angle, so angle $ACB = 90^\circ$."),
    q(PS, PROB, 3, r"$P(A) = 0.5$, $P(B) = 0.4$ and $P(A \text{ and } B) = 0.2$. What is $P(A \text{ or } B)$?",
      ["$0.7$", "$0.9$", "$0.2$", "$0.1$"], "A",
      r"Add the two probabilities, then subtract the probability of both: $0.5 + 0.4 - 0.2 = 0.7$. Subtracting the overlap stops it being counted twice.",
      check=lambda: near(0.5 + 0.4 - 0.2, 0.7, 1e-9)),
    q(ALG, EXP, 3, r"Simplify $3x^2y \times 4xy^3$.", ["$7x^3y^4$", "$12x^2y^3$", "$12x^2y^4$", "$12x^3y^4$"], "D",
      r"Multiply the numbers: $3 \times 4 = 12$. Add the indices for each letter: $x^{2+1} = x^3$ and $y^{1+3} = y^4$.",
      check=lambda: all(3 * x ** 2 * y * 4 * x * y ** 3 == 12 * x ** 3 * y ** 4 for x in (2, 3) for y in (2, 5))),
    q(PS, STAT, 2, "A box plot shows a lower quartile of 12 and an upper quartile of 30. What is the interquartile range?",
      ["$42$", "$21$", "$18$", "$30$"], "C",
      r"The interquartile range is the upper quartile minus the lower quartile: $30 - 12 = 18$.", check=lambda: 30 - 12 == 18),
]

B = [
    q(RAT, PCT, 3, "In a sale, prices are reduced by 30%. The sale price of a coat is £84. What was the original price?",
      ["£109.20", "£120", "£114", "£280"], "B",
      "The sale price is 70% of the original, so divide by 0.7: 84 divided by 0.7 = £120. Adding 30% to £84 gives the wrong answer, £109.20.",
      check=lambda: near(84 / 0.7, 120, 1e-9)),
    q(GEO, TRIG, 3, r"In triangle $ABC$, angle $A = 40^\circ$, angle $B = 75^\circ$ and side $a = 8\ \text{cm}$. What is the length of side $b$, to 3 significant figures?",
      [r"$12.0\ \text{cm}$", r"$5.32\ \text{cm}$", r"$15.0\ \text{cm}$", r"$10.4\ \text{cm}$"], "A",
      r"Use the sine rule: $\frac{b}{\sin 75^\circ} = \frac{8}{\sin 40^\circ}$, so $b = \frac{8 \sin 75^\circ}{\sin 40^\circ} = 12.0\ \text{cm}$.",
      check=lambda: round(8 * sin(75) / sin(40), 1) == 12.0),
    q(GEO, AREA, 3, r"A cone has base radius $3\ \text{cm}$ and height $4\ \text{cm}$. What is its volume, to 1 decimal place? (Volume of a cone $= \frac{1}{3}\pi r^2 h$)",
      [r"$113.1\ \text{cm}^3$", r"$47.1\ \text{cm}^3$", r"$12.0\ \text{cm}^3$", r"$37.7\ \text{cm}^3$"], "D",
      r"$\frac{1}{3} \times \pi \times 3^2 \times 4 = 12\pi = 37.7\ \text{cm}^3$.", check=lambda: round(math.pi * 9 * 4 / 3, 1) == 37.7),
    q(GEO, TRIG, 3, r"Two sides of a triangle are $6\ \text{cm}$ and $10\ \text{cm}$, and the angle between them is $30^\circ$. What is the area of the triangle?",
      [r"$30\ \text{cm}^2$", r"$26.0\ \text{cm}^2$", r"$15\ \text{cm}^2$", r"$60\ \text{cm}^2$"], "C",
      r"Area $= \frac{1}{2}ab\sin C = \frac{1}{2} \times 6 \times 10 \times \sin 30^\circ = 30 \times 0.5 = 15\ \text{cm}^2$.",
      check=lambda: near(0.5 * 6 * 10 * sin(30), 15, 1e-9)),
    q(ALG, EQN, 3, r"What is the positive solution of $2x^2 + 3x - 4 = 0$, to 2 decimal places?", ["$0.85$", "$2.35$", "$1.70$", "$0.35$"], "A",
      r"Use the quadratic formula with $a = 2$, $b = 3$, $c = -4$: $x = \frac{-3 \pm \sqrt{9 + 32}}{4} = \frac{-3 \pm \sqrt{41}}{4}$. The positive solution is $0.85$.",
      check=lambda: round((-3 + math.sqrt(41)) / 4, 2) == 0.85),
    q(ALG, GRA, 3, r"What is the minimum value of $y = x^2 - 4x + 1$?", ["$1$", "$2$", "$-3$", "$-4$"], "C",
      r"Complete the square: $y = (x - 2)^2 - 4 + 1 = (x - 2)^2 - 3$. The smallest value of the squared bracket is $0$, so the minimum of $y$ is $-3$.",
      check=lambda: min((x / 100) ** 2 - 4 * (x / 100) + 1 for x in range(0, 401)) == -3),
    q(GEO, VEC, 3, r"$\overrightarrow{OA} = \mathbf{a}$ and $\overrightarrow{OB} = \mathbf{b}$. $M$ is the midpoint of $AB$. What is $\overrightarrow{OM}$ in terms of $\mathbf{a}$ and $\mathbf{b}$?",
      [r"$\mathbf{a} + \mathbf{b}$", r"$\tfrac{1}{2}(\mathbf{a} + \mathbf{b})$", r"$\tfrac{1}{2}(\mathbf{b} - \mathbf{a})$", r"$\mathbf{b} - \mathbf{a}$"], "B",
      r"$\overrightarrow{AB} = \mathbf{b} - \mathbf{a}$, so $\overrightarrow{AM} = \frac{1}{2}(\mathbf{b} - \mathbf{a})$. Then $\overrightarrow{OM} = \mathbf{a} + \frac{1}{2}(\mathbf{b} - \mathbf{a}) = \frac{1}{2}(\mathbf{a} + \mathbf{b})$.",
      check=lambda: 4 + 0.5 * (10 - 4) == 0.5 * (4 + 10)),
    q(PS, PROB, 3, "A bag contains 7 black and 3 white counters. Two counters are taken at random without replacement. What is the probability that they are the same colour?",
      [r"$\dfrac{7}{15}$", r"$\dfrac{21}{50}$", r"$\dfrac{29}{50}$", r"$\dfrac{8}{15}$"], "D",
      r"Both black: $\frac{7}{10} \times \frac{6}{9} = \frac{42}{90}$. Both white: $\frac{3}{10} \times \frac{2}{9} = \frac{6}{90}$. Add them: $\frac{48}{90} = \frac{8}{15}$.",
      check=lambda: Fr(7, 10) * Fr(6, 9) + Fr(3, 10) * Fr(2, 9) == Fr(8, 15)),
    q(PS, STAT, 3, r"""The table shows the times taken by 20 students to finish a puzzle.

| Time (minutes) | Frequency |
| - | - |
| 0 to 10 | 4 |
| 10 to 20 | 10 |
| 20 to 30 | 6 |

What is the estimate of the mean time?""", ["15 minutes", "6.67 minutes", "16 minutes", "17 minutes"], "C",
      r"Use the midpoints $5$, $15$ and $25$: $(5 \times 4) + (15 \times 10) + (25 \times 6) = 320$. Divide by the $20$ students: $16$ minutes.",
      check=lambda: (5 * 4 + 15 * 10 + 25 * 6) / 20 == 16),
    q(RAT, PCT, 3, "£3000 is invested at 2.5% compound interest per year. What is it worth after 5 years, to the nearest pound?",
      ["£3375", "£3075", "£3381", "£3394"], "D",
      r"Multiply by $1.025$ for each year: $3000 \times 1.025^5 = 3394.22\ldots$, which is £3394. £3375 would be simple interest.",
      check=lambda: round(3000 * 1.025 ** 5) == 3394),
    q(RAT, RP, 3, "A car travels 45 km at 60 km/h and then another 45 km at 90 km/h. What is its average speed for the whole journey?",
      ["72 km/h", "75 km/h", "70 km/h", "150 km/h"], "A",
      "The times are 45 divided by 60 = 0.75 hours and 45 divided by 90 = 0.5 hours, a total of 1.25 hours. Average speed is total distance over total time: 90 divided by 1.25 = 72 km/h.",
      check=lambda: 90 / (45 / 60 + 45 / 90) == 72),
    q(NUM, FAC, 3, r"$a = 6.4$ and $b = 2.5$, each correct to 1 decimal place. What is the upper bound of $\dfrac{a}{b}$, to 2 decimal places?",
      ["$2.56$", "$2.63$", "$2.53$", "$2.59$"], "B",
      r"For the largest answer, divide the largest $a$ by the smallest $b$: $\frac{6.45}{2.45} = 2.63$.", check=lambda: round(6.45 / 2.45, 2) == 2.63),
]

save_form("gcse-maths", "mock-2", "GCSE Maths Practice Paper 2", "mock", [
    module("non-calc", "Part 1: no calculator", "non-calc", 25, A),
    module("calc", "Part 2: calculator allowed", "calc", 25, B),
], summary="Higher · grades 4 to 9 · 24 questions · 50 min")
