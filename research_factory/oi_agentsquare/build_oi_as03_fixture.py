import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
prompts=json.loads((ROOT/"upstream/runtime/prompts/alfworld_3prompts.json").read_text(encoding="utf-8"))
planning_text=(ROOT/"upstream/runtime/planning_prompt.py").read_text(encoding="utf-8")

STOP={"a","an","the","some","to","in","on"}

def task_text(v):
    m=re.search(r"Your task is to:\s*(.*?)\s*\n",v)
    if not m:
        raise ValueError("task missing")
    return m.group(1).strip().rstrip(".")

def task_type_from_key(k):
    return k.split("_")[1]

def tokens(s):
    return {x for x in re.findall(r"[a-z0-9]+",s.lower()) if x not in STOP}

# Extract few-shot task texts by task type from planning_prompt source with a simple
# source-grounded scan around each dictionary entry.
types=["put","clean","heat","cool","examine","puttwo"]
fewshot={}
for t in types:
    # Find the exact string literal block for this key by locating the next key.
    marker=f'"{t}":'
    start=planning_text.index(marker)
    ends=[planning_text.find(f'"{u}":',start+len(marker)) for u in types if planning_text.find(f'"{u}":',start+len(marker))!=-1]
    end=min(ends) if ends else len(planning_text)
    block=planning_text[start:end]
    fewshot[t]={m.strip().rstrip(".") for m in re.findall(r"Your task is to:\s*(.*?)\s*(?:\\r?\\n|\n)",block)}

tasks={k:task_text(v) for k,v in prompts.items()}
eligible=[]
for k,t in tasks.items():
    typ=task_type_from_key(k)
    if t not in fewshot.get(typ,set()):
        eligible.append(k)

pairs=[]
for tk in eligible:
    tt=tokens(tasks[tk])
    for mk in sorted(tasks):
        if mk==tk: continue
        mt=tokens(tasks[mk])
        u=tt|mt
        score=len(tt&mt)/len(u) if u else 0.0
        pairs.append((score,tk,mk,sorted(tt&mt),tasks[tk],tasks[mk]))

pairs.sort(key=lambda x:(-x[0],x[1],x[2]))
best=pairs[0]
result={
    "selection_rule":"max token-set Jaccard over eligible target vs any distinct frozen successful task; ties lexicographic",
    "stopwords":sorted(STOP),
    "eligible_targets":[{"key":k,"task":tasks[k],"type":task_type_from_key(k)} for k in sorted(eligible)],
    "selected":{
        "target_key":best[1],
        "target_task":best[4],
        "target_type":task_type_from_key(best[1]),
        "memory_key":best[2],
        "memory_task":best[5],
        "jaccard":best[0],
        "shared_tokens":best[3],
    },
    "top_pairs":[
        {"score":p[0],"target_key":p[1],"memory_key":p[2],"target_task":p[4],"memory_task":p[5]}
        for p in pairs[:10]
    ]
}
(ROOT/"OI_AS_03_FIXTURE_SELECTION.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
