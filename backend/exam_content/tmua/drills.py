r"""TMUA skill drills: 6 original questions for each of the 14 skills, easier to harder.
Run from this folder: python drills.py"""
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _exam import q, save_drills  # noqa: E402
from tmua_common import *  # noqa: E402,F403

R = [x for x in range(-6, 7) if x not in (-1, 0, 1, 2, -2)]
NS = ["necessary but not sufficient", "sufficient but not necessary", "necessary and sufficient", "neither necessary nor sufficient"]

D = {}

D[MAN] = ("Expanding, factorising, indices, surds and algebraic fractions, done quickly without a calculator.", [
    q(ALG, MAN, 1, r"Which of the following is the expansion of $(x + 3)(2x - 5)$?",
      [r"$2x^2 + x - 15$", r"$2x^2 - x - 15$", r"$2x^2 + 11x - 15$", r"$2x^2 + x + 15$", r"$2x^2 - 2$"], "A",
      r"$2x^2 - 5x + 6x - 15 = 2x^2 + x - 15$.", check=lambda: all((x + 3) * (2 * x - 5) == 2 * x * x + x - 15 for x in R)),
    q(ALG, MAN, 1, r"What is the value of $8^{2/3}$?", ["$2$", "$4$", r"$\dfrac{16}{3}$", "$8$", "$16$"], "B",
      r"$8^{2/3} = \left(8^{1/3}\right)^2 = 2^2 = 4$.", check=lambda: math.isclose(8 ** (2 / 3), 4)),
    q(ALG, MAN, 2, r"What is the value of $\sqrt{50} - \sqrt{18}$?", [r"$\sqrt{2}$", "$2$", r"$2\sqrt{2}$", "$4$", r"$4\sqrt{2}$"], "C",
      r"$\sqrt{50} = 5\sqrt{2}$ and $\sqrt{18} = 3\sqrt{2}$, so the difference is $2\sqrt{2}$.",
      check=lambda: math.isclose(math.sqrt(50) - math.sqrt(18), 2 * math.sqrt(2))),
    q(ALG, MAN, 2, r"What is the coefficient of $x^2$ in the expansion of $(1 + 2x)^5$?", ["$10$", "$20$", "$32$", "$40$", "$80$"], "D",
      r"The $x^2$ term is $\binom{5}{2}(2x)^2 = 10 \times 4x^2 = 40x^2$.", check=lambda: math.comb(5, 2) * 4 == 40),
    q(ALG, MAN, 3, r"Given that $a + \dfrac{1}{a} = 3$, what is the value of $a^2 + \dfrac{1}{a^2}$?", ["$5$", "$7$", "$9$", "$11$", r"$3\sqrt{3}$"], "B",
      r"Square: $a^2 + 2 + \frac{1}{a^2} = 9$, so $a^2 + \frac{1}{a^2} = 7$.",
      check=lambda: math.isclose(((3 + math.sqrt(5)) / 2) ** 2 + ((3 + math.sqrt(5)) / 2) ** -2, 7)),
    q(ALG, MAN, 3, r"For $x \ne 2$ and $x \ne -1$, which of the following is equal to $\dfrac{x^2 - 4}{x^2 - x - 2}$?",
      [r"$\dfrac{x - 2}{x + 1}$", r"$\dfrac{x + 2}{x - 1}$", r"$\dfrac{x - 2}{x - 1}$", r"$x + 2$", r"$\dfrac{x + 2}{x + 1}$"], "E",
      r"$x^2 - 4 = (x - 2)(x + 2)$ and $x^2 - x - 2 = (x - 2)(x + 1)$. Cancel $x - 2$ to get $\frac{x + 2}{x + 1}$.",
      check=lambda: all(F(x * x - 4, x * x - x - 2) == F(x + 2, x + 1) for x in R)),
])

D[EQN] = ("Linear and quadratic equations and inequalities, simultaneous equations, and the discriminant.", [
    q(ALG, EQN, 1, r"Which of the following is the solution of $5 - 2x \ge 11$?",
      [r"$x \le -3$", r"$x \ge -3$", r"$x \le 3$", r"$x \ge 3$", r"$x \le -8$"], "A",
      r"Subtract $5$: $-2x \ge 6$. Dividing by $-2$ reverses the inequality: $x \le -3$.",
      check=lambda: all((5 - 2 * x >= 11) == (x <= -3) for x in range(-20, 20))),
    q(ALG, EQN, 1, r"What are the solutions of $x^2 = 5x$?",
      [r"$x = 5$ only", r"$x = 0$ or $x = 5$", r"$x = -5$ or $x = 0$", r"$x = \pm\sqrt{5}$", r"$x = 0$ only"], "B",
      r"$x^2 - 5x = 0$, so $x(x - 5) = 0$ and $x = 0$ or $x = 5$. Dividing by $x$ at the start would lose $x = 0$.",
      check=lambda: 0 == 0 and 25 == 25),
    q(ALG, EQN, 2, r"Real numbers $x$ and $y$ satisfy $x - y = 1$ and $x^2 + y^2 = 13$. What are the possible values of $x + y$?",
      [r"$5$ only", r"$-5$ only", r"$5$ or $-5$", r"$1$ or $13$", r"$3$ or $-2$"], "C",
      r"Substitute $y = x - 1$: $2x^2 - 2x - 12 = 0$, so $x = 3$ or $x = -2$, giving $(3, 2)$ and $(-2, -3)$. Then $x + y = 5$ or $-5$.",
      check=lambda: 9 + 4 == 13 and 4 + 9 == 13),
    q(ALG, EQN, 2, r"What is the complete solution of $x^2 - x - 6 > 0$?",
      [r"$-2 < x < 3$", r"$x < -3$ or $x > 2$", r"$x > 3$", r"$x < -2$ or $x > 3$", r"$x < -2$"], "D",
      r"$x^2 - x - 6 = (x - 3)(x + 2)$, an upward parabola that is positive outside its roots: $x < -2$ or $x > 3$.",
      check=lambda: all((x * x - x - 6 > 0) == (x < -2 or x > 3) for x in range(-20, 20))),
    q(ALG, EQN, 3, r"For which values of $k$ does $kx^2 + 4x + k = 0$ have two distinct real roots?",
      [r"$k > 2$", r"$-2 < k < 2$", r"$k < 2$", r"$k \ne 0$", r"$-2 < k < 2$ and $k \ne 0$"], "E",
      r"Two distinct roots need $16 - 4k^2 > 0$, so $-2 < k < 2$. Also $k \ne 0$, because then the equation is linear with only one root.",
      check=lambda: all(16 - 4 * k * k > 0 for k in (-1, 1)) and 16 - 0 > 0),
    q(ALG, EQN, 3, r"What is the complete solution of $|x - 3| < 2x$?",
      [r"$x > 1$", r"$x > 3$", r"$x > -3$", r"$1 < x < 3$", r"$x < 1$"], "A",
      r"For $x \ge 3$: $x - 3 < 2x$ always holds. For $x < 3$: $3 - x < 2x$ gives $x > 1$. Together, $x > 1$.",
      check=lambda: all((abs(x / 10 - 3) < 2 * x / 10) == (x / 10 > 1) for x in range(-50, 80))),
])

D[POLY] = ("The factor and remainder theorems, completing the square and the roots of polynomials.", [
    q(ALG, POLY, 1, r"Given that $x - 2$ is a factor of $x^3 - 3x^2 + kx - 2$, what is the value of $k$?", ["$1$", "$2$", "$3$", "$4$", "$6$"], "C",
      r"By the factor theorem, the value at $x = 2$ is zero: $8 - 12 + 2k - 2 = 0$, so $k = 3$.", check=lambda: 8 - 12 + 6 - 2 == 0),
    q(ALG, POLY, 1, r"What is the remainder when $x^4 + 1$ is divided by $x + 1$?", ["$-2$", "$-1$", "$0$", "$1$", "$2$"], "E",
      r"The remainder is the value at $x = -1$: $(-1)^4 + 1 = 2$.", check=lambda: (-1) ** 4 + 1 == 2),
    q(ALG, POLY, 2, r"The equation $2x^3 - 5x^2 + x + 2 = 0$ has roots $1$ and $2$. What is the sum of all three roots?",
      [r"$-\dfrac{5}{2}$", r"$\dfrac{1}{2}$", "$2$", r"$\dfrac{5}{2}$", "$5$"], "D",
      r"The product of the roots is $-\frac{2}{2} = -1$, so the third root is $-\frac{1}{2}$. The sum is $1 + 2 - \frac{1}{2} = \frac{5}{2}$, which also equals $\frac{5}{2}$ from the $x^2$ coefficient.",
      check=lambda: 2 * F(-1, 2) ** 3 - 5 * F(-1, 2) ** 2 + F(-1, 2) + 2 == 0),
    q(ALG, POLY, 2, r"What are the coordinates of the vertex of $y = 2x^2 - 8x + 3$?",
      [r"$(-2, -5)$", r"$(2, -5)$", r"$(2, 3)$", r"$(4, 3)$", r"$(2, 5)$"], "B",
      r"$2x^2 - 8x + 3 = 2(x - 2)^2 - 5$, so the vertex is $(2, -5)$.", check=lambda: all(2 * x * x - 8 * x + 3 == 2 * (x - 2) ** 2 - 5 for x in R)),
    q(ALG, POLY, 3, r"The polynomial $x^3 + px + q$ has a factor $(x - 1)^2$. What is the value of $q$?", ["$-3$", "$-2$", "$1$", "$2$", "$3$"], "D",
      r"$x = 1$ is a repeated root, so it is a root of the polynomial and of its derivative: $1 + p + q = 0$ and $3 + p = 0$. So $p = -3$ and $q = 2$.",
      check=lambda: all(x ** 3 - 3 * x + 2 == (x - 1) ** 2 * (x + 2) for x in R)),
    q(ALG, POLY, 3, r"How many distinct real roots does $x^3 - 3x^2 + 4 = 0$ have?", ["$1$", "$2$", "$3$", "It cannot be determined."], "B",
      r"$x = -1$ and $x = 2$ are roots, and $x^3 - 3x^2 + 4 = (x + 1)(x - 2)^2$. So the distinct roots are $-1$ and $2$.",
      check=lambda: all(x ** 3 - 3 * x * x + 4 == (x + 1) * (x - 2) ** 2 for x in R)),
])

D[LOG] = ("The laws of indices and logarithms, and solving exponential equations.", [
    q(ALG, LOG, 1, r"What is the value of $\log_5 125$?", ["$2$", "$3$", "$5$", "$25$", r"$\dfrac{1}{3}$"], "B",
      r"$5^3 = 125$, so $\log_5 125 = 3$.", check=lambda: 5 ** 3 == 125),
    q(ALG, LOG, 1, r"What is the value of $\log_{10} 50 + \log_{10} 2$?", ["$2$", "$3$", "$10$", "$52$", r"$\log_{10} 52$"], "A",
      r"$\log_{10} 50 + \log_{10} 2 = \log_{10} 100 = 2$.", check=lambda: math.isclose(math.log10(50) + math.log10(2), 2)),
    q(ALG, LOG, 2, r"Solve $2^{x + 3} = 32$.", ["$x = 1$", "$x = 2$", "$x = 3$", "$x = 4$", "$x = 5$"], "B",
      r"$32 = 2^5$, so $x + 3 = 5$ and $x = 2$.", check=lambda: 2 ** 5 == 32),
    q(ALG, LOG, 2, r"Given that $\log_a 2 = p$ and $\log_a 3 = q$, which of the following is equal to $\log_a 18$?",
      [r"$p + q$", r"$2p + q$", r"$p + 2q$", r"$2pq$", r"$pq^2$"], "C",
      r"$18 = 2 \times 3^2$, so $\log_a 18 = \log_a 2 + 2\log_a 3 = p + 2q$.", check=lambda: 2 * 3 ** 2 == 18),
    q(ALG, LOG, 3, r"Solve $\log_3 (x + 1) - \log_3 (x - 1) = 1$.", [r"$x = \dfrac{1}{2}$", "$x = 1$", r"$x = \dfrac{3}{2}$", "$x = 2$", "$x = 3$"], "D",
      r"$\log_3 \frac{x + 1}{x - 1} = 1$, so $x + 1 = 3(x - 1)$ and $x = 2$. This satisfies $x > 1$, so both logarithms exist.",
      check=lambda: math.isclose(math.log(3, 3) - math.log(1, 3), 1)),
    q(ALG, LOG, 3, r"Which of the following is the largest?", [r"$\log_5 100$", r"$\log_3 30$", r"$\pi$", r"$3.2$", r"$\log_2 10$"], "E",
      r"$2^{33} = 8 \times 1024^3 \approx 8.6 \times 10^9 < 10^{10}$, so $2^{3.3} < 10$ and $\log_2 10 > 3.3$. $3^{16} = 43\,046\,721 > 30^5 = 24\,300\,000$, so $3^{3.2} > 30$ and $\log_3 30 < 3.2$. Also $\pi < 3.2$, and $\log_5 100 < 3$ because $5^3 = 125$.",
      check=lambda: max([math.log(100, 5), math.log(30, 3), math.pi, 3.2, math.log2(10)]) == math.log2(10)),
])

D[SEQ] = ("Arithmetic and geometric sequences and series, sigma notation and recurrence relations.", [
    q(ALG, SEQ, 1, r"An arithmetic sequence has first term $7$ and common difference $3$. What is its $20$th term?", ["$57$", "$60$", "$64$", "$67$", "$70$"], "C",
      r"$u_{20} = 7 + 19 \times 3 = 64$.", check=lambda: 7 + 19 * 3 == 64),
    q(ALG, SEQ, 1, r"What is the $8$th term of the geometric sequence $3, 6, 12, \ldots$?", ["$48$", "$96$", "$192$", "$384$", "$768$"], "D",
      r"$u_8 = 3 \times 2^7 = 3 \times 128 = 384$.", check=lambda: 3 * 2 ** 7 == 384),
    q(ALG, SEQ, 2, r"What is the value of $4 + 7 + 10 + \cdots + 61$?", ["$610$", "$620$", "$650$", "$680$", "$1300$"], "C",
      r"There are $\frac{61 - 4}{3} + 1 = 20$ terms, so the sum is $\frac{20}{2}(4 + 61) = 650$.", check=lambda: sum(range(4, 62, 3)) == 650),
    q(ALG, SEQ, 2, r"What is the value of $\displaystyle\sum_{k=1}^{6} 2^k$?", ["$126$", "$127$", "$128$", "$254$", "$255$"], "A",
      r"$2 + 4 + 8 + 16 + 32 + 64 = 126$, or $\frac{2(2^6 - 1)}{2 - 1} = 126$.", check=lambda: sum(2 ** k for k in range(1, 7)) == 126),
    q(ALG, SEQ, 3, r"A sequence has $u_1 = 2$ and $u_{n+1} = 3u_n - 2$. What is $u_4$?", ["$26$", "$28$", "$30$", "$82$", "$84$"], "B",
      r"$u_2 = 4$, $u_3 = 10$, $u_4 = 28$.", check=lambda: 3 * (3 * (3 * 2 - 2) - 2) - 2 == 28),
    q(ALG, SEQ, 3, r"The sum to infinity of a geometric series is $4$ times its first term. What is the common ratio?",
      [r"$\dfrac{1}{4}$", r"$\dfrac{1}{3}$", r"$\dfrac{1}{2}$", r"$\dfrac{2}{3}$", r"$\dfrac{3}{4}$"], "E",
      r"$\frac{a}{1 - r} = 4a$, so $1 - r = \frac{1}{4}$ and $r = \frac{3}{4}$.", check=lambda: 1 / (1 - F(3, 4)) == 4),
])

D[COORD] = ("Straight lines, gradients, perpendicular lines and circles in the coordinate plane.", [
    q(GEO, COORD, 1, r"What is the gradient of the line through $(2, -1)$ and $(6, 7)$?", [r"$\dfrac{1}{2}$", "$1$", "$2$", "$3$", "$4$"], "C",
      r"$\frac{7 - (-1)}{6 - 2} = \frac{8}{4} = 2$.", check=lambda: (7 + 1) / (6 - 2) == 2),
    q(GEO, COORD, 1, r"What are the centre and radius of the circle $(x - 1)^2 + (y + 3)^2 = 16$?",
      [r"centre $(1, -3)$, radius $4$", r"centre $(-1, 3)$, radius $4$", r"centre $(1, -3)$, radius $16$", r"centre $(-1, 3)$, radius $16$", r"centre $(1, 3)$, radius $4$"], "A",
      r"$(x - a)^2 + (y - b)^2 = r^2$ has centre $(a, b)$ and radius $r$, so the centre is $(1, -3)$ and the radius is $\sqrt{16} = 4$."),
    q(GEO, COORD, 2, r"Which line passes through $(1, 1)$ and is parallel to $4x - 2y = 7$?",
      [r"$y = -2x + 3$", r"$y = 2x - 1$", r"$y = \frac{1}{2}x + \frac{1}{2}$", r"$y = -\frac{1}{2}x + \frac{3}{2}$", r"$y = 2x + 1$"], "B",
      r"$4x - 2y = 7$ has gradient $2$. Through $(1, 1)$: $y - 1 = 2(x - 1)$, so $y = 2x - 1$.", check=lambda: 2 * 1 - 1 == 1),
    q(GEO, COORD, 2, r"What is the perpendicular bisector of the line segment from $(0, 0)$ to $(4, 2)$?",
      [r"$y = 2x - 3$", r"$y = \frac{1}{2}x$", r"$y = -\frac{1}{2}x + 2$", r"$y = -2x + 5$", r"$y = -2x + 3$"], "D",
      r"The midpoint is $(2, 1)$ and the segment has gradient $\frac{1}{2}$, so the bisector has gradient $-2$: $y - 1 = -2(x - 2)$, or $y = -2x + 5$.",
      check=lambda: -2 * 2 + 5 == 1),
    q(GEO, COORD, 3, r"For which values of $m$ is the line $y = mx$ a tangent to the circle $x^2 + (y - 4)^2 = 4$?",
      [r"$m = \pm 1$", r"$m = \pm\sqrt{2}$", r"$m = \pm\sqrt{3}$", r"$m = \pm 2$", r"$m = \pm\sqrt{5}$"], "C",
      r"The distance from the centre $(0, 4)$ to $mx - y = 0$ must equal the radius $2$: $\frac{4}{\sqrt{m^2 + 1}} = 2$, so $m^2 + 1 = 4$ and $m = \pm\sqrt{3}$.",
      check=lambda: math.isclose(4 / math.sqrt(3 + 1), 2)),
    q(GEO, COORD, 3, r"What is the area of the triangle with vertices $(0, 0)$, $(6, 0)$ and $(2, 5)$?", ["$6$", "$10$", "$12$", "$13$", "$15$"], "E",
      r"The base along the $x$-axis is $6$ and the height is the $y$-coordinate $5$, so the area is $\frac{1}{2} \times 6 \times 5 = 15$.",
      check=lambda: abs(6 * 5 - 0 * 2) / 2 == 15),
])

D[TRIG] = ("Exact values, the sine and cosine rules, identities and solving trigonometric equations.", [
    q(GEO, TRIG, 1, r"What is the value of $\sin 30^\circ + \cos 60^\circ$?", [r"$\dfrac{1}{2}$", r"$\dfrac{\sqrt{3}}{2}$", "$1$", r"$\sqrt{3}$", "$2$"], "C",
      r"Both are $\frac{1}{2}$, so the sum is $1$.", check=lambda: math.isclose(math.sin(math.radians(30)) + math.cos(math.radians(60)), 1)),
    q(GEO, TRIG, 1, r"Solve $\cos x = -\dfrac{1}{2}$ for $0^\circ \le x \le 180^\circ$.",
      [r"$60^\circ$", r"$120^\circ$", r"$150^\circ$", r"$210^\circ$", r"$240^\circ$"], "B",
      r"$\cos 60^\circ = \frac{1}{2}$, and cosine is negative in the second quadrant, so $x = 180^\circ - 60^\circ = 120^\circ$.",
      check=lambda: math.isclose(math.cos(math.radians(120)), -0.5)),
    q(GEO, TRIG, 2, r"A triangle has sides $6$ and $8$ with an angle of $30^\circ$ between them. What is its area?",
      ["$12$", "$24$", r"$12\sqrt{3}$", r"$24\sqrt{3}$", "$48$"], "A",
      r"Area $= \frac{1}{2}ab\sin C = \frac{1}{2} \times 6 \times 8 \times \frac{1}{2} = 12$.", check=lambda: math.isclose(0.5 * 48 * math.sin(math.radians(30)), 12)),
    q(GEO, TRIG, 2, r"What is the exact value of $\tan 225^\circ$?", [r"$-\sqrt{3}$", "$-1$", r"$\dfrac{1}{\sqrt{3}}$", "$1$", r"$\sqrt{3}$"], "D",
      r"$225^\circ = 180^\circ + 45^\circ$, and tangent repeats every $180^\circ$, so $\tan 225^\circ = \tan 45^\circ = 1$.",
      check=lambda: math.isclose(math.tan(math.radians(225)), 1)),
    q(GEO, TRIG, 3, r"Given that $\sin x = 2\cos x$, what is the value of $\sin^2 x$?",
      [r"$\dfrac{1}{5}$", r"$\dfrac{1}{3}$", r"$\dfrac{2}{5}$", r"$\dfrac{3}{5}$", r"$\dfrac{4}{5}$"], "E",
      r"$\sin^2 x = 4\cos^2 x = 4(1 - \sin^2 x)$, so $5\sin^2 x = 4$ and $\sin^2 x = \frac{4}{5}$.",
      check=lambda: math.isclose(math.sin(math.atan(2)) ** 2, 0.8)),
    q(GEO, TRIG, 3, r"How many solutions does $2\sin^2 x = \sin x$ have in the interval $0 \le x < 2\pi$?", ["$2$", "$3$", "$4$", "$5$", "$6$"], "C",
      r"$\sin x(2\sin x - 1) = 0$. $\sin x = 0$ gives $x = 0$ and $\pi$; $\sin x = \frac{1}{2}$ gives $\frac{\pi}{6}$ and $\frac{5\pi}{6}$. Do not divide by $\sin x$, or two solutions are lost.",
      check=lambda: all(math.isclose(2 * math.sin(t) ** 2, math.sin(t), abs_tol=1e-12) for t in (0, math.pi, math.pi / 6, 5 * math.pi / 6))),
])

D[GRAPH] = ("Sketching curves, transformations of graphs and counting intersections without a calculator.", [
    q(GEO, GRAPH, 1, r"The graph of $y = (x - 2)^2 + 1$ is the graph of $y = x^2$ after which translation?",
      ["2 left and 1 up", "2 right and 1 up", "2 right and 1 down", "1 right and 2 up", "2 left and 1 down"], "B",
      r"Replacing $x$ by $x - 2$ moves the graph $2$ to the right, and adding $1$ moves it $1$ up."),
    q(GEO, GRAPH, 1, r"The graph of $y = f(x)$ is reflected in the $y$-axis. What is the equation of the new graph?",
      [r"$y = f(-x)$", r"$y = -f(x)$", r"$y = -f(-x)$", r"$y = f(x) + 1$", r"$y = \dfrac{1}{f(x)}$"], "A",
      r"Reflecting in the $y$-axis sends $(x, y)$ to $(-x, y)$, so the new graph is $y = f(-x)$. $y = -f(x)$ is the reflection in the $x$-axis."),
    q(GEO, GRAPH, 2, r"How many real solutions does the equation $x^2 = 2^x$ have?", ["$1$", "$2$", "$3$", "$4$", "infinitely many"], "C",
      r"$x = 2$ and $x = 4$ are solutions. For negative $x$, $x^2$ falls from very large to $0$ while $2^x$ stays between $0$ and $1$, so the graphs cross once more. Beyond $x = 4$, $2^x$ grows faster. That makes $3$.",
      check=lambda: 2 ** 2 == 4 and 2 ** 4 == 16 and (-1) ** 2 > 2 ** -1 and 0 < 2 ** 0),
    q(GEO, GRAPH, 2, r"The function $f$ has its greatest value, $5$, at $x = 1$. Where is the greatest point on the graph of $y = 3f(2x)$?",
      [r"$(2, 15)$", r"$(2, 5)$", r"$\left(\tfrac{1}{2}, 5\right)$", r"$\left(\tfrac{1}{2}, 15\right)$", r"$(1, 15)$"], "D",
      r"$f(2x)$ takes the value $f(1)$ when $2x = 1$, that is $x = \frac{1}{2}$. Multiplying by $3$ makes the greatest value $15$."),
    q(GEO, GRAPH, 3, r"Where does the graph of $y = x(x - 2)^2$ touch the $x$-axis without crossing it?",
      [r"at $x = 0$ only", r"at $x = -2$ only", r"at $x = 0$ and $x = 2$", "nowhere", r"at $x = 2$ only"], "E",
      r"A squared factor gives a repeated root, where the graph touches the axis: $x = 2$. At the single root $x = 0$ the sign of $y$ changes, so the graph crosses there."),
    q(GEO, GRAPH, 3, r"What is the least value of $|x - 1| + |x + 3|$ as $x$ varies over the real numbers?", ["$2$", "$3$", "$4$", "$5$", "$6$"], "C",
      r"$|x - 1| + |x + 3|$ is the sum of the distances from $x$ to $1$ and to $-3$. For any $x$ between $-3$ and $1$ this is $4$, the distance between them; outside it is larger.",
      check=lambda: min(abs(x / 10 - 1) + abs(x / 10 + 3) for x in range(-100, 100)) == 4),
])

D[DIFF] = ("Differentiating powers of x, gradients, tangents and normals, stationary points and optimisation.", [
    q(CAL, DIFF, 1, r"What is $\dfrac{d}{dx}\left(4x^3 - 2x + 7\right)$?",
      [r"$12x^2 - 2$", r"$12x^2 - 2x$", r"$4x^2 - 2$", r"$12x^3 - 2$", r"$12x^2 + 5$"], "A",
      r"Differentiate each term: $4x^3 \to 12x^2$, $-2x \to -2$ and the constant $7 \to 0$."),
    q(CAL, DIFF, 1, r"What is the gradient of the curve $y = \dfrac{1}{x}$ at the point where $x = 2$?",
      ["$-2$", r"$-\dfrac{1}{2}$", r"$-\dfrac{1}{4}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{2}$"], "C",
      r"$y = x^{-1}$, so $\frac{dy}{dx} = -x^{-2} = -\frac{1}{4}$ at $x = 2$.", check=lambda: -1 / 2 ** 2 == -0.25),
    q(CAL, DIFF, 2, r"For $y = \sqrt{x}\,(x + 3)$, what is the value of $\dfrac{dy}{dx}$ at $x = 1$?", [r"$\dfrac{3}{2}$", "$2$", r"$\dfrac{5}{2}$", "$3$", "$4$"], "D",
      r"$y = x^{3/2} + 3x^{1/2}$, so $\frac{dy}{dx} = \frac{3}{2}x^{1/2} + \frac{3}{2}x^{-1/2}$, which is $\frac{3}{2} + \frac{3}{2} = 3$ at $x = 1$.",
      check=lambda: 1.5 + 1.5 == 3),
    q(CAL, DIFF, 2, r"Which of the following describes the stationary point of $y = x^2 - 6x + 5$?",
      [r"$(3, -4)$, a maximum", r"$(3, -4)$, a minimum", r"$(-3, 32)$, a minimum", r"$(3, 4)$, a minimum", r"$(6, 5)$, a minimum"], "B",
      r"$\frac{dy}{dx} = 2x - 6 = 0$ at $x = 3$, where $y = 9 - 18 + 5 = -4$. $\frac{d^2y}{dx^2} = 2 > 0$, so it is a minimum.",
      check=lambda: 9 - 18 + 5 == -4),
    q(CAL, DIFF, 3, r"For which values of $k$ is $f(x) = x^3 + kx^2 + 3x$ increasing for every real $x$?",
      [r"$k \le 3$", r"$k \ge -3$", r"$-9 \le k \le 9$", r"$k = 0$ only", r"$-3 \le k \le 3$"], "E",
      r"$f'(x) = 3x^2 + 2kx + 3$ must never be negative, so its discriminant must satisfy $4k^2 - 36 \le 0$, giving $-3 \le k \le 3$.",
      check=lambda: all(3 * x * x + 6 * x + 3 >= 0 for x in range(-20, 20))),
    q(CAL, DIFF, 3, r"The normal to $y = x^2$ at the point $(1, 1)$ meets the curve again at another point. What is its $x$-coordinate?",
      ["$-3$", "$-2$", r"$-\dfrac{3}{2}$", "$-1$", r"$-\dfrac{1}{2}$"], "C",
      r"The tangent gradient is $2$, so the normal has gradient $-\frac{1}{2}$: $y = 1 - \frac{1}{2}(x - 1)$. Setting $x^2$ equal to this gives $2x^2 + x - 3 = 0$, so $(2x + 3)(x - 1) = 0$ and $x = -\frac{3}{2}$.",
      check=lambda: 2 * F(9, 4) - F(3, 2) - 3 == 0),
])

D[INT] = ("Integrating powers of x, definite integrals and areas between curves.", [
    q(CAL, INT, 1, r"Which of the following is $\displaystyle\int (6x^2 + 2)\,dx$?",
      [r"$2x^3 + 2x + c$", r"$12x + c$", r"$6x^3 + 2x + c$", r"$2x^3 + c$", r"$3x^3 + 2x + c$"], "A",
      r"Raise each power by one and divide by the new power: $6x^2 \to 2x^3$ and $2 \to 2x$. Then add the constant $c$."),
    q(CAL, INT, 1, r"What is the value of $\displaystyle\int_0^3 2x\,dx$?", ["$3$", "$6$", "$9$", "$12$", "$18$"], "C",
      r"$\left[x^2\right]_0^3 = 9 - 0 = 9$.", check=lambda: 3 ** 2 == 9),
    q(CAL, INT, 2, r"What is the value of $\displaystyle\int_1^4 x^{-1/2}\,dx$?", ["$1$", "$2$", "$3$", "$4$", "$6$"], "B",
      r"An antiderivative is $2x^{1/2}$, so the integral is $2(2) - 2(1) = 2$.", check=lambda: 2 * 2 - 2 * 1 == 2),
    q(CAL, INT, 2, r"What is the area between the curve $y = 4 - x^2$ and the $x$-axis, from $x = 0$ to $x = 2$?",
      [r"$\dfrac{8}{3}$", "$4$", r"$\dfrac{14}{3}$", r"$\dfrac{16}{3}$", "$8$"], "D",
      r"$\int_0^2 (4 - x^2)\,dx = \left[4x - \frac{x^3}{3}\right]_0^2 = 8 - \frac{8}{3} = \frac{16}{3}$.", check=lambda: 8 - F(8, 3) == F(16, 3)),
    q(CAL, INT, 3, r"What is the value of $\displaystyle\int_{-2}^{2} (x^3 + x^2)\,dx$?", ["$0$", r"$\dfrac{4}{3}$", r"$\dfrac{8}{3}$", "$4$", r"$\dfrac{16}{3}$"], "E",
      r"The $x^3$ part is odd, so it integrates to $0$ over $[-2, 2]$. The $x^2$ part gives $\left[\frac{x^3}{3}\right]_{-2}^{2} = \frac{8}{3} + \frac{8}{3} = \frac{16}{3}$.",
      check=lambda: F(8, 3) * 2 == F(16, 3)),
    q(CAL, INT, 3, r"Given that $\displaystyle\int_1^a \frac{1}{x^2}\,dx = \frac{1}{2}$ and $a > 1$, what is the value of $a$?",
      [r"$\sqrt{2}$", r"$\dfrac{3}{2}$", "$2$", "$3$", "$4$"], "C",
      r"$\left[-\frac{1}{x}\right]_1^a = 1 - \frac{1}{a} = \frac{1}{2}$, so $a = 2$.", check=lambda: 1 - F(1, 2) == F(1, 2)),
])

D[STMT] = ("Converses, contrapositives, negations and quantifiers: what a mathematical statement really says.", [
    q(LOGIC, STMT, 1, r"""What is the converse of "If a shape is a square, then it is a rectangle"?""",
      ["If a shape is not a square, then it is not a rectangle.", "If a shape is a rectangle, then it is a square.",
       "If a shape is not a rectangle, then it is not a square.", "A shape is a square and a rectangle.", "If a shape is a square, then it is not a rectangle."], "B",
      r"The converse of ‘if $P$ then $Q$’ is ‘if $Q$ then $P$’. Here the original is true but its converse is false."),
    q(LOGIC, STMT, 1, r"""For a real number $x$, what is the negation of "$x > 3$"?""",
      [r"$x \le 3$", r"$x < 3$", r"$x > -3$", r"$x \ge 3$", r"$x < -3$"], "A",
      r"The negation must be true exactly when $x > 3$ is false, which includes $x = 3$: so it is $x \le 3$."),
    q(LOGIC, STMT, 2, r"""The statement "$P$ only if $Q$" means the same as which of the following?""",
      ["If Q, then P.", "P and Q are both true.", "If P, then Q.", "If not P, then not Q.", "P if and only if Q."], "C",
      r"‘$P$ only if $Q$’ says $P$ cannot be true unless $Q$ is, which is ‘if $P$ then $Q$’."),
    q(LOGIC, STMT, 2, r"""Which of the following is logically equivalent to "If it is sunny, then I go out"?""",
      ["If I go out, then it is sunny.", "If it is not sunny, then I do not go out.", "It is sunny and I go out.",
       "If I do not go out, then it is not sunny.", "I go out only when it is not sunny."], "D",
      r"Only the contrapositive, ‘if not $Q$ then not $P$’, is equivalent. The converse and the inverse are not."),
    q(LOGIC, STMT, 3, r"""What is the negation of "There is a real number $x$ such that $x^2 < 0$"?""",
      [r"There is a real number $x$ such that $x^2 \ge 0$.", r"For every real number $x$, $x^2 < 0$.", r"There is no real number $x$ with $x^2 \ge 0$.",
       r"For every real number $x$, $x^2 > 0$.", r"For every real number $x$, $x^2 \ge 0$."], "E",
      r"The negation of ‘there is an $x$ with $P(x)$’ is ‘every $x$ has not $P(x)$’. The negation of $x^2 < 0$ is $x^2 \ge 0$, not $x^2 > 0$."),
    q(LOGIC, STMT, 3, r"""Consider the statements:

I: For every real number $x$, there is a real number $y$ with $y > x$.
II: There is a real number $y$ such that, for every real number $x$, $y > x$.

Which of these statements are true?""",
      ["neither", "I only", "II only", "both"], "B",
      r"I is true: take $y = x + 1$. II is false: it claims there is a largest real number. The order of ‘for every’ and ‘there is’ matters."),
])

D[NSC] = ("Necessary, sufficient, and necessary-and-sufficient conditions, tested with examples and counterexamples.", [
    q(LOGIC, NSC, 1, r"""For a real number $x$, which of the following describes the condition "$x = 2$" for the statement "$x^2 = 4$"?""", NS, "B",
      r"If $x = 2$ then $x^2 = 4$, so it is sufficient. $x = -2$ also gives $x^2 = 4$, so it is not necessary."),
    q(LOGIC, NSC, 1, r"""For a whole number $n$, which of the following describes the condition "$n$ is even" for the statement "$n$ is a multiple of $6$"?""", NS, "A",
      r"Every multiple of $6$ is even, so it is necessary. $n = 4$ is even but not a multiple of $6$, so it is not sufficient."),
    q(LOGIC, NSC, 2, r"""For real numbers $x$ and $y$, which of the following describes the condition "$x > 0$ and $y > 0$" for the statement "$x + y > 0$"?""", NS, "B",
      r"Two positive numbers have a positive sum, so it is sufficient. $x = 5$, $y = -1$ has a positive sum without both being positive, so it is not necessary."),
    q(LOGIC, NSC, 2, r"""For a triangle, which of the following describes the condition "two of its angles are equal" for the statement "two of its sides are equal"?""", NS, "C",
      r"A triangle has two equal sides exactly when the angles opposite them are equal, so each condition implies the other: necessary and sufficient."),
    q(LOGIC, NSC, 3, r"""For a real number $x$, which of the following describes the condition "$x^2 < x$" for the statement "$0 < x < 1$"?""", NS, "C",
      r"$x^2 < x$ means $x(x - 1) < 0$, which holds exactly when $0 < x < 1$. So the two conditions are equivalent.",
      check=lambda: all(((x / 10) ** 2 < x / 10) == (0 < x / 10 < 1) for x in range(-30, 30))),
    q(LOGIC, NSC, 3, r"""For a real number $x$, which of the following describes the condition "$x > 1$" for the statement "$x^2 > 4$"?""", NS, "D",
      r"$x = 1.5$ satisfies $x > 1$ but not $x^2 > 4$, so it is not sufficient. $x = -3$ satisfies $x^2 > 4$ but not $x > 1$, so it is not necessary.",
      check=lambda: 1.5 ** 2 < 4 and (-3) ** 2 > 4),
])

D[PRF] = ("Counterexamples, direct proof, proof by contradiction, contrapositive and exhaustion.", [
    q(PROOF, PRF, 1, r"""Which number is a counterexample to "All multiples of $3$ are odd"?""", ["$3$", "$9$", "$6$", "$15$", "$21$"], "C",
      r"A counterexample must be a multiple of $3$ that is not odd: $6$. The others are odd multiples of $3$."),
    q(PROOF, PRF, 1, r"""To show that a statement of the form "for every $n$, $P(n)$" is false, what is enough?""",
      [r"one value of $n$ for which $P(n)$ is false", r"one value of $n$ for which $P(n)$ is true", r"checking $P(n)$ for $n = 1$ to $10$",
       r"showing that $P(n)$ is true for infinitely many $n$", r"a proof that $P(n)$ is true for every $n$"], "A",
      r"A single counterexample disproves a ‘for every’ statement. Checking many true cases never proves or disproves it."),
    q(PROOF, PRF, 2, r"""Which of the following is a suitable first line for a proof by contradiction that "there is no largest even number"?""",
      ["Suppose every even number is smaller than 100.", "Suppose there is no largest even number.", "Let n be any odd number.",
       "Suppose there is a largest even number, N.", "Let the even numbers be 2, 4, 6, and so on."], "D",
      r"A proof by contradiction starts by assuming the statement is false: that a largest even number $N$ exists. Then $N + 2$ is a larger even number, a contradiction."),
    q(PROOF, PRF, 2, r"Which of the following is a valid proof that the product of any two consecutive integers is even?",
      [r"$3 \times 4 = 12$, which is even.", r"Of $n$ and $n + 1$, one is even, so $n(n + 1)$ has a factor of $2$.",
       r"$n(n + 1) = n^2 + n$, and $n^2$ is always even.", r"Consecutive integers add to an odd number.", r"$n(n + 1)$ is even because $n + 1$ is even."], "B",
      r"Consecutive integers alternate between odd and even, so one of $n$ and $n + 1$ is even and the product is even. $n^2$ is not always even, and $n + 1$ is not always even."),
    q(PROOF, PRF, 3, r"""Which is the most direct way to prove "for every integer $n$, if $n^2$ is even then $n$ is even"?""",
      [r"Check that $2^2$, $4^2$ and $6^2$ are even.", r"Show that if $n$ is even, then $n^2$ is even.", r"Assume $n^2$ is even and take the square root.",
       r"Show that $n^2$ is even for every integer $n$.", r"Prove the contrapositive: if $n$ is odd, $n = 2k + 1$, then $n^2 = 2(2k^2 + 2k) + 1$ is odd."], "E",
      r"The contrapositive ‘if $n$ is odd then $n^2$ is odd’ is equivalent and easy to prove. Showing ‘if $n$ is even then $n^2$ is even’ proves the converse, and the fourth claim is false.",
      check=lambda: all((n * n) % 2 == 1 for n in range(-41, 42, 2))),
    q(PROOF, PRF, 3, r"Which of the following is a valid proof that $n^2 + n + 1$ is odd for every integer $n$?",
      [r"$1^2 + 1 + 1 = 3$ and $2^2 + 2 + 1 = 7$ are odd.", r"$n^2 + n + 1 > 0$, so it is odd.",
       r"$n^2 + n = n(n + 1)$ is a product of consecutive integers, so it is even, and adding $1$ makes it odd.",
       r"$n^2$ is odd and $n$ is odd, so their sum plus $1$ is odd.", r"$n^2 + n + 1$ is prime, so it is odd."], "C",
      r"$n(n + 1)$ is always even, so $n^2 + n + 1$ is one more than an even number. The other arguments use examples or false claims ($n^2$ is not always odd, and $4^2 + 4 + 1 = 21$ is not prime).",
      check=lambda: all((n * n + n + 1) % 2 == 1 for n in range(-50, 50))),
])

D[ERR] = ("Spotting the first invalid step: dividing by zero, losing solutions, squaring, reversing inequalities.", [
    q(PROOF, ERR, 1, r"""A student solves $2x + 3 = 11$:

(1) $2x = 14$
(2) $x = 7$

Which line contains the first error?""", ["(1)", "(2)", "There is no error."], "A",
      r"Subtracting $3$ from $11$ gives $8$, not $14$. The correct working is $2x = 8$, so $x = 4$.", check=lambda: 2 * 4 + 3 == 11),
    q(PROOF, ERR, 1, r"""A student claims that $(a + b)^2 = a^2 + b^2$ for all real $a$ and $b$. Which values show that the claim is wrong?""",
      [r"$a = 0$, $b = 0$", r"$a = 1$, $b = 0$", r"$a = 0$, $b = 5$", r"$a = 1$, $b = 1$", r"$a = 0$, $b = -2$"], "D",
      r"$(1 + 1)^2 = 4$ but $1^2 + 1^2 = 2$. In every other pair one number is $0$, and then the claim happens to hold. In general $(a + b)^2 = a^2 + 2ab + b^2$.",
      check=lambda: (1 + 1) ** 2 != 1 + 1),
    q(PROOF, ERR, 2, r"""A student solves $x^2 = 3x$:

(1) Divide both sides by $x$: $x = 3$.
(2) So the only solution is $x = 3$.

What is wrong?""",
      [r"Line (1) divides by $x$, which could be $0$, and loses the solution $x = 0$.", r"Line (1) should give $x = \frac{1}{3}$.",
       r"Line (2) should say $x = \pm 3$.", r"Nothing: $x = 3$ is the only solution.", r"The equation has no real solutions."], "A",
      r"Dividing by $x$ assumes $x \ne 0$. Factorising instead, $x(x - 3) = 0$, gives both solutions, $x = 0$ and $x = 3$."),
    q(PROOF, ERR, 2, r"""A student solves $-2x < 6$:

(1) Divide both sides by $-2$: $x < -3$.

What is the correct solution?""", [r"$x < -3$", r"$x > -3$", r"$x < 3$", r"$x > 3$", r"$x < -12$"], "B",
      r"Dividing an inequality by a negative number reverses it, so $x > -3$. Check: $x = 0$ satisfies $-2x < 6$.",
      check=lambda: all((-2 * x < 6) == (x > -3) for x in range(-20, 20))),
    q(PROOF, ERR, 3, r"""A student 'proves' that $\dfrac{a + b}{2} \ge \sqrt{ab}$ for all positive $a$ and $b$:

(1) Assume $\dfrac{a + b}{2} \ge \sqrt{ab}$.
(2) Squaring, $(a + b)^2 \ge 4ab$.
(3) So $a^2 - 2ab + b^2 \ge 0$, that is $(a - b)^2 \ge 0$, which is true.
(4) Hence $\dfrac{a + b}{2} \ge \sqrt{ab}$.

What is the main flaw in this argument?""",
      [r"Line (2) is wrong: squaring is never allowed in an inequality.", r"$(a - b)^2 \ge 0$ is false for some values.",
       r"It starts by assuming what it is trying to prove; a correct proof must start from $(a - b)^2 \ge 0$ and work forwards.",
       r"The result is false for some positive $a$ and $b$.", r"Line (3) should give $(a + b)^2 \ge 0$."], "C",
      r"Reaching a true statement from the claim proves nothing. Running the steps backwards from $(a - b)^2 \ge 0$, each step reversible because both sides are positive, gives a valid proof."),
    q(PROOF, ERR, 3, r"""Which line contains the first error?

(1) Let $x = -3$.
(2) Then $x^2 = 9$.
(3) So $\sqrt{x^2} = \sqrt{9} = 3$.
(4) But $\sqrt{x^2} = x$, so $3 = -3$.""", ["(1)", "(2)", "(3)", "(4)", "There is no error."], "D",
      r"$\sqrt{x^2} = |x|$, not $x$. For $x = -3$, $\sqrt{x^2} = 3 = |x|$, so line (4) is the error.", check=lambda: math.sqrt((-3) ** 2) == abs(-3)),
])

save_drills("tmua", D)
