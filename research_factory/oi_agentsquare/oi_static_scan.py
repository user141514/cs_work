#!/usr/bin/env python3
"""Outcome-blind O+I headroom scan over frozen AgentSquare module catalogs."""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream" / "search"
TYPES = ("planning", "reasoning", "tooluse", "memory")

def load(kind: str):
    return json.loads((UPSTREAM / f"{kind}_modules.json").read_text(encoding="utf-8"))

catalogs = {kind: load(kind) for kind in TYPES}
by_name = {kind: {m["name"]: m for m in mods} for kind, mods in catalogs.items()}

# Source-anchored semantic guards: refuse to silently apply the frozen mapping
# if the pinned upstream code no longer expresses these behaviors.
for module in catalogs["planning"]:
    if module["name"] == "None":
        continue
    code = module["code"].lower()
    assert "reasoning instructions" in code, module["name"]
    assert "instructions for calling the tool" in code, module["name"]

tp = by_name["memory"]["TP"]
tp_code = tp["code"].lower()
assert "generate plans based on similar experiences" in tp_code
assert "plan from successful attempt" in tp_code

def signature(kind: str, name: str):
    if name == "None":
        return set()
    if kind == "planning":
        return {"DECOMPOSE", "REASON_GUIDE", "TOOL_GUIDE"}
    if kind == "reasoning":
        return {"REASON"}
    if kind == "tooluse":
        if name in {"ANYTOOL", "TOOLBENCH", "TOOLFORMER"}:
            return {"TOOL_SELECT"}
        return {"TOOL_RESPONSE"}
    if kind == "memory":
        if name == "TP":
            return {"MEMORY_RETRIEVE", "CURRENT_GUIDANCE", "PLAN_CONTROL"}
        return {"MEMORY_RETRIEVE"}
    raise AssertionError(kind)

def evaluate(config):
    sig = {kind: signature(kind, config[kind]) for kind in TYPES}
    hard = []
    soft = []

    # I1: concrete tool/API selection has one authority.
    tool_select_owners = [k for k, tags in sig.items() if "TOOL_SELECT" in tags]
    if len(tool_select_owners) > 1:
        hard.append("I1_MULTIPLE_TOOL_SELECT")

    # I2: current task decomposition/plan control must not be duplicated.
    planning_active = config["planning"] != "None"
    foreign_plan_owners = [k for k, tags in sig.items() if k != "planning" and "PLAN_CONTROL" in tags]
    if planning_active and foreign_plan_owners:
        hard.append("I2_DECOMPOSITION_AUTHORITY")

    # I3: memory is evidence/guidance boundary, not current-plan authority.
    if "PLAN_CONTROL" in sig["memory"] or "TOOL_SELECT" in sig["memory"]:
        hard.append("I3_MEMORY_BOUNDARY")

    # Soft coupling: cross-boundary guidance without outright rejection.
    if planning_active and config["reasoning"] != "None" and "REASON_GUIDE" in sig["planning"]:
        soft.append("PLANNING_TO_REASONING_GUIDANCE")
    if planning_active and config["tooluse"] != "None" and "TOOL_GUIDE" in sig["planning"]:
        soft.append("PLANNING_TO_TOOL_GUIDANCE")
    if "CURRENT_GUIDANCE" in sig["memory"] and config["reasoning"] != "None":
        soft.append("MEMORY_TO_REASONING_GUIDANCE")

    return {"hard": sorted(set(hard)), "soft": sorted(set(soft)), "signatures": {k: sorted(v) for k, v in sig.items()}}

def enumerate_space(tooluse_names):
    names = {
        "planning": [m["name"] for m in catalogs["planning"]],
        "reasoning": [m["name"] for m in catalogs["reasoning"]],
        "tooluse": tooluse_names,
        "memory": [m["name"] for m in catalogs["memory"]],
    }
    rows = []
    for values in itertools.product(*(names[k] for k in TYPES)):
        config = dict(zip(TYPES, values))
        rows.append({"config": config, **evaluate(config)})
    return rows

def summarize(rows):
    n = len(rows)
    hard_rows = [r for r in rows if r["hard"]]
    soft_rows = [r for r in rows if r["soft"]]
    hard_types = Counter(x for r in rows for x in r["hard"])
    soft_types = Counter(x for r in rows for x in r["soft"])
    module_participation = defaultdict(Counter)
    for r in rows:
        if r["hard"]:
            for kind, name in r["config"].items():
                module_participation[kind][name] += 1
    reps = []
    seen = set()
    for r in hard_rows:
        key = tuple(r["hard"])
        if key not in seen:
            seen.add(key)
            reps.append({"config": r["config"], "hard": r["hard"], "soft": r["soft"]})
    return {
        "total": n,
        "hard_inadmissible": len(hard_rows),
        "hard_inadmissible_rate": len(hard_rows) / n if n else 0,
        "soft_coupled": len(soft_rows),
        "soft_coupled_rate": len(soft_rows) / n if n else 0,
        "hard_by_type": dict(sorted(hard_types.items())),
        "soft_by_type": dict(sorted(soft_types.items())),
        "hard_module_participation": {k: dict(sorted(v.items())) for k, v in module_participation.items()},
        "representative_hard_conflicts": reps,
    }

alfworld = enumerate_space(["None"])
full = enumerate_space([m["name"] for m in catalogs["tooluse"]])

assert len(alfworld) == 6 * 7 * 1 * 5 == 210
assert len(full) == 6 * 7 * 5 * 5 == 1050

result = {
    "baseline": {
        "repo": "tsinghua-fib-lab/AgentSquare",
        "commit": "8f5b3fe5d8a32f9b59d20370823bef2a2c86928c",
        "seam": "recombination -> OI gate -> predict_performance",
    },
    "mapping_guards": {
        "all_non_none_planning_emit_reasoning_instructions": True,
        "all_non_none_planning_emit_tool_calling_instructions": True,
        "memory_TP_generates_current_plans": True,
    },
    "alfworld_executable_space": summarize(alfworld),
    "full_catalog_diagnostic": summarize(full),
}
rate = result["alfworld_executable_space"]["hard_inadmissible_rate"]
if rate < 0.05:
    verdict = "ZERO_OR_NEGLIGIBLE_HEADROOM"
elif rate < 0.25:
    verdict = "NONTRIVIAL_HEADROOM"
else:
    verdict = "LARGE_HEADROOM"
result["triage_verdict"] = verdict

out = ROOT / "OI_AS_00_RESULT.json"
out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
