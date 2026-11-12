r"""GCSE Maths Practice Paper 1 (Foundation and crossover, grades 1-5): 12 non-calculator + 12 calculator
multiple-choice questions. Original questions written by the Notenix team. Run: python mock1.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from gcse_maths_common import *  # noqa: E402,F403

A = [
    q(NUM, FDP, 1, r"Work out $0.6 \times 0.3$.", ["$1.8$", "$0.18$", "$0.018$", "$18$"], "B",
      r"$6 \times 3 = 18$. There are two decimal places in the question in total, so the answer has two: $0.18$.",
      check=lambda: near(0.6 * 0.3, 0.18, 1e-9)),
    q(NUM, FAC, 1, r"Round $4768$ to 2 significant figures.", ["$4700$", "$4770$", "$48$", "$4800$"], "D",
      r"The first two significant figures are $4$ and $7$. The next digit is $6$, so round up to $4800$. Keep the zeros to hold the place value.",
      check=lambda: round(4768, -2) == 4800),
    q(ALG, EXP, 1, r"Expand $4(2x - 3)$.", ["$8x - 12$", "$8x - 3$", "$6x - 7$", "$2x - 12$"], "A",
      r"Multiply both terms inside the bracket by $4$: $4 \times 2x = 8x$ and $4 \times (-3) = -12$.",
      check=lambda: all(4 * (2 * x - 3) == 8 * x - 12 for x in R)),
    q(ALG, EQN, 1, r"Solve $\dfrac{x}{3} + 2 = 7$.", ["$x = 3$", "$x = 27$", "$x = 15$", "$x = 9$"], "C",
      r"Subtract $2$ from both sides: $\frac{x}{3} = 5$. Multiply both sides by $3$: $x = 15$.", check=lambda: 15 / 3 + 2 == 7),
    q(RAT, RP, 1, r"$40$ sweets are shared in the ratio $2 : 3$. How many sweets are in the smaller share?", ["$8$", "$24$", "$16$", "$20$"], "C",
      r"There are $2 + 3 = 5$ parts, so one part is $40 \div 5 = 8$ sweets. The smaller share is $2$ parts: $16$.", check=lambda: 40 / 5 * 2 == 16),
    q(GEO, ANG, 1, r"Two angles lie on a straight line. One of them is $115^\circ$. What is the other?",
      [r"$65^\circ$", r"$75^\circ$", r"$245^\circ$", r"$115^\circ$"], "A",
      r"Angles on a straight line add up to $180^\circ$: $180 - 115 = 65^\circ$.", check=lambda: 180 - 115 == 65),
    q(PS, PROB, 1, "A fair six-sided dice is rolled. What is the probability of rolling a prime number?",
      [r"$\dfrac{1}{3}$", r"$\dfrac{2}{3}$", r"$\dfrac{1}{6}$", r"$\dfrac{1}{2}$"], "D",
      r"The prime numbers on a dice are $2$, $3$ and $5$. Remember that $1$ is not prime. So the probability is $\frac{3}{6} = \frac{1}{2}$.",
      check=lambda: Fr(len([n for n in range(1, 7) if n > 1 and all(n % k for k in range(2, n))]), 6) == Fr(1, 2)),
    q(PS, STAT, 1, r"What is the mean of $4,\ 6,\ 9,\ 13$?", ["$7.5$", "$8$", "$9$", "$32$"], "B",
      r"Add the numbers: $4 + 6 + 9 + 13 = 32$. Divide by how many there are: $32 \div 4 = 8$.", check=lambda: (4 + 6 + 9 + 13) / 4 == 8),
    q(NUM, IND, 2, r"Work out $2^3 \times 3^2$.", ["$72$", "$36$", "$54$", "$48$"], "A",
      r"$2^3 = 8$ and $3^2 = 9$, so the answer is $8 \times 9 = 72$.", check=lambda: 2 ** 3 * 3 ** 2 == 72),
    q(ALG, SEQ, 2, r"The $n$th term of a sequence is $5n - 2$. Which of these numbers is a term in the sequence?", ["$40$", "$41$", "$43$", "$45$"], "C",
      r"A term plus $2$ must be a multiple of $5$. $43 + 2 = 45 = 5 \times 9$, so $43$ is the 9th term. The others do not work.",
      check=lambda: [t for t in (40, 41, 43, 45) if (t + 2) % 5 == 0] == [43]),
    q(ALG, GRA, 2, r"A point on the line $y = 2x + 3$ has $x$-coordinate $-2$. What is its $y$-coordinate?", ["$-7$", "$-1$", "$1$", "$7$"], "B",
      r"Substitute $x = -2$: $y = 2 \times (-2) + 3 = -4 + 3 = -1$.", check=lambda: 2 * (-2) + 3 == -1),
    q(GEO, AREA, 2, r"A rectangle is $8\ \text{cm}$ long and $5\ \text{cm}$ wide. What is its perimeter?",
      [r"$40\ \text{cm}$", r"$13\ \text{cm}$", r"$80\ \text{cm}$", r"$26\ \text{cm}$"], "D",
      r"The perimeter is the distance all the way round: $8 + 5 + 8 + 5 = 26\ \text{cm}$. Note that $40$ is the area in $\text{cm}^2$.",
      check=lambda: 2 * (8 + 5) == 26),
]

B = [
    q(RAT, PCT, 1, "Work out 35% of £260.", ["£74.29", "£9.10", "£91", "£169"], "C",
      r"$35\% = 0.35$, and $0.35 \times 260 = 91$, so the answer is £91.", check=lambda: near(0.35 * 260, 91, 1e-9)),
    q(NUM, FDP, 2, r"Write $\dfrac{3}{8}$ as a decimal.", ["$0.375$", "$0.38$", "$2.67$", "$0.83$"], "A",
      r"Divide the numerator by the denominator: $3 \div 8 = 0.375$.", check=lambda: 3 / 8 == 0.375),
    q(GEO, AREA, 2, r"What is the area of a circle of radius $7\ \text{cm}$, to 1 decimal place?",
      [r"$44.0\ \text{cm}^2$", r"$22.0\ \text{cm}^2$", r"$49.0\ \text{cm}^2$", r"$153.9\ \text{cm}^2$"], "D",
      r"Area is $\pi r^2 = \pi \times 7^2 = 49\pi = 153.9\ \text{cm}^2$. Note that $44.0$ is the circumference, $2\pi r$.",
      check=lambda: round(math.pi * 49, 1) == 153.9),
    q(GEO, AREA, 2, r"The two shorter sides of a right-angled triangle are $6\ \text{cm}$ and $8\ \text{cm}$. How long is the hypotenuse?",
      [r"$14\ \text{cm}$", r"$10\ \text{cm}$", r"$100\ \text{cm}$", r"$7\ \text{cm}$"], "B",
      r"By Pythagoras, $c^2 = 6^2 + 8^2 = 36 + 64 = 100$, so $c = \sqrt{100} = 10\ \text{cm}$.", check=lambda: math.hypot(6, 8) == 10),
    q(RAT, RP, 2, "A train travels 150 km in 2.5 hours. What is its average speed?", ["375 km/h", "60 km/h", "152.5 km/h", "50 km/h"], "B",
      "Speed is distance divided by time: 150 divided by 2.5 = 60 km/h.", check=lambda: 150 / 2.5 == 60),
    q(ALG, EQN, 2, r"Solve $3(x + 4) = 5x - 2$.", ["$x = 1$", "$x = 3$", "$x = 5$", "$x = 7$"], "D",
      r"Expand: $3x + 12 = 5x - 2$. Subtract $3x$ and add $2$: $14 = 2x$, so $x = 7$.", check=lambda: 3 * (7 + 4) == 5 * 7 - 2),
    q(GEO, VEC, 2, r"The point $(3, 1)$ is rotated $90^\circ$ anticlockwise about the origin. What are the coordinates of its image?",
      ["$(-1, 3)$", "$(1, -3)$", "$(-3, -1)$", "$(3, -1)$"], "A",
      r"A $90^\circ$ anticlockwise rotation about the origin sends $(x, y)$ to $(-y, x)$, so $(3, 1)$ goes to $(-1, 3)$."),
    q(PS, STAT, 2, "A scatter graph shows that as the temperature rises, ice cream sales rise. What type of correlation is this?",
      ["Negative correlation", "No correlation", "Positive correlation", "Inverse proportion"], "C",
      "When both quantities increase together the correlation is positive. Negative correlation is when one goes up as the other goes down."),
    q(PS, PROB, 2, r"Events $A$ and $B$ are independent. $P(A) = 0.3$ and $P(B) = 0.5$. What is the probability that both happen?",
      ["$0.8$", "$0.2$", "$0.35$", "$0.15$"], "D",
      r"For independent events, multiply the probabilities: $0.3 \times 0.5 = 0.15$.", check=lambda: near(0.3 * 0.5, 0.15, 1e-9)),
    q(RAT, PCT, 2, "£500 is invested at 4% simple interest per year. How much interest is earned in total after 3 years?",
      ["£20", "£60", "£62.43", "£560"], "B",
      "Simple interest is the same every year: 4% of £500 is £20 per year, so after 3 years the interest is £60. £62.43 would be compound interest.",
      check=lambda: near(500 * 0.04 * 3, 60, 1e-9)),
    q(ALG, EXP, 2, r"Factorise $6x + 15$.", ["$6(x + 15)$", "$3(2x + 15)$", "$3(2x + 5)$", "$2(3x + 7)$"], "C",
      r"The highest common factor of $6$ and $15$ is $3$. Take it outside the bracket: $3(2x + 5)$.",
      check=lambda: all(3 * (2 * x + 5) == 6 * x + 15 for x in R)),
    q(GEO, ANG, 2, r"The bearing of $B$ from $A$ is $070^\circ$. What is the bearing of $A$ from $B$?",
      [r"$250^\circ$", r"$110^\circ$", r"$290^\circ$", r"$020^\circ$"], "A",
      r"A back bearing differs by $180^\circ$. Since $70$ is less than $180$, add: $70 + 180 = 250^\circ$.", check=lambda: (70 + 180) % 360 == 250),
]

save_form("gcse-maths", "mock-1", "GCSE Maths Practice Paper 1", "mock", [
    module("non-calc", "Part 1: no calculator", "non-calc", 25, A),
    module("calc", "Part 2: calculator allowed", "calc", 25, B),
], summary="Foundation and crossover · grades 1 to 5 · 24 questions · 50 min")
