<!-- Generated from tools/native-language-cases.json; do not edit by hand. -->

| Case | Check | Build | Execute | REPL |
| --- | --- | --- | --- | --- |
| Integer arithmetic | accepts | accepts | matches reference | matches reference |
| if / else | accepts | accepts | matches reference | matches reference |
| while | accepts | accepts | matches reference | output differs |
| Short-circuit OR / AND | accepts | accepts | matches reference | matches reference |
| Record construction and field read | accepts | accepts | matches reference | matches reference |
| Array&lt;Integer&gt; | accepts | accepts | matches reference | matches reference |
| elsif | accepts | accepts | matches reference | matches reference |
| break | accepts | accepts | matches reference | matches reference |
| next | accepts | accepts | matches reference | matches reference |
| Default argument | accepts | accepts | matches reference | matches reference |
| Array&lt;Boolean&gt; | accepts | accepts | matches reference | matches reference |
| Nullable String | accepts | accepts | matches reference | matches reference |
| Ordinary enum | accepts | accepts | matches reference | matches reference |
| UTF-8 String literal | accepts | accepts | matches reference | matches reference |
| Array of named records | accepts | accepts | matches reference | matches reference |
| Hash literal and required lookup | accepts | accepts | matches reference | matches reference |
| Array each with live growth and index | accepts | accepts | matches reference | matches reference |
| Range each (inclusive / exclusive / reversed) | accepts | accepts | matches reference | matches reference |
| Range with captured endpoint effects (requires fn) | accepts | accepts | matches reference | matches reference |
| UTF-8 length, indexing, concatenation and interpolation | accepts | accepts | matches reference | matches reference |
| Unicode local identifier | rejects valid input | rejects valid input | not reached | rejects valid input |
| Unicode scalar escapes | accepts | accepts | matches reference | matches reference |
| String search and code-point APIs | accepts | accepts | matches reference | matches reference |
| Empty String and ASCII indexing | accepts | accepts | matches reference | matches reference |
| Mixed numeric arithmetic and conversion | accepts | accepts | matches reference | matches reference |
| Portable Integer endpoints | accepts | accepts | matches reference | matches reference |
| Semicolon and comment separators | accepts | accepts | matches reference | matches reference |
| Recursive calls and all-path returns | accepts | accepts | matches reference | matches reference |
| Mutable parameter rebinding is local | accepts | accepts | matches reference | matches reference |
| Named-only arguments and reordering | accepts | accepts | matches reference | matches reference |
| Default arguments refer to earlier arguments | accepts | accepts | matches reference | matches reference |
| Value-producing if | accepts | accepts | matches reference | matches reference |
| Conditional expression evaluates one branch | accepts | accepts | matches reference | matches reference |
| Postfix return and loop transfers | accepts | accepts | matches reference | matches reference |
| Scalar case and case expression | accepts | accepts | matches reference | matches reference |
| Record defaults and reordered explicit fields | accepts | accepts | matches reference | matches reference |
| Reject unsupported record equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nullable narrowing and early return | accepts | accepts | matches reference | matches reference |
| Nullable short-circuit and safe member | accepts | accepts | matches reference | matches reference |
| Nil equality | accepts | accepts | matches reference | matches reference |
| Payload enum and exhaustive case | accepts | accepts | matches reference | matches reference |
| Raw-value enum | accepts | accepts | matches reference | matches reference |
| Transparent type alias | accepts | accepts | matches reference | matches reference |
| Nominal newtype construction and projection | accepts | accepts | matches reference | matches reference |
| Parameters following nested generic annotations | accepts | accepts | matches reference | matches reference |
| Generic function application | accepts | accepts | matches reference | matches reference |
| Generic record | accepts | accepts | matches reference | matches reference |
| Literal-field union narrowing | accepts | accepts | matches reference | matches reference |
| Typed function value and lexical capture | accepts | accepts | matches reference | matches reference |
| Function value mutates captured binding | accepts | accepts | matches reference | matches reference |
| Array alias and parameter rebinding | accepts | accepts | matches reference | matches reference |
| Array index captured before growing RHS | accepts | accepts | matches reference | matches reference |
| Nested managed Array values | accepts | accepts | matches reference | matches reference |
| Array value-producing iteration | accepts | accepts | matches reference | matches reference |
| Hash key/value iteration | accepts | accepts | matches reference | matches reference |
| Empty Hash inference and update | accepts | accepts | matches reference | matches reference |
| Hash deletion, membership and size | accepts | accepts | matches reference | matches reference |
| Stored Range bounds and conversion | accepts | accepts | matches reference | matches reference |
| Inclusive Range maximum endpoint | accepts | accepts | matches reference | matches reference |
| Result storage and exhaustive case | accepts | accepts | matches reference | matches reference |
| Result try propagation | accepts | accepts | matches reference | matches reference |
| Result catch recovery | accepts | accepts | matches reference | matches reference |
| Class fields, initializer and method | rejects valid input | rejects valid input | not reached | rejects valid input |
| Explicit interface conformance | rejects valid input | rejects valid input | not reached | rejects valid input |
| Module declaration and constant | accepts | accepts | matches reference | matches reference |
| Top-level constant | accepts | accepts | matches reference | matches reference |
| Symbol literal equality | accepts | accepts | matches reference | matches reference |
| Named import alias and reachable file | accepts | accepts | matches reference | matches reference |
| Reject unused local binding | accepts; reference rejects | accepts; reference rejects | differs | output differs |
| Reject immutable binding assignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject record field rebinding | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject non-Boolean condition | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject incorrect call argument type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject missing value-bearing return | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject break outside a loop | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject escaping branch-local binding | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject unchecked nullable member access | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject out-of-range Integer literal | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject general postfix if | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject implicit interpolation conversion | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array bounds failure | accepts | accepts | differs | rejects as reference |
| String bounds failure | accepts | accepts | differs | rejects as reference |
| Portable Integer runtime overflow | accepts | accepts | matches reference | rejects as reference |
| Reject unsupported Hash compound assignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject unsupported brace Unicode escape | rejects as reference | rejects as reference | not reached | rejects as reference |
| Embedded zero and supplementary scalar escapes | accepts | accepts | matches reference | matches reference |
| Reject unsupported array equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject unsupported hash equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unsupported String repetition and REPL diagnostic origin | rejects as reference | rejects as reference | not reached | rejects as reference |
| UTF-8 collection storage and aliases | accepts | accepts | matches reference | matches reference |
| UTF-8 and NUL literal byte boundaries | accepts | accepts | matches reference | matches reference |
| Long UTF-8 literals | accepts | accepts | matches reference | matches reference |
| Required named-only arguments preserve authored evaluation order | accepts | accepts | matches reference | matches reference |
| Record labels may be reordered with contextual field types | accepts | accepts | matches reference | matches reference |
| Duplicate named arguments are rejected | rejects as reference | rejects as reference | not reached | rejects as reference |
| Positional-only parameters cannot be supplied by name | rejects as reference | rejects as reference | not reached | rejects as reference |
| Positional arguments cannot follow named arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named-only arguments retain imported declaration identity | accepts | accepts | matches reference | matches reference |
| Imported record aliases survive retained bindings | accepts | accepts | matches reference | matches reference |
| Standard package aliases preserve checked receiver identity | accepts | accepts | matches reference | matches reference |
| Session declarations supersede automatic project imports | accepts | accepts | matches reference | matches reference |
| Defaults read preceding parameters | accepts | accepts | matches reference | matches reference |
| Fresh managed defaults, explicit order and skipped traps | accepts | accepts | matches reference | matches reference |
| Required named parameter after positional defaults | accepts | accepts | matches reference | matches reference |
| Imported function and record defaults retain declaration scope | accepts | accepts | matches reference | matches reference |
| Reject a default referencing a later parameter | rejects as reference | rejects as reference | not reached | rejects as reference |
| Check a default even when the caller supplies a value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject a default referencing a later record field | rejects as reference | rejects as reference | not reached | rejects as reference |
| If effects | accepts | accepts | matches reference | matches reference |
| If managed | accepts | accepts | matches reference | matches reference |
| If widening | accepts | accepts | matches reference | matches reference |
| If transfer | accepts | accepts | matches reference | matches reference |
| If elsif | accepts | accepts | matches reference | matches reference |
| Case effects | accepts | accepts | matches reference | matches reference |
| Case string | accepts | accepts | matches reference | matches reference |
| Guard void | accepts | accepts | matches reference | matches reference |
| Assignment transfer | accepts | accepts | matches reference | matches reference |
| Guard loop | accepts | accepts | matches reference | matches reference |
| Guard each | accepts | accepts | matches reference | matches reference |
| Logical transfer | accepts | accepts | matches reference | matches reference |
| Guard return | accepts | accepts | matches reference | matches reference |
| Logical operators inside ternary branches | accepts | accepts | matches reference | matches reference |
| Immutable Array capability survives a value branch | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nullable scalars preserve zero and false | accepts | accepts | matches reference | matches reference |
| Nullable assignment retains its precise flow type | accepts | accepts | matches reference | matches reference |
| Omitted default differs from explicit nil | accepts | accepts | matches reference | matches reference |
| Nullable Array elements and stable record fields | accepts | accepts | matches reference | matches reference |
| Safe navigation evaluates the receiver once | accepts | accepts | matches reference | matches reference |
| Safe navigation skips argument side effects | accepts | accepts | matches reference | matches reference |
| Nullable Hash and Array storage | accepts | accepts | matches reference | output differs |
| Loop guards recheck replaced nullable values | accepts | accepts | matches reference | output differs |
| Safe navigation preserves nullable field results | accepts | accepts | matches reference | matches reference |
| Reject nonnullable use after assignment of nil | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject stale nullable field narrowing after receiver assignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Retained nullable assignments preserve checked flow and display | accepts | accepts | matches reference | matches reference |
| Rejected REPL assignment preserves the preceding fact | rejects as reference | rejects as reference | not reached | rejects as reference |
| Conditional REPL replacement invalidates the preceding fact | accepts | accepts | matches reference | output differs |
| Partial failure discards stale REPL narrowing | accepts | accepts | differs | rejects as reference |
| Retained optional values use lazy safe navigation | accepts | accepts | matches reference | matches reference |
| REPL rejects authored return outside a function | accepts | accepts | matches reference | rejects as reference |
| Enum named payload order and patterns | accepts | accepts | matches reference | matches reference |
| Recursive enum values stored in Hash | accepts | accepts | matches reference | matches reference |
| Enum payload shadows an outer binding | accepts | accepts | matches reference | matches reference |
| Nullable enum and record payloads | accepts | accepts | matches reference | matches reference |
| Enum selector order and lexical loop transfers | accepts | accepts | matches reference | matches reference |
| Enum managed payload retains an Array alias | accepts | accepts | matches reference | matches reference |
| Recursive record and enum fields | accepts | accepts | matches reference | rejects as reference |
| Imported enum alias preserves nominal identity | accepts | accepts | matches reference | matches reference |
| Reject an incomplete enum case | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject assignment to enum payload binding | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject equality across enum declarations | rejects as reference | rejects as reference | not reached | rejects as reference |
| Retained Range binding preserves bounds without replay | accepts | accepts | matches reference | matches reference |
| Distinct concrete record instances | accepts | accepts | matches reference | matches reference |
| Nested nominal type arguments | accepts | accepts | matches reference | matches reference |
| Generic enum constructors and exhaustive patterns | accepts | accepts | matches reference | matches reference |
| Recursive generic record with optional tail | accepts | accepts | matches reference | matches reference |
| Recursive generic enum with managed containers | accepts | accepts | matches reference | matches reference |
| Nested generic arguments and named payload evaluation order | accepts | accepts | matches reference | matches reference |
| Generic templates and arguments retain import identity | accepts | accepts | matches reference | matches reference |
| Generic record arguments are invariant | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum arguments are invariant | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic records with concrete default fields | accepts | accepts | matches reference | matches reference |
| Explicit nominal type argument count | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unused generic fields require valid types | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: unit | accepts | accepts | matches reference | matches reference |
| Result: try each | accepts | accepts | matches reference | matches reference |
| Result: try precedence | accepts | accepts | matches reference | matches reference |
| Result: try error conversion | accepts | accepts | matches reference | matches reference |
| Result: catch lazy once | accepts | accepts | matches reference | matches reference |
| Result: catch transfers | accepts | accepts | matches reference | matches reference |
| Result: catch conversion | accepts | accepts | matches reference | matches reference |
| Result: required use | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: required use binding | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: required use transfer | accepts | accepts | matches reference | matches reference |
| Result: try homonym | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: try incompatible error | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: try non result function | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: catch immutable error | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: catch argument rejected | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: managed payloads | accepts | accepts | matches reference | matches reference |
| Result: nested payload | accepts | accepts | matches reference | matches reference |
| Result: nullable error | accepts | accepts | matches reference | matches reference |
| Result: unused loop local | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: unused branch local | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: explicit reassignment | accepts | accepts | matches reference | matches reference |
| Result: catch empty handler | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: catch nested composition | rejects as reference | rejects as reference | not reached | rejects as reference |
| Result: user homonym required use | accepts | accepts | matches reference | matches reference |
| Generic function identity | accepts | accepts | matches reference | matches reference |
| Generic function generic default | accepts | accepts | matches reference | matches reference |
| Generic function recursive | accepts | accepts | matches reference | matches reference |
| Generic function generic nested | accepts | accepts | matches reference | matches reference |
| Generic function generic nil | accepts | accepts | matches reference | matches reference |
| Generic function generic result | accepts | accepts | matches reference | matches reference |
| Generic container values and abstract element access | accepts | accepts | matches reference | matches reference |
| Generic function aliases and nominal argument identity | accepts | accepts | matches reference | matches reference |
| Reject mutable aliases of unconstrained immutable type parameters | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic iteration reads typed elements without introducing mutation | accepts | accepts | matches reference | matches reference |
| Explicit and omitted generic defaults execute in declaration order | accepts | accepts | matches reference | matches reference |
| Nominal field types use declaration scope rather than caller type parameters | accepts | accepts | matches reference | matches reference |
| Reject generic unused unresolved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject generic unused arithmetic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject generic used arithmetic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject generic unused invalid return | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic functions require explicit type arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic function type argument counts are exact | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic function arguments retain explicit type identity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Local values shadow generic functions | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unused generic parameter defaults are checked abstractly | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unused generic functions require complete return flow | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic record defaults use preceding fields | accepts | accepts | matches reference | matches reference |
| Generic record defaults construct typed containers | accepts | accepts | matches reference | output differs |
| Omitted generic managed defaults allocate independently | accepts | accepts | matches reference | matches reference |
| Generic defaults retain nested nominal values | accepts | accepts | matches reference | matches reference |
| Generic defaults call generic functions with distinct type owners | accepts | accepts | matches reference | matches reference |
| Generic defaults preserve nil and explicit values | accepts | accepts | matches reference | matches reference |
| Generic defaults construct standard Result payloads | accepts | accepts | matches reference | matches reference |
| Generic explicit fields precede defaults in declaration order | accepts | accepts | matches reference | matches reference |
| Imported generic defaults retain declaration scope and aliases | accepts | accepts | matches reference | matches reference |
| Generic defaults use lazy typed control expressions | accepts | accepts | matches reference | matches reference |
| Unused generic defaults accept valid abstract values | accepts | accepts | matches reference | matches reference |
| Reject concrete values as unconstrained generic defaults even when unused | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject unresolved names in unused generic defaults | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject references to later fields in generic defaults | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject self-references in generic field defaults | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject required fields after generic record defaults | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject arithmetic on unconstrained generic default values | rejects as reference | rejects as reference | not reached | rejects as reference |
| Explicit fields do not hide invalid generic defaults | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic defaults cannot capture caller locals | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic defaults retain prior fields through full if and enum case expressions | accepts | accepts | matches reference | matches reference |
| Scalar aliases in signatures | accepts | accepts | matches reference | matches reference |
| Aliases in Array and Hash arguments | accepts | accepts | matches reference | output differs |
| Nullable generic alias | accepts | accepts | matches reference | matches reference |
| Identity alias in generic function signatures | accepts | accepts | matches reference | matches reference |
| Record constructor through an alias | accepts | accepts | matches reference | matches reference |
| Generic record alias and field defaults | accepts | accepts | matches reference | matches reference |
| Enum variants through an alias | accepts | accepts | matches reference | output differs |
| Generic enum alias and pattern inference | accepts | accepts | matches reference | output differs |
| Reordered generic alias pattern arguments | accepts | accepts | matches reference | output differs |
| Nested generic alias pattern arguments | accepts | accepts | matches reference | output differs |
| Result alias propagation and recovery | accepts | accepts | matches reference | matches reference |
| Generic record defaults with aliased field types | accepts | accepts | matches reference | matches reference |
| Reject Void as an alias target | rejects as reference | rejects as reference | not reached | rejects as reference |
| Imported aliases and record construction | accepts | accepts | matches reference | matches reference |
| Alias target resolves in its defining module | accepts | accepts; reference rejects | differs | matches reference |
| Bare import of a type alias | accepts | accepts | matches reference | matches reference |
| Recursive nominal alias | accepts | accepts | matches reference | rejects as reference |
| Reject a direct alias cycle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject a growing generic alias cycle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject an unused unresolved alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject an unused alias with wrong arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject duplicate alias declarations | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject an alias with a nominal declaration name | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject incompatible generic alias arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject inconsistent repeated alias pattern parameters | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject mismatched concrete alias pattern arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Imported recursive alias in ordinary execution and REPL | accepts | accepts | matches reference | matches reference |
| Independent aliases in nested generic arguments | accepts | accepts | matches reference | matches reference |
| Unused typed callback body is checked, without constructing a function value | accepts | accepts | matches reference | matches reference |
| Generic aliases compose callback parameter and return types | accepts | accepts | matches reference | matches reference |
| Unused callback call rejects wrong arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unused callback call rejects a wrong argument type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unused callback call rejects a wrong return type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Callback type rejects Void as a parameter | rejects as reference | rejects as reference | not reached | rejects as reference |
| Anonymous positional and higher-order calls | accepts | accepts | matches reference | matches reference |
| Nested closures share cells across independent factories | accepts | accepts | matches reference | matches reference |
| Escaped iteration bindings retain independent cells | accepts | accepts | matches reference | matches reference |
| Concrete closure signatures and callable defaults | accepts | accepts | matches reference | matches reference |
| Immutable nullable proofs and mixed closure captures | accepts | accepts | matches reference | matches reference |
| Captured nominal Hash and Result values survive replacement | accepts | accepts | matches reference | matches reference |
| Retained shared closures run each initializer once | accepts | accepts | matches reference | matches reference |
| Closure and mutable Array cycles survive submission collection | accepts | accepts | matches reference | matches reference |
| Brace iteration with nested controls and lexical transfers | accepts | accepts | matches reference | matches reference |
| Multiline Array and Range brace iteration | accepts | accepts | matches reference | matches reference |
| Array and Range transformation values and indexed chains | accepts | accepts | matches reference | matches reference |
| Live traversal, retained values and reducer evaluation order | accepts | accepts | matches reference | matches reference |
| Transform closures, nested arrays and retained managed values | accepts | accepts | matches reference | matches reference |
| Collection block requires a value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Selection requires a Boolean predicate | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reducer preserves the accumulator type | rejects as reference | rejects as reference | not reached | rejects as reference |
| A collection block cannot return from its enclosing function | rejects as reference | rejects as reference | not reached | rejects as reference |
| Readonly receiver does not grant mutation through that reference | rejects as reference | rejects as reference | not reached | rejects as reference |
| Short-circuit Array and Range predicates and boundary values | accepts | accepts | matches reference | matches reference |
| Live predicate sources, captures and generic callbacks | accepts | accepts | matches reference | matches reference |
| Predicates require Boolean results | rejects as reference | rejects as reference | not reached | rejects as reference |
| Predicates require a result value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Predicate blocks cannot return from their enclosing function | rejects as reference | rejects as reference | not reached | rejects as reference |
| Indexed predicates remain unsupported | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nullable Array and Range search results and short-circuiting | accepts | accepts | matches reference | matches reference |
| Retained search values, live traversal and managed captures | accepts | accepts | matches reference | matches reference |
| Search predicates require Boolean results | rejects as reference | rejects as reference | not reached | rejects as reference |
| Indexed search blocks remain unsupported | rejects as reference | rejects as reference | not reached | rejects as reference |
| Integer methods | accepts | accepts | matches reference | matches reference |
| Integer method order | accepts | accepts | matches reference | matches reference |
| Integer clamp invalid | accepts | accepts | matches reference | rejects as reference |
| Integer method extra argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Integer method missing argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Integer clamp missing bound | rejects as reference | rejects as reference | not reached | rejects as reference |
| Integer method float argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Integer method nullable argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Float rounding at ties, subnormals and portable Integer limits | accepts | accepts | matches reference | matches reference |
| Float finite, infinite and NaN classification | accepts | accepts | matches reference | matches reference |
| Float absolute value preserves NaN and normalizes negative zero | accepts | accepts | matches reference | matches reference |
| Float receiver effects and optional calls | accepts | accepts | matches reference | matches reference |
| Float floor nonfinite | accepts | accepts | matches reference | rejects as reference |
| Float floor nan | accepts | accepts | matches reference | rejects as reference |
| Float floor outside | accepts | accepts | matches reference | rejects as reference |
| Float ceil nonfinite | accepts | accepts | matches reference | rejects as reference |
| Float ceil nan | accepts | accepts | matches reference | rejects as reference |
| Float ceil outside | accepts | accepts | matches reference | rejects as reference |
| Float round nonfinite | accepts | accepts | matches reference | rejects as reference |
| Float round nan | accepts | accepts | matches reference | rejects as reference |
| Float round outside | accepts | accepts | matches reference | rejects as reference |
| Float extra argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Float aliases, record receivers and captured calls retain managed values | accepts | accepts | matches reference | matches reference |
| Float to_i nonfinite failure class | accepts | accepts | matches reference | rejects as reference |
| Float to_i nan failure class | accepts | accepts | matches reference | rejects as reference |
| Float to_i outside failure class | accepts | accepts | matches reference | rejects as reference |
| Float to_i negative-outside failure class | accepts | accepts | matches reference | rejects as reference |
| Float rounding preserves an absent nullable result | rejects as reference | rejects as reference | not reached | rejects as reference |
| Float classification returns Boolean | rejects as reference | rejects as reference | not reached | rejects as reference |
| String queries use code-point offsets and literal matching | accepts | accepts | matches reference | matches reference |
| String query empty and longer-pattern boundaries | accepts | accepts | matches reference | matches reference |
| String receiver capture, source order and managed values | accepts | accepts | matches reference | matches reference |
| Optional String queries skip arguments and flatten optional results | accepts | accepts | matches reference | matches reference |
| String query arguments preserve lexical loop transfers | accepts | accepts | matches reference | matches reference |
| String empty query rejects extra arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| String search requires a substring | rejects as reference | rejects as reference | not reached | rejects as reference |
| String search rejects Integer arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| String search requires a present substring | rejects as reference | rejects as reference | not reached | rejects as reference |
| String search results require narrowing | rejects as reference | rejects as reference | not reached | rejects as reference |
| String predicate results remain Boolean | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unicode sequences | accepts | accepts | matches reference | matches reference |
| Empty single | accepts | accepts | matches reference | matches reference |
| Fresh array storage | accepts | accepts | matches reference | matches reference |
| Optional transforms | accepts | accepts | matches reference | matches reference |
| Managed closures | accepts | accepts | matches reference | matches reference |
| Nul preservation | accepts | accepts | matches reference | matches reference |
| Chars arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Codepoints arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reverse arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Readonly derived array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Point element type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Character element type | rejects as reference | rejects as reference | not reached | rejects as reference |
| String slice success | accepts | accepts | matches reference | matches reference |
| String slice captures receiver before evaluating endpoints | accepts | accepts | matches reference | matches reference |
| String slice failure negative start | accepts | accepts | differs | rejects as reference |
| String slice failure negative end | accepts | accepts | differs | rejects as reference |
| String slice failure reversed | accepts | accepts | differs | rejects as reference |
| String slice failure exclusive outside | accepts | accepts | differs | rejects as reference |
| String slice failure inclusive end | accepts | accepts | differs | rejects as reference |
| String slice failure portable max | accepts | accepts | differs | rejects as reference |
| String slice optional | accepts | accepts | matches reference | matches reference |
| String slice range values | accepts | accepts | matches reference | matches reference |
| String slice unicode units | accepts | accepts | matches reference | matches reference |
| String slice transfer | accepts | accepts | matches reference | matches reference |
| String slice invalid order | accepts | accepts | differs | rejects as reference |
| String slice missing argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| String slice extra argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| String slice wrong argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| String slice nullable argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| String slice wrong result | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape simple controls | accepts | accepts | matches reference | matches reference |
| String escape quote backslash | accepts | accepts | matches reference | matches reference |
| String escape escaped interpolation | accepts | accepts | matches reference | matches reference |
| String escape octal nul | accepts | accepts | matches reference | matches reference |
| String escape octal ascii | accepts | accepts | matches reference | matches reference |
| String escape octal invalid byte | accepts | accepts | matches reference | matches reference |
| String escape hex nul | accepts | accepts | matches reference | matches reference |
| String escape hex ascii | accepts | accepts | matches reference | matches reference |
| String escape hex utf8 | accepts | accepts | matches reference | matches reference |
| String escape hex astral | accepts | accepts | matches reference | matches reference |
| String escape hex invalid byte | accepts | accepts | matches reference | matches reference |
| String escape unicode bmp | accepts | accepts | matches reference | matches reference |
| String escape unicode astral | accepts | accepts | matches reference | matches reference |
| String escape unicode limit | accepts | accepts | matches reference | matches reference |
| String escape escaped hash not interpolation | accepts | accepts | matches reference | matches reference |
| String escape unicode hash not interpolation | accepts | accepts | matches reference | matches reference |
| String escape mixed interpolation | accepts | accepts | matches reference | matches reference |
| String escape invalid unknown | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid short hex | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid hex digit | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid short unicode | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid surrogate | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid unicode high | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid octal high | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid octal digit | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid short octal | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid brace | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid interpolated escape | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape scalar boundaries | accepts | accepts | matches reference | matches reference |
| String escape byte boundaries | accepts | accepts | matches reference | matches reference |
| String escape digit boundaries | accepts | accepts | matches reference | matches reference |
| String escape all byte values | accepts | accepts | matches reference | matches reference |
| String escape invalid large unicode | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid last surrogate | rejects as reference | rejects as reference | not reached | rejects as reference |
| String escape invalid large octal | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array edges | accepts | accepts | matches reference | matches reference |
| Array empty | accepts | accepts | matches reference | matches reference |
| Array copies | accepts | accepts | matches reference | matches reference |
| Array shallow | accepts | accepts | matches reference | matches reference |
| Array slice live | accepts | accepts | matches reference | matches reference |
| Array slice rebind | accepts | accepts | matches reference | matches reference |
| Array first empty | accepts | accepts | differs | rejects as reference |
| Array last empty | accepts | accepts | differs | rejects as reference |
| Array slice negative | accepts | accepts | differs | rejects as reference |
| Array optional | accepts | accepts | matches reference | matches reference |
| Array borrowed mutable | accepts | accepts | matches reference | matches reference |
| Array borrowed readonly | accepts | accepts | matches reference | matches reference |
| Array temporary first mutation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array nullable items | accepts | accepts | matches reference | matches reference |
| Array float boolean string | accepts | accepts | matches reference | matches reference |
| Array receiver order | accepts | accepts | matches reference | matches reference |
| Array optional slice | accepts | accepts | matches reference | matches reference |
| Array generic managed | accepts | accepts | matches reference | matches reference |
| Array enum items | accepts | accepts | matches reference | matches reference |
| Array shallow callable | accepts | accepts | matches reference | matches reference |
| Array slice boundaries | accepts | accepts | matches reference | matches reference |
| Array copy fresh outer | accepts | accepts | matches reference | matches reference |
| Array slice return | accepts | accepts | matches reference | matches reference |
| Array slice next | accepts | accepts | matches reference | matches reference |
| Array invalid reversed | accepts | accepts | differs | rejects as reference |
| Array invalid past | accepts | accepts | differs | rejects as reference |
| Array invalid inclusive end | accepts | accepts | differs | rejects as reference |
| Array invalid max exclusive | accepts | accepts | differs | rejects as reference |
| Array invalid max inclusive | accepts | accepts | differs | rejects as reference |
| Array invalid min start | accepts | accepts | differs | rejects as reference |
| Array invalid emptypredicate arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array invalid first arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array invalid last arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array invalid dup arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array invalid reverse arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array invalid slice type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array invalid slice arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array temporary copy mutation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array callable result | accepts | accepts | matches reference | matches reference |
| Array mutation edges | accepts | accepts | matches reference | matches reference |
| Array mutation representations | accepts | accepts | matches reference | matches reference |
| Array mutation nullable items | accepts | accepts | matches reference | matches reference |
| Array mutation managed alias | accepts | accepts | matches reference | matches reference |
| Array mutation receiver order | accepts | accepts | matches reference | matches reference |
| Array mutation argument growth | accepts | accepts | matches reference | matches reference |
| Array mutation argument clear | accepts | accepts | matches reference | matches reference |
| Array mutation optional | accepts | accepts | matches reference | matches reference |
| Array mutation each pop | accepts | accepts | matches reference | matches reference |
| Array mutation each shift | accepts | accepts | matches reference | matches reference |
| Array mutation each unshift | accepts | accepts | matches reference | matches reference |
| Array mutation map shift | accepts | accepts | matches reference | matches reference |
| Array mutation select shift | accepts | accepts | matches reference | matches reference |
| Array mutation reduce pop | accepts | accepts | matches reference | matches reference |
| Array mutation find shift | accepts | accepts | matches reference | matches reference |
| Array mutation assignment unshift | accepts | accepts | matches reference | matches reference |
| Array mutation assignment rebuild | accepts | accepts | matches reference | matches reference |
| Array mutation assignment shrink | accepts | accepts | differs | rejects as reference |
| Array mutation compound shrink | accepts | accepts | differs | rejects as reference |
| Array mutation invalid target first | accepts | accepts | differs | rejects as reference |
| Array mutation loop shrink bounds | accepts | accepts | differs | rejects as reference |
| Array mutation transfer | accepts | accepts | matches reference | matches reference |
| Array mutation readonly pop | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation readonly shift | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation readonly unshift | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation temporary | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation wrong element | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation missing unshift | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation extra pop | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation extra shift | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array mutation pop empty | accepts | accepts | differs | rejects as reference |
| Array mutation shift empty | accepts | accepts | differs | rejects as reference |
| Array query integers | accepts | accepts | matches reference | matches reference |
| Array query empty | accepts | accepts | matches reference | matches reference |
| Array query booleans | accepts | accepts | matches reference | matches reference |
| Array query unicode nul | accepts | accepts | matches reference | matches reference |
| Array query floats | accepts | accepts | matches reference | matches reference |
| Array query enums | accepts | accepts | matches reference | matches reference |
| Array query fresh | accepts | accepts | matches reference | matches reference |
| Array query nested alias | accepts | accepts | matches reference | matches reference |
| Array query record concat | accepts | accepts | matches reference | matches reference |
| Array query hash concat | accepts | accepts | matches reference | matches reference |
| Array query nullable concat | accepts | accepts | matches reference | matches reference |
| Array query callable concat | accepts | accepts | matches reference | matches reference |
| Array query generic concat | accepts | accepts | matches reference | matches reference |
| Array query include receiver | accepts | accepts | matches reference | matches reference |
| Array query include growth | accepts | accepts | matches reference | matches reference |
| Array query count receiver | accepts | accepts | matches reference | matches reference |
| Array query count growth | accepts | accepts | matches reference | matches reference |
| Array query index receiver | accepts | accepts | matches reference | matches reference |
| Array query index growth | accepts | accepts | matches reference | matches reference |
| Array query concat receiver | accepts | accepts | matches reference | matches reference |
| Array query concat growth | accepts | accepts | matches reference | matches reference |
| Array query optional | accepts | accepts | matches reference | matches reference |
| Array query concat optional | accepts | accepts | matches reference | matches reference |
| Array query transfer | accepts | accepts | matches reference | matches reference |
| Array query predicate nesting | accepts | accepts | matches reference | matches reference |
| Array query expression nesting | accepts | accepts | matches reference | matches reference |
| Array query nil values | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query nullable equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query record equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query record unique | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query payload equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query nested equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query function equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query wrong needle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query wrong concat | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query missing include | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query extra count | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query missing index | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query extra unique | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query missing concat | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array query temporary mutation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range string keys | accepts | accepts | matches reference | matches reference |
| Hash and Range integer keys | accepts | accepts | matches reference | matches reference |
| Hash and Range empty | accepts | accepts | matches reference | matches reference |
| Hash and Range snapshot values | accepts | accepts | matches reference | matches reference |
| Hash and Range snapshot deleted | accepts | accepts | matches reference | matches reference |
| Hash and Range snapshot rebound | accepts | accepts | matches reference | matches reference |
| Hash and Range snapshot growth | accepts | accepts | matches reference | matches reference |
| Hash and Range snapshot alias | accepts | accepts | matches reference | matches reference |
| Hash and Range shallow values | accepts | accepts | matches reference | matches reference |
| Hash and Range block rebinding | accepts | accepts | matches reference | matches reference |
| Hash and Range float values | accepts | accepts | matches reference | matches reference |
| Hash and Range boolean values | accepts | accepts | matches reference | matches reference |
| Hash and Range string values | accepts | accepts | matches reference | matches reference |
| Hash and Range nullable values | accepts | accepts | matches reference | matches reference |
| Hash and Range record values | accepts | accepts | matches reference | matches reference |
| Hash and Range callable values | accepts | accepts | matches reference | matches reference |
| Hash and Range range values | accepts | accepts | matches reference | matches reference |
| Hash and Range nested | accepts | accepts | matches reference | matches reference |
| Hash and Range transfers | accepts | accepts | matches reference | matches reference |
| Hash and Range return | accepts | accepts | matches reference | matches reference |
| Hash and Range generic | accepts | accepts | matches reference | matches reference |
| Hash and Range one parameter | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range three parameters | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range indexed hash | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range duplicate parameter | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range extra argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range array pair | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range range pair | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range hash transform | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range range ends | accepts | accepts | matches reference | matches reference |
| Hash and Range range extrema | accepts | accepts | matches reference | matches reference |
| Hash and Range range fresh | accepts | accepts | matches reference | matches reference |
| Hash and Range range effect | accepts | accepts | matches reference | matches reference |
| Hash and Range range optional | accepts | accepts | matches reference | matches reference |
| Hash and Range range carrier | accepts | accepts | matches reference | matches reference |
| Hash and Range range growth | accepts | accepts | matches reference | matches reference |
| Hash and Range range extra | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range range string | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash and Range mutable value | accepts | accepts | matches reference | matches reference |
| Hash and Range captured bindings | accepts | accepts | matches reference | matches reference |
| Array join edges | accepts | accepts | matches reference | matches reference |
| Array join unicode nul | accepts | accepts | matches reference | matches reference |
| Array join byte boundaries | accepts | accepts | matches reference | matches reference |
| Array join temporary | accepts | accepts | matches reference | matches reference |
| Array join readonly | accepts | accepts | matches reference | matches reference |
| Array join grow | accepts | accepts | matches reference | matches reference |
| Array join shorten | accepts | accepts | matches reference | matches reference |
| Array join clear | accepts | accepts | matches reference | matches reference |
| Array join replace | accepts | accepts | matches reference | matches reference |
| Array join rebind | accepts | accepts | matches reference | matches reference |
| Array join grow rebind | accepts | accepts | matches reference | matches reference |
| Array join order | accepts | accepts | matches reference | matches reference |
| Array join empty argument | accepts | accepts | matches reference | matches reference |
| Array join optional | accepts | accepts | matches reference | matches reference |
| Array join transfer | accepts | accepts | matches reference | matches reference |
| Array join nested | accepts | accepts | matches reference | matches reference |
| Array join lambda | accepts | accepts | matches reference | matches reference |
| Array join integer elements | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array join nullable elements | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array join boolean elements | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array join nested elements | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array join wrong separator | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array join missing separator | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array join extra separator | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function values | accepts | accepts | matches reference | matches reference |
| Named function managed result | accepts | accepts | matches reference | matches reference |
| Named function float boolean | accepts | accepts | matches reference | matches reference |
| Named function void zero | accepts | accepts | matches reference | matches reference |
| Named function storage | accepts | accepts | matches reference | matches reference |
| Named function nullable | accepts | accepts | matches reference | matches reference |
| Named function nullable anonymous | accepts | accepts | matches reference | matches reference |
| Named function nullable parameter | accepts | accepts | matches reference | matches reference |
| Named function shadow capture | accepts | accepts | matches reference | matches reference |
| Named function mutable parameter | accepts | accepts | matches reference | matches reference |
| Named function recursion | accepts | accepts | matches reference | matches reference |
| Named function result | accepts | accepts | matches reference | matches reference |
| Named function generic use | accepts | accepts | matches reference | matches reference |
| Named function adapters | accepts | accepts | matches reference | matches reference |
| Named function imports | accepts | accepts | matches reference | matches reference |
| Named function default rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function keyword rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function generic rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function parameter rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function result rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function signature arity rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function arity rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function argument rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function keyword call rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function nullable call rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function result ignored | rejects as reference | rejects as reference | not reached | matches reference |
| Named function imported default rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Named function field optional | accepts | accepts | matches reference | matches reference |
| Named function field order | accepts | accepts | matches reference | matches reference |
| Named function generic nested | accepts | accepts | matches reference | matches reference |
| Hash key spelling quoted | accepts | accepts | matches reference | matches reference |
| Hash key spelling computed | accepts | accepts | matches reference | matches reference |
| Hash key spelling integer | accepts | accepts | matches reference | matches reference |
| Hash key spelling effects | accepts | accepts | matches reference | matches reference |
| Hash key spelling boolean-rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash key spelling nil-rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| String trimming unicode white space | accepts | accepts | matches reference | matches reference |
| String trimming non white space | accepts | accepts | matches reference | matches reference |
| String trimming empty and all space | accepts | accepts | matches reference | matches reference |
| String trimming directional | accepts | accepts | matches reference | matches reference |
| String trimming interior and nul | accepts | accepts | matches reference | matches reference |
| String trimming unicode count | accepts | accepts | matches reference | matches reference |
| String trimming invalid bytes | accepts | accepts | matches reference | matches reference |
| String trimming optional | accepts | accepts | matches reference | matches reference |
| String trimming receiver effects | accepts | accepts | matches reference | matches reference |
| String trimming managed values | accepts | accepts | matches reference | matches reference |
| String trimming generic alias | accepts | accepts | matches reference | matches reference |
| String trimming source retention | accepts | accepts | matches reference | matches reference |
| String trimming strip arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| String trimming lstrip arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| String trimming rstrip arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| String trimming wrong result | rejects as reference | rejects as reference | not reached | rejects as reference |
| String trimming nullable rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| String trimming named argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol names and types | accepts | accepts | matches reference | matches reference |
| Symbol keyword names | accepts | accepts | matches reference | matches reference |
| Symbol operator names | accepts | accepts | matches reference | matches reference |
| Symbol quoted unicode | accepts | accepts | matches reference | matches reference |
| Symbol quoted escapes | accepts | accepts | matches reference | matches reference |
| Symbol quoted literal interpolation | accepts | accepts | matches reference | matches reference |
| Symbol normal interpolation | accepts | accepts | matches reference | matches reference |
| Symbol hash labels | accepts | accepts | matches reference | matches reference |
| Symbol arguments and defaults | accepts | accepts | matches reference | matches reference |
| Symbol record defaults | accepts | accepts | matches reference | matches reference |
| Symbol controls | accepts | accepts | matches reference | matches reference |
| Symbol generic alias | accepts | accepts | matches reference | matches reference |
| Symbol managed callback | accepts | accepts | matches reference | matches reference |
| Symbol optional | accepts | accepts | matches reference | matches reference |
| Symbol arrays and range | accepts | accepts | matches reference | matches reference |
| Multiline interpolation reference boundary | accepts; reference rejects | accepts; reference rejects | differs | output differs |
| Symbol interpolation default origins | accepts | accepts | matches reference | matches reference |
| Symbol interpolation lambda origins | accepts | accepts | matches reference | matches reference |
| Symbol interpolation local ids | accepts | accepts | matches reference | matches reference |
| Symbol interpolation unknown rejection | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid integer assignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid addition | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid condition | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid escape | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid scalar | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid quoted nesting | rejects as reference | rejects as reference | not reached | rejects as reference |
| Symbol invalid missing name | rejects as reference | rejects as reference | not reached | rejects as reference |
| Keyword Symbols retain String semantics in files and the REPL | accepts | accepts | matches reference | matches reference |
| Symbol patterns require an explicit String literal | rejects as reference | rejects as reference | not reached | rejects as reference |
| Inferred and annotated scalar constants | accepts | accepts | matches reference | matches reference |
| Ordered constant initializers execute once | accepts | accepts | matches reference | matches reference |
| Managed Array Hash and record constants | accepts | accepts | matches reference | output differs |
| Typed empty containers and nullable constants | accepts | accepts | matches reference | matches reference |
| Function-valued constants retain global reads | accepts | accepts | matches reference | matches reference |
| Nested namespace constants preserve lexical parents | accepts | accepts | matches reference | matches reference |
| Reopened namespaces share constant identity | accepts | accepts | matches reference | matches reference |
| Declaration-owned defaults read lexical constants | accepts | accepts | matches reference | matches reference |
| Scalar copies may have mutable local bindings | accepts | accepts | matches reference | matches reference |
| Array parameter mutability preserves shared identity | accepts | accepts | matches reference | matches reference |
| Named constant imports preserve source ownership | accepts | accepts | matches reference | matches reference |
| Bare module aliases retain constant and method identities | accepts | accepts | matches reference | matches reference |
| Imported module initializers precede their consumers once | accepts | accepts | matches reference | matches reference |
| Constant Array bindings reject direct mutation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Constant Array bindings reject indexed writes | rejects as reference | rejects as reference | not reached | rejects as reference |
| Constant references cannot become mutable bindings | rejects as reference | rejects as reference | not reached | rejects as reference |
| Hash parameter mutability preserves shared identity | accepts | accepts | matches reference | output differs |
| Constant bindings cannot be reassigned | rejects as reference | rejects as reference | not reached | rejects as reference |
| Qualified constant bindings cannot be reassigned | rejects as reference | rejects as reference | not reached | rejects as reference |
| Duplicate constant declarations are rejected | rejects as reference | rejects as reference | not reached | rejects as reference |
| Constant annotations check initializer types | rejects as reference | rejects as reference | not reached | rejects as reference |
| Stable nullable constant reads narrow after a guard | accepts | accepts | matches reference | matches reference |
| An initializer invokes an earlier function-valued constant | accepts | accepts | matches reference | matches reference |
| Module records retain their lexical declaration owner | accepts | accepts | matches reference | matches reference |
| Nested module enums preserve qualified variants | accepts | accepts | matches reference | matches reference |
| Private module methods permit lexical calls | accepts | accepts | matches reference | matches reference |
| Private module methods reject external calls | rejects as reference | rejects as reference | not reached | rejects as reference |
| Qualified module payload patterns are exhaustive | accepts | accepts | matches reference | matches reference |
| Qualified generic record aliases preserve constructor identity | accepts | accepts | matches reference | matches reference |
| Module aliases and defaults resolve lexical type owners | accepts | accepts | matches reference | matches reference |
| Private methods permit calls qualified by their own module | accepts | accepts | matches reference | matches reference |
| Private methods reject external qualified access | rejects as reference | rejects as reference | not reached | rejects as reference |
| Private methods reject external function-value access | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic module methods remain unsupported by the reference | rejects as reference | rejects as reference | not reached | rejects as reference |
| Imported module aliases preserve method and record identity | accepts | accepts | matches reference | matches reference |
| Constant inference nil | rejects as reference | rejects as reference | not reached | rejects as reference |
| Constant inference array | rejects valid input | rejects valid input | not reached | rejects valid input |
| Constant inference hash | rejects valid input | rejects valid input | not reached | rejects valid input |
| Constant record bindings reject field mutation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Constant record projection rejects Array mutation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Keyword Symbol constant uses ordinary String semantics | accepts | accepts | matches reference | matches reference |
| Float and Boolean conversion, special values and rounding boundaries | accepts | accepts | matches reference | output differs |
| Scalar String conversion across callbacks, retained values and optional calls | accepts | accepts | matches reference | output differs |
| Nullable Float and Boolean conversion preserves absence and values | accepts | accepts | matches reference | matches reference |
| Conversion and Float puts evaluate receivers once in authored order | accepts | accepts | matches reference | matches reference |
| Converted constants retain exact strings across module identity and callbacks | accepts | accepts | matches reference | matches reference |
| Float to_s rejects unexpected arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Boolean to_s rejects unexpected arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Scalar String results cannot initialize a numeric binding | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union scalar cases | accepts | accepts | matches reference | matches reference |
| Union numeric normalization | accepts | accepts | matches reference | matches reference |
| Union inferred array | accepts | accepts | matches reference | matches reference |
| Union inferred hash | accepts | accepts | matches reference | output differs |
| Union contextual array | accepts | accepts | matches reference | matches reference |
| Union widen | accepts | accepts | matches reference | matches reference |
| Union retained mutation | accepts | accepts | matches reference | output differs |
| Union optional | accepts | accepts | matches reference | matches reference |
| Union grouped optional | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union optional widen | accepts | accepts | matches reference | matches reference |
| Union record field | accepts | accepts | matches reference | matches reference |
| Union generic record | accepts | accepts | matches reference | matches reference |
| Union generic function | accepts | accepts | matches reference | matches reference |
| Union generic alias | accepts | accepts | matches reference | matches reference |
| Union closure capture | accepts | accepts | matches reference | output differs |
| Union callable argument | accepts | accepts | matches reference | matches reference |
| Union enum payload | accepts | accepts | matches reference | matches reference |
| Union pass composite | accepts | accepts | matches reference | matches reference |
| Union nullable alternative | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union imported alias | accepts | accepts | matches reference | matches reference |
| Union else discard | accepts | accepts | matches reference | matches reference |
| Union case value | accepts | accepts | matches reference | matches reference |
| Union direct operator reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union direct method reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union narrowing reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union incompatible reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union duplicate pattern reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union incomplete pattern reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union foreign pattern reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union pattern arity reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union composite pattern reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union array readonly reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union boundary mixed numeric array | accepts | accepts | matches reference | matches reference |
| Union boundary default | accepts | accepts | matches reference | matches reference |
| Union boundary lazy optional | accepts | accepts | matches reference | matches reference |
| Union boundary result | accepts | accepts | matches reference | matches reference |
| Union boundary lambda patterns | accepts | accepts | matches reference | matches reference |
| Union boundary returned pattern capture | accepts | accepts | matches reference | matches reference |
| Union boundary shadow pattern | accepts | accepts | matches reference | matches reference |
| Union boundary array nil inference | accepts | accepts | matches reference | matches reference |
| Union boundary array only nil | accepts | accepts | matches reference | matches reference |
| Union boundary hash nil inference | accepts | accepts | matches reference | output differs |
| Union boundary optional array inference | accepts | accepts | matches reference | matches reference |
| Union boundary nullable scalar into union | accepts | accepts | matches reference | matches reference |
| Union boundary nullable union same payload | accepts | accepts | matches reference | matches reference |
| Union boundary generic nested union | accepts | accepts | matches reference | matches reference |
| Union boundary generic collapsed | accepts | accepts | matches reference | matches reference |
| Union boundary alias pattern reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union boundary named pattern reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union boundary discard read reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union boundary binding escape reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union boundary wrong return reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union boundary invariant array reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject runtime function calls as scalar case patterns | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nullable scalar conversion into a numeric union preserves absence | accepts | accepts | matches reference | matches reference |
| Imported inferred constants retain instantiated record types | accepts | accepts | matches reference | matches reference |
| Imported inferred constants retain callable result types | accepts | accepts | matches reference | matches reference |
| Reject authored internal Nil annotation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject authored internal Nil alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject authored internal Nil parameter | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject authored internal Nil lambda | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject authored internal Nil import | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum string roundtrip | accepts | accepts | matches reference | matches reference |
| Raw enum string failure | accepts | accepts | matches reference | matches reference |
| Raw enum integer roundtrip | accepts | accepts | matches reference | matches reference |
| Raw enum integer failure | accepts | accepts | matches reference | matches reference |
| Raw enum empty zero utf8 | accepts | accepts | matches reference | matches reference |
| Raw enum nested module | accepts | accepts | matches reference | output differs |
| Raw enum import alias | accepts | accepts | matches reference | output differs |
| Raw enum module import alias | accepts | accepts | matches reference | output differs |
| Raw enum array hash | accepts | accepts | matches reference | output differs |
| Raw enum nullable | accepts | accepts | matches reference | matches reference |
| Raw enum evaluation order | accepts | accepts | matches reference | output differs |
| Raw enum result return | accepts | accepts | matches reference | matches reference |
| Raw enum result try | accepts | accepts | matches reference | matches reference |
| Raw enum result catch | accepts | accepts | matches reference | matches reference |
| Raw enum ordinary method defaults | accepts | accepts | matches reference | matches reference |
| Raw enum payload method closure | accepts | accepts | matches reference | matches reference |
| Raw enum method argument order | accepts | accepts | matches reference | matches reference |
| Raw enum method private internal | accepts | accepts | matches reference | matches reference |
| Raw enum method receiver once | accepts | accepts | matches reference | matches reference |
| Raw enum method return callable | accepts | accepts | matches reference | matches reference |
| Raw enum type alias static | accepts | accepts | matches reference | matches reference |
| Raw enum generic method | accepts | accepts | matches reference | matches reference |
| Raw enum mixed members reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum mixed types reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum duplicate string reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum duplicate integer reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum duplicate zero reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum computed string reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum interpolated string reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum computed integer reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum float reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum boolean reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum nil reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum unary plus reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum large reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum payload reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum payload raw reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum generic raw reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum reserved raw method reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum reserved from method reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum class method reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum variant after method reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum method private external reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum method immutable self reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum method wrong argument reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum from wrong type reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum from missing reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum from extra reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum from named reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum raw extra reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum implicit conversion reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum plain raw reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum plain from reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum instance from reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum static raw reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Raw enum dot variant reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nested imported raw enum alias chain | accepts | accepts | matches reference | matches reference |
| Safe enum method calls skip nil arguments | accepts | accepts | matches reference | matches reference |
| Raw enum error uses canonical record identity | accepts | accepts; reference rejects | differs | matches reference |
| Retain an implicit enum method receiver in a closure | accepts | accepts | matches reference | matches reference |
| Distinguish ordinary enum methods from collection blocks | accepts | accepts | matches reference | matches reference |
| Generic enum method two types | accepts | accepts | matches reference | matches reference |
| Generic enum method explicit self | accepts | accepts | matches reference | matches reference |
| Generic enum method implicit self | accepts | accepts | matches reference | matches reference |
| Generic enum method closure self | accepts | accepts | matches reference | matches reference |
| Generic enum method closure explicit | accepts | accepts | matches reference | matches reference |
| Generic enum method default named | accepts | accepts | matches reference | matches reference |
| Generic enum method recursive | accepts | accepts | matches reference | matches reference |
| Generic enum method returned enum | accepts | accepts | matches reference | matches reference |
| Generic enum method nested generic | accepts | accepts | matches reference | matches reference |
| Generic enum method nullable | accepts | accepts | matches reference | matches reference |
| Generic enum method array payload | accepts | accepts | matches reference | matches reference |
| Generic enum method import alias | accepts | accepts | matches reference | matches reference |
| Generic enum method alias target | accepts | accepts | matches reference | matches reference |
| Generic enum method namespace | accepts | accepts | matches reference | matches reference |
| Generic enum method private internal | accepts | accepts | matches reference | matches reference |
| Generic enum method private external reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method unused body reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method unused operator reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method unused return reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method concrete template reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method wrong argument reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method missing argument reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method extra argument reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method immutable self reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method payloadless reserved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method duplicate reject | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic enum method through transparent alias chains | accepts | accepts | matches reference | matches reference |
| Generic enum method through an imported nested alias | accepts | accepts | matches reference | matches reference |
| Generic enum alias method skips absent receiver arguments | accepts | accepts | matches reference | matches reference |
| Array ordering: integer order | accepts | accepts | matches reference | matches reference |
| Array ordering: empty single | accepts | accepts | matches reference | matches reference |
| Array ordering: integer limits | accepts | accepts | matches reference | matches reference |
| Array ordering: unicode prefix nul | accepts | accepts | matches reference | output differs |
| Array ordering: invalid bytes | accepts | accepts | matches reference | matches reference |
| Array ordering: float specials | accepts | accepts | matches reference | output differs |
| Array ordering: independent copy | accepts | accepts | matches reference | matches reference |
| Array ordering: single evaluation | accepts | accepts | matches reference | matches reference |
| Array ordering: optional | accepts | accepts | matches reference | matches reference |
| Array ordering: aliases | accepts | accepts | matches reference | matches reference |
| Array ordering: captured copy | accepts | accepts | matches reference | matches reference |
| Array ordering: retained | accepts | accepts | matches reference | matches reference |
| Array ordering: reject boolean | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject nullable element | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject record | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject enum | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject nested array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject callable | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Array ordering: reject extra argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject descending extra | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject string operator | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject nullable receiver | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array ordering: reject immutable output | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: integer keys | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: empty single | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: numeric live | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: managed narrowed | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: unicode keys | accepts | accepts | matches reference | output differs |
| Array keyed ordering: nullable values | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: union values | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: boolean values | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: nested alias copy | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: receiver once | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: nested blocks | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: closure key | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: callable values | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: aliases | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: immutable receiver | accepts | accepts | matches reference | matches reference |
| Array keyed ordering: key panic | accepts | accepts | matches reference | rejects as reference |
| Array keyed ordering: reject boolean key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject array key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject nil key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject nullable key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject mixed key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject range | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject hash | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject extra argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject named argument | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject with index | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject two parameters | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject return | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject break | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject next | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: reject immutable output | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array keyed ordering: absent safe receiver | accepts | accepts | matches reference | matches reference |
| Safe collection iteration | accepts | accepts | matches reference | matches reference |
| Safe collection transforms | accepts | accepts | matches reference | matches reference |
| Safe collection managed | accepts | accepts | matches reference | output differs |
| Collection capture identities | accepts | accepts | matches reference | matches reference |
| Safe block map | accepts | accepts | matches reference | matches reference |
| Safe block indexed map | accepts | accepts | matches reference | matches reference |
| Safe block select | accepts | accepts | matches reference | matches reference |
| Safe block indexed select | accepts | accepts | matches reference | matches reference |
| Safe block reduce | accepts | accepts | matches reference | matches reference |
| Safe block any | accepts | accepts | matches reference | matches reference |
| Safe block all | accepts | accepts | matches reference | matches reference |
| Safe block none | accepts | accepts | matches reference | matches reference |
| Safe block find | accepts | accepts | matches reference | matches reference |
| Safe block find index | accepts | accepts | matches reference | matches reference |
| Safe block sort by | accepts | accepts | matches reference | matches reference |
| Safe block sort by descending | accepts | accepts | matches reference | matches reference |
| Safe block receiver and initial order | accepts | accepts | matches reference | matches reference |
| Safe block retains live array | accepts | accepts | matches reference | matches reference |
| Safe block nested range | accepts | accepts | matches reference | matches reference |
| Safe block nullable container literals | accepts | accepts | matches reference | matches reference |
| Safe block value call chaining | accepts | accepts | matches reference | matches reference |
| Safe block generic | accepts | accepts | matches reference | matches reference |
| Safe block invalid ordinary nullable each | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid ordinary nullable map | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid unsafe result | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid safe index modifier | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid safe map index modifier | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid return from map | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid break from map | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid next from select | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid invalid key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid wrong receiver | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid nullable predicate | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid hash transform | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe block invalid readonly receiver | rejects as reference | rejects as reference | not reached | rejects as reference |
| Array batches | accepts | accepts | matches reference | matches reference |
| Range batches | accepts | accepts | matches reference | matches reference |
| Range streaming | accepts | accepts | matches reference | matches reference |
| Live full batch | accepts | accepts | matches reference | matches reference |
| Exhausted partial batch | accepts | accepts | matches reference | matches reference |
| Requested size preserved | accepts | accepts | matches reference | matches reference |
| Retained source and size | accepts | accepts | matches reference | matches reference |
| Shrink source | accepts | accepts | matches reference | matches reference |
| Receiver size order | accepts | accepts | matches reference | matches reference |
| Argument mutates source | accepts | accepts | matches reference | matches reference |
| Empty evaluates size | accepts | accepts | matches reference | matches reference |
| Safe optional | accepts | accepts | matches reference | matches reference |
| Safe absent runtime size | accepts | accepts | matches reference | matches reference |
| Transfers | accepts | accepts | matches reference | matches reference |
| Nested loops | accepts | accepts | matches reference | matches reference |
| Fresh batches | accepts | accepts | matches reference | matches reference |
| Managed shallow | accepts | accepts | matches reference | matches reference |
| Readonly fresh batch | accepts | accepts | matches reference | matches reference |
| Nullable elements | accepts | accepts | matches reference | matches reference |
| Generic batches | accepts | accepts | matches reference | matches reference |
| Captures | accepts | accepts | matches reference | matches reference |
| Literal zero | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal paren zero | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal zero padded | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal negative | accepts | accepts | matches reference | rejects as reference |
| Literal negative zero | accepts | accepts | matches reference | rejects as reference |
| Literal positive zero | accepts | accepts | matches reference | rejects as reference |
| Dynamic zero array | accepts | accepts | matches reference | rejects as reference |
| Dynamic zero empty range | accepts | accepts | matches reference | rejects as reference |
| Never size | accepts | accepts | matches reference | matches reference |
| Invalid wrong size | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid float size | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid missing size | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid empty args | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid extra arg | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid named arg | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid wrong arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid indexed arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid duplicate params | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid hash | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid ordinary optional | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid safe index modifier | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid readonly source | rejects as reference | rejects as reference | not reached | rejects as reference |
| Unary plus | accepts | accepts | matches reference | matches reference |
| Trailing comma | accepts | accepts | matches reference | matches reference |
| Multiline size | accepts | accepts | matches reference | matches reference |
| Invalid unreachable body | rejects as reference | rejects as reference | not reached | rejects as reference |
| Safe never size | accepts | accepts | matches reference | matches reference |
| Bang callables | accepts | accepts | matches reference | matches reference |
| Bang function value | accepts | accepts | matches reference | matches reference |
| Suffix symbols | accepts | accepts | matches reference | matches reference |
| Uppercase nullable | accepts | accepts | matches reference | matches reference |
| Suffix import | accepts | accepts | matches reference | matches reference |
| Invalid double suffix | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid upper callable | rejects as reference | rejects as reference | not reached | rejects as reference |
| Adjacent bang and equality token boundary in the pinned reference | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid binding alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid parameter alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid binding newtype | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid parameter newtype | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid binding __trb_saved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid parameter __trb_saved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Extended operator symbols | accepts | accepts | matches reference | matches reference |
| Bang enum method | accepts | accepts | matches reference | matches reference |
| Nested optional angles | accepts | accepts | matches reference | matches reference |
| Reserved symbol labels | accepts | accepts | matches reference | output differs |
| Ordinary not equal | accepts | accepts | matches reference | matches reference |
| Bang captured value | accepts | accepts | matches reference | matches reference |
| Invalid field alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid function alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid block alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid label alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid field newtype | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid function newtype | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid block newtype | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid label newtype | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid field __trb_saved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid function __trb_saved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid block __trb_saved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid label __trb_saved | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid operator whitespace | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid bare reserved value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Generic closer origins | accepts | accepts | matches reference | matches reference |
| Invalid angle surplus | rejects as reference | rejects as reference | not reached | rejects as reference |
| Reject a question suffix on an uppercase call name | rejects as reference | rejects as reference | not reached | rejects as reference |
| Scalar identities | accepts | accepts | matches reference | matches reference |
| Nominal equality | accepts | accepts | matches reference | matches reference |
| Nested identities | accepts | accepts | matches reference | matches reference |
| Float abi | accepts | accepts | matches reference | output differs |
| Managed containers | accepts | accepts | matches reference | output differs |
| Optional | accepts | accepts | matches reference | matches reference |
| Nullable float | accepts | accepts | matches reference | matches reference |
| Callable captures | accepts | accepts | matches reference | matches reference |
| Managed captures | accepts | accepts | matches reference | matches reference |
| Instance methods | accepts | accepts | matches reference | matches reference |
| Closed factory | accepts | accepts | matches reference | matches reference |
| Closed lambda | accepts | accepts | matches reference | matches reference |
| Implicit methods | accepts | accepts | matches reference | matches reference |
| Captured self | accepts | accepts | matches reference | matches reference |
| Safe lazy call | accepts | accepts | matches reference | matches reference |
| Generic container | accepts | accepts | matches reference | matches reference |
| Representation array | accepts | accepts | matches reference | matches reference |
| Representation callable | accepts | accepts | matches reference | matches reference |
| Representation union | accepts | accepts | matches reference | matches reference |
| Enum representation | accepts | accepts | matches reference | matches reference |
| Record representation | accepts | accepts | matches reference | matches reference |
| Closed record | accepts | accepts | matches reference | matches reference |
| Namespace | accepts | accepts | matches reference | matches reference |
| Import alias | accepts | accepts | matches reference | matches reference |
| Transparent alias | accepts | accepts | matches reference | matches reference |
| Default argument | accepts | accepts | matches reference | matches reference |
| Constant | accepts | accepts | matches reference | matches reference |
| Raw newtype constructors reject named arguments | rejects as reference | rejects as reference | not reached | rejects as reference |
| Newtype class and instance methods cannot share a name | rejects as reference | rejects as reference | not reached | rejects as reference |
| Private method | accepts | accepts | matches reference | matches reference |
| Closed optional factory | accepts | accepts | matches reference | matches reference |
| Invalid implicit assignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid different nominal | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid representation assignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid wrong constructor | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid wrong arity | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid arithmetic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid ordering | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid representation equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid mutable equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid forwarding | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed external | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed import alias | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Invalid private external | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid instance via type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid class via instance | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid nullable representation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid nil representation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid generic declaration | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid any representation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid void representation | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid bare array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid bare hash | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid cycle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid container cycle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed nested array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed callable | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid late directive | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid duplicate directive | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid reserved new | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid reserved value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid reserved initialize | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid body code | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid duplicate declaration | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid record collision | rejects as reference | rejects as reference | not reached | rejects as reference |
| Float widening | accepts | accepts | matches reference | matches reference |
| Union mutation | accepts | accepts | matches reference | matches reference |
| Mutable representation | accepts | accepts | matches reference | matches reference |
| Closed union | accepts | accepts | matches reference | matches reference |
| Closed enum | accepts | accepts | matches reference | matches reference |
| Unused newtype declaration with a builtin name | accepts | accepts | matches reference | matches reference |
| Unused newtype declaration with a builtin name | accepts | accepts | matches reference | matches reference |
| Invalid hash cycle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid callable cycle | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed union array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Invalid closed enum array | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nominal values remain invalid Hash keys | rejects as reference | rejects as reference | not reached | rejects as reference |
| Union output remains a builtin gap | rejects valid input | rejects valid input | not reached | rejects valid input |
| Literal types: scalar | accepts | accepts | matches reference | matches reference |
| Literal types: negative | accepts | accepts | matches reference | matches reference |
| Literal types: zero | accepts | accepts | matches reference | matches reference |
| Literal types: grouping | accepts | accepts | matches reference | matches reference |
| Literal types: spelling | accepts | accepts | matches reference | matches reference |
| Literal types: operators | accepts | accepts | matches reference | matches reference |
| Literal types: widening | accepts | accepts | matches reference | matches reference |
| Literal types: subsumption | accepts | accepts | matches reference | matches reference |
| Literal types: union injection | accepts | accepts | matches reference | output differs |
| Literal types: union widen | accepts | accepts | matches reference | matches reference |
| Literal types: union case | accepts | accepts | matches reference | matches reference |
| Literal types: case alternatives | accepts | accepts | matches reference | matches reference |
| Literal types: array context | accepts | accepts | matches reference | matches reference |
| Literal types: hash context | accepts | accepts | matches reference | output differs |
| Literal types: alias | accepts | accepts | matches reference | matches reference |
| Literal types: record | accepts | accepts | matches reference | matches reference |
| Literal types: return | accepts | accepts | matches reference | matches reference |
| Literal types: default | accepts | accepts | matches reference | matches reference |
| Literal types: callable | accepts | accepts | matches reference | matches reference |
| Literal types: generic | accepts | accepts | matches reference | matches reference |
| Literal types: newtype | accepts | accepts | matches reference | matches reference |
| Literal types: unicode | accepts | accepts | matches reference | output differs |
| Literal types: invalid wrong integer | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid wrong string | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid inferred scalar | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid computed integer | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid computed string | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid unary plus | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid nullable modifier | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid float type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid boolean type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid wrong return | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid missing union case | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid outside union case | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid duplicate case | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: common field | accepts | accepts | matches reference | matches reference |
| Literal types: discriminated case | accepts | accepts | matches reference | matches reference |
| Literal types: scalar case | accepts | accepts | matches reference | matches reference |
| Literal types: string union operators | accepts | accepts | matches reference | matches reference |
| Literal types: integer union operators | accepts | accepts | matches reference | matches reference |
| Literal types: escaped delimiters | accepts | accepts | matches reference | matches reference |
| Literal types: escaped spelling | accepts | accepts | matches reference | matches reference |
| Literal types: generic record | accepts | accepts | matches reference | matches reference |
| Literal types: enum payload | accepts | accepts | matches reference | matches reference |
| Literal types: closed newtype | accepts | accepts | matches reference | matches reference |
| Literal types: newtype equality | accepts | accepts | matches reference | matches reference |
| Literal types: string output | accepts | accepts | matches reference | matches reference |
| Literal types: collection assignment | accepts | accepts | matches reference | output differs |
| Literal types: union else | accepts | accepts | matches reference | matches reference |
| Literal types: union parenthesized | accepts | accepts | matches reference | matches reference |
| Literal types: union overlap | accepts | accepts | matches reference | matches reference |
| Literal types: union import | accepts | accepts | matches reference | matches reference |
| Literal types: common numeric field | accepts | accepts | matches reference | output differs |
| Literal types: invalid union missing field | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid union replaced narrowing | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid overlap wrong field | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid mixed selector | accepts | accepts | matches reference | output differs |
| Literal types: invalid wrong array value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid wrong hash value | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid wrong reassignment | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid wrong generic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid computed generic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid too large type | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid interpolated string | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: invalid duplicate escaped case | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: boundary literal hash key | accepts | accepts | matches reference | output differs |
| Literal types: boundary literal index | accepts | accepts | matches reference | matches reference |
| Literal types: boundary literal natural sort | accepts | accepts | matches reference | matches reference |
| Literal types: boundary literal sort key | accepts | accepts | matches reference | matches reference |
| Literal types: boundary literal search | accepts | accepts | matches reference | matches reference |
| Literal types: boundary literal join | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: boundary literal call argument | accepts | accepts | matches reference | matches reference |
| Literal types: boundary alias optional | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: mixed zero tags | accepts | accepts | matches reference | matches reference |
| Literal types: string sort | accepts | accepts | matches reference | matches reference |
| Literal types: key snapshot | accepts | accepts | matches reference | matches reference |
| Literal types: union hash key | accepts | accepts | matches reference | output differs |
| Literal types: invalid hash bare index | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Literal types: invalid hash bare construction | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal types: optional union literal | accepts | accepts | matches reference | matches reference |
| Literal types: optional singleton binding | accepts | accepts | matches reference | matches reference |
| Literal types: optional literal array | accepts | accepts | matches reference | matches reference |
| Literal types: union float widen | accepts | accepts | matches reference | matches reference |
| Literal types: nullable union float widen | accepts | accepts | matches reference | matches reference |
| Literal types: invalid nullable literal arithmetic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal union Hash keys: string | accepts | accepts | matches reference | matches reference |
| Literal union Hash keys: integer | accepts | accepts | matches reference | matches reference |
| Literal union Hash keys: computed identity | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: methods | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: bare key method | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: bare key index | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Literal union Hash keys: keys | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: iteration | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: copy merge | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: nullable | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: unicode nul | accepts | accepts | matches reference | output differs |
| Literal union Hash keys: wrong domain | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Literal union Hash keys: mixed key | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Literal union Hash keys: optional key | rejects as reference | rejects as reference | not reached | rejects as reference |
| Literal union Hash keys: optional refined | accepts | accepts | matches reference | matches reference |
| Top-level bindings: scalars | accepts | accepts | matches reference | matches reference |
| Top-level bindings: mutable | accepts | accepts | matches reference | matches reference |
| Top-level bindings: managed replacement | accepts | accepts | matches reference | matches reference |
| Top-level bindings: collection mutation | accepts | accepts | matches reference | matches reference |
| Top-level bindings: collection rebinding | accepts | accepts | matches reference | matches reference |
| Top-level bindings: closure shadowing | accepts | accepts | matches reference | matches reference |
| Top-level bindings: closure writing | accepts | accepts | matches reference | matches reference |
| Top-level bindings: callback | accepts | accepts | matches reference | matches reference |
| Top-level bindings: defaults | accepts | accepts | matches reference | matches reference |
| Top-level bindings: nullable replace | accepts | accepts | matches reference | output differs |
| Top-level bindings: nullable compound | rejects as reference | rejects as reference | not reached | rejects as reference |
| Top-level bindings: nullable call | rejects as reference | rejects as reference | not reached | rejects as reference |
| Top-level bindings: nullable fresh guard | accepts | accepts | matches reference | matches reference |
| Top-level bindings: module identity | accepts | accepts | matches reference | matches reference |
| Top-level bindings: immutable | rejects as reference | rejects as reference | not reached | rejects as reference |
| Top-level bindings: readonly alias | rejects as reference | rejects as reference | not reached | rejects as reference |
| Top-level bindings: private import | rejects as reference | rejects as reference | not reached | diagnostic/output differs |
| Top-level bindings: duplicate | rejects as reference | rejects as reference | not reached | rejects as reference |
| Top-level bindings: blank | rejects as reference | rejects as reference | not reached | rejects as reference |
| Top-level bindings: mutable constant | rejects as reference | rejects as reference | not reached | rejects as reference |
| Lexical globals: function shadow | accepts | accepts | matches reference | output differs |
| Lexical globals: binding before function | accepts | accepts | matches reference | matches reference |
| Lexical globals: function self initializer | accepts | accepts | matches reference | matches reference |
| Lexical globals: generic lexical | accepts | accepts | matches reference | output differs |
| Lexical globals: default lexical | accepts | accepts | matches reference | output differs |
| Lexical globals: lambda lexical | accepts | accepts | matches reference | output differs |
| Lexical globals: mutable function | accepts | accepts | matches reference | matches reference |
| Lexical globals: multiple bindings | accepts | accepts | matches reference | matches reference |
| Lexical globals: invalid forward read | rejects as reference | rejects as reference | not reached | rejects as reference |
| Lexical globals: invalid forward write | rejects as reference | rejects as reference | not reached | rejects as reference |
| Lexical globals: invalid self initializer | rejects as reference | rejects as reference | not reached | rejects as reference |
| Lexical globals: invalid forward generic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Lexical globals: invalid shadowed generic | rejects as reference | rejects as reference | not reached | rejects as reference |
| Optional output: nil | accepts | accepts | matches reference | matches reference |
| Optional output: integer | accepts | accepts | matches reference | matches reference |
| Optional output: float | accepts | accepts | matches reference | matches reference |
| Optional output: boolean | accepts | accepts | matches reference | matches reference |
| Optional output: string | accepts | accepts | matches reference | matches reference |
| Optional output: replaced receiver | accepts | accepts | matches reference | matches reference |
