# Gate 6B Native Single-File Build

Gate 6B extends the measured Gate 6A file entry into a Go-free, self-hosted
single-file executable build. Its acceptance criteria and non-inferiority
bounds were registered before implementation in
[issue #39](https://github.com/type-rb/type-rb-native/issues/39). The ownership
and process boundary is defined by
[Decision 0009](decisions/0009-native-single-file-build.md).

## Status

The implementation candidate is active. Gate 6B does not close until its
focused benchmark, raw observations, process inventory, and summarized result
pass the registered bounds. This is not the complete Gate 6 product-feasibility
exit and does not create a supported TypeRB command.

## Experimental command

Self-emitted B1 and later compiler generations accept:

```text
compiler build SOURCE --output OUTPUT --qbe QBE --cc CC
```

The order is fixed for this experiment. `SOURCE`, `OUTPUT`, `QBE`, and `CC` are
literal process arguments, so paths containing spaces require no shell quoting
inside the compiler. `check SOURCE` and `emit-qbe SOURCE` remain unchanged.

The exact usage is:

```text
usage: compiler {check|emit-qbe} SOURCE
       compiler build SOURCE --output OUTPUT --qbe QBE --cc CC
```

| Condition | stdout | stderr | Exit status |
| --- | --- | --- | ---: |
| Build succeeds | empty | empty | 0 |
| Compiler diagnostic | empty | deterministic diagnostic | 1 |
| Invalid command shape | empty | exact usage | 64 |
| Unreadable source | empty | path-bearing read error | 66 |
| Intermediate or publication failure | empty | exact operation diagnostic | 73 |
| QBE or CC failure | inherited child stdout, if any | inherited child stderr plus exact phase diagnostic | 70 |

Child stdout is inherited, but the registered QBE and CC invocations do not
write stdout on success. The driver does not translate child diagnostics; it
adds only `compiler: qbe failed` or `compiler: cc failed` after a failed child.

## Owned and external work

Repository-owned TypeRB source performs:

- source-file reading and checked compiler execution;
- QBE IL redirection and stdout restoration;
- argument-vector construction;
- direct `fork`/`execv` child launch and `waitpid` status decoding;
- phase diagnostics and command exit mapping;
- intermediate cleanup; and
- atomic final publication.

The supplied QBE binary, `/usr/bin/cc` in the registered measurement, the
assembler and linker it drives, the Darwin SDK, libc, and other system
libraries remain explicit external components. The ordinary build graph is:

```text
Native compiler
    -> QBE
    -> CC
        -> assembler/linker
```

It contains no Go compiler, reference `trb`, shell, or hidden source-content
adapter.

## Artifact lifecycle and reproducibility

The driver writes `OUTPUT.trbn.ssa` and `OUTPUT.trbn.s`, then creates an
adjacent `OUTPUT.trbn.XXXXXX` directory. The temporary executable has the same
basename as `OUTPUT`; after successful linking it is renamed atomically over
the requested path. Every success and failure path removes the `.trbn.ssa`,
`.trbn.s`, temporary executable, and temporary directory.

Using the same basename preserves Darwin's ad-hoc code-signature identifier.
The integration suite therefore requires byte-identical output among B1, B2,
and the external file-emission/QBE/CC recipe when each recipe links an output
with the same basename. The default content-derived Mach-O UUID and arm64
ad-hoc signature remain intact and the resulting program must execute.

## Correctness coverage

The bootstrap integration suite retains B1/B2/B3 compiler-QBE identity and the
Gate 5 normalized compiler-executable check, then adds:

- B1 and B2 builds of every valid and mutation conformance source;
- expected runtime behavior for every produced executable;
- byte-identical B1, B2, and external-recipe application outputs;
- B1 and B2 rejection of every invalid source before deliberately failing
  external tool paths can run;
- exact usage, unreadable-source, intermediate, QBE, CC, and publication
  failures;
- preservation of child stderr and observation of nonzero child status;
- replacement of an existing output only after a complete successful link;
- source, output, and tool paths containing spaces; and
- absence of every `*.trbn.*` artifact after success or failure.

## Registered measurement

After two warmups, seven alternating observations use the checked-in compiler
source to compare Native-owned `build` with the established external
`emit-qbe`/QBE/CC recipe. The run records elapsed time, observed
orchestration-root peak RSS, B1/B2 convergence, executable runtime and size,
stripped compiler size, exact process inventory, machine and tool versions,
and raw rows.

Native-owned time and RSS must remain within 25% of the external recipe, B1 and
B2 must remain within 25% of each other, produced executable behavior and size
must not regress, and stripped compiler size must remain at or below 172,251
bytes (15% above the 149,784-byte Gate 6A compiler). Any correctness mismatch,
leaked intermediate, unexpected process, or greater-than-2x time/RSS regression
stops the slice for diagnosis.

The TypeRB-authored
[`gate6b-benchmark`](../tools/gate6b-benchmark/README.md) harness constructs the
fixed point, runs the correctness and executable-identity preflight, records
two indexed warmups and alternating observations, enforces the compiler-size
ceiling, and writes the exact process inventory. Its external comparison mode
retains `.ssa` and `.s` files, while Native `build` includes its required
cleanup in every measured observation.

## Deferred scope

This slice supports one source file, one output, explicit tool paths, and
Darwin arm64. Project discovery, module graphs, package and native-library
boundaries, production runtime integration, incremental builds, toolchain
selection, a second target, debugging, release bootstrap, and stable CLI design
remain later work.
