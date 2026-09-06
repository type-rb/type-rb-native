# MIR Array-loop bounds diagnostic — Darwin arm64

Status: **not accepted**. The two local runtime cohorts pass, but the current
compiler build wall-time ratio is `1.0505660577`, exceeding the unchanged
`1.05` limit. Do not round that observation into a pass, use hosted acceptance
to rescue it, or update the accepted Pages snapshot.

[Issue #303](https://github.com/type-rb/type-rb-native/issues/303) and its
[pre-timing quantitative registration](https://github.com/type-rb/type-rb-native/issues/303#issuecomment-5559049058)
define the comparison. The measured baseline is
`1afd60c2c7257ed34fd2a2aa70cb8b9164433009`. Candidate patches apply to the
isolated proof checkpoint `98eb48e0261853aec4b03c541eb6617f8995a93e`, whose
ancestry also includes the independently accepted scalar-output change in
PR #300. The comparison baseline has not been moved to absorb that cost.

## Runtime observations

Same TypeRB sources, separately compiled by the baseline and initial connected
Native compilers. Compilation is excluded. Each cohort has two warmups and
seven retained processes per role, with alternating retained order. All 108
processes across six comparisons produce exact expected stdout, empty stderr
and status zero. All memory, control and catastrophic requirements pass.

| Spectral-norm cohort | Baseline wall (s) | Candidate wall (s) | Wall ratio | CPU ratio |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2.217853125 | 2.166737959 | 0.9769528625 | 0.9779874843 |
| 2 | 2.217186542 | 2.170778792 | 0.9790690819 | 0.9770994101 |

This is about 2.1–2.3% less wall time than the previous Native executable,
**not a Pure Go comparison**. Inputs are spectral-norm 5500, fannkuch-redux 10
and n-body 1000000. The latter two are local non-regression controls, not their
larger cross-language publication inputs. Their executable bytes are unchanged.

Spectral QBE decreases from 51699 to 51561 bytes by removing two redundant
inner-loop access checks. Its 50992-byte executable does not grow. Checked
Integer arithmetic remains, including induction increments. A different or
shorter output Array does not inherit the input Array's proof.

The subsequent compiler-only refinements reproduce the measured application
QBE byte-for-byte. This establishes code-generation identity, not a new runtime
cohort or an accepted platform result.

## Compiler-cost observations

Every row below is a distinct source candidate, not an unchanged retry. Each
comparison retains two warmups and seven interleaved observations per role.
Every produced compiler matches its same-basename input seed byte-for-byte.
All RSS and retained-observation catastrophic checks pass. All five candidates
remain rejected under the complete cost contract.

| Candidate | Build wall ratio | Build CPU ratio | RSS ratio | Result |
| --- | ---: | ---: | ---: | --- |
| Initial connection | 1.0596764519 | 1.0625217605 | 0.9987859166 | Wall/CPU fail |
| Opaque shortcut | 1.0588673547 | 1.0707447727 | 1.0000000000 | Wall/CPU fail |
| Direct row ownership | 1.0573644454 | 1.0525063040 | 0.9967598218 | Wall/CPU fail |
| Selected-read-only lookup | 1.0516833588 | 1.0543707721 | 1.0004056795 | Wall/CPU fail |
| Shared failure construction | 1.0505660577 | 1.0492299872 | 1.0048959608 | Wall fails |

The opaque shortcut is not retained. The current source removes the obsolete
header wrapper, passes the checked six-cell rows directly to their existing MIR
owner instead of flattening and reconstructing them, delays function lookup
until a selected read needs it, and shares 39 identical cold error-result
constructions. These are implementation refinements, not broader proof rules.

The current compiler is 349256 bytes with 247772 bytes of Mach-O text and
1110340 bytes of compiler QBE, inside the existing absolute ceilings. B2/B3/B4
SHA256 is `88a56205b62bb9510ad9cab0a360677bd9bd00fb2ee0ba489a407f3d19103713`.
Passing these size limits does not compensate for the build-time miss.

## Correctness and scope

- The initial connection passed recovery-enabled root 95/compiler 127 suites
  and the complete 70-case corpus at B2/B3/B4. An earlier root failure was a
  missing new module in the mutation fixture; that consumer now tests changes,
  missing files and malformed bodies for the thirteenth module too.
- The current source passes compiler 128 tests, including 39 MIR-focused tests,
  and all 70 corpus cases at B2/B3/B4 (210 rows). Repeated and adjacent QBE agree.
- Controls include empty/singleton and nested loops, reused local slots,
  shorter outputs, checked overflow, changed indices, aliases, opaque effects
  and malformed or forged plans. Five focused executions also match the pinned
  reference's output or failure class. Native and reference wrapper exit codes
  need not be numerically identical for a language panic.
- Current-source full recovery, current CLI integration, Linux targets,
  process graphs, memory authorities and hosted runtime acceptance remain
  pending. Earlier full recovery must not be relabeled as a current-head pass.
- A proposed immutable-to-mutable checked-value alias was rejected by the
  reference before timing and was removed. The underlying pre-existing Native
  mismatch is tracked separately in [issue #305](https://github.com/type-rb/type-rb-native/issues/305).

The scope remains an experimental structured Array-region proof, not complete
block/value MIR for arbitrary functions or completion of emitter ownership
recovery. No language rule, budget or acceptance condition has been relaxed.

## Reproduction

Host: Apple M2 Pro, 10 logical CPUs, 32 GiB RAM, macOS 26.6.2, Darwin arm64.
Toolchain: pinned reference `5dc09070cf7f88a569279f5e63982a6de59d692c`, QBE 1.3,
Apple clang 21.0.0 (`clang-2100.1.1.101`), profile `darwin-arm64-v0`.
Ordinary warm-cache local execution; no CPU pinning, controlled frequency or
host-wide isolation claim. Owned heavy correctness/build batches did not
overlap the runtime cohorts; build-cost cohorts were separate from them.
Unrelated host activity was not excluded. Small differences near a threshold
are not evidence of isolated instruction latency.

Runtime uses the unchanged `tools/native-mir-guarded-multiply/measure.py`:

```sh
python3 tools/native-mir-guarded-multiply/measure.py \
  BASELINE_EXECUTABLE CANDIDATE_EXECUTABLE \
  benchmarks/benchmarksgame/spectral-norm/expected/5500.txt \
  UNIQUE_EVIDENCE_DIRECTORY 5500 0.98
```

Repeat independently; use limits 1.02 for the two control inputs above. The
controller records monotonic wall time and wait4 CPU/RSS. Raw CSVs, summaries
and every runtime stdout/stderr are retained here.

`build-cost-observer.py` exposes the local build observer's path constants as
arguments, retaining its timing, wait4 accounting, schedule and evaluation:

```sh
python3 build-cost-observer.py \
  CANDIDATE_CHECKOUT UNIQUE_EVIDENCE_PARENT \
  BASELINE_COMPILER CANDIDATE_COMPILER QBE
```

Use absolute, same-basename `compiler` seeds and a checkout containing the
registered baseline commit. It builds each compiler from its own exact source
closure using `build ENTRY --output compiler --qbe QBE --cc /usr/bin/cc
--target darwin-arm64-v0`. Build CPU includes waited tool descendants; RSS is
the wait4 orchestration-root observation, not summed process-tree memory.
Raw build rows and summaries retain every warmup, retained result and failure.

`*.patch.json` preserves exact unified diffs relative to the stated source
checkpoint. Decode and apply only in a separate diagnostic checkout.
`identities.json` records candidate hashes and the current canonical source
digests. No compiler binaries are committed.
