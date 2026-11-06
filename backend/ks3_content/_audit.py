"""Audit every KS3 test and note JSON: stray backslashes outside $...$ maths, control characters,
answer present, 4 distinct options, topics set, and the answer-position spread."""
import glob
import json
import re
import sys

BS = chr(92)
problems = 0
for f in sorted(glob.glob("tests/*.json")):
    t = json.load(open(f, encoding="utf-8"))
    spots = []
    for i, q in enumerate(t["questions"], 1):
        texts = [q["question"], q["explanation"], *q["options"]]
        for s in texts:
            outside = re.sub(r"\$[^$]*\$", "", s)
            if BS in outside or BS + BS in s or any(c in s for c in "\t\f\b\r\v\a"):
                print(f"{f} Q{i}: odd character in {s[:70]!r}")
                problems += 1
        if q["answer"] not in q["options"] or len(set(q["options"])) != 4 or not q.get("topic"):
            print(f"{f} Q{i}: answer/options/topic problem")
            problems += 1
        spots.append(q["options"].index(q["answer"]))
    print(f"{f}: {len(t['questions'])} Qs, answers at A-D: {[spots.count(k) for k in range(4)]}")
for f in sorted(glob.glob("notes/*.json")):
    n = json.load(open(f, encoding="utf-8"))
    outside = re.sub(r"\$[^$]*\$", "", n["body"])
    if BS in outside or any(c in n["body"] for c in "\t\f\b\r\v\a"):
        print(f"{f}: odd character")
        problems += 1
print("PROBLEMS:", problems)
sys.exit(1 if problems else 0)
