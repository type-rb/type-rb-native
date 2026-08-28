# Gate 6A File-Oriented Compiler Entry

Gate 6A begins self-hosted product-feasibility work by giving the Native
compiler an ordinary file-oriented entry. Its registered acceptance criteria
and performance bounds are in
[issue #35](https://github.com/type-rb/type-rb-native/issues/35), and the
boundary is defined by
[Decision 0008](decisions/0008-file-oriented-compiler-entry.md).

## Status

The implementation and correctness coverage are present. Gate 6A remains open
until the registered direct-time, peak-RSS, stripped-size, process-inventory,
and fixed-point measurements are recorded and reviewed.

This slice is not the complete Gate 6 exit and does not create a supported
TypeRB command. Project discovery, multi-module resolution, output management,
QBE and linker orchestration, production managed-runtime integration,
incremental builds, package and native-library boundaries, another target,
debugging, and maintenance evaluation remain later work.

## Experimental command boundary

The self-emitted B1 and later compiler generations accept:

```text
compiler check SOURCE
compiler emit-qbe SOURCE
```

`SOURCE` is a filesystem path. The compiler reads the file itself and does not
place source contents in the process argument vector.

| Condition | stdout | stderr | Exit status |
| --- | --- | --- | ---: |
| `check` succeeds | `ok` | empty | 0 |
| `emit-qbe` succeeds | deterministic QBE IL | empty | 0 |
| compiler diagnostic | empty | one deterministic diagnostic | 1 |
| invalid command or mode | empty | exact usage | 64 |
| unreadable source path | empty | exact path-bearing read error | 66 |

The exact usage line is:

```text
usage: compiler {check|emit-qbe} SOURCE
```

The command currently emits QBE to stdout so the file boundary can be isolated
and measured. It does not yet choose an output path, invoke QBE, or link an
executable.

## Recovery and differential adapter

B0 is a recovery compiler produced from the versioned bootstrap snapshot. It
continues to accept source contents through this explicit hidden form:

```text
gate4-compiler --source-content MODE SOURCE
```

Self-emitted Native compilers and the matched optimized Go artifact retain the
same hidden shape for bootstrap recovery and differential tests. It is not an
ordinary command, compatibility promise, or proposed public API. The explicit
flag prevents file paths and source contents from sharing an ambiguous argv
shape. The adapter can be removed after ordinary releases no longer need the
B0 recovery route for the relevant checks.

## Ownership and runtime boundary

The entry generator, file handling, stderr routing, compiler frontend, and QBE
emitter are repository-owned TypeRB source. The emitted runtime uses libc
`fopen`, `fseek`, `ftell`, `fread`, and `fclose` behind the existing explicit
system boundary. File-oriented `check` and `emit-qbe` do not spawn Go, the
reference compiler, a shell, QBE, a linker, or another process.

The authored compiler entry returns an internal status and selects stdout or
stderr diagnostic routing according to its adapter. This is an implementation
boundary, not a TypeRB language change and not a replacement for ordinary
`def main()` semantics.

## Correctness evidence

The bootstrap integration test builds B0, B1, B2, and B3, then requires:

- byte-identical B1/B2/B3 compiler QBE;
- retained normalized B1/B2 executable identity;
- B1 and B2 file-oriented results equal to the hidden adapter for the compiler
  source and every valid, invalid, and mutation conformance input;
- diagnostics only on stderr with status 1 and no partial QBE;
- exact usage and unreadable-path behavior; and
- successful checking of a valid source file larger than 512 KiB.

The large-file case also keeps the lexer hot path from allocating a new stack
slot per input byte. This prevents compiler stack consumption from growing
linearly for long runs of whitespace and proves that the source is read from
the file rather than smuggled through argv.

## Registered measurements

After two warmups, seven alternating observations compare B1 and B2
file-oriented `emit-qbe` with the hidden source-content path for the checked-in
compiler source. File-oriented median time and peak RSS must remain within 25%
of the hidden path, adjacent Native generations must remain within 25%, and the
stripped compiler may grow by at most 10% from the Gate 5 baseline. A complete
process inventory and raw machine-readable observations are committed before
Gate 6A closes.
