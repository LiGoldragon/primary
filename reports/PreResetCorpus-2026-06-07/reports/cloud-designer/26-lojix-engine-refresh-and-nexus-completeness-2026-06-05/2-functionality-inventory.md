# lojix functionality inventory — Stack A vs the rewrite surfaces

Lens: enumerate EVERY distinct piece of functionality the legacy deploy
stack actually performs, then check it against the GREEN rewrite's
Nexus engine feature catalog
(`/home/li/wt/github.com/LiGoldragon/lojix/triad-port/schema/nexus.schema`),
the SEMA durable-state plane (same dir, `sema.schema`), and the two wire
contracts (`signal-lojix` + `meta-signal-lojix` `lib.schema`).

Anchor principle z6qu (Principle, VeryHigh, psyche 2026-06-05): the Nexus
schema is the engine's INTERNAL FEATURE CATALOG — *every* computation,
filter, condition, conditional write, and internal logic-feature MUST be a
declared Nexus verb+object, so the complete feature surface is visible in
the schema and nothing lives as inline hand-written logic. This inventory
is the checklist against that principle: any Stack A behavior that has no
Nexus verb/object (or SEMA root) is either a migration gap or a feature
that would otherwise land as hidden inline logic — a z6qu violation.

Primary source: legacy Stack A monolith
`/git/github.com/LiGoldragon/lojix-cli/src/*.rs` (activate, artifact,
build, check, cluster, copy, deploy, host, process, project, request,
stage, error, lib, main).

## Method note — what each rewrite surface is allowed to carry

Per intent l6zw / 3d5z / bodd (the triad-separation corrections): the two
Signal contracts carry ONLY wire vocabulary (peer-callable verbs +
records + codec); Nexus and SEMA are daemon-internal and must NOT appear
in any contract. So "covered by the wire contract" answers a DIFFERENT
question than "covered by Nexus". For the migration-gap check that matters
here, the test for an *internal effect* is: is there a Nexus
`EffectCommand` / `EffectResult` variant (or a SEMA root) for it? A wire
verb existing is necessary for external operations but says nothing about
whether the internal pipeline step is modeled.

## (a) External operations — what a caller can ask for

These are the Stack A request surface (`request.rs` `LojixRequest`
variants + `main.rs` dispatch) mapped to the rewrite's wire roots.

| Stack A operation | file:symbol | Rewrite wire home | Status |
|---|---|---|---|
| FullOs deploy | `request.rs:13 FullOs` → `deploy.rs:89 deploy` | meta-signal `Deploy` → `DeployRequest::System` + `DeploymentKind::FullOs` | covered |
| OsOnly deploy | `request.rs:24 OsOnly` | meta-signal `Deploy` + `DeploymentKind::OsOnly` | covered |
| HomeOnly deploy | `request.rs:35 HomeOnly` | meta-signal `Deploy` → `DeployRequest::Home` (`HomeDeployment` + `HomeMode`) | covered |
| CheckHostKeyMaterial | `check.rs:29 CheckHostKeyMaterial` | signal `CheckHostKeyMaterial` → `KeyMaterialQuery` / `KeyMaterialReport` | covered |
| (new) Query generations | — (no Stack A equiv; new daemon surface) | signal `Query` → `Selection` / `GenerationListing` | new, no parity baseline |
| (new) WatchDeployments | — | signal `WatchDeployments` → subscription handshake | new |
| (new) WatchCacheRetention | — | signal `WatchCacheRetention` | new |
| (new) Unwatch | — | signal `Unwatch` | new |
| (new) Pin / Unpin / Retire | — | meta-signal `Pin` / `Unpin` / `Retire` | new (GC-roots policy surface) |

The four Stack A external operations all have a wire home. The rewrite
ADDS a large query/observe/retention surface that Stack A never had
(Stack A is a one-shot CLI; the daemon is long-lived with durable state),
which is correct per ARCHITECTURE.md §1. No external-operation *parity*
gap. The gaps are all in the internal pipeline (section e).

### Eval-only is a request-level shape Stack A carries that the wire flattens

Stack A's `SystemAction::Eval` (`build.rs:11`) produces a derivation path
and NO closure — `DeployOutcome::Evaluated { derivation_path }`
(`deploy.rs:69`). On the wire, `SystemAction` keeps `Eval`
(signal-lojix:lib:56) but the meta-signal `DeployRequest` discriminant
carries `SystemAction` so Eval rides through. In Nexus, `NixEvalCommand`
exists and `EvaluatedClosure` is a real EffectResult, so the eval path is
*modeled* in the catalog. But note SEMA has no "eval-only, nothing
durable to record" terminal — see gap G14.

## (b) Internal effects — the deploy pipeline

This is the substance for the z6qu check. Stack A's `deploy.rs:89 deploy`
runs this pipeline in order. Each stage below is a real Stack A effect;
the right column is its Nexus `EffectCommand`/`EffectResult` home (or
absence).

| # | Pipeline stage | Stack A file:symbol | Nexus catalog home | Status |
|---|---|---|---|---|
| 1 | Load + decode cluster proposal | `cluster.rs:20 ProposalSource::load` | — (folded into `FlakeAuthRequest.source`?) | GAP G1 |
| 2 | Project horizon from proposal + viewpoint | `project.rs:18 HorizonProjection::project` | — | GAP G2 |
| 3 | Validate home user exists in horizon | `deploy.rs:31 validate_home_user` | — | GAP G3 |
| 4 | Resolve builder target (local vs remote, isRemoteNixBuilder gate) | `deploy.rs:49 resolve_builder_target` | partial: `BuildTarget [Local (Remote BuilderNode)]` | partial G4 |
| 5 | Resolve extra substituters from horizon nodes (ygg→URL, pubkey) | `deploy.rs:210 from_horizon_nodes` + `CacheEndpoint` | partial: `ExtraSubstituter {url public_key}` carries RESULT only | GAP G5 |
| 6 | Materialize horizon.json + flake.nix override input | `artifact.rs:65 HorizonDir::write` | — | GAP G6 |
| 7 | Materialize system override input (nixSystemName flake) | `artifact.rs:93 SystemDir::write` | — | GAP G6 |
| 8 | Materialize deployment override input (includeHome flake-text) | `artifact.rs:128 DeploymentDir::write` | — (DeploymentKind carries intent, not the flake) | GAP G6 |
| 9 | Materialize secrets override input (copy sops files + flake) | `artifact.rs:155 SecretsDir::write` + `ClusterSecrets` | — (nothing about secrets anywhere) | GAP G7 |
| 10 | NAR-hash each materialized dir (`nix hash path --sri`) | `artifact.rs:218 NarHashInput::invocation` | — | GAP G6 |
| 11 | Build FlakeInputRef (`path:…?narHash=…`) per input | `cluster.rs:64 FlakeInputRef::from_local_path` | — | GAP G6 |
| 12 | Stage generated inputs to REMOTE builder (mkdir + rsync) | `stage.rs:170 RemoteInputStage::run` | — | GAP G8 |
| 13 | Nix eval drvPath (Eval action) | `build.rs:289 nix_invocation` (EvalDrvPath) | `EffectCommand::NixEval` → `NixEvalCommand` | covered |
| 14 | Nix build closure (`--override-input` x4, extra-substituters) | `build.rs:289 nix_invocation` (BuildClosure) + `build.rs:374 execution_invocation` (wrap in ssh when remote) | `EffectCommand::NixBuild` → `NixBuildCommand` | partial G9 |
| 15 | Copy closure (Dispatcher→target / Builder→target / skip) | `copy.rs:35 ClosureCopy::invocation` (`--substitute-on-destination`, `--from`/`--to`) | `EffectCommand::CopyClosure` → `CopyClosureCommand` | partial G10 |
| 16 | System activate: nix-env --set + switch-to-configuration | `activate.rs:39 ssh_invocation` | `EffectCommand::ActivateGeneration` + `ActivationKind` | partial G11 |
| 17 | BootOnce: transient systemd-run unit + bootctl oneshot/default | `activate.rs:92 boot_once_script` + `135 systemd_run_invocation` | `ActivationKind::BootOnce` (the discriminant only) | GAP G11 |
| 18 | EFI reconcile (readlink system profile, set-default, clear-oneshot) | `activate.rs:212 reconcile_efi` + steps 169/177/190 | — (no EffectCommand step) | GAP G11 |
| 19 | Home activate: profile-set + activate, local-vs-remote context | `activate.rs:266 HomeActivation` (`run_profile`/`run_activate`/`is_local_context`) | — (no home EffectCommand at all) | GAP G12 |
| 20 | path-info / GC | (NOT in Stack A — daemon-new per ARCHITECTURE.md) | `EffectCommand::PathInfoGc` → `PathInfoGcCommand` | new |

Stack A also has a generic process-execution substrate
(`process.rs ProcessInvocation`, `ShellCommand`, `ShellArgument` shell
quoting, `ProcessGroup`+`KillOnDrop` child-tree reaping). That is plumbing
beneath every effect, not a feature to catalog — but the KillOnDrop /
process-group reaping behavior (`process.rs:64`) is a real operational
property (Ctrl-C kills the whole nix/ssh tree) that the daemon must
preserve and that no schema captures. Noted as G13 (mechanism, not
schema-shaped).

### z6qu reading of section (b)

Of the 19 Stack-A internal effects, the Nexus catalog models 6 as
first-class verbs (`ResolveFlakeAuth`, `NixEval`, `NixBuild`,
`CopyClosure`, `ActivateGeneration`, `PathInfoGc`). The remaining ~13 —
proposal load, horizon projection, home-user validation, substituter
resolution, the entire artifact-materialization subsystem (4 input dirs +
NAR-hash + flake-ref), remote input staging, secrets handling, EFI
reconcile, BootOnce mechanics, and home activation — have NO Nexus
verb/object. Under z6qu these are exactly the features that would
otherwise land as hidden inline logic inside effect handlers. The catalog
is currently a coarse 6-verb skeleton; Stack A's real pipeline is ~3x
denser. This is THE headline finding.

## (c) Durable state mutations + reads

The daemon owns durable state Stack A never had (Stack A is stateless —
it writes a `~/.cache/lojix/...` artifact cache, `artifact.rs:55`, but
holds no live-set / event-log). So this section is mostly NEW surface,
measured against ARCHITECTURE.md §1's four owned planes.

| Owned plane (ARCHITECTURE.md §1) | SEMA root | Status |
|---|---|---|
| Live generation set | `LiveSetTable` / `LiveGeneration` + `QueryGenerations`/`RecordGenerationActivated` | covered |
| GC roots tree (current/boot-pending/rollback/pinned/recent) | `GcRootsTable` / `GcRoot` + `PinGeneration`/`UnpinGeneration`/`RetireGeneration` | covered (but see G15) |
| Deploy event log (append-only typed events) | `EventLogTable` / `EventLogEntry` / `LoggedEvent` + `ReadEventLog`/`RecordPhaseTransition` | covered |
| Container lifecycle mirror | `ContainerLifecycleTable` + `RecordContainerTransition` | covered |
| Deploy submission record | `RecordDeploySubmitted` → `DeploySubmission` | covered |

Reads: `QueryGenerations`, `ReadEventLog`, `CheckKeyMaterial` (note:
key-material check is modeled as a SEMA READ, which is odd — see G16).
Writes: deploy-submitted, phase-transition, generation-activated, pin,
unpin, retire, container-transition — a complete-looking write surface
for the daemon's OWN state model.

The artifact cache (`~/.cache/lojix/{horizon,system,deployment,secrets}`,
`artifact.rs`) and the remote staging root
(`/var/tmp/lojix/generated-inputs/<key>`, `stage.rs:136`) are durable
filesystem state Stack A mutates that the SEMA plane does not model. They
are build-input scratch, not daemon-owned database state, so arguably out
of SEMA scope — but the GC-roots plane is explicitly about protecting
freshly-built closures from cache eviction (`recent/<timestamp>`), and
the artifact cache is the input side of that same lifecycle. Flagged as
G6's durable-state shadow.

## (d) Observation / streaming surfaces

All NEW (Stack A has none — it streams nix/ssh stderr to the operator's
terminal live, `process.rs:89 inherit_stdio`, but that is process I/O,
not a subscription surface).

| Surface | Wire home | Status |
|---|---|---|
| Deployment phase stream | signal `WatchDeployments` + `DeploymentPhaseEvent` (Submitted/Building/Built/Copying/Activating/Activated/Failed) | covered (handshake form per day-one decision 2tfa) |
| Cache-retention stream | signal `WatchCacheRetention` + `CacheRetentionTransitionEvent` (Pinned/Unpinned/Promoted/Demoted/Retired/Evicted) | covered (handshake form) |
| Subscription open/close | `SubscriptionOpened`/`SubscriptionClosed`/`Unwatch` | covered |

Note (from prior report 25's streaming analysis + the signal-lojix header
comment lines 11-20): schema-next CANNOT yet emit a daemon-pushed event
FRAME, so Watch/Unwatch is authored as a request→`SubscriptionToken`
handshake and the two event payloads are namespace records. The actual
push transport is the named follow-on. This is a known, documented
limitation, not a gap in THIS inventory — but it means the streaming
surface is contract-complete and transport-incomplete.

Stack A's live-feedback behaviors that the daemon must NOT lose:
- nix build progress + ssh diagnostics streamed to the operator terminal
  (`build.rs:343 run` comment; `process.rs` inherit_stderr). In a daemon
  these become `DeploymentPhaseEvent detail` strings, but the rich
  line-by-line nix progress is lost unless modeled. G17.
- BootOnce re-attach guidance printed on ssh drop
  (`activate.rs:235-251` eprintln) — operator recovery affordance, no
  schema home. G11 sub-item.

## (e) The migration-gap list — Stack A functionality NOT yet in the rewrite

Exhaustive, specific, cited. Severity is the author's read for the
synthesis agent; "z6qu" tags gaps that are inline-logic-hiding risks.

### G1 — proposal load (Medium)
`cluster.rs:20 ProposalSource::load` reads + NOTA-decodes a
`ClusterProposal`. The Nexus catalog has no proposal-load verb;
`FlakeAuthRequest { source flake }` (nexus.schema:55) names a
`ProposalSource` but `ResolveFlakeAuth`'s result is `ResolvedFlake
{ flake revision }` — flake resolution, NOT proposal decode. Where does
"decode the cluster proposal" live? Under z6qu it needs a verb or it
becomes hidden inline logic in the FlakeAuth handler.

### G2 — horizon projection (High, z6qu)
`project.rs:18 project` → `ClusterProposal::project(viewpoint)` is the
core typed-cluster-data computation: proposal + viewpoint → per-node
`Horizon`. EVERY downstream effect (builder resolution, substituter URLs,
home-user validation, the horizon.json artifact) depends on it. It has NO
Nexus verb. This is the single biggest hidden-logic risk: horizon
projection is decision-making over cluster data and z6qu says
decision-making is a declared Nexus verb. Also intertwines with raw/pretty
split (9p8v/avvh): the projection that produces the horizon.json artifact
is RAW horizon; the rewrite's Nexus catalog should make the projection
step visible as a verb so the raw→artifact seam is explicit.

### G3 — home-user validation (Low, z6qu)
`deploy.rs:31 validate_home_user` rejects a HomeOnly deploy whose user is
not in the projected horizon users (→ `Error::UnknownHomeUser`). This is a
typed condition/gate on a deploy — exactly a z6qu "condition on results"
that must be a Nexus verb/object. No home-user validation verb exists; the
meta-signal `DeployRejectionReason` enum (meta:110) lists ClusterUnknown /
NodeUnknown but NO UnknownHomeUser reason. Both the gate (Nexus) and the
rejection reason (wire) are missing.

### G4 — builder resolution gate (Medium, partial)
`deploy.rs:49 resolve_builder_target` does three things: (1) viewpoint
node → local self-build target; (2) sibling node → must have
`is_remote_nix_builder` else `Error::InvalidBuilder`; (3) unknown node →
`Error::UnknownBuilder`. Nexus has `BuildTarget [Local (Remote
BuilderNode)]` (nexus.schema:52) — the RESULT shape — but no verb that
PERFORMS the resolution+validation, and the `is_remote_nix_builder` gate
(a typed condition) is unmodeled. meta-signal has `BuilderUnreachable`
(meta:110) but not an "invalid builder / not a remote builder" reason.
The local-build-never-rejected discipline (nexus.schema header lines
17-23, intent dropped-guard) is correctly encoded as `Local` being a
first-class variant — that part is good.

### G5 — substituter resolution (Medium, z6qu)
`deploy.rs:210 from_horizon_nodes` + `CacheEndpoint::url`
(`deploy.rs:236`) computes each substituter's URL from the node's
ygg_address (`http://[<ipv6>]`) or `nix_url`, and requires
`nix_pub_key_line`, else `Error::InvalidSubstituter` /
`UnknownSubstituter`. Both Nexus `ExtraSubstituter` and meta-signal
`ExtraSubstituter` carry `{url public_key}` — the already-RESOLVED values.
The resolution computation (node-name → URL+key, with the ygg-vs-nixurl
choice and the validation gate) has no Nexus verb. Caller would have to
pre-resolve, which pushes horizon knowledge to the client — wrong, since
the daemon owns horizon projection. z6qu: the URL-derivation logic must be
a declared verb.

### G6 — artifact materialization subsystem (HIGH, z6qu) — the biggest gap
The entire `artifact.rs` + `cluster.rs` FlakeInputRef machinery is absent
from Nexus and SEMA. Specifically:
- `HorizonDir::write` (`artifact.rs:65`): serialize horizon to
  `horizon.json` + write the `fromJSON(readFile ./horizon.json)` flake
  template.
- `SystemDir::write` (`artifact.rs:93`): write a `{ system = "x86_64-linux"
  }` flake.
- `DeploymentDir::write` (`artifact.rs:128`): write the
  `{ deployment.includeHome = true|false }` flake-text
  (`build.rs:85 flake_text`). The home-on/home-off distinction
  (`DeploymentShape`, `build.rs:57`) drives a per-shape cache dir
  (`home-on`/`home-off`) — this includeHome flake is HOW DeploymentKind
  is realized, and it is gone.
- `NarHashInput::calculate` (`artifact.rs:218`): `nix hash path --type
  sha256 --sri` of each dir.
- `FlakeInputRef::flake_ref` (`cluster.rs:76`): `path:<dir>?narHash=<sri>`
  with URL-encoding (`as_url_parameter`, `cluster.rs:112`).
- These become the four `--override-input horizon|system|deployment|
  secrets <ref>` args to `nix build` (`build.rs:307`).

Nexus's `NixBuildCommand { GenerationIdentifier ClosurePath target
substituters }` (nexus.schema:58) has NO place for the override-input
refs, and `NixEvalCommand { … flake attribute }` (nexus.schema:57) has
only flake+attribute. The whole override-flake-input mechanism — the thing
that makes lojix's hermetic per-deploy build work — is unrepresented. This
is the densest cluster of hidden-inline-logic risk under z6qu. It is also
where the raw/pretty seam (9p8v) lands: horizon.json is RAW horizon
serialized for Nix.

Durable-state shadow: the `~/.cache/lojix/...` artifact cache
(`artifact.rs:55/84/119/146`) is keyed by cluster/node/system/shape and
NAR-hashed for content-addressed reuse — a real caching feature with no
SEMA representation.

### G7 — secrets handling (HIGH, z6qu) — entirely absent
`artifact.rs:155 SecretsDir::write` + `ClusterSecrets`
(`artifact.rs:181`) copy three sops files
(`router-wifi-sae-passwords.sops`, `router-backup-wifi-password.sops`,
`local-llm-api-token.sops`) from `<proposal-dir>/secrets/` into a secrets
override flake (`SECRETS_FLAKE_TEMPLATE`, `artifact.rs:21`), conditionally
(only when the first sops file exists). This produces the
`--override-input secrets <ref>` (`build.rs:323`). NOTHING about secrets
appears in Nexus, SEMA, or either wire contract. A FullOs deploy of a node
that needs router wifi passwords WILL be functionally broken without it.
Hard-coded file names are themselves a smell (should be horizon-driven),
but the FEATURE must exist somewhere. This is a silent-correctness gap,
not just a tidiness gap.

### G8 — remote input staging (Medium, z6qu)
`stage.rs:170 RemoteInputStage::run` — when building on a REMOTE builder,
the generated input dirs must be rsync'd to the builder first
(`/var/tmp/lojix/generated-inputs/<hash-key>/<input>/`), via per-input
`mkdir -p` + `rsync -a --delete` (`stage.rs:152/159`), and the
FlakeInputRefs are rewritten to the remote paths (`stage.rs:184 plan`).
`deploy.rs:124` branches local (`BuildInputReferences::from_local_artifact`)
vs remote (`RemoteInputStage::from_artifact(builder).run()`). Nexus's
`BuildTarget::Remote` exists but the staging effect — a real
mkdir+rsync+ref-rewrite pipeline gated on remote-build — has no verb.
Tightly coupled to G6 (you stage what you materialized).

### G9 — NixBuild override-inputs + remote-ssh-wrap (Medium, partial)
Beyond G6's missing refs: `build.rs:374 execution_invocation` wraps the
whole nix invocation in an ssh-to-builder ShellCommand when a builder is
set — i.e. the build RUNS ON the builder over ssh, not via nix's own
`--builders`. Nexus `NixBuildCommand` carries `target BuildTarget` so the
intent is there, but the "wrap in ssh and run remotely" mechanics (vs
local) plus the `--refresh --no-link --print-out-paths` flag set
(`build.rs:298`) are unmodeled. Also `NixBuildCommand` lacks the flake +
attribute (it has ClosurePath as if the path is an input, but build
PRODUCES the path) — the command/result shapes look swapped; the build
command should carry flake+attribute+overrides and the RESULT carries the
ClosurePath. Worth a closer look by the schema-shape sub-agent.

### G10 — copy-closure substitute-on-destination + 3-way routing (Low, partial)
`copy.rs:35 invocation` encodes three routes (Dispatcher→target via
`--to`; Builder==target → skip; Builder!=target → `--from <b> --to
<target>`) and ALWAYS passes `--substitute-on-destination` (the
sign-via-cache trick, `copy.rs` doc lines 19-25). Nexus `CopyClosureCommand
{ GenerationIdentifier ClusterName NodeName ClosurePath }` has no source
field — it can't express "copy FROM the builder" vs "from dispatcher",
and the skip-when-already-there optimization and substitute-on-destination
flag are unmodeled. The source routing depends on where G9's build landed,
so this needs the `BuildLocation` (`build.rs:205`) carried through.

### G11 — activation: EFI reconcile + BootOnce + Test-no-bootloader (HIGH, z6qu)
`activate.rs SystemActivation` is the densest correctness logic in Stack A
and Nexus flattens it to `ActivationKind [Switch Boot Test BootOnce]` (a
discriminant) + one `ActivateGeneration` verb. Lost:
- EFI reconcile (`reconcile_efi`, `activate.rs:212`): after Boot/Switch,
  readlink `/nix/var/nix/profiles/system` → derive generation → `bootctl
  set-default <entry>` + `bootctl set-oneshot ''`. The `requires_efi_reconcile`
  gate (`activate.rs:160`, true only for Boot/Switch) is a typed condition.
  Three distinct ssh steps (`activate.rs:169/177/190`) with NO Nexus verbs.
- BootOnce (`activate.rs:92 boot_once_script` + `135
  systemd_run_invocation`): a transient `systemd-run --wait` unit so a
  dropped ssh doesn't abort activation; bootctl oneshot=new
  default=old(running). Entirely unmodeled beyond the discriminant.
- Test never touches the bootloader (`activate.rs:58` — runs
  switch-to-configuration test WITHOUT the nix-env --set); the
  nix-env-set-vs-not condition is unmodeled.
- The transient-unit name minting + re-attach guidance
  (`activate.rs:75 unit_name`, `235-251`) — operator recovery affordance.
This is the second-biggest hidden-logic cluster. The daemon either grows a
much richer activation effect catalog or buries `switch-to-configuration`
+ `bootctl` + `systemd-run` orchestration as inline handler logic (z6qu
violation). `signal-lojix:lib:SystemAction` keeps all six actions but
`ActivationKind` drops `Eval`/`Build` (correct — those don't activate),
yet nothing models the within-activation branching.

### G12 — home activation (HIGH, z6qu) — no effect verb at all
`activate.rs:266 HomeActivation` has its own pipeline: `run_profile`
(nix-env -p `~/.local/state/nix/profiles/home-manager` --set) +
`run_activate` (`<store>/activate`), gated by `HomeMode`
(Build=noop / Profile / Activate, `build.rs:39`), AND a
local-vs-remote context detection (`is_local_context`, `activate.rs:331`:
compare current USER + `hostname -s` against requested user+node, choose
local exec or ssh-as-user). The wire carries `HomeDeployment` +
`HomeMode`, but Nexus has NO home-activate EffectCommand — only the
system `ActivateGeneration`. A HomeOnly deploy currently has no internal
effect home. The local-vs-remote-context decision is pure z6qu
decision-making with no verb.

### G13 — process child-tree reaping (Low, mechanism)
`process.rs:64 ProcessGroup::leader() + KillOnDrop` reaps the whole nix +
ssh child tree on Ctrl-C / future-drop. In a long-lived daemon this
becomes per-deploy cancellation. Mechanism, not schema-shaped, but the
daemon must preserve cancel-kills-the-tree or a cancelled deploy leaks a
running remote nix build. Flag for the daemon-impl sub-agent.

### G14 — eval-only terminal has no SEMA write (Low)
`SystemAction::Eval` produces a drvPath and records nothing durable
(`deploy.rs:69 Evaluated`). Nexus models `NixEval`→`EvaluatedClosure`, but
SEMA's `SemaWriteInput` (sema:53) has no "evaluated, nothing to commit"
path and the live-set/event-log only know built/activated generations.
Probably correct (eval is a dry-run), but worth confirming the Nexus
`EffectCompleted(ClosureEvaluated …)` can terminate to a `ReplyToSignal`
WITHOUT a SEMA write — the `NexusAction` union (nexus.schema:76) does
allow `ReplyToSignal` directly, so this is likely fine; noting for
completeness.

### G15 — GC-roots slot mechanics not in the effect catalog (Medium, z6qu)
ARCHITECTURE.md §1 specifies rich GC behavior: per-kind slots
(current/boot-pending/rollback[N]/pinned/recent[ts]), `nix path-info -r`
closure introspection, two-phase deletion respecting narinfo TTL,
promotion/demotion between slots. SEMA models the STATE
(`GcRootsTable`/`GcRoot`, `GenerationSlot`) and the cache-retention
transitions exist as wire events (Promoted/Demoted/Evicted). But the only
Nexus GC effect is `PathInfoGc { ClusterName NodeName }` →
`GarbageCollected { reclaimed_paths }` — a single coarse verb. The
slot-promotion logic, the rollback-ring eviction, the TTL-respecting
two-phase delete, and the gcroots-symlink writes
(`/nix/var/nix/gcroots/criomos/...`) are all decision-making with no Nexus
verbs. This is daemon-NEW functionality (not a Stack A port) but it is the
same z6qu risk: a whole retention engine would hide inside one
`PathInfoGc` handler.

### G16 — key-material check modeled as a SEMA read (Low, design-smell)
`check.rs CheckHostKeyMaterial` is a LIVE ssh-to-host operation: cat the
host's `/etc/criomOS/complex/publication.nota`, decode, diff against
horizon expectations (`check.rs:36 run`). It touches NO durable daemon
state. Yet sema.schema:48 models it as `SemaReadInput::CheckKeyMaterial`.
Reading host state over ssh is an EFFECT (network I/O against an external
host), not a SEMA durable-state read. Per the inner/outer-world vocabulary
(9ypt: SEMA is the INNER durable-state world), a live host probe belongs
in Nexus as an EffectCommand, not SEMA. Misplacement; flag for the
schema-shape sub-agent. Also the three concern types
(ssh-pubkey / ygg-pubkey / ygg-address) and the per-mismatch operator
hints (`check.rs:144` etc.) ARE preserved on the wire
(`KeyMaterialConcern`, `KeyMaterialMismatch.operatorHint`) — good parity
there.

### G17 — live nix-progress streaming (Medium)
Stack A streams nix build progress + ssh diagnostics line-by-line to the
operator terminal (`process.rs:89 inherit_stdio`, `build.rs:343` comment).
The daemon's `DeploymentPhaseEvent` (signal:92) has coarse phases
(Building/Built/...) + an optional `detail` string — it can carry phase
transitions but NOT the rich live nix output. Either accept the
fidelity loss (phases only) or model a progress-line event. Decision for
the psyche; flagged as an intent-clarification candidate.

## Headline summary for the synthesis agent

The external-operation surface has full parity (4 Stack A ops all have a
wire home) and the daemon correctly ADDS query/watch/pin/retire +
durable-state planes. The durable-state and observation surfaces look
complete against ARCHITECTURE.md §1.

The gap is the INTERNAL EFFECT catalog. Nexus declares 6 effect verbs;
Stack A's real pipeline is ~19 distinct effects. Under z6qu (Nexus =
the visible catalog of every internal feature, VeryHigh), the ~13
unmodeled effects are precisely the features that will otherwise become
hidden inline logic inside effect handlers. The highest-severity gaps:
- G6 artifact materialization (the override-flake-input subsystem — 4
  input dirs, NAR-hash, flake-ref) — entirely absent;
- G7 secrets handling — entirely absent, a silent-correctness gap;
- G11 activation EFI-reconcile + BootOnce — densest logic, flattened to a
  discriminant;
- G12 home activation — no effect verb at all despite a wire
  `HomeDeployment`;
- G2 horizon projection — core decision-making with no verb.

Two design-shape smells for the schema sub-agent: G9 (NixBuildCommand
appears to carry ClosurePath as input when build PRODUCES it — command/
result shapes look swapped, and override-inputs have no field) and G16
(live key-material host-probe wrongly modeled as a SEMA read instead of a
Nexus effect). G3/G4/G5 each also need matching rejection reasons added to
the wire enums (UnknownHomeUser, InvalidBuilder, InvalidSubstituter).

One intent-clarification candidate for the psyche: G17 — accept coarse
phase-only deploy observation, or model live nix-progress-line events?
