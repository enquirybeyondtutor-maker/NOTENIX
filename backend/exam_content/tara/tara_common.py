"""Shared names for TARA content scripts (domains and skills match services/exams.EXAMS['tara'])."""
CT, PS = "Critical thinking", "Problem solving"
MAIN, CONC, ASSUME, STRW, FLAW, MATCH, PRIN = ("Main conclusion", "Drawing conclusions", "Assumptions",
                                              "Strengthening and weakening", "Flaws in reasoning",
                                              "Matching arguments", "Applying principles")
REL, PROC, SIM = "Relevant selection", "Finding procedures", "Identifying similarity"

Q_MAIN = "Which of the following best expresses the main conclusion of the above argument?"
Q_CONC = "Which of the following conclusions can be drawn from the above passage?"
Q_ASSUME = "Which of the following is an underlying assumption of the above argument?"
Q_WEAK = "Which of the following, if true, would most weaken the above argument?"
Q_STR = "Which of the following, if true, would most strengthen the above argument?"
Q_FLAW = "Which of the following best identifies the flaw in the above argument?"
Q_MATCH = "Which of the following most closely parallels the reasoning used in the above argument?"
Q_PRIN = "Which of the following best illustrates the principle underlying the above argument?"


import hashlib as _h
import re as _re
import sys as _sys
from pathlib import Path as _P

_sys.path.insert(0, str(_P(__file__).resolve().parent.parent))
from _exam import q as _q  # noqa: E402

_DOMAIN = {s: CT for s in (MAIN, CONC, ASSUME, STRW, FLAW, MATCH, PRIN)} | {s: PS for s in (REL, PROC, SIM)}


def _num(s):
    t = _re.search(r"(\d{1,2}):(\d{2})", s)   # a time: minutes after midnight
    if t:
        return int(t.group(1)) * 60 + int(t.group(2)) + (720 if "pm" in s and int(t.group(1)) != 12 else 0)
    m = _re.search(r"-?\d[\d,]*(?:\.\d+)?", s.replace("£", ""))
    return float(m.group().replace(",", "")) if m else None


_rng = __import__("random").Random(2026)
_slots: list[int] = []


def _next_slot() -> int:
    """Answer positions for text options: each block of five questions uses every position once."""
    if not _slots:
        block = [0, 1, 2, 3, 4]
        _rng.shuffle(block)
        _slots.extend(block)
    return _slots.pop(0)


def mc(skill, diff, question, correct, wrongs, explanation, passage=None, check=None, order=None, options=None):
    """A five-option question written with the right answer first. Numeric options are put in
    ascending order; text options are placed so the right answer's letter varies (a stable
    pseudo-random slot from the question text). order="keep" keeps options as written."""
    opts = [correct, *wrongs]
    if options:   # options given in display order (e.g. days of the week); must hold correct + wrongs
        assert sorted(options) == sorted(opts), f"options do not match: {question[:60]}"
        opts = list(options)
    elif order == "keep":
        pass
    elif all(_num(o) is not None and len(o) <= 12 for o in opts):   # plain numbers, sums of money, times
        opts = sorted(opts, key=_num)
    else:
        slot = _next_slot() % len(opts)
        rest = list(wrongs)
        opts = rest[:slot] + [correct] + rest[slot:]
    letter = "ABCDEFGH"[opts.index(correct)]
    return _q(_DOMAIN[skill], skill, diff, question, opts, letter, explanation, check=check, passage=passage)
