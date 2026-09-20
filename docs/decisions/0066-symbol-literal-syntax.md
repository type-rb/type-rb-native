# Symbol spelling with String semantics

Portable Symbol expressions such as `:ready` and `:"a b"` have the reference
String type. Equality, receiver methods, nullable values, generic arguments,
defaults, captures and collection storage use the existing String contracts.
They introduce no intern table, new runtime representation or MIR operation.

A quoted Symbol decodes String escapes without evaluating interpolation-looking
text. The lexer therefore preserves a quote containing live `#{` as raw token
kind 7. The expression parser selects ordinary String expansion or literal
Symbol decoding. Hash entry and named-argument colons retain their own grammar;
the lexer does not infer meaning from a preceding colon.

Expansion occurs at the forward syntax cursor before semantic checking. It
replaces that raw token and moves only the unparsed suffix. Previously published
declarations, defaults and controls keep their origins; later declarations are
cataloged after expansion. Nested expressions follow the same path. Ordinary
quotes without interpolation continue through the existing lexer. A Symbol name
becomes a checked String literal, consumed identically by MIR and the REPL.

This retains the existing token-based parser architecture. Expanding many quoted
expressions still copies future tokens; a linear token-buffer representation is
future compiler organization/performance work. No speedup or complete lexical
coverage is claimed here.

Shared cases cover quoted/identifier/operator names, Unicode and escaped bytes,
literal interpolation spelling, actual String interpolation, Hash labels, named
arguments, defaults, controls, generic aliases, optional results and retained
values. Source-erased and reordered MIR executes under forced GC. Separate CLI
checks retain Unicode/NUL through callbacks and Hashes, preserve later diagnostic
lines and recover a retained session after an invalid escape. Compiler core
self-use of Symbol spelling remains blocked by the preceding immutable seed;
ordinary core and CLI fixed points still verify the complete implementation.

The reference quoted-Symbol validation and Ruby quoting correction is tracked in
[TypeRB PR #747](https://github.com/type-rb/type-rb/pull/747). Single-quote semantics
and unquoted control-keyword framing remain explicit boundaries under
[TypeRB #748](https://github.com/type-rb/type-rb/issues/748) and
[TypeRB #749](https://github.com/type-rb/type-rb/issues/749). Multiline interpolation
also retains a shared reference gap. These cases do not establish complete Symbol
or basic-language coverage. Existing invalid interpolated escapes now reject the
whole REPL declaration, avoiding the former cascade of unrelated body errors.
