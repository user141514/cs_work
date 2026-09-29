import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
r0=json.loads((ROOT/"OI_AS_00_RESULT.json").read_text(encoding="utf-8"))
r4=json.loads((ROOT/"OI_AS_04_RESULT.json").read_text(encoding="utf-8"))
planning=json.loads((ROOT/"upstream/search/planning_modules.json").read_text(encoding="utf-8"))
memory=json.loads((ROOT/"upstream/search/memory_modules.json").read_text(encoding="utf-8"))
workflow=(ROOT/"upstream/runtime/workflow.py").read_text(encoding="utf-8")
alf=(ROOT/"upstream/runtime/alfworld_run.py").read_text(encoding="utf-8")

soft=r0["alfworld_executable_space"]["soft_by_type"]
assert soft=={
    "MEMORY_TO_REASONING_GUIDANCE":42,
    "PLANNING_TO_REASONING_GUIDANCE":175,
}
assert "PLANNING_TO_TOOL_GUIDANCE" not in soft

assert "sub_tasks = solver.planning" in workflow
assert "action = solver.reasoning" in workflow
assert "init_prompt = env.init_prompt_update(sub_tasks, sub_task_id)" in workflow
assert "Current task: ' + sub_tasks[sub_task_id]['reasoning instruction']" in alf

non_none_planners=[m for m in planning if m["name"]!="None"]
assert len(non_none_planners)==5
for m in non_none_planners:
    c=m["code"].lower()
    assert "reasoning instructions" in c
    assert m["performance"]>0
none_planner=next(m for m in planning if m["name"]=="None")
assert none_planner["performance"]==0

tp=next(m for m in memory if m["name"]=="TP")
assert tp["performance"]==0.36
assert r4["terminated_seam"]=="MemoryTP-plan-conflict"
assert r4["material_conflicts"]==0 and r4["eligible_targets_screened"]==6

candidates={
    "PLANNING_TO_REASONING_GUIDANCE":{
        "exposure_count":soft["PLANNING_TO_REASONING_GUIDANCE"],
        "A_independent_seam":True,
        "B_responsibility_conflict":False,
        "B_evidence":"Pinned workflow explicitly executes planner first, then injects each subtask reasoning instruction as Current task for the reasoning module; this is hierarchical planner-to-executor handoff, not two independent same-level action owners.",
        "C_identifiable_contrast":False,
        "C_evidence":"All five non-None planners emit reasoning instructions; the only unexposed planning option is None, which removes decomposition itself. Existing module labels therefore cannot isolate guidance from planning presence.",
        "D_preexisting_directional_evidence":False,
        "D_evidence":"OI-AS-00 provides occupancy only. Frozen planning labels do not vary the exposure among active planners, and OI-AS-01..04 produced no failure trace attributed to planner-to-reasoner guidance.",
        "E_minimal_isolated_intervention":True,
        "E_evidence":"A future study could in principle preserve subtask decomposition while replacing or removing the reasoning-instruction field, but that possibility alone is insufficient after B/C/D fail."
    },
    "MEMORY_TO_REASONING_GUIDANCE":{
        "exposure_count":soft["MEMORY_TO_REASONING_GUIDANCE"],
        "A_independent_seam":False,
        "A_evidence":"Under the frozen mapping CURRENT_GUIDANCE is TP-only; TP is exactly the MemoryTP/I3 seam terminated by OI-AS-04.",
        "B_responsibility_conflict":False,
        "B_evidence":"As a soft tag this is memory evidence or guidance consumed by reasoning; the only TP plan-authority form was already tested as the hard seam.",
        "C_identifiable_contrast":False,
        "C_evidence":"The soft exposure is concentrated in TP rather than varying independently of memory-module identity.",
        "D_preexisting_directional_evidence":False,
        "D_evidence":"The original TP low label motivated the hard seam, but the complete conflict-prevalence screen found 0/6 macro-plan conflicts; no distinct soft-guidance harm signal remains.",
        "E_minimal_isolated_intervention":True,
        "E_evidence":"OI-TP already demonstrated guidance-form manipulation is technically possible, but this is not an independent residual mechanism."
    },
    "PLANNING_TO_TOOL_GUIDANCE":{
        "exposure_count":0,
        "A_independent_seam":True,
        "B_responsibility_conflict":False,
        "C_identifiable_contrast":False,
        "D_preexisting_directional_evidence":False,
        "E_minimal_isolated_intervention":False,
        "eligibility":"ABSENT_FROM_ALFWORLD_EXECUTABLE_SPACE",
        "evidence":"AgentSquare ALFWorld search filters tooluse to None, so this soft tag has zero executable exposure."
    }
}

keys=[
    "A_independent_seam",
    "B_responsibility_conflict",
    "C_identifiable_contrast",
    "D_preexisting_directional_evidence",
    "E_minimal_isolated_intervention",
]
for c in candidates.values():
    c["passes_all_A_to_E"]=all(bool(c.get(k,False)) for k in keys)

admitted=[k for k,v in candidates.items() if v["passes_all_A_to_E"]]
result={
    "experiment":"OI-AS-05",
    "status":"COMPLETED_TERMINATE_AGENTSQUARE_ALFWORLD_OI_LINE" if not admitted else "COMPLETED_RETAIN_RESIDUAL_SEAM",
    "admitted_residual_seams":admitted,
    "candidates":candidates,
    "decision":"TERMINATE_AGENT_SQUARE_ALFWORLD_OI" if not admitted else "RETAIN_EXACTLY_ONE_NEW_SEAM",
    "hard_gate_integration_authorized":False,
    "new_intervention_authorized":bool(admitted),
    "scope_boundary":{
        "terminated":"Current AgentSquare/ALFWorld O+I research line under the frozen module space and evidence chain.",
        "not_terminated":"Orthogonality + Invariants as a general research idea on other baselines or tasks where an independent conflict mechanism is evidenced before intervention design."
    }
}
(ROOT/"OI_AS_05_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
