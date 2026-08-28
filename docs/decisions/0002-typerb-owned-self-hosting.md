# 0002: TypeRB-Owned Self-Hosting

Status: accepted

## Context

Native code generation alone could remove the Go toolchain from application
builds while leaving the compiler itself implemented in Go. That would test an
important product property, but it would not meet this project's intended
ownership boundary. The desired end state is a TypeRB compiler and runtime
whose maintained implementation is TypeRB and whose ordinary release path can
reproduce the compiler without Go or another host implementation language.

Building a complete frontend before testing native execution would still spend
substantial effort before resolving the runtime, ABI, performance, and
distribution questions. Self-hosting therefore needs to be an explicit later
gate without becoming a prerequisite for the earliest executable experiment.

## Decision

All repository-owned compiler and runtime implementation source is written in
TypeRB. The project is not ported to Rust, Zig, C, or another host language.

External code generators, assemblers, linkers, SDKs, and system libraries are
allowed. Their complete cost and distribution requirements are measured and
reported. Generated backend IR, C, assembly, and object files are compiler
outputs rather than maintained host implementations.

Early gates use the Go reference compiler to compile TypeRB implementation
source and may consume a narrow, versioned, data-only bootstrap snapshot. The
Go compiler remains the semantic reference and differential oracle throughout
the experiment.

Later gates add an independent TypeRB-authored parser, resolver, checker, and
compiler driver. Bootstrap is demonstrated in stages:

1. The Go reference compiler builds the B0 native compiler from TypeRB source.
2. B0 builds the B1 native compiler from the same source.
3. B1 builds B2.
4. B1 and B2 are reproducibly equivalent under the recorded policy and behave
   equivalently on the compiler conformance corpus.

Ordinary releases then use a previous native TypeRB compiler as their seed. A
Go bootstrap remains available for recovery and differential testing, but is
not required by the normal build or release path.

## Consequences

- Native feasibility can be tested before duplicating the complete frontend.
- Gate 0 and later implementation work starts in TypeRB, so early components
  can become part of the self-hosted compiler rather than being rewritten.
- The temporary snapshot boundary remains removable once the independent
  frontend lowers directly to Native MIR.
- Self-hosting performance is measured explicitly; a fast Go-bootstrapped
  prototype does not by itself pass product feasibility.
- Using QBE, LLVM, a linker, or platform libraries does not disqualify the
  compiler from self-hosting, but every dependency remains part of toolchain
  size, build time, portability, licensing, and security evaluation.
- The independent frontend must conform to the reference specification. This
  repository does not gain authority to define a divergent native dialect.

## Alternatives considered

### Keep the compiler implemented in Go

Rejected as the final state because application builds could become native
while compiler development and release bootstrap still depend on Go-owned
implementation source.

### Port the compiler to another systems language

Rejected because it replaces one host-language dependency with another and
does not advance TypeRB self-hosting.

### Replace every external tool

Rejected because self-hosting concerns the implementation owned by this
project. Reimplementing mature code generators, assemblers, linkers, SDKs, or
system libraries is a separate question and would obscure the native compiler
experiment's cost and risk.

### Require self-hosting before native execution

Rejected as an ordering constraint. It would duplicate the complete frontend
before the experiment has shown that the native runtime and backend can meet
their correctness and product goals.
