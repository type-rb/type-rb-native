<!-- Generated from tools/native-language-cases.json; do not edit by hand. -->

Each count describes registered probes, not language coverage percentages.

| Family | Phase | Probes with differences | Uncovered contracts | Reference syntax nodes |
| --- | --- | --- | --- | --- |
| Source text and lexical forms | basic | 2 / 64 | Invalid UTF-8 source and diagnostic positions; CRLF and source normalization; Remaining reserved contexts and malformed literal contracts | CommentStatement, BlankStatement, Identifier |
| Strings and UTF-8 | basic | 10 / 180 | Reference output-mode Unicode case differences (TypeRB #791); Embedded-expression boundaries beyond the reviewed interpolation probes | Literal, InterpolatedString |
| Numeric and Boolean operations | basic | 2 / 44 | All operators and assignment forms; mixed widening and every portable failure boundary; Short-circuit side effects and invalid RHS diagnostics across nested control | UnaryExpression, BinaryExpression |
| Bindings, constants and mutation | basic | 12 / 99 | Shadowing, duplicate declarations, unused/discard bindings and mutation through projections; Untyped empty collection inference; qualified namespace binding members (TypeRB #787) | VariableStatement, AssignmentStatement |
| Function declarations and calls | basic | 0 / 7 | Every all-path return, evaluation-order and mutable-argument boundary | MethodStatement, ReturnStatement, CallExpression, ExpressionStatement |
| Defaults and named arguments | basic | 0 / 13 | Method, function-value and payload-enum argument parity |  |
| Conditions and value-producing branches | basic | 0 / 16 | Nullable/union common result types and broader expression nesting boundaries | IfStatement |
| Loop control and transfers | basic | 1 / 10 | Additional nested transfer and diagnostic-origin differential probes | WhileStatement, BreakStatement, NextStatement |
| Case statements and expressions | basic | 0 / 5 | Exhaustiveness, repeated/unreachable branches and pattern-binding diagnostics | CaseStatement |
| Records and field bindings | basic | 1 / 36 | Nominal cycles and defaults involving remaining unsupported value types | RecordStatement, RecordFieldStatement |
| Member access and projections | basic | 0 / 4 | Safe member access, chained field narrowing and receiver replacement | MemberExpression |
| Nullable values and narrowing | basic | 4 / 44 | Class/callback and general pattern narrowing; collection/union optional conversions; Nullable standard-library methods beyond the currently implemented Native APIs |  |
| Enums and tagged values | basic | 5 / 110 | Method-specific type parameters, enum attributes and wider pattern forms; Reference REPL initializer replay (TypeRB #768) and shadowed standard error identity (#769); imported/nested REPL presentation parity | EnumStatement, EnumMemberStatement |
| Transparent aliases | basic | 6 / 33 | Literal/discriminated union alias targets; Authored alias spelling in REPL display and diagnostics | TypeAliasStatement |
| Nominal newtypes | basic | 4 / 83 | Class/interface representation dependencies; Method-specific generic parameters with the remaining callable/generic family | NewtypeStatement |
| Generic declarations and applications | basic | 4 / 80 | Remaining method-specific generic combinations and deferred generic class methods; Wider constraints and type applications | GenericExpression |
| Union values, literal types and discriminated unions | basic | 28 / 192 | Reference grouped annotation and nullable-alternative boundaries (TypeRB #764 and #765); composite type patterns remain staged in the reference; Reference union private-field visibility and common-field assignment defects (TypeRB #814 and #815) |  |
| Function values and lexical capture | basic | 0 / 56 | Callable equality, method references and remaining parameter-capability/narrowing combinations | LambdaExpression |
| Arrays and checked indexes | basic | 21 / 233 | Remaining receiver combinations and contextual/discarded empty collection inference; Wider invalid element/mutation combinations | ArrayLiteral, IndexExpression |
| Hash values and operations | basic | 13 / 30 | Wider key/value representations, empty inference and managed lifetime combinations | HashLiteral |
| Structured and value-producing iteration | basic | 2 / 176 | Remaining receiver APIs that shorten or reorder an Array during traversal | IterationExpression, BlockExpression |
| Range values and boundaries | basic | 0 / 19 | none registered | RangeExpression |
| Result and typed propagation | basic | 5 / 81 | General union errors and compiler-declared structured package boundaries | TryExpression, CatchExpression |
| Classes, fields and methods | basic | 4 / 75 | Initialized superclass storage and constructor chaining; inherited overrides (TypeRB #797); Static self.new; Reference constructor-path and receiver-default discrepancies (TypeRB #800 and #801) | ClassStatement, FieldStatement |
| Explicit interface conformance | basic | 0 / 21 | Variance and method-specific generic contracts with the reference object specification; Initialized-superclass and override dependencies | InterfaceStatement |
| Modules and constant lookup | basic | 1 / 38 | Forward initialization dependencies and cycles; remaining module method boundaries | ModuleStatement |
| Symbol values | basic | 2 / 35 | Single-quoted Symbol spellings; Remaining reference operator/control framing and multiline interpolation boundaries | SymbolLiteral |
| Project imports and declaration identity | basic | 1 / 23 | Bare/named aliases, graph conflicts, missing/unused imports and file/project/REPL identity | ImportStatement |
| Target source interop | toolchain | 0 / 0 | Go/Ruby/TypeScript source emission and platform interop | NativeStatement, NativeBlock, NativeExpression |
| JSX and web bindings | packages | 0 / 0 | Typed JSX and official web-package boundaries | JSXElement |
| Package capability activation | packages | 0 / 0 | Package-owned activation and resolution | ActivateStatement |
| Retired authored attempt syntax | retired | 0 / 0 | none registered | AttemptExpression |
