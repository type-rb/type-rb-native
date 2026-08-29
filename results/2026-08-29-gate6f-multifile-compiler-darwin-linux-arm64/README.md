# Gate 6F Multi-file Self-hosted Compiler Results

Gate 6F passes its registered source-closure, self-hosting, Darwin performance,
memory, size, application-identity, ownership, and pinned Linux arm64 criteria.
The canonical TypeRB-authored compiler is now a real three-module project, and
every ordinary replacement generation compiles that actual closure without Go.

The temporary flat source remains recovery- and comparison-only. It is derived
from the canonical modules, is not checked in, and is never substituted into
the ordinary B1-to-B4 chain.

## Revisions and evidence

- TypeRB Native implementation and benchmark harness:
  `7cb7e85c0b5bff14157dc1a686829c010d095b70`
- pinned TypeRB reference compiler:
  `fa9e0503cc681bcaa691f6f11d2f1e19ca8e6453` (`0.3.49-dev`)
- Darwin QBE 1.3 SHA-256:
  `03f50f24156449e0df41ef65444add1670d017be822edf4aa99bc8566952592b`
- TypeRB-authored benchmark executable SHA-256:
  `4004423755396b65468afa3781a3865870e527c8de737919cb54f6d0e882cecd`

The canonical compiler closure is:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| `compiler.trb` | 149,407 | `d6cbf5100e2d76f6d04ff48a597de11fea8abd952f9c8e212f1d6f71de30c9ce` |
| `storage.trb` | 2,588 | `d4c77fec9e5c5e8580cb0b5ee71fbd2c9c714555cbd4fd1457fcd44cc6db1f9d` |
| `path.trb` | 1,644 | `6347003851071b73cb8dbf38622fcc7cf3be6abf81ea253b9aad081fb057510a` |

The independently re-derived temporary flat source is 153,301 bytes with
SHA-256
`df46782b9ef321eb302ec1886f7ea5733b197638ed9565cf3e5e65449cecbe23`.

The committed [`raw.csv`](raw.csv) has 57 data rows and no nonzero status. The
437-line [`process-inventory.txt`](process-inventory.txt) has six nonzero
statuses, all required negative probes proving that B1, B2, B3, B4, the flat
compiler, and the application contain no Go build metadata.

```text
eba4dcfe1f6764c1d64e1783d9bc47ae9a7c2b26634d2597e67cf695fe75e080  raw.csv
ef371da1df0685d78c5d5a942c19f3eaf798bd88fbd3656800967d660c89ef14  process-inventory.txt
66f3c497b26c82a0b9106a1154260fb862bfe3638af4b2ac42b86c2506865db1  seed-provenance.txt
df6559a079b318b726c0d811227292bbf09ec3fbdfbb4cd6ab2f1fbe6e17cc5c  linux-correctness.txt
1070c9d8ad606eff0342384589aea9f0b5100d2315660ac4e4821400d1bcfbbb  linux-run.sh
ab6c8be1b6ea8eec78c3041e90c4375e5e3d5d002901100983ac2cffaab0bb21  linux-run.log
76364a4cb7354bad12c70347a7905fdcfd7b6dd9916d9a7569985dcbeec86bb5  linux-process.trace
```

The exact B0/B1 commands, real-closure snapshot, deterministic flat-source
derivation, phase output, and hashes are retained in
[`seed-provenance.txt`](seed-provenance.txt). The fixed Linux image, complete
commands, ELF identities, and application run are retained in
[`linux-correctness.txt`](linux-correctness.txt),
[`linux-run.sh`](linux-run.sh), [`linux-run.log`](linux-run.log), and
[`linux-process.trace`](linux-process.trace).

## Correctness and ownership boundary

PR #56 established the canonical split and passed the complete configured
corpus. PR #57 added the fixed benchmark controller and passed 76 general
tests, two benchmark derivation tests, and 13 self-hosted compiler tests. The
permanent coverage proves that:

- the pinned reference snapshot, B0, and ordinary Native compiler load the
  real entry, storage, and path closure;
- imported records and helpers resolve through explicit imports without
  transitive re-export assumptions;
- independent storage and path mutations change emitted compiler QBE;
- missing or malformed compiler modules fail before QBE or CC, while an
  unrelated invalid sibling remains outside the closure;
- the hidden source-content adapter remains single-source; and
- the complete earlier valid, mutation, invalid, build-failure, Darwin, Linux,
  file-root, atomic-publication, and cleanup corpus remains green.

The formal ordinary Darwin chain is:

```text
B1 build compiler.trb closure -> B2/compiler
B2 build compiler.trb closure -> B3/compiler
B3 build compiler.trb closure -> B4/compiler
```

B2, B3, and B4 are byte-identical at 244,696 bytes with SHA-256:

```text
2b63bd297e2e049f51c54b59299385aabf05d93ff218c701a5c6a54307358e12
```

Their fixed-point QBE SHA-256 is
`626bcdfb28c6517c50b86851edf76f4ab5b0d8ada7d28e73209ff10e193bae67`.
The comparison-only flat compiler has SHA-256
`c95cd3438c2265348104ae1fada6e80be515b941e0508ed3c856a414da9fb314`
and flat QBE SHA-256
`75869d86aff5964e908bad6fd6808d454b3c0aca6b55e9c261cd0783242c39fe`.

The B4 compiler built the Gate 6E five-module application twice. Both 53,288
byte executables are identical, print `file-root-ok`, and retain the registered
Darwin SHA-256:

```text
413d97fd8a3f26e1086795b1fd5306ad5817613e7080ddba410eb8264c0a67b9
```

The benchmark accepts one prepared B1. Recovery is not a child, argument, or
timed phase in the ordinary chain. Native compiler artifacts link only to
`libSystem` on Darwin, contain no Go metadata, and directly retain the
`fork`/`execv`/`waitpid` boundary to explicit QBE and CC paths. No Native
intermediate remains.

## Measurement method

The TypeRB-authored controller first verifies the canonical multi-file chain,
the independently derived flat compiler, and the Gate 6E application. It then
records two indexed warmups and seven alternating B1-to-B2 builds for each
source organization, followed by a separate identically ordered two-warmup,
seven-observation peak-RSS series. Both candidates use the same B1, QBE, CC,
and `compiler` output basename. Correctness checks, hashing, stripping, and
inventory occur outside timed intervals. Medians below exclude iterations
`-2` and `-1`.

The exact formal command was:

```text
/tmp/type-rb-native-gate6f-final.mWHyQH/tools/benchmark-7cb7e85 \
  /Users/fujita-h/trb/worktrees/type-rb-native-gate6f-results \
  /tmp/type-rb-native-gate6f-final.mWHyQH/recovery/b1 \
  reference-fa9e050-real-closure-b0-temporary-flat-b1 \
  /tmp/type-rb-native-gate6f-final.mWHyQH/tools/benchmark-7cb7e85 \
  /tmp/qbe-1.3/qbe \
  /usr/bin/cc \
  /opt/homebrew/bin/go \
  /tmp/type-rb-native-gate6f-final.mWHyQH/darwin/workspace \
  /tmp/type-rb-native-gate6f-final.mWHyQH/darwin/raw.csv \
  /tmp/type-rb-native-gate6f-final.mWHyQH/darwin/process-inventory.txt
```

The Darwin host was an Apple M2 Pro with 32 GiB RAM, macOS 26.6.2 (25G83),
Go 1.27.0, and Apple clang 21.0.0.

## Compiler build results

Elapsed values are seconds; RSS values are bytes. Each row summarizes seven
recorded observations after warmup.

| Source organization | Median time | Minimum | Maximum | Versus flat median |
| --- | ---: | ---: | ---: | ---: |
| canonical multi-file | 0.712012 | 0.708830 | 0.727004 | -0.37% |
| temporary flat | 0.714688 | 0.708936 | 0.743917 | baseline |

| Source organization | Median RSS | Minimum | Maximum | Versus flat median |
| --- | ---: | ---: | ---: | ---: |
| canonical multi-file | 36,716,544 | 36,585,472 | 37,208,064 | -0.09% |
| temporary flat | 36,749,312 | 36,519,936 | 36,831,232 | baseline |

The multi-file median is faster than the flat median and uses slightly less
RSS, so both registered 10% source-organization bounds pass.

Against the Gate 6C absolute baselines, multi-file time is 21.56% higher than
0.585709 seconds and RSS is 0.13% higher than 36,667,392 bytes. Both pass the
registered 25% ceilings of 0.732136 seconds and 45,834,240 bytes. The largest
recorded multi-file time, 0.727004 seconds, is also below the time ceiling,
although the criterion applies to the median.

## Compiler and application sizes

| Artifact | Raw bytes | Stripped bytes |
| --- | ---: | ---: |
| canonical multi-file B4 | 244,696 | 199,992 |
| temporary-flat compiler | 244,728 | 199,992 |

The multi-file fixed point is 4.09% below the 208,530-byte absolute cap and has
zero stripped-size overhead relative to the flat equivalent, passing the 5%
relative cap. The Gate 6E application remains exactly 53,288 bytes with the
same behavior and SHA-256; this source-organization slice changed no frontend,
emitter, runtime, or optimization policy.

## Pinned Linux arm64 result

The unchanged Gate 6D image rebuilt the actual three-module compiler closure
under `linux-arm64-v0`. Linux B1, B2, B3, and B4 are byte-identical at 182,384
bytes with SHA-256:

```text
f8b7826f54d527acead4a6ab6849dbac3c6f5955df5c199e09adfd61ec454d78
```

B4 emits the exact Darwin seed QBE, and it builds the five-module application
twice to identical 68,568-byte ELF executables. The application prints
`file-root-ok` and retains the prior Linux application SHA-256
`6f27705eca2c8666951503b082dc1d05600808d81ecab66b2ac4419ac3ea7073`.
The repository mount was read-only, the process trace exposes QBE, CC,
assembler, collect2, and linker execution, and no intermediate remained.
Linux timing was not added to the Darwin-only registered performance claim.

## Conclusion and deferred scope

Gate 6F establishes that the self-hosted compiler itself can use the same
explicit file-root module closure as ordinary programs without measurable
source-organization or size regression. The real multi-file path is slightly
faster and smaller than its mechanically flat comparator in this result, while
remaining exact across Darwin and Linux replacement generations.

Further compiler decomposition, configured projects, package imports, public
module identity, incremental compilation, automatic tool discovery, release
seed policy, and production runtime integration remain separate bounded work.
