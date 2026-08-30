# Decision 0022: Linux arm64 LLD Linker

## Status

Accepted for the Gate 6M experiment.

## Context

The first formal Gate 6M run closed an exact Linux arm64 B2/B3/B4 compiler
chain and passed the registered correctness checks, but each compiler was
333,608 bytes. That exceeded the immutable 310,000-byte per-target bound in
[issue #113](https://github.com/type-rb/type-rb-native/issues/113). The failure
is preserved by
[workflow run 33316156337](https://github.com/type-rb/type-rb-native/actions/runs/33316156337).

The compiler code and target-neutral QBE were already deterministic. ELF
inspection instead identified about 60 KiB of file padding in the GNU-linked
layout: load segments retained 64 KiB alignment while RELRO placement advanced
the final writable segment. The size problem therefore belongs to the explicit
Linux link recipe, not the TypeRB language, frontend, runtime semantics, or QBE
program.

Controlled links of the same generated assembly produced these raw compiler
sizes:

| Link recipe | Bytes | Relevant consequence |
| --- | ---: | --- |
| GNU linker, registered Gate 6D flags | 333,608 | Preserves 64 KiB segment alignment and RELRO |
| GNU linker with 4 KiB maximum page size | 276,264 | Narrows compatibility with 64 KiB-page Linux kernels |
| GNU linker without RELRO | 273,128 | Removes a hardening property |
| LLD with the registered stripping flags | 273,232 | Preserves 64 KiB segment alignment, PIE, RELRO, and immediate binding |

## Decision

The internal `linux-arm64-v0` profile passes `-fuse-ld=lld` to the supplied
GCC- or Clang-compatible C toolchain driver. It retains
`-Wl,--gc-sections,--strip-all` and the existing `-lm` boundary. The
`darwin-arm64-v0` profile and the target-neutral emitted QBE remain unchanged.

LLD is an explicit external component of the Linux arm64 toolchain. Linux
bootstrap, runtime-memory, and Gate 6M workflows must install it. Verification
must record its version, observe `ld.lld` in the current-runtime transition and
ordinary application-build process traces, and inspect the resulting ELF
segments and dynamic flags. A missing LLD installation is an environment error;
the compiler does not silently fall back to another linker for this profile.

The selection is compiler-build orchestration data only. Project-only linker
strings and dispatch state are omitted from ordinary application QBE, just like
the existing project walker and compiler-owned C-driver adapter.

This decision amends the Linux linker selection in
[Decision 0011](0011-linux-arm64-target-profile.md). It does not change that
decision's historical Gate 6D result or make the experimental target profile a
stable TypeRB interface.

## Consequences

- The registered Gate 6M compiler-size threshold remains unchanged.
- Linux arm64 compiler and application builds have a declared QBE, C-driver,
  LLD, system-library, and loader boundary.
- Exact Native-to-Native fixed points remain mandatory; changing the linker
  does not permit post-link normalization.
- Linux environments that provide the C driver but not LLD cannot use the
  current `linux-arm64-v0` recipe.
- Darwin behavior and portable application QBE hashes are not affected by the
  profile-specific selection.

## Alternatives considered

### Raise the Gate 6M size threshold

Rejected. The threshold was registered before formal measurement and the
excess came from a replaceable linker layout rather than required compiler
capability.

### Force a 4 KiB maximum page size

Rejected. It would meet the size bound but narrow the resulting executable's
kernel-page-size compatibility. The selected LLD layout meets the bound while
retaining 64 KiB segment alignment.

### Disable RELRO

Rejected. It would meet the size bound by removing an executable-hardening
property. LLD retains GNU RELRO and immediate binding at nearly the same size.

### Compress or rewrite the compiler after linking

Deferred. No post-link transformation is needed, and introducing one would
complicate executable identity, process evidence, and distribution without
addressing the linker-layout cause.
