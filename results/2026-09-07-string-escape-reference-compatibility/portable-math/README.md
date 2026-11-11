# Portable Math reference compatibility

The selected development reference is TypeRB `0.4.12-dev` at
`7a6b7405c895f2d7f377956b17e9e569de6fb069`, merged through
[type-rb/type-rb#852](https://github.com/type-rb/type-rb/pull/852).
It adds portable `Math.sin`, `Math.cos` and `Math.pow` and selects Ruby 4.0.9.
This is an exact development pin, not a release or supported version range.

Native `cbd507fc3564da442fc8cc91024ea945d66aec1b` previously passed
https://github.com/type-rb/type-rb-native/actions/runs/41935948994.
That run predates this reference update and does not qualify the new pin.
A subsequent Main run failed during Linux symbol inspection and then passed
an investigated, unchanged retry: [run 42923392428](https://github.com/type-rb/type-rb-native/actions/runs/42923392428).
The original failure remains visible; harness diagnostics are tracked separately
in #1326. Historical evidence and seeds are unchanged.

The Native companion implements verified Float signatures, direct platform
math calls and checked REPL dispatch. Focused implementation controls passed
against the reference candidate. Qualification against the exact merged reference completed locally. Hosted
PR acceptance and subsequent Main validation remain separate authorities.

| Local validation | Result |
| --- | --- |
| Exact reference build and bundled source verification | Passed; 50 pinned files verified |
| Maintained preflight | All checks passed, including snapshot-v4, time, filesystem, network and project contracts |
| MIR math and existing standard call controls | 22 tests passed |
| Ordinary Math check/build/execution/REPL | Both registered cases matched the exact reference |
| Complete reference registry and exact AST | 2,741 cases matched; 67 known Native parity gaps remain |

Ordinary core and CLI fixed points and 424 conformance source checks were
already successful for source `ffc67c97f80c51789a649fe9aa85e4ee9189827b`.
Compiler and recovery source bytes remain unchanged during pin integration.
The CLI SHA-256 is `21f1856209b420fb95cd49e1102d93eb5891c452211dbd76cb2cca566d87d0cf`;
the core SHA-256 is `8202f99bd1f22614be517b0a187fb429f0895bcc02ee0450cc1ccabef12932af`.
Reference-registry agreement is not a claim that all those cases pass in Native.
The first integration preflight rejected a stale manifest digest before time
observations ran. Only its reference identity and matching digest changed;
all existing time inputs and expected outcomes were retained and then passed.

The preceding browser/JSON compatibility observations remain available at the
[exact preceding revision](https://github.com/type-rb/type-rb-native/blob/cbd507fc3564da442fc8cc91024ea945d66aec1b/results/2026-09-07-string-escape-reference-compatibility/browser-contract-identity/README.md).
The active record-Array cost cohort elsewhere in this registered slot is unchanged.
