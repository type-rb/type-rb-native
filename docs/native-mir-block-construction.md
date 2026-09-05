# Native MIR block-row construction

Status: accepted in [PR #250](https://github.com/type-rb/type-rb-native/pull/250),
merged as `a1c5177583d26bea264b288ca1d8ea54af40afc6`.

[Issue #249](https://github.com/type-rb/type-rb-native/issues/249) and its
[pre-implementation baseline](https://github.com/type-rb/type-rb-native/issues/249#issuecomment-5549924209)
register a compiler-only recovery slice against
`5a23176040fee3541ed8578115622ffcd7aa2733`.

`gate4_mir_block` now owns the internal 16-cell block layout instead of eight
inline Array constructors in MIR commit. Its named arguments identify the
block, source origin, parameter and instruction ranges, terminator, condition,
successors, edge arguments, and return value. Every invocation returns a fresh
mutable row. Publication order and all caller-supplied values remain unchanged.
The verifier and QBE adapter are not changed.

The constructor test independently spells every expected cell for branch,
return, and trap rows. Mutating one branch's identity, origin, and edge-argument
start must not affect a second invocation. The existing independently authored
MIR verifier fixtures retain their literal rows rather than reusing the builder
as their oracle.

## Local evidence

The compiler source SHA-256 is
`869761c3c5474f42ffca66a45eac952d5a0cca804f986a6f572ba13e63aa9a1f`;
the compiler-test source SHA-256 is
`d3a90291169ce7092a776500b78449b3dcf6d2e3fcf0013bd432c74ff5458179`.
Using QBE 1.3 and Apple clang 21 on Darwin arm64, the three ordinary Native
generations produce identical compilers. The target-neutral compiler QBE is
1,116,173 bytes, a 2,849-byte reduction from 1,119,022, with SHA-256
`1ab2f14c2aa5bd692eccef4032d89f9e5951c3066d4faeb97721eae13de8a2f5`.
The compiler code section shrinks from 249,956 to 248,800 bytes. The complete
349,224-byte executable remains unchanged in size because of alignment.

All 22 valid, three mutation, and eleven runtime-invalid Native programs retain
byte-identical QBE and exact runtime output, diagnostics, and status. All three
language benchmark sources retain byte-identical QBE and Darwin executables.
The pinned reference compiler exports the isolated compiler closure to snapshot
v4 successfully. Focused constructor, MIR, scalar, and Array tests pass. All
80 root tests and 90 compiler tests pass with the pinned reference compiler
and QBE explicitly enabled, exercising recovery and ordinary self-hosting
rather than counting skipped optional work. Root formatting and root/core type
checks also pass.

## Acceptance and remaining scope

Require at least 1,000 bytes of target-neutral compiler-QBE reduction, strict
same-run code-section shrinkage on both arm64 targets, and non-growing complete
compilers. Preserve the existing absolute ceilings, 1.05 build-wall/RSS ratios,
2.0 catastrophic limit, fully enabled recovery tests, fixed points, target and
memory regressions, and byte-identical generated application QBE.

The [exact-head formal run](https://github.com/type-rb/type-rb-native/actions/runs/33950334542)
at `f96552344d546bf0805d6b3a2df7698a04cbc5a9` passes all required checks.
Direct inspection of both target artifacts additionally confirms the stricter
issue-specific code-section and QBE shrink conditions, rather than treating
the ordinary 1.05 CI size allowance as sufficient.

| Target | Complete bytes, before → after | Code bytes, before → after | Build-wall ratio | RSS ratio |
| --- | ---: | ---: | ---: | ---: |
| Darwin arm64 | 349,224 → 349,224 | 249,956 → 248,800 | 1.015267 | 1.000596 |
| Linux arm64 | 315,256 → 313,768 | 252,640 → 251,152 | 1.020921 | 0.998320 |

Both targets emit the same 1,116,173-byte QBE identity recorded above. Complete
compilers total 662,992 bytes, 1,488 bytes below the same-run baseline. The
28 retained interleaved build observations per target independently reproduce
the published medians; all retained and adjacent closure observations pass the
2.0 catastrophic bound. No marker or numerical limit changes.

This change improves representation ownership and compiler compactness. It
makes no application-speedup claim and introduces no new semantic fact, ABI,
runtime, or language behavior. Recovering the complete temporary MIR allowance
and removing the remaining direct-emitter semantic ownership are still due.
