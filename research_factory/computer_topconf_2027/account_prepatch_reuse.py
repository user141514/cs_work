from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def parse_added_segments_by_file(patch_text: str):
    result = {}
    current_file = None
    current_segment = []

    def flush():
        nonlocal current_segment
        if current_file and current_segment:
            result.setdefault(current_file, []).append(current_segment)
        current_segment = []

    for line in patch_text.splitlines():
        if line.startswith("diff --git "):
            flush()
            current_file = None
        elif line.startswith("+++ b/"):
            flush()
            current_file = line[len("+++ b/"):]
        elif line.startswith("@@"):
            flush()
        elif line.startswith("+") and not line.startswith("+++"):
            current_segment.append(line[1:])
        else:
            flush()
    flush()
    return result


def unreleased_lines(text: str):
    lines = []
    active = False
    for line in text.splitlines():
        if line.startswith("## [Unreleased]"):
            active = True
            continue
        if active and line.startswith("## ["):
            break
        if active:
            lines.append(line)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pre-patch", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--reuse-mode", choices=["inherited", "restart"], required=True)
    args = ap.parse_args()

    patch_text = Path(args.pre_patch).read_text(encoding="utf-8")
    segments_by_file = parse_added_segments_by_file(patch_text)
    repo = Path(args.repo)

    total_segments = 0
    preserved_segments = 0
    total_lines = 0
    preserved_lines = 0
    meaningful_lines_total = 0
    meaningful_lines_preserved = 0
    files = {}

    for rel, segments in segments_by_file.items():
        final_path = repo / rel
        final_text = final_path.read_text(encoding="utf-8") if final_path.exists() else ""
        f_total_segments = len(segments)
        f_preserved_segments = 0
        f_total_lines = sum(len(seg) for seg in segments)
        f_preserved_lines = 0

        pre_meaningful = [line for seg in segments for line in seg if line.strip()]
        final_unreleased = Counter(unreleased_lines(final_text))
        f_meaningful_preserved = 0
        for line in pre_meaningful:
            if final_unreleased[line] > 0:
                f_meaningful_preserved += 1
                final_unreleased[line] -= 1

        for seg in segments:
            needle = "\n".join(seg)
            if needle in final_text:
                f_preserved_segments += 1
                f_preserved_lines += len(seg)

        total_segments += f_total_segments
        preserved_segments += f_preserved_segments
        total_lines += f_total_lines
        preserved_lines += f_preserved_lines
        meaningful_lines_total += len(pre_meaningful)
        meaningful_lines_preserved += f_meaningful_preserved
        files[rel] = {
            "segments_total": f_total_segments,
            "segments_preserved": f_preserved_segments,
            "added_lines_total": f_total_lines,
            "added_lines_preserved_in_exact_segments": f_preserved_lines,
            "meaningful_added_lines_total": len(pre_meaningful),
            "meaningful_added_lines_byte_identical_in_final_unreleased": f_meaningful_preserved,
        }

    raw_line_fraction = preserved_lines / total_lines if total_lines else 0.0
    raw_segment_fraction = preserved_segments / total_segments if total_segments else 0.0
    raw_meaningful_line_fraction = (
        meaningful_lines_preserved / meaningful_lines_total if meaningful_lines_total else 0.0
    )

    credited_line_fraction = raw_line_fraction if args.reuse_mode == "inherited" else 0.0
    credited_segment_fraction = raw_segment_fraction if args.reuse_mode == "inherited" else 0.0
    credited_meaningful_line_fraction = (
        raw_meaningful_line_fraction if args.reuse_mode == "inherited" else 0.0
    )

    out = {
        "reuse_mode": args.reuse_mode,
        "files": files,
        "segments_total": total_segments,
        "segments_byte_identical_in_final": preserved_segments,
        "added_lines_total": total_lines,
        "added_lines_byte_identical_in_final": preserved_lines,
        "raw_segment_fraction": raw_segment_fraction,
        "raw_line_fraction": raw_line_fraction,
        "meaningful_added_lines_total": meaningful_lines_total,
        "meaningful_added_lines_byte_identical_in_final_unreleased": meaningful_lines_preserved,
        "raw_meaningful_line_fraction": raw_meaningful_line_fraction,
        "credited_segment_fraction": credited_segment_fraction,
        "credited_line_fraction": credited_line_fraction,
        "credited_meaningful_line_fraction": credited_meaningful_line_fraction,
        "note": "Primary conservative reuse metric is byte-identical nonblank pre-revision added lines retained inside the same file's final [Unreleased] section. Exact contiguous-segment survival is also reported as a stricter auxiliary metric. Pre-revision deletions are not credited.",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
