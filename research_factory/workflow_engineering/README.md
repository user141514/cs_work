# WFE-02：离线执行准入与结果提交检查器

## 当前状态

实现的是一个独立的、无模型的检查器，不是完整工作流平台，也不是操作系统沙箱。WFE-03.1 后的活跃目录为 `D:/cs_work/research_factory/workflow_engineering/`；`D:/bio_paper` 中的旧副本仅保留为历史来源。

验证已经覆盖两类环境：独立 Linux / Python 3.13.5，以及 PC2 原生 Windows 10 / Python 3.7.0。WFE-04 后 PC2 完整套件为 74/74 通过、0 skip。除原有准入/SQLite/junction 检查外，新增了 lease 复验和真实 Stage-B launcher 的 model-free dry-run adapter。真实执行器仍未 live 接入。

## 重跑全部离线测试

在本目录执行：

```sh
python -B verify_offline.py --output-dir verification_local
```

或只运行完整检查器测试集：

```sh
python -B -m unittest discover -s tests -v
```

不安装依赖，不联网、不运行模型、不调用任何历史实验启动脚本。测试使用临时工作目录与 SQLite 数据库；验证器只将报告写入指定的输出目录。验证器在整套测试期间将 `socket.socket.connect` 和 `subprocess.Popen` 设为拒绝调用，检查器本身不含网络或模型客户端。它不是对其他进程的网络防火墙。

## WFE-04：dry-run executor adapter

`executor_adapter.py` 只做：重新验证 RUNNING lease → 锁定真实 `run_stageb_agent.ps1` 哈希 → 校验 prompt 属于冻结 read scope → 生成结构化 PowerShell argv → 暴露未来 receipt 字段和 live 前置条件。它没有启动原语，`would_launch` 永远为 false。

真实 PC2 dry-run 发现当前历史 launcher 会写 `D:/stageb_agent_runtime/{arms,venvs}` 与 `D:/cs_work/external/spec_stageb_logs`，不在当前 lease 的 session/write scope 内，因此 `live_ready=false`。另有 `atomic_dispatch_claim`、`executor_parameters_not_frozen_in_gate` 和 `executor_path_ownership` 三个剩余 enforcement gap。详见 `WFE04_RESULT.md`。

## 最小执行链

```text
受信协调者冻结 contract.json
    → Gate.initialize：绑定本轮唯一 task/plan/workflow/step/run
    → admit：核身份、依赖、路径、冲突、预算；持久化预约
    → 调用方执行已获准的工作（检查器自己不派发）
    → submit：重读契约与文件；核对输入、产物、哈希和用量
    → finish：记录 KEEP / MODIFY / TERMINATE，写下一步，STOPPED
```

`finish` 不运行下一步，`next_step.authorized` 固定为 false。停止后的同一个数据库不能重新启动、重复提交或重置预算。新步骤需要协调者重新获得明确授权、建立新的运行契约，并保留旧数据库。

契约文件与状态目录必须位于 worker 工作区之外，由协调者维护。`authorized: true` 是受信协调者写入的授权记录，不是用户身份认证、数字签名或防篡改权限系统。

## API 与命令行

```python
from offline_gate import Gate, GateError

gate = Gate.initialize(contract_path, state_dir)
lease = gate.admit(request)
# 只有拿到 lease，受控适配器才允许执行该单元；本轮只有测试假 worker。
accepted = gate.submit(receipt)
state = gate.finish(finish_request)
assert state["phase"] == "STOPPED"
```

命令行接受 JSON 文件，成功退出码为 0，拒绝为 2，并输出 JSON：

```sh
python offline_gate.py init --contract contract.json --state-dir control/run1
python offline_gate.py admit --state-dir control/run1 --request admission.json
python offline_gate.py submit --state-dir control/run1 --request receipt.json
python offline_gate.py finish --state-dir control/run1 --request finish.json
python offline_gate.py status --state-dir control/run1
```

完整可运行的契约、请求、假 worker 和回执实例位于 `tests/test_offline_gate.py` 的 `GateTests.setUp/unit/request/receipt/finish_request`。不是依赖真实会话或外部数据的伪代码。

## 固定的接口

- **身份**：task_id/task_version、workflow_id/workflow_version、plan_id/plan_version、step_id、run_id；每次请求必须精确匹配，版本不能用布尔值冒充整数。
- **任务契约**：目标、验收、停止条件、初始输入清单及哈希、评价文件及哈希、工作区、保护路径、预算、工作单元与依赖。
- **单元**：depends_on、reads、writes、required_artifacts、actions、reservation。只允许 offline_read/offline_test/offline_write；模型调用与 token 预算必须为零。
- **回执**：身份、unit_id、attempt_id、执行状态、上报结论、完整产物清单和 SHA256、上报用量。文件存在与哈希只代表结构有效，不代表科学正确。

资源预算是整数；全步骤上限与单元预约在 SQLite `BEGIN IMMEDIATE` 事务中一起校验和更新。最多两个 RUNNING 单元，冲突的读写集合不能同时准入。失败尝试不会退还预约，避免失败后无成本重试。`reported_usage` 明确是适配器/回执上报值，不是独立计量；真实接入后必须由可信执行器提供计量。

## 已测试的拒绝边界

缺失/过期身份、未授权步骤或动作、依赖环、未知/未声明依赖、前置结果未验收、冻结输入或评价被改、读写冲突、目录包含关系、跨工作区路径、符号链接逃逸/重定向、预存旧产物、缺失/篡改产物、硬链接伪装独立产物、失败执行冒充科学负例、超预算、重复准入/回执、停止后重启、给下一步自行授权。

合法独立工作可以同时准入；存在真实依赖的工作在前置回执通过后可以继续。两条并发冲突请求只放行一条，重开 Gate 对象不会清空已记录状态。

## 结论维度不能混淆

- `status=ACCEPTED` + `evidence_status=STRUCTURALLY_VALID`：产物结构/来源校验通过。
- `status=INVALID`：执行、输入或证据契约不合法，不能用作科学反例。
- `reported_conclusion`：仅保存 worker 的原始声明。
- `scientific_conclusion=UNASSESSED`：本检查器始终不代替领域评价器判断科学成败。

契约变化后允许显式 MODIFY/TERMINATE 收尾，并记录 `closure_validation_error`，但不允许 KEEP 接受已经失效的证据。存在 RUNNING 单元时不能悄悄收尾；必须先收取执行结果。未提供进程取消/超时回收器。

## 边界与后续真实接入前提

1. 本实现只约束经过它的请求。直接 shell/MCP、worker 未声明的文件/服务访问、修改控制数据库等行为尚未被 OS 权限隔离阻断。
2. 路径检查是检查时刻的校验，不是消除文件系统 TOCTOU 的证明。Windows junction 与 SQLite 的本机已覆盖上述离线验收，但 ACL、跨进程权限隔离和检查后路径/文件被竞态替换仍不是本检查器的证明范围。
3. 真实适配器需要完整提取会话与工具路径、独立计量、绑定 lease 到真正的 launch、隔离输出与权限、处理取消/进程崩溃；跨运行去重和总预算也由协调者负责。本轮没有实现这些功能。
4. 不自动重试、不自动搜索、不自动启动下一步。预算预约保守、不退款；有助于拒绝越权，不证明执行效率最佳。
5. 历史错误工作区 fixture 是根据记录制作的最小开发反例，文件中的臂名称为示意，既不是历史原会话，也不是同任务 A/B 回放结果。

唯一后续步骤由 MASTER_PLAN.md 决定；WFE-03.1 的迁移结果记录在 WFE03_1_RESULT.md。本代码不自动推进。
