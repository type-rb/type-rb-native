# TypeRB Native capability map

This directory contains a dependency-free static capability map for the
experimental TypeRB Native project. It deliberately catalogs capabilities
before they become scheduled implementation work.

The four evidence states have narrow meanings:

- `verified`: reproducible public evidence exists for the stated scope;
- `partial`: some behavior exists, but coverage or evidence remains incomplete;
- `open`: the capability is needed but not implemented or verified; and
- `unassessed`: the capability is cataloged, but its exact gap has not been
  inventoried.

These states do not create a support promise, compatibility guarantee, or
product commitment. Public evidence links point only to this repository.

Run the structural check from the repository root:

```sh
node tools/capability-map-check.mjs
```

For local review, serve `docs/capabilities` with any static HTTP server. The
site has no package-manager or build dependency.
