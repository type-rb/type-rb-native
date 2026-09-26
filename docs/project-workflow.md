# Project workflow

Planned work is tracked on the [TypeRB Native project](https://github.com/orgs/type-rb/projects/6).
Agents do the implementation work. The maintainer approves initiatives and
answers decisions. There are no sprints: a weekly review and work-in-progress
limits keep the flow moving.

## Items

- **Initiative** (issue type): a measurable outcome delivered through several
  tasks, such as a reduced benchmark ratio or a completed language family.
  Long-running milestone issues, such as MIR consolidation (#439) and
  basic-language completion (#454), stay open as parents of initiatives.
- **Task** or **Bug** (issue type): one reviewable change, normally one PR. Each
  task is a sub-issue of exactly one initiative. A bug waiting for triage and an
  emergency repair of `main` may exist without a parent.

Open initiatives with the Initiative form and tasks with the Task form. They add
the issue to the project and set its type.

## Views and fields

| View | Shows |
| --- | --- |
| Initiatives | Initiative board grouped by Initiative state |
| Tasks | Task and bug board grouped by Status |
| Decisions | Items whose Attention is Needs decision |
| All | Every item as a table |

| Field | Values and meaning |
| --- | --- |
| Status (tasks) | Backlog, Ready, In progress, In review, Merged, Verified, Dropped |
| Initiative state | Proposed, Approved, Active, Measuring, Done, Dropped |
| Attention | None, Blocked (link the blocker), Needs decision (state the question) |
| Priority | P0 urgent, P1 next, P2 later |
| Area, Family | Surface of the work; Family is a registry id from `tools/native-language-cases.json` |
| Claim, Claim updated | Current owner as `<agent>:<run-id>` and the date it last confirmed the claim |
| Touches | Main files or modules the task changes, used to avoid conflicting work |
| Metric, Target, Baseline, Current, Measured, Evidence | Initiative measurement; see below |

A task is **Ready** when its issue states the acceptance criteria, dependencies
and Touches, and its initiative is Active.

## Starting work

- Anyone may record a Backlog task, a bug or a Proposed initiative.
- Tasks may be planned under an Approved or Active initiative.
- Implement only Ready tasks under an Active initiative. Take P0 before P1
  before P2, and older items first within a priority.
- Keep at most five initiatives Active so that started work finishes.
- An agent run holds at most one task In progress and one In review.
- When `Main validation` fails, repairing or reverting `main` comes first and may
  skip the Ready and initiative rules. Record the repair as a task afterwards
  when the fix needs follow-up work.

## Claiming a task

Claims are serialized through a create-only branch, so two agents cannot own
the same task:

```bash
git push --force-with-lease=refs/heads/claim/task-<n>: origin origin/main:refs/heads/claim/task-<n>
```

The empty expected value makes the push fail when the branch already exists.
A plain push is not a claim because it can fast-forward an existing branch. If
the push fails, choose another task.

After a successful claim, set Claim to `<agent>:<run-id>` with an identifier
unique to the run, set Claim updated to today and move Status to In progress.
Refresh Claim updated each day the work continues. A claim that has not been
updated for two days and has no open PR is stale: comment on the issue, delete
the branch and claim the task again. Delete the claim branch and clear Claim
when the task reaches Verified or Dropped, or when the owner stops working on it.

## Delivering a task

1. Work on a separate branch and open a PR whose body contains `Task: #<n>`.
   Do not use closing keywords; merging must not close the task. Move Status to
   In review.
2. Merge once PR acceptance passes, following [CI validation](ci-validation.md),
   and move Status to Merged.
3. After `Main validation` succeeds on a `main` revision that contains the merge
   commit, comment the merge commit and the run URL on the task, move Status to
   Verified and close the issue as completed.
4. If `Main validation` fails because of the change, fix or revert it before
   other merges and keep the task open until a later run succeeds.

A dropped task records the reason in a comment and is closed as not planned.

## Authority

| Agents act without asking | Agents set Needs decision and wait |
| --- | --- |
| Create, refine and order tasks under Approved or Active initiatives | Approve, activate, rescope or drop an initiative, or change its target |
| Implement, open PRs, merge after PR acceptance passes and clean up branches | Change bootstrap seeds, the reference pin or releases |
| Fix or revert a failing `main` | Remove or weaken required CI checks |
| Update documentation within the task's scope | Change secrets, permissions, organization or project settings |
| File, reproduce and triage bugs | Post to other repositories or external services |

A maintainer's direct request defines its own scope and completion point; these
rules apply to work an agent takes from the board.

## Initiative metrics

An initiative states one Metric with the command or workflow that measures it,
and a Target. Baseline records the value, revision and conditions. Current,
Measured and Evidence record the latest value, its date and a link to the run or
comment that produced it. A value without Measured and Evidence is not a
measurement, and a value measured before the latest relevant merge is stale.
Compare only measurements taken under the Baseline conditions.

Move an initiative to Measuring when its tasks are merged or the target appears
to be reached. It is Done when Evidence shows the target, or when the maintainer
accepts the result and the issue records why.

## Weekly review

Each week the maintainer, with an agent preparing the summary, reviews:

- the Decisions view and Blocked items;
- Current against Target for each Active initiative;
- Proposed initiatives to approve or drop, and which ones become Active;
- stale claims and tasks that stayed In review or Merged.

The board and issues are the source of truth for work state. Local session notes
may hold environment details and handoffs, but not task ownership or status.
