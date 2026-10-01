import sys, pathlib, json, hashlib, types, copy
import torch

ROOT = pathlib.Path("external/feedback_utility_hook_v2").resolve()
sys.path.insert(0, str(ROOT / "overlay"))
import transformers
import transformers.utils.import_utils as iu
iu._torchvision_available = False
sys.path.insert(0, str(ROOT))

from ouro.configuration_ouro import OuroConfig
from ouro.modeling_ouro import OuroForCausalLM

torch.manual_seed(20261002)
torch.set_grad_enabled(False)

cfg = OuroConfig(
    vocab_size=128,
    hidden_size=32,
    intermediate_size=64,
    num_hidden_layers=1,
    num_attention_heads=4,
    num_key_value_heads=4,
    max_position_embeddings=64,
    total_ut_steps=4,
    use_cache=False,
    head_dim=8,
    bos_token_id=0,
    eos_token_id=1,
    pad_token_id=0,
)
cfg._attn_implementation = "eager"
model = OuroForCausalLM(cfg).eval().cpu()
ids = torch.tensor([[2, 5, 7, 11, 13, 17, 19]], dtype=torch.long)

def tensor_digest(t):
    a = t.detach().cpu().contiguous().numpy().tobytes()
    return hashlib.sha256(a).hexdigest()

def state_digest():
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode())
        h.update(tensor_digest(v).encode())
    return h.hexdigest()

def config_digest():
    return hashlib.sha256(json.dumps(model.config.to_dict(), sort_keys=True, default=str).encode()).hexdigest()

def maxdiff(a, b):
    return float((a.detach().cpu() - b.detach().cpu()).abs().max())

state_before = state_digest()
config_before = config_digest()
cuda_before = int(torch.cuda.memory_allocated()) if torch.cuda.is_available() else 0

with torch.no_grad():
    base_out, base_hs_raw, base_gates_raw = model.model(input_ids=ids, use_cache=False)
base_hs = [x.detach().clone() for x in base_hs_raw]
base_gates = [x.detach().clone() for x in base_gates_raw]
base_last = base_out.last_hidden_state.detach().clone()

mapping = {}
for d in (2, 3):
    u = d - 1
    with torch.no_grad():
        exit_logits = model(input_ids=ids, use_cache=False, exit_at_step=u, logits_to_keep=1).logits.detach().clone()
    manual_logits = model.lm_head(base_hs[u][:, -1:, :]).detach().clone()
    correct_diff = maxdiff(exit_logits, manual_logits)
    wrong_u = d if d < 4 else None
    wrong_diff = None
    if wrong_u is not None:
        with torch.no_grad():
            wrong_logits = model(input_ids=ids, use_cache=False, exit_at_step=wrong_u, logits_to_keep=1).logits.detach().clone()
        wrong_diff = maxdiff(wrong_logits, manual_logits)
    mapping[str(d)] = {
        "scientific_depth": d,
        "runtime_index": u,
        "correct_mapping_max_abs_diff": correct_diff,
        "old_v1_mapping_max_abs_diff": wrong_diff,
    }

norm = model.model.norm
original_forward = norm.forward

def run_hook(target_depth=None, epsilon=None, sign=1):
    records_pre = []
    records_post = []
    delta_holder = {}

    def hooked_forward(self, x):
        y = original_forward(x)
        d = len(records_pre) + 1
        pre = y.detach().clone()
        records_pre.append(pre)
        if target_depth is not None and d == target_depth:
            last = y[:, -1, :]
            if epsilon is None:
                raise RuntimeError("epsilon required when target_depth is set")
            if epsilon == 0:
                delta = torch.zeros_like(last)
            else:
                gen = torch.Generator(device="cpu")
                seed = int(hashlib.sha256(f"fixture||{d}".encode()).hexdigest()[:16], 16) % (2**63 - 1)
                gen.manual_seed(seed)
                r = torch.randint(0, 2, last.shape, generator=gen, device="cpu", dtype=torch.int64)
                v = (r * 2 - 1).to(dtype=last.dtype, device=last.device)
                rms = torch.sqrt(torch.mean(last * last, dim=-1, keepdim=True))
                delta = sign * float(epsilon) * rms * v
            y = y.clone()
            y[:, -1, :] = y[:, -1, :] + delta
            delta_holder["delta"] = delta.detach().clone()
        records_post.append(y.detach().clone())
        return y

    norm.forward = types.MethodType(hooked_forward, norm)
    try:
        with torch.no_grad():
            out, hs, gates = model.model(input_ids=ids, use_cache=False)
        return (
            out.last_hidden_state.detach().clone(),
            [x.detach().clone() for x in hs],
            [x.detach().clone() for x in gates],
            records_pre,
            records_post,
            delta_holder.get("delta"),
        )
    finally:
        norm.forward = original_forward

# no-op wrapper: exact upstream path plus recording only
noop_last, noop_hs, noop_gates, _, _, _ = run_hook()
noop = {
    "last_max_abs_diff": maxdiff(noop_last, base_last),
    "hidden_max_abs_diff": max(maxdiff(a, b) for a, b in zip(noop_hs, base_hs)),
    "gate_max_abs_diff": max(maxdiff(a, b) for a, b in zip(noop_gates, base_gates)),
}

epsilon_zero = {}
perturb = {}
for d in (2, 3):
    z_last, z_hs, z_gates, z_pre, z_post, z_delta = run_hook(target_depth=d, epsilon=0.0, sign=1)
    epsilon_zero[str(d)] = {
        "last_max_abs_diff": maxdiff(z_last, base_last),
        "hidden_max_abs_diff": max(maxdiff(a, b) for a, b in zip(z_hs, base_hs)),
        "gate_max_abs_diff": max(maxdiff(a, b) for a, b in zip(z_gates, base_gates)),
        "recorded_pre_depth_max_abs_diff": maxdiff(z_pre[d-1], base_hs[d-1]),
        "delta_norm": float(torch.linalg.vector_norm(z_delta)),
    }

    signs = {}
    for sign in (+1, -1):
        p_last, p_hs, p_gates, p_pre, p_post, delta = run_hook(target_depth=d, epsilon=0.03, sign=sign)
        earlier_max = 0.0
        if d > 1:
            earlier_max = max(maxdiff(p_hs[i], base_hs[i]) for i in range(d-1))
        changed_at_d = (p_hs[d-1] - base_hs[d-1]).detach()
        nonlast_max = float(changed_at_d[:, :-1, :].abs().max()) if changed_at_d.shape[1] > 1 else 0.0
        last_delta_diff = maxdiff(changed_at_d[:, -1, :], delta)
        future = {
            str(s): maxdiff(p_hs[s-1][:, -1, :], base_hs[s-1][:, -1, :])
            for s in range(d+1, 5)
        }
        signs["plus" if sign == 1 else "minus"] = {
            "pre_depth_max_abs_diff": maxdiff(p_pre[d-1], base_hs[d-1]),
            "earlier_hidden_max_abs_diff": earlier_max,
            "target_nonlast_change_max_abs": nonlast_max,
            "target_last_change_vs_delta_max_abs_diff": last_delta_diff,
            "delta_norm": float(torch.linalg.vector_norm(delta)),
            "future_last_token_max_abs_diff_by_depth": future,
            "future_effect_nonzero": any(v > 1e-8 for v in future.values()),
        }
    perturb[str(d)] = signs

state_after = state_digest()
config_after = config_digest()
cuda_after = int(torch.cuda.memory_allocated()) if torch.cuda.is_available() else 0

tol = 1e-5
checks = {
    "upstream_hidden_count_4": len(base_hs) == 4,
    "upstream_gate_count_4": len(base_gates) == 4,
    "correct_mapping_d2": mapping["2"]["correct_mapping_max_abs_diff"] <= tol,
    "correct_mapping_d3": mapping["3"]["correct_mapping_max_abs_diff"] <= tol,
    "noop_identity": max(noop.values()) <= tol,
    "epsilon0_d2_identity": max(epsilon_zero["2"]["last_max_abs_diff"], epsilon_zero["2"]["hidden_max_abs_diff"], epsilon_zero["2"]["gate_max_abs_diff"]) <= tol,
    "epsilon0_d3_identity": max(epsilon_zero["3"]["last_max_abs_diff"], epsilon_zero["3"]["hidden_max_abs_diff"], epsilon_zero["3"]["gate_max_abs_diff"]) <= tol,
    "plusminus_d2_locality_and_future": all(
        x["pre_depth_max_abs_diff"] <= tol
        and x["earlier_hidden_max_abs_diff"] <= tol
        and x["target_nonlast_change_max_abs"] <= tol
        and x["target_last_change_vs_delta_max_abs_diff"] <= tol
        and x["future_effect_nonzero"]
        for x in perturb["2"].values()
    ),
    "plusminus_d3_locality_and_future": all(
        x["pre_depth_max_abs_diff"] <= tol
        and x["earlier_hidden_max_abs_diff"] <= tol
        and x["target_nonlast_change_max_abs"] <= tol
        and x["target_last_change_vs_delta_max_abs_diff"] <= tol
        and x["future_effect_nonzero"]
        for x in perturb["3"].values()
    ),
    "weights_unchanged": state_before == state_after,
    "config_unchanged": config_before == config_after,
    "no_cuda_allocation": cuda_before == 0 and cuda_after == 0,
}
report = {
    "fixture": {
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "device": "cpu",
        "seed": 20261002,
        "config": {
            "vocab_size": 128,
            "hidden_size": 32,
            "intermediate_size": 64,
            "num_hidden_layers": 1,
            "num_attention_heads": 4,
            "num_key_value_heads": 4,
            "total_ut_steps": 4,
            "use_cache": False,
        },
    },
    "mapping": mapping,
    "noop": noop,
    "epsilon_zero": epsilon_zero,
    "perturbation": perturb,
    "state_digest_before": state_before,
    "state_digest_after": state_after,
    "config_digest_before": config_before,
    "config_digest_after": config_after,
    "cuda_memory_before": cuda_before,
    "cuda_memory_after": cuda_after,
    "checks": checks,
    "all_pass": all(checks.values()),
}
path = ROOT / "hook_preflight_report.json"
path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
if not report["all_pass"]:
    raise SystemExit(31)
