r"""TMUA Practice Test 2: Paper 1 (20) + Paper 2 (20), 75 minutes each. Original questions.
Run from this folder: python mock2.py"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from tmua_common import *  # noqa: E402,F403

R = range(-6, 7)

P1 = [
    q(ALG, MAN, 1, r"For $x > 0$, which of the following is equal to $\dfrac{x^{1/2} \times x^{3/2}}{x^{-1}}$?",
      [r"$x^{-3}$", r"$x$", r"$x^2$", r"$x^3$", r"$x^4$"], "D",
      r"Add the powers in the numerator: $x^{1/2 + 3/2} = x^2$. Dividing by $x^{-1}$ multiplies by $x$, giving $x^3$.",
      check=lambda: math.isclose((2 ** 0.5 * 2 ** 1.5) / 2 ** -1, 2 ** 3)),
    q(ALG, EQN, 1, r"What is the sum of the solutions of $|2x - 3| = 7$?",
      ["$-2$", "$3$", "$5$", "$7$", "$10$"], "B",
      r"$2x - 3 = 7$ gives $x = 5$; $2x - 3 = -7$ gives $x = -2$. The sum is $3$.",
      check=lambda: abs(2 * 5 - 3) == 7 and abs(2 * -2 - 3) == 7),
    q(ALG, POLY, 1, r"What is the constant term when $(x - 1)(x + 2)(x - 3)$ is expanded?",
      ["$-6$", "$-2$", "$0$", "$2$", "$6$"], "E",
      r"The constant term is the product of the constants: $(-1)(2)(-3) = 6$.",
      check=lambda: (0 - 1) * (0 + 2) * (0 - 3) == 6),
    q(ALG, LOG, 1, r"What is the value of $\log_3 81 - \log_3 9 + \log_3 1$?",
      ["$2$", "$3$", "$4$", "$6$", "$9$"], "A",
      r"$\log_3 81 = 4$, $\log_3 9 = 2$ and $\log_3 1 = 0$, so the value is $4 - 2 + 0 = 2$.",
      check=lambda: 3 ** 4 == 81 and 3 ** 2 == 9),
    q(ALG, SEQ, 1, r"The arithmetic sequence $5, 9, 13, \ldots$ continues. Which term is equal to $101$?",
      ["the 23rd", "the 24th", "the 25th", "the 26th", "the 27th"], "C",
      r"The $n$th term is $5 + 4(n - 1)$. Setting $5 + 4(n - 1) = 101$ gives $n - 1 = 24$, so $n = 25$.",
      check=lambda: 5 + 4 * 24 == 101),
    q(GEO, COORD, 1, r"What is the distance between the points $(-3, 4)$ and $(5, -2)$?",
      ["$10$", "$12$", "$14$", "$18$", "$100$"], "A",
      r"The differences are $8$ and $6$, so the distance is $\sqrt{8^2 + 6^2} = \sqrt{100} = 10$.",
      check=lambda: math.hypot(8, 6) == 10),
    q(GEO, TRIG, 2, r"Given that $\sin x = \dfrac{3}{5}$ and $90^\circ < x < 180^\circ$, what is the value of $\tan x$?",
      [r"$-\dfrac{4}{3}$", r"$-\dfrac{3}{4}$", r"$\dfrac{3}{5}$", r"$\dfrac{3}{4}$", r"$\dfrac{4}{3}$"], "B",
      r"$\cos^2 x = 1 - \frac{9}{25} = \frac{16}{25}$, and cosine is negative for obtuse angles, so $\cos x = -\frac{4}{5}$. Then $\tan x = \frac{3/5}{-4/5} = -\frac{3}{4}$.",
      check=lambda: F(3, 5) ** 2 + F(-4, 5) ** 2 == 1 and F(3, 5) / F(-4, 5) == F(-3, 4)),
    q(GEO, GRAPH, 2, r"The graph of $y = x^2$ is reflected in the $x$-axis and then translated $3$ units in the positive $y$-direction. Where does the new graph cross the positive $x$-axis?",
      [r"$x = 1$", r"$x = \sqrt{2}$", r"$x = \sqrt{3}$", r"$x = 3$", r"$x = 9$"], "C",
      r"Reflecting gives $y = -x^2$; translating up gives $y = 3 - x^2$. This is zero when $x^2 = 3$, so $x = \sqrt{3}$ on the positive side.",
      check=lambda: math.isclose(3 - math.sqrt(3) ** 2, 0, abs_tol=1e-12)),
    q(CAL, DIFF, 2, r"For which values of $x$ is the function $f(x) = 2x^3 - 9x^2 + 12x$ decreasing?",
      [r"$x < 1$ or $x > 2$", r"$x < 1$", r"$x > 2$", r"$0 < x < 3$", r"$1 < x < 2$"], "E",
      r"$f'(x) = 6x^2 - 18x + 12 = 6(x - 1)(x - 2)$, which is negative between its roots: $1 < x < 2$.",
      check=lambda: all((6 * (x / 10) ** 2 - 18 * x / 10 + 12 < 0) == (1 < x / 10 < 2) for x in range(-20, 40))),
    q(CAL, INT, 2, r"Evaluate $\displaystyle\int_0^1 (x + 1)^2\,dx$.",
      ["$1$", r"$\dfrac{4}{3}$", "$2$", r"$\dfrac{7}{3}$", "$3$"], "D",
      r"An antiderivative is $\frac{(x + 1)^3}{3}$, so the integral is $\frac{8}{3} - \frac{1}{3} = \frac{7}{3}$.",
      check=lambda: F(8, 3) - F(1, 3) == F(7, 3)),
    q(ALG, EQN, 2, r"Real numbers $x$ and $y$ satisfy $x + y = 5$ and $xy = 6$. What is the value of $x^2 + y^2$?",
      ["$7$", "$9$", "$11$", "$12$", "$13$"], "E",
      r"$x^2 + y^2 = (x + y)^2 - 2xy = 25 - 12 = 13$.",
      check=lambda: 2 ** 2 + 3 ** 2 == 13),
    q(ALG, MAN, 2, r"Which of the following is equal to $\dfrac{1}{\sqrt{5} - 2}$?",
      [r"$\sqrt{5} + 2$", r"$\sqrt{5} - 2$", r"$\dfrac{\sqrt{5} + 2}{9}$", r"$\dfrac{\sqrt{5} - 2}{3}$", r"$2 - \sqrt{5}$"], "A",
      r"Multiply top and bottom by $\sqrt{5} + 2$: the denominator becomes $5 - 4 = 1$, leaving $\sqrt{5} + 2$.",
      check=lambda: math.isclose(1 / (math.sqrt(5) - 2), math.sqrt(5) + 2)),
    q(ALG, POLY, 2, r"The equation $x^3 - 3x + k = 0$, where $k > 0$, has a repeated root. What is the value of $k$?",
      [r"$\dfrac{1}{2}$", "$1$", r"$\dfrac{3}{2}$", "$2$", "$4$"], "D",
      r"A repeated root is also a root of the derivative $3x^2 - 3$, so it is $x = 1$ or $x = -1$. $x = 1$ needs $1 - 3 + k = 0$, so $k = 2$; $x = -1$ needs $k = -2$, which is not positive.",
      check=lambda: 1 - 3 + 2 == 0 and 3 * 1 - 3 == 0),
    q(ALG, LOG, 2, r"Solve $\log_x 8 = \dfrac{3}{2}$, where $x > 0$ and $x \ne 1$.",
      [r"$x = 4$", r"$x = 6$", r"$x = 8$", r"$x = 12$", r"$x = 16$"], "A",
      r"$x^{3/2} = 8$, so $x = 8^{2/3} = (8^{1/3})^2 = 4$.",
      check=lambda: math.isclose(4 ** 1.5, 8)),
    q(ALG, SEQ, 3, r"A geometric series has second term $6$ and sum to infinity $27$. What is the sum of the possible values of its first term?",
      ["$9$", "$18$", "$24$", "$27$", "$36$"], "D",
      r"$ar = 6$ and $\frac{a}{1 - r} = 27$. So $a = 27(1 - r)$ and $27r(1 - r) = 6$, giving $9r^2 - 9r + 2 = 0$ and $r = \frac{1}{3}$ or $\frac{2}{3}$. Then $a = 18$ or $9$, with sum $27$.",
      check=lambda: all(F(a) * r == 6 and F(a) / (1 - r) == 27 for a, r in ((18, F(1, 3)), (9, F(2, 3))))),
    q(GEO, COORD, 3, r"The tangent to the circle $x^2 + y^2 = 25$ at the point $(3, 4)$ crosses the $x$-axis at $P$. What is the $x$-coordinate of $P$?",
      ["$4$", "$5$", r"$\dfrac{25}{4}$", "$7$", r"$\dfrac{25}{3}$"], "E",
      r"The radius to $(3, 4)$ has gradient $\frac{4}{3}$, so the tangent has gradient $-\frac{3}{4}$ and equation $3x + 4y = 25$. At $y = 0$, $x = \frac{25}{3}$.",
      check=lambda: 3 * 3 + 4 * 4 == 25 and F(25, 3) * 3 == 25),
    q(GEO, TRIG, 3, r"What is the sum of the solutions of $2\cos^2 x + 3\sin x - 3 = 0$ in the interval $0 \le x \le 2\pi$?",
      [r"$\pi$", r"$\dfrac{7\pi}{6}$", r"$\dfrac{3\pi}{2}$", r"$2\pi$", r"$\dfrac{5\pi}{2}$"], "C",
      r"Use $\cos^2 x = 1 - \sin^2 x$: $2\sin^2 x - 3\sin x + 1 = 0$, so $\sin x = 1$ or $\frac{1}{2}$. That gives $x = \frac{\pi}{2}$, $\frac{\pi}{6}$ and $\frac{5\pi}{6}$, with sum $\frac{3\pi}{2}$.",
      check=lambda: all(math.isclose(2 * math.cos(t) ** 2 + 3 * math.sin(t) - 3, 0, abs_tol=1e-12) for t in (math.pi / 2, math.pi / 6, 5 * math.pi / 6))),
    q(GEO, GRAPH, 3, r"For how many integer values of $k$ does the equation $x^2 - 4|x| + k = 0$ have exactly four distinct real solutions?",
      ["$1$", "$2$", "$3$", "$4$", "$5$"], "C",
      r"Let $t = |x|$. Four solutions need $t^2 - 4t + k = 0$ to have two distinct positive roots: discriminant $16 - 4k > 0$ and product $k > 0$. So $0 < k < 4$, giving $k = 1, 2, 3$.",
      check=lambda: [k for k in range(-10, 10) if 16 - 4 * k > 0 and k > 0] == [1, 2, 3]),
    q(CAL, DIFF, 3, r"What is the shortest distance from the point $(0, 2)$ to the curve $y = x^2$?",
      ["$1$", r"$\dfrac{\sqrt{7}}{2}$", r"$\sqrt{2}$", r"$\dfrac{3}{2}$", "$2$"], "B",
      r"The squared distance is $D = x^2 + (x^2 - 2)^2 = x^4 - 3x^2 + 4$. $D' = 4x^3 - 6x = 0$ gives $x^2 = \frac{3}{2}$, so $D = \frac{9}{4} - \frac{9}{2} + 4 = \frac{7}{4}$ and the distance is $\frac{\sqrt{7}}{2}$.",
      check=lambda: math.isclose(min((x / 1000) ** 4 - 3 * (x / 1000) ** 2 + 4 for x in range(-3000, 3000)), 7 / 4, abs_tol=1e-5)),
    q(CAL, INT, 3, r"What is the total area of the regions enclosed between the graphs of $y = x^3$ and $y = x$?",
      [r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$", r"$\dfrac{3}{4}$", "$1$", "$2$"], "B",
      r"They meet at $x = -1$, $0$ and $1$. For $0 \le x \le 1$, $\int_0^1 (x - x^3)\,dx = \frac{1}{2} - \frac{1}{4} = \frac{1}{4}$, and the region for $-1 \le x \le 0$ has the same area by symmetry. The total is $\frac{1}{2}$.",
      check=lambda: F(1, 2) - F(1, 4) == F(1, 4)),
]

P2 = [
    q(LOGIC, STMT, 1, r"""Which of the following is the contrapositive of the statement

"If a shape is a square, then it has four right angles"?""",
      ["If a shape does not have four right angles, then it is not a square.", "If a shape has four right angles, then it is a square.",
       "If a shape is not a square, then it does not have four right angles.", "A shape is a square if and only if it has four right angles.",
       "If a shape is a square, then it does not have four right angles."], "A",
      r"The contrapositive of ‘if $P$ then $Q$’ is ‘if not $Q$ then not $P$’, and it is always equivalent to the original. Swapping without negating gives the converse; negating without swapping gives the inverse."),
    q(LOGIC, NSC, 1, r"""For a whole number $n$, which of the following describes the condition "$n$ is even" for the statement "$n$ is divisible by $4$"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "A",
      r"Every multiple of $4$ is even, so being even is necessary. But $6$ is even and not a multiple of $4$, so it is not sufficient.",
      check=lambda: all(n % 2 == 0 for n in range(0, 200, 4)) and 6 % 4 != 0),
    q(PROOF, PRF, 1, r"""Which of the following pairs $(a, b)$ is a counterexample to the statement

"If $a$ and $b$ are irrational, then $ab$ is irrational"?""",
      [r"$a = \sqrt{2}$, $b = \sqrt{3}$", r"$a = \sqrt{2}$, $b = \sqrt{2}$", r"$a = \pi$, $b = 2$", r"$a = 1$, $b = \sqrt{2}$", r"$a = \sqrt{3}$, $b = \sqrt{5}$"], "B",
      r"A counterexample needs both numbers irrational and their product rational. $\sqrt{2} \times \sqrt{2} = 2$ works. In the other pairs either one number is rational or the product ($\sqrt{6}$, $\sqrt{15}$) is irrational."),
    q(LOGIC, STMT, 2, r"""Which of the following is the negation of the statement

"Some prime numbers are even"?""",
      ["Some prime numbers are odd.", "All prime numbers are even.", "Some even numbers are not prime.",
       "No prime number is even.", "All even numbers are prime."], "D",
      r"‘Some primes are even’ says at least one even prime exists. Its negation says there is none: no prime is even. (The original is true, because of $2$.)"),
    q(PROOF, ERR, 2, r"""A student solves $\sqrt{x + 2} = x$ as follows.

(1) Squaring both sides: $x + 2 = x^2$.
(2) So $x^2 - x - 2 = 0$.
(3) So $(x - 2)(x + 1) = 0$.
(4) So $x = 2$ or $x = -1$.
(5) Therefore the equation has two solutions, $x = 2$ and $x = -1$.

Which line is the first one that is wrong?""",
      ["(1)", "(2)", "(3)", "(4)", "(5)"], "E",
      r"Squaring can create extra solutions, so each one must be checked. $x = -1$ gives $\sqrt{1} = 1 \ne -1$. Lines (1) to (4) are correct, but line (5) wrongly accepts $x = -1$.",
      check=lambda: math.sqrt(2 + 2) == 2 and math.sqrt(-1 + 2) != -1),
    q(LOGIC, NSC, 2, r"For a real number $x$, which of the following is a sufficient condition for $x^2 < 1$?",
      [r"$x < 1$", r"$0 < x < 1$", r"$x^2 < 2$", r"$|x| \le 1$", r"$x > -1$"], "B",
      r"If $0 < x < 1$ then $0 < x^2 < x < 1$. The others allow values with $x^2 \ge 1$: $x = -5$, $x = 1.2$, $x = 1$ and $x = 5$ respectively.",
      check=lambda: all((x / 100) ** 2 < 1 for x in range(1, 100)) and (-5) ** 2 >= 1 and 1.2 ** 2 < 2 and 1.2 ** 2 >= 1),
    q(LOGIC, STMT, 2, r"""For a real number $x$, let $P$ be the statement "$x > 3$" and $Q$ be the statement "$x > 5$". Which of the following is true for every real $x$?""",
      [r"$P \Rightarrow Q$", r"$P \Leftrightarrow Q$", r"$(\text{not } P) \Rightarrow Q$", r"$Q \Rightarrow (\text{not } P)$", r"$Q \Rightarrow P$"], "E",
      r"Any $x > 5$ is also greater than $3$, so $Q \Rightarrow P$. But $x = 4$ makes $P$ true and $Q$ false, so $P \Rightarrow Q$ and $P \Leftrightarrow Q$ fail; $x = 0$ breaks the third, and $x = 6$ breaks the fourth.",
      check=lambda: all(x > 3 for x in range(6, 100)) and 4 > 3 and not 4 > 5),
    q(PROOF, PRF, 2, r"Which of the following is a valid proof that the sum of any two odd integers is even?",
      [r"Let the integers be $2m + 1$ and $2n + 1$, where $m$ and $n$ are integers. Their sum is $2(m + n + 1)$, which is even.",
       r"$3 + 5 = 8$, which is even.",
       r"Let the integers be $2n + 1$ and $2n + 3$. Their sum is $4n + 4$, which is even.",
       r"An odd number plus an even number is odd, so an odd number plus an odd number cannot be odd.",
       r"Let the integers be $2n + 1$ and $2n + 1$. Their sum is $4n + 2$, which is even."], "A",
      r"A proof must cover every pair of odd integers, so the two numbers need independent letters. One example proves nothing, and the third and fifth arguments only cover consecutive or equal odd numbers."),
    q(ALG, MAN, 2, r"""$x$ and $y$ are real numbers with $x < y < 0$. Which of the following must be true?

I: $x^2 > y^2$
II: $xy > 0$
III: $\dfrac{1}{x} < \dfrac{1}{y}$""",
      ["I only", "II only", "I and II only", "I and III only", "I, II and III"], "C",
      r"Both are negative and $x$ is further from zero, so $x^2 > y^2$ (I) and $xy > 0$ (II). III is false: $x = -3$, $y = -1$ gives $-\frac{1}{3} > -1$.",
      check=lambda: (-3) ** 2 > (-1) ** 2 and (-3) * (-1) > 0 and not (1 / -3 < 1 / -1)),
    q(LOGIC, NSC, 3, r"For real numbers $a$ and $b$, which of the following is a necessary and sufficient condition for $(a - b)^2 + (a + b)^2 = 0$?",
      [r"$a = b$", r"$a = -b$", r"$a = 0$ and $b = 0$", r"$a = 0$ or $b = 0$", r"$ab = 0$"], "C",
      r"The sum expands to $2a^2 + 2b^2$, which is zero only when $a = 0$ and $b = 0$. Each of the other conditions allows a non-zero value, such as $a = b = 1$.",
      check=lambda: all(((a - b) ** 2 + (a + b) ** 2 == 0) == (a == 0 and b == 0) for a in R for b in R)),
    q(PROOF, ERR, 3, r"""A student attempts to prove that $x + \dfrac{1}{x} \ge 2$ for every real number $x \ne 0$.

(1) $(x - 1)^2 \ge 0$ for every real $x$.
(2) So $x^2 - 2x + 1 \ge 0$.
(3) So $x^2 + 1 \ge 2x$.
(4) Dividing both sides by $x$: $x + \dfrac{1}{x} \ge 2$.
(5) Hence the result holds for every real $x \ne 0$.

Which line contains the first error?""",
      ["(1)", "(2)", "(3)", "(4)", "(5)"], "D",
      r"Dividing an inequality by a negative number reverses it, so line (4) is valid only for $x > 0$. The claim is false for negative $x$: $x = -1$ gives $-2$.",
      check=lambda: -1 + 1 / -1 < 2),
    q(LOGIC, STMT, 3, r"""Consider the statements about integers:

I: For every integer $a$, there is an integer $b$ such that $a + b = 0$.
II: There is an integer $b$ such that, for every integer $a$, $a + b = 0$.
III: For every integer $a$, there is an integer $b$ such that $ab = 1$.

Which of these statements are true?""",
      ["none of them", "I only", "II only", "III only", "I and III only"], "B",
      r"I is true: take $b = -a$. II is false: no single $b$ works for both $a = 0$ and $a = 1$. III is false: for $a = 2$, $ab = 1$ would need $b = \frac{1}{2}$, which is not an integer.",
      check=lambda: all(a + (-a) == 0 for a in R)),
    q(PROOF, PRF, 3, r"""A proof that there are infinitely many prime numbers begins:

"Suppose there are only finitely many primes, $p_1, p_2, \ldots, p_k$. Let $N = p_1 p_2 \cdots p_k + 1$."

Which of the following correctly continues the proof?""",
      [r"$N$ is prime, so it is a prime that is not on the list.", r"$N$ is divisible by $p_1$, which is a contradiction.",
       r"$N$ is even, so it is not prime.",
       r"Each $p_i$ leaves remainder $1$ when divided into $N$, so a prime factor of $N$ is not on the list: a contradiction.",
       r"$N$ is larger than every $p_i$, so it must be a new prime."], "D",
      r"$N$ need not be prime itself ($2 \times 3 \times 5 \times 7 \times 11 \times 13 + 1 = 30031 = 59 \times 509$). But it has some prime factor, and none of $p_1, \ldots, p_k$ divides $N$, so that factor is a prime not on the list.",
      check=lambda: 2 * 3 * 5 * 7 * 11 * 13 + 1 == 59 * 509),
    q(LOGIC, NSC, 3, r"""$f(x) = ax^2 + bx + c$, where $a \ne 0$. Which of the following describes the condition "$b^2 > 4ac$" for the statement "$f(x) = 0$ has two distinct positive real roots"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "A",
      r"Two distinct real roots require $b^2 > 4ac$, so it is necessary. But $x^2 - 1 = 0$ satisfies it and has roots $\pm 1$, not both positive, so it is not sufficient.",
      check=lambda: 0 ** 2 > 4 * 1 * -1),
    q(GEO, GRAPH, 2, r"""The graph of $y = f(x)$ passes through the point $(1, 3)$. Which of the following graphs must pass through the point $(2, 3)$?

I: $y = f(x - 1)$
II: $y = f\!\left(\dfrac{x}{2}\right)$
III: $y = f(2x)$""",
      ["I only", "II only", "III only", "I and II only", "I and III only"], "D",
      r"At $x = 2$: I gives $f(1) = 3$ and II gives $f(1) = 3$. III gives $f(4)$, which is unknown."),
    q(GEO, COORD, 3, r"The points $A(0, 0)$, $B(4, 0)$ and $C(k, 3)$ are given. For how many real values of $k$ is triangle $ABC$ right-angled?",
      ["$0$", "$1$", "$2$", "$3$", "$4$"], "C",
      r"A right angle at $A$ needs $k = 0$, and at $B$ needs $k = 4$. At $C$ it needs $\vec{CA} \cdot \vec{CB} = -k(4 - k) + 9 = 0$, so $k^2 - 4k + 9 = 0$, which has no real roots (discriminant $-20$). So there are $2$ values.",
      check=lambda: 16 - 36 < 0),
    q(ALG, SEQ, 3, r"""A sequence is defined by $u_1 = k$ and $u_{n+1} = 2u_n - 3$ for $n \ge 1$. Which of the following statements are true?

I: If $k = 3$, the sequence is constant.
II: If $k > 3$, the sequence is increasing.
III: If $k < 3$, the sequence eventually has negative terms.""",
      ["I only", "I and II only", "I and III only", "II and III only", "I, II and III"], "E",
      r"Subtract $3$: $u_{n+1} - 3 = 2(u_n - 3)$, so $u_n = 3 + 2^{n-1}(k - 3)$. This is constant when $k = 3$, increases without limit when $k > 3$, and decreases without limit (so becomes negative) when $k < 3$.",
      check=lambda: all(3 + 2 ** (n - 1) * (2.9 - 3) < 0 for n in range(10, 15))),
    q(CAL, INT, 3, r"""Which of the following statements are true?

I: $\displaystyle\int_{-1}^{1} x^3\,dx = 0$
II: $\displaystyle\int_{-1}^{1} |x|\,dx = 0$
III: $\displaystyle\int_{0}^{2\pi} \sin x\,dx = 0$""",
      ["I only", "II only", "I and II only", "II and III only", "I and III only"], "E",
      r"I: $x^3$ is odd, so the areas above and below cancel. III: over a full period the positive and negative parts of $\sin x$ cancel. II: $|x| \ge 0$, and the integral is $1$.",
      check=lambda: math.isclose(-math.cos(2 * math.pi) + math.cos(0), 0, abs_tol=1e-12)),
    q(LOGIC, STMT, 2, r"""For a real number $x$, the statement "$x > 2$ only if $x^2 > 4$" means the same as which of the following?""",
      [r"If $x^2 > 4$, then $x > 2$.", r"$x > 2$ if and only if $x^2 > 4$.", r"If $x > 2$, then $x^2 > 4$.",
       r"If $x \le 2$, then $x^2 \le 4$.", r"$x^2 > 4$ only if $x > 2$."], "C",
      r"‘$P$ only if $Q$’ means $P$ cannot happen without $Q$, that is, ‘if $P$ then $Q$’. Here: if $x > 2$ then $x^2 > 4$."),
    q(PROOF, PRF, 3, r"""Which of the following is a valid proof of the statement

"For every integer $n$, if $n^2$ is odd then $n$ is odd"?""",
      [r"Checking $n = 1, 3, 5$ gives $n^2 = 1, 9, 25$, all odd.",
       r"If $n$ is even, then $n = 2m$ for some integer $m$, so $n^2 = 4m^2$ is even. This proves the contrapositive.",
       r"Assume $n$ is odd. Then $n^2$ is odd.",
       r"$n^2$ is odd, so $n^2 = 2m + 1$ and $n = \sqrt{2m + 1}$, which is odd.",
       r"Odd numbers have odd squares, so the statement is true."], "B",
      r"Proving ‘if $n$ is even then $n^2$ is even’ proves the contrapositive, which is equivalent. The third and fifth arguments prove the converse, examples are not a proof, and a square root of an odd number need not be an odd integer.",
      check=lambda: all((n * n) % 2 == 1 for n in range(-51, 52, 2))),
]

save_form("tmua", "mock-2", "TMUA Practice Test 2", "mock", [
    module("p1", "Paper 1", "p1", 75, P1),
    module("p2", "Paper 2", "p2", 75, P2),
], summary="Paper 1 + Paper 2 · 40 questions · 2 h 30 min")
