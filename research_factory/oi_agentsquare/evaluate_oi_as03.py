import ast,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
planner=json.loads((ROOT/"oi_as03/planningio.clean.result.json").read_text(encoding="utf-8"))
memory=json.loads((ROOT/"oi_as03/original_tp_memory.result.json").read_text(encoding="utf-8"))

# Parse PlanningIO exactly as AgentSquare PlanningBase does.
ptext=planner["agent_text"]
dict_strings=re.findall(r"\{[^{}]*\}",ptext)
dicts=[ast.literal_eval(ds) for ds in dict_strings]

def classify_step(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "apple" in s and ("find" in s or "take" in s or "pick" in s) and "clean" not in s:
        return "ACQUIRE(apple)"
    if "apple" in s and "clean" in s and "sinkbasin" in s:
        return "CLEAN(apple,sinkbasin)"
    if "apple" in s and "sidetable" in s and ("put" in s or "place" in s):
        return "PLACE(apple,sidetable)"
    return "OTHER"

planning_sig=[classify_step(d) for d in dicts if classify_step(d)!="OTHER"]

mtext=memory["parsed"]["memory_text"].lower()
memory_sig=[]
# Parse action-bearing clauses, not incidental noun mentions in search-location lists.
def first_match_pos(patterns):
    hits=[]
    for pat in patterns:
        m=re.search(pat,mtext)
        if m: hits.append(m.start())
    return min(hits) if hits else -1

pos_acq=first_match_pos([
    r"\btake the apple\b",
    r"\bpick up the apple\b",
    r"\bpick the apple up\b",
])
pos_clean=first_match_pos([
    r"\bclean (?:the apple|it)\b",
    r"\bbring (?:the )?apple to sinkbasin[^.]*clean\b",
])
pos_place=first_match_pos([
    r"\bcarry the cleaned apple to sidetable\b",
    r"\bput (?:the )?(?:cleaned )?apple .*sidetable\b",
    r"\bput it .*sidetable\b",
])
if pos_acq>=0: memory_sig.append(("ACQUIRE(apple)",pos_acq))
if pos_clean>=0 and "sinkbasin" in mtext: memory_sig.append(("CLEAN(apple,sinkbasin)",pos_clean))
if pos_place>=0: memory_sig.append(("PLACE(apple,sidetable)",pos_place))
memory_sig=[x for x,_ in sorted(memory_sig,key=lambda z:z[1])]

required=["ACQUIRE(apple)","CLEAN(apple,sinkbasin)","PLACE(apple,sidetable)"]
material_conflict = planning_sig != required or memory_sig != required or planning_sig != memory_sig

result={
    "status":"CONFLICT_EXPOSURE_PRESENT" if material_conflict else "NO_CONFLICT_EXPOSURE",
    "material_conflict":material_conflict,
    "required_signature":required,
    "planningio_signature":planning_sig,
    "original_tp_signature":memory_sig,
    "planningio_subtasks":dicts,
    "planningio_thread_id":planner.get("thread_id"),
    "planningio_usage":planner.get("usage"),
    "planningio_valid_no_tool_execution":planner.get("valid_no_tool_execution"),
    "original_tp_memory_text":memory["parsed"]["memory_text"],
    "original_tp_thread_id":memory.get("thread_id"),
    "original_tp_usage":memory.get("usage"),
    "fixture_selection":json.loads((ROOT/"OI_AS_03_FIXTURE_SELECTION.json").read_text(encoding="utf-8"))["selected"],
    "decision_boundary":"material task-required macro conflict only; lexical/search/open-close differences do not count",
}
(ROOT/"OI_AS_03_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
