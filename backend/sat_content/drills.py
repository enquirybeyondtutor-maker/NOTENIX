r"""Notenix SAT skill drills: one 'module' per skill (6 questions each), plus a short description
of every skill for the drill pages and the public /sat/skills pages.
Run: python drills.py  (writes drills.json, and frontend/lib/sat-skills.json for the SEO pages)."""
import json
import re
from pathlib import Path

from _sat import module, save_form, RW_SKILLS, MATH_SKILLS
from drills_rw import D as RW
from drills_math import D as MATH

INFO = {
    "Words in Context": "Choosing the most precise word or phrase for a blank, using clues in the sentence around it.",
    "Text Structure and Purpose": "Working out why a text was written and how its sentences fit together.",
    "Cross-Text Connections": "Comparing two short texts and predicting how one author would respond to the other.",
    "Central Ideas and Details": "Finding the main idea of a passage and the details that support it.",
    "Command of Evidence: Textual": "Choosing the finding or quotation that best supports a claim.",
    "Command of Evidence: Quantitative": "Using data from a table or graph to complete or support a statement.",
    "Inferences": "Choosing the most logical conclusion that follows from a passage.",
    "Boundaries": "Punctuating between clauses and phrases: commas, semicolons, colons and full stops.",
    "Form, Structure, and Sense": "Subject-verb agreement, verb tense, pronouns and modifiers.",
    "Transitions": "Choosing the linking word that shows how two ideas connect.",
    "Rhetorical Synthesis": "Using notes to write a sentence that achieves a specific goal.",
    "Linear equations in one variable": "Solving equations like $5(x - 2) = 3x + 6$, and spotting when there are no or infinitely many solutions.",
    "Linear functions": "Reading and building functions like $f(x) = mx + b$ from words, tables and graphs.",
    "Linear equations in two variables": "Slopes, intercepts and equations of lines, including parallel and perpendicular lines.",
    "Systems of linear equations": "Solving two equations together, and when a system has no or infinitely many solutions.",
    "Linear inequalities": "Solving inequalities and using them to model limits like budgets and capacities.",
    "Nonlinear functions": "Quadratic and exponential functions: vertices, growth and decay.",
    "Nonlinear equations and systems": "Solving quadratics and systems that include a curve.",
    "Equivalent expressions": "Expanding, factorising and simplifying expressions, including exponents.",
    "Ratios, rates and units": "Proportions, speeds, unit conversions and scale.",
    "Percentages": "Percentages of amounts, percentage change and reverse percentages.",
    "One-variable data": "Mean, median, mode, range and spread of a data set.",
    "Two-variable data and models": "Scatterplots, lines of best fit and linear or exponential models.",
    "Probability": "Simple and conditional probability, including two-way tables.",
    "Sample statistics and margin of error": "What a random sample tells you about a population, and margins of error.",
    "Studies and experiments": "When a study shows cause and effect, and who its results apply to.",
    "Area and volume": "Areas and volumes of 2D and 3D shapes, and how they scale.",
    "Lines, angles and triangles": "Angle facts, parallel lines and similar triangles.",
    "Right triangles and trigonometry": "Pythagoras, special right triangles, and sine, cosine and tangent.",
    "Circles": "Circumference, area, arcs, sectors and circle equations.",
}


def slug(skill: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", skill.lower()).strip("-")


_NUMERIC = re.compile(r"^\$?-?[\d.,{}]+\$?$")


def spread_math(questions: list, start: int) -> None:
    """Move correct answers to an even cycle of letters, but only for questions whose options
    are not plain numbers (numeric options stay in increasing order, as on the SAT)."""
    order = "DACB"
    for n, q in enumerate(questions):
        if q["type"] != "mcq" or all(_NUMERIC.match(o.replace(" ", "")) for o in q["options"]):
            continue
        target = order[(start + n) % 4]
        i, j = "ABCD".index(q["answer"]), "ABCD".index(target)
        q["options"][i], q["options"][j] = q["options"][j], q["options"][i]
        q["answer"] = target


def main():
    mods = []
    for n, skill in enumerate(MATH):
        spread_math(MATH[skill], n)
    for domains, bank, section in ((RW_SKILLS, RW, "rw"), (MATH_SKILLS, MATH, "math")):
        for domain, skills in domains.items():
            for skill in skills:
                qs = bank[skill]
                assert len(qs) == 6, f"{skill}: {len(qs)} questions"
                key, m = module(slug(skill), skill, section, 0, qs)
                m["domain"], m["about"] = domain, INFO[skill]
                mods.append((key, m))
    save_form("drills", "SAT skill drills", "drills", mods, summary="6 practice questions for each SAT skill")

    # Public skill pages: description + the first 3 questions of each drill (with answers).
    data = json.loads((Path(__file__).parent / "drills.json").read_text(encoding="utf-8"))
    pages = [{"slug": k, "skill": m["title"], "domain": m["domain"], "section": m["section"], "about": m["about"],
              "samples": m["questions"][:3]} for k, m in data["modules"].items()]
    out = Path(__file__).resolve().parents[2] / "frontend" / "lib" / "sat-skills.json"
    out.write_text(json.dumps(pages, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(pages)} skill pages -> {out.name}")


if __name__ == "__main__":
    main()
