# Experimental Native target profiles

The compiler shares TypeRB semantics, MIR, runtime generation and target-neutral
QBE across the registered profiles. These internal profiles are experimental;
they do not imply a stable installation or product-support commitment.

| Profile | QBE target | Executable and toolchain |
| --- | --- | --- |
| `darwin-arm64-v0` | `arm64_apple` | Mach-O; system assembler/linker through the registered C toolchain driver. |
| `linux-arm64-v0` | `arm64` | ELF; system assembler and LLD. |
| `linux-amd64-v0` | `amd64_sysv` | ELF; system assembler and LLD. |

Current [target validation](../.github/workflows/linux-amd64-targets.yml) checks
ordinary compiler generations, application results and failure behavior, executable
identity/dependencies, process boundaries and target-neutral output equality.
Unknown profiles fail before source or tool access. Compiler-owned builds invoke
explicit tool paths directly and publish output only after all phases succeed.

Darwin and Linux arm64 have [verified immutable checkout seeds](bootstrap-seed-updates.md).
Linux amd64 currently derives its setup compiler from the immutable initial root
and exact accepted source transitions. That recovery/setup evidence remains
separate from ordinary candidate self-hosting; it is not a published amd64 seed.
The checkout launcher currently bootstraps on the two arm64 platforms.

See [CI validation](ci-validation.md) for integration requirements and the
[historical target contracts](history.md) for source-era observations. Migration
correctness checks do not establish final Pure Go performance qualification.
