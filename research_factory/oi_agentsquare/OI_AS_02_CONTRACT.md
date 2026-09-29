# OI-AS-02 — Controlled Memory-Boundary Intervention

Date: 2026-09-29
Plan: OI-AS-20260929
Status: AUTHORIZED_BY_USER_CONTINUATION

## Scientific question

Does removing current-task PLAN_CONTROL from AgentSquare MemoryTP improve task behavior when all other agent components and inference conditions are held fixed?

## Frozen model/runtime condition

Inference backend:
- Codex CLI / authenticated local Codex provider
- model: GPT-5.6 Luna
- reasoning effort: medium
- structured/non-interactive invocation where applicable

Both arms MUST use the same model, effort, prompt/output constraints, retry policy and model-call budget.

This is not an exact reproduction of AgentSquare's original GPT-4o / GPT-4o-mini absolute scores. It is a controlled causal comparison of Original-TP vs OI-TP under one common backend.

## Intervention

Original TP:
retrieved successful trajectories
-> LLM generates a plan/strategy for the ongoing task
-> memory module returns that plan

OI-TP:
same retrieval source/top-k
-> same number of LLM calls
-> LLM produces bounded memory-derived guidance/constraints only
-> memory module returns guidance
-> current-task plan/subgoal decomposition remains owned by the planning module

## Fixed components

Before benchmark execution freeze:
- planning=IO;
- reasoning=IO;
- tooluse=None;
- identical task subset/order/seeds;
- identical environment and prompts outside the memory intervention;
- identical retry/timeout policy;
- equal model-call budget per episode.

## Required implementation proof

Before running tasks:
1. show a source diff between TP and OI-TP;
2. prove retrieval/top-k/storage path unchanged;
3. prove both arms make the same number of memory-side model calls;
4. prove only Original TP requests/returns a current-task Plan;
5. run a model-route smoke proving GPT-5.6 Luna + medium works through Codex without OPENAI_API_KEY.

## Primary outcome

Paired ALFWorld task success on the same small frozen task subset.

Secondary:
- episode-level paired differences;
- model-call count;
- wall time;
- invalid/runtime failures;
- any behavior showing planning-authority conflict.

## Stop / escalation

First pilot uses the smallest subset sufficient to catch runtime or strong directional failure. Do not launch full AgentSquare search.

If the two arms are operationally valid and show a coherent directional difference, pre-register the next larger paired subset.
If OI-TP is worse or causes invariant-preserving but task-breaking behavior, treat that as evidence against the current invariant intervention rather than silently changing the invariant.

## Forbidden

- changing model/effort between arms;
- using Sol/xhigh for one arm and Luna/medium for the other;
- substituting a different benchmark after seeing results;
- changing the OI-TP prompt after observing task outcomes without creating a new run;
- calling this an exact AgentSquare reproduction or publication result.
