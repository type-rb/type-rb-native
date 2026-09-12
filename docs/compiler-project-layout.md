# Ordinary compiler project layout

`compiler/src/` is the canonical ordinary compiler source closure.
`compiler/conformance/` contains its authored behavior and diagnostic cases;
`compiler/trbconfig.jsonc` is the reference-side project configuration.
The [architecture](architecture.md) records current module responsibilities.
There is one implementation tree, with no old-path copy, symlink or forwarding layer.

Ordinary builds start at the canonical entry and follow explicit imports.
Snapshot recovery validates that closure and derives a temporary flattened input;
it does not replace normal source loading. `src/compiler_recovery_layout.trb`
records every canonical module and exact import prefix. Recovery reading, flattening
and staging consume that inventory; module mutation controls cover its dependencies. Source moves update imports, recovery,
CLI staging, tests, CI routing and operational consumers together.

Cross-revision measurement controllers use `tools/compiler-project.sh` from the
controller checkout and resolve each source root independently. The helper accepts
the current or authenticated historical project layout, rejects ambiguous/missing
projects, and runs before timing. It is not a compiler subprocess.

Source that helper before `tools/native-mir-transition-policy.sh`. Moved markers
retain their identity and cannot grant a historical transition allowance again.
Frozen baseline paths, negative layout/rename tests and immutable records remain
reproduction inputs. Their original layouts are available through the
[historical record](history.md); current source has no compatibility aliases.
