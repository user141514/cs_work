import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
fixture = json.loads((ROOT / "OI_AS_02B_FIXTURE.json").read_text(encoding="utf-8"))
prompts = ROOT / "oi_as02b_prompts"
prompts.mkdir(exist_ok=True)

memory_case = fixture["memory_success_case"]
target_initial = fixture["target_initial"]

original_memory_prompt = f"""You are performing the memory-transform step from AgentSquare MemoryTP.
Return only the requested structured JSON. The field memory_text must contain the answer to the following exact task.

You will be given a successful case where you successfully complete the task. Then you will be given an ongoing task. Do not summarize these two cases, but rather use the successful case to think about the strategy and path you took to attempt to complete the task in the ongoing task. Devise a concise, new plan of action that accounts for your task with reference to specific actions that you should have taken. You will need this later to solve the task. Give your plan after "Plan".
Success Case:
{memory_case}
Ongoing task:
{target_initial}
Plan:
"""

oi_memory_prompt = f"""You are performing the orthogonalized memory-transform step for an AgentSquare memory module.
Return only the requested structured JSON. The field memory_text must contain the answer to the following exact task.

You will be given a successful case where an agent completed a task, followed by an ongoing task.
Extract transferable memory-derived guidance that may help the reasoning module, but DO NOT produce a plan, ordered steps, subgoals, or concrete next actions for the ongoing task.
Return at most five concise constraints, checks, or heuristics. These are non-authoritative hints only; the planning module remains solely responsible for the current-task plan.
Success Case:
{memory_case}
Ongoing task:
{target_initial}
Guidance:
"""

(prompts / "memory_original.txt").write_text(original_memory_prompt, encoding="utf-8")
(prompts / "memory_oi.txt").write_text(oi_memory_prompt, encoding="utf-8")

memory_schema = {
    "type": "object",
    "properties": {"memory_text": {"type": "string"}},
    "required": ["memory_text"],
    "additionalProperties": False,
}
(prompts / "memory_schema.json").write_text(json.dumps(memory_schema, indent=2), encoding="utf-8")

manifest = {
    "memory_original_sha256": hashlib.sha256(original_memory_prompt.encode()).hexdigest(),
    "memory_oi_sha256": hashlib.sha256(oi_memory_prompt.encode()).hexdigest(),
    "memory_schema_sha256": hashlib.sha256((prompts / "memory_schema.json").read_bytes()).hexdigest(),
}
(prompts / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps(manifest, indent=2, sort_keys=True))
