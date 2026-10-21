<!-- Generated from tools/native-language-cases.json; do not edit by hand. -->

Each count describes registered probes, not language coverage percentages.

| Family | Phase | Probes with differences | Uncovered contracts | Reference syntax nodes |
| --- | --- | --- | --- | --- |
| Source text and lexical forms | basic | 0 / 64 | Invalid UTF-8 source and diagnostic positions; CRLF and source normalization; Remaining reserved contexts and malformed literal contracts | CommentStatement, BlankStatement, Identifier |
| Strings and UTF-8 | basic | 2 / 182 | Reference output-mode Unicode case differences (TypeRB #791); Embedded-expression boundaries beyond the reviewed interpolation probes | Literal, InterpolatedString |
| Immutable Bytes | basic | 0 / 22 | Bytes values across remaining nominal wrappers and imported declarations |  |
| Numeric and Boolean operations | basic | 1 / 86 | Remaining operators and assignment forms; mixed widening and portable failure boundaries; Lazy evaluation with remaining transfer, nullable invalidation and projection combinations | UnaryExpression, BinaryExpression |
| Bindings, constants and mutation | basic | 5 / 163 | Remaining collection-inference combinations; qualified namespace binding members (TypeRB #787) | VariableStatement, AssignmentStatement |
| Function declarations and calls | basic | 0 / 49 | none registered | MethodStatement, ReturnStatement, CallExpression, ExpressionStatement |
| Defaults and named arguments | basic | 0 / 63 | Imported method-default shadowing across execution modes (reference issue #1134) |  |
| Conditions and value-producing branches | basic | 0 / 16 | Nullable/union common result types and broader expression nesting boundaries | IfStatement |
| Loop control and transfers | basic | 0 / 10 | Additional nested transfer and diagnostic-origin differential probes | WhileStatement, BreakStatement, NextStatement |
| Case statements and expressions | basic | 0 / 16 | none registered | CaseStatement |
| Records and field bindings | basic | 0 / 41 | Nominal cycles and defaults involving remaining unsupported value types | RecordStatement, RecordFieldStatement |
| Member access and projections | basic | 1 / 8 | Safe member access, chained field narrowing and receiver replacement | MemberExpression |
| Nullable values and narrowing | basic | 12 / 100 | Class/callback and general pattern narrowing; remaining collection/union optional conversions; unguarded nullable indexing (issue #1120); Nullable standard-library methods beyond the currently implemented Native APIs |  |
| Enums and tagged values | basic | 4 / 170 | Method-specific type parameters, attribute output-mode effects and remaining pattern/control combinations; Reference REPL initializer replay (TypeRB #768) and shadowed standard error identity (#769); imported/nested REPL presentation parity | EnumStatement, EnumMemberStatement |
| Transparent aliases | basic | 3 / 110 | Authored alias spelling in diagnostics, nominal import display and nullable union alternative ordering (#455); Transparent alias compatibility at conditional branch joins (proposal #1128) | TypeAliasStatement |
| Nominal newtypes | basic | 1 / 84 | Class/interface representation dependencies; Method-specific generic parameters with the remaining callable/generic family | NewtypeStatement |
| Generic declarations and applications | basic | 2 / 162 | Remaining method-specific generic combinations and deferred generic class methods; Wider constraints and type applications; Generic output of concrete aggregate values; Nullable type-argument output differs from the reference Go representation (#691) | GenericExpression |
| Union values, literal types and discriminated unions | basic | 10 / 218 | Reference grouped annotation and nullable-alternative boundaries (TypeRB #764 and #765); composite type patterns remain staged in the reference |  |
| Function values and lexical capture | basic | 0 / 116 | Method references and remaining parameter-capability/narrowing combinations | LambdaExpression |
| Arrays and checked indexes | basic | 11 / 324 | Remaining receiver and inference combinations; unguarded nullable indexing (issue #1120); Wider invalid element/mutation combinations | ArrayLiteral, IndexExpression |
| Hash values and operations | basic | 12 / 69 | Wider key/value representations, dynamic Any operations, remaining inference combinations and managed lifetimes; nullable Hash reference Go lowering and unguarded indexing (issue #1120) | HashLiteral |
| Structured and value-producing iteration | basic | 0 / 176 | Remaining receiver APIs that shorten or reorder an Array during traversal | IterationExpression, BlockExpression |
| Range values and boundaries | basic | 0 / 19 | none registered | RangeExpression |
| Result and typed propagation | basic | 0 / 81 | General union errors and compiler-declared structured package boundaries | TryExpression, CatchExpression |
| Classes, fields and methods | basic | 0 / 85 | Initialized superclass storage and constructor chaining; inherited overrides (TypeRB #797) | ClassStatement, FieldStatement |
| Explicit interface conformance | basic | 0 / 21 | Variance and method-specific generic contracts with the reference object specification; Initialized-superclass and override dependencies | InterfaceStatement |
| Modules and constant lookup | basic | 1 / 40 | Remaining module method and qualified mutable namespace-member boundaries | ModuleStatement |
| Symbol values | basic | 1 / 36 | Remaining reference operator/control framing and multiline interpolation boundaries | SymbolLiteral |
| Project imports and declaration identity | basic | 0 / 49 | Bare/named aliases, graph conflicts, missing/unused imports and file/project/REPL identity | ImportStatement |
| Target source interop | toolchain | 0 / 0 | Go/Ruby/TypeScript source emission and platform interop | NativeStatement, NativeBlock, NativeExpression |
| Portable HTTP values | packages | 0 / 29 | Networking, streaming, transport adapters and Web semantic/type providers |  |
| JSX and web bindings | packages | 0 / 0 | Typed JSX and official web-package boundaries | JSXElement |
| Package capability activation | packages | 0 / 0 | Package-owned activation and resolution | ActivateStatement |
| Retired authored attempt syntax | retired | 0 / 0 | none registered | AttemptExpression |
| JSON values and comments | packages | 0 / 33 | Typed record codecs, wire attributes and date/time codecs; Deterministic precedence for multiple invalid object members requires the decision in #1138 |  |
