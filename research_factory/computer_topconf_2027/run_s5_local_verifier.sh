#!/usr/bin/env bash
set -euo pipefail

repo="$1"
logdir="$2"
official="D:/bio_paper/external/swe_together_official_20260928/tasks/pi-mono-auto-ec7037ba/tests/test.sh"
probe="D:/bio_paper/research_factory/computer_topconf_2027/s5_autocomplete_evaluator_probe.mjs"
postprocess="D:/bio_paper/research_factory/computer_topconf_2027/s5_verifier_postprocess.py"
support_repo="D:/bio_paper/external/spec_stageb_s5_base_69d02"

mkdir -p "$logdir"
repo=$(cd "$repo" && pwd)
logdir=$(cd "$logdir" && pwd)
tmp="$logdir/adapted_test.sh"

sed \
  -e "s|/workspace/pi-mono|$repo|g" \
  -e "s|/workspace/repo|$repo|g" \
  -e "s|/logs/verifier|$logdir|g" \
  -e "s|/baseline/changelog_snap|$logdir/baseline_changelog_snap|g" \
  "$official" > "$tmp"

# The public v043 verifier contains one base64-encoded environment prelude.
# Literal substitutions above cannot rewrite the embedded /workspace/pi-mono.
# Re-encode only that diagnostic prelude for the local-equivalent repo; scoring
# gates and weights remain unchanged.
official_prelude_b64="c2V0ICtlOyBjZCAvd29ya3NwYWNlL3BpLW1vbm8gJiYgY29tbWFuZCAtdiBucHggPi9kZXYvbnVsbCAmJiBlY2hvIE9L"
local_prelude_b64=$(printf 'set +e; cd "%s" && command -v npx >/dev/null && echo OK' "$repo" | base64 | tr -d '\r\n')
sed -i "s|$official_prelude_b64|$local_prelude_b64|g" "$tmp"

# Run the public verifier first and preserve its raw observations.
bash "$tmp"
cp "$logdir/gates.json" "$logdir/gates.official_raw.json"
cp "$logdir/reward.txt" "$logdir/reward.official_raw.txt"

# Repair only the two existing T7 observation surfaces. The public verifier's
# generic export-function probe cannot invoke CombinedAutocompleteProvider,
# which is the actual public API modified by the canonical task solution.
tsx_runner="$repo/node_modules/.bin/tsx"
if [ ! -x "$tsx_runner" ]; then
  tsx_runner="$support_repo/node_modules/.bin/tsx"
fi
if [ ! -x "$tsx_runner" ]; then
  echo "No usable tsx runner for repaired S5 evaluator" >&2
  exit 2
fi

set +e
"$tsx_runner" "$probe" "$repo/packages/tui/src/autocomplete.ts" > "$logdir/evaluator_probe.json"
probe_rc=$?
set -e

# Exit 1 is the expected scientific negative for the buggy base.
# Exit >=2 means the evaluator itself could not execute.
if [ "$probe_rc" -ge 2 ]; then
  echo "S5 direct evaluator probe failed to execute, rc=$probe_rc" >&2
  exit "$probe_rc"
fi

python "$postprocess" "$logdir/gates.json" "$logdir/reward.txt" "$logdir/evaluator_probe.json" > "$logdir/evaluator_postprocess.json"

echo "---LOCAL_EQUIVALENT_REWARD---"
cat "$logdir/reward.txt"
echo "---EVALUATOR_PROBE---"
cat "$logdir/evaluator_probe.json"
echo "---GATES---"
cat "$logdir/gates.json"
