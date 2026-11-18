# Controller source-only test specification

Tests are intentionally unrun. They must execute only in an isolated temporary
fixture environment after independent review; never invoke native/runtime stages.

1. Missing manifest and malformed JSON return 2 and print STOP; no filesystem
   creation, subprocess, service, credential, or network action occurs.
2. The supplied template fails closed on its first pending input.
3. Each missing required key fails with that key named; empty and `PENDING`
   values fail.
4. A different candidate commit fails; malformed provider hash and empty hash
   map fail.
5. A structurally complete synthetic fixture still stops rather than claiming
   admission: executable stages are deliberately unavailable pending review.
6. Static parser/controller suite must later validate typed receipt grammar and
   exact heads, IDs, complete consumption; matrix wrong-kind, duplicate and
   unknown IDs; Order unresolved; Question-to-Result and Task-to-Done routing;
   retained unbound Answer; carried Q2/T2 IDs/deadline and absent O2 marker;
   native read acknowledgement distinct from submission; and closure/cgroup
   evidence. No fixture may emit a production/native PASS.

Admission gaps are concrete: exact package output paths and provider hashes;
source-bound event API; reviewed full prompts; immutable admission and hash
binding. This artifact is an executable fail-closed boundary, not an admitted
runtime controller. No permission follows from source gate results.
