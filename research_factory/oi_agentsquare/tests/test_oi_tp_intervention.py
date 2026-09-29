import ast
import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "runtime"
TARGET = ROOT / "interventions" / "memory_oi_tp.py"

original_source = (UPSTREAM / "memory_modules.py").read_text(encoding="utf-8")
oi_source = TARGET.read_text(encoding="utf-8")

# Static authority checks.
assert "class MemoryOITP(MemoryTP)" in oi_source
assert "k=1" in oi_source
assert "Do NOT create a plan" in oi_source
assert "planning module is the sole authority" in oi_source
assert "Plan from successful attempt" in original_source
assert "Devise a concise, new plan of action" in original_source
assert "def addMemory" not in oi_source, "OI-TP must inherit Original TP storage path"

# Provide minimal fake upstream modules so the intervention can be loaded without
# AgentSquare's runtime dependencies.
class FakeMemoryTP:
    def __init__(self):
        self.llm_type = "fake-model"
        self.scenario_memory = None

fake_memory_modules = types.ModuleType("memory_modules")
fake_memory_modules.MemoryTP = FakeMemoryTP
sys.modules["memory_modules"] = fake_memory_modules

calls = []
def fake_llm_response(**kwargs):
    calls.append(kwargs)
    return "fact: containers must be opened before taking objects; constraint: verify receptacle state"

fake_utils = types.ModuleType("utils")
fake_utils.llm_response = fake_llm_response
sys.modules["utils"] = fake_utils

spec = importlib.util.spec_from_file_location("memory_oi_tp_under_test", TARGET)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Collection:
    def __init__(self, count):
        self._count = count
    def count(self):
        return self._count

class Doc:
    def __init__(self, trajectory):
        self.metadata = {"task_trajectory": trajectory}

class Store:
    def __init__(self):
        self._collection = Collection(1)
        self.calls = []
    def similarity_search_with_score(self, query, k):
        self.calls.append((query, k))
        return [(Doc("successful prior trajectory"), 0.01)]

obj = object.__new__(mod.MemoryOITP)
obj.llm_type = "gpt-5.6-luna"
obj.scenario_memory = Store()

query = """You are in the kitchen.
Your task is to: dummy one >
intermediate text
Your task is to: dummy two >
You are in the living room.
Your task is to: put a mug on the desk >
"""

out = obj.retriveMemory(query)
assert obj.scenario_memory.calls == [("put a mug on the desk", 1)]
assert len(calls) == 1
assert calls[0]["model"] == "gpt-5.6-luna"
assert calls[0]["temperature"] == 0.1
prompt = calls[0]["prompt"]
assert "successful prior trajectory" in prompt
assert "put a mug on the desk" in prompt
assert "Do NOT create a plan" in prompt
assert "planning module is the sole authority" in prompt
assert out.startswith("Memory guidance from successful attempt")
assert "Plan from successful attempt" not in out

# Empty-memory behavior remains no-call / empty string.
calls.clear()
obj.scenario_memory = Store()
obj.scenario_memory._collection = Collection(0)
assert obj.retriveMemory(query) == ""
assert calls == []
assert obj.scenario_memory.calls == []

print("OI_TP_STATIC_BEHAVIOR=PASS")
