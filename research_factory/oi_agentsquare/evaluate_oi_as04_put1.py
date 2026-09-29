import ast,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=ROOT/"oi_as04"/"react_put_1"
planner=json.loads((D/"planningio.result.json").read_text(encoding="utf-8"))
memory=json.loads((D/"original_tp_memory.result.json").read_text(encoding="utf-8"))

# PlanningIO parse exactly as AgentSquare PlanningBase.
dicts=[ast.literal_eval(ds) for ds in re.findall(r"\{[^{}]*\}",planner["agent_text"])]

def pclass(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "apple" in s and ("find" in s or "take" in s or "pick" in s) and "put" not in s:
        return "ACQUIRE(apple)"
    if "apple" in s and "sidetable" in s and ("put" in s or "place" in s):
        return "PLACE(apple,sidetable)"
    if "apple" in s and "clean" in s and "sinkbasin" in s:
        return "CLEAN(apple,sinkbasin)"
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
    r"\btake that specific apple\b",
    r"\btake (?:the |that )?apple\b",
    r"\bpick up (?:the |that )?apple\b",
])
p_place=pos([
    r"\bgo to sidetable 1, and put it there\b",
    r"\bgo to sidetable[^.]*put (?:the )?apple\b",
    r"\bput (?:the )?apple .*sidetable\b",
])
p_clean=pos([
    r"\bclean (?:the )?apple\b",
    r"\bbring (?:the )?apple to sinkbasin[^.]*clean\b",
])

msig=[]
if p_acq>=0: msig.append(("ACQUIRE(apple)",p_acq))
if p_clean>=0: msig.append(("CLEAN(apple,sinkbasin)",p_clean))
if p_place>=0: msig.append(("PLACE(apple,sidetable)",p_place))
msig=[x for x,_ in sorted(msig,key=lambda z:z[1])]

required=["ACQUIRE(apple)","PLACE(apple,sidetable)"]
forbidden_extra="CLEAN(apple,sinkbasin)"
conflict = psig != required or msig != required or forbidden_extra in psig or forbidden_extra in msig or psig != msig

result={
    "target_key":"react_put_1",
    "memory_key":"react_clean_1",
    "required_signature":required,
    "forbidden_extra_macro":forbidden_extra,
    "planningio_signature":psig,
    "original_tp_signature":msig,
    "material_conflict":conflict,
    "status":"CONFLICT_EXPOSURE_PRESENT" if conflict else "NO_CONFLICT_EXPOSURE",
    "planningio_valid_no_tool_execution":planner.get("valid_no_tool_execution"),
    "planningio_usage":planner.get("usage"),
    "original_tp_usage":memory.get("usage"),
    "original_tp_memory_text":memory["parsed"]["memory_text"],
    "decision_boundary":"task-required ACQUIRE->PLACE only; inserting CLEAN from the paired clean-memory task would be material conflict; incidental sinkbasin search mentions do not count",
}
(D/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
