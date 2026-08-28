# Gate 6D Benchmark Harness

This TypeRB-authored harness verifies and measures the Linux arm64 target chain
defined by
[Decision 0011](../../docs/decisions/0011-linux-arm64-target-profile.md) and
pre-registered in
[issue #47](https://github.com/type-rb/type-rb-native/issues/47). It accepts an
already prepared Linux B1 Native compiler and never runs recovery itself.

The harness:

1. constructs the actual B1-to-B2-to-B3-to-B4 chain with explicit
   `linux-arm64-v0` Native build commands;
2. requires exact B2/B3/B4 compiler bytes, fixed-point QBE, source checks, and
   complete Native-intermediate cleanup;
3. runs every valid, mutation, and invalid file-oriented conformance case
   through B1, B2, B3, and B4, including executable identity and behavior;
4. verifies Linux paths containing spaces, unknown-target rejection before
   tool access, missing source/QBE/CC behavior, and publication failures;
5. records two warmups and the requested alternating observations for each
   Native generation and its equivalent external QBE/CC recipe;
6. records two RSS warmups and up to three observations with GNU `time -v`;
7. records raw and stripped compiler identity and size, the QBE sidecar, the
   fixed-point IL, the environment and seed provenance, and exact tool
   versions; and
8. inspects ELF headers, loader, dynamic dependencies and symbols, then uses
   `strace` to record the ordinary Native-to-QBE-to-CC-to-assembler/linker
   process graph.

The external recipe is a subcommand of this same controller. It starts the
selected Native compiler's `emit-qbe` command, writes the returned IL, and
invokes the same QBE and CC paths. The controller is a measurement observer,
not a child in an ordinary Native build. Its implementation source remains
TypeRB even though the current reference compiler uses Go to build this
out-of-chain measurement executable.

## Pinned environment

Build the Linux arm64 image from the digest-pinned Debian base. The Dockerfile
also verifies the QBE 1.3 archive checksum and records every installed package
version in the image.

```sh
docker build --platform linux/arm64 \
  -f tools/gate6d-benchmark/Dockerfile \
  -t type-rb-native-gate6d:measurement \
  tools/gate6d-benchmark

docker image inspect type-rb-native-gate6d:measurement \
  --format '{{.Id}} {{.Architecture}} {{.Os}}'
```

The exact resulting image ID belongs in `ENVIRONMENT_PROVENANCE` and the result
document. The pinned base digest alone does not conceal package or image-layer
identity: both are retained in the process inventory.

## Controller and seed preparation

Cross-compile the TypeRB-authored controller with the pinned TypeRB compiler:

```sh
GOOS=linux GOARCH=arm64 trb build --compile \
  --config tools/gate6d-benchmark/trbconfig.jsonc \
  --outfile /tmp/type-rb-native-gate6d-run/gate6d-benchmark
```

Prepare the target-neutral fixed-point B1 QBE through the documented recovery
path, copy it to `/tmp/type-rb-native-gate6d-run/b1.ssa`, then translate it in
the measurement image:

```sh
docker run --rm --platform linux/arm64 \
  -v /tmp/type-rb-native-gate6d-run:/run \
  type-rb-native-gate6d:measurement \
  /bin/sh -c '/usr/local/bin/qbe -t arm64 -o /run/b1.s /run/b1.ssa &&
    /usr/bin/cc /run/b1.s -Wl,--gc-sections,--strip-all -o /run/b1'
```

The shell above is recovery setup only. Its exact commands, input QBE hash,
revisions, and output seed hash must be recorded separately and are excluded
from the ordinary chain and every timed observation.

## Run

Use a clean primary repository worktree so its Git revision is visible inside
the container. Keep the measurement workspace on the container-local Linux
filesystem. A Docker Desktop bind mount materially distorts the compiler's
many small IL writes and is rejected as a performance environment; only the
seed, controller, and final reports use the `/run` bind mount.

```sh
docker run --rm --platform linux/arm64 --cap-add SYS_PTRACE \
  -v "$PWD:/repo:ro" \
  -v /tmp/type-rb-native-gate6d-run:/run \
  type-rb-native-gate6d:measurement \
  /run/gate6d-benchmark \
  /repo \
  /run/b1 \
  'SEED_PROVENANCE' \
  'ENVIRONMENT_PROVENANCE' \
  /run/gate6d-benchmark \
  /usr/local/bin/qbe \
  /usr/bin/cc \
  /tmp/type-rb-native-gate6d-workspace \
  7 \
  /run/raw.csv \
  /run/process-inventory.txt
```

`SYS_PTRACE` is used only for the post-measurement process inventory. The
elapsed-time and RSS commands do not run under `strace`. CSV iterations `-2`
and `-1` are warmups; medians use iterations `0` and later. RSS uses the same
two warmups and at most three recorded iterations to limit measurement cost.

The Linux link recipe already applies `--strip-all`, so raw compiler artifacts
are distribution-shaped. The harness nevertheless reapplies GNU `strip` to a
separate copy and requires exact stripped B2/B3/B4 identity. It rejects a
generated compiler above the registered 208,530-byte limit and records the
compiler plus QBE distribution components separately.
