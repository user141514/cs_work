import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
P=ROOT/"oi_as02b_prompts"
RUNS=ROOT/"oi_as02b_runs"
fixture=json.loads((ROOT/"OI_AS_02B_FIXTURE.json").read_text(encoding="utf-8"))
orig_mem=json.loads((RUNS/"memory/original.result.json").read_text(encoding="utf-8"))["parsed"]["memory_text"]
oi_mem=json.loads((RUNS/"memory/oi.result.json").read_text(encoding="utf-8"))["parsed"]["memory_text"]

cp=next(x for x in fixture["checkpoints"] if x["id"]=="C4")
template=(P/"action_C4_template.txt").read_text(encoding="utf-8")
assert "{{MEMORY_TEXT}}" in template

outdir=RUNS/"C4"
outdir.mkdir(parents=True,exist_ok=True)
arms={}
for arm,mem in [("original",orig_mem),("oi",oi_mem)]:
    text=template.replace("{{MEMORY_TEXT}}",mem)
    path=outdir/f"{arm}.prompt.txt"
    path.write_text(text,encoding="utf-8")
    arms[arm]={"prompt_file":path.as_posix(),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size}
manifest={"checkpoint":"C4","gold_action":cp["gold_action"],"template_sha256":hashlib.sha256((P/"action_C4_template.txt").read_bytes()).hexdigest(),"action_schema_sha256":hashlib.sha256((P/"action_schema.json").read_bytes()).hexdigest(),"model":"gpt-5.6-luna","reasoning_effort":"medium","arms":arms}
(outdir/"MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(manifest,indent=2,sort_keys=True))
