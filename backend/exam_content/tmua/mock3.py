r"""TMUA Practice Test 3: Paper 1 (20) + Paper 2 (20), 75 minutes each. Original questions.
Run from this folder: python mock3.py"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from tmua_common import *  # noqa: E402,F403

R = range(-6, 7)

P1 = [
    q(ALG, MAN, 1, r"For non-zero $x$ and $y$, which of the following is equal to $\dfrac{(3x^2y)^2}{xy^3}$?",
      [r"$\dfrac{3x^3}{y}$", r"$\dfrac{6x^3}{y}$", r"$\dfrac{9x}{y}$", r"$9x^3y$", r"$\dfrac{9x^3}{y}$"], "E",
      r"$(3x^2y)^2 = 9x^4y^2$. Dividing by $xy^3$ gives $9x^{4-1}y^{2-3} = \frac{9x^3}{y}$.",
      check=lambda: F((3 * 4 * 3) ** 2, 2 * 27) == F(9 * 8, 3)),
    q(ALG, EQN, 1, r"Which of the following is the complete solution of $3x - 7 > 2(x + 1)$?",
      [r"$x > 9$", r"$x < 9$", r"$x > 5$", r"$x > -9$", r"$x < -5$"], "A",
      r"Expand: $3x - 7 > 2x + 2$. Subtract $2x$ and add $7$: $x > 9$.",
      check=lambda: all((3 * x - 7 > 2 * (x + 1)) == (x > 9) for x in range(-30, 30))),
    q(ALG, POLY, 1, r"What is the least value of $x^2 + 6x + 2$ as $x$ varies over the real numbers?",
      ["$-11$", "$-9$", "$-8$", "$-7$", "$2$"], "D",
      r"Complete the square: $x^2 + 6x + 2 = (x + 3)^2 - 7$, which is least when $x = -3$, giving $-7$.",
      check=lambda: min(x * x + 6 * x + 2 for x in range(-20, 20)) == -7),
    q(ALG, LOG, 1, r"Given that $\log_2 a = 3$ and $\log_2 b = 5$, what is the value of $\log_2 \dfrac{a^2}{b}$?",
      ["$-5$", "$-3$", "$-1$", "$0$", "$1$"], "E",
      r"$\log_2 \frac{a^2}{b} = 2\log_2 a - \log_2 b = 6 - 5 = 1$.",
      check=lambda: math.log2(8 ** 2 / 32) == 1),
    q(ALG, SEQ, 1, r"What is the sum of the first $50$ positive even numbers?",
      ["$2450$", "$2500$", "$2550$", "$2600$", "$5100$"], "C",
      r"$2 + 4 + \cdots + 100 = 2(1 + 2 + \cdots + 50) = 2 \times \frac{50 \times 51}{2} = 2550$.",
      check=lambda: sum(range(2, 101, 2)) == 2550),
    q(GEO, COORD, 1, r"Where do the lines $y = 3x - 2$ and $2x + y = 8$ intersect?",
      [r"$(1, 1)$", r"$(4, 0)$", r"$(3, 7)$", r"$(2, 4)$", r"$(2, 6)$"], "D",
      r"Substitute: $2x + 3x - 2 = 8$, so $x = 2$ and $y = 3(2) - 2 = 4$.",
      check=lambda: 3 * 2 - 2 == 4 and 2 * 2 + 4 == 8),
    q(GEO, TRIG, 2, r"A triangle has sides of length $5$ and $7$ with an angle of $60^\circ$ between them. What is the length of the third side?",
      [r"$\sqrt{29}$", r"$\sqrt{39}$", "$7$", r"$\sqrt{59}$", r"$\sqrt{74}$"], "B",
      r"By the cosine rule, $c^2 = 25 + 49 - 2(5)(7)\cos 60^\circ = 74 - 35 = 39$, so $c = \sqrt{39}$.",
      check=lambda: math.isclose(25 + 49 - 70 * math.cos(math.radians(60)), 39)),
    q(GEO, GRAPH, 2, r"The graph of $y = \dfrac{1}{x - 2} + 3$ has a vertical and a horizontal asymptote. At which point do the asymptotes meet?",
      [r"$(-2, 3)$", r"$(2, -3)$", r"$(2, 3)$", r"$(3, 2)$", r"$(-3, 2)$"], "C",
      r"The graph of $y = \frac{1}{x}$, with asymptotes $x = 0$ and $y = 0$, has been moved $2$ right and $3$ up. So the asymptotes are $x = 2$ and $y = 3$, meeting at $(2, 3)$."),
    q(CAL, DIFF, 2, r"What is the equation of the tangent to the curve $y = x^3 - 2x$ at the point where $x = 1$?",
      [r"$y = x - 2$", r"$y = x$", r"$y = 3x - 4$", r"$y = -x$", r"$y = x + 2$"], "A",
      r"At $x = 1$, $y = -1$ and $\frac{dy}{dx} = 3x^2 - 2 = 1$. The tangent is $y + 1 = 1(x - 1)$, that is $y = x - 2$.",
      check=lambda: 1 - 2 == -1 and 3 - 2 == 1 and 1 - 2 == -1),
    q(CAL, INT, 2, r"Evaluate $\displaystyle\int_1^2 (6x^2 - 4x + 1)\,dx$.",
      ["$5$", "$6$", "$7$", "$8$", "$9$"], "E",
      r"An antiderivative is $2x^3 - 2x^2 + x$. At $2$: $16 - 8 + 2 = 10$. At $1$: $2 - 2 + 1 = 1$. The integral is $9$.",
      check=lambda: (16 - 8 + 2) - (2 - 2 + 1) == 9),
    q(ALG, EQN, 2, r"The line $y = x + c$ is a tangent to the curve $y = x^2 - 3x$. What is the value of $c$?",
      ["$-4$", "$-2$", "$0$", "$2$", "$4$"], "A",
      r"Setting $x^2 - 3x = x + c$ gives $x^2 - 4x - c = 0$. A tangent meets the curve once, so the discriminant $16 + 4c$ is zero and $c = -4$.",
      check=lambda: 16 + 4 * -4 == 0),
    q(ALG, MAN, 2, r"Given that $x = 2 + \sqrt{3}$, what is the value of $x + \dfrac{1}{x}$?",
      ["$2$", r"$2\sqrt{3}$", "$4$", r"$4 + \sqrt{3}$", "$7$"], "C",
      r"$\frac{1}{2 + \sqrt{3}} = \frac{2 - \sqrt{3}}{4 - 3} = 2 - \sqrt{3}$, so $x + \frac{1}{x} = 4$.",
      check=lambda: math.isclose((2 + math.sqrt(3)) + 1 / (2 + math.sqrt(3)), 4)),
    q(ALG, POLY, 2, r"When $p(x) = x^3 + ax + b$ is divided by $x - 1$ the remainder is $4$, and when it is divided by $x + 1$ the remainder is $6$. What is the value of $ab$?",
      ["$-10$", "$-5$", "$3$", "$5$", "$10$"], "A",
      r"$p(1) = 1 + a + b = 4$ and $p(-1) = -1 - a + b = 6$. Adding gives $2b = 10$, so $b = 5$ and $a = -2$. Then $ab = -10$.",
      check=lambda: 1 - 2 + 5 == 4 and -1 + 2 + 5 == 6),
    q(ALG, LOG, 2, r"Which of the following is the solution of $5^x = 3^{x + 1}$?",
      [r"$x = \dfrac{\log 3}{\log 5}$", r"$x = \dfrac{\log 3}{\log \frac{5}{3}}$", r"$x = \dfrac{\log 5}{\log 3}$",
       r"$x = \dfrac{\log \frac{5}{3}}{\log 3}$", r"$x = \dfrac{3}{2}$"], "B",
      r"Take logs: $x\log 5 = (x + 1)\log 3$, so $x(\log 5 - \log 3) = \log 3$ and $x = \frac{\log 3}{\log 5 - \log 3} = \frac{\log 3}{\log \frac{5}{3}}$.",
      check=lambda: math.isclose(5 ** (math.log(3) / math.log(5 / 3)), 3 ** (math.log(3) / math.log(5 / 3) + 1))),
    q(ALG, SEQ, 3, r"The sum of the first $n$ terms of a sequence is $S_n = 3n^2 + 2n$. What is the $10$th term of the sequence?",
      ["$53$", "$55$", "$57$", "$59$", "$61$"], "D",
      r"The $10$th term is $S_{10} - S_9 = (300 + 20) - (243 + 18) = 320 - 261 = 59$.",
      check=lambda: (3 * 100 + 20) - (3 * 81 + 18) == 59),
    q(GEO, COORD, 3, r"A circle passes through the points $(0, 0)$, $(6, 0)$ and $(0, 8)$. What is the area of the circle?",
      [r"$16\pi$", r"$25\pi$", r"$36\pi$", r"$48\pi$", r"$100\pi$"], "B",
      r"The right angle at the origin means the hypotenuse, from $(6, 0)$ to $(0, 8)$, is a diameter. Its length is $10$, so the radius is $5$ and the area is $25\pi$.",
      check=lambda: math.hypot(6, 8) == 10),
    q(GEO, TRIG, 3, r"How many solutions does the equation $\cos 2x = \cos x$ have in the interval $0 \le x < 2\pi$?",
      ["$1$", "$2$", "$3$", "$4$", "$6$"], "C",
      r"Use $\cos 2x = 2\cos^2 x - 1$: $2\cos^2 x - \cos x - 1 = 0$, so $\cos x = 1$ or $\cos x = -\frac{1}{2}$. That gives $x = 0$, $\frac{2\pi}{3}$ and $\frac{4\pi}{3}$.",
      check=lambda: all(math.isclose(math.cos(2 * t), math.cos(t), abs_tol=1e-12) for t in (0, 2 * math.pi / 3, 4 * math.pi / 3))),
    q(GEO, GRAPH, 3, r"Let $f(x) = x^3 - 3x$. For how many real values of $k$ does the equation $f(x) = k$ have exactly two distinct real solutions?",
      ["$1$", "$2$", "$3$", "$4$", "infinitely many"], "B",
      r"$f'(x) = 3x^2 - 3$, so there is a local maximum $f(-1) = 2$ and a local minimum $f(1) = -2$. A horizontal line meets the graph exactly twice only when it touches a turning point: $k = 2$ or $k = -2$.",
      check=lambda: (-1) ** 3 + 3 == 2 and 1 - 3 == -2),
    q(CAL, DIFF, 3, r"A rectangle has two vertices on the $x$-axis and the other two on the curve $y = 12 - x^2$, above the axis and placed symmetrically about the $y$-axis. What is the largest possible area of the rectangle?",
      ["$16$", "$20$", "$24$", "$28$", "$32$"], "E",
      r"With vertices at $x = \pm a$, the area is $A = 2a(12 - a^2) = 24a - 2a^3$. $A' = 24 - 6a^2 = 0$ gives $a = 2$, so $A = 4 \times 8 = 32$.",
      check=lambda: max(2 * (a / 1000) * (12 - (a / 1000) ** 2) for a in range(0, 3400)) <= 32 + 1e-9),
    q(CAL, INT, 3, r"Given that $\displaystyle\int_0^k (2x - 3)\,dx = 4$ and $k > 0$, what is the value of $k$?",
      ["$1$", "$2$", "$3$", "$4$", "$5$"], "D",
      r"The integral is $k^2 - 3k$, so $k^2 - 3k - 4 = 0$ and $(k - 4)(k + 1) = 0$. With $k > 0$, $k = 4$.",
      check=lambda: 16 - 12 == 4),
]

P2 = [
    q(LOGIC, STMT, 1, r"""The statement "If $n$ is a multiple of $4$, then $n$ is even" is true. Which value of $n$ shows that its converse is false?""",
      ["$6$", "$8$", "$12$", "$16$", "$20$"], "A",
      r"The converse is ‘if $n$ is even, then $n$ is a multiple of $4$’. To show it is false we need an even number that is not a multiple of $4$: $6$.",
      check=lambda: 6 % 2 == 0 and 6 % 4 != 0 and all(n % 4 == 0 for n in (8, 12, 16, 20))),
    q(LOGIC, NSC, 1, r"""For a triangle, which of the following describes the condition "the triangle is equilateral" for the statement "the triangle is isosceles"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "B",
      r"An equilateral triangle has (at least) two equal sides, so it is isosceles: the condition is sufficient. A triangle with sides $5$, $5$, $8$ is isosceles but not equilateral, so it is not necessary."),
    q(PROOF, PRF, 1, r"""Which value of $x$ is a counterexample to the statement

"$x^2 \ge x$ for every real number $x$"?""",
      [r"$-2$", r"$0$", r"$\dfrac{1}{2}$", r"$1$", r"$2$"], "C",
      r"$x = \frac{1}{2}$ gives $x^2 = \frac{1}{4} < \frac{1}{2}$. For the other values, $x^2 \ge x$ holds.",
      check=lambda: F(1, 4) < F(1, 2) and all(x * x >= x for x in (-2, 0, 1, 2))),
    q(LOGIC, STMT, 2, r"""Which of the following is logically equivalent to

"Not all cats are black"?""",
      ["No cats are black.", "All cats are not black.", "Some cats are black.", "Some cats are not black.", "Some black things are not cats."], "D",
      r"‘Not all cats are black’ says that at least one cat is not black, which is exactly ‘some cats are not black’. ‘No cats are black’ is much stronger."),
    q(PROOF, ERR, 2, r"""A student solves $\log_2 \left(x^2\right) = 4$ as follows.

(1) $\log_2 \left(x^2\right) = 2\log_2 x$.
(2) So $2\log_2 x = 4$.
(3) So $\log_2 x = 2$.
(4) So $x = 4$ is the only solution.

Which line is the first one that is not valid for every $x$ for which the equation makes sense?""",
      ["(1)", "(2)", "(3)", "(4)", "The working is correct."], "A",
      r"The equation makes sense for any $x \ne 0$, but $\log_2 x$ needs $x > 0$. The correct identity is $\log_2 (x^2) = 2\log_2 |x|$, so line (1) loses the solution $x = -4$.",
      check=lambda: math.log2((-4) ** 2) == 4),
    q(LOGIC, NSC, 2, r"""For integers $a$ and $b$, which of the following describes the condition "$a + b$ is even" for the statement "$a$ and $b$ are both even"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "A",
      r"If $a$ and $b$ are both even, so is $a + b$: the condition is necessary. But $a = b = 1$ makes $a + b$ even with neither even, so it is not sufficient.",
      check=lambda: (1 + 1) % 2 == 0),
    q(LOGIC, STMT, 2, r"""For a real number $x$, which of the following statements are true?

I: If $x^2 = 4$, then $x = 2$.
II: $x = 2$ only if $x^2 = 4$.
III: $x^2 = 4$ if $x = -2$.""",
      ["I only", "II only", "III only", "I and II only", "II and III only"], "E",
      r"I is false ($x = -2$). II means ‘if $x = 2$ then $x^2 = 4$’, which is true. III means ‘if $x = -2$ then $x^2 = 4$’, which is also true.",
      check=lambda: (-2) ** 2 == 4 and 2 ** 2 == 4),
    q(PROOF, PRF, 2, r"Which of the following is a valid proof that $n^2 - 1$ is a multiple of $8$ for every odd integer $n$?",
      [r"$n^2 - 1 = (n - 1)(n + 1)$, and both factors are even, so the product is a multiple of $4$.",
       r"$3^2 - 1 = 8$, $5^2 - 1 = 24$ and $7^2 - 1 = 48$, all multiples of $8$.",
       r"$n^2 - 1$ is even, so it is a multiple of $8$.",
       r"Write $n = 2k + 1$. Then $n^2 - 1 = 4k^2 + 4k$, which is a multiple of $4$.",
       r"Write $n = 2k + 1$. Then $n^2 - 1 = 4k(k + 1)$, and one of $k$ and $k + 1$ is even, so $n^2 - 1$ is a multiple of $8$."], "E",
      r"$4k(k + 1)$ contains $4$ and the even number $k(k + 1)$, so it is a multiple of $8$. The first and fourth arguments only reach a multiple of $4$; examples and ‘even’ are not enough.",
      check=lambda: all((n * n - 1) % 8 == 0 for n in range(-51, 52, 2))),
    q(ALG, MAN, 2, r"""$a$ and $b$ are real numbers with $a > b$. Which of the following must be true?

I: $a^3 > b^3$
II: $a^2 > b^2$
III: $a - 1 > b - 1$""",
      ["I only", "I and III only", "III only", "I and II only", "I, II and III"], "B",
      r"Cubing keeps the order of real numbers (I), and subtracting $1$ from both sides does too (III). II fails: $a = 1$, $b = -2$ gives $1 < 4$.",
      check=lambda: all(a ** 3 > b ** 3 for a in R for b in R if a > b) and not 1 > 4),
    q(LOGIC, NSC, 3, r"For a real number $x$, which of the following is a necessary and sufficient condition for $x^3 > x$?",
      [r"$x > 1$", r"$x > 0$", r"$|x| > 1$", r"$-1 < x < 0$ or $x > 1$", r"$x < -1$ or $0 < x < 1$"], "D",
      r"$x^3 - x = x(x - 1)(x + 1)$, which is positive for $-1 < x < 0$ and for $x > 1$ (check the sign in each interval between $-1$, $0$ and $1$).",
      check=lambda: all(((x / 10) ** 3 > x / 10) == (-1 < x / 10 < 0 or x / 10 > 1) for x in range(-40, 41))),
    q(PROOF, ERR, 3, r"""A student writes:

(1) Let $f(x) = x^3$.
(2) Then $f'(x) = 3x^2$, so $f'(0) = 0$.
(3) Any point where the derivative is zero is a turning point.
(4) So the graph of $y = x^3$ has a turning point at $x = 0$.

Which line contains the first error?""",
      ["(1)", "(2)", "(3)", "(4)", "There is no error."], "C",
      r"A zero derivative gives a stationary point, which need not be a turning point. For $y = x^3$, $f'(x) = 3x^2 \ge 0$ on both sides of $0$, so the graph keeps increasing through a point of inflection."),
    q(LOGIC, STMT, 3, r"""Which of the following is the negation of the statement

"For every positive integer $n$, if $n$ is prime then $n + 2$ is prime"?""",
      [r"There is a positive integer $n$ such that $n$ is prime and $n + 2$ is not prime.",
       r"For every positive integer $n$, if $n$ is prime then $n + 2$ is not prime.",
       r"For every positive integer $n$, if $n$ is not prime then $n + 2$ is not prime.",
       r"There is a positive integer $n$ such that $n$ is prime and $n + 2$ is prime.",
       r"There is a positive integer $n$ such that $n$ is not prime and $n + 2$ is prime."], "A",
      r"The negation of ‘for every $n$, $P(n)$’ is ‘for some $n$, not $P(n)$’, and ‘if prime then $n + 2$ prime’ fails exactly when $n$ is prime and $n + 2$ is not. (The original is false: $n = 7$ gives $9$.)",
      check=lambda: is_prime(7) and not is_prime(9)),
    q(PROOF, PRF, 3, r"""A student wants to prove by contradiction that $\sqrt{2} + \sqrt{3}$ is irrational. They write:

"Suppose $\sqrt{2} + \sqrt{3} = r$, where $r$ is rational. Squaring gives $5 + 2\sqrt{6} = r^2$, so $\sqrt{6} = \dfrac{r^2 - 5}{2}$."

Which fact completes the proof?""",
      [r"$\sqrt{2}$ and $\sqrt{3}$ are both irrational.", r"$r^2$ is rational.", r"$r \ne 0$.",
       r"$\sqrt{6}$ is irrational.", r"The sum of two irrational numbers is irrational."], "D",
      r"The right-hand side is rational because $r$ is, so $\sqrt{6}$ would be rational. Knowing that $\sqrt{6}$ is irrational gives the contradiction. The last statement is false ($\sqrt{2} + (-\sqrt{2}) = 0$)."),
    q(LOGIC, NSC, 3, r"""$f(x) = x^2 + px + q$, where $p$ and $q$ are real. Which of the following describes the condition "$q < 0$" for the statement "$f(x) = 0$ has two real roots of opposite sign"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "C",
      r"The product of the roots is $q$. Roots of opposite sign need a negative product, so $q < 0$ is necessary. Conversely, if $q < 0$ the discriminant $p^2 - 4q$ is positive, so there are two real roots whose product is negative: sufficient too.",
      check=lambda: all(p * p - 4 * q > 0 for p in R for q in range(-6, 0))),
    q(GEO, TRIG, 2, r"""Which of the following must be true for every angle $\theta$ with $0^\circ < \theta < 90^\circ$?

I: $\sin\theta < \tan\theta$
II: $\cos\theta < 1$
III: $\sin\theta + \cos\theta > 1$""",
      ["I only", "I and II only", "I and III only", "II and III only", "I, II and III"], "E",
      r"II holds because $\theta \ne 0^\circ$. Then I follows: $\tan\theta = \frac{\sin\theta}{\cos\theta} > \sin\theta$ as $0 < \cos\theta < 1$. III: $\sin\theta + \cos\theta = \sqrt{2}\sin(\theta + 45^\circ)$, and $45^\circ < \theta + 45^\circ < 135^\circ$ makes this more than $1$.",
      check=lambda: all(math.sin(math.radians(t)) < math.tan(math.radians(t)) and math.sin(math.radians(t)) + math.cos(math.radians(t)) > 1 for t in range(1, 90))),
    q(ALG, POLY, 3, r"$p(x)$ is a cubic polynomial with $p(1) = p(2) = p(3) = 0$ and $p(0) = -12$. What is the value of $p(4)$?",
      ["$-12$", "$6$", "$8$", "$12$", "$24$"], "D",
      r"$p(x) = a(x - 1)(x - 2)(x - 3)$. Then $p(0) = -6a = -12$, so $a = 2$, and $p(4) = 2 \times 3 \times 2 \times 1 = 12$.",
      check=lambda: 2 * (0 - 1) * (0 - 2) * (0 - 3) == -12 and 2 * 3 * 2 * 1 == 12),
    q(CAL, DIFF, 3, r"""$f$ is a polynomial with $f'(x) > 0$ for every real $x$. Which of the following must be true?

I: The equation $f(x) = 0$ has at most one real root.
II: $f(2) > f(1)$
III: $f''(x) > 0$ for every real $x$""",
      ["I only", "I and II only", "I and III only", "II and III only", "I, II and III"], "B",
      r"$f$ is strictly increasing, so it takes each value at most once (I) and $f(2) > f(1)$ (II). III fails: $f(x) = x^3 + x$ has $f'(x) = 3x^2 + 1 > 0$ but $f''(x) = 6x$, which is negative for $x < 0$."),
    q(ALG, LOG, 3, r"Which of the following numbers is the largest?",
      [r"$2^{30}$", r"$5^{12}$", r"$7^{10}$", r"$10^{9}$", r"$3^{20}$"], "E",
      r"$3^{20} = 9^{10}$ and $2^{30} = 8^{10}$, and both are larger than $7^{10}$. $5^{12} = 25^6 < 10^9$. Finally $9^{10} = 10^{10} \times 0.9^{10}$, and $0.9^{10} > 0.1$, so $3^{20} > 10^9$.",
      check=lambda: max([2 ** 30, 5 ** 12, 7 ** 10, 10 ** 9, 3 ** 20]) == 3 ** 20),
    q(LOGIC, STMT, 2, r"For a real number $x$, which one of the following statements is false?",
      [r"If $x > 1$, then $x^2 > 1$.", r"If $x^2 > 1$, then $x > 1$.", r"If $x > 1$, then $x^3 > 1$.",
       r"If $x^3 > 1$, then $x > 1$.", r"If $x < -1$, then $x^2 > 1$."], "B",
      r"$x = -2$ gives $x^2 = 4 > 1$ but $x < 1$, so the second statement is false. Cubing keeps the order, so the third and fourth are true, and the first and last are true by squaring.",
      check=lambda: (-2) ** 2 > 1 and not -2 > 1),
    q(PROOF, PRF, 3, r"Which of the following is a valid proof that no square number ends in the digit $7$?",
      [r"$1, 4, 9, 16, 25, 36, 49, 64, 81, 100$ do not end in $7$.",
       r"$7$ is prime, so it cannot be the last digit of a square.",
       r"The last digit of $n^2$ depends only on the last digit of $n$, and the squares of $0, 1, \ldots, 9$ end in $0, 1, 4, 9, 6, 5, 6, 9, 4, 1$, none of which is $7$.",
       r"Squares of odd numbers are odd and $7$ is odd, so the argument must consider odd numbers only.",
       r"$\sqrt{7}$ is irrational, so no square ends in $7$."], "C",
      r"Every integer ends in one of $0$ to $9$, and $(10a + b)^2 = 100a^2 + 20ab + b^2$ ends in the same digit as $b^2$. Checking all ten cases covers every integer. A list of examples does not."),
]

save_form("tmua", "mock-3", "TMUA Practice Test 3", "mock", [
    module("p1", "Paper 1", "p1", 75, P1),
    module("p2", "Paper 2", "p2", 75, P2),
], summary="Paper 1 + Paper 2 · 40 questions · 2 h 30 min")
