import hashlib,json,runpy
from pathlib import Path

ROOT=Path(__file__).resolve().parent
bank=json.loads((ROOT/"upstream/runtime/prompts/alfworld_3prompts.json").read_text(encoding="utf-8"))
screen=json.loads((ROOT/"OI_AS_04_SCREEN_MANIFEST.json").read_text(encoding="utf-8"))
pair=next(x for x in screen["pairs"] if x["target_key"]=="react_examine_1")
assert pair["memory_key"]=="react_examine_0"

target_traj=bank[pair["target_key"]]
memory_traj=bank[pair["memory_key"]]
lines=target_traj.splitlines()
first_action=next(i for i,line in enumerate(lines) if line.startswith("> "))
target_initial="\n".join(lines[:first_action]).strip()

planning_ns=runpy.run_path(str(ROOT/"upstream/runtime/planning_prompt.py"))
few_shot=planning_ns["planning_prompt"]["examine"]
planning_prompt='''You are a planner who divides a {task_type} task into several subtasks. You also need to give the reasoning instructions for each subtask and the instructions for calling the tool. Your output format should follow the example below.
The following are some examples:
Task: {example}

Task: {task_description}
'''.format(example=few_shot,task_description=target_initial,task_type="examine")

memory_prompt=f"""You are performing the memory-transform step from AgentSquare MemoryTP.
Return only the requested structured JSON. The field memory_text must contain the answer to the following exact task.

You will be given a successful case where you successfully complete the task. Then you will be given an ongoing task. Do not summarize these two cases, but rather use the successful case to think about the strategy and path you took to attempt to complete the task in the ongoing task. Devise a concise, new plan of action that accounts for your task with reference to specific actions that you should have taken. You will need this later to solve the task. Give your plan after "Plan".
Success Case:
{memory_traj}
Ongoing task:
{target_initial}
Plan:
"""

schema={"type":"object","properties":{"memory_text":{"type":"string"}},"required":["memory_text"],"additionalProperties":False}
out=ROOT/"oi_as04"/"react_examine_1"
out.mkdir(parents=True,exist_ok=True)
(out/"planningio.prompt.txt").write_text(planning_prompt,encoding="utf-8")
(out/"original_tp_memory.prompt.txt").write_text(memory_prompt,encoding="utf-8")
(out/"memory_schema.json").write_text(json.dumps(schema,indent=2),encoding="utf-8")
fixture={
  "target_key":pair["target_key"],"target_task":pair["target_task"],"target_type":"examine",
  "memory_key":pair["memory_key"],"memory_task":pair["memory_task"],
  "target_initial":target_initial,"memory_success_case":memory_traj,
  "required_signature":["ACQUIRE(pen)","FIND_USE(desklamp)"],
}
(out/"FIXTURE.json").write_text(json.dumps(fixture,indent=2,sort_keys=True),encoding="utf-8")
manifest={
  "model":"gpt-5.6-luna","reasoning_effort":"medium",
  "target_key":pair["target_key"],"memory_key":pair["memory_key"],
  "planning_prompt_sha256":hashlib.sha256((out/"planningio.prompt.txt").read_bytes()).hexdigest(),
  "memory_prompt_sha256":hashlib.sha256((out/"original_tp_memory.prompt.txt").read_bytes()).hexdigest(),
  "memory_schema_sha256":hashlib.sha256((out/"memory_schema.json").read_bytes()).hexdigest(),
  "same_target_occurrences_in_planning_prompt":planning_prompt.count("Your task is to: examine the pen with the desklamp."),
}
(out/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(manifest,indent=2,sort_keys=True))
