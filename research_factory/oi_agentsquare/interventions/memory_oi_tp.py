"""OI-AS-02 orthogonalized TP intervention.

This module intentionally subclasses the frozen AgentSquare MemoryTP so storage,
embedding/database setup and addMemory() remain inherited. Only retriveMemory()
is overridden to remove current-task PLAN_CONTROL while preserving retrieval
and one memory-side LLM call.
"""
import re

from memory_modules import MemoryTP
from utils import llm_response


class MemoryOITP(MemoryTP):
    def retriveMemory(self, query_scenario):
        # Preserve Original TP task extraction.
        task_name = re.findall(r'Your task is to:\s*(.*?)\s*>', query_scenario)[2]

        # Preserve Original TP empty-memory behavior.
        if self.scenario_memory._collection.count() == 0:
            return ''

        # Preserve Original TP retrieval source and top-k.
        similarity_results = self.scenario_memory.similarity_search_with_score(
            task_name, k=1
        )

        task_description = 'You are in the' + query_scenario.rsplit('You are in the', 1)[1]
        guidance = []

        # Preserve one LLM call per retrieved memory. Change only output authority:
        # memory may expose bounded evidence/constraints, but not a current-task plan.
        for result in similarity_results:
            prompt = f"""You will be given a successful case where you successfully completed a task,
and an ongoing task. Extract only reusable memory-derived guidance for the ongoing task.

Do NOT create a plan, ordered action sequence, subgoals, to-do list, or decide the next action.
Do NOT take ownership of current-task planning. The planning module is the sole authority for
current-task decomposition.

Return concise guidance in two parts:
1. Useful prior facts/patterns that may transfer.
2. Constraints or pitfalls the planner/reasoner should consider.

Success Case:
{result[0].metadata['task_trajectory']}
Ongoing task:
{task_description}
Memory Guidance:
"""
            guidance.append(
                llm_response(
                    prompt=prompt,
                    model=self.llm_type,
                    temperature=0.1,
                )
            )

        return 'Memory guidance from successful attempt in similar task:\n' + '\n'.join(guidance)
