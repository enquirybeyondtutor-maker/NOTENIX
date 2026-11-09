r"""TMUA Practice Test 1: Paper 1 (20) + Paper 2 (20), 75 minutes each. Original questions.
Run from this folder: python mock1.py"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from tmua_common import *  # noqa: E402,F403

R = range(-6, 7)

P1 = [
    q(ALG, MAN, 1, r"What is the coefficient of $x$ in the expansion of $(2x - 3)^3$?",
      ["$-54$", "$-27$", "$27$", "$54$", "$108$"], "D",
      r"The $x$ term comes from choosing $2x$ once and $-3$ twice: $\binom{3}{1}(2x)(-3)^2 = 3 \times 2x \times 9 = 54x$.",
      check=lambda: math.comb(3, 1) * 2 * (-3) ** 2 == 54),
    q(ALG, EQN, 1, r"The line $y = 2x + 1$ meets the curve $x^2 + y = 9$ at two points. What is the sum of the $y$-coordinates of these points?",
      ["$-8$", "$-2$", "$2$", "$5$", "$12$"], "B",
      r"Substitute: $x^2 + 2x + 1 = 9$, so $x^2 + 2x - 8 = 0$ and $x = 2$ or $x = -4$. Then $y = 5$ or $y = -7$, with sum $-2$.",
      check=lambda: (2 * 2 + 1) + (2 * -4 + 1) == -2 and 4 + 5 == 9 and 16 - 7 == 9),
    q(ALG, POLY, 1, r"What is the remainder when $x^3 - 4x^2 + 2x + 5$ is divided by $x - 3$?",
      ["$-16$", "$-10$", "$-2$", "$0$", "$2$"], "E",
      r"By the remainder theorem, the remainder is the value at $x = 3$: $27 - 36 + 6 + 5 = 2$.",
      check=lambda: 27 - 36 + 6 + 5 == 2),
    q(ALG, LOG, 1, r"Given that $2^x = 5$, what is the value of $4^{x + 1}$?",
      ["$20$", "$25$", "$50$", "$100$", "$400$"], "D",
      r"$4^{x + 1} = 4 \times 4^x = 4 \times (2^x)^2 = 4 \times 25 = 100$.",
      check=lambda: math.isclose(4 ** (math.log2(5) + 1), 100)),
    q(ALG, SEQ, 1, r"A geometric series has first term $12$ and common ratio $-\dfrac{1}{3}$. What is its sum to infinity?",
      ["$9$", "$12$", "$16$", "$18$", "$36$"], "A",
      r"$S_\infty = \frac{a}{1 - r} = \frac{12}{1 + \frac{1}{3}} = \frac{12}{4/3} = 9$. A ratio of $+\frac{1}{3}$ would give $18$.",
      check=lambda: F(12) / (1 - F(-1, 3)) == 9),
    q(GEO, COORD, 1, r"The line $L$ passes through $(1, 2)$ and is perpendicular to the line $2x + 3y = 6$. Where does $L$ cross the $y$-axis?",
      [r"$\left(0, -\tfrac{1}{2}\right)$", r"$\left(0, \tfrac{1}{2}\right)$", r"$(0, 1)$", r"$\left(0, \tfrac{3}{2}\right)$", r"$\left(0, \tfrac{7}{2}\right)$"], "B",
      r"$2x + 3y = 6$ has gradient $-\frac{2}{3}$, so $L$ has gradient $\frac{3}{2}$. Then $2 = \frac{3}{2}(1) + c$ gives $c = \frac{1}{2}$.",
      check=lambda: F(-2, 3) * F(3, 2) == -1 and 2 - F(3, 2) == F(1, 2)),
    q(GEO, TRIG, 2, r"How many solutions does the equation $\sin 2x = \dfrac{1}{2}$ have in the interval $0^\circ \le x \le 360^\circ$?",
      ["$1$", "$2$", "$3$", "$4$", "$6$"], "D",
      r"As $x$ runs from $0^\circ$ to $360^\circ$, $2x$ runs from $0^\circ$ to $720^\circ$: two full cycles. Each cycle has two solutions of $\sin\theta = \frac{1}{2}$ ($30^\circ$ and $150^\circ$ plus multiples of $360^\circ$), so there are $4$.",
      check=lambda: sum(1 for t in (30, 150, 390, 510) if 0 <= t <= 720) == 4),
    q(GEO, GRAPH, 2, r"The point $(4, 5)$ lies on the graph of $y = f(x)$. Which point must lie on the graph of $y = 2f(x - 3) + 1$?",
      [r"$(1, 11)$", r"$(7, 6)$", r"$(7, 11)$", r"$(7, 12)$", r"$(8, 11)$"], "C",
      r"Replacing $x$ by $x - 3$ moves the graph $3$ to the right, so $x = 7$ gives $f(4) = 5$. Then $y = 2 \times 5 + 1 = 11$.",
      check=lambda: (4 + 3, 2 * 5 + 1) == (7, 11)),
    q(CAL, DIFF, 2, r"What is the gradient of the curve $y = (x^2 + 1)(x - 2)$ at the point where $x = 2$?",
      ["$-3$", "$1$", "$2$", "$4$", "$5$"], "E",
      r"Expand: $y = x^3 - 2x^2 + x - 2$, so $\frac{dy}{dx} = 3x^2 - 4x + 1$. At $x = 2$ this is $12 - 8 + 1 = 5$.",
      check=lambda: 3 * 4 - 8 + 1 == 5),
    q(CAL, INT, 2, r"Evaluate $\displaystyle\int_1^4 \left(3\sqrt{x} - \frac{1}{x^2}\right) dx$.",
      [r"$\dfrac{53}{4}$", r"$\dfrac{55}{4}$", "$14$", r"$\dfrac{59}{4}$", r"$\dfrac{61}{4}$"], "A",
      r"An antiderivative is $2x^{3/2} + \frac{1}{x}$. At $4$: $16 + \frac{1}{4}$. At $1$: $2 + 1$. The difference is $\frac{65}{4} - 3 = \frac{53}{4}$.",
      check=lambda: F(16) + F(1, 4) - 3 == F(53, 4)),
    q(ALG, EQN, 2, r"For which values of $k$ does the equation $x^2 + kx + 9 = 0$ have no real roots?",
      [r"$k < -6$ or $k > 6$", r"$-6 < k < 6$", r"$-3 < k < 3$", r"$k < 6$", r"$0 < k < 6$"], "B",
      r"No real roots means the discriminant is negative: $k^2 - 36 < 0$, so $-6 < k < 6$.",
      check=lambda: all((k * k - 36 < 0) == (-6 < k < 6) for k in range(-20, 21))),
    q(ALG, MAN, 2, r"What is the value of $\left(\sqrt{12} + \sqrt{3}\right)^2$?",
      ["$15$", "$21$", "$27$", "$36$", "$45$"], "C",
      r"$\sqrt{12} = 2\sqrt{3}$, so the bracket is $3\sqrt{3}$ and its square is $9 \times 3 = 27$.",
      check=lambda: math.isclose((math.sqrt(12) + math.sqrt(3)) ** 2, 27)),
    q(ALG, POLY, 2, r"Given that $x + 2$ is a factor of $x^3 + ax^2 - x - 2$, what is the sum of the distinct real roots of $x^3 + ax^2 - x - 2 = 0$?",
      ["$-2$", "$-1$", "$0$", "$1$", "$2$"], "A",
      r"$f(-2) = -8 + 4a + 2 - 2 = 4a - 8 = 0$, so $a = 2$. Then $x^3 + 2x^2 - x - 2 = (x + 2)(x^2 - 1)$, with roots $-2$, $-1$ and $1$, whose sum is $-2$.",
      check=lambda: all(x ** 3 + 2 * x * x - x - 2 == (x + 2) * (x * x - 1) for x in R)),
    q(ALG, LOG, 2, r"What is the sum of the real solutions of $3^{2x} - 4 \cdot 3^x + 3 = 0$?",
      ["$-3$", "$-1$", "$0$", r"$\dfrac{1}{2}$", "$1$"], "E",
      r"Let $u = 3^x$: $u^2 - 4u + 3 = 0$, so $u = 1$ or $u = 3$. Then $x = 0$ or $x = 1$, with sum $1$.",
      check=lambda: 9 ** 0 - 4 + 3 == 0 and 9 - 12 + 3 == 0),
    q(ALG, SEQ, 3, r"What is the value of $\displaystyle\sum_{k=1}^{20} (3k - 2)$?",
      ["$570$", "$580$", "$590$", "$600$", "$610$"], "C",
      r"$3\sum k - \sum 2 = 3 \times \frac{20 \times 21}{2} - 40 = 630 - 40 = 590$.",
      check=lambda: sum(3 * k - 2 for k in range(1, 21)) == 590),
    q(GEO, COORD, 3, r"The circle $x^2 + y^2 - 6x + 8y = 0$ meets the $x$-axis at two points. What is the distance between them?",
      ["$3$", "$4$", "$5$", "$6$", "$10$"], "D",
      r"On the $x$-axis $y = 0$, so $x^2 - 6x = 0$ and $x = 0$ or $x = 6$. The distance is $6$. (The value $10$ is the diameter.)",
      check=lambda: 6 * 6 - 36 == 0),
    q(GEO, TRIG, 3, r"What is the greatest value of $\dfrac{1}{3\sin x + 4\cos x + 7}$ as $x$ varies over the real numbers?",
      [r"$\dfrac{1}{12}$", r"$\dfrac{1}{7}$", r"$\dfrac{1}{5}$", r"$\dfrac{1}{3}$", r"$\dfrac{1}{2}$"], "E",
      r"$3\sin x + 4\cos x = 5\sin(x + \alpha)$ for some angle $\alpha$, so it ranges from $-5$ to $5$. The denominator is smallest, $7 - 5 = 2$, so the greatest value is $\frac{1}{2}$.",
      check=lambda: math.isclose(min(3 * math.sin(t / 100) + 4 * math.cos(t / 100) for t in range(0, 629)) + 7, 2, abs_tol=1e-3)),
    q(GEO, GRAPH, 3, r"How many points of intersection do the graphs of $y = \left|x^2 - 4\right|$ and $y = 5$ have?",
      ["$2$", "$3$", "$4$", "$6$", "$8$"], "A",
      r"$|x^2 - 4| = 5$ means $x^2 - 4 = 5$ or $x^2 - 4 = -5$. The first gives $x = \pm 3$; the second needs $x^2 = -1$, which has no real solutions. So there are $2$ points.",
      check=lambda: abs(9 - 4) == 5),
    q(CAL, DIFF, 3, r"A closed cylinder has volume $16\pi$. What is the smallest possible total surface area of the cylinder?",
      [r"$16\pi$", r"$20\pi$", r"$24\pi$", r"$32\pi$", r"$48\pi$"], "C",
      r"$h = \frac{16}{r^2}$, so $S = 2\pi r^2 + 2\pi r h = 2\pi r^2 + \frac{32\pi}{r}$. Then $\frac{dS}{dr} = 4\pi r - \frac{32\pi}{r^2} = 0$ gives $r = 2$ and $h = 4$, so $S = 8\pi + 16\pi = 24\pi$.",
      check=lambda: min(2 * r * r / 1000 ** 2 + 32 / (r / 1000) for r in range(1000, 4000)) > 23.99 and 2 * 4 + 16 == 24),
    q(CAL, INT, 3, r"The function $f$ is defined for $x \ge 0$ by $f(x) = \displaystyle\int_0^x (t^2 - 4)\,dt$. For which value of $x > 0$ does $f(x)$ take its least value?",
      ["$1$", "$2$", r"$2\sqrt{3}$", "$4$", "$6$"], "B",
      r"$f'(x) = x^2 - 4$, which is negative for $0 < x < 2$ and positive for $x > 2$. So $f$ decreases then increases, with its least value at $x = 2$. ($2\sqrt{3}$ is where $f(x) = 0$.)",
      check=lambda: min(range(1, 600), key=lambda k: (k / 100) ** 3 / 3 - 4 * k / 100) == 200),
]

P2 = [
    q(LOGIC, STMT, 1, r"""Which of the following is the converse of the statement

"If it is raining, then the ground is wet"?""",
      ["If the ground is not wet, then it is not raining.", "If it is not raining, then the ground is not wet.",
       "If the ground is wet, then it is raining.", "It is raining and the ground is not wet.",
       "If it is raining, then the ground is not wet."], "C",
      r"The converse of ‘if $P$ then $Q$’ swaps the two parts: ‘if $Q$ then $P$’. Swapping and negating both parts gives the contrapositive instead."),
    q(LOGIC, NSC, 1, r"""For a real number $x$, which of the following describes the condition "$x = 3$" for the statement "$x^2 = 9$"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "B",
      r"If $x = 3$ then $x^2 = 9$, so the condition is sufficient. But $x = -3$ also gives $x^2 = 9$, so it is not necessary.",
      check=lambda: 3 ** 2 == 9 and (-3) ** 2 == 9),
    q(PROOF, PRF, 1, r"""Which of the following numbers is a counterexample to the statement

"Every odd number greater than $1$ is prime"?""",
      ["$3$", "$5$", "$7$", "$9$", "$11$"], "D",
      r"A counterexample must be odd, greater than $1$ and not prime. $9 = 3 \times 3$ is the only such number in the list.",
      check=lambda: not is_prime(9) and all(is_prime(n) for n in (3, 5, 7, 11))),
    q(LOGIC, STMT, 1, r"""$A$ and $B$ are statements. Which of the following is logically equivalent to

"It is not the case that both $A$ and $B$ are true"?""",
      ["not A and not B", "not A or not B", "A or B", "not A or B", "A and not B"], "B",
      r"‘Not both’ fails only when $A$ and $B$ are both true, so it holds exactly when at least one of them is false: ‘not $A$ or not $B$’."),
    q(PROOF, ERR, 2, r"""A student is asked to prove that, for all real numbers $a$ and $b$, if $a^2 = b^2$ then $a = b$. The student writes:

(1) Suppose $a^2 = b^2$.
(2) Then $a^2 - b^2 = 0$.
(3) So $(a - b)(a + b) = 0$.
(4) So $a - b = 0$.
(5) Hence $a = b$.

Which line is the first one that does not follow from the line before it?""",
      ["(2)", "(3)", "(4)", "(5)", "The argument is correct."], "C",
      r"From $(a - b)(a + b) = 0$ we only know that $a - b = 0$ or $a + b = 0$. Line (4) ignores the second case, which is why the claim is false: $a = 1$, $b = -1$."),
    q(LOGIC, NSC, 2, r"For an integer $n$, which of the following is a necessary and sufficient condition for $n^2$ to be even?",
      ["$n$ is divisible by $4$", "$n$ is odd", "$n$ is prime", "$n^2 > 4$", "$n$ is even"], "E",
      r"If $n$ is even, $n^2$ is even; if $n$ is odd, $n^2$ is odd. So $n^2$ is even exactly when $n$ is even. Divisible by $4$ is sufficient but not necessary ($n = 2$).",
      check=lambda: all((n * n % 2 == 0) == (n % 2 == 0) for n in range(-30, 31))),
    q(LOGIC, STMT, 2, r"""Which of the following is the negation of the statement

"All quadrilaterals with four equal sides are squares"?""",
      ["No quadrilateral with four equal sides is a square.", "There is a quadrilateral with four equal sides that is not a square.",
       "All squares have four equal sides.", "Some squares do not have four equal sides.",
       "Every quadrilateral that is not a square has four unequal sides."], "B",
      r"To deny ‘all $X$ are $Y$’ you need just one $X$ that is not $Y$: here, one quadrilateral with four equal sides that is not a square (a rhombus without right angles, for example)."),
    q(PROOF, PRF, 2, r"Which of the following is a suitable first line for a proof by contradiction that $\sqrt{3}$ is irrational?",
      [r"Assume that $\sqrt{3}$ is rational, so $\sqrt{3} = \frac{p}{q}$ for integers $p$ and $q$ with $q \ne 0$ and no common factor.",
       r"Assume that $\sqrt{3}$ is irrational.", r"Assume that $3$ is not a perfect square.",
       r"Assume that $p^2 = 3q^2$ has a solution in which $p$ and $q$ are both even.",
       r"Assume that $\sqrt{3} = 1.732\ldots$"], "A",
      r"A proof by contradiction assumes the opposite of what is to be proved. The opposite of ‘irrational’ is ‘rational’, written in lowest terms so that a contradiction can be reached."),
    q(ALG, MAN, 2, r"""$a$ and $b$ are positive real numbers with $a > b$. Which of the following must be true?

I: $a^2 > b^2$
II: $\dfrac{1}{a} > \dfrac{1}{b}$
III: $a - b > b - a$""",
      ["I only", "II only", "I and II only", "I and III only", "I, II and III"], "D",
      r"I: multiply $a > b$ by the positive numbers $a$ and $b$ and chain the results, so $a^2 > ab > b^2$. II is false: $a = 2$, $b = 1$ gives $\frac{1}{2} < 1$. III: $a - b$ is positive and $b - a$ is negative.",
      check=lambda: 1 / 2 < 1 / 1),
    q(LOGIC, NSC, 2, r"""For real numbers $x$ and $y$, which of the following describes the condition "$xy > 0$" for the statement "$x > 0$ and $y > 0$"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "A",
      r"If $x > 0$ and $y > 0$ then $xy > 0$, so the condition is necessary. But $x = y = -1$ gives $xy > 0$ with neither positive, so it is not sufficient.",
      check=lambda: (-1) * (-1) > 0),
    q(PROOF, ERR, 3, r"""A student attempts to prove by induction that $2^n > n^2$ for every positive integer $n$.

(1) When $n = 1$: $2 > 1$, so the statement is true.
(2) Assume that $2^k > k^2$ for some positive integer $k$.
(3) Then $2^{k+1} = 2 \times 2^k$.
(4) So $2^{k+1} > 2k^2$.
(5) Since $2k^2 \ge (k + 1)^2$ for every positive integer $k$, we get $2^{k+1} > (k + 1)^2$.
(6) Hence, by induction, $2^n > n^2$ for every positive integer $n$.

Which line contains the first error?""",
      ["(1)", "(3)", "(4)", "(5)", "(6)"], "D",
      r"$2k^2 \ge (k + 1)^2$ means $k^2 - 2k - 1 \ge 0$, which is false for $k = 1$ and $k = 2$. So line (5) is wrong, and indeed the claim fails at $n = 2$, $3$ and $4$ ($2^4 = 4^2$).",
      check=lambda: 2 * 1 < 4 and 2 * 4 < 9 and 2 ** 4 == 4 ** 2),
    q(LOGIC, STMT, 3, r"""Consider the statements:

I: For every positive real number $\varepsilon$, there is a positive integer $N$ such that $\dfrac{1}{N} < \varepsilon$.
II: There is a positive integer $N$ such that, for every positive real number $\varepsilon$, $\dfrac{1}{N} < \varepsilon$.

Which of these statements are true?""",
      ["neither", "I only", "II only", "both"], "B",
      r"I is true: given $\varepsilon$, take $N$ larger than $\frac{1}{\varepsilon}$. II is false: whatever $N$ is chosen, $\varepsilon = \frac{1}{N}$ fails. Swapping the order of ‘for every’ and ‘there is’ changes the meaning."),
    q(PROOF, PRF, 3, r"Which of the following is a valid proof that $n^3 - n$ is divisible by $6$ for every integer $n$?",
      [r"Checking $n = 1, 2, 3, 4, 5$ gives $0, 6, 24, 60, 120$, all multiples of $6$.",
       r"$n^3 - n = n(n^2 - 1)$, and $n^2 - 1$ is always even.",
       r"$n^3 - n = (n - 1)n(n + 1)$, a product of three consecutive integers, so it has a factor of $2$ and a factor of $3$.",
       r"$n^3$ and $n$ are both even or both odd, so $n^3 - n$ is even.",
       r"$n^3 - n$ is divisible by $3$ because $n^3$ is divisible by $3$."], "C",
      r"Among three consecutive integers one is a multiple of $3$ and at least one is even, so the product is a multiple of $6$. Checking cases is not a proof, $n^2 - 1$ is odd when $n$ is even, evenness alone gives only a factor of $2$, and $n^3$ need not be a multiple of $3$.",
      check=lambda: all((n ** 3 - n) % 6 == 0 for n in range(-50, 51))),
    q(LOGIC, NSC, 3, r"""For a real number $x$, which of the following describes the condition "$|x - 1| < 2$" for the statement "$0 < x < 3$"?""",
      ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"], "A",
      r"$|x - 1| < 2$ means $-1 < x < 3$. Every $x$ with $0 < x < 3$ satisfies it, so it is necessary. But $x = -\frac{1}{2}$ satisfies it without $0 < x < 3$, so it is not sufficient.",
      check=lambda: all(abs(x / 10 - 1) < 2 for x in range(1, 30)) and abs(-0.5 - 1) < 2),
    q(GEO, GRAPH, 2, r"""Let $f(x) = x^2 - 2x$. Which of the following statements are true?

I: $f$ is increasing for $x > 1$.
II: $f(x) \ge -1$ for all real $x$.
III: The equation $f(x) = 0$ has two distinct real roots.""",
      ["I only", "I and II only", "I and III only", "II and III only", "I, II and III"], "E",
      r"$f(x) = (x - 1)^2 - 1$: a parabola with vertex $(1, -1)$. So it increases for $x > 1$ (I) and is never below $-1$ (II). Its roots are $0$ and $2$ (III).",
      check=lambda: all(x * x - 2 * x >= -1 for x in R) and 0 - 0 == 0 and 4 - 4 == 0),
    q(ALG, EQN, 3, r"How many real numbers $x$ satisfy both $x^4 - 5x^2 + 4 = 0$ and $x^3 = x$?",
      ["$0$", "$1$", "$2$", "$3$", "$4$"], "C",
      r"$x^4 - 5x^2 + 4 = (x^2 - 1)(x^2 - 4)$, with roots $\pm 1$ and $\pm 2$. $x^3 = x$ has roots $0$ and $\pm 1$. The common values are $1$ and $-1$.",
      check=lambda: {x for x in R if x ** 4 - 5 * x * x + 4 == 0} & {x for x in R if x ** 3 == x} == {1, -1}),
    q(GEO, TRIG, 3, r"""Which of the following statements are true for all real $\theta$ (where each side is defined)?

I: $\sin^2\theta \le |\sin\theta|$
II: $\sin\theta + \cos\theta \le \sqrt{2}$
III: $\tan\theta \ge \sin\theta$""",
      ["none of them", "I only", "II only", "I and II only", "I and III only", "I, II and III"], "D",
      r"I: $|\sin\theta| \le 1$, so $\sin^2\theta = |\sin\theta| \cdot |\sin\theta| \le |\sin\theta|$. II: $\sin\theta + \cos\theta = \sqrt{2}\sin(\theta + 45^\circ) \le \sqrt{2}$. III fails for $\theta = 120^\circ$, where $\tan\theta < 0 < \sin\theta$.",
      check=lambda: math.tan(math.radians(120)) < 0 < math.sin(math.radians(120))),
    q(CAL, INT, 3, r"""$f$ is a continuous function with $\displaystyle\int_0^2 f(x)\,dx = 3$. Which of the following must be true?

I: $\displaystyle\int_0^2 2f(x)\,dx = 6$
II: $\displaystyle\int_0^1 f(x)\,dx = \frac{3}{2}$
III: $\displaystyle\int_2^4 f(x - 2)\,dx = 3$""",
      ["I only", "II only", "III only", "I and II only", "I and III only", "I, II and III"], "E",
      r"I: constants come out of an integral. III: shifting both the function and the limits by $2$ does not change the area. II need not hold: with $f(x) = \frac{3}{2}x$, the integral over $[0, 2]$ is $3$ but over $[0, 1]$ it is $\frac{3}{4}$.",
      check=lambda: F(3, 4) * 4 == 3 and F(3, 4) * 1 != F(3, 2)),
    q(LOGIC, STMT, 2, r"""$n$ is an integer. Which of the following is logically equivalent to

"If $n^2$ is a multiple of $3$, then $n$ is a multiple of $3$"?""",
      [r"If $n$ is a multiple of $3$, then $n^2$ is a multiple of $3$.",
       r"If $n^2$ is not a multiple of $3$, then $n$ is not a multiple of $3$.",
       r"$n^2$ is a multiple of $3$ and $n$ is not a multiple of $3$.",
       r"$n$ is a multiple of $3$ only if $n^2$ is a multiple of $3$.",
       r"If $n$ is not a multiple of $3$, then $n^2$ is not a multiple of $3$."], "E",
      r"A statement is equivalent to its contrapositive: ‘if not $Q$ then not $P$’. The first and fourth sentences are the converse (also true here, but not equivalent), the second is the inverse, and the third is the negation."),
    q(PROOF, PRF, 3, r"""Consider the statement:

"For every positive integer $n$, $n^2 + 1$ is not divisible by $3$."

Which of the following is correct?""",
      [r"It is true: every square leaves remainder $0$ or $1$ on division by $3$, so $n^2 + 1$ leaves remainder $1$ or $2$.",
       r"It is false: $n = 1$ gives $2$, which is not divisible by $3$.", r"It is false: $n = 2$ gives $5$.",
       r"It is true because $n^2 + 1$ is always odd.", r"It cannot be decided without checking every positive integer $n$."], "A",
      r"$n$ leaves remainder $0$, $1$ or $2$ on division by $3$, so $n^2$ leaves $0$, $1$ or $1$. Then $n^2 + 1$ leaves $1$ or $2$, never $0$. Examples where it is not divisible do not disprove it, and $n^2 + 1$ is even when $n$ is odd.",
      check=lambda: all((n * n + 1) % 3 != 0 for n in range(1, 300))),
]

save_form("tmua", "mock-1", "TMUA Practice Test 1", "mock", [
    module("p1", "Paper 1", "p1", 75, P1),
    module("p2", "Paper 2", "p2", 75, P2),
], summary="Paper 1 + Paper 2 · 40 questions · 2 h 30 min")
