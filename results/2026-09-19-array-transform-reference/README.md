# Array transform reference integration

Status: validation in progress; this is not an accepted compatibility result.

The exact TypeRB reference is `0.4.8-dev` at
`245ebcba45905037ea8f30d647d0893796441c88`. It includes the sequential live
Array traversal contract from TypeRB PR #729. No release or bootstrap seed is
changed. Historical measurements retain their original reference identities.

The integration starts from Native source
`1c9df940694bab240daa53f5ad6156ac8eab7787`; its prerequisite validation is
https://github.com/type-rb/type-rb-native/actions/runs/35437299015.
That prerequisite run does not validate this reference update or transforms.
Candidate correctness, shared-language and recovery results will be recorded
before acceptance.
