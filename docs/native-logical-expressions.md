# Short-circuit Boolean expressions

Issue [#308](https://github.com/type-rb/type-rb-native/issues/308) implements
`||` and `&&` together. Both operands must be non-nullable Boolean and both
are resolved and checked. The left operand executes once; the right executes
only after false for OR, or true for AND. Precedence runs from unary operators,
arithmetic, ordering, equality and AND to OR. Parentheses override grouping.
Logical compound assignment and bitwise operators are outside this slice.

## Accepted independent feature

Merged [PR #317](https://github.com/type-rb/type-rb-native/pull/317) extracts
the language capability from draft PR #307 without its
Array-loop proof or bounds-check optimization. Its accepted implementation
baseline is `450ed9d1bd8a43b85cb5cfb653326d0eee42d6ec`, with reference
`47a160cae05ddc2035c7430735c4762d36bbc9c4`. The earlier combined candidate's
cost rejection remains valid and is not an isolated Boolean-feature result.
Issue #303 retains its original frozen baseline and acceptance requirements.

All seventeen required jobs passed in the
[exact-head validation](https://github.com/type-rb/type-rb-native/actions/runs/34090466286),
including recovery-enabled suites (97 root and 119 compiler tests), ordinary
fixed points, CLI, memory, process and target checks, and compiler costs.
Hosted build wall ratios were 1.003077 on Darwin arm64 and 1.003922 on Linux
arm64; complete compiler sizes were 332,728 and 307,544 bytes. The existing
limits were unchanged. This is capability acceptance, not a runtime speedup.
The [local selection record](https://github.com/type-rb/type-rb-native/tree/0197303234d047ba6b413a6fdee870fbccc698d1/results/2026-09-07-independent-logical-expressions-darwin-arm64)
is retained in Git history rather than occupying the active candidate slot.

## Ownership

Structured checking calls the Boolean-only MIR plan constructor and binds its
result to the exact operator origin in existing storage. The adapter verifies
that binding and lowers a branch, conditional RHS and private Boolean merge
slot. QBE can promote the slot; it is not an eager binary AND/OR instruction.
Malformed, absent and opposite-operator plans fail closed.

The current flat scalar and Array projections cannot represent conditional
work, so logical expressions disable those projections conservatively.
Conditional Array-header temporaries are invalidated at branch boundaries;
managed-root operations stay on their executed paths. No RHS call, allocation
or trap may be hoisted. This does not complete general function-CFG MIR.

REPL evaluation consumes the same plan and parses a skipped RHS without
evaluating it. Its unary operand precedence must remain above every binary
operator; the independent regression requires `-1 + 2` to produce `1`, not
`-3`. Compiled and REPL controls cover truth tables, nesting, grouping,
side effects, managed values, invalid operands and required/skipped traps.

## Acceptance and adoption

Require reference checks, recovery-enabled suites, previous-Native fixed
points, conformance, CLI/REPL, target/process/memory and measured compiler
cost. Existing workloads must retain exact QBE. Ordinary 1.05 compiler/build/RSS
ratios, 2.0 catastrophic limits and absolute transition ceilings remain unchanged.
No new marker, allowance, runtime improvement or Pure Go claim is introduced.

The core uses syntax understood by the immutable published seed. The generated
core builds the CLI, allowing exit and history-publication guards to use OR.
Core-source self-adoption needs a separately verified previous-Native setup
transition; do not change seed assets or add a hidden Go fallback. The current
reference already includes the condition-parser repair from TypeRB PR #649.
