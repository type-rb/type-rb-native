# Decision 0014: Indexed self-hosted function lookup

## Status

Accepted for the Gate 6G experiment.

## Context

The self-hosted frontend keeps declarations in source-ordered parallel arrays.
Every direct call previously scanned the complete function array during
resolution, checking, and emission, including after a match. That is bounded
for the current compiler, but a generated chain of 6,000 functions exposes
quadratic growth.

Reversing every lookup and returning at the first match preserved the existing
last-declaration result and improved the generated scale source, but it made
the canonical compiler slower. Its declaration order and the cost of checked
reverse iteration made that general strategy unsuitable.

## Decision

Function declarations retain their canonical source-ordered arrays. After the
complete module closure is parsed and before declaration resolution begins, the
compiler builds one deterministic internal index:

- the bucket count is zero for an empty table, otherwise the smallest power of
  two at least twice the function count with a minimum of 16;
- `(module index * 257 + name length) % bucket count` selects a bucket;
- each bucket head and declaration's next link use demand-sized Integer
  storage; and
- declarations are inserted in source order at the head, so the first exact
  module-and-name match is the last canonical declaration, matching the prior
  behavior even for duplicate invalid input.

The bucket key only partitions candidates. Lookup still compares the complete
module identity and String, so collisions cannot change semantics. The table
is rebuilt from canonical arrays and has no independent declaration ownership.
The parser finishes all declarations before the index is built, so incremental
mutation, deletion, and rehashing are not part of this boundary.

Lower-cardinality module, record, import, field, and local lookup remains over
the canonical arrays. Applicable short-lived tables may return from the last
matching entry, but they do not acquire a second persistent index without
separate evidence.

Lexical character-set membership remains a direct scan of the checked-in ASCII
sets and returns at the first exact character match. It does not retain index
state or change the accepted identifier alphabet; it only avoids scanning the
known-irrelevant remainder after success.

## Consequences

The ordinary resolver must build the function index before any indexed lookup;
there is no linear semantic fallback. Exact collision, duplicate,
module-qualified, missing-key, and bucket-growth tests protect that invariant.
The generated QBE, diagnostics, source order, target behavior, and external
QBE/CC boundary do not change.

This is compiler-internal TypeRB code. It does not add public `Hash` semantics,
a compiler-runtime intrinsic, Native MIR data, snapshot data, or a user-facing
configuration surface. A worst-case bucket may still be linear; a stronger
hash is justified only by later profiles and must not weaken portable String
semantics.

## Rejected alternatives

### Reverse every linear lookup

Rejected after diagnostic measurement. It improved the 6,000-function source
but substantially regressed the canonical compiler.

### Add a public or runtime String hash operation

Rejected for this slice. Public Hash behavior and a new compiler-runtime
intrinsic would expand language or runtime design to solve an internal table
problem.

### Replace canonical declaration arrays

Rejected. Source order drives deterministic diagnostics and emission. The
index accelerates lookup but is not another source of truth.
