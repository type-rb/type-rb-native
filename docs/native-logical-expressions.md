# Short-circuit Boolean expressions

Issue [#308](https://github.com/type-rb/type-rb-native/issues/308) adds `||`
and `&&` together to the ordinary compiler. This is an implementation of the
pinned TypeRB contract, not a new language decision. Both operands must be
non-nullable `Boolean`; the result is `Boolean`. The left operand executes
once. `||` executes the right operand only after `false`, and `&&` only after
`true`. Both operands are resolved and checked even when a constant left
operand skips the right at runtime.

Precedence is unary `!`, arithmetic, ordering, equality, `&&`, then `||`; parentheses
override grouping. Logical compound assignment and bitwise operators remain
outside this slice.

The [local implementation checkpoint](../results/2026-09-07-logical-expressions-darwin-arm64/README.md)
passes correctness and ordinary fixed-point checks, but the combined candidate
still exceeds its build-time limit. It is not accepted or released.

## Ownership

The checker constructs a bounded structured logical plan using the MIR
Boolean-only constructor. The existing source-indexed checked projection
binds that plan to its operator origin. Plan 76 skips with true, and plan 77
skips with false. These internal tags are deliberately not eager binary
instructions and are rejected by ordinary checked-binary lowering.

The adapter validates the plan and operator binding before lowering the right
region. It lowers a branch and Boolean merge, not an eager `or` or `and`.
An initialized private Boolean slot joins nested RHS control flow without
reconstructing a backend predecessor; QBE can promote this slot.
Conditional header temporaries are invalidated at branch boundaries. Runtime
managed-root operations remain on their executed paths.

This is not complete function-CFG MIR coverage. The current flat scalar and
Array projections are disabled for a logical expression because they cannot
represent its conditional work. They must never hoist RHS operations, traps,
or effects. A later complete CFG connection can remove this conservative
boundary; it must not rediscover short-circuit semantics in the backend.

## Acceptance and self-adoption

Require differential truth tables, grouping, nested calls and mutation,
skipped and required traps, invalid operands, malformed-plan rejection, the
existing corpus, recovery coverage and ordinary file-root fixed points.
Measure compiler build time, RSS and artifacts under existing policy; this
feature does not relax the bounds or accept the rejected Array-loop candidate.

The core implementation uses only syntax accepted by the published Native
seed. The CLI and REPL are built by the newly generated core, so they can
already use logical guards without adding a bootstrap stage. The REPL consumes
the same checked plan and advances over a skipped RHS using syntax parsing,
never evaluation. Exit-command and history-publication guards are initial
compiler-tooling consumers; a failed history write must not attempt rename.

Before replacing core compiler guards with logical expressions, retain
and verify a previous-Native setup compiler that understands those expressions,
and wire its exact source provenance into ordinary bootstrap and recovery.
Do not change immutable released assets, silently invoke Go, or claim local
self-adoption as a working fresh bootstrap. Keep self-adoption a separate
reviewable checkpoint until all these consumers can rebuild it.

The pinned reference has a separate condition-parsing defect:
[type-rb#648](https://github.com/type-rb/type-rb/issues/648) loses the suffix
of some conditions beginning with a parenthesized operand. The managed-RHS
fixture deliberately retains that valid source shape. Record its reference
failure and any fixed-reference comparison separately; do not mislabel a
newer or patched oracle as the unchanged compatibility pin.
The fix merged in [type-rb#649](https://github.com/type-rb/type-rb/pull/649)
at `8220f9c121c836d4c0e01aecbf8e8aeb4dab8ef9`; compatibility advancement is
separate from the source-identified supplemental comparison.

Basic supported-language gaps that force duplicated checks or deeply nested
compiler code are candidates for bounded implementation alongside maintenance.
Pair closely related forms and their tests, but do not turn a local cleanup
into an unmeasured full-language expansion. Verify before replacing the
workaround, then remove it rather than retaining two implementation paths.
