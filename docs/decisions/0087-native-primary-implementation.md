# Native as the primary TypeRB implementation

Status: proposed for maintainer review.

## Context

Today the Go implementation in `type-rb/type-rb` is the language and
conformance source of truth. Native follows an exact revision recorded in
`TYPE_RB_REVISION`, uses it as a differential oracle and recovery compiler, and
keeps it consumer-neutral (`AGENTS.md`).

Native's goal is the complete TypeRB toolchain: the `trb` mode for Native
executables, the `go`, `ruby` and `typescript` source modes, the everyday
commands and the official packages. [Decision 0086](0086-production-web-application-path.md)
sets the package path and the rule of one project configuration for every mode.

The maintainer's direction is to invert the relationship once Native covers
the language and tooling:

- Native becomes TypeRB. Its command becomes `trb`.
- The Go implementation continues in parallel as a reference under another
  command name, such as `trbg`, for as long as it is useful. It may be retired.

## Decision

Native becomes the primary TypeRB implementation. The Go implementation becomes
a parallel reference and differential oracle.

The change happens in three phases.

1. **Now: the reference is still the source of truth.** Native follows
   `TYPE_RB_REVISION`, and closes basic-language coverage (#454), the web
   application path (#622) and the missing commands. Specification improvements
   found while reproducing the reference are proposed, not implemented as
   deviations. The reference accepts `mode: trb` for analysis, so one
   configuration works in both implementations during the transition.
2. **Switch: Native takes the `trb` command** once the switch gate below is met.
   The specification and the conformance cases move with the primary. The Go
   implementation follows the specification instead of defining it.
3. **Afterwards: the Go implementation is kept only while it adds value**, as a
   differential oracle, a recovery path or a source-mode builder. Its
   retirement is a separate decision.

### Switch gate

The command name moves only when every item below holds, with evidence recorded
on the tracking issue:

- Basic-language coverage is complete (#454), with no registered pending
  contract.
- Native implements `check`, `fmt`, `lint`, `lsp`, `test`, `install`, `run`,
  `build` and `repl` for `mode: trb`, and matches the frozen scenario manifests
  for them.
- The source modes have an agreed path at the switch (see the open questions).
- Seeds, recovery and releases no longer need the Go implementation for
  ordinary builds.

## Consequences

These documents change at the switch, not before:

- `AGENTS.md`: the source-of-truth and consumer-neutrality invariants.
- `TYPE_RB_REVISION` and `docs/type-rb-compatibility.md`: the reference becomes
  a pinned oracle instead of the definition.
- [Decision 0086](0086-production-web-application-path.md) and the package
  sharing initiative (#636): shared package sources are owned by the primary.
- Distribution, the editor extension's server command, and every document that
  names `trbn`.

Until then, current rules apply unchanged. This decision authorizes no rename,
no specification move and no change in the reference repository.

## Open questions for the maintainer

1. **Source modes at the switch.** How are `go`, `ruby` and `typescript`
   projects built when `trb` becomes Native?
   - Native emits them before the switch. This is the strictest gate and the
     latest switch.
   - Native invokes the Go implementation for the source modes during the
     transition. This allows an early switch but couples the two
     implementations.
   - Users run the Go implementation for the source modes until Native emits
     them. This allows an early switch, but projects in those modes need
     another command.
2. **Where the specification and conformance cases live after the switch.**
   - In this repository.
   - In a neutral specification repository that both implementations pin.
   - In the reference repository, repurposed for the specification.
3. **Repository and command naming.** Whether the repositories are renamed
   along with the commands, and when.
