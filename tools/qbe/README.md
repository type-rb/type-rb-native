# Native QBE variant

`backend.json` pins the QBE 1.3 release archive and all three patch digests.
`python3 tools/qbe_toolchain.py /path/to/qbe-1.3` verifies them, applies the
patches without fuzz, builds QBE and checks supported-target instruction emission.
The binary's receipt records upstream, patch, builder and C compiler identities.
Checkout builds include those tracked inputs in their content cache. An explicit
`TRBN_QBE` override must support the same operations and ARM64 operand selection.

The six added upstream lines define a unary single/double floating-point `sqrt`
and select `fsqrt`, `sqrtss` or `sqrtsd`. Native uses the double form only for
the independently verified standard `Math.sqrt` declaration. Other declarations and existing callable paths retain the ordinary call ABI.
Directly taking a standard module function as a value remains unsupported by
Native; an ordinary wrapper function can be passed as a callable.
There is no constant folding, fast-math mode or new runtime helper. Native does
not expose libm `errno`; observable floating-point results remain the contract.

The external C driver is a test, not compiler or runtime implementation. It
compares both scalar widths with libm under four rounding modes, including
signed zero, subnormals, infinities, NaNs and deterministic random bit patterns.
Run `python3 tools/qbe_sqrt_test.py --qbe /path/to/qbe` on arm64 and amd64.
RV64 and Windows emission are checked; those are not supported Native runtimes.

`arm64-immediates.patch` retains encodable integer constants in the second
operand of addition, subtraction, bitwise operations and shifts. It reuses QBE's
immediate classifiers, normalizes word constants and reduces shift counts modulo
the result width as required by the IL. Unsupported constants, variable operands,
addresses and floating-point operations keep ordinary register selection. Logical
masks use their own printing rule instead of the arithmetic `lsl #12` suffix.
Run `python3 tools/qbe_integer_test.py --qbe /path/to/qbe` for an independent
fixed-width arithmetic oracle, signed and unsigned boundaries, oversized shift
counts and fallback controls. AMD64 tests pass negative and oversized shift
counts through registers because its upstream emitter does not normalize them
to assembler immediates; ARM64 tests retain these immediate cases.
`--baseline /path/to/previous/qbe` also compares
unchanged AMD64 emission. The patch adds no target-independent optimization or
runtime helper.

`arm64-memory.patch` folds a single-use address addition into a load or store
when its register base and positive, naturally aligned constant offset fit the
instruction. It uses the existing memory operand representation and shared
liveness, spilling and register allocation. Multiply used addresses, frame and
symbol addresses, variable offsets and unsupported displacements retain the
ordinary path. Address definitions are inspected before instruction storage is
replaced. No memory operation moves or changes width.
Run `python3 tools/qbe_memory_test.py --qbe /path/to/qbe` for byte-level load/store
checks, signed extension, floating-point bit preservation, displacement bounds,
fallbacks and enough live base pointers to require spilling. Its optional
`--baseline` control compares AMD64 emission with the preceding backend.

Maintenance is three small pinned patches, one acquisition helper and target/edge tests.
A QBE upgrade must rebase the patches, run upstream tests, run these controls on
each supported host, and repeat ordinary compiler validation. Historical seed
manifests and their replay workflows retain their original stock QBE identity;
the current compatibility schema records this variant separately. No patched
binary is mislabeled as an upstream release.
