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
| Nullable String | rejects valid input | rejects valid input | not reached | rejects valid input |
| Ordinary enum | rejects valid input | rejects valid input | not reached | rejects valid input |
| UTF-8 String literal | accepts | accepts | matches reference | matches reference |
| Array of named records | accepts | accepts | matches reference | matches reference |
| Hash literal and required lookup | accepts | accepts | matches reference | matches reference |
| Array each with live growth and index | accepts | accepts | matches reference | matches reference |
| Range each (inclusive / exclusive / reversed) | accepts | accepts | matches reference | matches reference |
| Range with captured endpoint effects (requires fn) | rejects valid input | rejects valid input | not reached | rejects valid input |
| UTF-8 length, indexing, concatenation and interpolation | accepts | accepts | matches reference | matches reference |
| Unicode local identifier | rejects valid input | rejects valid input | not reached | rejects valid input |
| Unicode scalar escapes | rejects valid input | rejects valid input | not reached | rejects valid input |
| String search and code-point APIs | rejects valid input | rejects valid input | not reached | rejects valid input |
| Empty String and ASCII indexing | accepts | accepts | matches reference | matches reference |
| Mixed numeric arithmetic and conversion | rejects valid input | rejects valid input | not reached | rejects valid input |
| Portable Integer endpoints | accepts | accepts | matches reference | matches reference |
| Semicolon and comment separators | accepts | accepts | matches reference | matches reference |
| Recursive calls and all-path returns | accepts | accepts | matches reference | matches reference |
| Mutable parameter rebinding is local | accepts | accepts | matches reference | matches reference |
| Named-only arguments and reordering | accepts | accepts | matches reference | matches reference |
| Default arguments refer to earlier arguments | accepts | accepts | matches reference | matches reference |
| Value-producing if | rejects valid input | rejects valid input | not reached | rejects valid input |
| Conditional expression evaluates one branch | rejects valid input | rejects valid input | not reached | rejects valid input |
| Postfix return and loop transfers | rejects valid input | rejects valid input | not reached | rejects valid input |
| Scalar case and case expression | rejects valid input | rejects valid input | not reached | rejects valid input |
| Record defaults and reordered explicit fields | accepts | accepts | matches reference | matches reference |
| Reject unsupported record equality | rejects as reference | rejects as reference | not reached | rejects as reference |
| Nullable narrowing and early return | rejects valid input | rejects valid input | not reached | rejects valid input |
| Nullable short-circuit and safe member | rejects valid input | rejects valid input | not reached | rejects valid input |
| Nil equality | rejects valid input | rejects valid input | not reached | rejects valid input |
| Payload enum and exhaustive case | rejects valid input | rejects valid input | not reached | rejects valid input |
| Raw-value enum | rejects valid input | rejects valid input | not reached | rejects valid input |
| Transparent type alias | rejects valid input | rejects valid input | not reached | rejects valid input |
| Nominal newtype construction and projection | rejects valid input | rejects valid input | not reached | rejects valid input |
| Parameters following nested generic annotations | accepts | accepts | matches reference | matches reference |
| Generic function application | rejects valid input | rejects valid input | not reached | rejects valid input |
| Generic record | rejects valid input | rejects valid input | not reached | rejects valid input |
| Literal-field union narrowing | rejects valid input | rejects valid input | not reached | rejects valid input |
| Typed function value and lexical capture | rejects valid input | rejects valid input | not reached | rejects valid input |
| Function value mutates captured binding | rejects valid input | rejects valid input | not reached | rejects valid input |
| Array alias and parameter rebinding | accepts | accepts | matches reference | matches reference |
| Array index captured before growing RHS | accepts | accepts | matches reference | matches reference |
| Nested managed Array values | accepts | accepts | matches reference | matches reference |
| Array value-producing iteration | rejects valid input | rejects valid input | not reached | rejects valid input |
| Hash key/value iteration | rejects valid input | rejects valid input | not reached | rejects valid input |
| Empty Hash inference and update | accepts | accepts | matches reference | matches reference |
| Hash deletion, membership and size | accepts | accepts | matches reference | matches reference |
| Stored Range bounds and conversion | rejects valid input | rejects valid input | not reached | rejects valid input |
| Inclusive Range maximum endpoint | accepts | accepts | matches reference | matches reference |
| Result storage and exhaustive case | rejects valid input | rejects valid input | not reached | rejects valid input |
| Result try propagation | rejects valid input | rejects valid input | not reached | rejects valid input |
| Result catch recovery | rejects valid input | rejects valid input | not reached | rejects valid input |
| Class fields, initializer and method | rejects valid input | rejects valid input | not reached | rejects valid input |
| Explicit interface conformance | rejects valid input | rejects valid input | not reached | rejects valid input |
| Module declaration and constant | rejects valid input | rejects valid input | not reached | rejects as reference |
| Top-level constant | rejects valid input | rejects valid input | not reached | rejects valid input |
| Symbol literal equality | rejects valid input | rejects valid input | not reached | rejects valid input |
| Named import alias and reachable file | accepts | accepts | matches reference | matches reference |
| Reject unused local binding | incorrectly accepts | incorrectly accepts | differs | output differs |
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
| Embedded zero and supplementary scalar escapes | rejects valid input | rejects valid input | not reached | rejects valid input |
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
