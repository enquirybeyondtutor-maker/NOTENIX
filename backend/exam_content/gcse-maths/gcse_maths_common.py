"""Shared names for GCSE Maths content scripts (match services/exams.EXAMS['gcse-maths'])."""
import math
from fractions import Fraction as Fr

NUM, ALG, RAT, GEO, PS = "Number", "Algebra", "Ratio and proportion", "Geometry and measures", "Probability and statistics"
FDP, IND, FAC = "Fractions, decimals and percentages", "Indices, standard form and surds", "Factors, multiples and estimation"
EXP, EQN, SEQ, GRA = "Expressions and formulae", "Equations and inequalities", "Sequences", "Graphs and functions"
RP, PCT = "Ratio and proportion", "Percentage change and growth"
ANG, AREA, TRIG, VEC = "Angles and shapes", "Area, volume and Pythagoras", "Trigonometry", "Vectors and transformations"
PROB, STAT = "Probability", "Statistics"

R = range(-6, 7)


def near(x, y, tol=5e-3):
    return abs(x - y) < tol


def sin(d):
    return math.sin(math.radians(d))


def cos(d):
    return math.cos(math.radians(d))


def tan(d):
    return math.tan(math.radians(d))


__all__ = ["math", "Fr", "NUM", "ALG", "RAT", "GEO", "PS", "FDP", "IND", "FAC", "EXP", "EQN", "SEQ", "GRA", "RP", "PCT",
           "ANG", "AREA", "TRIG", "VEC", "PROB", "STAT", "R", "near", "sin", "cos", "tan"]
