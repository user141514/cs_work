# S5 Stage-B Scientific Runtime Identity Decision V1

date: 2026-09-28
status: SCIENTIFIC_IDENTITY_FROZEN__OMP_GPT56_SOL
scope: S5 and remaining Stage-B scientific arms

## Claim

The S1-S5 scientific comparison must keep the coding-agent configuration fixed.

Authoritative scientific contract:
- STAGE_B_CONTROLLED_REPLAY_PROTOCOL_V1.md
- S5_STAGE_B_BOUNDARY_FREEZE_V1.md

Frozen scientific identity:
- GPT-5.6 Sol
- xhigh reasoning
- OMP process under lifetime
- no skills
- no rules
- no extensions
- tools = read,bash,edit,write,grep,glob
- isolated worktree per arm

## Evidence

Valid S1 scientific arms used this exact identity, including:
- R0 turn_e5044b6bb9244fee9c93101cc163773f
- R3 turn_7b43e3051aea4c97a1b538f798cf972a

Both completed terminal/quiescent under lifetime.

A later infrastructure-only preflight in STAGEB_AGENT_RUNTIME_CONTRACT_V1.md selected Claude Code + DeepSeek after a native Codex isolation preflight failed.

That fallback is not scientifically interchangeable with the already-observed S1 agent identity.

## Decision

For Stage-B science:
- continue with the frozen OMP + GPT-5.6 Sol/xhigh configuration;
- do not use the Claude/DeepSeek freeze receipt to generate S5 scientific outcomes;
- retain the Claude/DeepSeek receipt as infrastructure evidence only.

Changing the model/backend after S1 would confound task/regime effects with agent-configuration effects and invalidate the S1-S5 aggregate H/V decision.

## Counterexample

If the scientific contract had frozen only an abstract tool-capable coding-agent class rather than one fixed configuration, a backend switch could be admissible.

It explicitly freezes one fixed coding-agent configuration and the valid S1 evidence names GPT-5.6 Sol/xhigh + OMP, so that counterexample does not apply.

## Rollback

If OMP + GPT-5.6 Sol becomes unavailable before a valid S5 arm starts:
- mark Stage B runtime-blocked;
- do not silently switch provider/model;
- any alternative backend requires a new independently frozen experimental cohort and cannot be pooled with S1.
