# Decision 0012: File-root module closure

## Status

Accepted for the Gate 6E experiment.

## Context

The self-hosted compiler could compile one source file, but a useful TypeRB
application is normally a graph of explicitly imported files. Pulling every
sibling into a build would disagree with the reference compiler, make broken
unrelated files observable, and erase module-local declaration identity.
Adding configured projects or packages at the same time would also turn an
internal feasibility slice into a premature public project contract.

The larger emitted program exposed two existing backend problems: the Gate 4
runtime checked machine-word overflow instead of TypeRB's portable Integer
range, and hot scalar and Array operations crossed outlined runtime helpers on
every loop iteration.

## Decision

The existing experimental file commands treat their source argument as the
entry of a config-free file-root program:

- the entry directory is the lexical source root;
- only the entry and the transitive closure of named project imports are
  loaded;
- optional `.trb`, direct-file precedence, and `name/index.trb` fallback match
  the pinned reference compiler;
- absolute, escaping, empty, package, and unsupported import forms are rejected;
- every module is read once and retains its own declaration namespace;
- only the entry module may provide the executable `main`; and
- the hidden source-content recovery adapter remains deliberately single-file.

File existence and reading are TypeRB-declared compiler intrinsics lowered by
the compiler executable entry. They are not language APIs or host-language
fallbacks. QBE and the system linker remain explicit external components.

Checked arithmetic now enforces the portable range
`-9007199254740991...9007199254740991`, including literal rejection and exact
runtime failure classes. The emitter may inline checked arithmetic and
constant Array addressing only in loop bodies. A deterministic whole-program
code-size budget is selected from declaration count: small applications get a
larger budget, medium programs a smaller budget, and large compiler-like
programs retain outlined helpers. Exhausting the budget changes only code
shape, never checking or failure semantics.

## Consequences

The self-hosted path can compile a representative multi-module executable
without Go, while unrelated siblings and module-local same-name declarations
remain safe. The same B1-to-B2-to-B3-to-B4 closure still applies to the full
compiler source.

This decision does not stabilize the CLI, import resolver, module identity,
intrinsics, or optimization policy. Configured projects, namespace imports,
packages, incremental loading, source-map quality, and production standard
library boundaries remain later work. Any promotion must be designed in the
reference TypeRB repository without Native gate terminology.
