import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOP=ROOT/"computer_topconf_2027"
REP=ROOT/"replays"/"RESEARCH_01_S3"
EXT=Path(r"D:/bio_paper/external/swe_together_official_20260928/tasks/pi-mono-auto-93c17d3b")

manifest=json.loads((TOP/"S3_STAGE_B_BOUNDARY_FREEZE_V1.json").read_text(encoding="utf-8"))
raw=json.loads((REP/"USER_REQUIREMENTS_RAW.json").read_text(encoding="utf-8"))
docker=(EXT/"environment"/"Dockerfile").read_text(encoding="utf-8")
task=(EXT/"task.toml").read_text(encoding="utf-8")

assert manifest["task"]=="pi-mono-auto-93c17d3b"
assert manifest["task_initial_state"]=="5133697bc454da5595655cf4b0c70d3c2c725677"
assert "ARG BASE_COMMIT=5133697bc454da5595655cf4b0c70d3c2c725677" in docker
assert "git checkout " + "$" + "{BASE_COMMIT}" in docker
assert 'docker_image = "ghcr.io/togetherbench/multi-user-turn-codebench/pi-mono-auto-93c17d3b:2f7d1992e60d"' in task

indices=[x["source_message_index"] for x in raw]
expected=[0,2,31,34,36,38,40,42,44,48,51,54]
assert indices==expected,(indices,expected)
classes={x["index"]:x["class"] for x in manifest["controlled_sequence"]}
assert list(classes)==expected
assert classes[0]=="CONTEXT_ONLY"
assert classes[2]=="AUTHORITATIVE_PRE_REVISION_REQUIREMENT"
assert classes[31]=="AUTHORITATIVE_LOCATION_CONSTRAINT"
assert classes[34]=="WORKFLOW_ONLY"
assert classes[36]=="AMBIGUOUS_BEHAVIORAL_CLARIFICATION__CONSERVATIVELY_INCLUDED"
assert classes[38]==classes[40]=="HISTORICAL_OBSERVATION"
assert classes[42]=="AUTHORITATIVE_MULTI_TURN_VERIFICATION_REQUIREMENT"
assert classes[44]=="AUTHORITATIVE_CORRECTION_AND_VERIFICATION_REQUIREMENT"
assert classes[48]==classes[51]=="WORKFLOW_ONLY"
assert classes[54]=="AUTHORITATIVE_LATE_REVISION"

by_idx={x["source_message_index"]:x["content"].lower() for x in raw}
assert "test extension" in by_idx[2] and "message_end" in by_idx[2]
assert "cwd/.pi/extensions" in by_idx[31]
assert "first turn open the ui" in by_idx[42]
assert "open on first turn, close on last turn" in by_idx[44]
assert "ui kinda freezes" in by_idx[54] and "can't type" in by_idx[54]

for label,h in manifest["source_hashes"].items():
    if label=="official_task_toml":
        p=EXT/"task.toml"
    elif label=="official_dockerfile":
        p=EXT/"environment"/"Dockerfile"
    elif label=="SPEC_STAGE_A_TASK_FREEZE_V1.md":
        p=TOP/label
    elif label in {"USER_REQUIREMENTS_RAW.json","SOURCE_FREEZE.json","PRE_REVISION_REQUIREMENTS.md","LATE_REVISION.md"}:
        p=REP/label
    else:
        raise AssertionError(label)
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    assert got==h,(label,got,h)

assert manifest["exact_r3_scope_status"]=="PENDING_COMMON_PRESTATE"
assert manifest["paid_arm_authorized"] is False
assert manifest["next_step"]=="S3_EXECUTION_LEVERAGE_GATE"

freeze=(TOP/"S3_STAGE_B_BOUNDARY_FREEZE_V1.md").read_text(encoding="utf-8")
assert "A live worktree path alone is never the scientific snapshot or reuse denominator." in freeze
assert "RESEARCH-01 Phase-B solution" in freeze
assert "No R0/R1/R2/R3 S3 arm is authorized" in freeze

for name in [
    "S3_STAGE_B_R2_RESULT_V1.md",
    "S3_STAGE_B_R3_RESULT_V1.md",
    "S3_STAGE_B_R2_R3_RESULT_V1.md",
]:
    assert not (TOP/name).exists(),name

result={
    "experiment":"S3_STAGE_B_BOUNDARY_FREEZE_V1",
    "status":"PASS",
    "task_initial_state":manifest["task_initial_state"],
    "controlled_user_indices":expected,
    "revision_boundary":manifest["revision_boundary"],
    "exact_r3_scope_status":manifest["exact_r3_scope_status"],
    "paid_arm_authorized":False,
    "next_step":"S3_EXECUTION_LEVERAGE_GATE",
}
(TOP/"S3_STAGE_B_BOUNDARY_FREEZE_RESULT_V1.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
