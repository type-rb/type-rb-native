<!-- Generated from tools/native-language-cases.json; do not edit by hand. -->

| Case | Check | Build | Execute | REPL |
| --- | --- | --- | --- | --- |
| Integer arithmetic | accepts | accepts | matches reference | matches reference |
| if / else | accepts | accepts | matches reference | matches reference |
| while | accepts | accepts | matches reference | output differs |
| Short-circuit OR / AND | accepts | accepts | matches reference | matches reference |
| Record construction and field read | accepts | accepts | matches reference | matches reference |
| Array&lt;Integer&gt; | accepts | accepts | matches reference | matches reference |
| elsif | rejects | rejects | not reached | rejects |
| break | rejects | rejects | not reached | rejects |
| next | rejects | rejects | not reached | rejects |
| Default argument | rejects | rejects | not reached | rejects |
| Array&lt;Boolean&gt; | rejects | rejects | not reached | rejects |
| Nullable String | rejects | rejects | not reached | rejects |
| Ordinary enum | rejects | rejects | not reached | rejects |
| UTF-8 String literal | accepts | rejects | not reached | rejects |
