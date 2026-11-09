r"""Notenix SAT Practice Test 1. Run: python mock1.py  (writes mock-1.json)"""
from _sat import module, save_form
from mock1_rw import RW1, RW2E
from mock1_rw_hard import RW2H
from mock1_math import M1, M2E, M2H

save_form("mock-1", "SAT Practice Test 1", "mock", [
    module("rw1", "Reading and Writing: Module 1", "rw", 32, RW1),
    module("rw2e", "Reading and Writing: Module 2", "rw", 32, RW2E),
    module("rw2h", "Reading and Writing: Module 2", "rw", 32, RW2H),
    module("m1", "Math: Module 1", "math", 35, M1),
    module("m2e", "Math: Module 2", "math", 35, M2E),
    module("m2h", "Math: Module 2", "math", 35, M2H),
], summary="98 questions · 2 h 14 min · adaptive Module 2 in each section")
