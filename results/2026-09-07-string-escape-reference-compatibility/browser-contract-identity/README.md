# Browser and JSON contract identity compatibility

This update uses the registered compatibility evidence slot. Earlier observations
retain their original source and reference identities.

The selected development reference is TypeRB `0.4.12-dev` at
`c49b67ec0f9e5941c52b787885f11a33c19f795f`, merged in
[type-rb/type-rb#850](https://github.com/type-rb/type-rb/pull/850).
It preserves defining-module provider contracts, distinguishes caller type
parameters, and retains declaration identity in browser and JSON code generation.
Its complete local Go suite and required PR checks passed. This is an exact
source pin, not a release or supported version range.

The preceding qualified Native main is
`56e5375ffc799967b9b6628f2c13147549863ee9`, validated by
https://github.com/type-rb/type-rb-native/actions/runs/41421430635.
That workflow predates this reference update; it does not qualify the new pin.
Historical manifests and immutable seeds retain their source-era identities.

## Local qualification

Exact-reference and ordinary Native qualification is pending for this candidate.
Record observed results here after the maintained commands complete.

## Scope

The original generated client with application `Body` and the `Payload` control
must both compile through the reference browser backend and pass twelve synthetic
Fetch checks each. Native client generation retains its exact output and rejects
invalid output paths without invoking target tools. Browser backend execution is
reference qualification; it does not establish Native TypeScript output support.
The renamed shared-import gap #1183 and package ownership review #1211 remain
separate. Full shared v0.5 and release qualification remain open.
