# 13 · Pi local Gemma + API key — execution and open decisions (2026-05-29)

Execution of the report-12 handoff after the psyche said **"implement"**.
New session; the prior (buggy) cloud-designer session had already
implemented ~90% of report 12 in the `CriomOS-home` working tree but
left it **uncommitted** with one broken piece. This report is the
takeover + execution log + the decisions now waiting on the psyche.

## Design decision resolved — canonical provider = `criomos-local`

report 12's "Main design choice" (which of `criomos-local` /
`prometheus` / `criomos-largeai`). **Resolved: `criomos-local`.** It is
the source default in `pi-models.nix`, it names the property the user
selects on (local / self-hosted vs cloud), and it does not leak a
hostname like `prometheus` (which lies if the largeAI node changes).
The legacy `prometheus` and `criomos-largeai` providers were NOT pruned
(the WIP gave all three the same command-backed auth as a safe
transition); full collapse-to-one is a follow-up, not load-bearing now.

## What the prior session had staged (uncommitted WIP)

Six modified files in the `CriomOS-home` working copy, implementing the
whole report-12 plan, split by me into two coherent halves:

- **Core fix** (`pi-models.nix` + `checks/pi-harness-profile`): a
  command-backed gopass key in `~/.pi/agent/auth.json`
  (`!gopass show -o goldragon.criome/local-llm-api-token`) so Pi stops
  sending `sk-no-key-required`; Gemma read from the criomos-lib
  inventory; default switched to local Gemma.
- **Version bumps** (`flake.nix`, `flake.lock`, `packages/pi`,
  `vscodium`): pi 0.76→0.77, claude-code 2.1.153→2.1.156. Left broken at
  `npmDepsHash = pkgs.lib.fakeHash`.

Pi's auth mechanism was verified against its own `docs/providers.md`:
the `"!command"` form is real (executes, caches stdout for process
life), and `auth.json` outranks the `models.json` key, so the
command-backed entry wins. hexis `mkManagedConfig` uses RFC-7396
merge-patch with per-pointer modes; `"always"` on `/criomos-local`
forces our entry while leaving the user's subscription creds untouched.

## Landed (CriomOS-home main)

1. `8aa75035` — core fix (pi-models.nix + check). Validated by the
   pi-harness-profile check (built locally; the prometheus remote
   builder is currently unreachable). Activated on ouranos.
2. `36f5de89` — `nix flake update criomos-lib` (ec851e52 → de676a8e, the
   verified Gemma rev = criomos-lib `origin/main` HEAD). I had wrongly
   split the criomos-lib bump into the deferred version-bump commit, so
   the first activation fixed auth but showed no Gemma; this corrects it.
   Re-activated.

Two activations were `lojix-cli (HomeOnly goldragon ouranos li … Activate
None None)` pinned to the exact pushed rev, built locally (builder
`None`).

## Verified

| Check | Result |
|---|---|
| `auth.json` `criomos-local.key` | `!gopass show -o goldragon.criome/local-llm-api-token` (command, not a literal token) |
| gopass key retrievable here | yes — 64 bytes (gpg unlocked; blind length check, value never read) |
| `auth.json` permissions | `0600` preserved (hexis did not loosen) |
| subscription creds (`openai-codex`) | intact (ensure-mode left undeclared entries alone) |
| Gemma in `criomos-local` | `gemma-4-31b`, `gemma-4-26b-a4b` present (11 models total) |
| `settings.json` defaults | `defaultProvider=criomos-local`, `defaultModel=gemma-4-26b-a4b`, `defaultThinkingLevel=off` |
| **live 200 auth call** | **BLOCKED** — see connectivity below |

So the 401's root cause is fixed in config: Pi will send the real token
the moment it can reach the endpoint. The end-to-end 200 confirmation
could not be made from ouranos right now.

## The blocker — prometheus is unreachable from ouranos right now

`ping prometheus.goldragon.criome` fails; `GET :11434/v1/models`
(no auth) returns HTTP 000; the nix remote builder + binary cache to
prometheus also time out. Multiple independent paths fail, so this is
network / prometheus state, not the Pi config. Most likely the in-flight
backup-net / gen-46 deploy on prometheus (report 12 noted gen 46 staged
for the `criome-backup` SSID rename). Consequence: I cannot confirm the
live 200, **and the now-default local Gemma is unreachable until
prometheus is back** — opening Pi right now would default to a backend
that cannot connect.

## Open decisions (waiting on the psyche)

1. **Default model while prometheus is down.** The WIP switched Pi's
   default from `openai-codex`/`gpt-5.5` to local `gemma-4-26b-a4b`. With
   prometheus unreachable, that default fails to connect. Keep the Gemma
   default (fine if prometheus is back imminently), or flip the default
   back to `openai-codex` for a working interim default (Gemma stays
   selectable either way)? Captured intent (record 1195) says
   "selectable," not "default."
2. **Phase B — pi 0.77 + claude 2.1.156.** Staged on a sibling change
   with the real `npmDepsHash`
   (`sha256-X0qMLqAi5pgrtTw5+DfSPsgIEngUnHwGxqYE6PL8NJU=`). Ready to
   land. Held because pi is the daily driver and a 0.76→0.77 bump is a
   behaviour change — proceed?
3. **codex-cli / llm-agents.** report 12 flagged updates available; the
   WIP did not touch them. Bump too, or leave?

## Deferred (with reason)

- **Multimodal `input` for Gemma.** Pi declares `input=["text"]`; the
  models carry an `mmproj` projector so `["text","image"]` is possible.
  Held: server-side vision is runtime-unverified (report 9 §2) and
  prometheus is down, so declaring image input now risks a broken UX
  (user sends an image → error). Add once server-side vision is
  confirmed.

## Anchors

- CriomOS-home main `36f5de89` (criomos-lib/Gemma) on `8aa75035` (core
  fix). Phase B sibling change `zolxzytlqzzs` (pi 0.77 + claude).
- `modules/home/profiles/min/pi-models.nix`; Pi auth:
  `…/coding-agent/docs/providers.md`; hexis `nix/wrap.nix` +
  `ARCHITECTURE.md`.
- Intent: records 1195 (local agents use local Gemma — selectable),
  1196 (command-backed key via standard profile path, no plaintext),
  1011/1012 (never expose a secret), 1023 (full-multimodal deploy).
- Prior: report 12 (handoff), report 9 (vision unverified), report 8
  (deploy safety).
