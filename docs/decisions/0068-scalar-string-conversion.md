# Scalar String conversion through verified MIR

Float and Boolean `to_s` take no arguments and return a String. Float `puts`
uses the same conversion before the existing String output operation. The
pinned reference defines shortest-roundtrip fixed decimal notation, `.0` for
whole values, `0.0` for either signed zero, and `NaN`, `Infinity` and `-Infinity`
for non-finite values. Boolean conversion returns `true` or `false`.

MIR conversion instruction 17 adds mode 4 for Float-to-String and mode 5 for
Boolean-to-String. Verification independently requires the exact scalar operand,
String result and unary shape. Float conversion has allocation/failure effects;
Boolean conversion returns immutable static text without allocation. Ordinary
root liveness retains values across Float formatting. Backend adapters translate
the verified mode without interpreting source expressions or receiver methods.

The TypeRB-owned runtime uses system `snprintf` and `strtod` to search significant
precision from one to seventeen digits and verify round trips. At a power of
two the lower binary rounding interval is narrower than the upper interval.
If the nearest decimal falls below the value and does not round trip, the
runtime also checks the next greater decimal coefficient before adding another
digit. Checking only the nearest decimal produces unnecessarily long output at
these boundaries. The selected decimal digits and exponent are expanded directly;
formatting the original binary value with `%f` would expose its binary tail.

Binary64 bounds the candidate to 64 bytes and fixed output to 384 bytes, including
sign and the smallest subnormal. Both are temporary stack buffers. Finite nonzero
results allocate one ordinary String; zero and non-finite results share static
descriptors. The small precision loop favors bounded implementation over final
conversion throughput; a faster decimal algorithm may replace it under the same
MIR and output contract after measurement.

The REPL calls ordinary Float `to_s` from its TypeRB implementation. The existing
immutable seed builds the core, and that core builds the CLI with the new method;
no seed, snapshot-format or host formatting fallback is added. General REPL value
display remains a separately tracked surface.

Shared ordinary check/build/run/REPL cases cover finite and non-finite values,
smallest/largest values, asymmetric intervals, receiver effects, optional calls,
constant initialization, retained callbacks and invalid signatures/results.
Independent MIR tests erase source, reorder instructions, force collection and
forge conversion modes. The CLI test uses an independent shortest-roundtrip
oracle for all 2,098 binary64 binades and adjacent values (8,392 conversions),
then verifies retained values and replay. Both target CLI authorities execute it.
