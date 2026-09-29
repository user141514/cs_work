from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def latest_jsonl(session_dir: Path) -> Path:
    files = list(session_dir.glob("*.jsonl"))
    if not files:
        raise SystemExit(f"no jsonl in {session_dir}")
    return max(files, key=lambda p: p.stat().st_mtime)


def ts_value(v):
    if isinstance(v, (int, float)):
        return float(v)
    return None


def parse_added_segments(patch_text: str):
    segs = []
    cur = []
    for line in patch_text.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            cur.append(line[1:])
        else:
            if cur:
                segs.append(cur)
                cur = []
    if cur:
        segs.append(cur)
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True)
    ap.add_argument("--session-dir", required=True)
    ap.add_argument("--marker", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--pre-patch", required=True)
    ap.add_argument("--reuse-mode", choices=["inherited", "restart"], required=True)
    args = ap.parse_args()

    session = latest_jsonl(Path(args.session_dir))
    rows = []
    for line in session.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    start_i = None
    start_ts = None
    for i, row in enumerate(rows):
        if row.get("type") != "message":
            continue
        msg = row.get("message") or {}
        if msg.get("role") != "user":
            continue
        text = ""
        for c in msg.get("content") or []:
            if isinstance(c, dict) and c.get("type") == "text":
                text += c.get("text", "")
        if args.marker in text:
            start_i = i
            start_ts = ts_value(msg.get("timestamp")) or ts_value(row.get("timestamp"))
    if start_i is None:
        raise SystemExit(f"marker not found: {args.marker}")

    usage = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "reasoningTokens": 0}
    cost = 0.0
    model_calls = 0
    tool_calls = 0
    tool_counts = {}
    mutating_calls = 0
    last_numeric_ts = start_ts

    for row in rows[start_i + 1:]:
        if row.get("type") != "message":
            continue
        msg = row.get("message") or {}
        tsv = ts_value(msg.get("timestamp")) or ts_value(row.get("timestamp"))
        if tsv is not None:
            last_numeric_ts = tsv
        if msg.get("role") != "assistant":
            continue
        u = msg.get("usage")
        if isinstance(u, dict):
            model_calls += 1
            for k in usage:
                usage[k] += int(u.get(k) or 0)
            c = u.get("cost")
            if isinstance(c, dict):
                cost += float(c.get("total") or 0)
        for c in msg.get("content") or []:
            if not isinstance(c, dict) or c.get("type") != "toolCall":
                continue
            name = c.get("name") or "unknown"
            tool_calls += 1
            tool_counts[name] = tool_counts.get(name, 0) + 1
            if name in {"edit", "write"}:
                mutating_calls += 1

    repo = Path(args.repo)
    numstat = subprocess.run(
        ["git", "-C", str(repo), "diff", "--numstat", "windows"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    final_test = (repo / "tests" / "test_anonymizer.py").read_text(encoding="utf-8")
    patch_text = Path(args.pre_patch).read_text(encoding="utf-8")
    segs = parse_added_segments(patch_text)
    total_lines = sum(len(s) for s in segs)
    preserved_lines = 0
    preserved_segments = 0
    for seg in segs:
        needle = "\n".join(seg)
        if needle in final_test:
            preserved_segments += 1
            preserved_lines += len(seg)

    if args.reuse_mode == "restart":
        credited_line_fraction = 0.0
        credited_segment_fraction = 0.0
    else:
        credited_line_fraction = preserved_lines / total_lines if total_lines else 0.0
        credited_segment_fraction = preserved_segments / len(segs) if segs else 0.0

    out = {
        "arm": args.arm,
        "session": str(session),
        "post_revision": {
            "model_calls": model_calls,
            "tool_calls": tool_calls,
            "tool_counts": tool_counts,
            "mutating_tool_calls": mutating_calls,
            "usage": usage,
            "reported_cost_usd": cost,
            "wall_seconds_from_numeric_timestamps": (
                ((last_numeric_ts - start_ts) / 1000.0 if (last_numeric_ts - start_ts) > 10000 else (last_numeric_ts - start_ts))
                if start_ts is not None and last_numeric_ts is not None
                else None
            ),
        },
        "final_diff_numstat_vs_windows": numstat.splitlines() if numstat else [],
        "pre_revision_reuse": {
            "mode": args.reuse_mode,
            "added_segments_total": len(segs),
            "added_segments_byte_identical_in_final": preserved_segments,
            "added_lines_total": total_lines,
            "added_lines_in_preserved_segments": preserved_lines,
            "credited_segment_fraction": credited_segment_fraction,
            "credited_line_fraction": credited_line_fraction,
        },
    }
    print(json.dumps(out, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
