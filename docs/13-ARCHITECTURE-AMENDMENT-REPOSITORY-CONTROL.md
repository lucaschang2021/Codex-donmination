# Codex Domination — Architecture Amendment: Repository Control Plane

> Status: **Master Architecture Amendment / 总架构修正案**
>
> Authority: this document is part of the Codex Domination architecture baseline. Where older planning text describes Git/GitHub orchestration only as an unspecified future capability, this amendment provides the current intended direction. It does **not** change the frozen v0.1 implementation scope.

---

## 1. Decision / 决策

Codex Domination will contain two coordinated control planes:

```text
Human / Controller
        │
        ▼
┌──────────────────────────────────────────────┐
│          Codex Domination Core               │
├──────────────────────┬───────────────────────┤
│ Agent Control Plane  │ Repository Control    │
│                      │ Plane                 │
│ threads              │ repositories          │
│ roles                │ branches              │
│ tasks                │ worktrees             │
│ status               │ commits               │
│ evidence             │ pull requests         │
│ stage gates          │ CI/checks             │
│ repair routing       │ merge/sync            │
└──────────────────────┴───────────────────────┘
        │                         │
        ▼                         ▼
 Official Codex Runtime       Git + GitHub
```

The Repository Control Plane is a first-class architectural subsystem, not a collection of convenience shell commands.

Codex Domination 的 Repository Control Plane 是一等架构模块，而不是若干 Git 命令的简单封装。

---

## 2. Product Outcome / 产品结果

The intended user experience is that normal development does not require routine manual Git administration.

A Controller should be able to admit a stage and allow Codex Domination to prepare and maintain the repository mechanics around that stage:

```text
Stage admitted
  → resolve project repository
  → resolve/create branch
  → resolve/create role worktree
  → verify clean/safe workspace
  → dispatch bounded Codex task
  → collect diff + validation evidence
  → create bounded commit
  → push branch
  → create/update pull request
  → observe CI/checks
  → Controller independently reviews
  → PASS / FIX / BLOCK
```

If `FIX`, the same branch/worktree is reused and the repair loop continues.

If `PASS`, the Controller may issue a merge authorization. Only then may Codex Domination perform the merge and post-merge synchronization allowed by policy.

---

## 3. Architectural Invariant / 核心不变量

> **Automate Git mechanics; preserve merge authority.**
>
> **自动化 Git 的机械操作，但保留最终合并授权。**

Repository automation must never convert any of the following into merge authority by itself:

- worker says “done”;
- tests pass;
- CI is green;
- task reaches `COMPLETED`;
- evidence manifest is complete;
- PR is mergeable.

A merge requires an explicit Controller decision recorded against a concrete repository state.

---

## 4. Core Modules / 核心模块

### 4.1 Repository Registry

Maps a project identity to repository metadata:

- local repository root;
- remote repository identity;
- default branch;
- branch naming policy;
- worktree root;
- permitted remote operations;
- GitHub repository binding where configured.

### 4.2 Branch Manager

Responsibilities:

- inspect current branch state;
- create bounded stage/feature branches;
- prevent accidental work on protected branches;
- validate base revision before work begins;
- detect branch divergence.

### 4.3 Worktree Manager

Responsibilities:

- create/reuse role-specific worktrees;
- bind roles to deterministic paths;
- verify worktree/branch relationship;
- prevent two roles from unintentionally sharing one mutable workspace;
- synchronize role worktrees after authorized merge.

### 4.4 Change Inspector

Responsibilities:

- `status` equivalent;
- changed-file inventory;
- staged/unstaged/untracked classification;
- diff statistics;
- conflict detection;
- dangerous/unexpected path detection;
- evidence handoff to Controller.

### 4.5 Commit Manager

Responsibilities:

- build a commit only from the admitted task boundary;
- reject unrelated or ambiguous changes;
- generate/validate commit metadata;
- record commit SHA into the stage evidence record.

### 4.6 Pull Request Manager

Responsibilities:

- push the intended branch;
- create/update the corresponding PR;
- bind PR identity to the stage/task;
- expose PR head SHA, base SHA, mergeability and review state;
- never imply approval merely because a PR exists.

### 4.7 CI/Check Observer

Responsibilities:

- watch GitHub Actions/check state;
- correlate checks with exact commit SHA;
- collect failing job/step evidence;
- feed mechanical failures into the repair loop;
- distinguish stale checks from checks on the current PR head.

### 4.8 Merge Gate

Responsibilities:

- accept an explicit Controller merge authorization;
- verify repository/PR identity;
- verify expected head SHA;
- invalidate authorization if the head changes;
- execute the permitted merge method;
- record merge result;
- trigger post-merge synchronization.

---

## 5. Merge Authorization Model / 合并授权模型

Merge authorization MUST be bound to a concrete immutable state.

Candidate model:

```text
MergeAuthorization
- authorization_id
- project_id
- stage_id
- repository
- pull_request_number
- expected_head_sha
- controller_decision_id
- issued_at
- status
```

Rules:

1. authorization targets one PR;
2. authorization targets one exact head SHA;
3. any new commit invalidates the previous authorization;
4. merge cannot proceed if required checks for the authorized head are not satisfied by policy;
5. authorization cannot be inferred from chat prose alone when a structured decision record exists;
6. worker roles cannot self-issue authorization.

This prevents a reviewed commit from being replaced by unreviewed changes before merge.

---

## 6. Stage-Gate Integration / 与阶段门控整合

Repository state becomes part of stage state.

```text
PLANNED
  ↓
ADMITTED
  ↓
WORKSPACE_READY
  ↓
IMPLEMENTING
  ↓
SUBMITTED
  ↓
VALIDATING
  ↓
PR_READY
  ↓
REVIEWING
  ├── FIX_REQUIRED → IMPLEMENTING
  ├── BLOCKED
  └── PASS
        ↓
MERGE_AUTHORIZED
        ↓
MERGED
        ↓
SYNCHRONIZED
        ↓
CLOSED
```

Not every version must expose all states publicly, but the architecture must not collapse `PASS`, `MERGE_AUTHORIZED`, and `MERGED` into one state.

---

## 7. Automated Repair Loop / 自动修复闭环

Mechanical failure does not require the user to manually operate Git.

Example:

```text
Codex task completes
  → Change Inspector collects diff
  → Commit/PR created or updated
  → CI fails
  → failure evidence normalized
  → Controller/repair policy routes bounded FIX task
  → same role thread + same bounded worktree
  → new commit pushed
  → PR head changes
  → old merge authorization automatically invalid
  → CI reruns
  → Controller re-review
```

The repair loop may automate transport and repository mechanics. It must not silently convert a failed or changed revision into an approved revision.

---

## 8. Safety Boundaries / 安全边界

Early implementations must explicitly protect against:

- committing unrelated local files;
- secrets entering commits or logs;
- accidental force-push;
- destructive reset/clean operations;
- branch deletion without policy;
- wrong-repository targeting;
- wrong-worktree targeting;
- merging a stale/unreviewed head;
- bypassing protected-branch checks;
- autonomous release/tag/publish actions;
- ambiguous remote selection;
- replayed merge authorization.

Default principle:

> destructive repository operations require higher authority than ordinary development operations.

---

## 9. Version Placement / 版本落位

This amendment does not expand the frozen v0.1 milestone.

Planned evolution:

- **v0.1–v0.5:** establish reliable Codex control loop first;
- **v0.6:** evidence collection may begin consuming Git diff/change metadata read-only;
- **v0.7–v0.8:** roles and Stage Gate bind to project/repository/worktree metadata;
- **v0.9:** narrow repository state may be exposed through structured control surfaces where safe;
- **v1.0:** repository awareness is integrated with the Controller workflow, with merge still explicitly gated;
- **v1.1:** Repository Control Plane automates normal branch/worktree/commit/PR/CI/repair/merge/sync mechanics under policy.

---

## 10. Target v1.1 Workflow / v1.1 目标工作流

```text
Controller: "Continue FlowTracer."
        │
        ▼
Stage Engine resolves current admitted stage
        │
        ▼
Role Registry resolves specialist Codex
        │
        ▼
Repository Registry resolves repo/branch/worktree
        │
        ▼
Workspace verified/prepared automatically
        │
        ▼
Task Packet generated and dispatched
        │
        ▼
Codex executes
        │
        ▼
Evidence + repository changes collected
        │
        ▼
Commit → Push → PR → CI
        │
        ▼
Controller Review
   ┌────┼────┐
   ▼    ▼    ▼
  FIX  BLOCK PASS
   │          │
   └→ repair  ▼
          Merge Authorization
                │
                ▼
          automatic merge
                │
                ▼
       post-merge synchronization
                │
                ▼
          next stage admission
```

The user manages engineering decisions; Codex Domination manages the repetitive repository choreography.

---

## 11. Methodological Meaning / 方法论意义

With this amendment, Codex Domination is not only an Agent orchestration layer.

It coordinates two traditionally separate control problems:

1. **Who should do the work, with what context and authority?** — Agent Control Plane.
2. **Where should the resulting code live, how is it validated, and when may it advance?** — Repository Control Plane.

The product therefore moves toward an executable AI software-engineering operating model:

> **Controller decides. Codex executes. Evidence proves. Git records. Codex Domination coordinates.**
