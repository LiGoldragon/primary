# Aged bead refresh — 2026-06-19

## Scope

The psyche asked to sort open beads by age and reword the really old ones with fresh intent after firsthand investigation.

I sorted the remaining open BEADS queue by `created_at` and investigated the oldest work directly in the relevant current repos/reports. I refreshed wording through the 2026-05-17 block and closed only items whose original implementation target is now clearly shipped or superseded.

Age-sorted export: `/tmp/open-beads-age-sorted-20260619.tsv`.

Open count after this pass: 110.

## Closed during this age-refresh pass

| Work | Reason |
|---|---|
| Kameo lore reference | `lore/rust/kameo.md` exists, alongside primary `skills/kameo.md` and `kameo-testing` examples. |
| horizon-rs nota-codec pin | horizon-rs no longer depends on `nota-codec` / `nota-derive`; it uses `nota-next`. |
| CriomOS nix module split | `modules/nixos/nix/{client,builder,cache,retention-agent}.nix` exists; remaining container work is a separate bead. |
| lojix crate split / signal-lojix skeleton | Current `lojix` daemon crate, CLI, and `signal-lojix` / `meta-signal-lojix` contracts exist; remaining cutover is tracked elsewhere. |
| criome Spartan BLS substrate | Current criome is the BLS auth substrate with `blst`, `signal-criome`, Kameo actors, `criome.sema`, admission, policy, and tests; remaining work is narrower. |
| lojix `deployment_{n}` identifier | Current lojix derives typed deployment identifiers from durable state; no `format!("deployment_{n}")` pattern remains. |

## Reworded / refreshed oldest open work

| Created | Refreshed work | Fresh intent |
|---|---|---|
| 2026-05-08 | lore boundary audit | Audit current doc boundaries and stale path/shim references; lore now intentionally keeps upstream/tool references while primary skills keep workspace discipline. |
| 2026-05-09 | chronos Phase 1 | Existing scaffold is present; implement `Sky` DE440/anise/solar TODOs and the `Subscribe` stream stub. |
| 2026-05-09 | Whisrs feature gaps | First repair missing `whisrs/INTENT.md`, then express prompt/vocabulary/history/retention/copy/search as durable `RecordingSession` features. |
| 2026-05-09 | horizon-rs serde cleanup | Remove serde from proposal-only input nouns while preserving JSON projection/output boundary derives. |
| 2026-05-10 | cluster registry | Choose the separate long-lived publication registry/trust-distribution component; do not put cluster-side registry behavior into clavifaber. |
| 2026-05-10 | clavifaber tests | Decide whether Prometheus e2e is still needed now that rootless bwrap and pki lifecycle tests exist; reuse the CriomOS-test-cluster runner if needed. |
| 2026-05-11 | Yggdrasil ownership | Wire clavifaber `YggdrasilKeypairSetup` into `complex-init`; make network/yggdrasil consume the resulting keypair instead of seeding it. |
| 2026-05-11 | SSH host identity decision | Current architecture says sshd owns SSH host key and clavifaber reads `.pub`; remaining work is stale-doc cleanup, if any. |
| 2026-05-11 | overlay roles | Decide the current Headscale/Tailscale/Yggdrasil role policy from the live modules, not a generic review. |
| 2026-05-11 | cluster mismatch handling | Keep lojix/lojix-cli read-only until a real cluster registry/trust runtime exists; do not revive automatic key-material repair yet. |
| 2026-05-12 | container-host | Add `mkCriomOSNode` / container-host now that the Nix role split is done. |
| 2026-05-12 | GC-root retention | Implement GC-root symlink materialization in lojix daemon durable state; CriomOS's current retention-agent is only Nix keep-option policy. |
| 2026-05-12 | Ghost publication node | Wait for generic container-host substrate before Ghost packaging/service work. |
| 2026-05-12 | DNS/tailnet runtime smoke | Use existing VM/nspawn suite to add booted DNS/tailnet assertions; do not add another runner scaffold. |
| 2026-05-12 | negative Horizon fixtures | Add fixtures only after production Horizon exposes the missing diagnostics/fields. |
| 2026-05-12 | Prometheus artifacts | Persist runner artifacts outside mktemp sandboxes or copy them back to the caller. |
| 2026-05-12 | Wi-Fi PKI fixtures | Add synthetic ClaviFaber certificate artifacts after publication planes are wired through CriomOS. |
| 2026-05-15 | CriomOS metal split | Split the still-large `modules/nixos/metal/default.nix` by hardware concern. |
| 2026-05-15 | CriomOS-home unused-input check | Add a cheap generic source-shape check for stale flake inputs/module references. |
| 2026-05-17 | large-AI model materialization | Move heavyweight model downloads/materialization to the large-AI node and keep normal system closure lighter. |
| 2026-05-17 | Whisrs durable-first epic | First add repo intent/architecture, then implement durable audio-first capture/history/retry. |
| 2026-05-17 | criome routed authorization | Finish real policy lookup, meta approval, master-key signing, and Lojix real-client witness; coordinator skeleton exists. |
| 2026-05-17 | tui-criome | Build long-running `meta-signal-criome` client only after encrypted meta session and one-shot meta CLI are established. |

## Left for the next age pass

The next oldest bead is the 2026-05-18 Horizon rewrite. I did not refresh it in this pass because `system-designer` currently owns the live lojix/signal-lojix migration claim, and that bead appears entangled with active design work. The next pass should continue from 2026-05-18 onward, respecting active repo claims.
