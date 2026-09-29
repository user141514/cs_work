from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def rebase_text(text: str, old_root: str, new_root: str) -> tuple[str, int]:
    pairs = [
        (old_root.replace("\\", "/"), new_root.replace("\\", "/")),
        (old_root.replace("/", "\\"), new_root.replace("/", "\\")),
        (old_root.replace("/", "\\").replace("\\", "\\\\"), new_root.replace("/", "\\").replace("\\", "\\\\")),
    ]
    total = 0
    for old, new in pairs:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            total += n
    return text, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("old_root")
    ap.add_argument("new_root")
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    total = 0
    touched = []
    for path in dst.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".jsonl", ".log", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text, n = rebase_text(text, args.old_root, args.new_root)
        if n:
            path.write_text(new_text, encoding="utf-8")
            total += n
            touched.append(str(path.relative_to(dst)))

    print(f"replacements={total}")
    for p in touched:
        print(p)


if __name__ == "__main__":
    main()
