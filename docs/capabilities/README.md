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

## Maintenance boundary

This catalog is the public, project-wide coverage view. It is not a task
tracker, roadmap, changelog, or record of work in progress.

Update `catalog.js` when a merged public result changes at least one
capability's status, scope, description, or best evidence link. Set
`catalog.updatedAt` to the date of that coverage review. A `verified` entry
must link to reproducible evidence already present in this public repository;
`partial` may omit a link when the remaining coverage is described accurately.

Do not add an entry for every implementation or optimization. If a result
improves an already represented capability without changing its catalog state,
leave the catalog unchanged. Formal performance snapshots belong in the
benchmark explorer and should be regenerated only from complete committed
result sets. Planning, prioritization, and current task state remain outside
both public views.

Run the structural check from the repository root:

```sh
node tools/capability-map-check.mjs
```

For local review, serve `docs/capabilities` with any static HTTP server. The
site has no package-manager or build dependency.
