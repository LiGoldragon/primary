# 4 · Hanging-bug + missed-polish ledger — deduplicated, re-verified against current source

cloud-designer lane D, session 72. 2026-06-19. The single deduplicated
register of every OPEN bug/polish item across cloud-lane reports 68/69/70/71
plus report 72's two verified seeds, each re-checked against current source
(cloud `3b38cdd`, signal-cloud + meta-signal-cloud `main`, horizon-rs,
CriomOS, the `cloud-designer-intent-refresh` branch at `88b852d`). Already-fixed
items are recorded only where their *partial* residue is still open; fully
closed items (report 66 `.com` fix, the live socket-spine apply behavioral
proof from report 70) are NOT relisted.

## TL;DR

- **One newly-confirmed P1 the branch did NOT close: the `cloud-daemon`
  flake wrapper never injects the Cloudflare credential the daemon reads.**
  The branch fixed the *flarectl* wrapper gopass path (`flake.nix:46`) and
  the INTENT.md handle wording, but the `cloud-daemon` postInstall wrapper
  (`flake.nix:96-99`) still injects only `HCLOUD_TOKEN` and
  `DIGITALOCEAN_ACCESS_TOKEN`. The daemon resolves the Cloudflare token by
  `std::env::var(handle)` (`cloudflare.rs:53`); with the production handle
  `CLOUDFLARE_DNS_TOKEN` (`tests/runtime.rs:470`), that var is absent in the
  daemon's environment, so `EnvironmentCredentialSource` returns
  `CredentialUnavailable` and every Cloudflare meta op fails unless the
  operator hand-exports it. This is a small flake fix, code-backed, and
  belongs on the designer feature branch.
- **The daemon was re-architected since report 68** (the old `src/daemon.rs`
  kameo `EngineActor` is gone; the spine is now EMITTED into
  `src/schema/daemon.rs` as an `ActorMultiListenerDaemon`). The structural
  finding survives the re-architecture intact: provider IO is still blocking
  `ureq`/`flarectl` called synchronously inside the `async` handlers
  (`schema_daemon.rs:74-109` → `lib.rs:693-699` → `apply_*`) with no
  `spawn_blocking` and no per-call timeout. **All report-68 citations into
  `daemon.rs` are now stale and must be re-grounded to `schema_daemon.rs` /
  `lib.rs`.**
- **Two designer-now report fixes:** report 71 §4 + 5-synthesis mermaids show
  the lojix deploy leg as `nix copy --to ssh-ng://`, but lojix moved to
  build-on-target (`nix build --eval-store auto --store ssh-ng://…`, report
  150). And `protocols/active-repositories.md:91` still describes cloud as a
  "single `EngineActor` over a synchronous sema-engine `Store`" — wrong on
  both legs now.
- **The report-68 P1/P2 structural ledger is otherwise intact**: wire
  two-tree drift, meta schema re-declaration, Hetzner unshipped, ad53
  platform half absent, encoder homeless, sema pilot dead, CredentialHandle
  custody, ImageName/ssh-key polish — all reproduce verbatim against current
  source. None has been fixed in code.

## Severity × lane matrix

| ID | Item | Sev | Lane | Status vs current source |
|---|---|---|---|---|
| D1 | CF daemon env-wiring gap | P1 | designer-now (flake on branch) | OPEN — branch fixed flarectl line, not daemon wrapper |
| D2 | Blocking provider IO in async handler (ex-#2) | P1 | operator-bead | OPEN — survives daemon re-architecture |
| D3 | Wire two-tree drift + schema_bridge straddle (ex-#3) | P1 | designer-now | OPEN — hand-written tree still drifted, 3141-line bridge |
| D4 | Meta schema re-declares signal-cloud types (68-3-P1-2) | P1 | designer-now | PARTIAL — Cargo dep added; schema still redeclares |
| D5 | Hetzner (lead-or-not) ships in no binary (ex-#4b) | P1 | designer-now + psyche | OPEN — `#[cfg(feature=hetzner)]`, no flake package |
| D6 | `apps.daemon` default is DNS-only (ex-#4a) | P1 | designer-now (flake on branch) + psyche | OPEN — `apps.daemon`→default→cloudflare-only |
| D7 | ad53 CloudNode platform half absent (ex-#5) | P1 | operator-bead + designer-now (INTENT stance) | OPEN — `NodeSpecies` ends at `TestVm` |
| D8 | report 71 §4 + 5-synthesis deploy-leg staleness | P2 | designer-now | OPEN — `nix copy` vs build-on-target |
| D9 | active-repositories.md:91 stale daemon description | P2 | designer-now | OPEN — "single EngineActor / sema Store" wrong |
| D10 | cloud ARCHITECTURE.md 5-actor/no-block + sema pilot unreconciled | P2 | designer-now | OPEN — branch never touched ARCHITECTURE.md |
| D11 | Config encoder has no NOTA/deploy-stack home (ex-#6) | P2 | designer-now | OPEN — `examples/write_config.rs`, 3 args, hardcoded |
| D12 | sema-engine pilot dead weight; two state machines (ex-#7) | P2 | designer-now + psyche | OPEN — `build_runtime` builds `Store`, not `SchemaStore` |
| D13 | Compute adapters near-byte mirrors; no shared REST client | P2 | designer-now | OPEN — two separate `HttpApi` + `create_server` |
| D14 | `ensure_ssh_key` never called on create path | P2 | operator-bead | OPEN — zero production callers |
| D15 | CredentialHandle = unvalidated wire-string-as-getenv | P2 | designer-now + psyche | OPEN — `CredentialHandle(String)`, no validation |
| D16 | ImageName unvalidated stringly newtype | P2 | designer-now | OPEN — `ImageName(String)`, no `TryFrom` |
| D17 | No committed socket-apply test (P1-b artifact axis) | P2 | operator-bead | OPEN — spine proven manually (report 70), no artifact |
| D18 | Three sibling errors, no `impl From` for RejectionReason | P3 | designer-now | OPEN — `meta_reply_for_*_error` ×3 |
| D19 | Cloudflare error-fidelity collapse (downgraded) | P3 | designer-now | OPEN — `RequestFailed` collapse, low urgency |
| D20 | Three `RejectionReason` types share one name (68-3-P2-2) | P3 | designer-now | OPEN — defensible per-channel, reader tension |
| D21 | report 70 wording: "alias newtype" / paraphrased parser quote | polish | designer-now | OPEN unless report-71 fix-list applied |

## The findings

### D1 · Cloudflare daemon credential never injected by the flake wrapper [P1, designer-now]
- **Location:** `cloud/flake.nix:96-99` (the `cloud-daemon` postInstall
  wrapper) vs `cloud/src/cloudflare.rs:53` and `tests/runtime.rs:470`.
- **Current state:** OPEN. The daemon resolves the Cloudflare token via
  `EnvironmentCredentialSource::token` → `std::env::var(handle.as_str())`
  (`cloudflare.rs:51-56`). The production-shipped handle is
  `CLOUDFLARE_DNS_TOKEN` (`tests/runtime.rs:470,513`). The `cloud-daemon`
  wrapper injects only `HCLOUD_TOKEN` and `DIGITALOCEAN_ACCESS_TOKEN`
  (`flake.nix:97-98`) — `CLOUDFLARE_DNS_TOKEN` is absent, so the daemon's CF
  path returns `Error::CredentialUnavailable`. The `cloudflareCli`
  wrapper's own `CF_API_TOKEN` (`flake.nix:46`) is a *separate*,
  flarectl-subprocess-local var; it does NOT satisfy the daemon's
  `std::env::var(CLOUDFLARE_DNS_TOKEN)` resolution, and in the live flow
  `ProcessRunner::run` overrides flarectl's env with the daemon-resolved
  token anyway (`cloudflare_cli.rs:50` `.env(CF_API_TOKEN, token.as_str())`)
  — so if the daemon resolution fails, flarectl never runs. The branch
  (`88b852d`) fixed only the flarectl wrapper line 46 and the INTENT.md
  wording; it left the daemon wrapper untouched.
- **Fix shape:** Add a third `--run` line to the `cloud-daemon` wrapper
  injecting `CLOUDFLARE_DNS_TOKEN` from `gopass show -o cloudflare.com/token`
  (mirroring the HCLOUD/DIGITALOCEAN lines, with the `:-$(…)` default form).
  Small flake fix, code-backed, acceptable on the designer feature branch.
- **Citation:** `flake.nix:96-99`; `cloudflare.rs:51-56`;
  `cloudflare_cli.rs:18,50`; `tests/runtime.rs:470,513`. **High confidence.**
- **Caveat:** Whether the daemon's `EnvironmentCredentialSource` CF path is
  load-bearing in the *current* default deploy depends on whether any
  operator runs CF meta ops through the daemon socket (report 70 proved DO
  over the socket; CF-over-socket has no recorded live run). The gap is a
  certainty in code; its production blast radius is "the moment someone
  drives a CF meta op through the deployed daemon."

### D2 · Blocking provider IO inside the async daemon handler [P1, operator-bead]
- **Location:** `cloud/src/schema_daemon.rs:74-109` →
  `cloud/src/lib.rs:693-699` → `apply_plan`/`apply_digitalocean_host_plan`
  (`lib.rs:1511,1637`)/`apply_hetzner_host_plan` (`lib.rs:1578`).
- **Current state:** OPEN, re-grounded. **The daemon was re-architected
  since report 68**: the kameo `EngineActor`/`src/daemon.rs` model is gone;
  the spine is now emitted into `src/schema/daemon.rs` as an
  `ActorMultiListenerDaemon`, with cloud hand-writing only
  `impl ComponentDaemon for CloudDaemon` (`schema_daemon.rs:48`). The
  blocking substance survives intact: `handle_working_input`
  (`schema_daemon.rs:74`) and `handle_meta_connection` (`:87`) are `async fn`
  that call the *synchronous* `engine.handle_schema_ordinary_input` /
  `handle_schema_meta_input` (`lib.rs:685,693`), which dispatch to blocking
  `ureq`/`flarectl` provider IO with **no `spawn_blocking`** and **no
  per-call timeout** (the only timeout is the 10-second *request-read*
  timeout, `schema_daemon.rs:40`, not a provider-call timeout). One hung
  provider call still blocks its executor task. Report 36's hazard outlived
  both the kameo cutover and the schema-engine cutover.
- **Fix shape:** Move provider IO off the async handler onto a bounded
  blocking plane (`tokio::task::spawn_blocking` behind a permit pool +
  per-call timeout), per `actor-systems.md`. Operator code change.
- **Citation:** `schema_daemon.rs:74-109`; `lib.rs:685-699,1511,1578,1637`.
  **High confidence.**

### D3 · Wire two-tree drift + 3141-line schema_bridge straddle [P1, designer-now]
- **Location:** `signal-cloud/src/lib.rs` (hand-written public API) vs
  `signal-cloud/src/schema/lib.rs` (generated); `cloud/src/schema_bridge.rs`.
- **Current state:** OPEN. Hand-written `signal-cloud/src/lib.rs` still
  declares 38 `pub struct`/`pub enum` locally and does NOT
  `pub use crate::schema`. The drift is live: hand-written `Servers(HostQuery)`
  (`lib.rs:398`) vs generated `ObserveServers(ObserveServers)`
  (`schema/lib.rs:424,451`). `schema_bridge.rs` is 3141 lines (vs `lib.rs`
  1802) — the largest hand-written file, un-gated, carrying the
  CLI-input/daemon-reply path. The cutover named in
  `signal-cloud/ARCHITECTURE.md` has not happened.
- **Fix shape:** Replace hand-written `src/lib.rs` types with
  `pub use crate::schema::lib` re-exports, delete the duplicates, collapse
  `schema_bridge.rs`, update downstream imports. Clean pre-production break.
  Designer feature branch + falsifiable test in cloud `tests/`.
- **Citation:** `signal-cloud/src/lib.rs:398`; `schema/lib.rs:424,451`;
  `cloud/src/schema_bridge.rs` (3141 L). **High confidence.**

### D4 · Meta schema re-declares signal-cloud types [P1→PARTIAL, designer-now]
- **Location:** `meta-signal-cloud/schema/lib.schema:101-105`;
  `meta-signal-cloud/Cargo.toml:28`.
- **Current state:** PARTIALLY MOVED. Since report 68, `meta-signal-cloud`
  *Cargo.toml* gained a `signal-cloud` git dependency (`:28`) — the
  cross-crate Rust import the finding asked for exists at crate level. But
  the *schema* (`lib.schema`) still redeclares `Provider` (`:101`),
  `Capability` (`:102`), `ProviderAccount` (`:103`), `DomainName` (`:105`),
  `RecordKind`, `DomainNameSystemRecord` as fresh local types — no `import`
  line. So the schema-level duplication 68-3-P1-2 named persists; only the
  Rust-dependency half advanced. Whether `ProviderProjection` was deleted is
  unverified this pass.
- **Fix shape:** Import the signal-cloud schema types into the meta schema
  (the `cloud/sema.schema` cross-crate import precedent), delete the
  redeclarations and any surviving `ProviderProjection` bridge. Designer
  branch.
- **Citation:** `meta-signal-cloud/schema/lib.schema:101-105`;
  `Cargo.toml:28`. **Medium confidence** (schema redeclaration confirmed;
  ProviderProjection deletion status not re-checked).

### D5 · Hetzner ships in no binary [P1, designer-now + psyche]
- **Location:** `cloud/src/lib.rs` (`#[cfg(feature="hetzner")]` throughout:
  `:38,126,546,1578…`); `cloud/flake.nix:123-130` (no hetzner package).
- **Current state:** OPEN. `apply_hetzner_host_plan` (`lib.rs:1578`) and all
  Hetzner code are `#[cfg(feature="hetzner")]`-gated; the flake ships only
  `packages.default` (cloudflare) and `packages.digitalocean`
  (`digitalocean,cloudflare`) — no `--features hetzner` build anywhere, no
  `tests/hetzner_live.rs`. Hetzner's apply path is dead code in every
  shipped binary. The cloud INTENT.md "Hetzner first" framing was corrected
  to DigitalOcean-lead on the branch (`hcp8`), so the *intent* contradiction
  is resolved; the *build* gap (no hetzner package at all) is the residue.
- **Fix shape:** Either add `packages.hetzner` + `tests/hetzner_live.rs`
  (make the deferred lead real), or accept Hetzner stays deferred behind DO
  per `hcp8`. The DO-lead supersession is captured; the remaining call is
  whether Hetzner gets a buildable package now — a psyche/scope decision.
  The flake-package half is a designer-branch sketch once decided.
- **Citation:** `lib.rs:38,1578`; `flake.nix:123-130`. **High confidence.**

### D6 · Default `apps.daemon` is DNS-only [P1, designer-now + psyche]
- **Location:** `cloud/flake.nix:189-191` (`apps.daemon`→`packages.default`)
  + `:123-124` (`default` = no extra features → `cloudflare` only).
- **Current state:** OPEN. `nix run .#daemon` builds the cloudflare-only
  default, which answers `NotBuilt` to both compute providers; compute is
  reachable only via `apps.daemon-digitalocean` (`flake.nix:194-197`). Build
  and intent disagree silently.
- **Fix shape:** Point `apps.daemon`/`apps.default` at the compute-capable
  build, OR confirm DNS-only-by-default is deliberate. The flake repoint is
  a designer-branch sketch; the posture choice is a psyche question.
- **Citation:** `flake.nix:123-124,189-191,194-197`. **High confidence.**

### D7 · ad53 CloudNode platform half absent [P1, operator-bead + designer-now stance]
- **Location:** `horizon-rs/.../species.rs:13-30` (`NodeSpecies` ends at
  `TestVm`); CriomOS (no nixos-generators/image-format/CloudNode).
- **Current state:** OPEN. `NodeSpecies` (`species.rs:13`) ends at `TestVm`
  (`:30`) — no `CloudNode`. No `BehavesAs`/`TypeIs` facet, no CriomOS gate
  module, no `nixos-generators` input or image-format output anywhere in
  horizon-rs/CriomOS (grep: zero hits for `nixos-generators|image-format|
  CloudNode|qcow2`). The "boot a baked CriomOS image" milestone cannot
  start, and no cloud-repo build depends on it, so the gap is invisible from
  the cloud lane.
- **Fix shape:** Operator-bead for the build (3 horizon-rs edits mirroring
  `TestVm` + 1 CriomOS gate module + a new nixos-generators image-format
  attr: qcow2 for DO, raw for Hetzner). Designer-now writes the CloudNode
  stance into `CriomOS/INTENT.md` + `horizon-rs/INTENT.md` so the cross-repo
  dependency is discoverable.
- **Citation:** `horizon-rs/.../species.rs:13-30`; CriomOS grep (0 hits).
  **High confidence.**

### D8 · report 71 §4 + 5-synthesis deploy-leg staleness [P2, designer-now]
- **Location:** `reports/cloud-designer/71-…/4-lojix-cloud-integration.md:18,
  119-120,242`; `5-synthesis.md:162`.
- **Current state:** OPEN. Both mermaids and prose show the lojix deploy leg
  as `nix copy --to ssh-ng://root@<node>.<cluster>.criome`. Report 150
  (`reports/system-designer/150-…build-on-target…`) establishes lojix moved
  to build-on-target: `nix build --eval-store auto --store ssh-ng://…
  <attr>^*` realizes the closure ON the target, then activates — precisely
  to keep large closures off the daemon host. The report-71 diagram predates
  that and now mis-describes the deploy mechanism.
- **Fix shape:** Update the report-71 deploy-leg legs (and any spec in
  report-72 synthesis) to build-on-target: replace `nix copy --to ssh-ng://`
  with the `nix build --eval-store auto --store ssh-ng://… ^*` realize-on-
  target + activate sequence. Designer report edit.
- **Citation:** `71/4-lojix-cloud-integration.md:18,242`; `71/5-synthesis.md:162`;
  `reports/system-designer/150-…:19,25-27`. **High confidence.**

### D9 · active-repositories.md:91 stale daemon description [P2, designer-now]
- **Location:** `protocols/active-repositories.md:91`.
- **Current state:** OPEN, doubly wrong now. It calls cloud's daemon a
  "single `EngineActor` over a synchronous sema-engine `Store`." Both legs
  are stale: (a) the daemon is no longer a kameo `EngineActor` — it's an
  emitted `ActorMultiListenerDaemon` (`schema_daemon.rs:5`); (b) the live
  runtime is the plain provider `Store`, NOT a sema-engine store
  (`schema_daemon.rs:66` builds `Arc::new(Store::new())`; the SchemaStore
  pilot is unreachable — see D12). It also still frames the DO live proof as
  "via an `#[ignore]` adapter test … no reproducible artifact," which
  predates report 70's actual socket-spine live run.
- **Fix shape:** Rewrite line 91 to the emitted-multi-listener-daemon +
  provider-`Store` reality, reference report 70's live socket-spine run, and
  keep the honest "no committed re-runnable artifact" (D17). Designer edit.
- **Citation:** `active-repositories.md:91`; `schema_daemon.rs:5,66`.
  **High confidence.**

### D10 · ARCHITECTURE.md 5-actor/no-block + sema pilot unreconciled [P2, designer-now]
- **Location:** `cloud/ARCHITECTURE.md:3-4,32-41`.
- **Current state:** OPEN. The branch (`88b852d`) touched only
  INTENT.md/README.md/flake.nix; ARCHITECTURE.md was never reconciled. It
  still opens "Its first target is Cloudflare DNS records" (`:3-4`) and the
  "Actor Shape" section (`:32-41`) still prescribes one-actor-per-concern
  (`CloudflareProvider`/`PlanStore`/`PolicyStore`/`RateLimitGate`/
  `RemoteOperationTracker`) plus "Provider calls must not block the
  listener" — both contradicted by the shipped single-engine
  emitted-daemon-over-`Arc<Store>` with blocking IO (D2). The doc *does* now
  carry an accurate "Schema-engine upgrade track" section describing the
  emitted spine, so it is internally inconsistent rather than uniformly
  stale.
- **Fix shape:** Reconcile the "Actor Shape" + opening to the real
  emitted-`ActorMultiListenerDaemon`-over-`Arc<Store>` shape (or mark the
  5-actor section explicitly aspirational and tie it to D2's blocking-plane
  fix). Designer-branch ARCHITECTURE.md draft.
- **Citation:** `cloud/ARCHITECTURE.md:3-4,32-41,93-160`. **High confidence.**

### D11 · Config encoder has no NOTA / deploy-stack home [P2, designer-now]
- **Location:** `cloud/examples/write_config.rs:30,39-50`.
- **Current state:** OPEN. The encoder is still an `examples/` target taking
  3 positional args (`<out.rkyv> <ordinary.sock> <meta.sock>`, `:30`) and
  hardcoding `DaemonConfiguration { … }` in Rust (`:40`); it parses zero
  NOTA. No `[[bin]]`/`apps.*` home, no NOTA `DaemonConfiguration` authoring
  file — the override's "encode typed NOTA into binary" pipeline does not
  exist.
- **Fix shape:** Re-home to a deploy-stack `bin`/nix app consuming a NOTA
  `DaemonConfiguration` file. Designer-branch sketch.
- **Citation:** `examples/write_config.rs:30,39-50`. **High confidence.**

### D12 · sema-engine pilot dead weight; two state machines [P2, designer-now + psyche]
- **Location:** `cloud/src/schema_daemon.rs:66-68`; `cloud/src/lib.rs:43-44`
  (`schema_runtime`, `schema_store` modules).
- **Current state:** OPEN. `build_runtime` builds `Arc::new(Store::new())`
  (`schema_daemon.rs:67`), NOT `SchemaStore`; the `SchemaRuntime`/`SchemaStore`
  pilot (`schema_runtime.rs`, `schema_store.rs`, still public modules at
  `lib.rs:43-44`) is constructed only in tests, rejects `PreparePlan`, and
  applies nothing. Two divergent state machines stand, one unreachable —
  contradicting the no-back-compat posture.
- **Fix shape:** Decide cut-vs-promote (psyche question), then reconcile
  ARCHITECTURE.md (D10). If cut, delete the pilot modules; if promoted, the
  702/4 directory-TCB question goes live. Designer-branch + psyche.
- **Citation:** `schema_daemon.rs:66-68`; `lib.rs:43-44`. **High confidence.**

### D13 · Compute adapters near-byte mirrors; no shared REST client [P2, designer-now]
- **Location:** `cloud/src/digitalocean.rs:118-128,274,337`;
  `cloud/src/hetzner.rs:103-105`; `cloud/Cargo.toml:30` (`google-cloud = []`).
- **Current state:** OPEN. `digitalocean.rs` and `hetzner.rs` each carry
  their own `trait Api`, `struct HttpApi`, and `create_server`/`create_host`
  with byte-identical plumbing differing only in REST path/envelope/key
  resolution. The owning noun (a shared compute-provider REST client) is
  missing, and `google-cloud = []` (`Cargo.toml:30`) is poised to triple the
  copy.
- **Fix shape:** Invent the shared compute-provider REST client before
  `google-cloud` lands; fold in D18. Designer-branch + falsifiable test.
- **Citation:** `digitalocean.rs:118,128,274`; `hetzner.rs:103`;
  `Cargo.toml:30`. **High confidence.**

### D14 · `ensure_ssh_key` never called on create path [P2, operator-bead]
- **Location:** `cloud/src/lib.rs:1658-1664` (DO create);
  `cloud/src/digitalocean.rs:248`/`hetzner.rs:228` (`ensure_ssh_key` defs).
- **Current state:** OPEN. `apply_digitalocean_host_plan` sets
  `ssh_keys: vec![plan.ssh_key_name…]` directly into `ServerSpec`
  (`lib.rs:1662`) with no `ensure_ssh_key` call first; the only production-
  adjacent caller of `ensure_ssh_key` is `tests/digitalocean_live.rs:38`. DO
  silently creates an unreachable droplet if the key name is unregistered;
  Hetzner 422-fails — opposite failure modes on one condition.
- **Fix shape:** Call `ensure_ssh_key` (or validate key presence and reject
  loudly + uniformly across DO/Hetzner) on the create path. Operator code.
- **Citation:** `lib.rs:1658-1664`; `digitalocean.rs:248`;
  `digitalocean_live.rs:38`. **High confidence.**

### D15 · CredentialHandle = unvalidated wire-string-as-getenv [P2, designer-now + psyche]
- **Location:** `meta-signal-cloud/src/lib.rs:30-42`; `cloudflare.rs:53`.
- **Current state:** OPEN. `CredentialHandle(String)` has only `new`/`as_str`
  (`meta-signal-cloud/src/lib.rs:30-42`); the wire-supplied string is used
  directly as an env-var name in `std::env::var(handle.as_str())`
  (`cloudflare.rs:53`), unsealed, gated only by the meta socket `0o600` mode.
- **Fix shape:** Validate/seal credential resolution rather than
  wire-string-as-getenv — a deliberate custody decision (psyche question 5
  in report 68). Designer-branch + psyche.
- **Citation:** `meta-signal-cloud/src/lib.rs:30-42`; `cloudflare.rs:53`.
  **High confidence.**

### D16 · ImageName unvalidated stringly newtype [P2, designer-now]
- **Location:** `meta-signal-cloud/src/lib.rs:148-158`; minted at
  `cloud/src/lib.rs:1326` (per report 68).
- **Current state:** OPEN. `ImageName(String)` has only `new`/`as_str`
  (`meta-signal-cloud/src/lib.rs:148-158`), no `TryFrom`/parse; empty string
  is a valid `ImageName`. Garbage fails at the provider API, not the wire
  edge.
- **Fix shape:** Add `TryFrom`/parse rejecting empty/whitespace, or split
  slug-vs-numeric-id forms. Designer-branch + falsifiable test.
- **Citation:** `meta-signal-cloud/src/lib.rs:148-158`. **High confidence.**

### D17 · No committed socket-apply test (P1-b artifact axis) [P2, operator-bead]
- **Location:** `cloud/tests/runtime.rs:292` (capability read only);
  `cloud/tests/digitalocean_live.rs:29` (`#[ignore]`, drives `HttpApi`
  directly); `cloud/flake.nix:155-161` (`--ignored --list` runs nothing).
- **Current state:** OPEN on the artifact axis. Report 70 proved the
  register→prepare→approve→apply→observe→destroy lifecycle over the real
  sockets against live DO (droplet 578873541) — but **manually**; no
  committed, re-runnable test drives `ApplyPlan` over the spine. The one
  committed spawned-daemon test answers a capability read only
  (`runtime.rs:292`); the only Nix check `--ignored --list`s the live test
  and executes nothing.
- **Fix shape:** Add a committed socket-apply lifecycle test (gated/mocked
  for CI, with a live-`#[ignore]` variant). Operator code; the falsifiable-
  test shell can be sketched in cloud `tests/` by designer.
- **Citation:** `tests/runtime.rs:292`; `tests/digitalocean_live.rs:29`;
  `flake.nix:155-161`. **High confidence.**

### D18 · Three sibling errors, no `impl From` for RejectionReason [P3, designer-now]
- **Location:** `cloud/src/lib.rs:1530,1621,1680`.
- **Current state:** OPEN. Three near-identical hand-written
  `meta_reply_for_cloudflare_error` / `_hetzner_error` / `_digitalocean_error`
  matchers; `impl From<…Error> for RejectionReason` is the right
  remediation. Folds into D13.
- **Citation:** `lib.rs:1530,1621,1680`. **High confidence.**

### D19 · Cloudflare error-fidelity collapse [P3, designer-now]
- **Location:** `cloud/src/cloudflare.rs` (error mapping).
- **Current state:** OPEN (downgraded by report 68's verify pass). Cloudflare
  collapses `ureq` errors to `RequestFailed`; the "unreachable/aspirational"
  framing was struck (`ZoneNotFound` is reachable, the meta arm is
  constructed in production). Only a P3 fidelity cleanup remains.
- **Citation:** report 68 `7-adversarial-verification.md:30`;
  `cloudflare.rs:12-27`. **Medium confidence** (not re-traced line-by-line
  this pass; carried from the downgrade verdict).

### D20 · Three `RejectionReason` types share one name [P3, designer-now]
- **Location:** ordinary/meta/sema schemas (per report 68 68-3-P2-2).
- **Current state:** OPEN. Distinct `pub enum RejectionReason` per channel
  (meta one confirmed at `meta-signal-cloud/src/schema/lib.rs:244`).
  Defensible per-channel; a reader-confusion tension, not a defect.
- **Fix shape:** Distinct names, or document the overload. Designer.
- **Citation:** `meta-signal-cloud/src/schema/lib.rs:244`; report 68
  `7-adversarial-verification.md:34`. **Medium confidence.**

### D21 · report 70 wording blemishes [polish, designer-now]
- **Location:** `reports/cloud-designer/70-tier2-daemon-spine-proven.md:83,86`.
- **Current state:** OPEN unless the report-71 §"Fix list" rows were applied.
  Report 70 labels `HostPlanPreparation` "an alias newtype over
  `DesiredHostState`" — it is a single-field struct
  (`meta-signal-cloud/src/lib.rs`); and paraphrases the parser error vs the
  codec's verbatim "expected … to hold {n} root **objects**, found {n}".
- **Fix shape:** Apply report-71's two P3 wording corrections. Designer
  report edit.
- **Citation:** `70-…:83,86`; report 71 `5-synthesis.md:80-81`. **High
  confidence.**

## What is NOT relisted (closed / superseded, for the reader's trust)

- **Report 66 `.com` gopass fix (DO):** landed at `7f190c3`
  (`flake.nix:71` reads `digitalocean.com/api-token`). Closed.
- **CF flarectl-wrapper gopass path:** corrected on the branch
  (`flake.nix:46` → `cloudflare.com/token`, commit `88b852d`). Closed — but
  note D1 is a *different* gap (the daemon wrapper, lines 96-99, not 46).
- **cloud INTENT.md Hetzner-first framing + CF handle wording:** corrected
  on the branch (`c92718e`, `88b852d`). The cloud-INTENT.md half is closed;
  the *flake daemon wrapper* (D1) and *active-repositories* (D9) residues
  stay open.
- **P1-b behavioral axis (apply over the socket):** proven live by report 70.
  Only the *artifact* axis (D17) remains.
- **68-4-F1/F3/F4, F3-image, P2-cloudflare-fidelity "unreachable" framing:**
  refuted/downgraded by report 68's verify pass; not relisted as risks (D19
  carries only the surviving P3 fidelity residue).
