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

This type graph is preparation for object execution. It does not establish
method-signature conformance, definite field initialization, legal field mutation,
constructor effects or dispatch safety. Those facts and the corresponding typed
operations must be checked and independently verified before QBE adaptation.
Abstract interface signatures must never become executable empty functions.
Object declarations still fail the ordinary execution boundary until those parts
are implemented; draft fixtures are not registered as passing capabilities.

A separate reference discrepancy remains in inherited self-method dispatch:
Go, Ruby and TypeScript do not agree when an inherited method calls an overridden
method. [TypeRB #797](https://github.com/type-rb/type-rb/issues/797) records a
field-free reproduction. Preserve that evidence while completing executable
method contracts; a passing nominal graph must not hide the discrepancy.

The implementation follows the reference class contract without resolving its
explicitly deferred questions: superclass constructor chaining, initialization
order across initialized superclasses, mutating-method receiver requirements,
variance, generic class methods and same-named fields/methods. Follow-on execution
work includes checked allocation and initialization, field reads/writes, instance
and class method selection, inherited/interface dispatch, concrete generic method
instances, GC roots, retained REPL behavior and source-erased emission.

Acceptance for the complete family requires paired positive and negative cases,
ordinary check/build/run/REPL behavior, independent MIR corruption and lifetime
controls, compiler self-use where applicable, ordinary fixed points and required
hosted integration authorities. Capabilities and the shared registry advance only
with those executable contracts. Intermediate type-graph checks are not a claim
that the object family or basic-language milestone is complete.
