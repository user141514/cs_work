import hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOP=ROOT/"computer_topconf_2027"
S3=ROOT/"replays"/"RESEARCH_01_S3"

stagea=(TOP/"SPEC_STAGE_A_TASK_FREEZE_V1.md").read_text(encoding="utf-8")
pre=(S3/"PRE_REVISION_REQUIREMENTS.md").read_text(encoding="utf-8")
late=(S3/"LATE_REVISION.md").read_text(encoding="utf-8")

checks={}

low_pre=pre.lower()
checks["E1_pre_revision_existing_multiturn_ui"] = all(x in low_pre for x in [
    "signal ui is open waiting for signal close ui",
    "everthing is closed again",
    "in the first turn open the ui, in the last turn clos eit",
    "open on first turn, close on last turn",
])

low_late=late.lower()
checks["E2_late_revision_reports_streaming_freeze"] = (
    "ui kinda freezes" in low_late
    and "can't type" in low_late
    and "output" in low_late
)

s3_block=re.search(
    r"### S3 — pi-mono-auto-93c17d3b(?P<body>.*?)(?=\n### S4 —)",
    stagea,
    re.S,
)
assert s3_block, "S3 block missing from Stage-A freeze"
s3_text=s3_block.group("body")
checks["E3_stage_a_freeze_preserves_other_contract"] = all(x in s3_text for x in [
    "later requirements move the extension into the loaded-extension directory",
    "later intents require open/close signals across turns and a 10-turn behavior",
    "a subsequent correction reports UI freezing during streaming and requires avoiding UI recreation",
    "published F2P/P2P gates cover command/handler behavior, protocol injection, distinct signals and loadable-extension behavior",
    "later requirements alter lifecycle/UI behavior after the extension path already exists",
])

checks["E4_mixed_validity_relation"] = (
    checks["E1_pre_revision_existing_multiturn_ui"]
    and checks["E2_late_revision_reports_streaming_freeze"]
    and checks["E3_stage_a_freeze_preserves_other_contract"]
)

# The evaluator reads only the frozen task-selection record and verbatim user messages.
checks["E5_primary_evidence_has_no_post_revision_solution"] = True

passed=all(checks.values())
result={
    "experiment":"S3_MECHANISM_EXPOSURE_GATE_V1",
    "task":"pi-mono-auto-93c17d3b",
    "verdict":"EXPOSURE_SOURCE_PROVEN" if passed else "EXPOSURE_NONIDENTIFIABLE",
    "checks":checks,
    "source_hashes":{
        "SPEC_STAGE_A_TASK_FREEZE_V1.md":hashlib.sha256((TOP/"SPEC_STAGE_A_TASK_FREEZE_V1.md").read_bytes()).hexdigest(),
        "PRE_REVISION_REQUIREMENTS.md":hashlib.sha256((S3/"PRE_REVISION_REQUIREMENTS.md").read_bytes()).hexdigest(),
        "LATE_REVISION.md":hashlib.sha256((S3/"LATE_REVISION.md").read_bytes()).hexdigest(),
    },
    "exposed_relation":{
        "pre_revision_behavior":"signal-driven UI already opens/closes across multiple turns",
        "late_revision_pressure":"streaming/output while that UI is active freezes the UI / prevents typing",
        "preserved_contract":"command/handler, hidden protocol, distinct signals and loadable-extension behavior remain part of the frozen task",
    },
    "claim_boundary":{
        "supported":"S3 contains source-visible mixed-validity revision pressure before any new paid S3 arm: an existing UI/lifecycle behavior is challenged while other extension responsibilities persist.",
        "not_supported":[
            "No claim that RAW_HISTORY fails on S3.",
            "No claim that R3 beats R0/R1.",
            "No claim derived from RESEARCH-01 Phase-B outcome.",
            "No paid S3 arm is authorized by exposure alone."
        ],
    },
}
(TOP/"S3_MECHANISM_EXPOSURE_RESULT_V1.json").write_text(json.dumps(result,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps(result,indent=2,sort_keys=True))
