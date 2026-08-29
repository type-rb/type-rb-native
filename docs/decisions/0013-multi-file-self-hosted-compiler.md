# Decision 0013: Multi-file self-hosted compiler closure

## Status

Accepted for the Gate 6F experiment.

## Context

Gate 6E proved that the Native compiler can load and compile a representative
file-root graph, but the compiler itself remained one 153 KB source file. That
left the new module path outside the most important self-hosting workload and
made further compiler maintenance unnecessarily monolithic.

The hidden recovery adapter deliberately accepts one source string. Expanding
that adapter into another project loader would duplicate the ordinary loader
and blur the boundary between recovery and normal compilation. Keeping a
second checked-in flattened compiler would instead create two sources of truth.

## Decision

The canonical compiler becomes an explicit TypeRB file-root closure:

- `compiler.trb` remains the entry and owns the frontend, emitter, compiler
  driver, and executable `main`;
- `storage.trb` owns the chunked Integer and String storage records and
  helpers;
- `path.trb` owns pure String and lexical path helpers; and
- the entry imports every cross-module type and function explicitly without
  transitive re-export.

The pinned reference bootstrap snapshot consumes that real closure. Recovery
may derive one temporary single-source equivalent by removing the exact
checked import prefix and concatenating the two imported sources. The
TypeRB-authored recovery utility validates that derivation and records its
inputs; no flattened source is committed. The hidden adapter remains
single-source and only prepares the initial seed.

Every ordinary generation starts from `compiler.trb` as a file path. B1 loads
the three-module closure to build B2, B2 builds B3 from the same closure, and
B3 builds B4. Exact B2/B3/B4 bytes and QBE, rather than the recovery seed
shape, define the self-hosted fixed point.

## Consequences

The compiler exercises its own module resolver on every normal regeneration,
and extracted declarations have one TypeRB source of truth. Recovery remains
available from the pinned reference compiler without entering measured or
ordinary builds.

Module filenames, import identities, the flattening utility, bootstrap
snapshot, and compiler command remain internal and unstable. This decision
does not add configured projects, packages, namespace imports, a public CLI,
or a TypeRB reference-repository dependency on Native.
