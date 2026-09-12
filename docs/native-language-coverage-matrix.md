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
| Default argument | rejects | rejects | not reached | rejects |
| Array&lt;Boolean&gt; | accepts | accepts | matches reference | matches reference |
| Nullable String | rejects | rejects | not reached | rejects |
| Ordinary enum | rejects | rejects | not reached | rejects |
| UTF-8 String literal | accepts | rejects | not reached | rejects |
| Array of named records | accepts | accepts | matches reference | matches reference |
| Hash literal and required lookup | accepts | accepts | matches reference | matches reference |
| Array each with live growth and index | accepts | accepts | matches reference | matches reference |
| Range each (inclusive / exclusive / reversed) | accepts | accepts | matches reference | matches reference |
| Range with captured endpoint effects (requires fn) | rejects | rejects | not reached | rejects |
