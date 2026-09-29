import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

rows=[]
# OI-AS-03 supplied the first eligible target result.
oi3=json.loads((ROOT/"OI_AS_03_RESULT.json").read_text(encoding="utf-8"))
rows.append({
    "target_key":"react_clean_1",
    "source":"OI-AS-03",
    "status":oi3["status"],
    "material_conflict":oi3["material_conflict"],
})

for key in ["react_cool_1","react_examine_1","react_heat_2","react_put_1","react_puttwo_1"]:
    x=json.loads((ROOT/"oi_as04"/key/"RESULT.json").read_text(encoding="utf-8"))
    rows.append({
        "target_key":key,
        "source":"OI-AS-04",
        "status":x["status"],
        "material_conflict":x["material_conflict"],
    })

conflicts=sum(int(x["material_conflict"]) for x in rows)
result={
    "experiment":"OI-AS-04",
    "status":"COMPLETED_TERMINATE_MEMORYTP_PLAN_CONFLICT_SEAM",
    "eligible_targets_screened":len(rows),
    "material_conflicts":conflicts,
    "conflict_rate":conflicts/len(rows),
    "targets":rows,
    "stop_rule_triggered":conflicts==0 and len(rows)==6,
    "terminated_seam":"MemoryTP-plan-conflict",
    "claim_boundary":{
        "supported":"Across the complete frozen eligible ALFWorld prompt-bank target set under the pre-registered lexical-nearest pairing screen, Original TP did not produce a material macro-plan conflict with PlanningIO in any of six targets.",
        "not_supported":[
            "This does not prove MemoryTP can never conflict under embedding retrieval or other tasks.",
            "This does not kill broader Orthogonality + Invariants.",
            "This does not establish full-episode task superiority for OI-TP.",
        ],
    },
}
(ROOT/"OI_AS_04_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
