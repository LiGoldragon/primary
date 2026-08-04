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

1. Preserve the currently healthy `0.26.0` state; do not use direct Home
   Manager/NixOS activation to compensate for a missing Lojix receipt.
2. Submit the approved owner Deploy for `goldragon/ouranos/li` with immutable
   CriomOS `9b3d344631628cb19dda1a22af4d7ef25c5f8def`, `ActivateNow`, and
   `RequireImmutable` through the Lojix owner channel.
3. Retain the full typed immediate admission result privately and record only
   its deployment identifier and marker in the evidence ledger. A substring
   match is not success.
4. Poll the ordinary Lojix node query until that same identifier, target
   revision, activation mode, and Current state occur together. Correlate the
   daemon journal terminal event to the identifier. Timeout, rejection, or a
   different identifier is a stop condition, not a cue for direct activation.
5. Independently prove the active Home profile closure contains Spirit `0.27.0`,
   then confirm Version `0.27.0`, Count through the documented five-predicate
   request, accepted Marker continuity, active/running/success judge and
   daemon, required judge ordering, and three listeners.
6. Hash-only argv/executable witnesses must then show OpenAiCodex true, Luna
   true, Terra false, XHigh true, Medium false, and the expected maintained
   wrapper/provider executable provenance. If any required witness fails after
   an acknowledged target activation, use only an acknowledged owner-channel
   rollback to the known-good immutable revision and repeat the same correlated
   Lojix query/journal/profile checks.

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
