# TypeRB Native benchmark explorer

This dependency-free static page presents the committed formal TypeRB Native
runtime and build evidence without replacing the result records or benchmark
methodology. It does not fetch mutable data at runtime.

Generate the committed page data from the repository root:

```sh
node tools/benchmark-pages-data.mjs
```

Check that the generated data still matches every source TSV and that the
public page retains its structural and evidence boundaries:

```sh
node tools/benchmark-pages-data.mjs --check
node tools/benchmark-pages-check.mjs
```

The displayed comparisons are limited to the exact programs, inputs, hosts,
toolchains, and metrics documented by the linked formal results. No composite
language score or general application-performance claim is implied.

## Updating the snapshot

Refresh this page only from a complete committed formal result set that passes
its registered correctness and measurement boundaries. Update the result roots,
case matrix, platform metadata, and snapshot date in
`tools/benchmark-pages-data.mjs`, regenerate `data.js`, and rerun both checks.
Review the page copy whenever the derived ranges or conclusions change.

Keep focused optimization measurements and partial reruns in their own result
records. Do not mix them into this cross-language snapshot. The explorer shows
one internally consistent selected snapshot; the linked result directories
remain the historical and reproducible source of truth.
