r"""AP Calculus AB free diagnostic: 10 no-calculator + 5 calculator multiple-choice questions,
one or more per College Board unit. Original questions. Run from this folder: python diagnostic.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, module, save_form  # noqa: E402
from apcalc_common import *  # noqa: E402,F403

A = [
    q(LIMD, LIM, 1, r"What is $\displaystyle\lim_{x \to 3} \frac{x^2 - 9}{x - 3}$?",
      ["$0$", "$3$", "$6$", "The limit does not exist."], "C",
      r"Substituting gives $\frac{0}{0}$, so factorise: $\frac{(x - 3)(x + 3)}{x - 3} = x + 3$ for $x \ne 3$. As $x \to 3$ this tends to $6$.",
      check=lambda: near((3.0001 ** 2 - 9) / 0.0001, 6, 1e-3)),
    q(LIMD, LIM, 2, r"What is $\displaystyle\lim_{x \to \infty} \frac{3x^2 - 5x}{1 - 2x^2}$?",
      [r"$-\dfrac{3}{2}$", r"$\dfrac{3}{2}$", "$0$", "The limit does not exist."], "A",
      r"Numerator and denominator have the same degree, so the limit is the ratio of the leading coefficients: $\frac{3}{-2} = -\frac{3}{2}$.",
      check=lambda: near((3e8 - 5e4) / (1 - 2e8), -1.5)),
    q(DIFD, DER, 1, r"If $f(x) = x^3 - \dfrac{4}{x}$, what is $f'(2)$?",
      ["$11$", "$13$", "$12$", "$14$"], "B",
      r"Write $f(x) = x^3 - 4x^{-1}$, so $f'(x) = 3x^2 + 4x^{-2}$. Then $f'(2) = 12 + 1 = 13$.",
      check=lambda: 3 * 4 + 4 / 4 == 13),
    q(DIFD, CHAIN, 2, r"What is $\dfrac{d}{dx}\left[\sin(x^2)\right]$?",
      [r"$\cos(x^2)$", r"$-2x\cos(x^2)$", r"$2x\sin(x^2)$", r"$2x\cos(x^2)$"], "D",
      r"By the chain rule, the derivative of $\sin(u)$ is $\cos(u)\cdot u'$. With $u = x^2$, $u' = 2x$, giving $2x\cos(x^2)$.",
      check=lambda: near((math.sin(1.0001 ** 2) - math.sin(0.9999 ** 2)) / 0.0002, 2 * math.cos(1))),
    q(DIFD, CHAIN, 3, r"The curve $x^2 + y^2 = 25$ passes through the point $(3, 4)$. What is $\dfrac{dy}{dx}$ at this point?",
      [r"$-\dfrac{3}{4}$", r"$\dfrac{3}{4}$", r"$-\dfrac{4}{3}$", r"$\dfrac{4}{3}$"], "A",
      r"Differentiate implicitly: $2x + 2y\frac{dy}{dx} = 0$, so $\frac{dy}{dx} = -\frac{x}{y} = -\frac{3}{4}$.",
      check=lambda: 9 + 16 == 25),
    q(DIFD, CTX, 2, r"A particle moves along the $x$-axis with position $x(t) = t^3 - 6t^2 + 9t$ for $t \ge 0$. At which times is the particle at rest?",
      ["$t = 1$ only", "$t = 3$ only", "$t = 1$ and $t = 3$", "$t = 2$ only"], "C",
      r"At rest means velocity zero: $v(t) = 3t^2 - 12t + 9 = 3(t - 1)(t - 3)$, which is zero at $t = 1$ and $t = 3$.",
      check=lambda: all(3 * t * t - 12 * t + 9 == 0 for t in (1, 3))),
    q(DIFD, ANA, 2, r"At what value of $x$ does the graph of $f(x) = x^3 - 3x^2$ have a point of inflection?",
      ["$0$", "$1$", "$2$", "$3$"], "B",
      r"$f''(x) = 6x - 6$, which is zero at $x = 1$ and changes sign there (negative before, positive after), so concavity changes at $x = 1$.",
      check=lambda: 6 * 1 - 6 == 0 and 6 * 0.9 - 6 < 0 < 6 * 1.1 - 6),
    q(INTD, INT, 1, r"What is $\displaystyle\int_0^2 (3x^2 + 1)\,dx$?",
      ["$8$", "$9$", "$12$", "$10$"], "D",
      r"An antiderivative is $x^3 + x$. Evaluating from $0$ to $2$ gives $(8 + 2) - 0 = 10$.",
      check=lambda: near(simpson(lambda x: 3 * x * x + 1, 0, 2), 10)),
    q(INTD, INT, 2, r"Let $g(x) = \displaystyle\int_0^x \sqrt{1 + t^3}\,dt$. What is $g'(2)$?",
      ["$1$", "$2$", "$3$", "$9$"], "C",
      r"By the Fundamental Theorem of Calculus, $g'(x) = \sqrt{1 + x^3}$. So $g'(2) = \sqrt{9} = 3$.",
      check=lambda: math.sqrt(1 + 8) == 3),
    q(INTD, DE, 2, r"Which function is the solution of $\dfrac{dy}{dx} = xy$ with $y(0) = 2$?",
      [r"$y = 2e^{x^2/2}$", r"$y = e^{x^2/2} + 1$", r"$y = 2e^{x^2}$", r"$y = \dfrac{x^2}{2} + 2$"], "A",
      r"Separate: $\frac{1}{y}\,dy = x\,dx$, so $\ln|y| = \frac{x^2}{2} + C$ and $y = Ae^{x^2/2}$. The condition $y(0) = 2$ gives $A = 2$.",
      check=lambda: near((2 * math.exp(1.0001 ** 2 / 2) - 2 * math.exp(0.9999 ** 2 / 2)) / 0.0002, 1 * 2 * math.exp(0.5), 1e-3)),
]

B = [
    q(INTD, APP, 2, r"What is the area of the region under $y = e^{-x^2}$ and above the $x$-axis, for $0 \le x \le 1$? (Calculator allowed.)",
      ["$0.632$", "$0.747$", "$0.842$", "$1.000$"], "B",
      r"Area $= \int_0^1 e^{-x^2}\,dx$. This has no elementary antiderivative, so evaluate it on the calculator: $\approx 0.747$.",
      check=lambda: near(simpson(lambda x: math.exp(-x * x), 0, 1), 0.747)),
    q(INTD, APP, 3, r"The region under $y = \sqrt{x}$ for $0 \le x \le 4$ is rotated about the $x$-axis. What is the volume of the solid formed? (Calculator allowed.)",
      ["$8.000$", "$12.566$", "$25.133$", "$50.265$"], "C",
      r"Disc method: $V = \pi\int_0^4 (\sqrt{x})^2\,dx = \pi\int_0^4 x\,dx = \pi \cdot 8 = 8\pi \approx 25.133$.",
      check=lambda: near(8 * math.pi, 25.133)),
    q(DIFD, CTX, 2, r"Water flows into a tank at a rate of $r(t) = 10e^{-0.2t}$ litres per minute. How many litres flow in during the first $5$ minutes? (Calculator allowed.)",
      ["$18.39$", "$31.61$", "$36.79$", "$50.00$"], "B",
      r"The amount is the integral of the rate: $\int_0^5 10e^{-0.2t}\,dt = 50\left(1 - e^{-1}\right) \approx 31.61$ litres.",
      check=lambda: near(simpson(lambda t: 10 * math.exp(-0.2 * t), 0, 5), 31.606, 1e-2)),
    q(DIFD, ANA, 3, r"For $f(x) = x^3$ on $[0, 2]$, the Mean Value Theorem guarantees a value $c$ in $(0, 2)$ with $f'(c) = \dfrac{f(2) - f(0)}{2 - 0}$. What is $c$? (Calculator allowed.)",
      ["$1.000$", "$1.333$", "$1.414$", "$1.155$"], "D",
      r"The average rate of change is $\frac{8 - 0}{2} = 4$. Solve $3c^2 = 4$: $c = \frac{2}{\sqrt{3}} \approx 1.155$.",
      check=lambda: near(3 * (2 / math.sqrt(3)) ** 2, 4)),
    q(LIMD, LIM, 2, r"""Let $f(x) = \begin{cases} kx + 1, & x < 2 \ x^2 - k, & x \ge 2 \end{cases}$

For which value of $k$ is $f$ continuous at $x = 2$?""",
      ["$1$", "$0$", r"$\dfrac{3}{2}$", "$3$"], "A",
      r"The two pieces must agree at $x = 2$: $2k + 1 = 4 - k$, so $3k = 3$ and $k = 1$.",
      check=lambda: 2 * 1 + 1 == 4 - 1),
]

save_form("ap-calc-ab", "diagnostic", "AP Calculus AB diagnostic", "diagnostic", [
    module("mcq-a", "Part A: no calculator", "mcq-a", 20, A),
    module("mcq-b", "Part B: graphing calculator", "mcq-b", 15, B),
], summary="15 multiple-choice questions covering all eight AP Calculus AB units, in the format of Section I.")
