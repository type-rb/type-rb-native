# Native OIDC Bearer authentication

Compiled applications implement `Bearer.verify`, `Bearer.authenticate` and
`Bearer.principal` from the pinned `trb/web/auth/bearer` package. Public records,
validation order, error kinds and stable messages follow `TYPE_RB_REVISION`.
The retained reference REPL has no OIDC adapter; Native preserves its explicit
diagnostic before validation or network access. It does not invoke a Go process.

The TypeRB provider owns configuration, header/token parsing, typed JSON
compatibility, key selection, claims, cache transitions and Web context values.
Verified MIR selects narrow host adapters for synchronous HTTP retrieval, RS256
verification, URI/IP parsing, environment access and clock/integer conversion.
Authored paths or lookalike declarations cannot authorize those adapters.

## Authentication behavior

Authorization accepts exactly one Bearer header. Discovery precedes token
decoding when no explicit JWKS URI is configured. Tokens require RS256 and a key
identifier. Keys require RSA, at least 2048 modulus bits, and an odd exponent of
at least three encoded in no more than four bytes. Verification uses SHA-256 and
PKCS#1 v1.5 through OpenSSL EVP; it does not implement RSA in TypeRB.

Issuer, audience, expiration, optional not-before, subject and configured roles
are checked in reference order. Metadata/JWKS typed fields preserve the reference
JSON field matching and null behavior. Claims retain float64 number semantics
instead of passing through the public JSON codec's portable Integer conversion.

Discovery is cached by issuer and keys by JWKS URI for five minutes. An unknown
key identifier can force a refresh, throttled for thirty seconds; a failed
refresh retains prior usable keys and the throttle. The single managed mutator
and synchronous boundary make each cache transition indivisible.

Successful middleware attaches a typed principal to the context passed to the
next handler. It leaves the original context unchanged. All authentication
failures produce the reference JSON 401 response and `WWW-Authenticate: Bearer`.

## HTTP and trust boundary

Each retrieval has a five-second total deadline across redirects. Only HTTP and
HTTPS are accepted; the tenth redirect is rejected. Non-200 responses fail
without waiting for their body. Successful bodies are bounded to 1 MiB after
decompression. Only gzip is automatically decoded, including concatenated
members; other content encodings remain opaque as in the reference transport.

Proxy selection is TypeRB-owned and captured on first use: uppercase
`HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY` take precedence over lowercase forms.
Loopback bypass, host/domain/port/CIDR matching and the CGI HTTP proxy rejection
are distinct from libcurl's defaults. `ALL_PROXY` is outside the reference policy.
HTTPS proxies use CONNECT while preserving end-server certificate verification.

TLS uses one static OpenSSL build shared by libcurl, RSA and digest consumers.
The minimum TLS version is 1.2. Automatic OpenSSL configuration and provider/engine
loading are disabled; `OPENSSL_CONF` cannot change this profile.

On macOS, an unset or empty `SSL_CERT_FILE` and `SSL_CERT_DIR` selects OS platform
trust through Security.framework. A nonempty override selects disk roots. Linux
probes the Go reference's first readable bundle and certificate directories;
those variables override the respective lists. Directory entries are ordinary
PEM files, not OpenSSL hash links. No Mozilla bundle is silently added, and
OpenSSL's compiled default paths are not used. Comparisons record the Go
toolchain, generated module version and environment; the current baseline is
Go 1.27 with its default platform-override behavior.

The client profile currently uses HTTP/1 and the threaded DNS resolver. Optional
HTTP/2 and IDN libraries are not linked. This is not a general HTTP client or a
server TLS API. Complete transport edge compatibility, shared database TLS and
release qualification remain explicit work in the owning tasks.

## Dependencies and installation

| Consumer | Selected libraries |
| --- | --- |
| Core compiler and lockfile checksum | No OIDC/crypto libraries |
| Full CLI and retained REPL | Existing static libcrypto; no OIDC client |
| Compiled Bearer application | libcurl, libssl, libcrypto and zlib; existing Web transport dependencies also apply |
| Web response compression | Existing libdeflate, independently of OIDC gzip decoding |

[oidc-dependencies.json](../tools/oidc-dependencies.json) pins curl and zlib by
release archive SHA-256 and upstream revision. OpenSSL comes from the existing
[crypto pins](../tools/crypto-dependencies.json), with the same configuration and
accepted `libcrypto.a` used by all TLS/crypto consumers. zlib supplies bounded
streaming decoding; libdeflate remains the separate whole-response gzip encoder.

Contributor builds require a C toolchain, Perl, make and CMake:

```sh
python3 tools/build-crypto-dependencies.py --archives /path/to/shared-crypto-sources --output bin/crypto
python3 tools/build-oidc-dependencies.py --archives /path/to/shared-oidc-sources \
  --crypto-archives /path/to/shared-crypto-sources --crypto bin/crypto --output bin/oidc
python3 tools/oidc_artifact_smoke.py bin/oidc --crypto bin/crypto --receipt oidc-link.json
```

Build-time lookup uses `oidc/` beside QBE or `TRBN_OIDC_LIB_DIR`; crypto uses the
existing matching crypto directory. Neither location is required at application
runtime. Applications statically contain both `TRBN-OIDC-V1` and
`TRBN-CRYPTO-V1` inventories. The OIDC receipt records the exact crypto archive
and configuration against which libssl/libcurl were built. Inspect and package
them with `tools/oidc_artifacts.py` and `tools/crypto_artifacts.py`.

Each OIDC artifact retains curl, zlib and OpenSSL notices. The crypto bundle
also retains its OpenSSL notice. Darwin links Security, CoreFoundation and
SystemConfiguration frameworks. Linux links the platform thread/dynamic-loader support. The artifact
CI matrix covers Darwin/Linux arm64/amd64; it is separate from ordinary compiler
host support and does not fill the darwin-amd64 compiler gap. Immutable release
publication and advisory/update ownership remain in [#1257](https://github.com/type-rb/type-rb-native/issues/1257).

## Lifetime and validation

Foreign callbacks operate on native buffers without invoking managed code.
Handles, RSA objects, trust-store parsing objects and gzip state are released
before returning. Managed body/error/redirect values are copied only at owned
allocation boundaries. Upstream process-global caches retain their documented
lifetime; they are distinct from per-request resources.

`tools/native-oidc-test.py` runs the same synthetic issuer/key/token corpus against
the pinned reference and Native, with local HTTP/HTTPS fixtures. It covers
middleware context propagation, invalid credentials, discovery/JWKS errors,
refresh behavior, proxies, redirects, trust overrides and bounded decompression.
Its `--stress` mode instruments emitted code with forced GC and foreign allocation
failures, verifies exact resource release, and uses a blocking configuration FIFO
to test OpenSSL initialization isolation. These probes are test-only C ABI
instrumentation, not repository-owned C runtime implementation.

Declaration/MIR tests reject changed ownership, parameters, mutation, bodies,
results and effects, including after source erasure. Pinned-header ABI assertions
cover libcurl/OpenSSL/zlib constants, native structs and platform interfaces.
Artifact smoke tests verify relocation, embedded inventories, HTTPS and absence
of dynamic TLS dependencies. Local checks, hosted target validation and immutable
release qualification remain separate evidence.
