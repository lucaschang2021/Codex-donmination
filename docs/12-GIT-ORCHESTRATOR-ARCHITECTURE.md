# Codex Domination — Git Orchestrator / Repository Control Plane

> Status: Architecture extension for the v0.1 → v1.1 roadmap. Git automation is a first-class part of the final Codex Domination control plane, but repository authority remains governed by Controller-approved policy.

## 1. Product Goal / 产品目标

Codex Domination should remove the repetitive Git and GitHub mechanics that currently sit between AI implementation and Controller review.

The user should not need to manually create branches, remember worktree paths, stage files, compose commits, push branches, open pull requests, watch CI, synchronize branches, or perform routine repository bookkeeping.

The target experience is:

```text
Controller admits a stage
        ↓
Codex Domination prepares repository workspace
        ↓
Worker Codex implements inside its assigned worktree/branch
        ↓
Repository evidence is collected automatically
        ↓
Controller reviews
        ↓
PASS → explicit merge authorization
        ↓
Git Orchestrator performs the authorized merge operation
        ↓
Repository/worktree state is synchronized
        ↓
Next stage may be admitted
```

The core principle is:

> Automate Git mechanics; preserve Git authority.

---

## 2. Architectural Position / 架构位置

The final control plane becomes:

```text
Human / Controller
        ↓
MCP / Control Surface
        ↓
Stage & Policy Engine
        ↓
Codex Domination Core
 ┌────────────┬──────────────┬──────────────┐
 │ Role       │ Task/Status  │ Evidence     │
 │ Registry   │ Engine       │ Engine       │
 └────────────┴──────────────┴──────────────┘
        ↓
Repository Control Plane / Git Orchestrator
        ↓
Git + Worktrees + GitHub + CI
        ↓
Persistent Codex Workers
```

Git Orchestrator is not a separate autonomous agent. It is a policy-controlled subsystem of Codex Domination.

---

## 3. Responsibilities / 职责

### 3.1 Repository discovery

- detect repository root
- identify default branch
- inspect current branch and HEAD
- inspect remotes
- detect dirty working tree
- enumerate worktrees
- map worktrees to roles/projects
- surface detached HEAD or invalid repository states

### 3.2 Branch lifecycle

Codex Domination may, under stage policy:

- create stage branch
- verify branch base
- update branch from approved base
- prevent accidental work on `main`
- detect divergence/conflict risk
- archive/delete completed local branches when policy allows

Suggested naming convention:

```text
feat/<stage>-<slug>
fix/<stage>-<slug>
docs/<slug>
ops/<slug>
```

### 3.3 Worktree lifecycle

For role-separated workflows:

- create/reuse role worktrees
- bind exact worktree path to Role Registry
- verify worker is operating inside the assigned path
- block cross-role directory confusion
- synchronize worktrees after approved merges
- detect stale/locked/orphaned worktrees

A role binding may look like:

```text
Project: FlowTracer
Role: Backend
Branch: feat/be-4
Worktree: D:/FlowTracer-wt/backend
Thread: <concrete Codex thread id>
```

### 3.4 Change tracking

Automatically collect:

- `git status --porcelain`
- changed files
- staged/unstaged/untracked classification
- `git diff --stat`
- patch/diff metadata
- commits created during the stage
- base/head SHAs
- unexpected files outside allowed scope

This feeds the Evidence Engine.

### 3.5 Commit preparation

Codex Domination may prepare and perform commits when stage policy explicitly allows it.

Commit creation must be based on:

- known project
- known stage
- known role
- allowed file scope
- validation status
- deterministic commit message template

Example:

```text
feat(be-4): implement radar scheduling contract
```

Worker agents must not silently rewrite unrelated history.

### 3.6 Push / remote synchronization

Automatable operations:

- push approved feature branch
- set upstream on first push
- fetch remote refs
- detect remote divergence
- surface rejected/non-fast-forward pushes

Unsafe defaults:

- no force push to protected branches
- no credential manipulation
- no silent remote replacement

### 3.7 Pull request lifecycle

Codex Domination can eventually:

- open PR from stage branch
- generate PR body from task contract + evidence manifest
- attach issue/stage references
- update PR after repair cycles
- read CI/check status
- collect review comments
- synchronize Controller decision with stage state

PR creation is a mechanical operation and may be automated by policy.

PR approval/merge remains authority-sensitive.

### 3.8 CI integration

Repository Control Plane should normalize:

```text
PENDING
RUNNING
PASS
FAIL
CANCELLED
TIMED_OUT
UNKNOWN
```

It may collect:

- workflow name
- run ID
- job/step summaries
- failed logs
- artifact references
- commit SHA associated with the run

CI outcomes become evidence, not final architectural judgment.

### 3.9 Merge execution

Merge is split into two concepts:

1. **Merge authorization** — Controller decision.
2. **Merge execution** — Git Orchestrator mechanical action.

The Git Orchestrator MUST NOT infer authorization from:

- worker saying "done"
- tests passing
- CI passing
- PR being mergeable
- absence of review comments

Required state:

```text
Stage = PASS
AND
MergeAuthorization = explicit + current
AND
AuthorizedHeadSHA = actual PR head SHA
```

Only then may the system perform the configured merge method.

If the head SHA changes after authorization, authorization becomes stale and merge must be blocked until Controller revalidates.

---

## 4. Proposed Internal Components / 内部模块

```text
repository/
├── repository_registry.py
├── git_adapter.py
├── branch_manager.py
├── worktree_manager.py
├── change_inspector.py
├── commit_manager.py
├── remote_manager.py
├── pr_manager.py
├── ci_watcher.py
├── merge_authorizer.py
└── models.py
```

### RepositoryRegistry
Maps project identity to repository root, remote, default branch and role worktrees.

### GitAdapter
Narrow execution boundary around Git. No arbitrary shell API should leak to higher layers.

### BranchManager
Creates, validates and synchronizes stage branches.

### WorktreeManager
Creates/reuses/synchronizes role worktrees.

### ChangeInspector
Produces deterministic repository evidence.

### CommitManager
Creates policy-compliant commits.

### RemoteManager
Fetches/pushes approved refs and detects divergence.

### PullRequestManager
Coordinates GitHub PR lifecycle through a provider adapter.

### CIWatcher
Normalizes CI status and failed evidence.

### MergeAuthorizer
Stores/checks explicit Controller merge authorization and head SHA binding.

---

## 5. Core Data Models / 核心数据模型

### RepositoryProfile

```text
project_id
repository_root
remote_name
remote_url
default_branch
provider
role_worktrees
```

### WorkspaceBinding

```text
project_id
stage_id
role_id
thread_id
branch
worktree_path
base_sha
```

### RepositorySnapshot

```text
head_sha
branch
clean
ahead
behind
changed_files
staged_files
unstaged_files
untracked_files
```

### PullRequestState

```text
number
url
base
head
head_sha
draft
mergeable
ci_state
review_state
```

### MergeAuthorization

```text
authorization_id
project_id
stage_id
pr_number
authorized_head_sha
authorized_by
authorized_at
merge_method
consumed
```

Authorization is single-use and invalidated by head movement.

---

## 6. Automation Levels / 自动化等级

Git automation should be progressive rather than all-or-nothing.

### G0 — Observe

Read-only repository status and worktree discovery.

### G1 — Prepare

Create/reuse branch and worktree from a frozen stage contract.

### G2 — Record

Stage/commit validated worker changes and collect evidence.

### G3 — Publish

Push feature branch, create/update PR, watch CI.

### G4 — Execute Authorized Merge

After explicit Controller authorization, perform merge and synchronize worktrees.

### G5 — Repository Housekeeping

Clean stale branches/worktrees, archive stage metadata, prepare next stage.

No level grants autonomous architectural approval.

---

## 7. Final Happy Path / 最终理想路径

The intended v1.x user experience is:

```text
User: "Continue FlowTracer."

Controller / Stage Engine
→ detects current stage BE-4
→ verifies BE-4 admission

Git Orchestrator
→ creates/reuses feat/be-4
→ binds Backend worktree
→ confirms clean base

Role Registry
→ resolves Backend Codex thread

Task Engine
→ generates bounded task packet
→ dispatches task

Worker Codex
→ implements changes

Evidence + Git Orchestrator
→ inspect diff
→ run validation
→ create commit
→ push branch
→ open/update PR
→ watch CI

Controller
→ independent review
→ FIX or PASS

If FIX:
→ repair packet returns to same worker
→ new commit/push/CI
→ evidence regenerated
→ Controller reviews again

If PASS:
→ Controller issues merge authorization bound to exact head SHA
→ Git Orchestrator merges
→ syncs main and worktrees
→ archives stage evidence
→ Stage Engine admits next stage
```

The human no longer performs normal Git choreography.

---

## 8. Failure Handling / 故障处理

### Dirty worktree

BLOCK destructive transition. Preserve user changes and report exact files.

### Wrong branch/worktree

BLOCK task dispatch until binding is corrected.

### Merge conflict

Classify as repository repair work. Create a bounded repair task; never resolve silently when semantic judgment is required.

### CI failure

Collect failing evidence and return a repair packet to the responsible role.

### Non-fast-forward push

Do not force by default. Fetch, classify divergence, and require a safe repair path.

### Stale merge authorization

If PR head SHA differs from authorized SHA, invalidate authorization automatically.

### GitHub/provider outage

Preserve local repository state and stage state; retry only idempotent operations.

---

## 9. Security & Safety Invariants / 安全不变量

- no force push to protected branch by default
- no automatic credential creation or export
- no arbitrary remote mutation
- no silent destructive reset/clean
- no branch deletion while unmerged work exists
- no merge without explicit authorization
- merge authorization bound to exact head SHA
- all repository mutations logged in Audit Store
- worker role permissions scoped to project/stage/worktree
- Git adapter exposes typed operations rather than unrestricted shell execution

---

## 10. Roadmap Placement / 版本路线定位

Repository control should be introduced incrementally across the existing roadmap:

- **v0.6 Evidence Layer**: read-only Git evidence (`status`, diff summary, SHAs).
- **v0.7 Role Registry**: bind roles to repositories, branches and worktrees.
- **v0.8 Stage Gate Engine**: stage-specific repository policy and workspace admission.
- **v0.9 MCP**: expose narrow read-only repository/status primitives where needed.
- **v1.0**: integrate branch/worktree validation and repository evidence into the full Controller-first workflow.
- **v1.1**: enable Git automation levels G1–G4: workspace preparation, commit/push/PR/CI, and Controller-authorized merge execution.

A future v1.2+ may add richer provider abstraction or team/shared-repository policy, but this is not required for the v1.1 architecture baseline.

---

## 11. Product Principle / 产品原则

The final experience should not be "AI can run Git commands".

It should be:

> The engineering workflow owns the repository lifecycle, and Git becomes an invisible, auditable execution layer underneath it.

Users should think in projects, stages, roles, evidence and decisions — not in repetitive branch/worktree/PR mechanics.
