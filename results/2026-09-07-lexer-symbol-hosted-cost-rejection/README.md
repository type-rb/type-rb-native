# Lexer symbol refinement: hosted cost rejection

Status: **rejected**, not runtime acceptance.

[Run 34065526252, attempt 1](https://github.com/type-rb/type-rb-native/actions/runs/34065526252)
tests source-distinct candidate `34d46e2bab76a2b506508d2bed7861cbd7872e02`
against frozen baseline `1afd60c2c7257ed34fd2a2aa70cb8b9164433009`.
It preserves the unchanged compiler policy and observation schedule.

| Target | Compiler ratio | Baseline build wall (s) | Candidate build wall (s) | Wall ratio |
| --- | ---: | ---: | ---: | ---: |
| Darwin arm64 | 1.049725 | 1.765 | 1.855 | 1.050992 |
| Linux arm64 | 1.049104 | 1.305 | 1.380 | 1.057471 |

Both build wall ratios exceed 1.05. Do not combine the earlier candidate's
Darwin pass with this candidate's Linux result, substitute a local pass, or
retry the unchanged compiler until it passes. Both target jobs stop at the
failed wall comparison, so later RSS/catastrophic evaluations and application
authorities are incomplete. The original comparison rows, all raw interleaved
observations, code sections, policies and generation identities are retained.
Full bootstrap/process evidence remains in the linked public artifacts.

This source's prior local evidence passes 138 compiler tests, 225 corpus
observations and exact ordinary fixed points. Numeric application QBE remains
unchanged. Long current-source root recovery and runtime acceptance were not
dispatched after this cost rejection, saving those batches without weakening
the eventual merge requirements. PR #307 remains draft and Pages is unchanged.

The lexer cleanup removes unused allocation and implementation duplication, but
does not provide enough cost headroom for the complete MIR candidate. Further
phase-level evidence and a smaller supported representation are needed.
A subsequent attempt to group verifier failure conditions with `||` was rejected
by the previous Native compiler's lexical preflight; that spelling is accepted
by the pinned reference but outside the current Native source subset. The
attempt was reverted before publication and is not a compiler candidate or
performance result. Do not broaden that subset solely to make a cost result pass.
