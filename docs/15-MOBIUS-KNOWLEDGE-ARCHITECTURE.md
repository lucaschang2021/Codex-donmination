# Möbius — Naming & Knowledge Architecture / 命名与知识架构

> Status: Architecture Amendment / 架构修正案
>
> This document formally names the product **Möbius / 莫比乌斯** and adds a first-class human knowledge layer centered on Obsidian-compatible knowledge projection.

---

## 1. Official Product Name / 正式产品名

**Möbius / 莫比乌斯** is the official product name.

The existing repository name `Codex-domination` and the historical term **Codex Domination** are retained as the project's origin/legacy identifier during migration, but the product is no longer conceptually limited to Codex.

Official positioning:

> **Möbius — Operating System for AI Engineering Teams.**
>
> **莫比乌斯：AI 软件工程团队操作系统。**

Architecture principle:

> **Codex-first, not Codex-only. Controller-first, automation-driven.**

---

## 2. Why Möbius / 为什么是莫比乌斯

The Möbius name represents the intended continuous engineering loop:

```text
Requirement
   ↓
Architecture / Contract
   ↓
Role + Runtime
   ↓
Execution
   ↓
Evidence
   ↓
Controller Review
   ↓
Git / CI / Merge
   ↓
Knowledge Projection
   ↓
Learning / Next Decision
   └──────────────────────→ next Requirement / Stage
```

The system is designed as a continuous governed loop rather than a sequence of isolated AI prompts.

---

## 3. Five-Layer Product Model / 五层产品模型

Möbius is composed of five major layers:

```text
1. Agent Runtime Layer
   CodexRuntime / HermesRuntime / future runtimes

2. Engineering Governance Layer
   Project Control / Role Registry / Task Contracts / Stage Gate / Policy

3. Evidence & Repository Layer
   Evidence Engine / Git Orchestrator / CI / PR / Merge Authorization / Audit

4. Knowledge & Memory Layer
   Structured project memory / architecture decisions / stage outcomes / failure knowledge

5. Human Knowledge Interface
   Obsidian-compatible knowledge projection / Markdown / backlinks / research & value threads
```

Short form:

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**

---

## 4. Obsidian Is a First-Class Human Knowledge Layer / Obsidian 是一等人类知识层

Obsidian is not the runtime database and must not become a hidden execution dependency.

Möbius keeps machine-readable orchestration state in its own structured storage. Obsidian acts as the human-facing **Knowledge Projection / Human Knowledge Interface**.

This preserves both goals:

- machines operate on deterministic structured state;
- humans receive durable, navigable, editable knowledge.

### Knowledge categories

Möbius should eventually project at least four categories into Obsidian-compatible Markdown:

#### A. Project Memory

- architecture decisions / ADRs
- version and stage completion records
- Controller PASS / FIX / BLOCK decisions
- merge/release records
- important implementation constraints

#### B. Engineering Knowledge

- recurring failure patterns
- runtime compatibility findings
- debugging notes
- reusable fixes
- testing patterns
- Git/worktree lessons
- security/reliability lessons

#### C. Research & Value Threads

- technical theses
- product hypotheses
- architectural trade-offs
- research questions
- strategic/value threads that emerge across projects

#### D. Human Workspace

- summaries intended for reading rather than execution
- backlinks between projects, decisions and concepts
- personal annotations
- follow-up questions
- long-term knowledge development

---

## 5. Source-of-Truth Boundary / 真值源边界

Möbius follows a strict separation:

```text
Machine Source of Truth
        │
        ├── Project state
        ├── Stage state
        ├── Role bindings
        ├── Task state
        ├── Evidence
        ├── Git/PR/CI state
        └── Audit records
        │
        ▼
Knowledge Projection Engine
        │
        ▼
Obsidian-compatible Markdown
        │
        ▼
Human reading / linking / annotation
```

Obsidian is therefore **not** required for task dispatch, Stage Gate decisions, CI evaluation or merge authorization.

The default synchronization direction is one-way:

```text
Möbius → Obsidian
```

A future bidirectional Agent Context feature may be admitted only after a separate permission, provenance and conflict-resolution design.

---

## 6. Knowledge Projection Engine / 知识投影引擎

Planned components:

```text
KnowledgeProjector
├── ProjectMemoryExporter
├── StageRecordExporter
├── ADRExporter
├── FailureKnowledgeExporter
├── ResearchThreadExporter
└── MarkdownExporter
```

Candidate output structure:

```text
Möbius Vault/
├── Projects/
│   ├── FlowTracer/
│   ├── Möbius/
│   └── Rasputin/
├── Architecture/
├── ADR/
├── Stages/
├── Failures/
├── Engineering-Knowledge/
├── Research/
├── Value-Threads/
└── Indexes/
```

Each generated note should carry provenance metadata such as:

```yaml
project: FlowTracer
stage: BE-7
source_type: controller_decision
runtime: codex
commit: <sha>
pr: <number>
created_at: <timestamp>
managed_by: mobius
```

Generated sections must be clearly distinguishable from user-authored annotations if future synchronization becomes bidirectional.

---

## 7. Unified Möbius Architecture / 统一莫比乌斯架构

```text
                         Human / Controller
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────┐
│                       MÖBIUS                             │
│                                                          │
│ Project Control   Role Registry   Task Contracts         │
│ Stage Gate        Policy          Audit                  │
│ Evidence Engine   Repository Control                     │
│ Knowledge Memory  Knowledge Projection                   │
└───────────────┬───────────────────┬──────────────────────┘
                │                   │
                │                   └──────────────→ Obsidian
                │                                  Human Knowledge
                ▼
         Agent Runtime Layer
        ┌────────┼─────────┐
        ▼        ▼         ▼
      Codex    Hermes    Future
        │        │
        └────┬───┘
             ▼
      Execution / Tools
             │
             ▼
      Git / Worktrees / CI
             │
             ▼
        PR / Merge State
             │
             └────────→ Evidence → Controller Gate
```

---

## 8. Runtime Strategy / Runtime 策略

Möbius remains **Codex-first** during implementation.

- `CodexRuntime` is the reference implementation and first production proof.
- `HermesRuntime` is the first planned additional runtime.
- Future runtimes must implement a narrow `AgentRuntime` interface and pass an explicit integration/ADR gate.

The upper governance system must not depend on runtime-specific concepts unless they are normalized at the adapter boundary.

Candidate interface:

```text
AgentRuntime
- discover()
- read_context()
- attach()
- dispatch()
- watch()
- interrupt()
- collect_result()
```

---

## 9. Repository Strategy / Git 与仓库策略

Repository Control remains a first-class subsystem:

```text
inspect repository
→ prepare branch/worktree
→ bind workspace to role
→ execute bounded task
→ collect evidence
→ commit/push/open PR
→ observe CI
→ Controller PASS/FIX/BLOCK
→ state-bound merge authorization
→ merge
→ synchronize repository state
→ project knowledge projection
```

The merge authorization must remain bound to an exact reviewed state such as the PR head SHA. Any later mutation invalidates the authorization.

---

## 10. Knowledge-Aware Completion Loop / 知识化闭环

A stage is not merely code-complete. The long-term Möbius loop should preserve useful institutional knowledge:

```text
Stage completes
   ↓
Evidence finalized
   ↓
Controller decision recorded
   ↓
Repository state finalized
   ↓
Knowledge extraction
   ↓
Project Memory + Engineering Knowledge + Research/Value Threads
   ↓
Obsidian projection
   ↓
Next stage can reuse proven knowledge
```

This turns execution history into cumulative engineering memory rather than disposable chat history.

---

## 11. Scope Discipline / 范围纪律

This amendment changes the **target architecture and product identity**, not the current implementation gate.

Current engineering order remains:

```text
prove Codex v0.1 runtime loop
→ read/resume/dispatch/status
→ evidence
→ roles/stage gate
→ MCP
→ repository automation
→ knowledge projection
→ Hermes/multi-runtime expansion
```

Obsidian and Hermes must not delay the first reliable Codex control-loop proof.

---

## 12. Final Product Thesis / 最终产品命题

Möbius is not merely an agent orchestrator and not merely a Git automation tool.

It is a governed operating system for AI engineering teams that combines:

```text
Agency
+ Governance
+ Evidence
+ Repository Automation
+ Long-term Knowledge
```

The system should make complex AI-assisted engineering feel continuous, auditable and cumulative.

> **Agents execute. Git records. Evidence proves. Obsidian remembers. Möbius governs.**
