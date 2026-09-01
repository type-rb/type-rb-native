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
