
import json, statistics
from pathlib import Path

root = Path("research_factory/oi_agentsquare/upstream/search")
rows = json.loads((root/"memory_modules.json").read_text(encoding="utf-8"))
by = {r["name"]: float(r["performance"]) for r in rows}
primary = ["DILU","Generative","TP","Voyager"]
missing = [x for x in primary if x not in by]
if missing:
    raise SystemExit(f"missing modules: {missing}")

tp = by["TP"]
admissible = [by[x] for x in primary if x != "TP"]
ordered = sorted(((name, by[name]) for name in primary), key=lambda x: x[1], reverse=True)
ranks = {name:i+1 for i,(name,_) in enumerate(ordered)}
unique_min = tp < min(admissible)
if tp >= statistics.median(admissible):
    verdict = "CONTRADICTORY"
elif unique_min:
    verdict = "DIRECTIONALLY_CONSISTENT"
else:
    verdict = "INCONCLUSIVE"

result = {
    "baseline_commit": "8f5b3fe5d8a32f9b59d20370823bef2a2c86928c",
    "population": primary,
    "exposure": {"violating": ["TP"], "admissible": ["DILU","Generative","Voyager"]},
    "performance": {name: by[name] for name in primary},
    "descending_rank": ranks,
    "tp_rank": ranks["TP"],
    "tp_minus_admissible_mean": tp - statistics.mean(admissible),
    "tp_minus_admissible_median": tp - statistics.median(admissible),
    "tp_unique_minimum": unique_min,
    "exact_one_sided_random_rank_probability": 0.25 if unique_min else None,
    "descriptive_none": by.get("None"),
    "verdict": verdict,
    "limitations": [
        "tiny n=4 module-level directional screen",
        "labels are module-level, not combination-level",
        "no causal or statistical-significance claim",
    ],
}
out = Path("research_factory/oi_agentsquare/OI_AS_01_RESULT.json")
out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
