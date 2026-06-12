# Lojix contract crates — state of the two sockets

Reconnaissance for the cloud-designer lane, session 41. Every claim
below is grounded in a file read or a command run; paths are absolute.

## Headline: the contract has been SPLIT, and prose docs lag the schema

The two repos now encode a clean **read/observe vs. owner-mutate**
split that the top-level prose docs (`signal-lojix/INTENT.md`,
`signal-lojix/ARCHITECTURE.md`) do NOT yet reflect:

- `signal-lojix` (ordinary working signal) = **peer-callable
  read / observe / subscribe** surface only.
- `meta-signal-lojix` (meta policy signal) = **owner-only mutation**
  surface: deploy submission + GC-roots retention policy.

This split is stated authoritatively in the schema files and the
generated `lib.rs` headers, e.g.
`/git/github.com/LiGoldragon/signal-lojix/src/lib.rs:4-6`:

> "Owner-only mutations (Deploy/Pin/Unpin/Retire) live in
> `meta-signal-lojix`."

and `/git/github.com/LiGoldragon/meta-signal-lojix/src/lib.rs:1-13`.

But `signal-lojix/INTENT.md:36-47` and `ARCHITECTURE.md:107-130` still
describe `Deploy`, `Pin`, `Unpin`, `Retire` as living in
`signal-lojix`, alongside a `signal_channel!` macro with
`opens`/`belongs`/`stream` event constructs. **Neither the macro nor
those constructs exist in the actual schema** — see "Schema syntax"
below. The prose is stale relative to the committed schema (schema
files dated 2026-06-05, prose `signal-lojix/INTENT.md` 2026-06-05,
`ARCHITECTURE.md` 2026-06-07; both describe the pre-split single
contract).

Both working copies are clean (`jj diff --stat` = 0 files in each); the
split is fully committed. Latest commits in both (`jj log`) are
"flatten crate to repo root — drop redundant triad-port/ subdir
(Spirit gdgv)" on `main` (signal-lojix `pklnvvnq`/`b31cd980`,
meta-signal-lojix `vuprvymr`/`317b7fab`).

## signal-lojix — ordinary (read / observe / subscribe) socket

Source of truth: `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema`.

**Operation roots (request enum)** — `lib.schema:23`, confirmed in
generated `src/schema/lib.rs:556-562` `pub enum Input`:

- `Query(Selection)` — read the live set; `Selection` is
  `[(ByNode NodeSelector) (ByGeneration GenerationLookup)
  (ByEventLog EventLogRange)]` (`lib.schema:75`).
- `WatchDeployments(DeploymentWatch)` — open deploy-phase
  subscription.
- `WatchCacheRetention(CacheRetentionWatch)` — open retention-
  transition subscription.
- `Unwatch(SubscriptionClose)` — close a subscription by token.
- `CheckHostKeyMaterial(KeyMaterialQuery)` — verify SSH / Yggdrasil
  host key material against a proposal source (`lib.schema:83-88`).

**Reply roots (output enum)** — `lib.schema:24`, generated
`src/schema/lib.rs:567-576`: `Queried(GenerationListing)`, `Watching`,
`Unwatched`, `KeyMaterialChecked`, plus typed rejections `QueryRejected`,
`WatchRejected`, `UnwatchRejected`, `KeyMaterialCheckRejected` (each
wrapping a `Rejected*` payload, `lib.schema:117-120`).

**"Event" payloads, but NOT a streaming channel.** The schema comment
(`lib.schema:11-20`) explicitly records a day-one decision (Spirit
`2tfa`): schema-next **cannot yet emit a daemon-pushed event frame** —
no event/stream root, no opens/belongs. So Watch is authored as an
ordinary request → `SubscriptionToken` reply handshake, and the two
event bodies (`DeploymentPhaseEvent` `lib.schema:92-100`,
`CacheRetentionTransitionEvent` `lib.schema:102-111`) are defined as
plain namespace records so streaming is not dropped from the vocabulary.
The schema-next event-frame-emission enhancement is the named follow-on.
This directly contradicts `ARCHITECTURE.md:93-137` which still describes
a `StreamingFrame` channel with live event streams.

## meta-signal-lojix — meta (owner-only policy) socket

Source of truth:
`/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema`.

**Operation roots (request enum)** — `lib.schema:57`, generated
`src/schema/lib.rs:359-364` `pub enum Input`:

- `Deploy(DeployRequest)` — submit a deploy. `DeployRequest` is
  `[(System SystemDeployment) (Home HomeDeployment)]` (`lib.schema:108`):
  one verb covers FullOs / OsOnly / HomeOnly via the `DeploymentKind`
  discriminant. `SystemDeployment` (`lib.schema:87-97`) carries cluster,
  node, `source ProposalSource`, `flake FlakeReference`, `SystemAction`,
  optional `Builder`, `Vec ExtraSubstituter`, optional `FlakeAttribute`
  (direct-build override). `HomeDeployment` (`lib.schema:98-107`) adds
  `UserName` + `HomeMode [Build Profile Activate]`.
- `Pin(PinRequest)` — pin a generation under a `PinLabel`
  (`lib.schema:110`).
- `Unpin(UnpinRequest)` — remove a pin by label (`lib.schema:111`).
- `Retire(RetireRequest)` — retire a generation (`lib.schema:112`).

**Reply roots (output enum)** — `lib.schema:58`, generated
`src/schema/lib.rs:369-378`: `Deployed(AcceptedDeploy)`,
`Pinned(AppliedPin)`, `Unpinned(AppliedUnpin)`, `Retired(AppliedRetire)`
plus typed rejections `DeployRejected`, `PinRejected`, `UnpinRejected`,
`RetireRejected` (each wrapping a `Rejected*` payload with a
`DatabaseMarker`, `lib.schema:129-132`).

**Rejection reason enums** are closed and domain-typed
(`lib.schema:124-127`), e.g. `DeployRejectionReason
[ClusterUnknown NodeUnknown ProposalSourceUnreachable
FlakeReferenceMalformed BuilderUnreachable SubstituterUnreachable
DeploymentInFlight UnsupportedDeployAction InternalError]`. The schema
notes (`lib.schema:38-41`, `119-123`) record audit-29 decisions:
local builds are permitted (no local-build guard), and
`UnsupportedDeployAction` / `InternalError` exist so the daemon rejects
honestly rather than falsely reporting `Deployed`.

**Shared-type ownership.** `signal-lojix` defines the shared nouns
once; `meta-signal-lojix` cross-imports 12 of them via the single-colon
path form `signal-lojix:lib:TypeName` (`lib.schema:43-56`), generated as
`pub use signal_lojix::schema::lib::X as X` (`src/schema/lib.rs:13-31`).
Imported: `DeploymentIdentifier`, `GenerationIdentifier`, `ClusterName`,
`NodeName`, `UserName`, `PinLabel`, `DeploymentKind`, `SystemAction`,
`GenerationSlot`, `ProposalSource`, `FlakeReference`, `DatabaseMarker`.
Nothing shared is redefined in the meta crate. The `signal-lojix` path
dependency is load-bearing for both schema generation and compilation
(`Cargo.toml:23`; build wiring `build.rs:28-36` via
`DEP_SIGNAL_LOJIX_SCHEMA_DIR`).

## Schema syntax in use (identical form in both)

Neither crate uses a literal `signal_channel!` macro (the term in
`signal-lojix/INTENT.md`/`ARCHITECTURE.md` is stale). The `.schema`
files use schema-rust-next's **positional brace/bracket triad** form,
processed in `build.rs` by `GenerationDriver` +
`GenerationPlan::wire_contract(...)` (signal-lojix `build.rs:23-31`;
meta `build.rs:33-40`). Document order:

1. Imports block `{ LocalAlias source:path:Type ... }` — present and
   populated in meta (`lib.schema:43-56`); present but empty `{}` in
   ordinary (`lib.schema:22`).
2. Operation-roots bracket `[Op1 Op2 ...]` — the request enum.
3. Reply-roots bracket `[Reply1 Reply2 ...]` — the output enum
   (success + `*Rejected`).
4. Definitions block `{ ... }` mapping each root to its payload type,
   then the payload record / sum / newtype definitions.

Within the definitions block: records are `Name { Field * ... }`
(a bare `*` after a TypeName means "field named after the type"; an
explicit lowercase name + TypeName is a named field, e.g.
`source ProposalSource`); sums are `Name [Variant ...]` or
`Name [(Variant PayloadType) ...]`; newtypes are `Name Integer` /
`Name String`. NOTA records are positional (matches the workspace
NOTA-is-positional rule). The generator emits, per crate: tuple-struct
roots, `pub enum Input` / `Output`, `InputRoute` / `OutputRoute`
(`src/schema/lib.rs:2166`/`2186` ordinary; `1289`/`1308` meta),
`route()` projections, signal-frame encode/decode, and (under
`nota-text`) NOTA codecs. Derives per record:
`rkyv::{Archive,Serialize,Deserialize}` + `Clone,Debug,PartialEq,Eq`,
and conditionally `nota_next::{NotaDecode,NotaEncode}`
(`src/schema/lib.rs:16-18`).

Both crates pin the same wire kernel and toolchain: `signal-frame`
(branch main), `rkyv 0.8` (the workspace feature set incl.
`pointer_width_32`, `unaligned`), `nota-next` (optional, `nota-text`
feature), edition 2024, `unsafe_code = forbid`
(`signal-lojix/Cargo.toml:18-31`, `meta-signal-lojix/Cargo.toml:18-32`).

## Two contracts → two CLIs: how cleanly do they map?

Very cleanly. The split is along the exact axis a two-CLI design wants:
**authority**, not just topic.

- **Ordinary socket → read/observe CLI.** Five non-mutating verbs:
  `Query`, `WatchDeployments`, `WatchCacheRetention`, `Unwatch`,
  `CheckHostKeyMaterial`. Safe for any peer; no policy authority needed.
  A `lojix` (or `lojix-query`) CLI binds this socket and speaks the
  `signal-lojix` `Input`/`Output` enums.

- **Meta socket → owner/policy CLI.** Four mutating verbs: `Deploy`,
  `Pin`, `Unpin`, `Retire`. These rewrite the live set / GC roots and
  are owner-only by construction. A second CLI (or a privileged
  subcommand group) binds the meta socket and speaks the
  `meta-signal-lojix` `Input`/`Output` enums.

Each socket is a self-contained `Input`/`Output`/`*Route` quad, so a
CLI per socket needs nothing from the other beyond the 12 shared nouns
— and those flow one-way (ordinary defines, meta imports), so a
meta-CLi transparently links the ordinary crate, but never vice-versa.

Caveats for the two-CLI plan:
1. The streaming asymmetry: `WatchDeployments`/`WatchCacheRetention`
   are currently request→token handshakes, not live event streams
   (schema-next can't emit event frames yet, `signal-lojix/schema/lib.schema:11-20`).
   A `watch` subcommand on the read CLI gets a token + commit sequence,
   not a tailing stream, until the named schema-next follow-on lands.
2. `signal-lojix/INTENT.md` + `ARCHITECTURE.md` are stale (still
   describe the single pre-split contract with a `signal_channel!`
   macro and live streams). They should be refreshed to the split
   reality before they mislead a CLI author — the schema files and
   `src/lib.rs` doc-comments are the current truth.
3. `lojix` daemon (the runtime + both binaries) is out of scope of
   both contract crates; the transport, socket binding, and
   authorization that gate the meta socket live there, not in these
   schemas (`meta-signal-lojix/ARCHITECTURE.md:16-19`).
