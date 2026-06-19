# 68 — cloud engine audit (frame and method)

Orchestrator frame for the cloud-lane deep audit the psyche requested:
*"investigate issues that touch your project and get me real explanations
with visuals and questions."* This is the cloud-designer successor to the
prime designer's report 702 (the engine-stack deep analysis), **scoped to
the cloud triad and its neighbourhood** — the surface 702's completeness
critic explicitly named as *"the single most-changed unaudited daemon …
+1199 DigitalOcean Phase 1 … a new sema-engine `Store` consumer, took the
kameo fork. Zero coverage."* 702 audited the stack and left cloud dark;
this closes that gap on the same method.

It also builds on the earlier cloud audits in this lane — `35-actor-divergence-forensics`,
`36-cloud-actor-audit`, `37-cloud-component-schema-triad-port` — and does
not redo them.

## What is already grounded (so the lanes go deep, not wide)

Established inline before fan-out:

| Fact | Evidence |
|---|---|
| Triad HEADs, all = `origin/main`, no drift | cloud `7f190c3`, signal-cloud `4e846bc`, meta-signal-cloud `54d62be` |
| cloud is in the kameo **fork** camp (the 702 split-brain) | `cloud/Cargo.toml:59-60` `[patch.crates-io] kameo = fork`; lock resolves `f491b45d`; triad-runtime pinned `f46f66e` (declares stock) |
| Report 66 P0 is **already done** | `7f190c3 cloud: read DigitalOcean token from domain gopass path` is on `origin/main`; `flake.nix:71` reads `digitalocean.com/api-token` |
| The `ad53` image home (CriomOS CloudNode profile) **does not exist yet** | only `CriomOS/modules/nixos/test-vm-guest.nix` (the TestVm pattern); no CloudNode species in `horizon-rs/lib/src/species.rs` |
| cloud has a `checks = {}` flake block | `cloud/flake.nix:132` — possibly a nix witness the 702 fleet lacks; the runtime lane confirms what it builds |
| cloud carries **no** local `ComponentKind` copy | grep of signal-cloud/meta-signal-cloud schema empty — one 702-class divergence cloud avoids |
| `protocols/active-repositories.md:91` is **stale** | still calls cloud "Documentation-only at birth"; three provider adapters + the synchronous Store path have since shipped |

## Scope — the cloud neighbourhood in five lanes

1. **Daemon + Store path** (`cloud` daemon, `schema_daemon`/`runtime`/
   `store`/`bridge`, the synchronous blocking-`ureq` Store) — invariants,
   the sema-engine `FamilyDirectory` trust-boundary question 702/4 raised,
   soundness-vs-surface (does the daemon provision, or only tests?),
   Tier-2 readiness, actor-vs-serial shape.
2. **Provider adapters** (`digitalocean.rs`/`hetzner.rs`/`cloudflare.rs`) —
   the `Provider` abstraction, feature gating, the `Api` traits, typed
   errors/newtypes, credential sourcing, which providers are live-proven
   (DO Tier-1 green, report 64) vs surface-only, and cross-adapter
   duplication.
3. **Wire contracts** (`signal-cloud` + `meta-signal-cloud`) — schema
   discipline, the typed domain newtypes, `@generated` freshness,
   ComponentKind (confirm no local copy), the codegen-tier findings
   applied to cloud's generated surface (panic-on-bad-name, newtype-impl
   ergonomics), and whether `image_name` is plumbed end-to-end.
4. **Runtime / fleet / nix** — the kameo-fork exposure and Tier-2 actor
   risk, the fleet-fix bead omission (702 named 5 daemons; cloud is a 6th
   fork-taker), the `checks={}` witness, the DO package variant, the
   one-rkyv-arg daemon discipline (and the missing config encoder, report
   64 §3.1), two-deploy-stack placement.
5. **Image home (ad53) + doc freshness** — the CloudNode-profile gap
   against the TestVm template, the per-provider image pipeline, and
   whether `cloud/INTENT.md`/`ARCHITECTURE.md` and `active-repositories.md`
   reflect DO Phase-1 + the 3-provider abstraction + ad53. This lane also
   surfaces the context-maintenance items.

## Method (702 template, scoped)

- **Phase 1 — per-lane deep analysis.** One agent per lane, reads the
  repo's `INTENT.md` first, then architecture/source/recent commits/prior
  cloud reports, applies the AGENTS.md hard overrides as audit criteria
  (Rust discipline, component-triad/daemon discipline, NOTA positional
  records, no pre-production back-compat). Every claim cites `file:line`
  and states what the **production path** does, not what a test can do.
  Each writes its numbered report with at least one mermaid visual.
- **Phase 2 — adversarial verification.** An independent skeptic tries to
  **refute** every P1/P2 finding against the code; a finding not grounded
  in `file:line` on the production path is Downgraded. Verdict ledger →
  `7-adversarial-verification.md`.
- **Phase 3 — completeness critic + synthesis.** A critic names the cloud
  surface the lanes missed (`6-completeness.md`); the synthesis folds
  **Confirmed-only** findings into a whole-cloud narrative with visuals,
  ranked risks, psyche questions, and beads (`8-synthesis.md`).

## Governing intent (the cloud neighbourhood)

`ad53` (Decision, Medium — cloud-node OS images live in CriomOS as a
CloudNode-species profile; the daemon references the image by id through
the existing HostPlan `image_name`). The component-triad and one-argument
daemon overrides (binary-only startup, no flags, never parse NOTA). The
two-deploy-stack discipline and no-pre-production-back-compat. Report 66
(the cloud-operator handoff, bead `primary-hpkj`) and the
`primary-kbmi` cloud/domain-criome runtime-daemon bead are the live
operator tracks this audit reconciles against.

## Layout

| File | Lane |
|---|---|
| `1-daemon-and-store.md` | daemon + synchronous Store path + sema consumer |
| `2-provider-adapters.md` | DigitalOcean / Hetzner / Cloudflare adapters |
| `3-wire-contracts.md` | signal-cloud + meta-signal-cloud |
| `4-runtime-fleet-nix.md` | kameo fork, fleet, nix checks, daemon discipline |
| `5-image-home-and-docs.md` | ad53 CloudNode gap + doc/intent freshness |
| `6-completeness.md` | what the lanes missed |
| `7-adversarial-verification.md` | the refutation verdicts |
| `8-synthesis.md` | whole-cloud narrative + ranked risks + questions + beads |
