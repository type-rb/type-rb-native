# Retired experiment controllers

Completed source-era benchmark projects are removed from current checkout and CI.
Their original controllers remain in the immutable
[pre-retirement tools inventory](https://github.com/type-rb/type-rb-native/tree/d568d9e712452f66fc9c48d6025bf73b79659661/tools).
They covered scalar/aggregate/managed recovery, compiler reconstruction, file and
project entry, module loading, lookup, numeric collections and bootstrap closure.
Use the exact registered source revision when reproducing an experiment; its old
contract is not another authority over today's compiler.

The retained [historical portable-entry workflow](../.github/workflows/historical-portable-entry.yml)
checks out exact tooling revision `5cf61c740aa600c34ed94f1b130ea2ffefd9e783` before
invoking the original controller. Its old command and artifact names identify
that frozen reproduction. Source, oracle, seed and measurement identities remain
unchanged. Current recovery, conformance, target and memory checks stay required.
