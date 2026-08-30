# Gate 6E File-root Multi-module Executables

Gate 6E extends the ordinary self-hosted file commands from one source unit to
an explicit import closure. Its registered boundary and measurement criteria
are recorded in [issue #51](https://github.com/type-rb/type-rb-native/issues/51),
and its ownership decision is [Decision 0012](decisions/0012-file-root-module-closure.md).

## Status

Gate 6E is complete at measured TypeRB Native revision
`b2b4740f39571dc35af9199dae817d94912b7a47`. The reviewed Darwin arm64
measurements, exact Native compiler closure, and pinned Linux arm64 correctness
run are recorded in the
[Gate 6E result](../results/2026-08-29-gate6e-file-root-darwin-linux-arm64/README.md).
This remains an internal experiment rather than a supported project or command
format.

The direct candidate selection described below remains valid when its index
peer never enters the file-root closure. The later
[TypeRB 0.4 compatibility mapping](type-rb-compatibility.md) additionally lets
one directory index resolve through either equivalent authored path and rejects
a resolved graph containing both peer module identities.

## File-root boundary

At the recorded Gate 6E revision, `check SOURCE`, `emit-qbe SOURCE`, and
`build SOURCE ...` treated `SOURCE` as the entry module and its directory as
the source root. The compiler loaded only transitive named project imports. It
accepted an optional `.trb` suffix, checked `name.trb` before
`name/index.trb`, read one snapshot per canonical module, and ignored unrelated
siblings.

Module ownership survives parsing, resolution, checking, and emission. Imported
records and functions resolve only through explicit bindings, same-named local
declarations in different modules remain distinct, and the entry module alone
owns `main`. Unsupported import forms and every graph, binding, usage, syntax,
and entrypoint error fail before QBE or CC starts.

The checked-in five-module application covers nested imports, a diamond,
directory-index fallback, records, calls, loops, Arrays, Strings, and
same-named private functions. Its invalid sibling proves that directory
enumeration is not part of the closure. Integration coverage also checks paths
with spaces, the then-current direct-file precedence, optional suffixes,
cycles, repeated exact application bytes, the optimized Go oracle, and the
exact B2/B3/B4 compiler fixed point.

## Shared emitted-code correction

The first performance probe found that the self-hosted emitter called runtime
helpers for every checked Integer operation and Array index. It also exposed
that those helpers used the wider int64 boundary rather than TypeRB's portable
Integer range. Gate 6E therefore corrects the shared runtime and emitter rather
than weakening the application:

- literals and results use the portable ±9,007,199,254,740,991 boundary;
- division-by-zero and range failures remain checked on every path;
- hot-loop arithmetic and safe constant Array addressing may be inlined; and
- deterministic program-size budgets keep the self-hosted compiler compact.

The formal alternating result places Native runtime 13.70% above optimized Go
and inside the registered 25% boundary. Native builds 44.89% faster, uses
48.22% less build RSS and 65.32% less runtime RSS, and produces a stripped
application 97.82% smaller than Go with no overhead relative to flattened
Native. The fixed-point compiler is 199,992 stripped bytes. The TypeRB-authored
[`gate6e-benchmark`](../tools/gate6e-benchmark/README.md) records the compiler
closure, raw series, hashes, dependency inventory, and recovery provenance.

## Deferred scope

Configured `trbconfig.jsonc` projects, namespace imports, packages, stable
module identities, incremental caches, automatic tool discovery, production
runtime integration, source maps, and public CLI design remain deferred. The
hidden source-content adapter remains single-file recovery infrastructure.
