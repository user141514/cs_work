import json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOP=ROOT/"computer_topconf_2027"
REP=ROOT/"replays"/"RESEARCH_01_S3"

ex=json.loads((TOP/"S3_MECHANISM_EXPOSURE_RESULT_V1.json").read_text(encoding="utf-8"))
bf=json.loads((TOP/"S3_STAGE_B_BOUNDARY_FREEZE_RESULT_V1.json").read_text(encoding="utf-8"))
snap=json.loads((REP/"phase_a"/"PHASE_A_SNAPSHOT.json").read_text(encoding="utf-8"))
dev=(REP/"RESULT.md").read_text(encoding="utf-8")
s1=(TOP/"S1_STAGE_B_CONTROLLED_REPLAY_RESULT_V1.md").read_text(encoding="utf-8")
s5=(TOP/"S5_STAGE_B_R0_RESULT_V1.md").read_text(encoding="utf-8")

assert ex["verdict"]=="EXPOSURE_SOURCE_PROVEN"
assert bf["status"]=="PASS"
assert bf["paid_arm_authorized"] is False
assert snap[".pi/extensions/signal-ui.ts"]["lines"]==100
assert snap["packages/coding-agent/test/signal-ui-extension.test.ts"]["lines"]==142
assert "provider duration: 1,701,705 ms (~28.36 min)" in dev
assert "DEVELOPMENT_ONLY" in dev
assert ("boundary_contaminated" in dev.lower() or "boundary-contaminated" in dev.lower())
assert "S1_R3_VS_RAW_HISTORY_VALUE = FAIL_ON_THIS_TASK" in s1
assert "S5_VALUE_GATE_V:" in s5 and "NEGATIVE." in s5 and "NOT a V-positive pressure witness" in s5

docker=Path(r"C:/Program Files/Docker/Docker/resources/bin/docker.exe")
docker_client_exists=docker.is_file()
docker_server_ready=False
docker_probe={"client_exists":docker_client_exists}
if docker_client_exists:
    p=subprocess.run(
        [str(docker),"version","--format","{{json .}}"],
        capture_output=True,text=True,encoding="utf-8",errors="ignore",timeout=30
    )
    docker_probe.update({
        "returncode":p.returncode,
        "stdout":p.stdout.strip(),
        "stderr":p.stderr.strip(),
    })
    if p.returncode==0:
        try:
            obj=json.loads(p.stdout)
            docker_server_ready=bool(obj.get("Server"))
        except Exception:
            docker_server_ready=False

old_checkout=Path(r"C:/Users/Administrator/AppData/Local/Temp/research01_s3_pi_mono")
old_checkout_exists=old_checkout.is_dir()
old_checkout_has_node_modules=(old_checkout/"node_modules").is_dir()

result={
    "experiment":"S3_EXECUTION_LEVERAGE_GATE_V1",
    "scientific_execution_leverage":"PASS",
    "current_execution_authorization":"DEFERRED_RUNTIME_NOT_READY" if not docker_server_ready else "RUNTIME_READY_FOR_NEXT_PREFLIGHT_STAGE",
    "paid_model_authorized_now":False,
    "initial_paid_sequence_if_runtime_passes":[
        "COMMON_PRESTATE",
        "R2_FULL_RESTART",
        "R3_ORACLE_SCOPED",
    ],
    "conditional_next_paid_arm":"R0_RAW_HISTORY only if R3-vs-R2 local headroom survives",
    "r1_policy":"NOT_AUTHORIZED_FOR_SYMMETRY; conditional only if R0 cannot adjudicate the frozen value gate",
    "lower_level_evidence":{
        "mechanism_exposure":"EXPOSURE_SOURCE_PROVEN",
        "offline_boundary":"PASS",
        "developmental_phase_a_material_work":{
            "extension_lines":snap[".pi/extensions/signal-ui.ts"]["lines"],
            "extension_bytes":snap[".pi/extensions/signal-ui.ts"]["bytes"],
            "test_lines":snap["packages/coding-agent/test/signal-ui-extension.test.ts"]["lines"],
            "test_bytes":snap["packages/coding-agent/test/signal-ui-extension.test.ts"]["bytes"],
            "phase_a_duration_minutes":28.36,
            "scientific_substitute":False,
        },
        "cheap_rival_pressure":{
            "S1":"R3-vs-R2 headroom pass; RAW_HISTORY value fail on task",
            "S5":"R3-vs-R2 headroom pass; S5 value gate V negative; RAW_HISTORY much cheaper",
        },
    },
    "runtime":{
        "docker_probe":docker_probe,
        "docker_server_ready":docker_server_ready,
        "developmental_checkout_exists":old_checkout_exists,
        "developmental_checkout_has_node_modules":old_checkout_has_node_modules,
        "developmental_checkout_admissible_scientific_prestate":False,
    },
    "early_stop_rule":[
        "runtime preflight fails -> zero model spend",
        "common prestate has no material derived work -> S3 NONIDENTIFIABLE",
        "R2 invalid/non-executable -> INVALID, no science verdict",
        "R3 fails R2 endpoint or preserves <30% meaningful work -> stop before R0/R1",
        "R3 headroom survives -> authorize exactly R0 next; R1 remains conditional",
    ],
    "next_step":"S3_RUNTIME_PREFLIGHT_V1",
}
(TOP/"S3_EXECUTION_LEVERAGE_RESULT_V1.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
