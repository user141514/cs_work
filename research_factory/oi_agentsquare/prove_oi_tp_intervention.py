import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UP = ROOT / "upstream" / "runtime"
ORIG = ROOT / "arms" / "original"
OI = ROOT / "arms" / "oi_tp"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# Original arm must be byte-identical to frozen runtime.
for p in sorted(UP.rglob("*")):
    if p.is_file():
        rel = p.relative_to(UP)
        assert sha(p) == sha(ORIG / rel), rel

# OI arm must be byte-identical except the two explicitly authorized files.
changed = []
for p in sorted(UP.rglob("*")):
    if p.is_file():
        rel = p.relative_to(UP)
        if sha(p) != sha(OI / rel):
            changed.append(rel.as_posix())
assert changed == ["memory_modules.py", "module_map.py"], changed

src = (OI / "memory_modules.py").read_text(encoding="utf-8")
tree = ast.parse(src)

def source_method(text, class_name, method_name):
    class_anchor = "class %s" % class_name
    class_start = text.index(class_anchor)
    next_class = text.find("\nclass ", class_start + len(class_anchor))
    class_end = len(text) if next_class < 0 else next_class
    class_text = text[class_start:class_end]
    method_anchor = "    def %s" % method_name
    method_start_local = class_text.index(method_anchor)
    next_method = class_text.find("\n    def ", method_start_local + len(method_anchor))
    method_end_local = len(class_text) if next_method < 0 else next_method
    return class_text[method_start_local:method_end_local]

classes = {n.name:n for n in tree.body if isinstance(n, ast.ClassDef)}
assert "MemoryTP" in classes
assert "MemoryTPOrthogonalized" in classes
oi_cls = classes["MemoryTPOrthogonalized"]
assert any(isinstance(b, ast.Name) and b.id == "MemoryTP" for b in oi_cls.bases)

methods = {n.name:n for n in oi_cls.body if isinstance(n, ast.FunctionDef)}
assert set(methods) == {"retriveMemory"}, set(methods)
method_text = source_method(src, "MemoryTPOrthogonalized", "retriveMemory")
assert method_text

# Frozen intervention properties.
assert "similarity_search_with_score(" in method_text
assert "task_name, k=1" in method_text
assert method_text.count("llm_response(") == 1
assert "temperature=0.1" in method_text
assert "Guidance from successful attempt" in method_text
assert "DO NOT produce a plan" in method_text
assert "planning module remains solely responsible" in method_text
assert "Plan from successful attempt" not in method_text
assert "Devise a concise, new plan of action" not in method_text

# addMemory/storage remains inherited from original TP.
assert "addMemory" not in methods
assert "super().__init__" not in method_text

orig_src = (ORIG / "memory_modules.py").read_text(encoding="utf-8")
orig_tree = ast.parse(orig_src)
orig_classes = {n.name:n for n in orig_tree.body if isinstance(n, ast.ClassDef)}
orig_tp = orig_classes["MemoryTP"]
orig_methods = {n.name:n for n in orig_tp.body if isinstance(n, ast.FunctionDef)}
orig_retrieve_text = source_method(orig_src, "MemoryTP", "retriveMemory")

# Both variants retain the same top-k and one memory-side model call in source.
assert "task_name, k=1" in orig_retrieve_text
assert orig_retrieve_text.count("llm_response(") == 1
assert method_text.count("llm_response(") == orig_retrieve_text.count("llm_response(")

result = {
    "changed_files": changed,
    "original_runtime_byte_identical": True,
    "retrieval_k": 1,
    "original_memory_llm_calls_per_retrieved_result": 1,
    "oi_memory_llm_calls_per_retrieved_result": 1,
    "storage_addMemory_inherited_unchanged": True,
    "original_output_authority": "current-task plan",
    "oi_output_authority": "bounded non-authoritative guidance",
    "fixed_agent_config": {
        "planning": "IO",
        "reasoning": "IO",
        "tooluse": "None",
        "memory_original": "TP",
        "memory_oi": "TP-OI"
    },
    "model_condition": "GPT-5.6 Luna / medium / Codex"
}
(ROOT / "OI_AS_02_INTERVENTION_PROOF.json").write_text(
    json.dumps(result, indent=2, sort_keys=True), encoding="utf-8"
)
print(json.dumps(result, indent=2, sort_keys=True))
