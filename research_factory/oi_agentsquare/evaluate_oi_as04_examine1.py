import ast,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
D=ROOT/"oi_as04"/"react_examine_1"
planner=json.loads((D/"planningio.result.json").read_text(encoding="utf-8"))
memory=json.loads((D/"original_tp_memory.result.json").read_text(encoding="utf-8"))

# PlanningIO parse exactly as AgentSquare PlanningBase.
dicts=[ast.literal_eval(ds) for ds in re.findall(r"\{[^{}]*\}",planner["agent_text"])]

def pclass(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "pen" in s and ("find" in s or "take" in s or "pick" in s) and "desklamp" not in s:
        return "ACQUIRE(pen)"
    if "desklamp" in s and ("find" in s or "use" in s or "turn on" in s):
        return "FIND_USE(desklamp)"
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
    r"\bpen is found, take it\b",
    r"\btake the pen\b",
    r"\bpick up the pen\b",
])
p_lamp=pos([
    r"\bsearching .* for a desklamp; once found, use/turn on the desklamp\b",
    r"\bfind (?:and )?use a desklamp\b",
    r"\buse/turn on the desklamp\b",
    r"\bturn on the desklamp\b",
    r"\buse the desklamp\b",
])

msig=[]
if p_acq>=0: msig.append(("ACQUIRE(pen)",p_acq))
if p_lamp>=0: msig.append(("FIND_USE(desklamp)",p_lamp))
msig=[x for x,_ in sorted(msig,key=lambda z:z[1])]

required=["ACQUIRE(pen)","FIND_USE(desklamp)"]
conflict = psig != required or msig != required or psig != msig
extra_examine = bool(re.search(r"\bexamine the pen with the desklamp\b",mtext))

result={
    "target_key":"react_examine_1",
    "memory_key":"react_examine_0",
    "required_signature":required,
    "planningio_signature":psig,
    "original_tp_signature":msig,
    "material_conflict":conflict,
    "status":"CONFLICT_EXPOSURE_PRESENT" if conflict else "NO_CONFLICT_EXPOSURE",
    "planningio_valid_no_tool_execution":planner.get("valid_no_tool_execution"),
    "planningio_usage":planner.get("usage"),
    "original_tp_usage":memory.get("usage"),
    "original_tp_memory_text":memory["parsed"]["memory_text"],
    "extra_redundant_examine_phrase":extra_examine,
    "decision_boundary":"required macros are ACQUIRE(pen)->FIND_USE(desklamp); extra verbal restatement of the final examine goal is not a separate frozen planner macro and does not create conflict",
}
(D/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
