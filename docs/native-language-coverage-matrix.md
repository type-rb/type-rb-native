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
| Mixed numeric arithmetic and conversion | rejects valid input | rejects valid input | not reached | rejects valid input |
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
| Raw-value enum | rejects valid input | rejects valid input | not reached | rejects valid input |
| Transparent type alias | accepts | accepts | matches reference | matches reference |
| Nominal newtype construction and projection | rejects valid input | rejects valid input | not reached | rejects valid input |
| Parameters following nested generic annotations | accepts | accepts | matches reference | matches reference |
| Generic function application | accepts | accepts | matches reference | matches reference |
| Generic record | accepts | accepts | matches reference | matches reference |
| Literal-field union narrowing | rejects valid input | rejects valid input | not reached | rejects valid input |
| Typed function value and lexical capture | accepts | accepts | matches reference | matches reference |
| Function value mutates captured binding | accepts | accepts | matches reference | matches reference |
| Array alias and parameter rebinding | accepts | accepts | matches reference | matches reference |
| Array index captured before growing RHS | accepts | accepts | matches reference | matches reference |
| Nested managed Array values | accepts | accepts | matches reference | matches reference |
| Array value-producing iteration | accepts | accepts | matches reference | matches reference |
| Hash key/value iteration | rejects valid input | rejects valid input | not reached | rejects valid input |
| Empty Hash inference and update | accepts | accepts | matches reference | matches reference |
| Hash deletion, membership and size | accepts | accepts | matches reference | matches reference |
| Stored Range bounds and conversion | rejects valid input | rejects valid input | not reached | rejects valid input |
| Inclusive Range maximum endpoint | accepts | accepts | matches reference | matches reference |
| Result storage and exhaustive case | accepts | accepts | matches reference | matches reference |
| Result try propagation | accepts | accepts | matches reference | matches reference |
| Result catch recovery | accepts | accepts | matches reference | matches reference |
| Class fields, initializer and method | rejects valid input | rejects valid input | not reached | rejects valid input |
| Explicit interface conformance | rejects valid input | rejects valid input | not reached | rejects valid input |
| Module declaration and constant | rejects valid input | rejects valid input | not reached | rejects as reference |
| Top-level constant | rejects valid input | rejects valid input | not reached | rejects valid input |
| Symbol literal equality | rejects valid input | rejects valid input | not reached | rejects valid input |
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
