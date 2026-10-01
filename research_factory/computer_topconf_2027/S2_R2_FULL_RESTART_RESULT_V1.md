# S2 R2 Full-Restart Result V1

date: 2026-10-02
status: VALID_R2_EXECUTION__VERIFIER_STRUCTURALLY_INVALID__NO_CORRECTNESS_VERDICT__SELECTOR_REPLAN_NEXT
task: pi-mono-auto-a4fca584
arm: R2_FULL_RESTART
formal_paper_candidate: false

## Decision

R2 FULL_RESTART executed validly and independently from TASK_INITIAL_STATE.

However, the frozen official verifier is structurally incompatible with the frozen task base before it reaches the local-install behavior that it is supposed to measure.

Therefore:

- R2 execution validity: **PASS**
- R2 product-semantic secondary evidence: **positive**
- frozen verifier raw reward: **0.0000**
- frozen verifier validity for R2 correctness: **INVALID**
- scientific R2 correctness verdict: **NONIDENTIFIABLE**
- PARTIAL_REFERENCE classification: **NOT APPLIED**
- S2 V-positive qualification: **NOT ESTABLISHED**
- R3: **NOT AUTHORIZED**
- R0/R1: **NOT AUTHORIZED**

Do not reinterpret the raw verifier 0.0000 as an S2/BFSC scientific negative.

Do not repair the verifier after observing this R2 outcome and then rescore the same arm.

## Independent R2 execution identity

R2 started from a fresh repository exported from the exact official task image:

TASK_INITIAL_STATE:

`e54dff7efb460e364a39e4a22369991a20c105b9`

Admission:
- clean repo;
- zero remotes;
- zero local heads;
- zero tags;
- fresh session directory;
- no common-prestate implementation;
- no U0-U3 session/history inheritance.

Scientific identity:
- GPT-5.6 Sol;
- xhigh;
- no fallback;
- OMP 18.1.15;
- Node v20.20.2;
- task Bun 1.3.13;
- harness Bun 1.3.14;
- user `agent`, uid1001;
- tools: read,bash,edit,write,grep,glob;
- no skills/rules/extensions/title.

Supervisor scan found zero R2 tool-path references to:
- S2 common-prestate bundle/session;
- R3 frozen scope;
- R2/R3 historical result material;
- reference/gold patch;
- oracle session/intents;
- canonical goals;
- RESEARCH-01 Phase-B;
- verifier results.

## Prompt transport

Frozen R2 prompt:
- bytes: 2,971
- SHA256:
  `e750cacc11477779443911df78f48510c76a7bf219eee0b22177698f630b77d4`

Delivered scientific user turn:
- bytes: 2,970
- SHA256:
  `992ba92d365970b4faa0eda35f8ea15a5b1cf59b65362b8bef2215deb321a0a8`

The only byte difference is the frozen file's final LF, stripped by shell command substitution.

All 2,970 semantic characters are identical.
No requirement information was added, removed, or altered.

Classification:

`VALID_SEMANTIC_CONTENT__SINGLE_TERMINAL_LF_TRANSPORT_NORMALIZATION`

No post-outcome rerun was performed.

## R2 session / work accounting

Session ID:

`01a0f834-4b2d-7000-9635-54855f211b55`

Frozen session copy:

`D:/cs_work/external/spec_stageb_sessions/s2_r2_full_frozen_v1/2026-10-01T16-02-51-821Z_01a0f834-4b2d-7000-9635-54855f211b55.jsonl`

Session:
- SHA256:
  `18ce317dc49fabd818b4dcebb83fb467ab98e5497f19a8f9c5996f7dcfffd6c8`
- bytes: 2,203,644
- lines: 236
- scientific user turns: 1
- final assistant stop: `stop`
- Lifetime: succeeded / terminal / quiescent / exit 0
- wall: 718.786338 s

Accounting:
- model calls: 50
- tool calls: 90
- mutating edit/write calls: 16
- input tokens: 221,540
- output tokens: 28,778
- cache-read tokens: 8,381,952
- reasoning tokens: 15,440
- reported cost: $4.8145008

The live R2 session is now read-only and must not be continued.

## Final R2 implementation snapshot

Tracked patch:
- bytes: 22,862
- SHA256:
  `3b6f6c182c9a73539cac1d6b4c2c8a4203ae3d5ef024089b459398d0cd792671`

Tracked modified files: 8

Untracked task artifacts:
1. `packages/coding-agent/src/cli/package-command.ts`
   - 4,731 bytes
   - SHA256 `b39adca3756da54abd4ae27ac901d91459b4bf8861f35c242c514c37f8ff3899`
2. `packages/coding-agent/test/package-cli.test.ts`
   - 4,480 bytes
   - SHA256 `f3711e431705b874f00fe107f2b60660e2506874b505a29fc9b49886722d445d`

No tracked deletions.

Fresh exact official-image reconstruction:
- `git apply --check --binary`: PASS
- patch application: PASS
- reconstructed status matches live R2
- all ten final changed/new file SHA256 values match the live R2 state.

Authority:
`S2_R2_FULL_RESTART_SNAPSHOT_V1/`

Snapshot manifest SHA256:
`a6e75270dd4ab9e109efb8b49788e447379efb2e0b41d8a33a962a250e01fd05`

## Product-semantic evidence from R2

The R2 implementation independently derived the final-spec architecture:

- CLI local source input is first resolved/validated from the invocation cwd;
- settings persistence is separately serialized relative to the concrete settings file;
- user/global settings use the global settings base;
- project-local settings use the project `.pi/settings.json` base;
- list/dedup/remove identity is scope-aware;
- local sources are referenced in place and not deleted;
- npm/git behavior is retained;
- documentation describes settings-file-relative local paths.

Secondary correctness evidence observed during the scientific run:

- targeted Vitest: 5 relevant tests passed;
- global local-directory install/list/dedup/remove path: PASS;
- project-local file install/remove path: PASS;
- settings-file-relative persistence: PASS in targeted tests;
- missing local-source validation: PASS;
- source-preservation behavior: PASS;
- independent end-to-end smoke: PASS;
- `npx tsgo --noEmit`: PASS;
- targeted Biome: PASS;
- broader package test run: 44/45, with the sole failure being the existing network-dependent nonexistent-GitHub-URL test timing out;
- `npm run check`: root Biome/TypeScript phases passed; later web-ui checking hit missing frozen-base build artifacts.

This evidence supports that the implementation is plausible and final-spec-directed.

It does **not** replace the pre-registered frozen verifier endpoint.

## Frozen verifier raw result

Same frozen official task verifier and official image were used.

Verifier:
- task.toml SHA256:
  `ef07e5601a1ea034f91613826367ec003154ab6a7ff4f86249641a940509e6f3`
- normalized test.sh SHA256:
  `cefe818bfb78d67eead6662a375387a6b350603016c2775e39affa97cfa5874a`

Raw final reward:

`0.0000`

Raw gates:
- upstream package-manager P2P: PASS
- upstream Biome: PASS
- upstream scoped tsgo: FAIL with the already-known baseline TS5112 issue
- local-install F2P gates: FAIL before behavior evaluation
- upstream local-install test-discovery/test-count gates: FAIL

## Why the primary verifier is structurally invalid

Frozen task base:

`packages/coding-agent/src/core/package-manager.ts`

contains:

- line 43: `export interface PackageManager`
- line 592: `export class DefaultPackageManager implements PackageManager`

A TypeScript interface has no runtime constructor.

Frozen verifier `test.sh` hardcodes:

- line 80: `import { PackageManager } ...`
- line 99: `new PackageManager(...)`
- line 215: same import
- line 234: same constructor call

Observed verifier failure:

`TypeError: PackageManager is not a constructor`

This occurs in test setup before the local-install behavior assertions execute.

Therefore the F2P measurement is not merely reporting that R2 failed the requested behavior.
It is attempting to instantiate a runtime class that does not exist in the frozen task architecture.

The structural mismatch is independent of the R2 patch: it is already present in the frozen base/verifier pair.

## PARTIAL_REFERENCE_GUARD adjudication

PRG-1 states:

> if R2 runtime/session/verifier is invalid, no scientific verdict; no R3/R0/R1 until validity is restored.

Therefore PRG-2's full-vs-partial R2 qualification is **not reached**.

Do not label this R2:
- FULL_SUCCESS;
- PARTIAL_REFERENCE;
- scientific failure;
- V-negative evidence.

S2's R2 correctness endpoint is:

`NONIDENTIFIABLE_VERIFIER_STRUCTURAL_INVALIDITY`

S2 cannot currently qualify as a V-positive witness because the required frozen R2 correctness predicate was not validly measured.

## Why there is no verifier repair in this arm

The verifier defect was diagnosed after the R2 outcome existed.

Changing:

`PackageManager -> DefaultPackageManager`

or altering any other gate now and rescoring this same completed R2 would create a post-outcome measurement change.

That is forbidden by the factory's no-post-hoc-rescue rule.

A future selector may decide whether:
- S2 should be retired as measurement-invalid;
- a prospective verifier-repair protocol is worth defining for a new task/run;
- the remaining S4 witness should be prioritized.

This completed R2 must not be rerun or rescored under a repaired verifier.

## Immediate authorization consequence

R3 is **not authorized**.

R0/R1 are **not authorized**.

S4 is not automatically activated by this result without selector replanning.

## NEXT_STEP

`BFSC_SELECTOR_REPLAN_AFTER_S2_VERIFIER_INVALID` only.

The selector must absorb:
- S5 V-negative;
- S3 V-ineligible / local partial-adjudication gap;
- S2 valid execution but primary verifier structurally invalid / correctness nonidentifiable;
- S4 as the only still-unobserved frozen V-witness slot.

Do not run S2 R3/R0/R1 before that selector decision.
Do not repair/rescore this completed R2.
