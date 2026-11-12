r"""GCSE Maths free diagnostic: 10 non-calculator + 10 calculator multiple-choice questions, at least
one per skill, mixing Foundation and Higher content. Original questions written by the Notenix team.
Run from this folder: python diagnostic.py"""
import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402

NUM, ALG, RAT, GEO, PS = "Number", "Algebra", "Ratio and proportion", "Geometry and measures", "Probability and statistics"
FDP, IND, FAC = "Fractions, decimals and percentages", "Indices, standard form and surds", "Factors, multiples and estimation"
EXP, EQN, SEQ, GRA = "Expressions and formulae", "Equations and inequalities", "Sequences", "Graphs and functions"
RP, PCT = "Ratio and proportion", "Percentage change and growth"
ANG, AREA, TRIG, VEC = "Angles and shapes", "Area, volume and Pythagoras", "Trigonometry", "Vectors and transformations"
PROB, STAT = "Probability", "Statistics"

A = [
    q(NUM, FDP, 1, r"Work out $\dfrac{3}{4} - \dfrac{2}{5}$.",
      [r"$\dfrac{1}{20}$", r"$\dfrac{7}{20}$", r"$\dfrac{1}{9}$", r"$\dfrac{5}{9}$"], "B",
      r"Use a common denominator of $20$: $\frac{15}{20} - \frac{8}{20} = \frac{7}{20}$.",
      check=lambda: Fr(3, 4) - Fr(2, 5) == Fr(7, 20)),
    q(NUM, IND, 2, r"Work out the value of $27^{\frac{2}{3}}$.",
      ["$18$", "$6$", "$81$", "$9$"], "D",
      r"The denominator $3$ means cube root and the numerator $2$ means square: $\sqrt[3]{27} = 3$ and $3^2 = 9$.",
      check=lambda: round(27 ** (2 / 3), 9) == 9),
    q(NUM, FAC, 1, r"What is the highest common factor (HCF) of $84$ and $126$?",
      ["$42$", "$21$", "$14$", "$6$"], "A",
      r"$84 = 2^2 \times 3 \times 7$ and $126 = 2 \times 3^2 \times 7$. The shared factors are $2 \times 3 \times 7 = 42$.",
      check=lambda: math.gcd(84, 126) == 42),
    q(ALG, EXP, 2, r"Expand and simplify $(2x - 3)(x + 4)$.",
      [r"$2x^2 - 12$", r"$2x^2 + 11x - 12$", r"$2x^2 + 5x - 12$", r"$2x^2 - 5x - 12$"], "C",
      r"Multiply each term: $2x^2 + 8x - 3x - 12$. Collect the $x$ terms: $2x^2 + 5x - 12$.",
      check=lambda: all((2 * x - 3) * (x + 4) == 2 * x * x + 5 * x - 12 for x in range(-5, 6))),
    q(ALG, EQN, 2, r"Solve $5x - 7 = 2x + 11$.",
      ["$x = 6$", "$x = 18$", r"$x = \dfrac{4}{3}$", r"$x = \dfrac{18}{7}$"], "A",
      r"Subtract $2x$ from both sides: $3x - 7 = 11$. Add $7$: $3x = 18$, so $x = 6$.",
      check=lambda: 5 * 6 - 7 == 2 * 6 + 11),
    q(ALG, SEQ, 2, r"The first four terms of a sequence are $7,\ 11,\ 15,\ 19$. What is the $n$th term?",
      ["$n + 4$", "$4n - 3$", "$3n + 4$", "$4n + 3$"], "D",
      r"The terms go up by $4$ each time, so the rule starts $4n$. When $n = 1$, $4n = 4$, and the first term is $7$, so add $3$: $4n + 3$.",
      check=lambda: [4 * n + 3 for n in (1, 2, 3, 4)] == [7, 11, 15, 19]),
    q(RAT, RP, 1, r"£120 is shared between Amy and Ben in the ratio $3 : 5$. How much does Ben, who has the larger share, receive?",
      ["£45", "£75", "£72", "£80"], "B",
      r"There are $3 + 5 = 8$ parts, so one part is £$120 \div 8$ = £15. Ben has $5$ parts: $5 \times 15$ = £75.",
      check=lambda: 120 / 8 * 5 == 75),
    q(GEO, ANG, 2, r"Each interior angle of a regular polygon is $150^\circ$. How many sides does the polygon have?",
      ["$10$", "$15$", "$12$", "$6$"], "C",
      r"Each exterior angle is $180^\circ - 150^\circ = 30^\circ$. Exterior angles add up to $360^\circ$, so there are $360 \div 30 = 12$ sides.",
      check=lambda: 360 / (180 - 150) == 12),
    q(NUM, IND, 3, r"Simplify $\sqrt{75} - \sqrt{12}$.",
      [r"$3\sqrt{3}$", r"$\sqrt{63}$", r"$7\sqrt{3}$", r"$3\sqrt{7}$"], "A",
      r"$\sqrt{75} = \sqrt{25 \times 3} = 5\sqrt{3}$ and $\sqrt{12} = \sqrt{4 \times 3} = 2\sqrt{3}$. So the answer is $5\sqrt{3} - 2\sqrt{3} = 3\sqrt{3}$.",
      check=lambda: abs(math.sqrt(75) - math.sqrt(12) - 3 * math.sqrt(3)) < 1e-9),
    q(PS, PROB, 2, r"A bag contains $5$ red counters and $3$ blue counters. Two counters are taken at random without replacement. What is the probability that both are red?",
      [r"$\dfrac{25}{64}$", r"$\dfrac{5}{16}$", r"$\dfrac{9}{14}$", r"$\dfrac{5}{14}$"], "D",
      r"The first is red with probability $\frac{5}{8}$. That leaves $4$ red out of $7$, so the second is red with probability $\frac{4}{7}$. Multiply: $\frac{5}{8} \times \frac{4}{7} = \frac{20}{56} = \frac{5}{14}$.",
      check=lambda: Fr(5, 8) * Fr(4, 7) == Fr(5, 14)),
]

B = [
    q(ALG, GRA, 2, r"A straight line passes through the points $(1, 3)$ and $(5, 11)$. What is the gradient of the line?",
      ["$4$", r"$\dfrac{1}{2}$", "$2$", "$8$"], "C",
      r"Gradient is change in $y$ divided by change in $x$: $\frac{11 - 3}{5 - 1} = \frac{8}{4} = 2$.",
      check=lambda: (11 - 3) / (5 - 1) == 2),
    q(RAT, PCT, 2, r"£2400 is invested at $3\%$ compound interest per year. What is the investment worth after $4$ years, to the nearest pound?",
      ["£2701", "£2688", "£2622", "£2712"], "A",
      r"Each year the amount is multiplied by $1.03$. After $4$ years: $2400 \times 1.03^4 = 2701.22\ldots$, which is £2701 to the nearest pound.",
      check=lambda: round(2400 * 1.03 ** 4) == 2701),
    q(GEO, AREA, 2, r"A cylinder has radius $4\ \text{cm}$ and height $10\ \text{cm}$. What is its volume, to the nearest $\text{cm}^3$?",
      [r"$251\ \text{cm}^3$", r"$503\ \text{cm}^3$", r"$126\ \text{cm}^3$", r"$1005\ \text{cm}^3$"], "B",
      r"Volume of a cylinder is $\pi r^2 h = \pi \times 4^2 \times 10 = 160\pi = 502.65\ldots$, which rounds to $503\ \text{cm}^3$.",
      check=lambda: round(math.pi * 16 * 10) == 503),
    q(GEO, TRIG, 2, r"In a right-angled triangle the hypotenuse is $12\ \text{cm}$ and one angle is $35^\circ$. What is the length of the side opposite the $35^\circ$ angle, to 3 significant figures?",
      [r"$9.83\ \text{cm}$", r"$8.40\ \text{cm}$", r"$20.9\ \text{cm}$", r"$6.88\ \text{cm}$"], "D",
      r"Opposite and hypotenuse means sine: $\sin 35^\circ = \frac{\text{opp}}{12}$, so $\text{opp} = 12 \sin 35^\circ = 6.88\ \text{cm}$.",
      check=lambda: round(12 * math.sin(math.radians(35)), 2) == 6.88),
    q(GEO, VEC, 2, r"$\mathbf{a} = \begin{pmatrix} 3 \\ -2 \end{pmatrix}$ and $\mathbf{b} = \begin{pmatrix} -1 \\ 4 \end{pmatrix}$. Work out $2\mathbf{a} - \mathbf{b}$.",
      [r"$\begin{pmatrix} 5 \\ 0 \end{pmatrix}$", r"$\begin{pmatrix} 7 \\ -8 \end{pmatrix}$",
       r"$\begin{pmatrix} 7 \\ 0 \end{pmatrix}$", r"$\begin{pmatrix} 5 \\ -8 \end{pmatrix}$"], "B",
      r"$2\mathbf{a} = \begin{pmatrix} 6 \\ -4 \end{pmatrix}$. Subtract $\mathbf{b}$ from each row: $6 - (-1) = 7$ and $-4 - 4 = -8$.",
      check=lambda: (2 * 3 - (-1), 2 * (-2) - 4) == (7, -8)),
    q(PS, STAT, 2, r"The mean of $20$ numbers is $6.5$. One more number is added and the mean of all $21$ numbers is $7$. What number was added?",
      ["$17$", "$7.5$", "$10.5$", "$27$"], "A",
      r"The $20$ numbers total $20 \times 6.5 = 130$. The $21$ numbers total $21 \times 7 = 147$. The new number is $147 - 130 = 17$.",
      check=lambda: 21 * 7 - 20 * 6.5 == 17),
    q(ALG, EQN, 3, r"Solve $x^2 - 5x - 14 = 0$.",
      [r"$x = 2$ or $x = -7$", r"$x = 14$ or $x = -1$", r"$x = -7$ or $x = -2$", r"$x = 7$ or $x = -2$"], "D",
      r"Find two numbers that multiply to $-14$ and add to $-5$: these are $-7$ and $2$. So $(x - 7)(x + 2) = 0$, giving $x = 7$ or $x = -2$.",
      check=lambda: all(x * x - 5 * x - 14 == 0 for x in (7, -2))),
    q(RAT, RP, 3, r"$y$ is inversely proportional to $x^2$. When $x = 2$, $y = 9$. What is the value of $y$ when $x = 6$?",
      ["$27$", "$3$", "$1$", "$81$"], "C",
      r"Write $y = \frac{k}{x^2}$. Using $x = 2$, $y = 9$: $k = 9 \times 4 = 36$. When $x = 6$, $y = \frac{36}{36} = 1$.",
      check=lambda: 9 * 2 ** 2 / 6 ** 2 == 1),
    q(ALG, GRA, 3, r"$f(x) = 3x - 2$ and $g(x) = x^2$. What is the value of $fg(2)$?",
      ["$16$", "$10$", "$8$", "$14$"], "B",
      r"$fg(2)$ means do $g$ first, then $f$. $g(2) = 2^2 = 4$, and $f(4) = 3 \times 4 - 2 = 10$.",
      check=lambda: 3 * (2 ** 2) - 2 == 10),
    q(NUM, IND, 2, r"Work out $(3 \times 10^5) \times (4 \times 10^{-2})$. Give your answer in standard form.",
      [r"$1.2 \times 10^4$", r"$12 \times 10^3$", r"$1.2 \times 10^3$", r"$1.2 \times 10^{-10}$"], "A",
      r"Multiply the numbers and add the powers: $12 \times 10^3$. In standard form the first number must be between $1$ and $10$, so this is $1.2 \times 10^4$.",
      check=lambda: abs(3e5 * 4e-2 - 1.2e4) < 1e-6),
]

save_form("gcse-maths", "diagnostic", "GCSE Maths diagnostic", "diagnostic", [
    module("non-calc", "Part 1: no calculator", "non-calc", 15, A),
    module("calc", "Part 2: calculator allowed", "calc", 15, B),
], summary="20 multiple-choice questions across number, algebra, ratio, geometry, probability and statistics, from Foundation to Higher.")
