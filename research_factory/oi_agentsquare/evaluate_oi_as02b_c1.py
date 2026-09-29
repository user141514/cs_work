import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
C=ROOT/"oi_as02b_runs"/"C1"
fixture=json.loads((ROOT/"OI_AS_02B_FIXTURE.json").read_text(encoding="utf-8"))
gold=next(x["gold_action"] for x in fixture["checkpoints"] if x["id"]=="C1")

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

result={
    "checkpoint":"C1",
    "gold_action":gold,
    "gold_normalized":norm(gold),
    "arms":arms,
    "paired_difference":int(arms["oi"]["correct"])-int(arms["original"]["correct"]),
    "checkpoint_verdict":"TIE_BOTH_CORRECT" if arms["oi"]["correct"] and arms["original"]["correct"] else (
        "OI_BETTER" if arms["oi"]["correct"] and not arms["original"]["correct"] else
        "ORIGINAL_BETTER" if arms["original"]["correct"] and not arms["oi"]["correct"] else
        "TIE_BOTH_WRONG"
    )
}
(C/"C1_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
