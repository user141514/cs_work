import argparse,json,subprocess,time
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
cmd=[
    CODEX,"exec","--ignore-user-config","--ignore-rules",
    "--disable","hooks","--disable","skill_search","--disable","plugins","--disable","apps",
    "--disable","browser_use","--disable","computer_use","--disable","multi_agent",
    "--disable","shell_tool","--disable","unified_exec","--disable","workspace_dependencies",
    "--ephemeral","--sandbox","read-only","--skip-git-repo-check","-C",r"D:/cs_work",
    "-m","gpt-5.6-luna","-c",'model_reasoning_effort="medium"',"--json","-"
]
start=time.time()
with jsonl.open("w",encoding="utf-8") as out:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=subprocess.STDOUT,text=True,encoding="utf-8",errors="ignore")
    p.stdin.write(prompt); p.stdin.close()
    deadline=start+args.timeout
    complete=False
    while time.time()<deadline:
        if jsonl.exists() and '"type":"turn.completed"' in jsonl.read_text(encoding="utf-8",errors="ignore"):
            complete=True; break
        if p.poll() is not None: break
        time.sleep(1)
    if p.poll() is None: kill_tree(p.pid)

agent_text=None; usage=None; thread_id=None; tool_events=[]
for raw in jsonl.read_text(encoding="utf-8",errors="ignore").splitlines():
    try: obj=json.loads(raw)
    except Exception: continue
    if obj.get("type")=="thread.started": thread_id=obj.get("thread_id")
    if obj.get("type")=="item.completed" and obj.get("item",{}).get("type")=="agent_message":
        agent_text=obj["item"].get("text")
    item=obj.get("item",{}) if isinstance(obj,dict) else {}
    if item.get("type") in {"command_execution","mcp_tool_call","tool_call"}:
        tool_events.append(item.get("type"))
    if obj.get("type")=="turn.completed": usage=obj.get("usage")

res={
    "complete":bool(complete and agent_text and usage),
    "valid_no_tool_execution":len(tool_events)==0,
    "tool_events":tool_events,
    "thread_id":thread_id,
    "agent_text":agent_text,
    "usage":usage,
    "elapsed_seconds":time.time()-start,
    "jsonl":str(jsonl),
}
Path(args.result).write_text(json.dumps(res,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(res,indent=2,sort_keys=True))
raise SystemExit(0 if res["complete"] and res["valid_no_tool_execution"] else 2)
