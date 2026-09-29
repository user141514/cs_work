import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RUNS=ROOT/"oi_as02b_runs"

rows=[]
for i in range(1,6):
    cp=f"C{i}"
    x=json.loads((RUNS/cp/f"{cp}_RESULT.json").read_text(encoding="utf-8"))
    rows.append(x)

orig_correct=sum(int(x["arms"]["original"]["correct"]) for x in rows)
oi_correct=sum(int(x["arms"]["oi"]["correct"]) for x in rows)
discordant=sum(int(x["arms"]["original"]["correct"] != x["arms"]["oi"]["correct"]) for x in rows)
paired_sum=sum(x["paired_difference"] for x in rows)

action_usage={
    "original":{"input_tokens":0,"output_tokens":0,"reasoning_output_tokens":0,"elapsed_seconds":0.0},
    "oi":{"input_tokens":0,"output_tokens":0,"reasoning_output_tokens":0,"elapsed_seconds":0.0},
}
for x in rows:
    for arm in ["original","oi"]:
        u=x["arms"][arm]["usage"]
        action_usage[arm]["input_tokens"]+=u["input_tokens"]
        action_usage[arm]["output_tokens"]+=u["output_tokens"]
        action_usage[arm]["reasoning_output_tokens"]+=u["reasoning_output_tokens"]
        action_usage[arm]["elapsed_seconds"]+=x["arms"][arm]["elapsed_seconds"]

memory={}
for arm in ["original","oi"]:
    r=json.loads((RUNS/"memory"/f"{arm}.result.json").read_text(encoding="utf-8"))
    memory[arm]={
        "input_tokens":r["usage"]["input_tokens"],
        "output_tokens":r["usage"]["output_tokens"],
        "reasoning_output_tokens":r["usage"]["reasoning_output_tokens"],
        "elapsed_seconds":r["elapsed_seconds"],
    }

verdict="NULL_ON_PILOT" if oi_correct==orig_correct else ("SUPPORTIVE_DIRECTION" if oi_correct>orig_correct else "CONTRADICTORY")

result={
    "pilot":"OI-AS-02B",
    "model_condition":"gpt-5.6-luna-medium",
    "checkpoint_results":[
        {
            "checkpoint":x["checkpoint"],
            "gold_action":x["gold_action"],
            "original_action":x["arms"]["original"]["action"],
            "oi_action":x["arms"]["oi"]["action"],
            "original_correct":x["arms"]["original"]["correct"],
            "oi_correct":x["arms"]["oi"]["correct"],
            "paired_difference":x["paired_difference"],
            "verdict":x["checkpoint_verdict"],
        } for x in rows
    ],
    "original_correct":orig_correct,
    "oi_correct":oi_correct,
    "n_checkpoints":5,
    "discordant_pairs":discordant,
    "paired_difference_sum":paired_sum,
    "verdict":verdict,
    "action_usage":action_usage,
    "memory_transform_usage":memory,
    "claim_boundary":{
        "supported":"On this frozen same-task heat-task trajectory, orthogonalizing TP memory authority changed the memory representation but produced no next-action differences at any of five checkpoints.",
        "not_supported":[
            "No claim that O+I is globally ineffective.",
            "No full-episode ALFWorld result.",
            "No search-efficiency result.",
            "No conclusion about cases where memory-derived and planner-derived plans conflict."
        ]
    }
}
(ROOT/"OI_AS_02B_RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
