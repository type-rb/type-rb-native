# Checked literal binding representation: rejected local diagnostic

Status: **rejected for compactness**, not a shipped compiler change or a runtime
performance result. This investigates the remaining ownership in
[issue #254](https://github.com/type-rb/type-rb-native/issues/254) against accepted
baseline `9ee27485f1612279994cc341b50b16b27f0df914`.

## Replacement and result

The diagnostic removes emitted-QBE literal parsing from direct binary lowering.
Checked values carry canonical literal bindings independently of their raw
source origin. Three cells per token in the existing origin store carry the
existing plan/fact, an exact binary-left/argument binding, and a binary-right/
actually-selected-call result. A verified scalar-MIR return query follows only
literals, parameters and unary plus. Unselected calls, computed values and
Float conversions retain unknown bindings. The selected-call budget and raw
scalar arithmetic proofs remain distinct and unchanged.

Transient scalar-lowering result and operand records are removed in the same
replacement. Four local representations were measured, without changing the
reference, runtime ABI, thresholds or transition markers:

| Representation | Compiler QBE bytes | Darwin code bytes | Complete compiler bytes |
| --- | ---: | ---: | ---: |
| Accepted baseline | 1,115,091 | 248,364 | 349,224 |
| v1: checked-value copy helper | 1,124,243 | 251,124 | 349,240 |
| v2: explicit constructor argument | 1,124,466 | 251,232 | 349,240 |
| v3: shared plan publication and packed call arguments | 1,124,008 | 250,888 | 349,240 |
| v4: update independently owned checked values | 1,123,993 | 250,836 | 349,240 |

All four miss the registered strict code/QBE reduction and complete non-growth.
They also exceed the existing 1,120,000-byte compiler-QBE ceiling. The 16-byte
complete-artifact increase is not waived as executable alignment. No hosted
performance runs, threshold changes, new markers or adoption are justified.

All four produce exact QBE/status/diagnostics for 53 existing conformance and
benchmark sources plus 19 synthetic literal/call controls. The controls cover
grouping, signs, underscores, 1024/1025, computed operands, nested and repeated
calls, contextual widening and portable-range failure. Their baseline behavior
was established separately; these comparisons are code-equivalence observations,
not new runtime measurements. Both the accepted and candidate compilers emit
the same candidate compiler QBE, and three ordinary same-basename generations
produce byte-identical candidate executables. Reference checking covers 17
compiler files. The first representation also passes 19 focused existing tests.
Full recovery and multi-target acceptance were not attempted for a known size
miss and are not claimed.

## Reproduction and retained artifacts

The four patches in this directory independently apply to the exact baseline
above. They are rejected source snapshots, not active implementation. Use the
repository's pinned reference `5dc09070cf7f88a569279f5e63982a6de59d692c`, QBE 1.3,
`darwin-arm64-v0` and the system C driver. Start with the accepted Native compiler,
build `compiler/src/compiler.trb` to an output named `compiler`, and use each
produced compiler to build the next generation with the same basename. Compare
bytes, `emit-qbe` output, and Mach-O `__text` before considering timing.

Local environment: macOS 26.6.2 (25G83), arm64, Apple clang 21.0.0
(clang-2100.1.1.101), QBE 1.3. CPU model was not recorded; these are artifact
size and code-equivalence observations, not elapsed-time comparisons.

The 19 synthetic inputs are retained in `controls/`; compile each separately
as a file root. They are not one multi-entry project. `observations.json`
records the final variant's exact source-output comparisons; the same 72/72
comparison count holds for each retained variant.

Compiler QBE SHA-256 values:

| Version | SHA-256 |
| --- | --- |
| baseline | `76aacbfbc985fc1a9ffb5c8594bcbdd71a532c17087b203ce26761696caa956a` |
| v1 | `9780fb0625776acffbb5694808e1cfac6661761be1ffd059931898e2046cb201` |
| v2 | `07da6e5adcfeca0a2a45322ddb69e095dde59f4e3672da822953fc7e14ccaf50` |
| v3 | `afc3ddb92cd831742bd53cb385f002f748a44b4a7cdb0d77afa3e6145c6467ce` |
| v4 | `890961b2e83e70647f12c029c118cd6939d3ec75b642be224abe410fbf4e9b9b` |

## Next action

#254 and #215 remain open. Revisit literal ownership with a representation that
removes enough existing checking/adapter storage and construction to recover
its measured cost, rather than adding a new allowance. In the meantime, an
independent optimization of already verified Integer operations can be measured
without expanding MIR coverage or adding source analysis to the emitter. Source
organization continues in bounded responsibility-based moves. No Pages snapshot
is replaced by this compiler-only rejected diagnostic.
