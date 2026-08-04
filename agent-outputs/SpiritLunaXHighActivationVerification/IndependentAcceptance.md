# Independent Spirit Luna/XHigh activation verification

Date: 2026-08-04, Europe/Madrid

Outcome: **ROLLBACK SIGNALLED — activation not accepted.** This lane made no
runtime, service, profile, Lojix, store, repository, or claim mutation beyond
the narrow evidence-file claim. All observations below are bounded and retain
only non-sensitive predicates, hashes, counts, and immutable revisions.

## Scope and evidence limits

The requested immutable CriomOS revision is
`9b3d344631628cb19dda1a22af4d7ef25c5f8def`. Its lock independently selects
CriomOS-home `3dc0bada3f636065e7fd093711305a153dd5925a` and Spirit
`7405eee89e3b1b5b6764eb1a50cbdf467b93c9a7`. The target Spirit manual identifies
the release as `0.27.0`.

The PRE observation captured Version `0.26.0` and Marker
`(25, 5374348791551424496)`. PRE Count is a deliberate evidence gap: safe
v14 Count requests were rejected by the installed parser before any result was
returned, so this verifier did not guess a query shape or inspect record data.
The initial ordinary profile witness was generation `275`; the Home Manager
profile link was first read during the post-trigger investigation, so it is not
claimed as an exact PRE closure witness.

## Independent PRE baseline

| Witness | Result | Classification |
|---|---|---|
| Lojix node query | Two historical UserEnvironment deployment/generation records (`1/1` and `2/2`) were returned, both labelled `Current`; their immutable CriomOS revisions were `e658bf55…` and `b4639094…`, never the target. Query marker was `(34, 34)`. This is not a unique current-generation witness. | stale / ambiguous |
| Spirit logical state | Version `0.26.0`; Marker `(25, 5374348791551424496)`; Count unavailable as described above. | wired except Count gap |
| Services and dependency | Judge and daemon were active/running/success with main status zero. Daemon `Requires` and starts `After` judge. | wired |
| Channels | Exactly three Spirit Unix listeners were live. | wired |
| Kernel provider predicates | Judge process: OpenAiCodex true, Terra true, Medium true, Luna false, XHigh false. Executable and argv identities were retained as SHA-256 witnesses only. | wired, old selection |

## Post-trigger independent result

The executor's `Current` announcement was treated only as the trigger. It is
not corroborated by any required durable witness.

1. Read-only Lojix query on the actual node `goldragon/ouranos` still returns
   only the two earlier records above, with no target revision. It therefore
   cannot identify a target deployment/generation/closure as Current.
2. The system Lojix daemon is active/running/success, but its same-day journal
   contains zero occurrences of the target immutable revision. It contains one
   `DeployAccepted` event that cannot be correlated to the target or the stated
   rollback revision from any durable revision or admission-handle witness.
3. The active Home Manager link is generation `957`, timestamped during this
   incident, but its realised closure contains Spirit `0.26.0`, not `0.27.0`.
   The ordinary profile remains `275`; this is a separate profile channel and
   cannot prove Home activation.
4. Live Spirit Version remains `0.26.0` and Marker remains the PRE marker.
   This alone fails the target release acceptance requirement.
5. Judge and daemon remain active/running/success with required ordering, and
   exactly three listeners remain live. These health facts do not establish the
   requested deployment.
6. Post kernel predicates remain OpenAiCodex true, Terra true, Medium true,
   Luna false, XHigh false. Maintained daemon/judge wrapper provenance remains
   present, but its SHA-256 identities are the old runtime identities. Thus the
   required Luna=true, Terra=false, XHigh=true, Medium=false witness fails.

`ROLLBACK` was immediately sent to `/root/map_dilemma` and `/root` for the
missing target Lojix provenance and again for Version `0.26.0`. The verifier did
not execute rollback.

## Engine finding

The executor report is an assertion, not a deployment receipt. It describes a
target owner Deploy and a later rollback-shaped request, but preserves neither
an exact typed admission handle nor a poll sequence correlated to it. It also
records no direct Home Manager or system activation. Direct evidence shows no
target revision in either the Lojix read model or daemon journal, while the
active Home closure is already `0.26.0`.

Supported conclusion: the target deployment is **not durably admitted and
Current**. The evidence cannot distinguish a request that was never admitted
from an uncorrelated transient client response. A completed target activation
followed by a fully durable rollback is also not proved: there is no target
journal event, target profile closure, `0.27.0` runtime, or Luna/XHigh runtime
witness. Claims of a transient local target process are therefore
contract-only, not wired.

## Public CLI and documentation witnesses

Both currently installed public CLIs were tested only with non-body requests.
Each accepted exactly one canonical selector object: ordinary `Version` and
owner `ObserveHead`. Each rejected `--help`, a representative flag, a path
operand, and two operands. The target manual defines a bare selector such as
`Version` as an object, rather than positional shorthand; adding a second
positional operand is rejected. Therefore a requirement to reject bare
`Version` itself would conflict with the deployed-origin object grammar.

The exact target-origin README/manual/architecture were inspected by immutable
revision and safe content hashes. Their examples use the five-predicate Count
schema and their guide says one object only, no flags/help/path operands. The
guide explicitly retires core certainty, privacy, referent, relation, and
old-operation claims. Its operational-confidentiality language is qualified as
outside the core model and is not stale privacy semantics. The target docs are
**contract-only** because the target is not active. The installed `0.26.0` CLI
object-only behaviour is **wired**, but cannot prove `0.27.0` schema/runtime.

The active Spirit source checkout's README, manual, and architecture documents
do not content-match the target-origin versions and are **stale**. They still
describe certainty/privacy/referent storage, eight-field queries, referent
registration, and retired operations including certainty/privacy change and
removal collection as active. This is a documentation fix blocker for a clean
retry/acceptance record. It is not the cause of the runtime failure, whose
independent deployment and version witnesses already fail.

## Rollback-safe retry acceptance procedure

The installed ordinary client and owner client/daemon are all Lojix `0.11.0`,
the same version declared by the Lojix revision selected by the target lock.
This is not a protocol or daemon repair prerequisite. The public owner CLI is,
however, intentionally a one-shot adapter: it prints one typed reply and exits
(`lojix/src/bin/meta-lojix.rs:1-21`; `lojix/src/client.rs:125-155`). It does not
persist a handle, correlate a journal event, or poll. A small audited operator
wrapper or manual ledger is therefore required before another live submission;
it is evidence tooling, not a substitute deployment mechanism.

1. Preserve the currently healthy `0.26.0` state; do not use direct Home
   Manager/NixOS activation to compensate for a missing Lojix receipt.
2. Construct exactly one owner-channel UserEnvironment Deploy for
   `goldragon/ouranos/li`, the approved immutable CriomOS revision
   `9b3d344631628cb19dda1a22af4d7ef25c5f8def`, `ActivateNow`, and
   `RequireImmutable`. The locked implementation selects the user activation
   package for this action (`lojix/src/schema_runtime.rs:954-965`) and
   `ActivateNow` sets the user profile then runs its activation package
   (`4429-4510`). Do not issue the rollback request in the same attempt.
3. Capture the complete immediate typed reply in a restricted operator ledger,
   parse it as either `DeployAccepted(handle)` or `DeployRejected(reason)`, and
   retain only the accepted deployment identifier and database marker in shared
   evidence. The source is explicit that the reply is an admission handle before
   effects run (`lojix/src/daemon.rs:340-374`); substring matching is invalid.
   A typed rejection is an immediate stop condition.
4. Start a bounded poll deadline after an accepted handle. Reissue the ordinary
   read-only node query and require a single generation row matching **all** of:
   the accepted deployment identifier, target source revision, UserEnvironment,
   LiveActivation, and Current. This is the correct durable read-model shape:
   the projection contains identifier, source revision, activation effect, and
   slot (`lojix/src/schema_runtime.rs:3160-3201`). Historical rows may also say
   Current, so revision or slot alone is insufficient.
5. In parallel, correlate the system Lojix daemon's terminal pipeline entry to
   the accepted identifier and marker. The actor logs its terminal output after
   driving the submitted deploy (`lojix/src/daemon.rs:580-585`); the pipeline
   persists every stage through activation-recording before terminal success
   (`lojix/src/schema_runtime.rs:876-892`, `1749-1757`, `2438-2464`). Absence of
   either correlation at deadline, a terminal rejection, a different identifier,
   or an unchanged read-model is a failed activation. Stop and preserve the
   evidence; do not directly activate and do not infer success from a process
   that appeared transiently.
6. Only after both correlations, independently prove the active Home profile
   closure contains Spirit `0.27.0`, then confirm Version `0.27.0`, Count through
   the documented five-predicate request, accepted Marker continuity,
   active/running/success judge and daemon, required judge ordering, and three
   listeners.
7. Hash-only argv/executable witnesses must then show OpenAiCodex true, Luna
   true, Terra false, XHigh true, Medium false, and the expected maintained
   wrapper/provider executable provenance. If any required witness fails after
   the acknowledged target activation, use only a separately acknowledged
   owner-channel rollback to the known-good immutable revision and repeat the
   same correlated admission, read-model, journal, profile, and runtime checks.

## Final classification

| Surface | Classification |
|---|---|
| Target immutable lock selection | contract-only |
| Lojix target Current state | stale / absent |
| Lojix daemon and ordinary query channels | wired, but do not contain target evidence |
| Active Home generation `957` | wired to old `0.26.0` closure |
| Judge/daemon dependency and three listeners | wired |
| Luna/XHigh selection | stale old Terra/Medium runtime |
| Target docs/examples | contract-only and non-stale |
| Active source docs | stale; fix blocker |
| Installed public CLI one-object rejection contract | wired for installed `0.26.0` only |
