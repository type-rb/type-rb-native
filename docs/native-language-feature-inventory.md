<!-- Generated from tools/native-language-cases.json; do not edit by hand. -->

Each count describes registered probes, not language coverage percentages.

| Family | Phase | Probes with differences | Uncovered contracts | Reference syntax nodes |
| --- | --- | --- | --- | --- |
| Source text and lexical forms | basic | 1 / 2 | Invalid UTF-8 source and diagnostic positions; CRLF and source normalization; Identifier categories, reserved words and malformed literals | CommentStatement, BlankStatement, Identifier |
| Strings and UTF-8 | basic | 4 / 13 | Unicode escapes and remaining String receiver APIs; Embedded-expression boundaries beyond the reviewed interpolation probes | Literal, InterpolatedString |
| Numeric and Boolean operations | basic | 1 / 6 | All operators and assignment forms; mixed widening and every portable failure boundary; Short-circuit side effects and invalid RHS diagnostics across nested control | UnaryExpression, BinaryExpression |
| Bindings, constants and mutation | basic | 3 / 5 | Shadowing, duplicate declarations, unused/discard bindings and mutation through projections | VariableStatement, AssignmentStatement |
| Function declarations and calls | basic | 0 / 3 | Every all-path return, evaluation-order and mutable-argument boundary | MethodStatement, ReturnStatement, CallExpression, ExpressionStatement |
| Defaults and named arguments | basic | 0 / 13 | Method, function-value and payload-enum argument parity |  |
| Conditions and value-producing branches | basic | 0 / 16 | Nullable/union common result types and broader expression nesting boundaries | IfStatement |
| Loop control and transfers | basic | 1 / 10 | Additional nested transfer and diagnostic-origin differential probes | WhileStatement, BreakStatement, NextStatement |
| Case statements and expressions | basic | 1 / 5 | Exhaustiveness, repeated/unreachable branches and pattern-binding diagnostics | CaseStatement |
| Records and field bindings | basic | 3 / 30 | Nominal cycles and defaults involving remaining unsupported value types | RecordStatement, RecordFieldStatement |
| Member access and projections | basic | 1 / 4 | Safe member access, chained field narrowing and receiver replacement | MemberExpression |
| Nullable values and narrowing | basic | 4 / 21 | Class/callback and general pattern narrowing; collection/union optional conversions; Nullable standard-library methods beyond the currently implemented Native APIs |  |
| Enums and tagged values | basic | 4 / 19 | Raw values and conversion failures, enum methods and attributes; Nested module declarations and wider pattern forms | EnumStatement, EnumMemberStatement |
| Transparent aliases | basic | 13 / 30 | Literal/union, callable and class/interface alias targets; nested module declarations; Authored alias spelling in REPL display and diagnostics | TypeAliasStatement |
| Nominal newtypes | basic | 1 / 1 | Closed/private constructors, methods, immutable representation and boundary diagnostics | NewtypeStatement |
| Generic declarations and applications | basic | 11 / 67 | Generic methods, classes and interfaces; Wider constraints and type applications | GenericExpression |
| Literal types and discriminated unions | basic | 1 / 1 | Shared discriminants, branch narrowing and invalid mutation/common-type boundaries |  |
| Function values and lexical capture | basic | 9 / 15 | Retained REPL code and environments across submissions; nominal remapping, collection and replay; Named declarations as values, callable equality, nullable signatures and remaining parameter-capability boundaries | LambdaExpression |
| Arrays and checked indexes | basic | 1 / 8 | Removal during assignments/iteration and retained managed receivers; Remaining Array receiver APIs and invalid element/mutation combinations | ArrayLiteral, IndexExpression |
| Hash values and operations | basic | 0 / 5 | All key/value representations, empty inference, managed lifetimes and missing-key failures | HashLiteral |
| Structured and value-producing iteration | basic | 2 / 4 | Map/filter/reduce/chains, nested transfers, receiver replacement and live growth | IterationExpression, BlockExpression |
| Range values and boundaries | basic | 2 / 5 | Endpoint effects, empty/reversed ranges and next at both portable limits | RangeExpression |
| Result and typed propagation | basic | 1 / 28 | General union errors and compiler-declared structured package boundaries | TryExpression, CatchExpression |
| Classes, fields and methods | basic | 1 / 1 | Initialization, inheritance, dispatch, privacy and readonly fields | ClassStatement, FieldStatement |
| Explicit interface conformance | basic | 1 / 1 | Generic conformance, variance, inherited contracts and rejection controls | InterfaceStatement |
| Modules and constant lookup | basic | 1 / 1 | Cross-module constants, member visibility and runtime initialization order | ModuleStatement |
| Symbol values | basic | 1 / 1 | Symbol typing, equality and public receiver operations | SymbolLiteral |
| Project imports and declaration identity | basic | 3 / 10 | Bare/named aliases, graph conflicts, missing/unused imports and file/project/REPL identity | ImportStatement |
| Target source interop | toolchain | 0 / 0 | Go/Ruby/TypeScript source emission and platform interop | NativeStatement, NativeBlock, NativeExpression |
| JSX and web bindings | packages | 0 / 0 | Typed JSX and official web-package boundaries | JSXElement |
| Package capability activation | packages | 0 / 0 | Package-owned activation and resolution | ActivateStatement |
| Retired authored attempt syntax | retired | 0 / 0 | none registered | AttemptExpression |
