# 5 · Adversarial verification — the hanging-bug ledger under refutation

cloud-designer, session 72. Each Lane-D finding (`4-hanging-bugs-ledger.md`)
was handed to an independent skeptic told to assume it was already fixed or
misframed, and to open the cited `file:line` in current source (cloud main
`3b38cdd` and the `cloud-designer-intent-refresh` worktree `88b852d`). The
skeptic returned `still_open`, a corrected severity/lane, and the `file:line`
it actually read. **21 findings, 20 confirmed open, 1 already fixed.** Four
findings carried framing errors the refutation corrected — the point of the
pass. The corrected severities/lanes feed `6-synthesis.md`'s fix ledger.

## Verdict ledger

| ID | Open | Sev | Lane | What the refutation found |
|---|---|---|---|---|
| D1 | ✓ | P1 | designer-now | CF token reaches the daemon by no name — `flake.nix:96-99` injects only HCLOUD + DIGITALOCEAN; the daemon `getenv`s the registered handle (`cloudflare.rs:51-56`) and `CF_API_TOKEN` is a *separate* flarectl-subprocess var that the daemon-resolved token overrides anyway. Holds regardless of handle name. |
| D2 | ✓ | P1 | operator-bead | Blocking provider IO confirmed on the only production path: one engine actor mailbox → sync `engine.handle_*` → bare `ureq .call()` with no `spawn_blocking`, no per-call timeout. Violates `actor-systems.md:235`. |
| D3 | ✓ | P1 | designer-now | Two-tree drift real + current + on the live path: `signal-cloud/src/lib.rs` declares 38 types and never re-exports `crate::schema`; the un-gated 3141-line `schema_bridge.rs` hand-maps them; `ObserveServers` vs hand-written `Servers` structurally diverge. |
| D4 | ✓ | P2 | designer-now | Schema half confirmed: `meta-signal-cloud/schema/lib.schema:1` is an empty `{}` import block, so `Provider`/`Capability`/`DomainName` are redeclared instead of imported from signal-cloud via the cross-crate form. |
| D5 | ✓ | **P2** (was P1) | designer-now | **Framing corrected:** Hetzner unshipped is real but P1 overstated — `hcp8` made DO lead, so a missing Hetzner *binary* is residue of a resolved decision, not a P1 gap. |
| D6 | ✓ | P1 | designer-now | `apps.default`/`apps.daemon` build default features (cloudflare-only); host requests to that binary return `RequestUnsupported{CapabilityNotCompiled}`. Whether DNS-only-default is deliberate is the psyche's call. |
| D7 | ✓ | P1 | operator-bead | **Critical-path blocker** confirmed at the source: `NodeSpecies` ends at `TestVm` (`horizon-rs/lib/src/species.rs:30`); zero hits for `CloudNode`/`nixos-generators`/`qcow2`/`image-format` across horizon-rs + CriomOS. No snapshot id exists to provision. |
| D8 | ✓ | P2 | designer-now | Report 71 §4:18-19,242 + 5-synthesis:160-163 show `nix copy --to ssh-ng://`; lojix is build-on-target (report 150). **Fixed this session.** |
| D9 | ✓ | P2 | designer-now | `active-repositories.md:91` "single `EngineActor` over a synchronous sema-engine `Store`" is stale vs the emitted `ActorMultiListenerDaemon`/`Arc<Store>`. **Fixed this session.** |
| D10 | ✓ | P2 | designer-now | `cloud/ARCHITECTURE.md:32-41` names 5 actors that don't exist + "must not block the ordinary listener" — contradicted by the shipped single blocking-IO engine. **Fixed this session** (marked shipped/divergence/target). |
| D11 | ✓ | P2 | designer-now | Config encoder is an `examples/` target with 3 hardcoded args, parses no NOTA — re-home to a deploy-stack bin consuming a NOTA `DaemonConfiguration`. |
| D12 | ✓ | P2 | designer-now | `schema_runtime.rs`/`SchemaStore` pilot unreachable from the daemon (`build_runtime` → `Arc<Store>`, not `SchemaStore`); cut-vs-promote pending. **Doc side noted this session** in ARCHITECTURE.md. |
| D13 | ✓ | P2 | designer-now | DO/Hetzner adapters are near-byte mirrors (own `trait Api`/`HttpApi`/`get`/`post`/`delete`); invent a shared compute-provider REST noun before `google-cloud` triples it. |
| D14 | ✓ | P2 | operator-bead | `ensure_ssh_key` never called on create; an unregistered `ssh_key_name` makes DO a **silent keyless droplet** and Hetzner a 422 — opposite failure modes on one precondition. |
| D15 | ✓ | P2 | designer-now | `CredentialHandle(String)` infallible `From<String>`, used verbatim as a `getenv` name in both cloudflare.rs:53 and hetzner.rs:69-77 — validate-vs-seal is a custody decision. |
| D16 | ✓ | **P3** (was P2) | designer-now | **Framing corrected — fix is harmful as written:** `ImageName::new("")` is *deliberately* minted for Destroy plans (`lib.rs:1313-1316`); a naive empty-reject `TryFrom` would break it. Downgraded to polish; garbage fails at the provider, not the wire edge. |
| D17 | ✓ | P2 | operator-bead | **Scope narrowed:** committed `ApplyPlan` tests exist but are all **in-process with mocked `Api`**; no committed test drives apply **over the daemon sockets** (socket tests stop at meta registration → `CredentialHandleUnknown`). The artifact axis of audit-68 P1-b. |
| D18 | ✓ | P3 | designer-now | Three near-identical `meta_reply_for_*_error` matchers, no `impl From<…Error> for RejectionReason`; folds into D13. |
| D19 | ✓ | P3 | designer-now | Cloudflare collapses every `ureq` class into `Error::RequestFailed`; split by Status (404→ZoneNotFound, 401/403→credential, 429→rate-limit). |
| D20 | ✓ | P3 | designer-now | Three distinct `RejectionReason` enums share one name across the triad schemas — distinct names or documented overload (no runtime collision). |
| D21 | ✗ | — | — | **Already fixed** in `d9df93f5` (report 70:83,86 self-audit wording). Dropped from the ledger. |

## What the refutation pass bought

Four corrections a single-pass audit would have shipped wrong:

- **D5 P1→P2** — "Hetzner ships in no binary" read as a P1 gap; it is the
  residue of an already-made decision (`hcp8` DO-lead), not an open hole.
- **D16 P2→P3, and the fix reversed** — the "validate `ImageName` non-empty"
  fix would have **broken** Destroy-plan minting, which deliberately uses an
  empty `ImageName`. The skeptic caught that the naive fix is a regression.
- **D17 scope narrowed** — not "no ApplyPlan test" (there are several,
  in-process/mocked) but specifically "no apply **over the sockets**." The
  precise gap is the committed re-runnable socket-lifecycle artifact.
- **D6 wording** — `apps.daemon` points at `packages.default` (cloudflare-only
  features), confirmed by reading the flake outputs, not assumed.

This is why findings are verified before they become beads: three of the four
corrections change either the severity or the *direction* of the fix.
