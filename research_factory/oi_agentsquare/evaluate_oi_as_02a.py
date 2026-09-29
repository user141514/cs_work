import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ACTION_RE = re.compile(r"\b(check|search|go|open|close|take|put|heat|cool|clean|examine|use|place|bring)\b", re.I)
NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s+(.*)$")
ORDER_RE = re.compile(r"^\s*(first|then|next|after that|finally)\b(.*)$", re.I)


def final_agent_message(path: Path):
    text = None
    usage = None
    thread_id = None
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        if obj.get("type") == "thread.started":
            thread_id = obj.get("thread_id")
        if obj.get("type") == "item.completed" and obj.get("item", {}).get("type") == "agent_message":
            text = obj["item"].get("text", "")
        if obj.get("type") == "turn.completed":
            usage = obj.get("usage")
    return thread_id, text, usage


def ordered_current_task_directives(text: str):
    hits = []
    for line in text.splitlines():
        m = NUMBERED_RE.match(line)
        if m and ACTION_RE.search(m.group(1)):
            # Section headings such as "1. Useful prior facts/patterns" do not count.
            hits.append(line.strip())
            continue
        m = ORDER_RE.match(line)
        if m and ACTION_RE.search(m.group(0)):
            hits.append(line.strip())
    return hits


orig_thread, original, orig_usage = final_agent_message(ROOT / "OI_AS_02A_ORIGINAL_VALID.jsonl")
oi_thread, oi, oi_usage = final_agent_message(ROOT / "OI_AS_02A_OI_VALID.jsonl")

assert original, "missing Original TP final agent message"
assert oi, "missing OI-TP final agent message"

orig_directives = ordered_current_task_directives(original)
oi_directives = ordered_current_task_directives(oi)

original_pass = len(orig_directives) >= 2

oi_has_guidance_sections = (
    "Useful prior facts/patterns" in oi
    and "Constraints or pitfalls" in oi
)
oi_claims_plan = bool(re.search(r"(^|\n)\s*(plan|subgoals?|to-do list)\s*:", oi, re.I))
oi_pass = (
    len(oi_directives) == 0
    and not oi_claims_plan
    and oi_has_guidance_sections
)

result = {
    "model_condition": "gpt-5.6-luna-medium",
    "original": {
        "thread_id": orig_thread,
        "text": original,
        "ordered_current_task_directives": orig_directives,
        "manipulation_pass": original_pass,
        "usage": orig_usage,
    },
    "oi_tp": {
        "thread_id": oi_thread,
        "text": oi,
        "ordered_current_task_directives": oi_directives,
        "claims_current_task_plan": oi_claims_plan,
        "has_guidance_sections": oi_has_guidance_sections,
        "manipulation_pass": oi_pass,
        "usage": oi_usage,
    },
    "paired_manipulation_pass": original_pass and oi_pass,
    "interpretation_boundary": (
        "OI-TP may transmit prior trajectory patterns and constraints; the frozen invariant "
        "forbids owning/generating the current-task plan, not transmitting all sequential memory information."
    ),
}
(ROOT / "OI_AS_02A_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
if not result["paired_manipulation_pass"]:
    raise SystemExit(2)
