import hashlib,json
from pathlib import Path
root=Path("research_factory/oi_agentsquare/upstream/search")
files=["agent_search.py","recombination.py","module_predictor.py","planning_modules.json","reasoning_modules.json","tooluse_modules.json","memory_modules.json"]
out={
  "repo":"tsinghua-fib-lab/AgentSquare",
  "commit":"8f5b3fe5d8a32f9b59d20370823bef2a2c86928c",
  "files":{}
}
for name in files:
    p=root/name
    out["files"][name]={"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
Path("research_factory/oi_agentsquare/UPSTREAM_MANIFEST.json").write_text(json.dumps(out,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(out,indent=2,sort_keys=True))
