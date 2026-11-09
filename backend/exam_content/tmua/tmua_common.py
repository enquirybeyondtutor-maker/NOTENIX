"""Shared names for TMUA content scripts (domains and skills match services/exams.EXAMS['tmua'])."""
ALG, GEO, CAL, LOGIC, PROOF = "Algebra and functions", "Geometry and graphs", "Calculus", "Logic", "Proof"
MAN, EQN, POLY, LOG, SEQ = ("Algebraic manipulation", "Equations and inequalities", "Polynomials",
                            "Exponentials and logarithms", "Sequences and series")
COORD, TRIG, GRAPH = "Coordinate geometry", "Trigonometry", "Graphs and transformations"
DIFF, INT = "Differentiation", "Integration"
STMT, NSC = "Logical statements", "Necessary and sufficient conditions"
PRF, ERR = "Proof and counterexamples", "Errors in proofs"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    k = 2
    while k * k <= n:
        if n % k == 0:
            return False
        k += 1
    return True
