# Stage-B Agent Runtime Contract V1

date: 2026-09-28
status: IMPLEMENTED_PENDING_PREFLIGHT
scope: runtime isolation only

## Purpose

Provide one clean, resumable coding-agent runtime for the frozen Stage-B R0/R1/R2/R3 experiment. This does not change SWE-Together tasks, verifier logic, S1-S5 identities, consolidated-spec rules, R3 oracle rules, pass/fail predicates, or the research topic.

Runtime failures are execution evidence only and never scientific negatives.

## Fixed-backend invariant

Backend selection happens once before any valid Stage-B scientific arm begins.

Selection order:

1. clean Codex preflight;
2. if Codex fails isolation, auth, or resume acceptance, clean Claude Code plus DeepSeek safe-mode preflight;
3. freeze the first passing backend in external/spec_stageb_logs/stageb_backend_freeze.json;
4. all later Stage-B arms use that backend.

Mixing Codex and Claude/DeepSeek across R0/R1/R2/R3 is forbidden.

## Clean Codex

Frozen configuration:

- native Codex CLI;
- model gpt-5.6-sol;
- reasoning effort xhigh;
- runtime root outside D:\bio_paper;
- isolated HOME and USERPROFILE;
- isolated CODEX_HOME;
- only auth.json copied from existing Codex home;
- user config and rules ignored;
- benchmark checkout outside D:\bio_paper.

Pass requires the literal main/windows diff, exact two changed files, first-turn marker, persisted thread id, successful resume marker, no global customization evidence, and a clean checkout.

## Claude Code plus DeepSeek fallback

Fallback is permitted only when clean Codex preflight fails before scientific execution.

Frozen mechanism:

- installed Claude Code CLI;
- safe-mode enabled;
- slash commands disabled;
- isolated HOME and USERPROFILE;
- DeepSeek Anthropic-compatible endpoint, token and model read in memory from existing Claude settings;
- token value never serialized to research files, receipts, logs, or prompts;
- built-in tools only.

Pass requires the same branch identity, clean checkout, first-turn marker, persistent session resume marker, and no forbidden customization evidence.

## Runtime artifacts

Source:

- research_factory/computer_topconf_2027/run_stageb_agent.ps1

Transient runtime:

- D:\stageb_agent_runtime\profiles
- D:\stageb_agent_runtime\arms

Evidence:

- external/spec_stageb_logs
- external/spec_stageb_logs/stageb_backend_freeze.json

## Wrapper actions

Inspect reports runtime paths and frozen state.

Preflight tries clean Codex first, then Claude Code plus DeepSeek only if needed, and freezes the first passing backend.

Launch requires a PASS freeze receipt. A new session reconstructs a fresh S1 arm. A continuation requires the existing session id and arm. Launch never changes backend.

## Invalid runs

Exclude from scientific denominators:

- wrong or missing benchmark refs;
- global customization contamination;
- backend mismatch;
- auth/provider failure;
- provider timeout without valid terminal result;
- lost session identity;
- preflight modifying checkout;
- forbidden gold/reference/future-outcome access.

## Acceptance before Stage B resumes

1. PowerShell syntax and Inspect smoke.
2. Clean Codex preflight.
3. Claude/DeepSeek preflight only if Codex fails.
4. Read back freeze receipt and verify secrets_recorded is false.
5. Run one S1 U0 acceptance through Launch.
6. Do not send U1-U4 until U0 returns a valid terminal result under frozen backend.
