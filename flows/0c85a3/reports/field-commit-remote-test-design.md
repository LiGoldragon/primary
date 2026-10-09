Qualified design: extend field-clj itself with one typed publish-and-test operation and a narrowly deployed remote execution mode. This is a design/source-ownership handoff only; no implementation or new runtime action is assigned.

CURRENT SOURCE
field-clj currently exposes commit, commit-to and observe. schema.clj owns Malli input/output; core.clj enforces one EDN input and FLOW_ID; commit.clj sequences publication; jj.clj performs commit/bookmark/push; remote.clj handles remote URLs. nix/default.nix and flake.nix package checks. The existing post-failure jj op restore in commit.clj69–75,88–99 can roll back concurrent writers and must not be reused. Existing tests do not prove foreign-index or concurrent-remote preservation.

PROPOSED LOCAL CONTRACT
One tagged request: #publish-and-test [{:message "..." :paths ["relative/path"] :checks ["checks.x86_64-linux.name"]}]. These fields are proposed; existing current-repository/FLOW_ID convention remains. Remote/ref and executor come from the installed typed Field configuration, not arbitrary shell text or a new per-call host flag. Check attributes are exact Nix-packaged derivations, not commands. Use the same safe publication implementation for existing commit/commit-to consumers; remove the broad JJ restore path rather than retaining a parallel unsafe publisher. Resolve commit-to's current mismatch (verification URL can differ from actual push remote) into one typed publication target used for push and verification, updating its consumers.

PUBLICATION
Reserve exact paths through existing Orchestrate coordination, capture immutable bytes/modes/deletions for that write set, and retain their source-base identity. Qualify fresh remote parent; if a selected remote path changed relative to the source base and differs from the intended blob, return a path conflict instead of overwriting it. Build a private GIT_INDEX_FILE tree from that parent; update only literal validated paths, verify exact resulting diff scope, then git commit-tree. Shared index, HEAD, worktree and JJ history are untouched. Push exact commit to the configured ref without force. On concurrent advance return expected/observed revisions and retain candidate; no automatic rebase/restore/force. On ambiguous push, receipt says publication unknown until exact reachability is qualified; no blind replay. Successful publication must be remotely reachable before testing begins.

REMOTE EVALUATION BOUNDARY
Existing nix-ssh@Prometheus is an SSH-NG store/build endpoint, not a general command channel. max-jobs=0, builders, fallback=false and eval-store do not move evaluation. Lojix source7356–7373 and its9406–9427 test explicitly keep it local; do not invoke its BuildOnly/bootstrap as an invented remote executor.
Deploy the SAME field-clj package on Prometheus with an executor-only typed request handler. Expose it through a dedicated restricted SSH forced-command binding configured by Field infrastructure; this is a new supported interface to implement, not a claimed current capability. Do not repurpose nix-ssh or run interpolated remote shell commands. The local client starts only SSH/process IO and lightweight Git/source work; all Nix commands, including metadata resolution, evaluation, realization and packaged-check execution, start inside that Prometheus handler. There is no local evaluator/compiler fallback.

The remote envelope carries an execution ID, canonical source URL, exact pushed commit, expected source tree, lock identity and exact check attributes/system. Handler validates its executor role/system, source allowlist and one typed value, obtains that exact immutable revision using configured remote fetch authentication, checks locked inputs without rewriting lock files, and realizes the specified check derivations with supported Nix build commands. Missing source credentials, unreachable revision, unsupported evaluator setup or dirty/unlocked inputs produce a specific refusal. Credentials stay in existing configured secret plumbing; none enter requests, receipts or store sources. Do not transfer/evaluate the laptop working tree.

For target-specific checks requiring materialized Horizon data, the request must reference exact immutable materialized input artifacts and hashes from the existing owner; absent those, refuse that target. First implementation may cover ordinary flake checks only and explicitly mark Horizon preflight unsupported. It must not improvise a second Horizon evaluator. Successful preflight is not a Lojix deployment receipt.

RECEIPT / FAILURE
Durable local and remote receipt: request ID, requested paths, parent/candidate/published commit, source-tree/lock identities, observed remote reachability, executor identity, check attributes, derivation/output paths, terminal result and bounded log references. Publication and checking have separate states. Push success followed by test failure remains Published + TestFailed; no history undo. A dropped transport after remote admission is TestUnknown with retained execution ID/remote receipt lookup, not a second build. Serialize duplicate execution IDs to avoid duplicate heavy evaluation; this needs only a bounded receipt/lock, not a general job scheduler. No activation/profile changes in this operation.

EXACT OWNERSHIP / SOURCE SCOPE
Field42265e owns publication/implementation/runtime coordination;6aa08d coordinates executor infrastructure. Mind design remains with me/41fa34. In field-clj: schema.clj, core.clj, commit.clj, remote.clj, replace jj.clj publication logic with git.clj; new publish_test.clj and nix_test.clj for orchestration/remote typed handler; corresponding existing test namespaces plus focused new tests, README, nix/default.nix and flake.nix. CriomOS/Home ownership configures the installed Field client target and Prometheus forced-command receiver/key/package; use one new narrowly scoped executor module under the existing owning deployment tree, no incidental host settings embedded in the generic CLI. Install that boundary through supported Lojix deployment, separate from any active job. No Lojix code change is needed for Field preflight; moving Lojix's own evaluator is a separate design, not silently accomplished here.

ACCEPTANCE
Package all tests in Nix and execute their evaluation/build on Prometheus from the committed/pushed candidate: unrelated staged/worktree content preserved; selected-file and remote-ref races refuse; push succeeds/test fails remains published; incorrect execution host refused before Nix; exact revision used despite later remote advances; transport loss reports unknown without duplication; failed remote path starts no local evaluator/Cargo/JVM compiler; genuine remote packaged check passes/fails with logs. Instrument process location, not just builder logs. No tests run in this qualification.

BOUNDARY INCIDENT
Through my read-only subflow I ran jj status and jj log in field-clj despite the intended no-JJ-history boundary. Status said the working copy has no changes; no import warning appeared, but this does not prove no import occurred. No authored edits, cleanup, build/test/SSH or live-runtime operations followed. Further JJ use is stopped. I report this separately rather than claim all repository state was proven unchanged.

STATUS ADDENDUM — 2026-10-09

The design body above is preserved from the sent message. Its retained
transcript is `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/07/rollout-2026-10-07T11-33-38-01a1176d-8dfd-75c2-aea9-b640c85a3316.jsonl`, command record 7284. The recorded hm-send
receipt is `Transported.{ 42265e idle }`; transport acceptance does not prove that the
recipient read the body. Field 42265e subsequently accepted coordination,
as reported to this flow.

Field 6aa08d qualifies the exact Prometheus target, access, write set,
and bootstrap for this design. This report records design only: it
authorizes no receiver installation or implementation. Field's report
records job98 as Succeeded and the protected Codex as unchanged.


RECEIVER DEPLOYMENT CONTRACT

Narrow receiver design inputs (proposed declarative scope; configured deployment values still require6aa qualification):

Use a NEW dedicated account, proposed name field-test, and a new narrowly scoped NixOS module, proposed path CriomOS/modules/nixos/services/field-test-executor.nix. Export typed services.field-test-executor options; import from the existing owning module aggregator only after6aa identifies its actual source path. Default enable=false. Enable only in the qualified Prometheus node module selected by the real deployment owner. Neither node name, target nor Horizon/transport is inferred here; Ouranos98 is not reused. Leave nix.sshServe, nix-ssh and generic builder authorization unchanged.

Required configuration: installed Field executor package; executor identity; supported system; allowed canonical source repositories (and publication refs if restricted); dedicated inbound authorized public keys; writable receipt root; read-only source-fetch credential file/provider reference when required. No permissive defaults for keys, executor identity, source allowlist or deployment target. Missing requirements keep receiver disabled/client refusing. Application parser accepts only remote packaged-check requests with immutable commit/tree/lock identities and allowlisted check selectors; it cannot publish, launch seats or activate profiles.

Inbound authentication: use a dedicated Field-controller keypair. The approved PUBLIC key is supplied to the node configuration from the authenticated caller's owned key inventory; it may be stored as public configuration. The PRIVATE key remains in the caller's existing credential owner/secret installation, exposed to the SSH client through a configured identity/agent, never request/receipt/store. No actual key source has yet been qualified, so do not copy personal keys, reuse nix-ssh keys, generate/enroll a key blindly or infer identity from a hostname. Pin the receiver host key through the owning trusted host-key configuration.

Authorized key uses a forced fixed store-path executor command and restrict-equivalent controls: no PTY, port/agent/X11 forwarding or arbitrary command. Handler reads one bounded typed value on stdin; ignore/refuse SSH_ORIGINAL_COMMAND rather than evaluating it. Account has no sudo/admin/deploy group, password login or interactive access. Do not mark it a Nix trusted-user. Its only intended Nix permission is ordinary access to the configured daemon's build interface; qualify restricted evaluator/fetch options under that unprivileged identity rather than broadening daemon trust if a check refuses.

Filesystem: module creates a0700 account-owned root, proposed /var/lib/field-test, with0700 receipts/work subdirectories. Execution IDs select validated child paths only; durable receipts and bounded logs stay there with0600 mode, no token bytes. Use per-execution locking for deduplication; no global job scheduler. Retain receipt on disconnect/failure. No access to Codex homes, existing Lojix job state or arbitrary writable repository checkout is part of the design.

Remote source fetch is a SEPARATE credential from inbound SSH. Public immutable sources require none. Private source access uses a dedicated read-only repository credential delivered by the existing node secret mechanism to a0700/0600 account-readable runtime location, outside Nix store; configure only its reference in declarative source. The executor injects it into the supported Nix fetch authentication mechanism inside its own process, using the existing Lojix secret-injection pattern only as a source precedent, not borrowing job credentials or changing Lojix. Actual secret name/provider and Nix mechanism must be qualified by6aa; absent it, report SourceAuthenticationUnavailable. Disable trace/environment logging of credential values and do not serialize them in requests/receipts/derivations.

Owning source split: Field CLI worker owns typed handler/client/schema and packaging;6aa qualifies infrastructure write-set/module aggregator/node enablement/public-key owner/host key/secret provider/ordinary Nix access. Field42265e alone authorizes application of that qualified node-specific deployment through the supported route. A generic client can be completed while receiver configuration remains absent, with explicit ExecutorUnconfigured refusal. This addendum supplies design shape, not missing live values or deployment authorization.


MESSAGE PROVENANCE FOR RECEIVER CONTRACT

The retained root transcript at
`/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/07/rollout-2026-10-07T11-33-38-01a1176d-8dfd-75c2-aea9-b640c85a3316.jsonl`,
command record 7354, records the receiver contract send with receipt
`Transported.{ 42265e working }`. Transport acceptance does not prove
that the recipient read the contract.
