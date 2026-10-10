# Receipt — evidence for the Psyche Opus and Psyche Sonnet recovery plan

Gathered read-only by a subflow of 8904b1 on 2026-09-26. No state changed.
Method: offline reads of `flows/` records and persisted native transcripts under
`~/.claude/projects/`; live read-only queries `herdr agent list`, `herdr session list`,
`hm-list`, `flow 'List.{}'`, `flow-next 'List.{}'`, `systemctl --user list-units`.
No session was resumed; no message was sent.

## Psyche Opus

- Last seat: **93ba9f**, `PsycheV2.{ Opus 93ba9f }`, model `claude-opus-5-5`, effort medium.
  Launched 2026-09-26 by e167d8 through flow-next 0.17; brief
  `/home/li/wt/primary/56ae53/flows/e167d8/reports/opus-successor-of-e167d8-launch.md` (d0f050a9).
- Chain: 88475f → e167d8 → 93ba9f. e167d8 is crossover/closed (its own log's last line).
- Native session: `93ba9ff6-d24a-4dd0-a5c7-f98fab5ca9de`
  `/home/li/.claude/projects/-home-li-primary/93ba9ff6-d24a-4dd0-a5c7-f98fab5ca9de.jsonl`
  3,182,521 bytes, 1901 lines, last write 2026-09-26 15:36 local (last `turn_duration`
  timestamp `2026-09-26T21:36:02.221Z`, messageCount 968).
  Context estimate from the final assistant `usage`: `cache_read_input_tokens` 375,024
  + `cache_creation_input_tokens` 495 ≈ **375.5k tokens** — above the ~200k line.
  Harness version recorded: 2.1.280; cwd `/home/li/primary`.
- Records on disk (all present):
  - `flows/93ba9f/log.md` (38 lines)
  - `flows/93ba9f/reports/` — audit-whats-what.md, books-compared.md, flow-0171-proof.md,
    flow-gate-fixture.md, jev-and-openrouter.md, letter-anatomy-2.md, opus-design-book.md,
    opus-primitive-message.md, roles-anatomy-2.md, word-identifiers-research.md
  - `flows/93ba9f/vision/` — automation, callerIdentity, datomVocabulary, ethosNames,
    fableRole, fieldTool, flowLaunching, jev, meaningLanguage, messagingInterface,
    mindRoles, presentation, primarySeats, psycheSharing, sessionClosing, wordIdentifiers
  - `flows/93ba9f/notion/semaCommunication.md`
  - **No `flows/93ba9f/summary.md`** (e167d8 has one: `flows/e167d8/summary.md`).
  - Predecessor material: `flows/e167d8/summary.md`, `flows/e167d8/log.md`,
    `flows/e167d8/reports/`, `flows/e167d8/vision/`, `flows/e167d8/witnesses/`.
- Artifacts published by 93ba9f (links only, not fetched): design book
  `P1PUozuFzS5kMNPgYEMA5q`; primitive-Message prototype `Qz8dpKBzJfbQgAbdUmfZCe`.
  Fable counterparts: `4aaZsqHKN19SLUxk1UHwjE`, `Dkzn57DKYhMyYc8GiKjRTP`.
  e167d8 final presentation book `https://claude.ai/artifact/9gfqFYs3H6yCs9vsPzLyov`.
- Route now: `flow-next 'List.{}'` returns exactly three rows — 93ba9f, b7ba00, e167d8 —
  all `Claude`, all agent-transport `Unavailable`, all Herdr-located in session
  `messaging-build`, state `Active`. 93ba9f row: agent name `claude-51c8e0d33c45a2f18801e089`,
  pane `w1H:p1`, terminal `term_65c661b2cab519d`, origin `{ e167d8 … opus-successor-of-e167d8 }`.
  `herdr session list`: `messaging-build` is **stopped**; only `default` runs. So the
  flow-next row is a stale registry record, not a live route.
- `hm-list`: `93ba9f  psychev2-opus-93ba9f  messaging-build  STALE`.
- `herdr agent list` (live): no Opus pane. Panes present in `default`: w1:p1 codex,
  w1:p2 mind-astra-6fe957, w1:p3 field-luna-19ff9f, w1:p7 field-luna-184bd8,
  w1:p8 psyche_fable_b7ba00 (session 8904b10d-7f06-4e44-9342-3a8a2d7e17bd, this flow),
  w1:p9 field-sol-9ac67c. Stable `flow 'List.{}'` also shows 22e12b field-astra (w1:pA).
- Recovery attempts in flight: **none for Opus**. `flows/56ae53/` contains only
  `fable-recovery/` (files listed below) and an empty `field-recovery-launch/`.
  The only `psyche-opus-native` launcher state files are historical, in `flows/753e69/`
  (and `flows/03e825/psyche-ultra-*`), predating this recovery.

## Psyche Sonnet

- Last seat: **9c7514**, `PsycheV2.{ Sonnet 9c7514 }`, model `claude-sonnet-5`,
  launched 2026-09-25 over Herdr by Psyche Medium e51411 (pane `wD:pW`, tab `wD:tK`,
  terminal `term_65c55829fcb1088`) as the living's side-channel companion.
  Never registered in Flow (`flows/88475f/handover.md`: "not on Flow").
- It did **not** die in the power failure: it was deliberately closed and its route
  retired in the 2026-09-26 Herdr cleanup ordered by e167d8 —
  `flows/e167d8/reports/herdr-cleanup-2026-09-26.md` ("9c7514 (wD:pW, the Sonnet companion)")
  and `flows/e167d8/witnesses/herdr-cleanup-records-2026-09-26.md`
  ("companion Psyche Sonnet 9c7514 (claude-sonnet-5 low), pane titled 'Psyche Opus 077114', idle").
- Native session: `9c7514c1-9da9-48b9-b5af-025c4f38f468`
  `/home/li/.claude/projects/-home-li-primary/9c7514c1-9da9-48b9-b5af-025c4f38f468.jsonl`
  602,527 bytes, 273 lines. Final `usage`: cache_read 95,476 + cache_creation 2,713
  ≈ **98k tokens** — below the ~200k line.
- **No `flows/9c7514/` directory exists.** No log, summary, report or vision of its own.
- Charter and role records that do exist:
  - `flows/e51411/vision/psycheSonnet.md` — the living's words defining the seat.
  - `flows/e51411/vision/launch.md` — "The default effort is medium"; "'Low' is a power,
    not an effort … Low corresponds with Sonnet."
  - `flows/e51411/handover.md` line 17, `flows/88475f/handover.md` line 18.
  - `flows/e51411/reports/field-split-proposal.md` line 27 — binding `claude-sonnet-5`.
  - `flows/f38926/log.md` line 153 (2026-09-20) — Psyche Sonnet = claude-sonnet-5;
    "no role-specific manifest file exists for Psyche seats".
  - Title-storage hazard: `flows/88475f/witnesses/b87854-retirement-2026-09-25.md`,
    `flows/38de5b/receipts/flow-launch-findings.md` — b87854 and 9c7514 shared title storage.
- Earlier, unrelated Sonnet lineage (2026-09-17 era, not the current seat):
  `flows/79715b/` ("primary Psyche sonnet", session
  `79715bc6-6ceb-4513-8185-a293fbf3dcac`, 1,877,819 bytes), and `3f2a43` named in
  `flows/108ab0/handoff.md` line 115 with no flow directory.
- Route now: no Sonnet row in `hm-list`, in `flow 'List.{}'`, in `flow-next 'List.{}'`,
  or in `herdr agent list`.
- Recovery attempts in flight: **none**.

## Deployment of the newer pair (live witness)

`systemctl --user`: `flow-nexus.service` (stable) running; `flow-nexus-next.service` running;
`flow-configuration-next.service` active/exited; `message-nexus-next.service` running;
`message-daemon.service` running.
Client versions: `/home/li/.local/bin/flow-next` → `/nix/store/9gf2j799wgxbp0vw6fidg9898mbxpz1p-flow-0.17.0/bin/flow`,
reports `flow 0.17.0`; `message-next` reports `0.17.0`; stable `flow` reports `0.12.2`.
Note: `flows/56ae53/fable-recovery/predecessor-handoff.md` speaks of **Flow 0.17.1**;
the installed next client is **0.17.0**. 0.17.1 (`ac216c89`) and 0.17.2 exist only on
branch `s1-e167d8` per `flows/93ba9f/log.md`.
Both next-pair Nexuses answered a query, so the services are live; no Start or Bind was
attempted, so the Start/Bind path itself is **not** witnessed as working post-failure.
8904b1 (this Fable) is bound in **stable** Flow (`default` session, w1:p8), not in flow-next.

## Fable recovery packet (for comparison / reuse)

`/home/li/wt/primary/56ae53/flows/56ae53/fable-recovery/` —
`README.md`, `predecessor-handoff.md`, `launch-manifest.json`, `profile.json`,
`state.json`, `state-recovery-v2.json`, `log-snapshot-pre-156b517b.md`,
`receipts/{psyche_fable_b7ba00.manifest.json, psyche_fable_b7ba00.v2.manifest.json,
psyche_fable_b7ba00.v2.first-prompt.md (34,369 bytes), psyche_fable_b7ba00.v2.native-bootstrap.json,
psyche_fable_b7ba00.v2.send-guard.json, invalid-first-prompt-b7ed066b.json,
native-marker-relocation-8904b1.json}`, `main-flow-hook-state/`.
Launcher: `node tools/native-batch-refresh.mjs start --manifest … --state …`.
Profile source hashes (sha256), from `profile.json`:
- `flows/56ae53/fable-recovery/predecessor-handoff.md` 1ac7572402b48c8dda2cd0895940b550a58894ba3d3868cc5217924fa7f02f80
- `flows/b7ba00/receipts/readiness-announce.md` a3253d14c56f7aa4997f60098b59aed41f2444577ba5aa6041242fbefcfc25b9
- `flows/b7ba00/vision/modelFlows.md` 5339c9c724df45da9323314c075d14ccef1fc55d7636cc1a569578c0cb3ca6c5
- `flows/56ae53/fable-recovery/log-snapshot-pre-156b517b.md` 8c85b86cd9c0e5083cc0ba169dff4b6e68c7d073e378983492d4e12f653af046
- `flows/56ae53/vision/model-flow-emergency.md` e7041b49c9fde37c3b4a8d1729bb2ea403acbd528b7fb2aef39033b1421c2cce

## Role templates

`SKILL_VARIABLES.md` carries only `Psyche medium Claude model: claude-opus-4-6[1m]` and
its no-million-context twin. There is no role template for Psyche Opus, Fable or Sonnet;
e167d8's summary open question 2 proposes adding them and is unanswered.

## Sources

- `flows/93ba9f/log.md`, `flows/93ba9f/reports/`, `flows/93ba9f/vision/primarySeats.md`
- `flows/e167d8/log.md`, `flows/e167d8/summary.md`,
  `flows/e167d8/reports/herdr-cleanup-2026-09-26.md`,
  `flows/e167d8/witnesses/herdr-cleanup-records-2026-09-26.md`
- `flows/b7ba00/log.md`, `flows/b7ba00/vision/modelFlows.md`, `flows/b7ba00/reports/`
- `flows/e51411/vision/psycheSonnet.md`, `flows/e51411/vision/launch.md`,
  `flows/e51411/handover.md`, `flows/e51411/reports/field-split-proposal.md`
- `flows/88475f/handover.md`, `flows/88475f/witnesses/b87854-retirement-2026-09-25.md`
- `flows/38de5b/receipts/flow-launch-findings.md`, `flows/f38926/log.md`,
  `flows/79715b/log.md`, `flows/108ab0/handoff.md`
- `flows/56ae53/log.md`, `flows/56ae53/vision/model-flow-emergency.md`,
  `flows/56ae53/fable-recovery/*`
- Live: `herdr agent list`, `herdr session list`, `hm-list`, `flow 'List.{}'`,
  `flow-next 'List.{}'`, `systemctl --user list-units`, `flow-next`/`message-next` version output
- Transcripts: `~/.claude/projects/-home-li-primary/93ba9ff6-….jsonl`,
  `…/9c7514c1-….jsonl`, `…/e167d857-….jsonl`, `…/b7ba0089-….jsonl`
