# 68 — adversarial verification: the refutation verdicts

The skeptic pass over every P1/P2 finding from the five lanes. Rule (as in
report 702's verify lane): a finding a skeptic could not ground in
`file:line` on the **production** path is **Downgraded** or **Refuted**, and
a walked-back finding does **not** reappear as a standing risk in
`8-synthesis.md`. This file is the single place that records *why* each
finding survived or fell.

23 P1/P2 findings adjudicated: **18 Confirmed** (incl. Confirmed-scoped),
**5 walked back** (1 Downgraded, 4 Refuted). The verify agents ran against
the live HEAD, which advanced to `3b38cdd` mid-audit (one commit past the
`7f190c3` fan-out pin) — so several reasons cite the newer revision and note
the one-commit drift.

## The verdict ledger

| Finding | Sev | Verdict | Load-bearing reason |
|---|---|---|---|
| `P1-a` no built rkyv config encoder | P1 | **Confirmed** (superseded) | True at `7f190c3` (only test callers); but `3b38cdd` adds `examples/write_config.rs` — the encoder now exists, so the live finding is the *sharper* `68-4-F5` (encoder has no deploy-stack home), not "no encoder". |
| `P1-b` no live end-to-end daemon-socket lifecycle | P1 | **Confirmed** (scoped by completeness) | DO live test drives `HttpApi` directly (`digitalocean_live.rs:33`); the socket-driven daemon tests observe capabilities / route a rejected registration — no **apply** crosses the socket. (Completeness note: a binary-from-rkyv lifecycle test *does* exist at `runtime.rs:291`; it serves a capability request but never provisions — so the gap is "no apply over the spine," not "no daemon test".) |
| `P2-a` actor is an elaborate Mutex; blocking IO in the handle | P2 | **Confirmed** | Single `EngineActor` (`daemon.rs:305`), both tiers ask one `ActorRef` (`:340/352`), meta handler calls blocking `ureq`/`flarectl` (`lib.rs:1594`) with zero `spawn_blocking` and no provider-call timeout — one hung provider stalls both sockets. Report 36's hazard survived the kameo cutover. |
| `P2-b` sema-engine pilot is dead weight on the live path | P2 | **Confirmed** | `build_runtime` builds `Arc<Store>` not `SchemaStore` (`schema_daemon.rs:67`); `SchemaRuntime`/`SchemaStore` constructed only in `tests/`; the pilot rejects `PreparePlan` and applies nothing. Dead-by-design Phase-1 experiment, but two divergent state machines stand. |
| `P2-c` ARCHITECTURE.md documents a daemon that does not run | P2 | **Confirmed** | `ARCHITECTURE.md:32-38` mandates 5 concern-actors + `:40-41` a no-block rule; code runs 1 actor and blocks the listener with `ureq` on the default `cloudflare` build. |
| `P1-hetzner-surface-only` Hetzner is intent's lead but unshipped | P1 | **Confirmed** | `provider_is_built(Hetzner)=cfg!(feature="hetzner")` (`lib.rs:1752-1758`); no flake package/check enables `--features hetzner`; `apply_hetzner_host_plan` unreachable in every shipped binary. Build and intent (`INTENT.md:18` "Hetzner first") disagree silently. |
| `P1-default-daemon-cloudflare-only` `nix run .#daemon` is DNS-only | P1 | **Confirmed** | `apps.daemon`→`packages.default`/`bin/cloud-daemon`; `Cargo.toml:27` default `[cloudflare]`; routing answers `NotBuilt` for both compute providers. The compute daemon is reachable only via `apps.daemon-digitalocean`. |
| `P2-compute-adapter-duplication` DO/Hetzner adapters are near-byte mirrors | P2 | **Confirmed** | `hetzner.rs`/`digitalocean.rs` share byte-identical `HttpApi` plumbing + `ProviderClient`, differing only in REST path/envelope/key-resolution; both wired via `production()`, no `#[cfg(test)]` gate. The owning noun (a shared compute-provider REST client) is missing. |
| `P2-create-never-registers-ssh-key` | P2 | **Confirmed-scoped** | `ensure_ssh_key` has zero production callers; DO `create_server` silently drops an unmatched key → unreachable droplet reported as success; Hetzner passes the name → 422. Opposite failure modes on one condition. (Scoped: the path is reachable but only on a misconfigured key.) |
| `P2-three-sibling-errors-no-impl-from` | P2 | **Confirmed-scoped** | Three near-identical hand-written `meta_reply_for_*_error` matchers (`lib.rs:1530/1621/1680`); `impl From` is the right remediation. (Scoped: only cloudflare+digitalocean reach a shipped package.) |
| `P2-cloudflare-error-fidelity` collapses statuses, arm aspirational | P2 | **Downgraded** | Cloudflare *does* collapse `ureq` errors to `RequestFailed` (`cloudflare.rs:147…`), but `ZoneNotFound` is **not** unreachable and `lib.rs:1535` is **not** aspirational — it is constructed on the production path (`lib.rs:1044/1068`). Fidelity tension is real; the "unreachable/aspirational" overstatement is struck. |
| `68-3-P1-1` two divergent type trees; hand-written API un-gated | P1 | **Confirmed** | Hand-written `src/lib.rs` (public API, what downstream imports) has drifted from `schema/lib.schema` (`state` vs `capability_state`, `name` vs `domain_name`, struct vs tuple, `Servers` vs `ObserveServers`); the daemon frames generated bytes but runs logic in the hand-written tree. One silent wire break already shipped (`0ff53ff`). |
| `68-3-P1-2` meta re-declares signal-cloud types instead of importing | P1 | **Confirmed** | meta `lib.schema:101-108` redeclares 7 types as fresh locals though signal-cloud exports them; `cloud/sema.schema:30-32` proves cross-crate import works; meta `build.rs` wires zero dependencies, forcing the `ProviderProjection` bridge. |
| `68-3-P2-1` newtype ergonomics live on the wrong (never-exported) tree | P2 | **Confirmed** | Public `DomainName` has only `new`/`as_str`; the `@generated` `DomainName` carries `Display`/`AsRef`/`From`/`PartialEq`, but `schema/mod.rs` is bare `pub mod lib`, so consumers of `CloudHost.name` cannot `to_string()` it. |
| `68-3-P2-2` three `RejectionReason` types share one name | P2 | **Confirmed** | Distinct production `pub enum`s in ordinary / meta / sema schema, each a different variant set. Defensible per-channel; a reader-confusion tension, not a defect. |
| `68-4-F2` triad-runtime pinned against a kameo it never declared | P1 | **Confirmed** | `Cargo.lock` pins triad-runtime `f46f66e` (declares stock kameo 0.20, no patch); cloud force-overrides kameo to the fork via its own `[patch.crates-io]`; cloud trails triad-runtime's own fork adoption (`60e0ed7`). The fork camp is **≥24 repos** — far larger than 702's "5+cloud" or report 67's "~15". |
| `68-4-F5` config encoder exists but has no deploy-stack home | P2 | **Confirmed** | `write_config.rs` is an auto-discovered `examples/` target (not `[[bin]]`/app), takes 3 positional args, hardcodes the shape in Rust, parses **zero** NOTA — the override's "encode typed NOTA into binary" pipeline does not exist. |
| `F1` (image) ad53 platform half entirely unbuilt | P1 | **Confirmed** | `species.rs:30` ends at `TestVm` (no `CloudNode`); no facet, no CriomOS gate module, no `nixos-generators` input / image-format output anywhere in horizon-rs+CriomOS. The milestone cannot start, and no cloud-repo build depends on it, so the gap is invisible from the cloud lane. |
| `F2` (image) `ImageName` is an unvalidated stringly newtype | P2 | **Confirmed** | `meta-signal-cloud/src/lib.rs:148-158` — `ImageName(String)` with only `new`/`as_str`; production mints `ImageName::new("")` (`lib.rs:1326`); garbage fails at the provider API, not the wire edge. |
| `68-4-F1` every read/create runs on the fork inside the mailbox; no lifecycle test | P1 | **Refuted** | `tests/schema_daemon.rs` and `runtime.rs:292` are non-ignored lifecycle tests that spawn the real daemon binary through the `EngineActor` mailbox and drive real ordinary reads + meta ops. The "no lifecycle test" limb is false; the blocking-actor substance is kept under `P2-a`. |
| `68-4-F3` default daemon is DNS-only and cannot provision any compute | P1 | **Refuted** | `flake.nix:125-129` ships `packages.digitalocean` (`--features digitalocean,cloudflare`) and `apps.daemon-digitalocean`, where `provider_is_built(DigitalOcean)=true` and `apply_digitalocean_host_plan` calls the real production client. A compute-capable daemon *is* shipped (just not the default). |
| `68-4-F4` the `checks={}` block never witnesses the daemon serving | P2 | **Refuted** | `checks.test` runs `cargoTest` over `runtime.rs`, whose non-ignored test spawns the real `cloud-daemon` binary from an rkyv config and asserts it serves a working capability request — so the check *does* witness the daemon serving (it just does not provision). cloud is genuinely ahead of the 702 fleet here. |
| `F3` (image) ARCHITECTURE.md is misleading | P1 | **Refuted** | The doc is explicitly **prescriptive** ("the first daemon *should* use one actor per concern") and two sections ("Current Implementation Slice", "Schema-engine upgrade track") openly disclose the `Arc<Store>` synchronous slice — stale/aspirational, not misleading. The doc-vs-code reconciliation survives as `P2-c`. |

## What the verify pass walked back (struck from standing risks)

The five below do **not** appear as risks in `8-synthesis.md`:

- **`68-4-F1`, `68-4-F3`, `68-4-F4` (Refuted).** The runtime lane's most
  alarming claims — "no daemon lifecycle test," "default daemon cannot
  provision anything," "the nix check never witnesses serving" — are all
  false. A binary-from-rkyv lifecycle test exists, a DigitalOcean compute
  daemon *is* shipped (as `apps.daemon-digitalocean`), and `checks.test`
  spawns the real daemon and asserts it serves. The honest residue is
  narrower and survives elsewhere: no apply *over the socket* (`P1-b`), the
  default app is DNS-only (`P1-default-daemon-cloudflare-only`), and the
  check witnesses *serving* but not *provisioning* (risk 1).
- **`F3` (Refuted).** cloud/ARCHITECTURE.md is prescriptive and
  self-disclosing, not misleading; the genuine doc-vs-code gap is `P2-c`.
- **`P2-cloudflare-error-fidelity` (Downgraded).** The error-mapping
  fidelity tension is real, but `ZoneNotFound` is reachable and the meta
  arm is constructed in production — the "unreachable/aspirational"
  framing is struck; only a P3 fidelity cleanup remains.

The net: the runtime lane over-reached (3 of its 5 P1/P2 claims refuted),
which is itself a finding — **cloud's nix/test witnesses are stronger than a
first read suggests, and stronger than the rest of the 702 fleet.** The
surviving risks are structural, not "it doesn't build/serve."
