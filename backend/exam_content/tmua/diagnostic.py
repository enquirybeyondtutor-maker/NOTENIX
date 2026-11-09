r"""TMUA free diagnostic: 6 Paper 1 + 6 Paper 2 style questions, 22 minutes each. Original questions.
Run from this folder: python diagnostic.py"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from tmua_common import *  # noqa: E402,F403

P1 = [
    q(ALG, MAN, 1, r"Which of the following is equivalent to $\dfrac{x^2 - 9}{x^2 + x - 6}$ for all $x \ne 2$ and $x \ne -3$?",
      [r"$\dfrac{x + 3}{x - 2}$", r"$\dfrac{x - 3}{x + 2}$", r"$\dfrac{x - 3}{x - 2}$", r"$\dfrac{x + 3}{x + 2}$", r"$\dfrac{x - 3}{x + 3}$"], "C",
      r"Factorise: $x^2 - 9 = (x - 3)(x + 3)$ and $x^2 + x - 6 = (x + 3)(x - 2)$. Cancelling $x + 3$ leaves $\frac{x - 3}{x - 2}$.",
      check=lambda: all(F(x * x - 9, x * x + x - 6) == F(x - 3, x - 2) for x in range(-10, 11) if x not in (2, -3))),
    q(ALG, EQN, 2, r"What is the complete set of values of $x$ for which $x^2 - 5x + 4 < 0$?",
      [r"$x < 1$ or $x > 4$", r"$1 < x < 4$", r"$-4 < x < -1$", r"$x < -4$ or $x > -1$", r"$x < 4$"], "B",
      r"$x^2 - 5x + 4 = (x - 1)(x - 4)$, a parabola opening upwards with roots $1$ and $4$. It is negative between the roots: $1 < x < 4$.",
      check=lambda: all(((x / 4) ** 2 - 5 * (x / 4) + 4 < 0) == (1 < x / 4 < 4) for x in range(-40, 41))),
    q(ALG, LOG, 2, r"Find all real solutions of $\log_2 x + \log_2 (x - 2) = 3$.",
      [r"$x = -2$", r"$x = 2$", r"$x = -2$ and $x = 4$", r"$x = 4$", r"$x = 6$"], "D",
      r"Combine the logs: $\log_2 (x(x - 2)) = 3$, so $x^2 - 2x = 8$ and $(x - 4)(x + 2) = 0$. The logarithms need $x > 2$, so $x = -2$ is rejected and only $x = 4$ remains.",
      check=lambda: 4 * (4 - 2) == 2 ** 3 and -2 <= 2),
    q(ALG, SEQ, 2, r"An arithmetic sequence has third term $11$ and eighth term $31$. What is the sum of its first $10$ terms?",
      ["$190$", "$200$", "$210$", "$230$", "$250$"], "C",
      r"$a + 2d = 11$ and $a + 7d = 31$, so $5d = 20$, $d = 4$ and $a = 3$. Then $S_{10} = \frac{10}{2}(2 \cdot 3 + 9 \cdot 4) = 5 \times 42 = 210$.",
      check=lambda: sum(3 + 4 * k for k in range(10)) == 210 and 3 + 8 == 11 and 3 + 28 == 31),
    q(CAL, DIFF, 2, r"The curve $y = x^3 - 6x^2 + 9x + 1$ has two stationary points. What is the $y$-coordinate of the local minimum?",
      ["$1$", "$3$", "$5$", "$7$", "$9$"], "A",
      r"$\frac{dy}{dx} = 3x^2 - 12x + 9 = 3(x - 1)(x - 3)$, so the stationary points are at $x = 1$ and $x = 3$. A positive cubic has its minimum at the larger one: $y(3) = 27 - 54 + 27 + 1 = 1$.",
      check=lambda: 27 - 54 + 27 + 1 == 1 and 1 - 6 + 9 + 1 == 5 and (2 ** 3 - 6 * 4 + 18 + 1) > 1),
    q(CAL, INT, 3, r"What is the area of the finite region enclosed by the curve $y = x^2$ and the line $y = 2x$?",
      [r"$\dfrac{1}{3}$", r"$\dfrac{2}{3}$", "$1$", r"$\dfrac{4}{3}$", r"$\dfrac{8}{3}$"], "D",
      r"They meet where $x^2 = 2x$, at $x = 0$ and $x = 2$. Between them the line is above the curve, so the area is $\int_0^2 (2x - x^2)\,dx = \left[x^2 - \frac{x^3}{3}\right]_0^2 = 4 - \frac{8}{3} = \frac{4}{3}$.",
      check=lambda: F(4) - F(8, 3) == F(4, 3)),
]

P2 = [
    q(LOGIC, STMT, 1, r"""Consider the statement:

"If a whole number is divisible by $6$, then it is divisible by $3$."

Which of the following is the contrapositive of this statement?""",
      ["If a whole number is not divisible by 3, then it is not divisible by 6.",
       "If a whole number is divisible by 3, then it is divisible by 6.",
       "If a whole number is not divisible by 6, then it is not divisible by 3.",
       "If a whole number is divisible by 6, then it is not divisible by 3.",
       "A whole number is divisible by 6 only if it is not divisible by 3."], "A",
      r"The contrapositive of ‘if $P$ then $Q$’ is ‘if not $Q$ then not $P$’. Here $Q$ is ‘divisible by $3$’ and $P$ is ‘divisible by $6$’. Swapping without negating gives the converse instead."),
    q(LOGIC, NSC, 2, r"""For a real number $x$, consider the conditions

$P$: $x > 2$
$Q$: $x^2 > 4$

Which of the following is true?""",
      ["P is necessary but not sufficient for Q.", "P is sufficient but not necessary for Q.",
       "P is necessary and sufficient for Q.", "P is neither necessary nor sufficient for Q."], "B",
      r"If $x > 2$ then $x^2 > 4$, so $P$ is sufficient for $Q$. But $x = -3$ gives $x^2 > 4$ without $x > 2$, so $P$ is not necessary.",
      check=lambda: all(x * x > 4 for x in range(3, 50)) and (-3) ** 2 > 4),
    q(PROOF, PRF, 2, r"""Consider the statement:

"$n^2 + n + 41$ is prime for every positive integer $n$."

Which of the following values of $n$ is a counterexample to the statement?""",
      ["$1$", "$10$", "$20$", "$39$", "$40$"], "E",
      r"$n = 40$ gives $1600 + 40 + 41 = 1681 = 41^2$, which is not prime. The other values give $43$, $151$, $461$ and $1601$, all of which are prime.",
      check=lambda: all(is_prime(n * n + n + 41) for n in (1, 10, 20, 39)) and not is_prime(40 * 40 + 40 + 41)),
    q(PROOF, ERR, 2, r"""A student writes the following argument.

(1) Let $a = b$, where $a$ and $b$ are non-zero.
(2) Then $a^2 = ab$.
(3) So $a^2 - b^2 = ab - b^2$.
(4) So $(a + b)(a - b) = b(a - b)$.
(5) So $a + b = b$.
(6) So $2b = b$, and therefore $2 = 1$.

Which line is the first one that does not follow from the line before it?""",
      ["(2)", "(3)", "(4)", "(5)", "(6)"], "D",
      r"Line (5) divides both sides of line (4) by $a - b$. Since $a = b$, this is dividing by zero, so it is not valid. Lines (2) to (4) are correct steps, and (6) would follow from (5)."),
    q(LOGIC, STMT, 3, r"""Which of the following is the negation of the statement

"Every student in the class passed at least one test"?""",
      ["No student in the class passed any test.", "Every student in the class failed at least one test.",
       "At least one student in the class passed no tests.", "At least one student in the class failed at least one test.",
       "Exactly one student in the class passed no tests."], "C",
      r"The negation of ‘every student has property $X$’ is ‘at least one student does not have property $X$’. Not passing at least one test means passing no tests. The statement about ‘exactly one’ is too strong."),
    q(LOGIC, NSC, 3, r"""Let $f(x) = x^3 + ax + b$, where $a$ and $b$ are real constants. Consider the statements:

I: If $a > 0$, then $f(x) = 0$ has exactly one real root.
II: If $f(x) = 0$ has exactly one real root, then $a > 0$.
III: If $a < 0$, then $f(x) = 0$ has three distinct real roots.

Which of these statements are true for all real values of $b$?""",
      ["none of them", "I only", "II only", "III only", "I and II only", "I and III only"], "B",
      r"If $a > 0$, then $f'(x) = 3x^2 + a > 0$, so $f$ is increasing and crosses zero exactly once: I is true. With $a = -1$ and $b = 10$, the local minimum value is positive, so there is exactly one real root even though $a < 0$. That one example shows both II and III are false.",
      check=lambda: (-4 * (-1) ** 3 - 27 * 10 ** 2) < 0),
]

save_form("tmua", "diagnostic", "TMUA diagnostic", "diagnostic", [
    module("p1", "Paper 1 style", "p1", 22, P1),
    module("p2", "Paper 2 style", "p2", 22, P2),
], summary="12 questions · 44 minutes · both papers")
