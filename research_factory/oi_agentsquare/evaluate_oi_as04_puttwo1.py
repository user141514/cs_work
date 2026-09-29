import ast,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=ROOT/"oi_as04"/"react_puttwo_1"
planner=json.loads((D/"planningio.result.json").read_text(encoding="utf-8"))
memory=json.loads((D/"original_tp_memory.result.json").read_text(encoding="utf-8"))

# PlanningIO parse exactly as AgentSquare PlanningBase.
dicts=[ast.literal_eval(ds) for ds in re.findall(r"\{[^{}]*\}",planner["agent_text"])]

def pclass(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "first cellphone" in s and ("find" in s or "take" in s or "pick" in s) and "put" not in s:
        return "ACQUIRE(cellphone#1)"
    if "first cellphone" in s and "sofa" in s and ("put" in s or "place" in s):
        return "PLACE(cellphone#1,sofa)"
    if "second cellphone" in s and ("find" in s or "take" in s or "pick" in s) and "put" not in s:
        return "ACQUIRE(cellphone#2)"
    if "second cellphone" in s and "sofa" in s and ("put" in s or "place" in s):
        return "PLACE(cellphone#2,sofa)"
    return "OTHER"

psig=[pclass(d) for d in dicts if pclass(d)!="OTHER"]

mtext=memory["parsed"]["memory_text"].lower()

def pos(patterns):
    hits=[]
    for pat in patterns:
        m=re.search(pat,mtext)
        if m: hits.append(m.start())
    return min(hits) if hits else -1

p_acq1=pos([
    r"\btake the first\b",
    r"\btake the first cellphone\b",
])
p_place1=pos([
    r"\bgo to sofa 1, put it there\b",
    r"\bput the first .*sofa\b",
])
# 'return for the second' is an action-bearing retrieval clause: it explicitly
# denotes going back to obtain the second already-identified cellphone.
p_acq2=pos([
    r"\breturn for the second\b",
    r"\btake the second\b",
    r"\bpick up the second\b",
])
p_place2=pos([
    r"\bput it in sofa 1\b",
    r"\bput the second .*sofa\b",
])

msig=[]
if p_acq1>=0: msig.append(("ACQUIRE(cellphone#1)",p_acq1))
if p_place1>=0: msig.append(("PLACE(cellphone#1,sofa)",p_place1))
if p_acq2>=0: msig.append(("ACQUIRE(cellphone#2)",p_acq2))
if p_place2>=0: msig.append(("PLACE(cellphone#2,sofa)",p_place2))
msig=[x for x,_ in sorted(msig,key=lambda z:z[1])]

required=[
    "ACQUIRE(cellphone#1)",
    "PLACE(cellphone#1,sofa)",
    "ACQUIRE(cellphone#2)",
    "PLACE(cellphone#2,sofa)",
]
multiplicity_ok=("two distinct cellphones" in mtext and ("both cellphones" in mtext or len(msig)==4))
conflict = psig != required or msig != required or not multiplicity_ok or psig != msig

result={
    "target_key":"react_puttwo_1",
    "memory_key":"react_puttwo_0",
    "required_signature":required,
    "planningio_signature":psig,
    "original_tp_signature":msig,
    "multiplicity_ok":multiplicity_ok,
    "material_conflict":conflict,
    "status":"CONFLICT_EXPOSURE_PRESENT" if conflict else "NO_CONFLICT_EXPOSURE",
    "planningio_valid_no_tool_execution":planner.get("valid_no_tool_execution"),
    "planningio_usage":planner.get("usage"),
    "original_tp_usage":memory.get("usage"),
    "original_tp_memory_text":memory["parsed"]["memory_text"],
    "decision_boundary":"must preserve two cellphone acquisition-placement cycles and sofa destination; 'return for the second' counts as an action-bearing retrieval/acquisition clause, not a wording-level omission",
}
(D/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
