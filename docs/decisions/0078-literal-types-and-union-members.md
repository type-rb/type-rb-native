# Literal constraints and common union members in MIR

Follow the pinned reference's explicit Integer/String literal type contract.
An authored literal can satisfy its singleton annotation; computed scalars and
inferred scalar bindings cannot narrow implicitly. Literal values widen to their
ordinary scalar type, and scalar alternatives subsume their literals in unions.
A literal type cannot itself have optional, Array-suffix or generic modifiers.
Containers, declarations and callable signatures can carry literal arguments.

Canonical singleton spellings encode String bytes without syntax delimiters.
They preserve equality across escape spellings and prevent quoted commas, angle
brackets or NUL from changing union/container structure. Compiler byte access has
one source owner shared by the frontend and backend constants.

MIR retains distinct singleton type IDs with a validated scalar representation.
A singleton constant records its exact value and scalar tag; an explicit widening
operation erases its constraint. The independent verifier checks the table,
constant payload, operand availability and result identity after source erasure.
QBE consumes these verified operations as constants and identity copies. No
singleton box, source inspection or runtime type inference is introduced.

Literal unions reuse the existing verified union representation and typed CFG.
Homogeneous alternatives widen through checked edges before numeric operations,
Range construction, ordering and equality. Mixed Integer/String literal cases
compare alternative tags, keeping `0` distinct from `"0"`. Singleton Hash keys
retain their semantic type IDs with the ordinary scalar key representation.
Hash keys formed from literal unions still need a separate verified key layout;
this change does not erase their constraint or accept unverified storage.
Common data members require every nominal alternative to expose the member;
selection lowers through the alternative's verified record layout. Exhaustive
literal cases and branch-local discriminant narrowing belong in semantic
checking and MIR, preserving overlapping alternatives and mutation invalidation.
Classes will reuse this boundary with their separate readonly-field contract.

The REPL preserves the singleton's semantic type independently of scalar storage.
Retained declarations, failed edits and replay must preserve those constraints.
Validation pairs ordinary check/build/execution/REPL observations with explicit
rejection cases, independently forged MIR and forced-GC lifetime controls.
This is part of basic-language completion in #454, not a performance qualification
or a claim that all union, object or generic features are complete.
