"""Re-spread correct-answer positions (A-D) in existing test JSON files, e.g. the hand-written baselines."""
import json
import sys
from _q import _spread

for path in sys.argv[1:]:
    t = json.load(open(path, encoding="utf-8"))
    _spread(f"{t['slot']}-{t['subject']}", t["questions"])
    json.dump(t, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(path, [[q["options"].index(q["answer"]) for q in t["questions"]].count(k) for k in range(4)])
