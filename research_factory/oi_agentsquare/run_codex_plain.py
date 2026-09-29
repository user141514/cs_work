import argparse, json, subprocess, time
from pathlib import Path

CODEX=r"C:/Users/Administrator/.codex/tools/bin/codex.cmd"

def kill_tree(pid):
    subprocess.run(["taskkill","/PID",str(pid),"/T","/F"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

ap=argparse.ArgumentParser()
ap.add_argument("--prompt",required=True)
ap.add_argument("--jsonl",required=True)
ap.add_argument("--result",required=True)
ap.add_argument("--timeout",type=int,default=240)
args=ap.parse_args()

prompt=Path(args.prompt).read_text(encoding="utf-8")
jsonl=Path(args.jsonl); jsonl.parent.mkdir(parents=True,exist_ok=True)
cmd=[CODEX,"exec","--ephemeral","--sandbox","read-only","--skip-git-repo-check","-C",r"D:/cs_work",
     "-m","gpt-5.6-luna","-c",'model_reasoning_effort="medium"',"--json","-"]
start=time.time()
with jsonl.open("w",encoding="utf-8") as out:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="ignore")
    p.stdin.write(prompt); p.stdin.close()
    deadline=start+args.timeout
    complete=False
    while time.time()<deadline:
        if jsonl.exists():
            t=jsonl.read_text(encoding="utf-8",errors="ignore")
            if '"type":"turn.completed"' in t:
                complete=True; break
        if p.poll() is not None: break
        time.sleep(1)
    if p.poll() is None: kill_tree(p.pid)

agent_text=None; usage=None; thread_id=None
for raw in jsonl.read_text(encoding="utf-8",errors="ignore").splitlines():
    try: obj=json.loads(raw)
    except Exception: continue
    if obj.get("type")=="thread.started": thread_id=obj.get("thread_id")
    if obj.get("type")=="item.completed" and obj.get("item",{}).get("type")=="agent_message":
        agent_text=obj["item"].get("text")
    if obj.get("type")=="turn.completed": usage=obj.get("usage")
res={
  "complete":bool(complete and agent_text and usage),
  "thread_id":thread_id,
  "agent_text":agent_text,
  "usage":usage,
  "elapsed_seconds":time.time()-start,
  "jsonl":str(jsonl)
}
Path(args.result).write_text(json.dumps(res,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(res,indent=2,sort_keys=True))
raise SystemExit(0 if res["complete"] else 2)
