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

## Safe retry audit — failed and restored base

The retry ledger was independently read at SHA-256
`ce89856b3ba11d0179af7cb71e01ae5a898317720d8ec71e42b16a019c98657d`.
Its target admission was ID `4`, marker `(44, 44)`. The subsequently requested
base restoration reused ID `4` with marker `(46, 46)`. Those are two distinct
attempts only when their markers and request chronology are retained; the ID is
not a unique attempt key.

Independent direct reads after the executor's STOP trigger found:

- no target revision and no ID-4 Current row in the Lojix UserEnvironment node
  read model;
- the base revision present, but no journal revision/ID/accepted-marker field
  that can bind its terminal result to either retry request;
- base Home generation `957` resolving to Spirit `0.26.0`;
- Spirit Version `0.26.0`, Count `24` through the documented five-predicate
  query, and Marker `(25, 5374348791551424496)`;
- judge and daemon active/running/success, daemon Requires/After judge, and
  exactly three listeners;
- OpenAiCodex/Terra/Medium remains selected on the judge process; Luna/XHigh
  remains false. The maintained wrapper provenance is present but old.

The installed ordinary and owner Spirit CLIs continue to accept one safe
selector object and reject help and multiple operands. This wired `0.26.0`
contract is not evidence for the target release. Target-origin documentation
remains contract-only and the active source docs remain stale as above.

## Definitive retry failure cause and correlation defect

Both retry-window terminal rejections carry the typed category
`ProposalSourceUnreachable`. Their logged failure stages are each
`MaterializeHorizon`; the target attempt failed at `2026-08-04T13:56:26+02:00`
and the requested base restoration at `2026-08-04T13:58:54+02:00`. No typed
`ClusterUnknown`, `NodeUnknown`, `FlakeReferenceMalformed`,
`BuilderUnreachable`, or `ActivationFailed` category occurred in the window.

This definitively places the blocker before Nix evaluation/build, activation,
or the Luna/XHigh runtime. It is the proposal-source/Horizon materialization
boundary. The allowed typed evidence cannot distinguish the inner cause among
an unreadable or unparsable proposal source and a subsequent projection or
materialization failure; do not expose or guess the source contents.

Owning implementation evidence:

- `lojix/src/schema_runtime.rs:3276-3285` emits `MaterializeHorizon` failure;
- `lojix/src/schema_runtime.rs:3485-3518` loads and projects the proposal source
  before producing materialized inputs;
- `lojix/src/schema_runtime.rs:2741-2773` maps that stage to
  `ProposalSourceUnreachable`;
- `lojix/src/daemon.rs:340-374` returns the accepted handle before effects and
  `:580-585` logs only the later terminal output;
- `meta-signal-lojix/src/schema/lib.rs:516-519` defines terminal
  `RejectedDeploy` as reason plus marker, with no deployment identifier or
  source revision;
- `lojix/src/lib.rs:668-678` allocates the next deployment ID from live
  generations only. A pre-Current failure therefore permits ID reuse.

The stated retry protocol has an observability defect: an immediate accepted
handle cannot be joined deterministically to a terminal rejection or journal
entry, and the live-generation allocator can reuse that handle's ID after
failure. Before any future retry, the proposal/Horizon materialization owner
must repair the private source/projection availability and the deployment
protocol must provide a durable terminal record containing the original
deployment identifier, accepted marker, immutable revision, action, and stage.
Until then, an owner Deploy may be admitted but cannot meet the required
correlated-Current acceptance gate. No third retry is supported.

## Final ProposalSource discrimination

Executor provenance, independently checked against the public repository,
establishes that both retry requests supplied the exact non-secret source
`/git/github.com/LiGoldragon/goldragon/datom.nota`. That path is absent: it is
not a symlink, regular file, or case variant. The public repository's only
matching proposal file is
`/git/github.com/LiGoldragon/goldragon/datom.dotos`; it is a regular `0644`
file owned by `li:users`, its parent is traversable, and the system Lojix daemon
runs as `li`. It is therefore readable by the daemon account.

This resolves the apparent executor/filesystem contradiction: the executor
used a stale `.nota` template, whereas the checkout contains `.dotos`. There is
no extension dispatch or fallback in the owning Lojix implementation:
`ProposalFile::new` takes the request path unchanged and `ProposalFile::load`
directly reads and parses it (`lojix/src/schema_runtime.rs:3502-3518`). The
missing `.nota` path therefore fails before proposal parsing and is routed by
the MaterializeHorizon failure mapping to `ProposalSourceUnreachable`. It is
not an immutable-reference, node-identity, build, activation, or provider
selection failure.

The supported Horizon CLI has a stdin parser/projection interface
(`horizon-rs/cli/src/main.rs:1-84`). The `.dotos` metadata-only preflight
passed: it established that the exact source exists, is readable by the daemon
account, and has traversable parents. An authorized disposable `0700` output
probe against the actual `.nota` request was blocked at the same source-absent
boundary; no source or materialized output was printed and cleanup was
verified. A separate `.dotos` projection attempt retained no output and did
not produce a parser/projection validation witness; that limitation does not
negate the passed metadata-only preflight. A direct build of the official
Horizon CLI likewise failed before its consumer binary became available; only
the `BuildFailure` category was retained and its private output was deleted.
This is not evidence that the existing `.dotos` file is invalid. The full
Lojix materialization writer is private to the deploy pipeline and must not be
invoked outside an authorized deploy because it writes materialized inputs.

If a future authorized preflight validates the `.dotos` source through the
supported Horizon consumer, the corrected typed request is exactly:

```text
(Deploy (UserEnvironment (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS?rev=9b3d344631628cb19dda1a22af4d7ef25c5f8def ActivateNow RequireImmutable None [])))
```

That correction is evidence only, not permission for a third retry. Aug-3
successful records do not retain ProposalSource, so source sameness cannot be
proved retrospectively.

## Corrected `.dotos` attempt audit — STOP, restored base

The corrected-attempt ledger exists at SHA-256
`19f4430b800376b7001fea2a8ae4c139d74d2b7431e54c1f5b7e7264ddd3fc07`.
It records only the approved `.dotos` ProposalSource and no forbidden `.nota`
source. Independent metadata checks reconfirm that exact public file exists,
is regular, is readable by the daemon account, and its parent is traversable.

Before a corrected target request was sent, a fresh Gate0 observed a target-like
profile/CLI state: Home generation `958` resolved to Spirit `0.27.0`, Version
reported `0.27.0`, Count was `24`, Marker remained
`(25, 5374348791551424496)`, and the units/listeners were healthy. It was not a
target runtime: the live judge process retained the exact old kernel witness
OpenAiCodex true, Terra true, Medium true, Luna false, XHigh false. Lojix had
no target revision in its node read model or journal. This was an uncorrelated
profile/process split, not a deployment receipt. No provider call was made by
this verifier.

The authorized recovery admission was ID `4`, marker `(53, 53)`. Independent
read-model evidence after the executor's stop signal found an ID-4 base row but
no target revision and no accepted-marker `(53, 53)` in the query result. Thus
ID reuse and the absence of a terminal journal correlation again make it
unsuitable as a recovery receipt.

The final independently observed base is healthy: Home generation `959` and
its closure resolve to Spirit `0.26.0`; Version is `0.26.0`, Count `24`, and
Marker `(25, 5374348791551424496)`. Judge and daemon are
active/running/success, daemon Requires/After judge, three listeners are live,
and the bounded judge argv is restored to OpenAiCodex/Terra/Medium (not
Luna/XHigh). No target acceptance, public-CLI target acceptance, provider
acceptance, or documentation acceptance is claimed from this attempt.

Conclusion: **STOP.** The corrected ProposalSource removes the known missing
path defect, but the intended target was not sent after Gate0 disclosed an
uncorrelated state, and the recovery itself lacks the required marker/terminal
correlation. No further retry is supported without a durable deployment
correlation repair.
