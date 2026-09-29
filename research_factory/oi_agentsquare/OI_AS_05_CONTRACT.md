# OI-AS-05 — Residual O+I Decision Gate

Date: 2026-09-30
Status: AUTHORIZED_BY_USER_CONTINUATION

## Purpose

Decide whether any residual soft coupling in the frozen AgentSquare/ALFWorld space warrants a distinct new mechanism test after the hard `MemoryTP-plan-conflict` seam was terminated.

This is a decision gate, not a new intervention experiment. It uses only frozen OI-AS-00..04 evidence and pinned AgentSquare source.

## Candidate residual soft couplings

From OI-AS-00 executable ALFWorld space:
- `PLANNING_TO_REASONING_GUIDANCE`: 175/210;
- `MEMORY_TO_REASONING_GUIDANCE`: 42/210;
- `PLANNING_TO_TOOL_GUIDANCE`: absent from executable ALFWorld because tooluse is fixed to None.

## Admission criteria for a NEW mechanism

A residual soft coupling may proceed only if ALL conditions hold before any new model/benchmark call:

A. **Independent seam** — it is not merely a relabeling/subset of the terminated MemoryTP/I2/I3 mechanism.

B. **Responsibility conflict** — pinned source shows two modules independently owning or issuing competing decisions at the same abstraction level, not an explicit producer→consumer or planner→executor interface.

C. **Identifiable contrast** — frozen data/module labels contain a contrast that varies this coupling without simultaneously removing the parent module or changing another major capability; otherwise existing evidence cannot directionally screen the mechanism.

D. **Pre-existing directional evidence** — frozen evidence already contains an outcome pattern, failure trace, or source contradiction specifically consistent with harm from this coupling. High occupancy alone is insufficient.

E. **Minimal isolated intervention** — a plausible intervention can remove only the suspected overlap while preserving the module's intended primary responsibility and interface contract.

If any criterion fails, the residual soft seam is NOT admitted. Do not generate a fresh experiment merely because one could be imagined after observing the previous seam's failure.

## Line-level decision rule

- If at least one residual soft seam passes A-E, retain AgentSquare/ALFWorld O+I for exactly that newly admitted seam.
- If no residual soft seam passes A-E, terminate the AgentSquare/ALFWorld O+I line. Preserve O+I only as a broader research idea requiring a different baseline/task with independent evidence.

No web research, new benchmark, new model call, or intervention implementation is authorized inside OI-AS-05.
