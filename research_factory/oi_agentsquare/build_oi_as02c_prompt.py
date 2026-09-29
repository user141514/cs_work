import hashlib, json, runpy
from pathlib import Path

ROOT=Path(__file__).resolve().parent
fixture=json.loads((ROOT/"OI_AS_02B_FIXTURE.json").read_text(encoding="utf-8"))
planning_ns=runpy.run_path(str(ROOT/"upstream/runtime/planning_prompt.py"))
few_shot=planning_ns["planning_prompt"]["heat"]
task_description=fixture["target_initial"]
prompt='''You are a planner who divides a {task_type} task into several subtasks. You also need to give the reasoning instructions for each subtask and the instructions for calling the tool. Your output format should follow the example below.
The following are some examples:
Task: {example}

Task: {task_description}
'''.format(example=few_shot,task_description=task_description,task_type="heat")

outdir=ROOT/"oi_as02c"
outdir.mkdir(exist_ok=True)
path=outdir/"planningio.prompt.txt"
path.write_text(prompt,encoding="utf-8")
manifest={
  "agent_square_commit":"8f5b3fe5d8a32f9b59d20370823bef2a2c86928c",
  "task_type":"heat",
  "task_description_sha256":hashlib.sha256(task_description.encode()).hexdigest(),
  "few_shot_sha256":hashlib.sha256(few_shot.encode()).hexdigest(),
  "prompt_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
  "prompt_bytes":path.stat().st_size,
  "model":"gpt-5.6-luna",
  "reasoning_effort":"medium",
  "feedback":"",
}
(outdir/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(manifest,indent=2,sort_keys=True))
print("TARGET_OCCURRENCES_IN_PROMPT",prompt.count("Your task is to: put a hot apple in fridge."))
