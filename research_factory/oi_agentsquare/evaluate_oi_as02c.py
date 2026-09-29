import ast, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
res=json.loads((ROOT/"oi_as02c/planningio.result.json").read_text(encoding="utf-8"))
text=res["agent_text"]

# Parse exactly as AgentSquare PlanningBase does.
dict_strings=re.findall(r"\{[^{}]*\}", text)
dicts=[ast.literal_eval(ds) for ds in dict_strings]

def classify(step):
    s=((step.get("description") or "")+" "+(step.get("reasoning instruction") or "")).lower()
    if "apple" in s and "heat" in s and "microwave" in s:
        return "HEAT(apple,microwave)"
    if "apple" in s and "fridge" in s and ("put" in s or "place" in s):
        return "PLACE(apple,fridge)"
    if "apple" in s and ("find" in s) and ("take" in s or "pick" in s):
        return "ACQUIRE(apple)"
    return "OTHER:"+s

planner_signature=[classify(d) for d in dicts]
expected=[
    "ACQUIRE(apple)",
    "HEAT(apple,microwave)",
    "PLACE(apple,fridge)",
]
recognized=[x for x in planner_signature if not x.startswith("OTHER:")]
material_conflict = recognized != expected

result={
    "status":"NO_CONFLICT_EXPOSURE" if not material_conflict else "CONFLICT_EXPOSURE_PRESENT",
    "planningio_parsed_subtasks":dicts,
    "planningio_signature":recognized,
    "original_tp_signature":expected,
    "material_conflict":material_conflict,
    "planningio_thread_id":res.get("thread_id"),
    "planningio_usage":res.get("usage"),
    "prompt_sha256":json.loads((ROOT/"oi_as02c/MANIFEST.json").read_text())["prompt_sha256"],
    "same_target_in_few_shot_and_query":True,
    "decision_boundary":"lexical differences and extra low-level hints do not count; only ordered macro responsibility conflict counts",
}
(ROOT/"OI_AS_02C_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
