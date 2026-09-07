# Recovery import follow-up

The first quick run at `1aaedb7562b3946291f35ce6dbf5d6df1a986184`
([34068649093](https://github.com/type-rb/type-rb-native/actions/runs/34068649093))
reported 95 root units with one failure: the recovery source's exact import
prefix had not been updated for the new logical-plan helpers. The ordinary
core and CLI path does not consume those recovery-only strings.

Both entry and checked-program recovery prefixes now include the exact new
imports. The quick canonical-source test reads and validates every module
through the real recovery source loader, rather than checking only the entry
prefix. Existing missing, modified and extra-import rejection tests remain.
All 95 local root units pass. This is deliberately a lightweight source-closure
test, not a current full recovery-enabled pass; that authority remains pending.

The independently triggered [CLI run 34068648944](https://github.com/type-rb/type-rb-native/actions/runs/34068648944)
at the same compiler source passes on Darwin arm64 and Linux arm64: published
seed/core/CLI fixed points, CLI/REPL/terminal behavior, scalar output, cache
invalidation and artifact packaging. It does not substitute for the full
Linux target, process or memory authorities.

The correction changes only recovery support and its test. The compiler/CLI
source digests and previously reported failed cost cohort remain unchanged.
