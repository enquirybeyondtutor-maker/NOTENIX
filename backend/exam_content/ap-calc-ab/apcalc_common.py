"""Shared names for AP Calculus AB content scripts (match services/exams.EXAMS['ap-calc-ab'])."""
import math

LIMD, DIFD, INTD = "Limits and continuity", "Differentiation", "Integration"
LIM = "Limits and continuity"
DER, CHAIN, CTX, ANA = ("Derivative rules", "Chain, implicit and inverse",
                        "Contextual applications", "Analytical applications")
INT, DE, APP = "Integration and accumulation", "Differential equations", "Applications of integration"


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    return s * h / 3


def near(x, y, tol=5e-4):
    return abs(x - y) < tol


__all__ = ["math", "LIMD", "DIFD", "INTD", "LIM", "DER", "CHAIN", "CTX", "ANA", "INT", "DE", "APP", "simpson", "near"]
