import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = ROOT / "upstream" / "runtime" / "prompts" / "alfworld_3prompts.json"
data = json.loads(source.read_text(encoding="utf-8"))

memory = data["react_heat_0"]
target = data["react_heat_1"]
lines = target.splitlines()

gold_actions = [
    "open fridge 1",
    "take apple 1 from diningtable 1",
    "go to microwave 1",
    "heat apple 1 with microwave 1",
    "put apple 1 in/on fridge 1",
]

checkpoints = []
for idx, action in enumerate(gold_actions, 1):
    marker = "> " + action
    positions = [i for i, line in enumerate(lines) if line.strip() == marker]
    if len(positions) != 1:
        raise RuntimeError("%r expected once, got %r" % (marker, positions))
    pos = positions[0]
    prefix = "\n".join(lines[:pos]).rstrip() + "\n>"
    checkpoints.append({
        "id": "C%d" % idx,
        "gold_action": action,
        "prefix": prefix,
    })

first_action = next(i for i, line in enumerate(lines) if line.startswith("> "))
target_initial = "\n".join(lines[:first_action]).strip()

fixture = {
    "source_file": source.as_posix(),
    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "memory_key": "react_heat_0",
    "target_key": "react_heat_1",
    "memory_success_case": memory,
    "target_initial": target_initial,
    "planner_owned_plan": [
        "Find and take the apple.",
        "Heat the apple with microwave 1.",
        "Put the heated apple in/on fridge 1.",
    ],
    "checkpoints": checkpoints,
}

out = ROOT / "OI_AS_02B_FIXTURE.json"
out.write_text(json.dumps(fixture, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({
    "source_sha256": fixture["source_sha256"],
    "memory_chars": len(memory),
    "target_initial_chars": len(target_initial),
    "checkpoints": [{"id": c["id"], "gold_action": c["gold_action"], "prefix_chars": len(c["prefix"])} for c in checkpoints],
}, indent=2))
