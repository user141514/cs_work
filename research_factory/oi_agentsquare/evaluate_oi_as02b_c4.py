import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
C=ROOT/"oi_as02b_runs"/"C4"
fixture=json.loads((ROOT/"OI_AS_02B_FIXTURE.json").read_text(encoding="utf-8"))
gold=next(x["gold_action"] for x in fixture["checkpoints"] if x["id"]=="C4")

def norm(s):
    s=s.strip()
    if s.startswith(">"): s=s[1:].strip()
    if s.endswith("."): s=s[:-1]
    s=re.sub(r"\s+"," ",s)
    return s.lower()

arms={}
for arm in ["original","oi"]:
    r=json.loads((C/f"{arm}.result.json").read_text(encoding="utf-8"))
    action=r["parsed"]["action"]
    arms[arm]={
        "action":action,
        "normalized":norm(action),
        "correct":norm(action)==norm(gold),
        "usage":r["usage"],
        "elapsed_seconds":r["elapsed_seconds"],
        "thread_id":r["thread_id"],
    }

if arms["oi"]["correct"] and arms["original"]["correct"]:
    verdict="TIE_BOTH_CORRECT"
elif arms["oi"]["correct"] and not arms["original"]["correct"]:
    verdict="OI_BETTER"
elif arms["original"]["correct"] and not arms["oi"]["correct"]:
    verdict="ORIGINAL_BETTER"
else:
    verdict="TIE_BOTH_WRONG"

result={
    "checkpoint":"C4",
    "gold_action":gold,
    "gold_normalized":norm(gold),
    "arms":arms,
    "paired_difference":int(arms["oi"]["correct"])-int(arms["original"]["correct"]),
    "checkpoint_verdict":verdict,
    "scoring_boundary":"exact-normalized only; no post-hoc fuzzy or semantic partial credit",
    "shared_error_note":"both arms chose open microwave 1 while frozen AgentSquare trajectory gold is direct heat; do not change gold after observing outputs"
}
(C/"C4_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
