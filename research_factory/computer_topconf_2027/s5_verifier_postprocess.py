#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("usage: s5_verifier_postprocess.py <gates.json> <reward.txt> <evaluator_probe.json>")

gates_path = Path(sys.argv[1])
reward_path = Path(sys.argv[2])
probe_path = Path(sys.argv[3])

probe = json.loads(probe_path.read_text(encoding="utf-8"))
required_probe = ("dirNoTrailingSpace", "dirMarker", "fileTerminates", "observed")
missing = [k for k in required_probe if k not in probe]
if missing:
    raise SystemExit(f"probe missing keys: {missing}")

# Terminal-file preservation is a frozen requirement sanity check.
# It is deliberately non-weighted, but an evaluator run is invalid if it fails.
if not probe["fileTerminates"]:
    raise SystemExit("evaluator sanity failed: terminal-file completion behavior was not preserved")

records = []
for raw in gates_path.read_text(encoding="utf-8").splitlines():
    raw = raw.strip()
    if not raw:
        continue
    records.append(json.loads(raw))

replacement = {
    "t7_f2p_autocomplete_dir_no_trailing_space": {
        "id": "t7_f2p_autocomplete_dir_no_trailing_space",
        "passed": bool(probe["dirNoTrailingSpace"]),
        "detail": "direct CombinedAutocompleteProvider.applyCompletion probe: "
                  f"line={probe['observed']['dirLine']!r} cursor={probe['observed']['dirCursorCol']}",
    },
    "t7_f2p_autocomplete_dir_marker": {
        "id": "t7_f2p_autocomplete_dir_marker",
        "passed": bool(probe["dirMarker"]),
        "detail": "direct CombinedAutocompleteProvider.applyCompletion probe: "
                  f"directory marker preserved={bool(probe['dirMarker'])}",
    },
}

seen = set()
corrected = []
for rec in records:
    gid = rec.get("id")
    if gid in replacement:
        if gid not in seen:
            corrected.append(replacement[gid])
            seen.add(gid)
        continue
    corrected.append(rec)

for gid in replacement:
    if gid not in seen:
        corrected.append(replacement[gid])

gates_path.write_text(
    "".join(json.dumps(rec, separators=(",", ":")) + "\n" for rec in corrected),
    encoding="utf-8",
)

weights = {
    "t1_f2p_changelog_unreleased_grew": 0.25,
    "t1_f2p_changelog_attribution_format": 0.25,
    "t7_f2p_autocomplete_dir_no_trailing_space": 0.30,
    "t7_f2p_autocomplete_dir_marker": 0.20,
}

latest = {}
for rec in corrected:
    gid = rec.get("id")
    if gid:
        latest[gid] = bool(rec.get("passed"))

reward = sum(weight for gid, weight in weights.items() if latest.get(gid, False))
reward_path.write_text(f"{reward:.4f}\n", encoding="utf-8")

print(json.dumps({
    "reward": round(reward, 4),
    "weighted_gates": {gid: latest.get(gid, False) for gid in weights},
    "fileTerminates": bool(probe["fileTerminates"]),
    "probe": probe["observed"],
}, separators=(",", ":")))
