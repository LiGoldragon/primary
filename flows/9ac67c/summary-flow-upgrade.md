# Field Sol Flow upgrade activation packet — 2026-09-26

## Authority and ownership

Psyche Fable 8904b1 ruled that Field Sol 9ac67c may own the breaking stable Flow 0.12.2 → 0.14.0 host transition, including the service override, subject to explicit acceptance. Field Sol accepts that ownership here. Field Sol also owns restoration of Prometheus and its access path. Acceptance starts no activation. Mind Astra 6fe957 owns the Home Flow 0.17.4 pin, generation, and source gates. Mind Sol 56ae53 owes documented stable-step deployment and proof on copied Flow and Message stores that target reads stored rows and rollback restores them. Flow imported-seat confirmation remains separate source work. The living's instruction to use the newer Flow was relayed by Mind Sol and accepted by Psyche Fable as an activation order; this flow did not hear it directly. Fable ruled that the order does not itself settle the stable override choice or authorize a switch now.

## Immutable source and Home stage

- Real remote `flow-0.17.4` tag resolves to `bc464e5e1b94fcc179af73111f43b69db1f69fc5`; the previous `flow-0.17.3` resolves to `0b512ee0b6681b1925fee7b6435aa7c2eac26bfb` and is unchanged.
- Observer change accepts Claude's plain direct-form startup only with the durable server prompt hash/footer and direct-form structure, retaining ordered skill, result, and receipt observations. Mind reports focused 7/7 and formatting success; no durable terminal test log was independently recovered.
- Home real-remote main is `5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`. Its declared stable Flow and Message are 0.14.0 lineage; separate next Flow remains older than 0.17.4.
- Remote Home stage `flow-0174-stage-56ae53` resolves to `daf026f1e02bcd092f0ecc43b81207c96c6ec1b3`. It changes only `flake.nix`, `flake.lock`, and the `flow-message-next` fixture, advancing the next Flow pin to 0.17.4 while retaining Messenger `93c12756f9c00dd3c13762590f17cee3a3712530` and Message-next `481b579fcf72797ffa9ccf8ce4e2283a58cdff97`.
- One Prometheus SSH job timed out before full Home generation. No generated candidate Home generation or unit has been witnessed for this stage. No Home main move or activation is claimed.

## Live baseline and red gates

1. Declared managed stable `flow-nexus.service` starts Flow 0.14.0, but an unmanaged user drop-in clears its ExecStart and selects Flow 0.12.2. Current active Flow process was witnessed as 0.12.2. The override's disposition during Home activation is unresolved. Field must decide it explicitly with the living under Fable's ruling.
2. Stable Flow store `~/.local/state/flow/flow.sema` was observed at 1,056,768 bytes and yielded 25 rows by read-only List. Stable Message store `~/.local/state/message/messenger.sema` was observed at 180,224 bytes. Its existing pre-open snapshot differs from the live store; journal evidence shows six service-start refusals caused by the mismatch, followed by manual recovery. Current exact hashes must be recorded afresh in the preactivation receipt.
3. Flow 0.17.4 upgrade notes require paired Message 0.17.0. The running stable Message is 0.14.0; the side-by-side next pair runs on isolated stores. That isolation proves neither stable-store readability nor reversibility. Mind's copied-store proof must cover both stores and the intended transition sequence.
4. Current stable Flow List yielded 25 rows. Target seat census at review: active with Herdr route available for Mind Luna, Field Luna, Field Astra, Psyche Sonnet, Field Sol, Psyche Fable, and Psyche Opus; Mind Astra is Pending with Herdr route available; predecessor Mind Sol is Active with Herdr route available but endpoint unavailable. This is a point-in-time census, not a quiet-window witness. Current Message registry, queue, and parked-delivery census is missing.
5. Prometheus SSH timed out before generation; restored builder and remote-access paths have not been witnessed. Field Sol coordinates access restoration with Mind and is blocked on Prometheus console access requested from the living.

## Required transition sequence, not yet executed

1. Mind Astra completes immutable Home pin/check/generation gates and hands Field a generated-unit and closure receipt. The earlier Flow 0.17.3 stage is superseded and must not be activated.
2. Mind Sol supplies the documented stable-step procedure and proof on copies: the target reads all 25 stored Flow rows, the paired Message state is preserved, and rollback reopens both original stores. Capture current full store hashes, service files, drop-in, old and new store paths, Message registry/ledger counts, and live routes immediately before the switch.
3. Field Sol records the override decision, tells stable seats, confirms a quiet window with no Message queue or parked deliveries, witnesses remote access, and stages exact old and new closures.
4. Before stopping the old pair, arm an automatic countdown rollback to the last working Flow/Message stack. Record its target, timeout, cancellation authority, and witness in the upgrade notes. Cancel only after a witness confirms network connectivity and remote access on the new stack.
5. On successful switch, verify exact new ExecStarts, Flow row count and target routes, Message registry/ledger counts and delivery probe, and remote access. On failure, stop the new pair; restore exact preactivation stores atomically while stopped; restore the prior generated Home profile/unit and ruled override; reload units; start the prior Message then Flow; verify old hashes, rows, routes, and remote access.

## Open decisions

- Override decision for the stable 0.12.2 → 0.14.0 step, placed before the living by Fable because the newer-Flow order does not specify it.
- Prometheus console or other witnessed access path needed to restore generation and prepare the Zeus gate.

No Home activation, service restart, stable-store migration, Prometheus build, or Zeus deployment is claimed in this packet.

## 2026-09-26 copied-pair and interim override addendum

- Mind Sol's committed copied-pair receipt on Primary main records stable Flow and Message source/copy pre/post/final hashes and sizes matching, distinct copy inodes, stable source inode/mtime, both live units active, and a read-only 25-top-level-row Flow List. Flow SHA-256 is `f03f610a9832378ef0f03fee16383266909d923051ccb5a71980cc9db78c0f03` at 1,056,768 bytes; Message SHA-256 is `4cb4e9ba3544a12afcb2d1771bfd67eb93e74d9aa6b898ba6251036061719457` at 180,224 bytes. Receipt revision: `0f71d10636ba1be49ba30983913fa3ce629beb30`. This is a witness of copied rollback inputs, not of target-binary readability, migration, or rollback execution.
- Mind Sol's interim operational disposition is to retain the current stable 0.12.2 override while 0.17.4 is validated through isolated disposable live-Start witnesses. Field Sol records and follows that status-quo hold: no stable service or store access is authorized by it. The later override removal/0.14.0 stable transition decision from Psyche Fable's ruling remains open; the interim hold does not decide it.

## 2026-09-26 exact stable target executable addendum

- A peer report said Flow 0.14.0 was unavailable because profile-resolved `flow`, `flow-nexus`, and `flow-meta` all point to 0.12.2. Direct read-only inspection resolved the narrower fact: the managed generated `flow-nexus.service` names `/nix/store/j689l77bmlfmgc6ichksrqnnmdnma8ig-flow-0.14.0/bin/flow-nexus`, and that exact store closure plus its sibling `flow` and `flow-meta` executables exist locally. The target binary is available by exact path, though not on the profile PATH.
- Message 0.14.0 is profile-exposed. Source inspection supports an explicit binary configuration naming a copied store and scratch sockets; no such isolated configuration or paired target-read test has been executed. Flow 0.14's copied store also preserves absolute socket paths, so an isolated mount namespace remapping both state and socket directories remains required. Do not open Message alone. Target-read, preservation under target, and rollback execution remain RED.

## 2026-09-26 Fable gate separation addendum

Psyche Fable's direct native answer (2026-09-27T04:07:39Z, locally 2026-09-26) separates two activations. Paired target-read of the copied stable Flow/Message stores gates a later activation that changes a stable service version. With the existing override retained, a Flow-next 0.17.4 activation need not open stable stores with the 0.14.0 targets if generated candidate units prove both that stable Flow remains the running 0.12.2 and stable Message remains the running version. A same-version restart does not itself require target-read; a version change restores that gate for the service. Next-Flow activation still requires captured stores, a timed rollback, seat notice and quiet window, live native Start witnesses, completed Home 0.17.4 checks and package build, and Field Sol's acceptance naming the exact generated unit. No candidate generated unit exists yet, so no activation is cleared. The packet's earlier stable target-read sequence applies to the later stable transition, not as a prerequisite for isolated next-Flow activation with both stable versions unchanged.

## 2026-09-26 Flow 0.17.4 source acceptance and independent test

Field Sol accepts immutable Flow source `bc464e5e1b94fcc179af73111f43b69db1f69fc5` for Home pin/build review only. A read-only source review of the real remote tag found the five-file 0.17.3→0.17.4 delta limited in production behavior to Claude direct-form observer handling. That branch requires the persisted prompt body digest and exact footer, direct-form structure, ordered selected Skill calls, correlated successful results, exact source expansions, and matching receipt/model/effort. It does not accept a missing or altered receipt. The release notes require Message 0.17.0 beside the new Flow. No Home unit or activation is accepted by this source verdict.

An independent bounded test on a clean immutable checkout ran the seven focused Claude observer tests with `cargo test --locked -p flow-nexus herdr::launch::tests::claude_`: exit 0, seven passed, zero failed. `cargo fmt --all -- --check` exited 0. The checkout remained clean. No production service/store or Claude/Flow process was started. These terminal results establish the focused source test, not the Home generation or live native Start witness.

Home real remote main was independently resolved at `daf026f1e02bcd092f0ecc43b81207c96c6ec1b3`, a three-file pin/fixture change from `5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`; stable Flow/Message, Messenger, and Message-next pins were retained. Mind Astra reports one bounded no-link activation-package evaluation failed before realization because `horizon.node.machine.hardware` was absent. The terminal error itself was not independently recovered. No candidate generated unit or activation-package output is accepted.
