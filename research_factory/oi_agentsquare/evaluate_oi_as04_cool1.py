import ast,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=ROOT/"oi_as04"/"react_cool_1"
planner=json.loads((D/"planningio.result.json").read_text(encoding="utf-8"))
memory=json.loads((D/"original_tp_memory.result.json").read_text(encoding="utf-8"))

# PlanningIO parse exactly as AgentSquare PlanningBase.
ptext=planner["agent_text"]
dicts=[ast.literal_eval(ds) for ds in re.findall(r"\{[^{}]*\}",ptext)]

def pclass(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "mug" in s and ("find" in s or "take" in s or "pick" in s) and "cool" not in s:
        return "ACQUIRE(mug)"
    if "mug" in s and "cool" in s and "fridge" in s:
        return "COOL(mug,fridge)"
    if "mug" in s and "shelf" in s and ("put" in s or "place" in s):
        return "PLACE(mug,shelf)"
    return "OTHER"

psig=[pclass(d) for d in dicts if pclass(d)!="OTHER"]

mtext=memory["parsed"]["memory_text"].lower()
def pos(patterns):
    hits=[]
    for pat in patterns:
        m=re.search(pat,mtext)
        if m: hits.append(m.start())
    return min(hits) if hits else -1

p_acq=pos([r"\btake the mug\b",r"\bpick up the mug\b",r"\bpick the mug up\b"])
p_cool=pos([r"\bcool (?:the mug|it)\b",r"\bgo to fridge[^.]*cool\b"])
p_place=pos([
    r"\bput (?:the )?(?:cooled|cool )?mug .*shelf\b",
    r"\bput (?:it|the cooled mug) .*shelf\b",
    r"\bvisit shelf[^.]*put the cooled mug\b",
    r"\bgo to (?:a )?shelf[^.]*put (?:the )?(?:cooled|cool )?mug\b",
])

msig=[]
if p_acq>=0: msig.append(("ACQUIRE(mug)",p_acq))
if p_cool>=0 and "fridge" in mtext: msig.append(("COOL(mug,fridge)",p_cool))
if p_place>=0: msig.append(("PLACE(mug,shelf)",p_place))
msig=[x for x,_ in sorted(msig,key=lambda z:z[1])]

required=["ACQUIRE(mug)","COOL(mug,fridge)","PLACE(mug,shelf)"]
conflict = psig != required or msig != required or psig != msig

result={
    "target_key":"react_cool_1",
    "memory_key":"react_cool_0",
    "required_signature":required,
    "planningio_signature":psig,
    "original_tp_signature":msig,
    "material_conflict":conflict,
    "status":"CONFLICT_EXPOSURE_PRESENT" if conflict else "NO_CONFLICT_EXPOSURE",
    "planningio_valid_no_tool_execution":planner.get("valid_no_tool_execution"),
    "planningio_usage":planner.get("usage"),
    "original_tp_usage":memory.get("usage"),
    "original_tp_memory_text":memory["parsed"]["memory_text"],
    "decision_boundary":"task-required macro conflict only; lexical/search/open-close differences do not count",
}
(D/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
