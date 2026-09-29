import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
bank=json.loads((ROOT/"upstream/runtime/prompts/alfworld_3prompts.json").read_text(encoding="utf-8"))
sel03=json.loads((ROOT/"OI_AS_03_FIXTURE_SELECTION.json").read_text(encoding="utf-8"))
eligible=[x["key"] for x in sel03["eligible_targets"]]
remaining=sorted(k for k in eligible if k!="react_clean_1")
STOP={"a","an","the","some","to","in","on"}

def task_text(v):
    m=re.search(r"Your task is to:\s*(.*?)\s*\n",v)
    if not m: raise ValueError("missing task")
    return m.group(1).strip().rstrip(".")

def toks(s):
    return {x for x in re.findall(r"[a-z0-9]+",s.lower()) if x not in STOP}

tasks={k:task_text(v) for k,v in bank.items()}
rows=[]
for tk in remaining:
    tt=toks(tasks[tk]); cand=[]
    for mk in sorted(tasks):
        if mk==tk: continue
        mt=toks(tasks[mk]); u=tt|mt
        score=len(tt&mt)/len(u) if u else 0.0
        cand.append((score,mk,sorted(tt&mt)))
    cand.sort(key=lambda x:(-x[0],x[1]))
    score,mk,shared=cand[0]
    rows.append({
        "target_key":tk,
        "target_task":tasks[tk],
        "target_type":tk.split("_")[1],
        "memory_key":mk,
        "memory_task":tasks[mk],
        "jaccard":score,
        "shared_tokens":shared,
    })
out={
    "selection_rule":"per-target max token-set Jaccard to any distinct frozen successful task; tie memory key lexicographic",
    "stopwords":sorted(STOP),
    "already_screened":["react_clean_1"],
    "execution_order":[r["target_key"] for r in rows],
    "pairs":rows,
}
(ROOT/"OI_AS_04_SCREEN_MANIFEST.json").write_text(json.dumps(out,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(out,indent=2,sort_keys=True))
