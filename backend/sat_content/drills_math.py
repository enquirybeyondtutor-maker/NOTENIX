r"""SAT skill drills, Math: 6 original questions per skill (19 skills), difficulty 1 -> 3.
Imported by drills.py; every `check` is verified on import."""
import math
from fractions import Fraction as F
from _sat import mq, spr

ALG, ADV, PSDA, GEO = "Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"
D = {}

S = "Linear equations in one variable"
D[S] = [
    mq(ALG, S, 1, r"If $x + 9 = 15$, what is the value of $x$?", ["$6$", "$9$", "$15$", "$24$"], "A", r"Subtract $9$ from both sides: $x = 6$.", check=lambda: 6 + 9 == 15),
    mq(ALG, S, 1, r"If $6x = 42$, what is the value of $x$?", ["$6$", "$7$", "$36$", "$48$"], "B", r"Divide both sides by $6$: $x = 7$.", check=lambda: 6 * 7 == 42),
    spr(ALG, S, 2, r"If $5(x - 2) = 3x + 6$, what is the value of $x$?", ["8"], r"$5x - 10 = 3x + 6$, so $2x = 16$ and $x = 8$.", check=lambda: 5 * (8 - 2) == 3 * 8 + 6),
    mq(ALG, S, 2, r"If $\dfrac{x}{3} + 4 = 10$, what is the value of $x$?", ["$2$", "$6$", "$18$", "$42$"], "C", r"$\frac{x}{3} = 6$, so $x = 18$.", check=lambda: 18 / 3 + 4 == 10),
    mq(ALG, S, 3, r"For what value of $k$ does the equation $3(x + k) = 3x + 12$ have infinitely many solutions?", ["$3$", "$4$", "$9$", "$12$"], "B",
       r"$3x + 3k = 3x + 12$ holds for every $x$ only when $3k = 12$, so $k = 4$.", check=lambda: 3 * 4 == 12),
    mq(ALG, S, 3, r"How many solutions does the equation $2(3x - 1) = 6x + 5$ have?", ["Zero", "Exactly one", "Exactly two", "Infinitely many"], "A",
       r"$6x - 2 = 6x + 5$ simplifies to $-2 = 5$, which is never true, so there are no solutions.", check=lambda: -2 != 5),
]

S = "Linear functions"
D[S] = [
    mq(ALG, S, 1, r"If $f(x) = 2x + 7$, what is $f(5)$?", ["$12$", "$14$", "$17$", "$19$"], "C", r"$f(5) = 2(5) + 7 = 17$.", check=lambda: 2 * 5 + 7 == 17),
    mq(ALG, S, 1, r"A taxi charges $\$3$ plus $\$2$ per mile. Which function gives the cost $C$ of a ride of $m$ miles?",
       [r"$C = 3m + 2$", r"$C = 2m + 3$", r"$C = 5m$", r"$C = 2 + m$"], "B", r"The fixed $\$3$ is the starting amount and $\$2$ is added per mile: $C = 2m + 3$.", check=lambda: 2 * 4 + 3 == 11),
    spr(ALG, S, 2, r"The function $g$ is linear, $g(0) = 4$ and $g(2) = 10$. What is $g(5)$?", ["19"],
        r"The slope is $\frac{10 - 4}{2} = 3$, so $g(x) = 3x + 4$ and $g(5) = 19$.", check=lambda: 3 * 5 + 4 == 19),
    mq(ALG, S, 2, r"A phone's battery is at $90\%$ and drops $15$ percentage points per hour of use. After how many hours of use will it be at $30\%$?",
       ["$3$", "$4$", "$5$", "$6$"], "B", r"$90 - 15h = 30$, so $15h = 60$ and $h = 4$.", check=lambda: 90 - 15 * 4 == 30),
    mq(ALG, S, 3, r"For the linear function $h$, $h(3) = 11$ and $h(7) = 23$. What is the value of $h(0)$?", ["$-1$", "$2$", "$5$", "$8$"], "B",
       r"Slope $= \frac{23 - 11}{7 - 3} = 3$. Then $h(0) = 11 - 3(3) = 2$.", check=lambda: 11 - 3 * 3 == 2 and 2 + 3 * 7 == 23),
    mq(ALG, S, 3, r"A plant is $12$ cm tall and grows $1.5$ cm per week. A second plant is $3$ cm tall and grows $3$ cm per week. After how many weeks will they be the same height?",
       ["$4$", "$5$", "$6$", "$9$"], "C", r"$12 + 1.5w = 3 + 3w$ gives $9 = 1.5w$, so $w = 6$.", check=lambda: 12 + 1.5 * 6 == 3 + 3 * 6),
]

S = "Linear equations in two variables"
D[S] = [
    mq(ALG, S, 1, r"What is the slope of the line $y = -4x + 9$?", ["$-4$", "$4$", "$9$", "$-9$"], "A", r"In $y = mx + b$, the slope is $m = -4$.", check=lambda: True),
    mq(ALG, S, 1, r"What is the $y$-intercept of the line $y = 3x - 5$?", [r"$(0, -5)$", r"$(0, 3)$", r"$(-5, 0)$", r"$(3, 0)$"], "A", r"When $x = 0$, $y = -5$.", check=lambda: 3 * 0 - 5 == -5),
    spr(ALG, S, 2, r"The line $4x + 2y = 18$ crosses the $y$-axis at $(0, b)$. What is $b$?", ["9"], r"Set $x = 0$: $2y = 18$, so $y = 9$.", check=lambda: 4 * 0 + 2 * 9 == 18),
    mq(ALG, S, 2, r"Pens cost $\$2$ and notebooks cost $\$5$. Ana spends exactly $\$31$ and buys $3$ notebooks. How many pens does she buy?", ["$6$", "$7$", "$8$", "$9$"], "C",
       r"$2p + 5(3) = 31$, so $2p = 16$ and $p = 8$.", check=lambda: 2 * 8 + 15 == 31),
    mq(ALG, S, 3, r"What is the slope of the line $3x - 6y = 12$?", [r"$-2$", r"$-\dfrac{1}{2}$", r"$\dfrac{1}{2}$", r"$2$"], "C",
       r"Solve for $y$: $y = \frac{1}{2}x - 2$. The slope is $\frac{1}{2}$.", check=lambda: F(3, 6) == F(1, 2)),
    mq(ALG, S, 3, r"Line $p$ passes through $(2, 3)$ and is perpendicular to $y = \dfrac{2}{3}x + 1$. What is the $y$-intercept of line $p$?", ["$0$", "$3$", "$5$", "$6$"], "D",
       r"Perpendicular slope is $-\frac{3}{2}$. $y - 3 = -\frac{3}{2}(x - 2)$, so $y = -\frac{3}{2}x + 6$. The $y$-intercept is $6$.", check=lambda: F(-3, 2) * 2 + 6 == 3),
]

S = "Systems of linear equations"
D[S] = [
    mq(ALG, S, 1, r"""$x + y = 9$
$x - y = 3$

What is the value of $x$?""", ["$3$", "$5$", "$6$", "$9$"], "C", r"Add the equations: $2x = 12$, so $x = 6$.", check=lambda: 6 + 3 == 9 and 6 - 3 == 3),
    mq(ALG, S, 1, r"""$y = x + 2$
$y = 3x - 4$

What is the value of $x$ in the solution?""", ["$1$", "$2$", "$3$", "$5$"], "C", r"$x + 2 = 3x - 4$, so $2x = 6$ and $x = 3$.", check=lambda: 3 + 2 == 3 * 3 - 4),
    spr(ALG, S, 2, r"""$2x + 3y = 13$
$x + 3y = 8$

What is the value of $y$?""", ["1"], r"Subtract the second equation from the first: $x = 5$. Then $5 + 3y = 8$, so $y = 1$.", check=lambda: 2 * 5 + 3 * 1 == 13 and 5 + 3 * 1 == 8),
    mq(ALG, S, 2, r"A theatre sold $200$ tickets. Adult tickets cost $\$10$ and child tickets $\$6$, and sales totalled $\$1{,}600$. How many adult tickets were sold?",
       ["$80$", "$100$", "$120$", "$150$"], "B", r"$a + c = 200$ and $10a + 6c = 1600$. Then $10a + 6(200 - a) = 1600$, so $4a = 400$ and $a = 100$.",
       check=lambda: 10 * 100 + 6 * 100 == 1600),
    mq(ALG, S, 3, r"""$3x - 2y = 4$
$6x - 4y = c$

For which value of $c$ does the system have infinitely many solutions?""", ["$2$", "$4$", "$8$", "$12$"], "C",
       r"The second equation must be the first doubled: $c = 2 \times 4 = 8$.", check=lambda: 2 * 4 == 8),
    mq(ALG, S, 3, r"""$ax + 2y = 5$
$3x + 6y = 1$

For which value of $a$ does the system have no solution?""", ["$1$", "$2$", "$3$", "$6$"], "A",
       r"Parallel lines need $\frac{a}{3} = \frac{2}{6}$, so $a = 1$. Then the constants differ ($5$ vs $\frac{1}{3}$ after scaling), so there is no solution.",
       check=lambda: F(1, 3) == F(2, 6) and F(5, 1) != F(1, 3)),
]

S = "Linear inequalities"
D[S] = [
    mq(ALG, S, 1, r"Which value of $x$ satisfies $x - 4 > 6$?", ["$8$", "$9$", "$10$", "$11$"], "D", r"$x > 10$, so only $11$ works.", check=lambda: 11 - 4 > 6 and not 10 - 4 > 6),
    mq(ALG, S, 1, r"Which inequality means \"$y$ is at least $12$\"?", [r"$y > 12$", r"$y < 12$", r"$y \ge 12$", r"$y \le 12$"], "C", r"\"At least $12$\" means $12$ or more: $y \ge 12$.", check=lambda: True),
    spr(ALG, S, 2, r"What is the greatest integer $x$ for which $3x + 5 \le 26$?", ["7"], r"$3x \le 21$, so $x \le 7$.", check=lambda: 3 * 7 + 5 <= 26 < 3 * 8 + 5),
    mq(ALG, S, 2, r"Which value of $x$ satisfies $-2x + 3 < -5$?", ["$2$", "$3$", "$4$", "$5$"], "D", r"$-2x < -8$, so $x > 4$ (dividing by a negative flips the sign). Only $5$ works.",
       check=lambda: -2 * 5 + 3 < -5 and not -2 * 4 + 3 < -5),
    mq(ALG, S, 3, r"A van carries at most $900$ kg. The driver weighs $80$ kg and each crate weighs $35$ kg. What is the greatest number of crates the van can carry with the driver?",
       ["$22$", "$23$", "$24$", "$25$"], "B", r"$80 + 35c \le 900$ gives $35c \le 820$, so $c \le 23.4$ and the greatest is $23$.",
       check=lambda: 80 + 35 * 23 <= 900 < 80 + 35 * 24),
    mq(ALG, S, 3, r"Which point satisfies both $y < x + 1$ and $y > -2x + 4$?", [r"$(0, 0)$", r"$(1, 1)$", r"$(2, 2)$", r"$(3, 5)$"], "C",
       r"$(2, 2)$: $2 < 3$ and $2 > 0$, both true. $(3, 5)$ fails $5 < 4$; $(0, 0)$ and $(1, 1)$ fail the second inequality.",
       check=lambda: 2 < 2 + 1 and 2 > -2 * 2 + 4 and not 5 < 3 + 1 and not 0 > 4 and not 1 > 2),
]

S = "Nonlinear functions"
D[S] = [
    mq(ADV, S, 1, r"If $f(x) = x^2 + 3$, what is $f(4)$?", ["$11$", "$16$", "$19$", "$22$"], "C", r"$f(4) = 16 + 3 = 19$.", check=lambda: 4 ** 2 + 3 == 19),
    mq(ADV, S, 1, r"An investment of $\$1{,}000$ doubles every $8$ years. What will it be worth after $16$ years?", [r"$\$2{,}000$", r"$\$3{,}000$", r"$\$4{,}000$", r"$\$16{,}000$"], "C",
       r"$16$ years is two doubling periods: $1{,}000 \times 2 \times 2 = 4{,}000$.", check=lambda: 1000 * 2 ** 2 == 4000),
    spr(ADV, S, 2, r"The graph of $y = (x - 5)^2 - 3$ has its vertex at $(h, k)$. What is $h + k$?", ["2"], r"The vertex is $(5, -3)$, so $h + k = 2$.", check=lambda: 5 + (-3) == 2),
    mq(ADV, S, 2, r"The function $f(x) = 500(0.8)^x$ models a value after $x$ years. By what percentage does the value decrease each year?",
       [r"$0.8\%$", r"$8\%$", r"$20\%$", r"$80\%$"], "C", r"Each year keeps $80\%$ of the value, so it decreases by $20\%$.", check=lambda: math.isclose(500 - 500 * 0.8, 0.20 * 500)),
    mq(ADV, S, 3, r"The function $f(x) = x^2 - 8x + 12$. For what value of $x$ does $f$ reach its minimum?", ["$2$", "$4$", "$6$", "$8$"], "B",
       r"The vertex is at $x = -\frac{-8}{2(1)} = 4$.", check=lambda: min(range(-20, 20), key=lambda x: x * x - 8 * x + 12) == 4),
    mq(ADV, S, 3, r"For $g(x) = 2^x$, what is $g(x + 3)$ equal to?", [r"$g(x) + 3$", r"$g(x) + 8$", r"$3g(x)$", r"$8g(x)$"], "D",
       r"$2^{x + 3} = 2^x \cdot 2^3 = 8 \cdot 2^x = 8g(x)$.", check=lambda: 2 ** (5 + 3) == 8 * 2 ** 5),
]

S = "Nonlinear equations and systems"
D[S] = [
    mq(ADV, S, 1, r"What are the solutions to $x^2 = 36$?", [r"$6$ only", r"$-6$ and $6$", r"$18$ only", r"$-18$ and $18$"], "B", r"Both $6^2$ and $(-6)^2$ equal $36$.", check=lambda: 6 ** 2 == 36 == (-6) ** 2),
    mq(ADV, S, 1, r"What are the solutions to $(x - 2)(x + 5) = 0$?", [r"$x = -2$ and $x = 5$", r"$x = 2$ and $x = -5$", r"$x = 2$ and $x = 5$", r"$x = -2$ and $x = -5$"], "B",
       r"A product is zero when a factor is zero: $x = 2$ or $x = -5$.", check=lambda: (2 - 2) * (2 + 5) == 0 == (-5 - 2) * (-5 + 5)),
    spr(ADV, S, 2, r"What is the positive solution of $x^2 + 3x - 28 = 0$?", ["4"], r"$(x + 7)(x - 4) = 0$, so $x = 4$ or $x = -7$.", check=lambda: 16 + 12 - 28 == 0),
    mq(ADV, S, 2, r"""$y = x^2$
$y = 2x + 3$

What is the positive $x$-value of a solution to the system?""", ["$1$", "$2$", "$3$", "$5$"], "C",
       r"$x^2 = 2x + 3$ gives $x^2 - 2x - 3 = 0$, $(x - 3)(x + 1) = 0$, so $x = 3$.", check=lambda: 9 == 2 * 3 + 3),
    spr(ADV, S, 3, r"What is the sum of the solutions of $2x^2 - 10x + 7 = 0$?", ["5"], r"For $ax^2 + bx + c = 0$ the sum of the solutions is $-\frac{b}{a} = \frac{10}{2} = 5$.",
        check=lambda: math.isclose(sum(((10 + s * math.sqrt(100 - 56)) / 4) for s in (1, -1)), 5)),
    mq(ADV, S, 3, r"For which value of $c$ does $x^2 + 10x + c = 0$ have exactly one real solution?", ["$5$", "$10$", "$20$", "$25$"], "D",
       r"One solution means the discriminant is zero: $100 - 4c = 0$, so $c = 25$.", check=lambda: 100 - 4 * 25 == 0),
]

S = "Equivalent expressions"
D[S] = [
    mq(ADV, S, 1, r"Which expression is equivalent to $3x + 2x - 4$?", [r"$5x - 4$", r"$x - 4$", r"$6x - 4$", r"$5x + 4$"], "A", r"Combine like terms: $3x + 2x = 5x$.", check=lambda: all(3 * x + 2 * x - 4 == 5 * x - 4 for x in range(5))),
    mq(ADV, S, 1, r"Which expression is equivalent to $(x + 3)(x + 2)$?", [r"$x^2 + 6$", r"$x^2 + 5x + 6$", r"$x^2 + 6x + 5$", r"$2x + 5$"], "B",
       r"$x^2 + 2x + 3x + 6 = x^2 + 5x + 6$.", check=lambda: all((x + 3) * (x + 2) == x * x + 5 * x + 6 for x in range(-4, 4))),
    mq(ADV, S, 2, r"Which expression is equivalent to $4x^2 - 9$?", [r"$(2x - 3)^2$", r"$(4x - 3)(x + 3)$", r"$(2x - 3)(2x + 3)$", r"$(4x - 9)(x + 1)$"], "C",
       r"Difference of squares: $(2x)^2 - 3^2 = (2x - 3)(2x + 3)$.", check=lambda: all(4 * x * x - 9 == (2 * x - 3) * (2 * x + 3) for x in range(-4, 4))),
    mq(ADV, S, 2, r"Which expression is equivalent to $\dfrac{x^5}{x^2}$ for $x \ne 0$?", [r"$x^{3}$", r"$x^{7}$", r"$x^{10}$", r"$x^{2.5}$"], "A", r"Subtract exponents: $x^{5 - 2} = x^3$.", check=lambda: 3 ** 5 / 3 ** 2 == 3 ** 3),
    spr(ADV, S, 3, r"If $(x + a)^2 = x^2 + 14x + 49$ for all $x$, what is the value of $a$?", ["7"], r"$(x + a)^2 = x^2 + 2ax + a^2$, so $2a = 14$ and $a = 7$.", check=lambda: 2 * 7 == 14 and 7 ** 2 == 49),
    mq(ADV, S, 3, r"Which expression is equivalent to $\left(9x^4\right)^{1/2}$ for $x > 0$?", [r"$3x^2$", r"$9x^2$", r"$3x^4$", r"$4.5x^2$"], "A",
       r"$9^{1/2} = 3$ and $(x^4)^{1/2} = x^2$.", check=lambda: math.isclose((9 * 2 ** 4) ** 0.5, 3 * 2 ** 2)),
]

S = "Ratios, rates and units"
D[S] = [
    mq(PSDA, S, 1, r"A recipe uses $2$ eggs for $12$ muffins. How many eggs are needed for $36$ muffins?", ["$4$", "$6$", "$8$", "$12$"], "B", r"$36$ is $3$ times $12$, so use $3 \times 2 = 6$ eggs.", check=lambda: 2 * 36 / 12 == 6),
    mq(PSDA, S, 1, r"A car travels $150$ miles in $3$ hours. What is its average speed?", [r"$45$ mph", r"$50$ mph", r"$60$ mph", r"$450$ mph"], "B", r"$150 \div 3 = 50$ miles per hour.", check=lambda: 150 / 3 == 50),
    spr(PSDA, S, 2, r"How many minutes are in $3.5$ hours?", ["210"], r"$3.5 \times 60 = 210$.", check=lambda: 3.5 * 60 == 210),
    mq(PSDA, S, 2, r"The ratio of boys to girls in a club is $3 : 5$. There are $40$ members. How many are girls?", ["$15$", "$24$", "$25$", "$30$"], "C",
       r"$5$ of every $8$ members are girls: $\frac{5}{8} \times 40 = 25$.", check=lambda: F(5, 8) * 40 == 25),
    spr(PSDA, S, 3, r"Water flows into a tank at $12$ litres per minute. How many hours does it take to fill a $3{,}600$-litre tank?", ["5"],
        r"$3{,}600 \div 12 = 300$ minutes, which is $5$ hours.", check=lambda: 3600 / 12 / 60 == 5),
    mq(PSDA, S, 3, r"A map scale is $1 : 50{,}000$. Two villages are $6$ cm apart on the map. How far apart are they in real life?", [r"$0.3$ km", r"$3$ km", r"$30$ km", r"$300$ km"], "B",
       r"$6 \times 50{,}000 = 300{,}000$ cm $= 3{,}000$ m $= 3$ km.", check=lambda: 6 * 50000 / 100 / 1000 == 3),
]

S = "Percentages"
D[S] = [
    mq(PSDA, S, 1, r"What is $25\%$ of $80$?", ["$20$", "$25$", "$32$", "$55$"], "A", r"$25\%$ is a quarter: $80 \div 4 = 20$.", check=lambda: F(25, 100) * 80 == 20),
    mq(PSDA, S, 1, r"$18$ is what percent of $72$?", [r"$18\%$", r"$25\%$", r"$40\%$", r"$54\%$"], "B", r"$\frac{18}{72} = 0.25 = 25\%$.", check=lambda: F(18, 72) == F(1, 4)),
    spr(PSDA, S, 2, r"A bike costs $\$240$. During a sale it is reduced by $35\%$. What is the sale price, in dollars?", ["156"], r"$240 \times 0.65 = 156$.", check=lambda: 240 * F(65, 100) == 156),
    mq(PSDA, S, 2, r"A town's population rose from $2{,}500$ to $3{,}000$. What was the percentage increase?", [r"$5\%$", r"$16.7\%$", r"$20\%$", r"$50\%$"], "C",
       r"Increase $= 500$, and $\frac{500}{2{,}500} = 20\%$.", check=lambda: F(500, 2500) == F(20, 100)),
    spr(PSDA, S, 3, r"After a $20\%$ increase, a price is $\$90$. What was the original price, in dollars?", ["75"], r"$1.2p = 90$, so $p = 75$.", check=lambda: 75 * F(12, 10) == 90),
    mq(PSDA, S, 3, r"A value is increased by $10\%$ and then the result is increased by another $10\%$. What is the overall percentage increase?", [r"$20\%$", r"$21\%$", r"$11\%$", r"$100\%$"], "B",
       r"$1.1 \times 1.1 = 1.21$, an overall increase of $21\%$.", check=lambda: math.isclose(1.1 * 1.1, 1.21)),
]

S = "One-variable data"
D[S] = [
    mq(PSDA, S, 1, r"What is the mean of $4, 6, 8, 10, 12$?", ["$6$", "$8$", "$10$", "$40$"], "B", r"The total is $40$ and there are $5$ numbers: $40 \div 5 = 8$.", check=lambda: (4 + 6 + 8 + 10 + 12) / 5 == 8),
    mq(PSDA, S, 1, r"What is the mode of $3, 5, 5, 7, 9, 5, 2$?", ["$2$", "$3$", "$5$", "$7$"], "C", r"$5$ appears three times, more than any other value.", check=lambda: [3, 5, 5, 7, 9, 5, 2].count(5) == 3),
    spr(PSDA, S, 2, r"What is the median of $12, 3, 8, 15, 6, 10$?", ["9"], r"In order: $3, 6, 8, 10, 12, 15$. The median is the mean of $8$ and $10$: $9$.", check=lambda: (8 + 10) / 2 == 9),
    mq(PSDA, S, 2, r"A data set has a mean of $20$. Each value is multiplied by $3$. What is the new mean?", ["$20$", "$23$", "$60$", "$400$"], "C",
       r"Multiplying every value by $3$ multiplies the mean by $3$: $60$.", check=lambda: sum(3 * x for x in [10, 20, 30]) / 3 == 60),
    mq(PSDA, S, 3, r"Data set P is $2, 4, 6, 8, 10$. Data set Q is $5, 6, 6, 6, 7$. Which statement is true?",
       ["P and Q have the same mean, and P has the larger standard deviation.", "P and Q have the same mean, and Q has the larger standard deviation.",
        "P has the larger mean, and the standard deviations are equal.", "Q has the larger mean, and P has the larger standard deviation."], "A",
       r"Both means are $6$. P's values are much more spread out, so P has the larger standard deviation.", check=lambda: sum([2, 4, 6, 8, 10]) == sum([5, 6, 6, 6, 7]) == 30),
    spr(PSDA, S, 3, r"The mean of $6$ numbers is $14$. When one number is removed, the mean of the remaining $5$ is $12$. What number was removed?", ["24"],
        r"Totals: $6 \times 14 = 84$ and $5 \times 12 = 60$, so the removed number is $84 - 60 = 24$.", check=lambda: 6 * 14 - 5 * 12 == 24),
]

S = "Two-variable data and models"
D[S] = [
    mq(PSDA, S, 1, r"A scatterplot shows that as temperature rises, ice-cream sales rise. What kind of association is this?", ["Positive", "Negative", "No association", "Exactly linear"], "A",
       r"Both variables increase together, which is a positive association.", check=lambda: True),
    mq(PSDA, S, 1, r"The line of best fit $y = 2x + 10$ predicts plant height $y$ (cm) after $x$ weeks. What is the predicted height after $6$ weeks?", [r"$16$ cm", r"$20$ cm", r"$22$ cm", r"$32$ cm"], "C",
       r"Substitute $x = 6$: $y = 2(6) + 10 = 22$ cm.", check=lambda: 2 * 6 + 10 == 22),
    mq(PSDA, S, 2, r"In the model $y = 1.5x + 40$, $y$ is a phone bill in dollars and $x$ is gigabytes used. What does $1.5$ represent?",
       ["The bill with no data used", "The extra cost for each additional gigabyte", "The number of gigabytes included", "The maximum bill"], "B",
       r"$1.5$ is the slope: the change in the bill for each extra gigabyte.", check=lambda: (1.5 * 3 + 40) - (1.5 * 2 + 40) == 1.5),
    spr(PSDA, S, 2, r"A model predicts sales $y = 120 - 4x$, where $x$ is the price in dollars. According to the model, at what price would sales be $0$?", ["30"],
        r"$120 - 4x = 0$, so $x = 30$.", check=lambda: 120 - 4 * 30 == 0),
    mq(PSDA, S, 3, r"A population of $5{,}000$ grows by $3\%$ each year. Which model gives the population $P$ after $t$ years?",
       [r"$P = 5{,}000 + 0.03t$", r"$P = 5{,}000(1.03)^t$", r"$P = 5{,}000(0.03)^t$", r"$P = 5{,}000 + 150t$"], "B",
       r"Growing by a fixed percentage each year is exponential: multiply by $1.03$ each year.", check=lambda: math.isclose(5000 * 1.03 ** 2, 5304.5)),
    mq(PSDA, S, 3, r"A scatterplot of hours of sleep and reaction time shows a strong negative association. Which conclusion is most appropriate?",
       ["More sleep causes faster reactions for everyone.", "In the data, people who slept more tended to have shorter reaction times.",
        "Reaction time determines how much people sleep.", "There is no relationship between sleep and reaction time."], "B",
       r"A negative association describes a tendency in the data, not cause and effect.", check=lambda: True),
]

S = "Probability"
D[S] = [
    mq(PSDA, S, 1, r"A fair coin is tossed. What is the probability of tails?", [r"$0$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$", r"$1$"], "C", r"There are $2$ equally likely outcomes, $1$ of them tails.", check=lambda: F(1, 2) == F(1, 2)),
    mq(PSDA, S, 1, r"A bag has $3$ red and $7$ blue marbles. What is the probability of picking red?", [r"$\dfrac{3}{10}$", r"$\dfrac{3}{7}$", r"$\dfrac{7}{10}$", r"$\dfrac{1}{3}$"], "A",
       r"$3$ of the $10$ marbles are red.", check=lambda: F(3, 10) == F(3, 10)),
    mq(PSDA, S, 2, r"A number from $1$ to $20$ is chosen at random. What is the probability it is a multiple of $4$?", [r"$\dfrac{1}{5}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$", r"$\dfrac{4}{5}$"], "B",
       r"$4, 8, 12, 16, 20$: $5$ of $20$, which is $\frac{1}{4}$.", check=lambda: F(len([n for n in range(1, 21) if n % 4 == 0]), 20) == F(1, 4)),
    mq(PSDA, S, 2, r"""In a class, $18$ of $30$ students play a sport, and $12$ of those $18$ also play an instrument. A student who plays a sport is chosen at random. What is the probability they also play an instrument?""",
       [r"$\dfrac{2}{5}$", r"$\dfrac{3}{5}$", r"$\dfrac{2}{3}$", r"$\dfrac{12}{30}$"], "C", r"Only sport players count: $\frac{12}{18} = \frac{2}{3}$.", check=lambda: F(12, 18) == F(2, 3)),
    mq(PSDA, S, 3, r"Two fair six-sided dice are rolled. What is the probability that the total is $7$?", [r"$\dfrac{1}{12}$", r"$\dfrac{1}{6}$", r"$\dfrac{7}{36}$", r"$\dfrac{1}{3}$"], "B",
       r"$6$ of the $36$ outcomes total $7$: $\frac{6}{36} = \frac{1}{6}$.", check=lambda: F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7), 36) == F(1, 6)),
    mq(PSDA, S, 3, r"A box has $4$ green and $6$ yellow counters. Two are drawn without replacement. What is the probability both are green?", [r"$\dfrac{2}{15}$", r"$\dfrac{4}{25}$", r"$\dfrac{1}{5}$", r"$\dfrac{2}{5}$"], "A",
       r"$\frac{4}{10} \times \frac{3}{9} = \frac{12}{90} = \frac{2}{15}$.", check=lambda: F(4, 10) * F(3, 9) == F(2, 15)),
]

S = "Sample statistics and margin of error"
D[S] = [
    mq(PSDA, S, 1, r"To estimate how many students at a school like a new lunch menu, which method gives the most reliable result?",
       ["Asking only the students in the lunch queue first", "Asking a random sample of students from the whole school", "Asking only the cooks", "Asking only students in one class"], "B",
       r"A random sample from the whole school is the most representative.", check=lambda: True),
    spr(PSDA, S, 2, r"In a random sample of $80$ of the $2{,}000$ households in a town, $20$ own a dog. About how many households in the town own a dog?", ["500"],
        r"$\frac{20}{80} = 25\%$, and $25\%$ of $2{,}000$ is $500$.", check=lambda: F(20, 80) * 2000 == 500),
    mq(PSDA, S, 2, r"A poll finds $52\%$ support with a margin of error of $4\%$. Which range is plausible for the true support?", [r"$48\%$ to $56\%$", r"$50\%$ to $54\%$", r"$52\%$ to $56\%$", r"$4\%$ to $52\%$"], "A",
       r"$52\% \pm 4\%$ gives $48\%$ to $56\%$.", check=lambda: (52 - 4, 52 + 4) == (48, 56)),
    mq(PSDA, S, 2, r"Two surveys of the same population are done the same way, one with $100$ people and one with $1{,}000$. Which is most likely true?",
       ["The larger survey has a smaller margin of error.", "The smaller survey has a smaller margin of error.", "Both have the same margin of error.", "Neither can be used to estimate anything."], "A",
       r"Larger random samples give more precise estimates, so a smaller margin of error.", check=lambda: True),
    mq(PSDA, S, 3, r"A survey of $500$ randomly chosen adults in one city estimates the mean commute is $34$ minutes, with a margin of error of $3$ minutes. Which conclusion is best supported?",
       ["Every adult in the city commutes 31 to 37 minutes.", "The mean commute for adults in the city is plausibly between 31 and 37 minutes.",
        "The mean commute for adults in the whole country is 34 minutes.", "Exactly half of adults commute more than 34 minutes."], "B",
       r"The interval estimates the city's mean, not individual commutes, and does not extend to other places.", check=lambda: True),
    mq(PSDA, S, 3, r"A website surveys visitors who choose to answer, and $85\%$ say they love the site. Why might this overestimate how much all visitors like it?",
       ["The sample is too large.", "People who choose to answer may feel more strongly than typical visitors.", "The percentage is too high to be possible.", "Websites cannot run surveys."], "B",
       r"Self-selected samples over-represent people with strong opinions, so the result may be biased.", check=lambda: True),
]

S = "Studies and experiments"
D[S] = [
    mq(PSDA, S, 1, r"Which study design allows a conclusion that a new teaching method causes better scores?",
       ["Comparing students who chose the method with those who did not", "Randomly assigning students to use the method or not, then comparing scores",
        "Asking students whether they like the method", "Measuring scores only for students using the method"], "B",
       r"Random assignment balances other differences, so a difference in scores can be put down to the method.", check=lambda: True),
    mq(PSDA, S, 2, r"Researchers notice that people who drink more coffee live in bigger cities. Which statement is most appropriate?",
       ["Coffee causes people to move to cities.", "Living in a city causes coffee drinking.", "The data show an association, not necessarily cause and effect.", "There is no relationship."], "C",
       r"Observational data show association only; other factors could explain it.", check=lambda: True),
    mq(PSDA, S, 2, r"In an experiment, $100$ volunteers are randomly split into two groups; one gets a new sunscreen and one a placebo cream. The sunscreen group has fewer burns. To whom do the results apply best?",
       ["All people in the world", "People similar to the volunteers", "Only the 50 people who got the sunscreen", "No one"], "B",
       r"Results from volunteers generalise best to people like them.", check=lambda: True),
    mq(PSDA, S, 2, r"Why do researchers use a placebo group in a drug trial?",
       ["To make the trial cheaper", "To check whether improvements are due to the drug rather than to expectations", "To give more people the drug", "To avoid needing volunteers"], "B",
       r"A placebo separates the drug's effect from the effect of simply being treated.", check=lambda: True),
    mq(PSDA, S, 3, r"A random sample of $300$ students from one school found that students who sleep more get better grades. Which conclusion is best supported?",
       ["More sleep causes better grades for all students.", "Students at that school who sleep more tend to get better grades.",
        "Better grades cause students to sleep more.", "All students in the country who sleep more get better grades."], "B",
       r"A random sample supports an association for that school's students, but it is not an experiment, so it does not show cause.", check=lambda: True),
    mq(PSDA, S, 3, r"Patients in a study were allowed to choose whether to take a new medicine. Those who chose it recovered faster. Why can't the study show the medicine caused faster recovery?",
       ["The sample was too small to be useful.", "Patients who chose the medicine may differ in other ways, such as being less ill.", "Medicines never affect recovery.", "Recovery speed cannot be measured."], "B",
       r"Without random assignment, other differences between the groups could explain the result.", check=lambda: True),
]

S = "Area and volume"
D[S] = [
    mq(GEO, S, 1, r"What is the area of a rectangle $8$ m long and $5$ m wide?", [r"$13\text{ m}^2$", r"$26\text{ m}^2$", r"$40\text{ m}^2$", r"$80\text{ m}^2$"], "C", r"Area $=$ length $\times$ width $= 8 \times 5 = 40$ square metres.", check=lambda: 8 * 5 == 40),
    mq(GEO, S, 1, r"What is the volume of a cube with edges of $3$ cm?", [r"$9\text{ cm}^3$", r"$18\text{ cm}^3$", r"$27\text{ cm}^3$", r"$54\text{ cm}^3$"], "C", r"Volume $=$ edge cubed $= 3^3 = 27$ cubic centimetres.", check=lambda: 3 ** 3 == 27),
    spr(GEO, S, 2, r"A cylinder has radius $2$ and height $5$. Its volume is $k\pi$. What is $k$?", ["20"], r"$V = \pi r^2 h = \pi(4)(5) = 20\pi$.", check=lambda: 2 ** 2 * 5 == 20),
    mq(GEO, S, 2, r"A triangle has area $24$ and base $8$. What is its height?", ["$3$", "$6$", "$12$", "$16$"], "B", r"$\frac{1}{2}(8)h = 24$, so $4h = 24$ and $h = 6$.", check=lambda: F(1, 2) * 8 * 6 == 24),
    mq(GEO, S, 3, r"Each edge of a cube is doubled. By what factor does its volume increase?", ["$2$", "$4$", "$6$", "$8$"], "D", r"Volume scales with the cube of the edge: $2^3 = 8$.", check=lambda: (2 * 3) ** 3 / 3 ** 3 == 8),
    spr(GEO, S, 3, r"A rectangular tank $50$ cm by $40$ cm is filled with water to a depth of $30$ cm. How many litres of water does it hold? ($1$ litre $= 1{,}000$ cm$^3$)", ["60"],
        r"$50 \times 40 \times 30 = 60{,}000$ cm$^3 = 60$ litres.", check=lambda: 50 * 40 * 30 / 1000 == 60),
]

S = "Lines, angles and triangles"
D[S] = [
    mq(GEO, S, 1, r"Two angles on a straight line measure $70^\circ$ and $x^\circ$. What is $x$?", ["$20$", "$90$", "$110$", "$290$"], "C", r"Angles on a straight line add to $180^\circ$: $x = 110$.", check=lambda: 180 - 70 == 110),
    mq(GEO, S, 1, r"In an equilateral triangle, what is the measure of each angle?", [r"$45^\circ$", r"$60^\circ$", r"$90^\circ$", r"$120^\circ$"], "B", r"The three equal angles share $180^\circ$: $60^\circ$ each.", check=lambda: 180 / 3 == 60),
    spr(GEO, S, 2, r"Two parallel lines are cut by a transversal. One angle measures $65^\circ$. Its corresponding angle measures $x^\circ$. What is $x$?", ["65"],
        r"Corresponding angles on parallel lines are equal: $65$.", check=lambda: True),
    mq(GEO, S, 2, r"Triangles $ABC$ and $DEF$ are similar with $AB = 4$ and $DE = 10$. If $AC = 6$, what is $DF$?", ["$12$", "$15$", "$16$", "$24$"], "B",
       r"Scale factor $= \frac{10}{4} = 2.5$, so $DF = 6 \times 2.5 = 15$.", check=lambda: 6 * F(10, 4) == 15),
    mq(GEO, S, 3, r"In triangle $XYZ$, angle $X$ is twice angle $Y$, and angle $Z$ is $30^\circ$. What is angle $X$?", [r"$50^\circ$", r"$75^\circ$", r"$100^\circ$", r"$120^\circ$"], "C",
       r"$2y + y + 30 = 180$, so $y = 50$ and angle $X = 100^\circ$.", check=lambda: 2 * 50 + 50 + 30 == 180),
    spr(GEO, S, 3, r"An exterior angle of a triangle measures $130^\circ$. One of the two opposite interior angles measures $55^\circ$. What is the other, in degrees?", ["75"],
        r"An exterior angle equals the sum of the two opposite interior angles: $130 - 55 = 75$.", check=lambda: 130 - 55 == 75),
]

S = "Right triangles and trigonometry"
D[S] = [
    spr(GEO, S, 1, r"A right triangle has legs $5$ and $12$. What is the length of the hypotenuse?", ["13"], r"$\sqrt{25 + 144} = \sqrt{169} = 13$.", check=lambda: math.isclose(math.hypot(5, 12), 13)),
    mq(GEO, S, 1, r"In a right triangle, the side opposite angle $A$ is $3$ and the hypotenuse is $5$. What is $\sin A$?", [r"$\dfrac{3}{4}$", r"$\dfrac{3}{5}$", r"$\dfrac{4}{5}$", r"$\dfrac{5}{3}$"], "B",
       r"$\sin A = \frac{\text{opposite}}{\text{hypotenuse}} = \frac{3}{5}$.", check=lambda: True),
    mq(GEO, S, 2, r"A $45^\circ$-$45^\circ$-$90^\circ$ triangle has legs of length $7$. What is the hypotenuse?", [r"$7$", r"$7\sqrt{2}$", r"$7\sqrt{3}$", r"$14$"], "B",
       r"In a $45$-$45$-$90$ triangle the hypotenuse is $\sqrt{2}$ times a leg.", check=lambda: math.isclose(math.hypot(7, 7), 7 * math.sqrt(2))),
    mq(GEO, S, 2, r"A $30^\circ$-$60^\circ$-$90^\circ$ triangle has a hypotenuse of $10$. What is the length of the side opposite the $30^\circ$ angle?", ["$5$", r"$5\sqrt{3}$", r"$10\sqrt{3}$", "$20$"], "A",
       r"The side opposite $30^\circ$ is half the hypotenuse: $5$.", check=lambda: math.isclose(10 * math.sin(math.radians(30)), 5)),
    mq(GEO, S, 3, r"If $\sin x^\circ = \cos 25^\circ$ and $0 < x < 90$, what is $x$?", ["$25$", "$55$", "$65$", "$75$"], "C", r"$\sin x^\circ = \cos(90 - x)^\circ$, so $90 - x = 25$ and $x = 65$.",
       check=lambda: math.isclose(math.sin(math.radians(65)), math.cos(math.radians(25)))),
    spr(GEO, S, 3, r"A ramp rises $1.5$ m over a horizontal distance of $2$ m. How long is the ramp, in metres?", ["2.5"], r"$\sqrt{1.5^2 + 2^2} = \sqrt{6.25} = 2.5$.", check=lambda: math.isclose(math.hypot(1.5, 2), 2.5)),
]

S = "Circles"
D[S] = [
    mq(GEO, S, 1, r"What is the circumference of a circle with radius $5$?", [r"$5\pi$", r"$10\pi$", r"$25\pi$", r"$50\pi$"], "B", r"$C = 2\pi r = 10\pi$.", check=lambda: 2 * 5 == 10),
    mq(GEO, S, 1, r"What is the area of a circle with radius $6$?", [r"$6\pi$", r"$12\pi$", r"$36\pi$", r"$72\pi$"], "C", r"$A = \pi r^2 = 36\pi$.", check=lambda: 6 ** 2 == 36),
    mq(GEO, S, 2, r"A circle has equation $(x - 3)^2 + (y + 2)^2 = 49$. What is its radius?", ["$3$", "$7$", "$24.5$", "$49$"], "B", r"The right side is $r^2 = 49$, so $r = 7$.", check=lambda: 7 ** 2 == 49),
    spr(GEO, S, 2, r"A central angle of $90^\circ$ cuts off an arc in a circle of radius $8$. The arc length is $k\pi$. What is $k$?", ["4"], r"$\frac{90}{360} \times 2\pi(8) = 4\pi$.", check=lambda: F(90, 360) * 16 == 4),
    mq(GEO, S, 3, r"What is the centre of the circle $x^2 + y^2 - 10x + 4y = 7$?", [r"$(5, -2)$", r"$(-5, 2)$", r"$(10, -4)$", r"$(-10, 4)$"], "A",
       r"Complete the square: $(x - 5)^2 + (y + 2)^2 = 36$, so the centre is $(5, -2)$.", check=lambda: 7 + 25 + 4 == 36),
    spr(GEO, S, 3, r"A sector of a circle of radius $9$ has a central angle of $40^\circ$. Its area is $k\pi$. What is $k$?", ["9"], r"$\frac{40}{360} \times \pi(81) = 9\pi$.", check=lambda: F(40, 360) * 81 == 9),
]
