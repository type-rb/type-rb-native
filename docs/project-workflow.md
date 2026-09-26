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

Open initiatives with the Initiative form and tasks with the Task form. They set
the issue type and add it to the project when the author has project write
permission. Otherwise, a project collaborator adds the issue during triage;
the form's project setting does not grant access to the project.

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
| Claim, Claim updated | Current owner as `<agent>:<run-id>@<claim-sha>` and the date it last confirmed the claim |
| Touches | Main files or modules the task changes, used to avoid conflicting work |
| Metric, Target, Baseline, Current, Measured, Evidence | Initiative measurement; see below |

A task is **Ready** when its issue states the acceptance criteria, dependencies
and Touches, and its initiative is Active.

## Starting work

- Anyone may record a Backlog task, a bug or a Proposed initiative.
- Tasks may be planned under an Approved or Active initiative.
- Implement only Ready tasks under an Active initiative. Take P0 before P1
  before P2, and older items first within a priority.
- Keep at most three initiatives Active so that started work finishes. Before
  activation, record the Metric, Target and Baseline and prepare the first task.
- An agent run holds at most one task In progress and one In review.
- When `Main validation` fails, repairing or reverting `main` comes first and may
  skip the Ready and initiative rules. Record the repair as a task afterwards
  when the fix needs follow-up work.

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

When the task reaches Verified or Dropped, or the owner stops working, update
the status and clear Claim while still holding the branch. Then release only
the saved token:

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
