import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
base=ROOT/"upstream"/"runtime"
files={}
for p in sorted(base.rglob("*")):
    if p.is_file():
        rel=p.relative_to(base).as_posix()
        files[rel]={"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
out={
  "repo":"tsinghua-fib-lab/AgentSquare",
  "commit":"8f5b3fe5d8a32f9b59d20370823bef2a2c86928c",
  "root":"search/alfworld",
  "files":files
}
(ROOT/"OI_AS_02_UPSTREAM_RUNTIME_MANIFEST.json").write_text(json.dumps(out,indent=2,sort_keys=True),encoding="utf-8")
print("FILES",len(files),"BYTES",sum(v["bytes"] for v in files.values()))
