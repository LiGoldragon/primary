# 71·1 — Self-audit: re-verifying report 68's Confirmed findings at HEAD 3b38cdd

An adversarial re-check of report 68's standing (Confirmed P1/P2) findings
against the *current* cloud tree (`3b38cdd`) and the pinned contracts
(signal-cloud `4e846bc`, meta-signal-cloud `54d62be` — both unchanged since
the audit's fan-out pin). The new fact in play is report 70: the Tier-2
daemon-socket lifecycle was driven live (droplet `578873541` created,
observed by the daemon, destroyed — every leg over the real sockets). The
question this report answers is what report 70 *actually closes* versus what
still stands, and whether report 68 graded each structural claim correctly.

All line citations re-checked against `3b38cdd`; the audit's lane reports
cited `7f190c3`/`3b38cdd` interchangeably (one-commit drift), so a few
numbers shifted by a line — noted where they did.

## The headline re-grade

Report 68 was, on the structural findings, **accurate and not overstated** —
every still-checkable structural claim reproduces at HEAD on the production
path. The two findings the prompt singles out (P1-b and risk #1) are the only
ones report 70 touches, and they move from "stands" to **partially closed**:
one axis (does the assembled spine provision a node?) is now *witnessed*; the
other axis (is there a *reproducible built artifact* — a CI/committed test —
that re-proves it?) is **still open**. Report 70's witness is a manual,
narrated run, not a committed socket-apply test; nothing in the repo at
`3b38cdd` drives an `ApplyPlan` over a spawned-daemon socket.

## P1-b / risk #1 — re-grade: PARTIALLY CLOSED (split the axis)

Report 68 framed these as two faces of one gap:
- **risk #1** = "no provider has a *built-artifact* witness of a live mutation."
- **P1-b** = "no *apply* crosses the daemon socket" (the ledger's corrected,
  narrowed form of the runtime lane's over-broad "no lifecycle test").

Report 70 proved the **live-behavior axis**: a create→observe→destroy
lifecycle ran over the real ordinary+meta sockets of a booted DO+Cloudflare
daemon against live DigitalOcean (report 70, "The witness"). The production
apply path it exercised is real and reachable: `apply_digitalocean_host_plan`
(`src/lib.rs:1637-1677`) calls `digitalocean.create_host`/`destroy_host_by_name`,
reached via `apply_host_plan`'s `#[cfg(feature = "digitalocean")]` arm
(`src/lib.rs:1569-1570`), shipped in `packages.digitalocean` (`flake.nix:125-129`).
So "the spine can apply a real mutation over the socket" is no longer a claim —
it is witnessed. **P1-b's behavioral substance is closed.**

The **artifact axis is not closed**:
- The only committed test that spawns the real `cloud-daemon` binary,
  `daemon_process_starts_from_binary_configuration_and_answers_working_request`
  (`tests/runtime.rs:292`), connects the *ordinary* socket (`runtime.rs:306-308`)
  and answers a **capability/working read** — it drives no `ApplyPlan` and no
  provider mutation over the socket. The `handle_meta_request` calls elsewhere
  in that file (`runtime.rs:211,230`) are **in-process against `Store`**, not
  over a spawned-daemon socket.
- The DO live test, `digitalocean_full_lifecycle_runs_against_the_real_api`
  (`tests/digitalocean_live.rs:29`), is `#[ignore]` ("live: spends real
  DigitalOcean money", `digitalocean_live.rs:28`) **and drives
  `digitalocean::HttpApi` directly** (`digitalocean_live.rs:33`) — it never
  crosses the socket. The only Nix *check* referencing it,
  `digitalocean-live-test-compiles` (`flake.nix:155-161`), still runs
  `--ignored --list` — it lists the test and runs nothing. The nix *app*
  `apps.digitalocean-live-test` (`flake.nix:199-202`) does run it, but an app
  is operator-invoked, not a CI check.
- Report 70's own witness was produced **manually**: its boot recipe is hand
  `cargo run --example write_config` + hand `cloud`/`meta-cloud` NOTA calls
  (report 70, "The working socket protocol"). It is a narrated run, not a
  committed/CI artifact that re-runs.

**Verdict.** P1-b: **partially closed** — the behavioral gap ("no apply over
the socket") is closed by report 70; the structural gap ("no committed
socket-apply test") still stands. Risk #1: **partially closed** — a live
mutation is now *witnessed* for DigitalOcean; a *reproducible built-artifact
witness* still does not exist (Cloudflare, the only default-built provider,
still has no live test; Hetzner has neither). Report 68 graded both correctly
*at its time*; they are now **stale in the favorable direction** for the
behavioral axis and **still-standing** for the artifact axis. The honest
post-70 phrasing: "DigitalOcean spine-witnessed-once-manually; no provider has
a re-runnable artifact."

## Still-standing structural claims — re-verified at HEAD

### Single-EngineActor blocking shape (P2-a) — STANDS, report 68 got it right
One `EngineActor` owns the whole engine (`src/schema/daemon.rs:239-241`,
`type Engine = Arc<Store>` at `schema_daemon.rs:54`). Both tiers route to the
**same** `ActorRef`: `handle_working_connection` and `handle_meta_connection`
each call `self.engine.ask(...)` on the one `engine: ActorRef<EngineActor>`
(`schema/daemon.rs:340,352`, field at `:299`). A single mailbox therefore
serialises working *and* meta requests. The handlers are `async fn handle`
but call synchronous `&self` methods (`handle_working_input` →
`handle_schema_ordinary_input`, `schema_daemon.rs:74-80`) that run **blocking
`ureq`** provider IO with **no `spawn_blocking`** anywhere in `src/` (the only
`spawn_blocking` token in the tree is a *comment* about a future deferral,
`hetzner.rs:10`) and **no per-provider-call timeout** (the one timeout,
`REQUEST_READ_TIMEOUT` at `schema_daemon.rs:40,92`, guards the socket *read*,
not the provider call). So one hung provider call blocks the actor task and
stalls both sockets — exactly P2-a. Report 70 confirms behaviorally: "this
lifecycle held one socket for the full duration of each blocking provider
call" (report 70, "What this changes"). **Report 68: correct, not overstated.**

### sema-engine "dead pilot" (P2-b) — STANDS, correct
`build_runtime` constructs `Arc<Store>` (the legacy provider store),
**not** `SchemaStore`/`SchemaRuntime` (`src/schema_daemon.rs:66-68`).
`SchemaRuntime`/`SchemaStore` are constructed only by their own
`impl`s in `src/schema_runtime.rs` and in `tests/` (no production caller).
The pilot rejects host preparation —
`PrepareHostPlan`/`PrepareHostDestruction` → `ProviderNotConfigured`
(`schema_runtime.rs:168-171`) and `PreparePlan`/`PrepareProjection` →
`PlanGenerationFailed` (`schema_runtime.rs:331-335`) — and applies nothing.
Two divergent state machines stand, one unreachable. **Report 68: correct.**

### Wire two-tree drift (68-3-P1-1/-P1-2) — STANDS, correct, contracts unchanged
Both contract repos are at the audit's pinned HEADs (signal-cloud `4e846bc`,
meta-signal-cloud `54d62be`), so nothing has regenerated. The hand-written
public tree still diverges from the generated tree by the exact fields the
audit named: `signal-cloud/src/lib.rs:237` `pub state` vs generated
`schema/lib.rs:277` `pub capability_state`; `lib.rs:316` `pub zone` vs
generated `:300` `pub domain_name`; hand-written `Servers(HostQuery)`
(`lib.rs:398`) vs generated `ObserveServers(ObserveServers)`
(`schema/lib.rs:424`). The generated tree IS freshness-gated
(`signal-cloud/build.rs:31` "checked-in … artifacts are fresh"); the
hand-written `src/lib.rs` is **not**. The silent wire break is real and
recorded: signal-cloud `0ff53ff` ("the prior regeneration silently broke the
Observation wire contract"). For -P1-2: the meta **schema** redeclares
`Provider`/`ProviderAccount`/`DomainName`/etc. as fresh locals
(`meta-signal-cloud/schema/lib.schema:33-72`) and its `build.rs` wires no
signal-cloud schema dependency into codegen
(`meta-signal-cloud/build.rs:23-27` — own crate_root only), forcing the
`ProviderProjection` bridge (`cloud/src/schema_store.rs:32`, used at
`schema_runtime.rs:351,372,451`). The `schema_bridge.rs` straddle is still the
largest file in the repo (107 KB / 3141 lines vs lib.rs 65 KB).
Minor nuance: meta-signal-cloud's *Cargo.toml* does declare a `signal-cloud`
dependency (`Cargo.toml:28`) — but the missing import is at the **schema
codegen** layer, which is what -P1-2 actually claimed; the finding stands.
Report 70 independently re-confirms the drift biting (the CLI must drive the
hand-written `Servers`, not the schema's `ObserveServers`). **Correct.**

### Hetzner-unshipped (P1-hetzner) — STANDS, correct
`provider_is_built(Hetzner) = cfg!(feature="hetzner")` (`src/lib.rs:1756`);
`apply_hetzner_host_plan` and its dispatch arm are both
`#[cfg(feature = "hetzner")]` (`src/lib.rs:1577,1567`). No `--features
hetzner` build exists anywhere in `flake.nix` (packages are only `default`
and `digitalocean`; checks/apps never enable hetzner). So the Hetzner apply
path is dead code in every shipped binary, while `INTENT.md` still names
Hetzner the lead. Default daemon corollary also stands: `default =
["cloudflare"]` (`Cargo.toml:27`); `apps.daemon`/`apps.default` point at
`packages.default` (`flake.nix:189-191,184-187`) which builds default
features only — so `nix run .#daemon` answers `NotBuilt` to both compute
providers; compute is reachable only via `apps.daemon-digitalocean`
(`flake.nix:194-197`). **Correct.**

## Lower-severity Confirmed still-checkable — spot re-verified

- **F2 — `ImageName` unvalidated** STANDS: `ImageName(String)` with only
  `new`/`as_str` (`meta-signal-cloud/src/lib.rs:148`), and production mints
  `ImageName::new("")` (`cloud/src/lib.rs:1326`). Correct.
- **`google-cloud` empty stub** STANDS: `google-cloud = []` (`Cargo.toml:30`)
  — the copy-tripling risk the compute-dedup finding names is real.
- **kameo fork on the prod path (68-4-F2)** STANDS structurally:
  `[patch.crates-io] kameo = {git = …LiGoldragon/kameo…}` (`Cargo.toml:59-60`)
  still force-overrides onto the only provisioning spine. (Fleet-size count
  not re-walked this pass.)

## What changed vs report 68, in one line each

- **P1-b / risk #1** — was "stands"; now **partially closed**: behavior
  witnessed (report 70), artifact still absent. Report 68 was right for its
  time; the behavioral half is now stale-favorable.
- **P2-a, P2-b, 68-3-P1-1/-2, P1-hetzner, P1-default-daemon, F2** — all
  **still stand verbatim** at `3b38cdd`; report 68 graded each correctly and
  none is overstated. Report 70 explicitly leaves these standing ("the
  remaining 68 risks stand").

## The one framing correction for downstream readers

`protocols/active-repositories.md:91` and any prose calling cloud a
"live-proven daemon spine" should now read **"DigitalOcean spine witnessed
live once (manual run, report 70); no re-runnable artifact yet."** Report
70's own closing line already draws this boundary: proving the spine "does
not make the daemon's architecture sound, it makes it usable for testing
today." The blocking-actor reshape (P2-a) is, post-70, the top structural
item — the live run held one socket for each blocking provider call.
