# Project workflow

Planned work is tracked in issues and the associated project board.
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

Open initiatives with the Initiative form, tasks with the Task form, and
specification improvements with the Specification proposal form. They set
the issue type and add it to the project when the author has project write
permission. The auto-add workflow also collects new or updated open issues from
this repository, including those created without the forms. A project
collaborator handles any missed additions during triage; the form's project
setting does not grant access. Use All for triage and historical lookup.

## Views and fields

| View | Shows |
| --- | --- |
| Initiatives | Open and recently closed initiatives, grouped by Initiative state |
| Tasks | Open work and issues closed in the last seven days, grouped by Status |
| Decisions | Items whose Attention is Needs decision |
| All | Every item as a table |

The Tasks filter is `-type:Initiative -closed:<@today-7d`; Initiatives uses
`type:Initiative -closed:<@today-7d`. Both hide work closed more than seven days
ago without removing it from All or requiring a sprint assignment. The rolling
window advances automatically. An issue without a closed date stays visible.

| Field | Values and meaning |
| --- | --- |
| Status (tasks) | Todo, In progress (including PR review and CI), Done |
| Initiative state | Proposed, Approved, Active (including measurement), Done |
| Attention | Empty when no help is needed; Blocked (link the blocker), Needs decision (state the question) |
| Priority | P0 urgent, P1 next, P2 later |
| Area, Family | Surface of the work; Family is a registry id from `tools/native-language-cases.json` |
| Claim, Claim updated | Current owner as `<agent>:<run-id>@<claim-sha>` and the date it last confirmed the claim |
| Touches | Main files or modules the task changes, used to avoid conflicting work |
| Metric, Target, Baseline, Current, Measured, Evidence | Initiative measurement; see below |

Todo records pending work; it does not authorize implementation. A task is
eligible to start when its initiative is Active, its acceptance criteria and
Touches are clear, its dependencies are resolved, and no decision is pending.
Imported issues without a parent remain available for triage, not automatic
execution. Closed issues remain in the project as Done; the close reason
distinguishes completed work from work closed as not planned.

## Starting work

- Anyone may record a Todo task, a bug or a Proposed initiative.
- Tasks may be planned under an Approved or Active initiative.
- Implement only eligible tasks under an Active initiative. Take P0 before P1
  before P2, and older items first within a priority.
- Keep at most three initiatives Active so that started work finishes. Before
  activation, record the Metric, Target and Baseline and prepare the first task.
- An agent run holds at most two tasks In progress: one being implemented and
  at most one waiting for PR review or CI. Waiting work still counts toward WIP.
- When `Main validation` fails, repairing or reverting `main` comes first and may
  skip the normal eligibility and initiative rules. Record the repair as a task
  afterwards when the fix needs follow-up work.

## Claiming a task

Claims are serialized through a create-only branch with a unique commit for
each acquisition attempt. Run this from the repository, replacing the task
number and owner with public identifiers:

```bash
set -eu
task=123
claim_owner='codex:REPLACE_WITH_RUN_ID'
claim_ref="refs/heads/claim/task-$task"
git fetch origin main
claim_base=$(git rev-parse origin/main)
claim_tree=$(git rev-parse "$claim_base^{tree}")
claim_nonce=$(python3 -c 'import uuid; print(uuid.uuid4())')
claim_sha=$(git commit-tree "$claim_tree" -p "$claim_base" \
  -m "Claim task $task by $claim_owner; nonce $claim_nonce")
git push --force-with-lease="$claim_ref:" origin "$claim_sha:$claim_ref"
```

The nonce must be fresh for every acquisition attempt, even in the same run.
Pushing `origin/main` directly is unsafe: when the existing branch already
points to that commit, Git returns success with `Everything up-to-date` even
with the empty lease. The distinct claim commit makes an existing branch reject
the create-only push. A plain push is not a claim either. If creation fails,
do not start work or update the board. If the network result is uncertain,
compare the remote ref with the saved `claim_sha` before retrying or proceeding.

The claim commit has the baseline tree and is only an ownership token. Create
the implementation branch from main, not from the claim branch. Keep the token
SHA for the lifetime of the claim and never add implementation commits to it.

After a successful claim, set Claim to `<agent>:<run-id>@<claim-sha>`, set Claim
updated to today and move Status to In progress. If a board update fails, retain
the branch and reconcile the fields before working. Refresh Claim updated each
day the work continues, and verify the remote ref still matches the saved token
before resuming work or changing ownership fields.

When the task reaches Done, or the owner stops working, reconcile Status and
clear Claim and Claim updated while still holding the branch. Unfinished work
returns to Todo; record any blocker in Attention. Then release only the saved
token:

```bash
git push --force-with-lease="$claim_ref:$claim_sha" origin ":$claim_ref"
```

Never replace the saved SHA with a newly observed owner's SHA to force release.
A claim that has not been updated for two days and has no open PR needs
investigation: comment on the issue and set Attention to Needs decision. A date
alone does not prove the owner stopped. Reclaim only after the maintainer
confirms it is inactive, using the old token's conditional deletion before a
fresh acquisition. A resumed former owner must stop if its token no longer
matches. Claim branches are coordination records and are never merged.

## Delivering a task

1. Work on a separate branch and open a PR. Use `Closes #<n>` for the Task or Bug
   whose acceptance criteria the PR completes. Keep Status In progress through
   review and CI. For partial work, use a plain issue reference and leave it open.
2. Merge once PR acceptance passes, following [CI validation](ci-validation.md),
   within the task's merge authorization. Merging to the default branch closes
   the linked task, and the project automation sets Done. For investigation or
   documentation work without a PR, record the result and evidence before
   closing the completed task.
3. Release the claim and clean up the implementation branch and worktree.
   Task closure does not require a separate wait for `Main validation`.
4. `Main validation` remains the repository integration authority. Monitor its
   result, and fix or revert a failure before further feature merges. If a
   revert removes a task's delivered result, reopen it and return it to Todo,
   or In progress if its owner still holds a valid claim and is fixing it.

Never use a closing keyword or a closing Development link for the parent
initiative in an implementation PR. A completed child does not prove the
initiative's outcome. Inspect the PR's linked issues before merging; even a
negated closing keyword can close an issue.

A dropped task records the reason in a comment and is closed as not planned.

## Project automation

Use issue cards as the work records; linked PRs supply review and CI context.
Enable these built-in workflows in Project settings:

- Auto-add to project: new or updated open issues in this repository, using
  `is:issue is:open` with the repository selected.
- Item added to project: issues get Status Todo. When importing already closed
  issues, explicitly set Done after adding them; this workflow has no state filter.
- Item closed: issues get Status Done.
- Item reopened: issues return to Todo.
- Auto-add sub-issues to project: keep child tasks with their parent.

Keep Auto-close issue disabled: dragging a card must not close an unfinished
issue. Pull request merged is unnecessary for this issue-only board; task
closure through its PR triggers Item closed. After reopening an issue, restore
In progress only if its owner still holds a valid claim and is resuming work.
Initiative state is managed separately from Status and is never inferred from
a merged child PR. Set a newly added initiative to Proposed during triage.

## Authority

| Agents act without asking | Agents set Needs decision and wait |
| --- | --- |
| Create, refine and order tasks under Approved or Active initiatives | Approve, activate, rescope or drop an initiative, or change its target |
| Implement, open PRs, merge after PR acceptance passes and clean up branches | Change bootstrap seeds, the reference pin or releases |
| Fix or revert a failing `main` | Remove or weaken required CI checks |
| Update documentation within the task's scope | Change secrets, permissions, organization or project settings |
| File, reproduce and triage bugs | Post to other repositories or external services |
| File specification proposals found while reproducing TypeRB | Adopt a specification change or send it upstream |

A maintainer's direct request defines its own scope and completion point; these
rules apply to work an agent takes from the board.

## Initiative metrics

An initiative states one Metric with the command or workflow that measures it,
and a Target. Baseline records the value, revision and conditions. Current,
Measured and Evidence record the latest value, its date and a link to the run or
comment that produced it. A value without Measured and Evidence is not a
measurement, and a value measured before the latest relevant merge is stale.
Compare only measurements taken under the Baseline conditions.

Keep an initiative Active while measuring its outcome. The maintainer confirms
completion from Evidence against Target, or explicitly accepts a different
result with the reason recorded. Then set Initiative state to Done and close
the issue as completed. To stop an initiative, record the maintainer's decision,
set Done and close as not planned. Reopening requires an explicit lifecycle
decision and must respect the three-Active limit; it does not resume work by itself.

## Weekly review

Each week the maintainer, with an agent preparing the summary, reviews:

- the Decisions view and Blocked items;
- Current against Target for each Active initiative;
- Proposed initiatives to approve or drop, and which ones become Active;
- stale claims, long-running tasks and PRs waiting for review or CI.

The board and issues are the source of truth for work state. Local session notes
may hold environment details and handoffs, but not task ownership or status.
