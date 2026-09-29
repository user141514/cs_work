# OI-AS-05 Result — Residual O+I Decision Gate

Date: 2026-09-30
Status: COMPLETED_TERMINATE_AGENTSQUARE_ALFWORLD_OI_LINE

## Question

After terminating the hard `MemoryTP-plan-conflict` seam, does any residual soft coupling in the frozen AgentSquare/ALFWorld space justify a distinct new mechanism test?

Admission required all five pre-registered criteria A-E:

A. independent seam;
B. genuine same-level responsibility conflict rather than explicit hierarchy/handoff;
C. identifiable frozen contrast;
D. pre-existing directional evidence of harm;
E. minimal isolated intervention.

## Candidate decisions

### PLANNING_TO_REASONING_GUIDANCE — REJECT

Exposure: 175/210 executable combinations.

- A: PASS — distinct from MemoryTP.
- B: FAIL — pinned workflow explicitly calls planner first, then injects each subtask's `reasoning instruction` as `Current task:` for the reasoning module. This is the intended hierarchical planner→executor interface, not two independent modules owning the same action decision.
- C: FAIL — all five non-None planning modules emit reasoning instructions. The only unexposed option is `planning=None`, which removes decomposition itself; existing frozen labels cannot isolate guidance from planning presence.
- D: FAIL — OI-AS-00 provides occupancy only, and OI-AS-01..04 contain no failure trace or outcome pattern specifically attributed to planner→reasoner guidance.
- E: PASS in principle — one could imagine preserving decomposition while stripping/replacing the reasoning-instruction field, but technical manipulability is insufficient when B/C/D fail.

### MEMORY_TO_REASONING_GUIDANCE — REJECT

Exposure: 42/210.

- A: FAIL — under the frozen OI-AS-00 mapping, CURRENT_GUIDANCE is TP-only and therefore is the same MemoryTP/I3 mechanism already terminated by OI-AS-04.
- B/C/D: FAIL — there is no independent residual responsibility conflict, independent contrast, or distinct harm signal after the 0/6 conflict-prevalence screen.
- E: PASS technically — OI-TP showed guidance-form manipulation is possible, but this is not a new seam.

### PLANNING_TO_TOOL_GUIDANCE — INELIGIBLE

Exposure in executable ALFWorld space: 0.

AgentSquare ALFWorld search fixes `tooluse=None`, so this tag is not an executable ALFWorld mechanism.

## Decision

No residual soft seam passes A-E.

**TERMINATE the current AgentSquare/ALFWorld Orthogonality + Invariants research line.**

Consequences:
- hard O+I gate integration is not authorized;
- no new soft-guidance intervention is authorized;
- do not rename/repackage the failed MemoryTP seam;
- do not use high soft-coupling occupancy alone as justification for another experiment.

## Scope boundary

Terminated:
- the current AgentSquare/ALFWorld O+I line under the frozen module space and evidence chain.

Not terminated:
- Orthogonality + Invariants as a general research idea on a different baseline/task where an independent conflict mechanism is evidenced before intervention design.

## Next research-factory action

Return control to the higher-level research selector/replanning layer with this line recorded as a negative result. Do not create OI-AS-06 on AgentSquare/ALFWorld without genuinely new external evidence.
