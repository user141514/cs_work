import json,re
from pathlib import Path

TOP=Path("research_factory/computer_topconf_2027")
result=json.loads((TOP/"S3_RUNTIME_PREFLIGHT_RESULT_V1.json").read_text(encoding="utf-8"))
evidence=(TOP/"S3_RUNTIME_PREFLIGHT_EVIDENCE_V1.txt").read_text(encoding="utf-8",errors="ignore")
contract=(TOP/"S3_RUNTIME_PREFLIGHT_V1.md").read_text(encoding="utf-8")

assert result["verdict"]=="DAEMON_NOT_READY"
assert result["model_calls_made"]==0
assert result["scientific_state_mutated"] is False
assert result["paid_model_authorized_now"] is False
assert result["docker"]["client_version"]=="29.8.0"
assert result["docker"]["daemon_reachable"] is False
assert result["docker"]["backend_binary_present"] is True
assert result["docker"]["registry_key_present"] is False
assert result["docker"]["prior_installer_attempt"]["result"]=="exit status 1"
assert result["official_assets"]["image_inspected"] is False
assert result["official_assets"]["image_pulled"] is False
assert result["pass_criteria"]["R1_daemon_reachable"] is False
assert result["pass_criteria"]["R5_zero_model_no_science_mutation"] is True
assert result["next_step_after_user_action"]=="RESUME_S3_RUNTIME_PREFLIGHT_V1_AT_R1_R2"

assert '"Server":null' in evidence
assert "failed to connect to the docker API" in evidence
assert 'cannot find registry key "SOFTWARE\\\\Docker Inc.\\\\Docker Desktop"' in evidence
assert "installer exited with status 1" in evidence
assert "VirtualizationFirmwareEnabled : True" in evidence
assert "PASS_RUNTIME_READY" in contract
assert "DAEMON_NOT_READY" in contract
assert "model_calls_authorized: false" in contract

for name in [
    "S3_COMMON_PRE_REVISION_SNAPSHOT_V1.md",
    "S3_STAGE_B_R2_RESULT_V1.md",
    "S3_STAGE_B_R3_RESULT_V1.md",
    "S3_STAGE_B_R0_RESULT_V1.md",
]:
    assert not (TOP/name).exists(), name

out={
    "experiment":"S3_RUNTIME_PREFLIGHT_V1",
    "verification":"PASS",
    "verdict":"DAEMON_NOT_READY",
    "model_calls_made":0,
    "paid_model_authorized_now":False,
    "resume_after_user_action":"RESUME_S3_RUNTIME_PREFLIGHT_V1_AT_R1_R2",
}
(TOP/"S3_RUNTIME_PREFLIGHT_VERIFY_V1.json").write_text(json.dumps(out,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(out,indent=2,sort_keys=True))
