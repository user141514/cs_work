#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <repo-path> <log-dir>" >&2
  exit 2
fi

repo="$1"
logdir="$2"
official="D:/bio_paper/external/swe_together_official_20260928/tasks/dataclaw-anonymizer-tests/tests/test.sh"
python_exe="D:/bio_paper/external/spec_stageb_s1_venv/Scripts/python.exe"

mkdir -p "$logdir"
tmp="$logdir/adapted_test.sh"

# Preserve the published verifier logic. Adapt only container-local paths and
# the Python executable to the frozen local-equivalent runtime.
sed \
  -e "s|/workspace/repo|$repo|g" \
  -e "s|/logs/verifier|$logdir|g" \
  -e "s|python3|\"$python_exe\"|g" \
  "$official" > "$tmp"

bash "$tmp"

echo "---LOCAL_EQUIVALENT_REWARD---"
cat "$logdir/reward.txt"
