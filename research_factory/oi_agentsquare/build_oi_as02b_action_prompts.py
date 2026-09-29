import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
fixture=json.loads((ROOT/"OI_AS_02B_FIXTURE.json").read_text(encoding="utf-8"))
prompts=ROOT/"oi_as02b_prompts"
prompts.mkdir(exist_ok=True)

action_schema={
  "type":"object",
  "properties":{"action":{"type":"string"}},
  "required":["action"],
  "additionalProperties":False,
}
(prompts/"action_schema.json").write_text(json.dumps(action_schema,indent=2),encoding="utf-8")

manifest=json.loads((prompts/"MANIFEST.json").read_text(encoding="utf-8"))
manifest["action_schema_sha256"]=hashlib.sha256((prompts/"action_schema.json").read_bytes()).hexdigest()
manifest["checkpoints"]={}

for cp in fixture["checkpoints"]:
    template=(
        "Interact with a household to solve a task. Your instructions must follow the examples.\n"
        "Here are some examples.\n"
        "{{MEMORY_TEXT}}\n"
        "Here is the task:\n"
        + cp["prefix"]
        + "\n\nReturn only JSON matching the provided schema, with exactly one ALFWorld action in the action field."
    )
    path=prompts/f"action_{cp['id']}_template.txt"
    path.write_text(template,encoding="utf-8")
    manifest["checkpoints"][cp["id"]]={
        "gold_action":cp["gold_action"],
        "template_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
    }

(prompts/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(manifest,indent=2,sort_keys=True))
