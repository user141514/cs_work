from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "upstream" / "runtime"
ARMS = ROOT / "arms"

if ARMS.exists():
    shutil.rmtree(ARMS)

for arm in ("original", "oi_tp"):
    shutil.copytree(UPSTREAM, ARMS / arm)

memory_path = ARMS / "oi_tp" / "memory_modules.py"
text = memory_path.read_text(encoding="utf-8")

needle = "class MemoryVoyager(MemoryBase):"
if needle not in text:
    raise RuntimeError("MemoryVoyager anchor missing")

oi_class = r'''
class MemoryTPOrthogonalized(MemoryTP):
    """TP retrieval with memory guidance only; current-task plan ownership stays in planning."""

    def retriveMemory(self, query_scenario):
        # Keep the original TP query parsing and retrieval path unchanged.
        task_name = re.findall(r'Your task is to:\s*(.*?)\s*>', query_scenario)[2]

        if self.scenario_memory._collection.count() == 0:
            return ''

        similarity_results = self.scenario_memory.similarity_search_with_score(
            task_name, k=1)

        # Keep one memory-side LLM call per retrieved result, but remove PLAN_CONTROL.
        experience_guidance = []
        task_description = 'You are in the' + query_scenario.rsplit('You are in the', 1)[1]

        for result in similarity_results:
            prompt = f"""You will be given a successful case where an agent completed a task, followed by an ongoing task.
Extract transferable memory-derived guidance that may help the reasoning module, but DO NOT produce a plan, ordered steps, subgoals, or concrete next actions for the ongoing task.
Return at most five concise constraints, checks, or heuristics. These are non-authoritative hints only; the planning module remains solely responsible for the current-task plan.
Success Case:
{result[0].metadata['task_trajectory']}
Ongoing task:
{task_description}
Guidance:
"""
            experience_guidance.append(
                llm_response(
                    prompt=prompt,
                    model=self.llm_type,
                    temperature=0.1
                )
            )

        return 'Guidance from successful attempt in similar task:\n' + '\n'.join(experience_guidance)

'''

text = text.replace(needle, oi_class + needle)
with memory_path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(text)

module_map = ARMS / "oi_tp" / "module_map.py"
map_text = module_map.read_text(encoding="utf-8")
old = "        'tp': MemoryTP,\n"
new = "        'tp': MemoryTP,\n        'tp-oi': MemoryTPOrthogonalized,\n"
if old not in map_text:
    raise RuntimeError("TP map anchor missing")
with module_map.open("w", encoding="utf-8", newline="\n") as f:
    f.write(map_text.replace(old, new))

print(ARMS / "original")
print(ARMS / "oi_tp")
