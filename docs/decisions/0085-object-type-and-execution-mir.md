# Object types and execution through MIR

Status: implementation in progress within the basic-language milestone.

Classes and interfaces retain nominal identities separate from records. Authored
object declarations preserve their source owner, type parameters, fields,
initializers and method kinds. Concrete instances own resolved type arguments,
parent and interface edges, and field types. Recursive field expansion publishes
a nominal shell before following storage edges; inheritance cycles are rejected
independently. Transparent aliases and imported names select the same declaration,
while generic applications with different arguments keep distinct identities.
Template checking copies the concrete instance catalog and lookup index.

MIR composite kinds 13 and 14 identify classes and interfaces. The MIR object
catalog owns declaration origins, parent and interface type IDs, and field types,
origins and readonly flags. Fields remain attached to their declaring type;
inheritance does not flatten away the owner needed for privacy and initialization.
All nominal shells precede container and field resolution, permitting recursive
storage through records, classes, Arrays, Hashes and nullable values.

The independent verifier rejects missing or mismatched nominal IDs, wrong object
kinds, invalid origins, malformed fields, non-class parents, non-interface
contracts and cyclic inheritance. Source-level repeated `implements` declarations
are accepted and normalized to unique resolved edges. An interface carries no
class fields or inheritance. Neither structural resemblance nor a matching display
name creates nominal conformance. The pinned reference rejects assigning a child
class value to a parent-class binding; the inheritance graph does not authorize
that conversion. An inherited explicit interface edge remains available.

Object methods, including nongeneric methods, retain immutable templates.
Interface templates describe contracts and cannot instantiate executable functions.
Concrete class methods specialize the class arguments followed by method arguments;
ordinary function signatures and calls own argument binding, defaults, results and
receiver identity. Discovery finishes before MIR signatures and layouts are frozen.

MIR instruction 63 allocates a field-free concrete class. Its independent verifier
checks nominal identity, operand shape and the absence of inherited or local
storage; its allocation effect participates in normal managed-root planning.
Instance and class calls, private internal calls, explicit method type arguments,
class factories, named/default parameters and stored/captured receivers use this path.
QBE emits object descriptors and allocation from the verified object catalog and
never reinterprets authored object declarations. Source-erased emission, forced
collection and corrupt allocation instructions exercise this boundary.

The retained REPL consumes the checked callee identity, preserves nominal values
with their original type catalog, and remaps concrete generic identities when a
later declaration changes catalog order. Typed, never-executed projections carry
stored values into the next check without calling their constructors again.
Class/interface input framing, project imports and explicit replay use the same
ordinary declaration and checking contracts.

Storage-bearing classes, inheritance and interface implementation remain explicitly
guarded at the ordinary execution boundary. The type graph and field-free path do
not establish method-signature conformance, definite field initialization, legal
field mutation or interface dispatch safety. Those facts need checked operations
and independent verification before their guards can be removed. Draft fixtures
remain outside the passing Capabilities registry until the coherent family is
accepted through the CLI and retained REPL as well as the core compiler.

Construction through a class alias remains guarded because the pinned reference
rejects that receiver; aliases remain valid type annotations. Accepted namespaced
class programs also expose target code-generation failures documented in
[TypeRB #798](https://github.com/type-rb/type-rb/issues/798). Keep those reproductions
separate from the shared passing execution cases until the reference fixes land.

A separate reference discrepancy remains in inherited self-method dispatch:
Go, Ruby and TypeScript do not agree when an inherited method calls an overridden
method. [TypeRB #797](https://github.com/type-rb/type-rb/issues/797) records a
field-free reproduction. Preserve that evidence while completing executable
method contracts; a passing nominal graph must not hide the discrepancy.

The implementation follows the reference class contract without resolving its
explicitly deferred questions: superclass constructor chaining, initialization
order across initialized superclasses, mutating-method receiver requirements,
variance, generic class methods and same-named fields/methods. Follow-on execution
work includes definite initialization, field reads/writes, inherited/interface
dispatch, complete method contracts and retained REPL behavior. Existing call,
GC-root and source-erased controls must extend to those operations.

Acceptance for the complete family requires paired positive and negative cases,
ordinary check/build/run/REPL behavior, independent MIR corruption and lifetime
controls, compiler self-use where applicable, ordinary fixed points and required
hosted integration authorities. Capabilities and the shared registry advance only
with those executable contracts. Intermediate type-graph checks are not a claim
that the object family or basic-language milestone is complete.
