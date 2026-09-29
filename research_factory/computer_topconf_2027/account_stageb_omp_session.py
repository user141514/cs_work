from __future__ import annotations

import argparse
import json
from pathlib import Path


def latest_jsonl(session_dir: Path) -> Path:
    files = list(session_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit(f"no jsonl in {session_dir}")
    return max(files, key=lambda p: p.stat().st_mtime)


def numeric_ts(row):
    msg = row.get("message") or {}
    for v in (msg.get("timestamp"), row.get("timestamp")):
        if isinstance(v, (int, float)):
            return float(v)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session-dir", required=True)
    args = ap.parse_args()

    session = latest_jsonl(Path(args.session_dir))
    rows = []
    for line in session.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    usage = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "reasoningTokens": 0}
    model_calls = 0
    tool_calls = 0
    tool_counts = {}
    mutating_tool_calls = 0
    cost = 0.0
    first_ts = None
    last_ts = None

    for row in rows:
        ts = numeric_ts(row)
        if ts is not None:
            if first_ts is None:
                first_ts = ts
            last_ts = ts

        if row.get("type") != "message":
            continue
        msg = row.get("message") or {}
        if msg.get("role") != "assistant":
            continue

        u = msg.get("usage")
        if isinstance(u, dict):
            model_calls += 1
            for key in usage:
                usage[key] += int(u.get(key) or 0)
            c = u.get("cost")
            if isinstance(c, dict):
                cost += float(c.get("total") or 0.0)

        for item in msg.get("content") or []:
            if not isinstance(item, dict) or item.get("type") != "toolCall":
                continue
            name = item.get("name") or "unknown"
            tool_calls += 1
            tool_counts[name] = tool_counts.get(name, 0) + 1
            if name in {"edit", "write"}:
                mutating_tool_calls += 1

    wall = None
    if first_ts is not None and last_ts is not None:
        delta = last_ts - first_ts
        wall = delta / 1000.0 if delta > 10000 else delta

    out = {
        "session": str(session),
        "model_calls": model_calls,
        "tool_calls": tool_calls,
        "tool_counts": tool_counts,
        "mutating_tool_calls": mutating_tool_calls,
        "usage": usage,
        "noncached_input_output": usage["input"] + usage["output"],
        "reported_cost_usd": cost,
        "wall_seconds_from_numeric_timestamps": wall,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
