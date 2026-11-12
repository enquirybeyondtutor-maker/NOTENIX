r"""GCSE Maths skill drills: 5 original questions for each of the 15 skills, easier to harder.
Written by the Notenix team. Run from this folder: python drills.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, save_drills  # noqa: E402
from gcse_maths_common import *  # noqa: E402,F403

D = {}

D[FDP] = ("Converting between fractions, decimals and percentages, and calculating with fractions.", [
    q(NUM, FDP, 1, r"Write $0.35$ as a fraction in its simplest form.",
      [r"$\dfrac{7}{20}$", r"$\dfrac{35}{10}$", r"$\dfrac{3}{5}$", r"$\dfrac{7}{25}$"], "A",
      r"$0.35 = \frac{35}{100}$. Divide top and bottom by $5$ to get $\frac{7}{20}$.", check=lambda: Fr(35, 100) == Fr(7, 20)),
    q(NUM, FDP, 1, r"Work out $\dfrac{2}{3} + \dfrac{1}{4}$.",
      [r"$\dfrac{3}{7}$", r"$\dfrac{11}{12}$", r"$\dfrac{3}{12}$", r"$\dfrac{1}{2}$"], "B",
      r"Use a common denominator of $12$: $\frac{8}{12} + \frac{3}{12} = \frac{11}{12}$. Never add the denominators.",
      check=lambda: Fr(2, 3) + Fr(1, 4) == Fr(11, 12)),
    q(NUM, FDP, 2, r"Work out $15\%$ of $240$.", ["$16$", "$24$", "$36$", "$3600$"], "C",
      r"$10\%$ of $240$ is $24$ and $5\%$ is $12$, so $15\%$ is $24 + 12 = 36$.", check=lambda: 240 * 15 / 100 == 36),
    q(NUM, FDP, 2, r"Work out $1\tfrac{2}{3} \div \dfrac{5}{6}$.",
      [r"$\dfrac{25}{18}$", r"$\dfrac{1}{2}$", r"$1\tfrac{7}{18}$", "$2$"], "D",
      r"Change to an improper fraction: $\frac{5}{3}$. Dividing by $\frac{5}{6}$ is the same as multiplying by $\frac{6}{5}$: $\frac{5}{3} \times \frac{6}{5} = \frac{30}{15} = 2$.",
      check=lambda: Fr(5, 3) / Fr(5, 6) == 2),
    q(NUM, FDP, 3, r"Write the recurring decimal $0.\dot{4}\dot{5}$ as a fraction in its simplest form.",
      [r"$\dfrac{5}{11}$", r"$\dfrac{9}{20}$", r"$\dfrac{45}{100}$", r"$\dfrac{4}{9}$"], "A",
      r"Let $x = 0.4545\ldots$ Then $100x = 45.4545\ldots$ Subtract: $99x = 45$, so $x = \frac{45}{99} = \frac{5}{11}$.",
      check=lambda: near(5 / 11, 0.454545, 1e-5)),
])

D[IND] = ("The laws of indices, standard form and simplifying surds.", [
    q(NUM, IND, 1, r"Simplify $5^3 \times 5^4$.", ["$5^{12}$", "$25^7$", "$5^7$", "$25^{12}$"], "C",
      r"When multiplying powers of the same base, add the indices: $5^{3+4} = 5^7$.", check=lambda: 5 ** 3 * 5 ** 4 == 5 ** 7),
    q(NUM, IND, 2, r"Write $3.6 \times 10^{-3}$ as an ordinary number.", ["$3600$", "$0.036$", "$0.00036$", "$0.0036$"], "D",
      r"A power of $-3$ means divide by $1000$, moving the digits three places to the right: $0.0036$.",
      check=lambda: near(3.6e-3, 0.0036, 1e-9)),
    q(NUM, IND, 2, r"Simplify $(2x^3)^4$.", ["$8x^7$", "$16x^{12}$", "$2x^{12}$", "$16x^7$"], "B",
      r"Raise each part to the power $4$: $2^4 = 16$ and $(x^3)^4 = x^{12}$, giving $16x^{12}$.",
      check=lambda: all((2 * x ** 3) ** 4 == 16 * x ** 12 for x in R)),
    q(NUM, IND, 3, r"Work out the value of $16^{-\frac{3}{4}}$.",
      [r"$\dfrac{1}{8}$", "$-12$", "$-8$", r"$\dfrac{1}{12}$"], "A",
      r"The fourth root of $16$ is $2$, and $2^3 = 8$. The negative sign means take the reciprocal: $\frac{1}{8}$.",
      check=lambda: near(16 ** (-3 / 4), 1 / 8, 1e-9)),
    q(NUM, IND, 3, r"Rationalise the denominator of $\dfrac{6}{\sqrt{3}}$.",
      [r"$6\sqrt{3}$", r"$3\sqrt{3}$", r"$2\sqrt{3}$", r"$\sqrt{2}$"], "C",
      r"Multiply top and bottom by $\sqrt{3}$: $\frac{6\sqrt{3}}{3} = 2\sqrt{3}$.", check=lambda: near(6 / math.sqrt(3), 2 * math.sqrt(3), 1e-9)),
])

D[FAC] = ("Primes, factors and multiples, rounding, estimating and error intervals.", [
    q(NUM, FAC, 1, "Which of these numbers is prime?", ["$51$", "$57$", "$59$", "$63$"], "C",
      r"$51 = 3 \times 17$, $57 = 3 \times 19$ and $63 = 7 \times 9$. Only $59$ has no factors other than $1$ and itself.",
      check=lambda: [n for n in (51, 57, 59, 63) if all(n % k for k in range(2, n))] == [59]),
    q(NUM, FAC, 1, r"What is the lowest common multiple (LCM) of $12$ and $18$?", ["$6$", "$36$", "$72$", "$216$"], "B",
      r"Multiples of $18$ are $18, 36, \ldots$ and $36$ is also a multiple of $12$. Note that $6$ is the highest common factor, not the LCM.",
      check=lambda: math.lcm(12, 18) == 36),
    q(NUM, FAC, 2, r"By rounding each number to 1 significant figure, estimate the value of $\dfrac{19.8 \times 4.92}{0.51}$.",
      ["$200$", "$50$", "$100$", "$2000$"], "A",
      r"Round to $\frac{20 \times 5}{0.5} = \frac{100}{0.5}$. Dividing by $0.5$ doubles the number, giving $200$.",
      check=lambda: 20 * 5 / 0.5 == 200),
    q(NUM, FAC, 2, r"Write $360$ as a product of its prime factors.",
      [r"$2^2 \times 3^2 \times 10$", r"$2^3 \times 45$", r"$2^2 \times 3^3 \times 5$", r"$2^3 \times 3^2 \times 5$"], "D",
      r"$360 = 2 \times 180 = 2 \times 2 \times 90 = 2 \times 2 \times 2 \times 45 = 2^3 \times 3^2 \times 5$. Every factor in the answer must be prime.",
      check=lambda: 2 ** 3 * 3 ** 2 * 5 == 360),
    q(NUM, FAC, 3, r"A length $l$ is $8.4\ \text{cm}$, correct to 1 decimal place. What is the error interval for $l$?",
      [r"$8.3 \le l < 8.5$", r"$8.35 \le l < 8.45$", r"$8.39 \le l < 8.41$", r"$8.4 \le l < 8.5$"], "B",
      r"Rounding to 1 decimal place means the nearest $0.1$, so the value can be up to half of that, $0.05$, either side: $8.35 \le l < 8.45$.",
      check=lambda: round(8.35 + 1e-9, 1) == 8.4 and round(8.4499, 1) == 8.4),
])

D[EXP] = ("Simplifying, expanding, factorising, substituting and rearranging formulae.", [
    q(ALG, EXP, 1, r"Simplify $3a + 5b - a + 2b$.", ["$2a + 7b$", "$4a + 7b$", "$2a + 3b$", "$9ab$"], "A",
      r"Collect like terms: $3a - a = 2a$ and $5b + 2b = 7b$.", check=lambda: 3 * 2 + 5 * 3 - 2 + 2 * 3 == 2 * 2 + 7 * 3),
    q(ALG, EXP, 1, r"Work out the value of $3x^2 - 2$ when $x = -4$.", ["$-50$", "$46$", "$142$", "$-46$"], "B",
      r"Square first: $(-4)^2 = 16$. Then $3 \times 16 - 2 = 46$.", check=lambda: 3 * (-4) ** 2 - 2 == 46),
    q(ALG, EXP, 2, r"Factorise $x^2 + 7x + 12$.",
      ["$(x + 2)(x + 6)$", "$(x + 1)(x + 12)$", "$(x + 3)(x + 4)$", "$(x - 3)(x - 4)$"], "C",
      r"Find two numbers that multiply to $12$ and add to $7$: these are $3$ and $4$.",
      check=lambda: all((x + 3) * (x + 4) == x * x + 7 * x + 12 for x in R)),
    q(ALG, EXP, 2, r"Make $r$ the subject of the formula $A = \pi r^2$, where $r > 0$.",
      [r"$r = \sqrt{A\pi}$", r"$r = \dfrac{A}{2\pi}$", r"$r = \dfrac{A^2}{\pi}$", r"$r = \sqrt{\dfrac{A}{\pi}}$"], "D",
      r"Divide both sides by $\pi$ to get $r^2 = \frac{A}{\pi}$, then take the square root.",
      check=lambda: near(math.sqrt(math.pi * 9 / math.pi), 3, 1e-9)),
    q(ALG, EXP, 3, r"Simplify fully $\dfrac{x^2 - 9}{x^2 + 5x + 6}$.",
      [r"$\dfrac{x - 3}{x + 2}$", r"$\dfrac{x + 3}{x + 2}$", r"$\dfrac{x - 3}{x + 3}$", r"$\dfrac{-9}{5x + 6}$"], "A",
      r"Factorise both: $\frac{(x - 3)(x + 3)}{(x + 2)(x + 3)}$. Cancel the common factor $(x + 3)$ to leave $\frac{x - 3}{x + 2}$.",
      check=lambda: Fr(5 ** 2 - 9, 5 ** 2 + 25 + 6) == Fr(5 - 3, 5 + 2)),
])

D[EQN] = ("Solving linear and quadratic equations, simultaneous equations and inequalities.", [
    q(ALG, EQN, 1, r"Solve $3x + 4 = 19$.", ["$x = 5$", "$x = 15$", "$x = 45$", r"$x = \dfrac{23}{3}$"], "A",
      r"Subtract $4$ from both sides: $3x = 15$. Divide by $3$: $x = 5$.", check=lambda: 3 * 5 + 4 == 19),
    q(ALG, EQN, 2, r"Solve the inequality $4x - 3 > 13$.", ["$x < 4$", "$x > 4$", "$x > 2.5$", "$x > 16$"], "B",
      r"Add $3$ to both sides: $4x > 16$. Divide by $4$: $x > 4$.", check=lambda: 4 * 4.1 - 3 > 13 and not 4 * 4 - 3 > 13),
    q(ALG, EQN, 2, r"Solve the simultaneous equations $2x + y = 11$ and $x - y = 1$.",
      [r"$x = 5,\ y = 1$", r"$x = 3,\ y = 5$", r"$x = 4,\ y = 3$", r"$x = 6,\ y = -1$"], "C",
      r"Add the two equations to eliminate $y$: $3x = 12$, so $x = 4$. Substitute into $x - y = 1$ to get $y = 3$.",
      check=lambda: 2 * 4 + 3 == 11 and 4 - 3 == 1),
    q(ALG, EQN, 3, r"Solve $x^2 + 6x - 3 = 0$ by completing the square.",
      [r"$x = 3 \pm 2\sqrt{3}$", r"$x = -3 \pm \sqrt{6}$", r"$x = -6 \pm 2\sqrt{3}$", r"$x = -3 \pm 2\sqrt{3}$"], "D",
      r"$(x + 3)^2 - 9 - 3 = 0$, so $(x + 3)^2 = 12$. Then $x + 3 = \pm\sqrt{12} = \pm 2\sqrt{3}$, giving $x = -3 \pm 2\sqrt{3}$.",
      check=lambda: all(near(x * x + 6 * x - 3, 0, 1e-9) for x in (-3 + 2 * math.sqrt(3), -3 - 2 * math.sqrt(3)))),
    q(ALG, EQN, 3, r"Solve the inequality $x^2 - x - 6 < 0$.",
      ["$-2 < x < 3$", r"$x < -2$ or $x > 3$", "$-3 < x < 2$", "$x < 3$"], "A",
      r"Factorise: $(x - 3)(x + 2) < 0$. The curve crosses the axis at $-2$ and $3$ and is below the axis between them, so $-2 < x < 3$.",
      check=lambda: all((x * x - x - 6 < 0) == (-2 < x < 3) for x in range(-8, 9))),
])

D[SEQ] = ("Term-to-term rules and nth terms of linear, geometric and quadratic sequences.", [
    q(ALG, SEQ, 1, r"What is the next term in the sequence $3,\ 8,\ 13,\ 18,\ \ldots$?", ["$21$", "$23$", "$22$", "$28$"], "B",
      r"The terms go up by $5$ each time, so the next term is $18 + 5 = 23$.", check=lambda: 18 + (8 - 3) == 23),
    q(ALG, SEQ, 1, r"The $n$th term of a sequence is $3n - 1$. What is the 10th term?", ["$31$", "$30$", "$29$", "$13$"], "C",
      r"Substitute $n = 10$: $3 \times 10 - 1 = 29$.", check=lambda: 3 * 10 - 1 == 29),
    q(ALG, SEQ, 2, r"What is the $n$th term of the sequence $20,\ 17,\ 14,\ 11,\ \ldots$?",
      ["$3n + 17$", "$20 - 3n$", "$17 - 3n$", "$23 - 3n$"], "D",
      r"The terms go down by $3$, so the rule starts $-3n$. When $n = 1$, $-3n = -3$, and the first term is $20$, so add $23$: $23 - 3n$.",
      check=lambda: [23 - 3 * n for n in (1, 2, 3, 4)] == [20, 17, 14, 11]),
    q(ALG, SEQ, 2, r"A geometric sequence starts $2,\ 6,\ 18,\ 54,\ \ldots$ What is the 6th term?", ["$486$", "$162$", "$1458$", "$108$"], "A",
      r"Each term is multiplied by $3$. The 5th term is $54 \times 3 = 162$ and the 6th is $162 \times 3 = 486$.",
      check=lambda: 2 * 3 ** 5 == 486),
    q(ALG, SEQ, 3, r"What is the $n$th term of the quadratic sequence $3,\ 8,\ 15,\ 24,\ \ldots$?",
      ["$n^2 + 2$", "$n^2 + 2n$", "$2n^2 + 1$", "$5n - 2$"], "B",
      r"The differences are $5, 7, 9$ and the second difference is $2$, so the rule starts $n^2$. Subtracting $n^2$ ($1, 4, 9, 16$) leaves $2, 4, 6, 8$, which is $2n$.",
      check=lambda: [n * n + 2 * n for n in (1, 2, 3, 4)] == [3, 8, 15, 24]),
])

D[GRA] = ("Straight-line graphs, gradients, quadratic graphs and function notation.", [
    q(ALG, GRA, 1, r"What are the gradient and $y$-intercept of the line $y = 3x - 5$?",
      ["Gradient $-5$, intercept $3$", "Gradient $3$, intercept $5$", "Gradient $3$, intercept $-5$", "Gradient $5$, intercept $3$"], "C",
      r"In $y = mx + c$, $m$ is the gradient and $c$ is the $y$-intercept. Here $m = 3$ and $c = -5$."),
    q(ALG, GRA, 2, r"Which line is parallel to $y = 2x + 1$ and passes through $(0, -4)$?",
      ["$y = 2x - 4$", "$y = -4x + 1$", r"$y = -\dfrac{1}{2}x - 4$", "$y = 2x + 4$"], "A",
      r"Parallel lines have the same gradient, $2$. Passing through $(0, -4)$ means the $y$-intercept is $-4$.",
      check=lambda: 2 * 0 - 4 == -4),
    q(ALG, GRA, 2, r"What is the gradient of a line perpendicular to $y = 4x + 3$?",
      ["$4$", "$-4$", r"$\dfrac{1}{4}$", r"$-\dfrac{1}{4}$"], "D",
      r"Perpendicular gradients multiply to $-1$. Since $4 \times \left(-\frac{1}{4}\right) = -1$, the gradient is $-\frac{1}{4}$.",
      check=lambda: Fr(4) * Fr(-1, 4) == -1),
    q(ALG, GRA, 3, r"What are the coordinates of the turning point of the graph $y = (x - 3)^2 + 2$?",
      ["$(-3, 2)$", "$(3, 2)$", "$(3, -2)$", "$(2, 3)$"], "B",
      r"$(x - 3)^2$ is smallest, zero, when $x = 3$, and then $y = 2$. So the minimum point is $(3, 2)$.",
      check=lambda: min(((x / 10 - 3) ** 2 + 2, x / 10) for x in range(0, 61)) == (2, 3)),
    q(ALG, GRA, 3, r"$f(x) = 2x + 6$. What is $f^{-1}(x)$?",
      [r"$\dfrac{x}{2} + 6$", r"$\dfrac{1}{2x + 6}$", r"$\dfrac{x - 6}{2}$", "$2x - 6$"], "C",
      r"Write $y = 2x + 6$ and rearrange for $x$: $x = \frac{y - 6}{2}$. So $f^{-1}(x) = \frac{x - 6}{2}$.",
      check=lambda: all(((2 * x + 6) - 6) / 2 == x for x in R)),
])

D[RP] = ("Simplifying and sharing in ratios, direct and inverse proportion, scales and compound measures.", [
    q(RAT, RP, 1, r"Write the ratio $18 : 24$ in its simplest form.", ["$3 : 4$", "$9 : 12$", "$4 : 3$", "$6 : 8$"], "A",
      r"Divide both numbers by their highest common factor, $6$: $18 \div 6 = 3$ and $24 \div 6 = 4$.", check=lambda: Fr(18, 24) == Fr(3, 4)),
    q(RAT, RP, 1, "A recipe uses 300 g of flour to make 12 biscuits. How much flour is needed for 20 biscuits?",
      ["180 g", "500 g", "308 g", "720 g"], "B",
      "One biscuit needs 300 divided by 12, which is 25 g. For 20 biscuits: 20 times 25 = 500 g.", check=lambda: 300 / 12 * 20 == 500),
    q(RAT, RP, 2, "It takes 5 workers 12 days to build a wall. How long would 8 workers take, working at the same rate?",
      ["19.2 days", "9 days", "7.5 days", "15 days"], "C",
      "The job is 5 times 12 = 60 worker-days. With 8 workers it takes 60 divided by 8 = 7.5 days. More workers means less time, so this is inverse proportion.",
      check=lambda: 5 * 12 / 8 == 7.5),
    q(RAT, RP, 2, r"A map has a scale of $1 : 25\,000$. Two villages are $6\ \text{cm}$ apart on the map. What is the real distance between them?",
      ["150 km", "15 km", "0.15 km", "1.5 km"], "D",
      r"$6 \times 25\,000 = 150\,000\ \text{cm}$. Divide by $100$ for metres ($1500\ \text{m}$), then by $1000$ for kilometres: $1.5\ \text{km}$.",
      check=lambda: 6 * 25000 / 100 / 1000 == 1.5),
    q(RAT, RP, 3, r"$y$ is directly proportional to $x^2$. When $x = 2$, $y = 20$. What is $y$ when $x = 5$?", ["$125$", "$50$", "$100$", "$500$"], "A",
      r"Write $y = kx^2$. Using $x = 2$, $y = 20$: $k = 5$. When $x = 5$, $y = 5 \times 25 = 125$.", check=lambda: 20 / 2 ** 2 * 5 ** 2 == 125),
])

D[PCT] = ("Percentage increase and decrease, reverse percentages, and compound growth and decay.", [
    q(RAT, PCT, 1, r"Increase $60$ by $20\%$.", ["$80$", "$72$", "$62$", "$12$"], "B",
      r"$20\%$ of $60$ is $12$, so the new amount is $60 + 12 = 72$. You can also multiply by $1.2$.", check=lambda: near(60 * 1.2, 72, 1e-9)),
    q(RAT, PCT, 2, "The price of a jacket falls from £80 to £68. What is the percentage decrease?", ["12%", "17.6%", "15%", "85%"], "C",
      "The decrease is £12. As a percentage of the original price: 12 divided by 80 is 0.15, which is 15%. Always divide by the original amount.",
      check=lambda: (80 - 68) / 80 == 0.15),
    q(RAT, PCT, 2, "After a 25% increase, the price of a ticket is £150. What was the price before the increase?",
      ["£112.50", "£187.50", "£125", "£120"], "D",
      "The new price is 125% of the original, so divide by 1.25: 150 divided by 1.25 = £120. Taking 25% off £150 gives the wrong answer.",
      check=lambda: 150 / 1.25 == 120),
    q(RAT, PCT, 2, "A car costs £12 000 and loses 10% of its value each year. What is it worth after 2 years?",
      ["£9720", "£9600", "£10 800", "£9000"], "A",
      r"Multiply by $0.9$ for each year: $12\,000 \times 0.9^2 = 9720$. Taking off $20\%$ in one go is not correct.",
      check=lambda: near(12000 * 0.9 ** 2, 9720, 1e-6)),
    q(RAT, PCT, 3, "A town has a population of 5000, which grows by 4% each year. After how many whole years does the population first exceed 6000?",
      ["4 years", "5 years", "6 years", "3 years"], "B",
      r"After $4$ years: $5000 \times 1.04^4 \approx 5849$. After $5$ years: $5000 \times 1.04^5 \approx 6083$, which is the first value above $6000$.",
      check=lambda: 5000 * 1.04 ** 4 < 6000 < 5000 * 1.04 ** 5),
])

D[ANG] = ("Angle facts, polygons, parallel lines, bearings and circle theorems.", [
    q(GEO, ANG, 1, r"Two angles of a triangle are $47^\circ$ and $68^\circ$. What is the third angle?",
      [r"$75^\circ$", r"$245^\circ$", r"$65^\circ$", r"$115^\circ$"], "C",
      r"Angles in a triangle add up to $180^\circ$: $180 - 47 - 68 = 65^\circ$.", check=lambda: 180 - 47 - 68 == 65),
    q(GEO, ANG, 1, "What is the sum of the interior angles of a hexagon?",
      [r"$360^\circ$", r"$540^\circ$", r"$1080^\circ$", r"$720^\circ$"], "D",
      r"The sum is $(n - 2) \times 180^\circ$. For a hexagon, $n = 6$: $4 \times 180 = 720^\circ$.", check=lambda: (6 - 2) * 180 == 720),
    q(GEO, ANG, 2, r"An isosceles triangle has one angle of $40^\circ$ between its two equal sides. What is the size of each of the other two angles?",
      [r"$70^\circ$", r"$40^\circ$", r"$140^\circ$", r"$100^\circ$"], "A",
      r"The other two angles are equal and add up to $180 - 40 = 140^\circ$, so each is $70^\circ$.", check=lambda: (180 - 40) / 2 == 70),
    q(GEO, ANG, 2, "What is the size of each exterior angle of a regular decagon (10 sides)?",
      [r"$144^\circ$", r"$36^\circ$", r"$18^\circ$", r"$30^\circ$"], "B",
      r"Exterior angles of any polygon add up to $360^\circ$. For a regular decagon each one is $360 \div 10 = 36^\circ$.", check=lambda: 360 / 10 == 36),
    q(GEO, ANG, 3, r"Points $A$, $B$ and $C$ lie on a circle with centre $O$. Angle $AOB = 124^\circ$, and $C$ is on the major arc $AB$. What is angle $ACB$?",
      [r"$124^\circ$", r"$248^\circ$", r"$62^\circ$", r"$56^\circ$"], "C",
      r"The angle at the centre is twice the angle at the circumference standing on the same arc, so angle $ACB = 124 \div 2 = 62^\circ$.",
      check=lambda: 124 / 2 == 62),
])

D[AREA] = ("Perimeter, area and volume, and Pythagoras' theorem.", [
    q(GEO, AREA, 1, r"A triangle has base $10\ \text{cm}$ and perpendicular height $7\ \text{cm}$. What is its area?",
      [r"$70\ \text{cm}^2$", r"$17\ \text{cm}^2$", r"$34\ \text{cm}^2$", r"$35\ \text{cm}^2$"], "D",
      r"Area of a triangle is $\frac{1}{2} \times \text{base} \times \text{height} = \frac{1}{2} \times 10 \times 7 = 35\ \text{cm}^2$.", check=lambda: 10 * 7 / 2 == 35),
    q(GEO, AREA, 2, r"What is the circumference of a circle of radius $6\ \text{cm}$, in terms of $\pi$?",
      [r"$12\pi\ \text{cm}$", r"$6\pi\ \text{cm}$", r"$36\pi\ \text{cm}$", r"$3\pi\ \text{cm}$"], "A",
      r"Circumference is $2\pi r = 2 \times \pi \times 6 = 12\pi\ \text{cm}$. Note that $36\pi$ would be the area.", check=lambda: 2 * 6 == 12),
    q(GEO, AREA, 2, r"The two shorter sides of a right-angled triangle are $5\ \text{cm}$ and $12\ \text{cm}$. How long is the hypotenuse?",
      [r"$17\ \text{cm}$", r"$13\ \text{cm}$", r"$169\ \text{cm}$", r"$10.9\ \text{cm}$"], "B",
      r"By Pythagoras, $c^2 = 5^2 + 12^2 = 25 + 144 = 169$, so $c = 13\ \text{cm}$.", check=lambda: math.hypot(5, 12) == 13),
    q(GEO, AREA, 2, r"A trapezium has parallel sides of $6\ \text{cm}$ and $10\ \text{cm}$, and a perpendicular height of $4\ \text{cm}$. What is its area?",
      [r"$64\ \text{cm}^2$", r"$240\ \text{cm}^2$", r"$32\ \text{cm}^2$", r"$20\ \text{cm}^2$"], "C",
      r"Area of a trapezium is $\frac{1}{2}(a + b)h = \frac{1}{2} \times (6 + 10) \times 4 = 32\ \text{cm}^2$.", check=lambda: (6 + 10) * 4 / 2 == 32),
    q(GEO, AREA, 3, r"What is the volume of a sphere of radius $3\ \text{cm}$, in terms of $\pi$? (Volume of a sphere $= \frac{4}{3}\pi r^3$)",
      [r"$9\pi\ \text{cm}^3$", r"$12\pi\ \text{cm}^3$", r"$108\pi\ \text{cm}^3$", r"$36\pi\ \text{cm}^3$"], "D",
      r"$\frac{4}{3} \times \pi \times 3^3 = \frac{4}{3} \times 27\pi = 36\pi\ \text{cm}^3$.", check=lambda: Fr(4, 3) * 27 == 36),
])

D[TRIG] = ("SOHCAHTOA, exact values, and the sine and cosine rules.", [
    q(GEO, TRIG, 1, r"In a right-angled triangle, which ratio gives $\tan x$?",
      ["Opposite ÷ adjacent", "Opposite ÷ hypotenuse", "Adjacent ÷ hypotenuse", "Adjacent ÷ opposite"], "A",
      "Tangent is opposite divided by adjacent (the TOA in SOHCAHTOA). Opposite over hypotenuse is sine and adjacent over hypotenuse is cosine."),
    q(GEO, TRIG, 2, r"In a right-angled triangle, the side adjacent to a $40^\circ$ angle is $8\ \text{cm}$. How long is the side opposite the angle, to 3 significant figures?",
      [r"$9.53\ \text{cm}$", r"$6.71\ \text{cm}$", r"$5.14\ \text{cm}$", r"$6.13\ \text{cm}$"], "B",
      r"Opposite and adjacent means tangent: $\text{opp} = 8 \tan 40^\circ = 6.71\ \text{cm}$.", check=lambda: round(8 * tan(40), 2) == 6.71),
    q(GEO, TRIG, 2, r"In a right-angled triangle, the side opposite angle $x$ is $5\ \text{cm}$ and the hypotenuse is $13\ \text{cm}$. What is $x$, to 1 decimal place?",
      [r"$67.4^\circ$", r"$21.0^\circ$", r"$22.6^\circ$", r"$0.4^\circ$"], "C",
      r"$\sin x = \frac{5}{13}$, so $x = \sin^{-1}\left(\frac{5}{13}\right) = 22.6^\circ$.", check=lambda: round(math.degrees(math.asin(5 / 13)), 1) == 22.6),
    q(GEO, TRIG, 2, r"What is the exact value of $\cos 60^\circ$?",
      [r"$\dfrac{\sqrt{3}}{2}$", "$1$", r"$\dfrac{\sqrt{2}}{2}$", r"$\dfrac{1}{2}$"], "D",
      r"$\cos 60^\circ = \frac{1}{2}$. The value $\frac{\sqrt{3}}{2}$ is $\cos 30^\circ$, which is the same as $\sin 60^\circ$.", check=lambda: near(cos(60), 0.5, 1e-9)),
    q(GEO, TRIG, 3, r"In triangle $ABC$, $a = 7\ \text{cm}$, $b = 9\ \text{cm}$ and angle $C = 60^\circ$. What is the length of side $c$, to 3 significant figures?",
      [r"$8.19\ \text{cm}$", r"$67.0\ \text{cm}$", r"$11.4\ \text{cm}$", r"$13.9\ \text{cm}$"], "A",
      r"Use the cosine rule: $c^2 = 7^2 + 9^2 - 2 \times 7 \times 9 \times \cos 60^\circ = 49 + 81 - 63 = 67$. So $c = \sqrt{67} = 8.19\ \text{cm}$.",
      check=lambda: round(math.sqrt(49 + 81 - 2 * 7 * 9 * cos(60)), 2) == 8.19),
])

D[VEC] = ("Column vectors, translations, reflections, rotations and enlargements.", [
    q(GEO, VEC, 1, r"The point $(2, 5)$ is translated by the vector $\begin{pmatrix} 4 \\ -3 \end{pmatrix}$. What are its new coordinates?",
      ["$(6, 8)$", "$(6, 2)$", "$(-2, 8)$", "$(8, -15)$"], "B",
      r"Add $4$ to the $x$-coordinate and subtract $3$ from the $y$-coordinate: $(2 + 4,\ 5 - 3) = (6, 2)$.", check=lambda: (2 + 4, 5 - 3) == (6, 2)),
    q(GEO, VEC, 2, r"Work out $\begin{pmatrix} 2 \\ -1 \end{pmatrix} + \begin{pmatrix} -5 \\ 4 \end{pmatrix}$.",
      [r"$\begin{pmatrix} 7 \\ -5 \end{pmatrix}$", r"$\begin{pmatrix} -10 \\ -4 \end{pmatrix}$",
       r"$\begin{pmatrix} -3 \\ 3 \end{pmatrix}$", r"$\begin{pmatrix} 3 \\ -3 \end{pmatrix}$"], "C",
      r"Add the top numbers and add the bottom numbers: $2 + (-5) = -3$ and $-1 + 4 = 3$.", check=lambda: (2 - 5, -1 + 4) == (-3, 3)),
    q(GEO, VEC, 2, r"The point $(3, -2)$ is reflected in the $x$-axis. What are the coordinates of its image?",
      ["$(-3, -2)$", "$(-3, 2)$", "$(-2, 3)$", "$(3, 2)$"], "D",
      r"Reflecting in the $x$-axis keeps the $x$-coordinate the same and changes the sign of the $y$-coordinate: $(3, 2)$."),
    q(GEO, VEC, 2, r"A shape of area $5\ \text{cm}^2$ is enlarged by scale factor $3$. What is the area of the enlarged shape?",
      [r"$45\ \text{cm}^2$", r"$15\ \text{cm}^2$", r"$8\ \text{cm}^2$", r"$125\ \text{cm}^2$"], "A",
      r"Lengths are multiplied by $3$, so areas are multiplied by $3^2 = 9$: $5 \times 9 = 45\ \text{cm}^2$.", check=lambda: 5 * 3 ** 2 == 45),
    q(GEO, VEC, 3, r"What is the magnitude of the vector $\begin{pmatrix} 5 \\ -12 \end{pmatrix}$?", ["$7$", "$13$", "$17$", "$169$"], "B",
      r"Use Pythagoras: $\sqrt{5^2 + (-12)^2} = \sqrt{25 + 144} = \sqrt{169} = 13$.", check=lambda: math.hypot(5, -12) == 13),
])

D[PROB] = ("Single events, expected outcomes, independent events and tree diagrams.", [
    q(PS, PROB, 1, "A bag contains 3 red, 5 blue and 2 green counters. One counter is taken at random. What is the probability that it is blue?",
      [r"$\dfrac{1}{5}$", r"$\dfrac{5}{8}$", r"$\dfrac{1}{2}$", r"$\dfrac{3}{10}$"], "C",
      r"There are $10$ counters and $5$ are blue, so the probability is $\frac{5}{10} = \frac{1}{2}$.", check=lambda: Fr(5, 3 + 5 + 2) == Fr(1, 2)),
    q(PS, PROB, 1, r"The probability that it rains tomorrow is $0.35$. What is the probability that it does not rain?",
      ["$0.35$", "$0.75$", "$1.35$", "$0.65$"], "D",
      r"The probabilities of an event happening and not happening add up to $1$: $1 - 0.35 = 0.65$.", check=lambda: near(1 - 0.35, 0.65, 1e-9)),
    q(PS, PROB, 2, "A fair coin is flipped and a fair six-sided dice is rolled. What is the probability of getting a head and a 6?",
      [r"$\dfrac{1}{12}$", r"$\dfrac{2}{3}$", r"$\dfrac{1}{8}$", r"$\dfrac{1}{6}$"], "A",
      r"The events are independent, so multiply: $\frac{1}{2} \times \frac{1}{6} = \frac{1}{12}$.", check=lambda: Fr(1, 2) * Fr(1, 6) == Fr(1, 12)),
    q(PS, PROB, 2, r"A biased spinner lands on red with probability $0.2$. It is spun $150$ times. How many times would you expect it to land on red?",
      ["$20$", "$30$", "$75$", "$3$"], "B",
      r"Expected number is probability times number of trials: $0.2 \times 150 = 30$.", check=lambda: near(0.2 * 150, 30, 1e-9)),
    q(PS, PROB, 3, "A bag contains 4 red and 6 blue counters. Two counters are taken at random without replacement. What is the probability of getting one of each colour?",
      [r"$\dfrac{4}{15}$", r"$\dfrac{6}{25}$", r"$\dfrac{8}{15}$", r"$\dfrac{12}{25}$"], "C",
      r"Red then blue: $\frac{4}{10} \times \frac{6}{9} = \frac{24}{90}$. Blue then red: $\frac{6}{10} \times \frac{4}{9} = \frac{24}{90}$. Add them: $\frac{48}{90} = \frac{8}{15}$.",
      check=lambda: 2 * Fr(4, 10) * Fr(6, 9) == Fr(8, 15)),
])

D[STAT] = ("Averages and range, frequency tables, charts, and histograms.", [
    q(PS, STAT, 1, r"What is the median of $3,\ 7,\ 8,\ 12,\ 15$?", ["$9$", "$12$", "$7$", "$8$"], "D",
      r"The numbers are already in order and the middle one of the five is $8$. Note that $9$ is the mean.", check=lambda: sorted([3, 7, 8, 12, 15])[2] == 8),
    q(PS, STAT, 1, r"What is the range of $4,\ 9,\ 2,\ 11,\ 6$?", ["$9$", "$6$", "$11$", "$6.4$"], "A",
      r"The range is the largest value minus the smallest: $11 - 2 = 9$.", check=lambda: max(4, 9, 2, 11, 6) - min(4, 9, 2, 11, 6) == 9),
    q(PS, STAT, 2, r"""The table shows the number of goals scored in 10 matches.

| Goals | 1 | 2 | 3 |
| - | - | - | - |
| Frequency | 4 | 5 | 1 |

What is the mean number of goals per match?""", ["$2$", "$1.7$", "$3.3$", "$0.6$"], "B",
      r"Total goals $= (1 \times 4) + (2 \times 5) + (3 \times 1) = 17$. Divide by the $10$ matches: $17 \div 10 = 1.7$.",
      check=lambda: (1 * 4 + 2 * 5 + 3 * 1) / 10 == 1.7),
    q(PS, STAT, 2, "In a survey of 60 people, 15 chose tea. What angle should represent tea on a pie chart?",
      [r"$15^\circ$", r"$25^\circ$", r"$90^\circ$", r"$60^\circ$"], "C",
      r"The fraction choosing tea is $\frac{15}{60} = \frac{1}{4}$, and a quarter of $360^\circ$ is $90^\circ$.", check=lambda: 15 / 60 * 360 == 90),
    q(PS, STAT, 3, "On a histogram, a class has width 20 and frequency 30. What is the frequency density for this class?",
      ["$600$", "$50$", "$0.67$", "$1.5$"], "D",
      r"Frequency density is frequency divided by class width: $30 \div 20 = 1.5$. On a histogram the area of each bar, not its height, shows the frequency.",
      check=lambda: 30 / 20 == 1.5),
])

save_drills("gcse-maths", D)
