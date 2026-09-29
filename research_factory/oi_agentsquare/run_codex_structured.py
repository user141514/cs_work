import argparse
import json
import subprocess
import time
from pathlib import Path

CODEX = r"C:/Users/Administrator/.codex/tools/bin/codex.cmd"

def kill_tree(pid):
    subprocess.run(["taskkill","/PID",str(pid),"/T","/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_one(prompt_path, schema_path, jsonl_path, model="gpt-5.6-luna", effort="medium", timeout=240):
    prompt = Path(prompt_path).read_text(encoding="utf-8")
    jsonl = Path(jsonl_path)
    jsonl.parent.mkdir(parents=True, exist_ok=True)
    cmd=[CODEX,"exec","--ephemeral","--sandbox","read-only","--skip-git-repo-check","-C",r"D:/cs_work",
         "-m",model,"-c",f'model_reasoning_effort="{effort}"',"--json","--output-schema",str(Path(schema_path).resolve()),"-"]
    start=time.time()
    with jsonl.open("w",encoding="utf-8") as out:
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="ignore")
        p.stdin.write(prompt)
        p.stdin.close()
        deadline=start+timeout
        complete=False
        while time.time()<deadline:
            if jsonl.exists():
                text=jsonl.read_text(encoding="utf-8",errors="ignore")
                if '"type":"turn.completed"' in text:
                    complete=True
                    break
            if p.poll() is not None:
                break
            time.sleep(1)
        if p.poll() is None:
            kill_tree(p.pid)
        else:
            try: p.wait(timeout=5)
            except Exception: pass
    elapsed=time.time()-start
    agent_text=None; usage=None; thread_id=None
    for raw in jsonl.read_text(encoding="utf-8",errors="ignore").splitlines():
        try: obj=json.loads(raw)
        except Exception: continue
        if obj.get("type")=="thread.started": thread_id=obj.get("thread_id")
        if obj.get("type")=="item.completed" and obj.get("item",{}).get("type")=="agent_message":
            agent_text=obj["item"].get("text")
        if obj.get("type")=="turn.completed": usage=obj.get("usage")
    parsed=None
    if agent_text:
        try: parsed=json.loads(agent_text)
        except Exception: pass
    return {
        "complete": bool(complete and usage is not None and parsed is not None),
        "thread_id": thread_id,
        "agent_text": agent_text,
        "parsed": parsed,
        "usage": usage,
        "elapsed_seconds": elapsed,
        "jsonl": str(jsonl),
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--prompt",required=True)
    ap.add_argument("--schema",required=True)
    ap.add_argument("--jsonl",required=True)
    ap.add_argument("--result",required=True)
    ap.add_argument("--timeout",type=int,default=240)
    args=ap.parse_args()
    res=run_one(args.prompt,args.schema,args.jsonl,timeout=args.timeout)
    Path(args.result).write_text(json.dumps(res,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(res,indent=2,sort_keys=True))
    raise SystemExit(0 if res["complete"] else 2)
