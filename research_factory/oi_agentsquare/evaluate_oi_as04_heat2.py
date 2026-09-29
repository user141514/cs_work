import ast,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=ROOT/"oi_as04"/"react_heat_2"
planner=json.loads((D/"planningio.result.json").read_text(encoding="utf-8"))
memory=json.loads((D/"original_tp_memory.result.json").read_text(encoding="utf-8"))

# PlanningIO parse exactly as AgentSquare PlanningBase.
dicts=[ast.literal_eval(ds) for ds in re.findall(r"\{[^{}]*\}",planner["agent_text"])]

def pclass(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "bread" in s and ("find" in s or "take" in s or "pick" in s) and "heat" not in s:
        return "ACQUIRE(bread)"
    if "bread" in s and "heat" in s and "microwave" in s:
        return "HEAT(bread,microwave)"
    if "bread" in s and "countertop" in s and ("put" in s or "place" in s):
        return "PLACE(bread,countertop)"
    return "OTHER"

psig=[pclass(d) for d in dicts if pclass(d)!="OTHER"]

mtext=memory["parsed"]["memory_text"].lower()

def pos(patterns):
    hits=[]
    for pat in patterns:
        m=re.search(pat,mtext)
        if m: hits.append(m.start())
    return min(hits) if hits else -1

p_acq=pos([
    r"\btake that specific bread instance\b",
    r"\btake (?:the |that )?bread\b",
    r"\bpick up (?:the |that )?bread\b",
])
p_heat=pos([
    r"\bgo to microwave 1, heat it\b",
    r"\bheat (?:the )?bread\b",
    r"\bmicrowave[^.]*heat\b",
])
p_place=pos([
    r"\bgo to a countertop and put the heated bread\b",
    r"\bput (?:the )?heated bread .*countertop\b",
    r"\bput (?:it|the bread) .*countertop\b",
])

msig=[]
if p_acq>=0: msig.append(("ACQUIRE(bread)",p_acq))
if p_heat>=0 and "microwave" in mtext: msig.append(("HEAT(bread,microwave)",p_heat))
if p_place>=0: msig.append(("PLACE(bread,countertop)",p_place))
msig=[x for x,_ in sorted(msig,key=lambda z:z[1])]

required=["ACQUIRE(bread)","HEAT(bread,microwave)","PLACE(bread,countertop)"]
conflict = psig != required or msig != required or psig != msig

result={
    "target_key":"react_heat_2",
    "memory_key":"react_heat_0",
    "required_signature":required,
    "planningio_signature":psig,
    "original_tp_signature":msig,
    "material_conflict":conflict,
    "status":"CONFLICT_EXPOSURE_PRESENT" if conflict else "NO_CONFLICT_EXPOSURE",
    "planningio_valid_no_tool_execution":planner.get("valid_no_tool_execution"),
    "planningio_usage":planner.get("usage"),
    "original_tp_usage":memory.get("usage"),
    "original_tp_memory_text":memory["parsed"]["memory_text"],
    "decision_boundary":"task-required macro conflict only; search details, optional open-close actions, and countertop index choice do not count",
}
(D/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
