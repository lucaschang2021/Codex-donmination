# Möbius — Master Architecture v1 / 莫比乌斯总架构 v1

> Status: **Target Architecture Baseline / 终局架构基线**
>
> Historical codename: **Codex Domination**.
>
> Product identity: **Möbius / 莫比乌斯 — Operating System for AI Engineering Teams.**

---

## 1. Product Thesis / 产品命题

Möbius is a controller-first AI engineering operating system that turns capable agent runtimes into a governed, observable, auditable and continuously learning software engineering organization.

莫比乌斯不是一个“更大的聊天窗口”，也不是一个放任 Agent 自主运行的软件工厂。它负责把不同 Agent 的执行能力、Git/CI 的交付状态、机械验证证据、长期工程知识与人类最终判断连接成一个持续闭环。

Core thesis:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

Möbius is **Codex-first, not Codex-only**. OpenAI Codex is the reference runtime and first implementation target. Hermes is the first planned additional runtime. Additional runtimes may be admitted only after explicit integration research and an ADR.

---

## 2. The Five Control Planes / 五大控制平面

```text
                         Human / Controller
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────┐
│                         MÖBIUS                             │
│                                                            │
│  1. Governance Plane                                       │
│     Project / Role / Task Contract / Stage Gate / Policy    │
│                                                            │
│  2. Runtime Plane                                          │
│     CodexRuntime / HermesRuntime / FutureRuntime            │
│                                                            │
│  3. Evidence Plane                                         │
│     execution state / validation / CI / audit               │
│                                                            │
│  4. Repository Plane                                       │
│     branch / worktree / commit / push / PR / merge          │
│                                                            │
│  5. Knowledge Plane                                        │
│     project memory / lessons / research / Obsidian export   │
└────────────────────────────────────────────────────────────┘
```

These planes are intentionally separate. A runtime may execute without owning merge authority. A repository action may be automated without deciding whether it is allowed. Evidence may be collected automatically without deciding whether quality is acceptable. Knowledge may be projected to Obsidian without making Obsidian the runtime source of truth.

---

## 3. Governance Plane / 工程治理层

The Governance Plane defines the engineering organization.

### 3.1 Project Control

Each project has explicit identity and state:

```text
project_id
repository
architecture baseline
current version
current stage
roles
runtime bindings
worktree strategy
validation profile
repository policy
knowledge namespace
controller authority
```

### 3.2 Role Registry

A role is a governance identity, not a model identity.

Candidate roles:

```text
Controller
Research
Backend
Frontend
Integration
Security Review
QA
Documentation
GitHub / Release
```

Each role may bind:

```text
runtime
agent/thread identity
workspace/worktree
allowed paths
forbidden actions
allowed tools
validation profile
stage eligibility
```

### 3.3 Bounded Task Contract

Every worker task should be represented as an explicit contract:

```text
Project
Version / Stage
Role
Runtime
Objective
Frozen Scope
Non-goals
Allowed Files
Permission Boundary
Acceptance Criteria
Required Validation
Evidence Requirements
Failure Rules
Report Format
```

The worker may complete the task. It may not redefine its own scope or silently admit the next stage.

### 3.4 Stage Gate Engine

Canonical state machine:

```text
PLANNED
   ↓
ADMITTED
   ↓
IMPLEMENTING
   ↓
SUBMITTED
   ↓
REVIEWING
   ├── FIX_REQUIRED ─────→ IMPLEMENTING
   ├── BLOCKED
   └── PASS
        ↓
MERGE_AUTHORIZED
        ↓
MERGED
        ↓
CLOSED
```

Only the Controller records `PASS / FIX / BLOCK` and final merge authorization.

---

## 4. Runtime Plane / Agent Runtime 层

Möbius separates **agency** from **governance**.

```text
AgentRuntime
├── CodexRuntime      # reference implementation
├── HermesRuntime     # planned second runtime
└── FutureRuntime     # explicit admission only
```

Normalized runtime capabilities should converge toward:

```text
discover()
read_context()
attach()
dispatch()
watch()
interrupt()
collect_result()
```

The abstraction must not pretend all runtimes are identical. Capability discovery is explicit. Unsupported semantics fail deterministically rather than being emulated unsafely.

### 4.1 Codex Runtime

Codex is the first product proof because persistent thread discovery, structured read, resume, turn execution and status observation map directly to Möbius' initial control-loop requirements.

### 4.2 Hermes Runtime

Hermes is the first planned non-Codex runtime. It is intended to contribute autonomous planning/tool-use/research capabilities under the same Möbius task, evidence and stage contracts.

Hermes integration is not considered implemented until a dedicated integration research stage confirms:

- supported invocation surface;
- persistence semantics;
- task identity;
- status/event semantics;
- interrupt/recovery behavior;
- permission model;
- artifact/evidence boundaries.

### 4.3 Runtime Independence

Upper layers must not directly depend on Codex- or Hermes-specific response models. Runtime adapters normalize only the semantics Möbius actually needs.

---

## 5. Evidence Plane / 证据层

The system must distinguish **worker claims** from **mechanical evidence**.

Candidate evidence:

```text
changed files
git diff / patch metadata
test commands and results
coverage
lint
type checks
build
migrations
Docker / service health
runtime errors
CI status
PR state
contract deviations
duration / retries
terminal worker result
```

Target artifact:

```text
VALIDATION-MANIFEST.md
```

Core rule:

> **Automate evidence, not judgment.**

Evidence is assembled automatically. The Controller still evaluates architecture, security, correctness risk and stage compliance.

---

## 6. Repository Plane / Git Orchestrator

Git is a first-class state machine, not a set of incidental shell commands.

Möbius should eventually manage:

```text
repository inspection
branch creation / reuse
worktree lifecycle
role ↔ worktree binding
clean-worktree checks
commit creation
push
PR creation / update
CI observation
review-state correlation
merge authorization
merge
post-merge main/worktree synchronization
```

### 6.1 Authority Separation

```text
Agent finishes
      ↓
Evidence collected
      ↓
Commit / Push / PR may be automated
      ↓
CI observed
      ↓
Controller review
      ↓
PASS
      ↓
MergeAuthorization(pr, exact_head_sha)
      ↓
Automatic merge allowed
```

If the PR head changes after authorization, the authorization is invalid.

> **Automate Git mechanics. Preserve Git authority.**

### 6.2 Repository Invariants

- no worker may infer merge authority from “task completed”;
- destructive repository actions require explicit policy;
- dirty/unexpected workspace state blocks automation by default;
- branch/worktree identity must remain visible in evidence;
- merge authorization must bind to reviewed repository state.

---

## 7. Knowledge Plane / 长期知识层

Möbius must accumulate engineering intelligence instead of discarding stage history.

Machine-readable source-of-truth knowledge may include:

```text
ArchitectureDecision
StageRecord
ControllerDecision
FailureRecord
FixPattern
RuntimeCompatibilityFinding
EngineeringLesson
ResearchThread
ProductHypothesis
ValueThread
```

The Knowledge Plane answers a different question from Git:

- Git records **what code changed**.
- Evidence records **what was mechanically verified**.
- Knowledge records **what the organization learned**.

---

## 8. Obsidian Knowledge Projection / Obsidian 知识投影

Obsidian is a first-class human knowledge interface, but it is not Möbius' authoritative runtime database.

```text
Möbius structured knowledge
          ↓
Knowledge Projection Engine
          ↓
Obsidian-compatible Markdown
          ↓
Human reading / backlinks / annotation / research
```

Initial synchronization is one-way:

```text
Möbius → Obsidian
```

Suggested vault projection:

```text
Möbius/
├── Projects/
│   └── <project>/
│       ├── Overview.md
│       ├── Architecture/
│       ├── Stages/
│       ├── Decisions/
│       └── Failures-and-Fixes/
├── Engineering-Knowledge/
├── Runtime-Knowledge/
├── Research-Threads/
└── Value-Threads/
```

Every projected note should retain provenance such as project, stage, source evidence, commit/PR, timestamp and generating component when available.

Future bidirectional editing requires a separate ADR covering provenance, conflict resolution, trust and permissions.

---

## 9. End-to-End Möbius Loop / 完整闭环

```text
Human defines intent
      ↓
Controller selects project + stage
      ↓
Frozen architecture / task contract loaded
      ↓
Role Registry resolves runtime + exact agent identity
      ↓
Repository Plane prepares branch/worktree
      ↓
Runtime dispatches bounded task
      ↓
Execution status observed
      ↓
Evidence Plane collects validation
      ↓
Controller independently reviews
      ├── FIX   → bounded repair loop
      ├── BLOCK → stop / contract or architecture decision
      └── PASS
             ↓
      MergeAuthorization bound to exact PR state
             ↓
      Repository Plane merges + synchronizes
             ↓
      Stage closed
             ↓
      Knowledge extracted
             ↓
      Obsidian projection updated
             ↓
      Next stage may be admitted
```

This loop is the reason for the name **Möbius**: the system is designed as a continuous engineering cycle where execution, verification, delivery and learning feed the next iteration.

---

## 10. Failure Taxonomy / 故障分类

```text
F1 — Implementation defect
     → repair inside current stage

F2 — Runtime / compatibility defect
     → repair runtime adapter / compatibility layer

F3 — Contract defect
     → Controller updates technical contract / ADR

F4 — Architectural invalidation
     → stop stage, issue ADR, explicitly redesign
```

Ordinary bugs must not silently churn the master architecture.

---

## 11. Multi-Project Operating Model / 多项目运行模型

One Möbius instance may eventually govern multiple real projects while preserving separate repositories, roles, worktrees, policies and knowledge namespaces.

Example:

```text
Möbius
├── FlowTracer
│   ├── Backend → CodexRuntime
│   ├── Frontend → CodexRuntime
│   ├── Research → HermesRuntime
│   └── Security Review → HermesRuntime
├── Rasputin
└── Möbius self-hosted development
```

Möbius itself should eventually be capable of using Möbius to develop Möbius, subject to stricter self-modification gates.

---

## 12. Structured Control Surface / MCP + API

Candidate tool families:

```text
project.*
role.*
runtime.*
agent.*
task.*
evidence.*
stage.*
repo.*
knowledge.*
```

Examples:

```text
project.get_state()
role.resolve()
agent.read()
task.dispatch()
task.status()
evidence.collect()
stage.review()
repo.get_state()
repo.open_pr()
repo.get_ci()
repo.merge_authorized()
knowledge.project()
```

A generic unrestricted shell is not the product surface.

---

## 13. Security / 权限原则

1. Controller authority is explicit and auditable.
2. Worker task scope does not imply repository authority.
3. Runtime authentication/sandbox/approval models are not bypassed.
4. Control-critical targeting uses exact identities.
5. Secrets are excluded from normalized events, evidence and knowledge projection.
6. Repository writes are policy-aware and state-checked.
7. Merge authorization is state-bound and revocable by repository change.
8. Knowledge projection preserves provenance and redaction boundaries.
9. Remote/multi-user operation requires separate authenticated identities and authorization policies.
10. Self-modifying Möbius workflows require stricter-than-default review gates.

---

## 14. Version Strategy / 版本策略

Implementation remains deliberately narrower than the target architecture.

```text
v0.1  Codex discovery
v0.2  structured read
v0.3  resume / attachment
v0.4  bounded dispatch
v0.5  status
v0.6  evidence
v0.7  role + project binding
v0.8  Stage Gate
v0.9  MCP control surface
v1.0  complete Codex-first control plane
v1.1  Repository Control + workflow automation + Knowledge Projection + Hermes path
```

Target architecture does not authorize skipping gates. The current Codex foundation remains the required first proof.

---

## 15. Non-goals / 非目标

Möbius is not intended to become:

- an unrestricted autonomous software factory;
- a generic consumer chatbot;
- a hidden permission-escalation layer;
- a replacement for Git/GitHub;
- a replacement for Obsidian;
- a replacement for Codex or Hermes;
- a system where worker completion automatically equals architectural approval.

It coordinates these systems while preserving their distinct responsibilities.

---

## 16. Product Identity / 产品身份

Official name:

# **Möbius / 莫比乌斯**

Positioning:

> **Operating System for AI Engineering Teams.**

Historical origin:

> `Codex Domination` is retained only as the early project codename and architectural history.

Canonical product formula:

> **Möbius = Agent Runtime + Engineering Governance + Evidence + Repository Automation + Long-term Knowledge.**

Canonical product sentence:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**
