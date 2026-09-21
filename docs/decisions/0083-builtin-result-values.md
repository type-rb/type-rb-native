# Builtin Result values, conversions and Unicode identifiers

Status: implemented direction under basic-language completion. This combines the
frontend, MIR, runtime and retained-session paths for one builtin value family.

`Array.try_fetch`, `String.try_fetch`, `Array.try_slice`, `String.try_slice` and
`Hash.try_fetch` return the canonical standard `Result` and structured error
declarations. The receiver and arguments are evaluated once, in authored order.
The retained receiver's size or key table is read after argument effects.
Negative indexes normalize against that live size; errors preserve the original
index. Slices require ordered nonnegative bounds, allowing an empty exclusive
range at the end. Hash errors preserve the requested Integer or String key.
Aliases do not replace canonical declaration identity.

These operations lower to existing typed MIR comparisons, branches, collection
reads and enum/record construction. No backend method-name analysis or alternate
Result representation is introduced. Implicit standard declarations are loaded
before type resolution, and a preliminary body pass completes inferred Result
instances before MIR catalogs freeze. The final catch expression receives the
known success type, including a directly returned empty Array; unrelated earlier
statements and explicit returns retain their own typing boundaries.

`String.try_to_i`, `String.try_to_f` and strict `String.to_f` use portable decimal
syntax and range rules. MIR verifies the scalar conversion and nonthrowing parse
status independently; existing typed branches construct success or the precise
`NumberParseErrorKind`. The shared runtime validates the entire byte sequence
before reporting range errors, rejects whitespace/NUL/hex/NaN/infinity spellings,
and preserves Float signed zero and subnormal values. System `strtod` converts an
already validated decimal sequence. It cannot decide authored syntax or the
Result failure model. The REPL uses the same core parsing operations, removing
its duplicate Integer parser.

Unicode identifier classification uses generated tables for the pinned Go
toolchain's Letter, Decimal_Number and Uppercase_Letter categories. A strict UTF-8
decoder and byte-preserving names retain distinct spellings without normalization.
ASCII constant/reserved-name rules remain unchanged. The immutable seed compiles
ASCII implementation source; the ordinary Native compiler's existing byte adapter
handles Unicode input. Recovered Native generations exercise these names directly.
The Go-hosted recovery frontend's ASCII fallback is recorded separately and does
not establish Unicode frontend coverage.

Paired ordinary check/build/execution/REPL cases retain rejected inputs and
presentation gaps. Independent MIR verification rejects forged conversion types,
payloads and instruction shapes; source-body erasure, reordered blocks and forced
collections exercise managed success/error payloads. Retained sessions cover
declaration growth, imported aliases, explicit replay and failed submissions.
Capabilities are generated from those reviewed outcomes. Untyped discarded empty
collections, nested contextual inference, remaining String APIs, malformed-source
origins and broader display parity remain explicit contracts. No full-language or
performance qualification follows from this family alone.
