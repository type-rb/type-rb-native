# Native HTTP transport

The Native Web project provider connects the pinned `Web.serve(ServerConfig)`
API to libuv for TCP and event delivery, and llhttp for HTTP/1.1 framing. Routing,
request/response values, typed input, middleware and recovery remain TypeRB
implementations. The public package source remains pinned to `TYPE_RB_REVISION`.

Compile a file-route project that calls `Web.serve()` or passes a
`Web::ServerConfig`. The server supports IPv4, IPv6 and host-name binding. REPL
evaluation reports the reference's explicit unavailable-runtime diagnostic;
it does not start a listener. See [Native CLI](native-cli.md) for building the
compiler and applications.

## Dependency build

`tools/network-dependencies.json` pins the source archives by version and SHA-256:
libuv 1.53.0 and llhttp 9.4.3. Both use the MIT license. The generated llhttp release
archive contains C sources, so Node.js is not a build or runtime requirement.
The repository's runtime implementation is TypeRB; a C compiler builds only the
external libraries and a compile-only ABI assertion probe.

```sh
python3 tools/build-network-dependencies.py \
  --archives /path/to/shared/source-archives \
  --output /path/to/network-libraries
TRBN_NETWORK_LIB_DIR=/path/to/network-libraries ./application
```

The build requires Python, CMake and a platform C toolchain. Temporary source and
object trees are removed on success and failure. The output includes the two
libraries, their license files and a build receipt with source pins, compiler,
platform and binary hashes. Reuse the archives and installed libraries across
applications; do not copy build trees or a new cache into every application.
A 128 MiB budget is sufficient for this dependency installation and its archives.

| Component | Role | Application dependency |
| --- | --- | --- |
| Platform C runtime / system library | Allocation, process and dynamic loading primitives | Existing dependency; macOS `libSystem`, Linux libc and platform link dependencies |
| libuv 1.53.0 | TCP sockets, address resolution, event delivery and signal/timer handles | New dynamically loaded library when the server starts |
| llhttp 9.4.3 | HTTP request framing and validation | New dynamically loaded library when the server starts |
| QBE and platform compiler/linker | Build the Native executable | Build tools; not invoked by a running server |
| Python and CMake | Build and qualify the two external libraries | Dependency build tools only |

The dependency receipt records the actual linked system libraries on each target,
including platform-specific transitive dependencies. Keep that receipt and both
license files with the distribution. A pin update requires rebuilding the ABI
probe and rerunning the socket and lifetime tests on every qualified target.

The current loader requires the explicit directory, resolves the complete private
ABI before starting, and checks the libuv version. llhttp has no runtime version
query: use the pinned builder and its receipt, not an arbitrary system llhttp
library. Distribution must ship the qualified libraries and notices alongside
applications that need the server. Applications that do not load the network
provider do not acquire a runtime libuv/llhttp requirement. TLS, HTTPS clients and
database libraries are separate adoption decisions.

## Ownership and execution

The source loader assigns the internal Web server and network declarations their
identities. An authored path, alias, function name or matching declaration cannot
grant foreign-call privileges. Full signatures are checked again by MIR; network
calls conservatively retain allocation, failure, I/O and mutation effects.
The application-specific server/router is a project provider. The exact owned
`Web` to server-provider edge binds the application's routes and is excluded from
ordinary package-dependency traversal; authored package cycles remain errors.

One thread runs the libuv loop and TypeRB handlers. Foreign callbacks only parse
or copy into explicitly owned raw buffers; they cannot invoke managed handlers or
allocate GC-managed values. A complete request pauses reading on its connection.
The TypeRB loop copies immutable request bytes into managed objects, dispatches
with the existing recovery boundaries, and copies the response out before an
asynchronous write. No managed address remains in libuv or llhttp after returning
to TypeRB. Write and close callbacks release raw buffers after their last use.

Each connection has an opaque checked identity. The transport bounds the read
chunk, pipelined remainder, header storage and number of accepted connections.
`body_limit_bytes` bounds each decoded body, including chunked input. A partial
request does not prevent another connection from receiving a complete request.
Only one managed handler executes at a time; this is not a general task scheduler
or a claim of concurrent TypeRB handler execution.

SIGINT and SIGTERM stop accepting connections, close idle connections, and allow
pending responses to drain until `shutdown_timeout_milliseconds`. Close callbacks
run before the loop is released. Signals and deadlines are serviced by the event
loop: interrupting an indefinitely running synchronous TypeRB handler requires
execution cancellation and is not established by transport shutdown tests.

## HTTP behavior

HTTP/1.0 and HTTP/1.1 requests share the existing Web route and middleware
dispatcher. The transport handles fragmented headers and bodies, chunked input,
binary bodies, keep-alive, pipelining and `Expect: 100-continue`. Request method
tokens retain the public `HttpMethod` semantics rather than llhttp's narrower
method enumeration. Host and transfer-framing headers do not become application
headers; trailers are not promoted into them.

llhttp's strict framing is retained. In particular, a request containing both
`Content-Length` and `Transfer-Encoding` receives 400; Go's `net/http` instead
discards Content-Length. These low-level parser differences are explicit in the
shared acceptance test. They are not evidence of byte-for-byte equivalence to
every `net/http` behavior. Protocol upgrades, streaming and HTTP/2 need separate
transport contracts.

## Validation and remaining work

`tools/native-web-network-test.py` retains real socket tests for fragmented and chunked input,
keep-alive/pipelining, body limits, malformed/conflicting framing, binary bodies,
routing and middleware, handler failure, disconnects, bind failure, concurrent
partial requests, signals and restart. Force GC at managed allocation boundaries
while requests remain alive, and verify raw/managed cleanup independently.
The CLI CI matrix exercises Darwin arm64 and Linux arm64; the Linux amd64 target
lane exercises its built core compiler. Cross-target ABI, compiler recovery,
ordinary fixed points and hosted integration remain required. Process supervision,
streaming, generic scheduling, TLS and
performance qualification have separate acceptance; do not infer them from this
transport.
