# Flow da88cf — Psyche Fable, overnight integration of 2026-09-25/26

Successor of 38de5b, launched by Psyche Opus 88475f on the living's order; reported to 88475f, then e167d8. Crossover-only once the successor Fable is ready (go sent ~02:20 host time).

## What the living asked
Verbatim in vision/: prometheus.md (Prometheus found powered off and started; all building moved to Prometheus; Nix builds for everything; local fallback only when remote fails), clusterData.md (fix the Tailscale problem following cluster topology, roles and features; Fable's judgment), daisyChain.md (test the daisy chain once deployed without hotfixes; keep running new code with Claude subworkers; recovered words on the LAN chain and joining Prometheus's Wi-Fi), garbageCollecting.md (start garbage collecting).

## Waves, chronologically
1. Inventory (Opus ×3 + Sonnet): temporary system state, branches/worktrees (207 repos, narrowed to 17 deploy-path repos), Wi-Fi picture, Prometheus return, Headscale design, deploy gap, wave-2 plan, local AI models status. Findings: Prometheus off since 12:55 (unclean shutdown); tailnet wholly down since ≤June (self-signed Headscale cert with the old cluster name, no trust anchor); Prometheus ran a hand-activated generation from an unmerged branch; messenger-clj hand-linked and unrooted; Flow via drop-in; ~100 local-build roots; six pre-existing check failures.
2. Integrate: field-clj pin (a676b3), Home Flow 0.12.2 + messenger-clj (00f95a), diverged Home line and the USB fix onto CriomOS/Home mains (3e2cc8be→e6a83edc with lojix 8.0.0; Home 4a9d85d7); CriomOS-lib Gemma restored; horizon-rs 0.13.0 single schema bump (tailnet refs, required country, UsbDownlink) with main moved off an abandoned line; repin train (signal-lojix 6.0.0, meta-signal-lojix 7.0.0, lojix 8.0.0 with row quarantine); bookmarks: tailnet repair (VM test passes), Wi-Fi country + 802.11n fix + hostapd verbosity, UsbDownlink consumer (VM chain test passes), Blueprint/registry/codex-next/lojix-ownership fixes, Herdr module fixes; integration-2 branches evaluated against the new data (blocked by design on the CA until Field mints). Discards: MAC-address branch chain in four repos, superseded pin chains, m1/m6, 16 stale workspaces; 36 stale locks released; 24 stale routes retired (88475f; grade B). Psyche recovery from five retired flows. Ouranos deploy blocked twice (request without secrets; proposal store path GC'd) — Field resubmitting with a rooted proposal.
3. Wave 3 (in flight at handoff): feature-gated Field monitoring and declared Herdr server in Home; six pre-existing CriomOS check repairs; lojix 8.1.0 realize-on-target; Home pins of flow 0.14.0 and message 0.14.0.

## Lessons
Prometheus's six builder slots (one datom field) throttled the whole night; declared fix in goldragon (8 jobs). Lojix stages every target closure through the operator's laptop store (design fixed in 8.1.0). Reused request packets carry stale choices (NoSecrets; GC'd proposal path). Deviations: one local cargo build of a scratch tool; one receipt committed with raw-git plumbing; other flows' dirty files committed under the dirty-tree rule; my own first commit used raw git.

## Unfinished at handoff
Ouranos activation and window cleanup; tailnet secrets (ouranos, Prometheus minted; mirror/vm-testing recipients unverified) and CA on the goldragon bookmark; step-2 main merge and second ouranos deploy (Nexus 8 with new data); Prometheus boot-once deploy (fallback from e6a83edc by ~03:30); live daisy-chain test (brief ready); Qwen roots removal + GC; wave-2 report; the 06:30 artifact from reports/night-2026-09-25.md via visual-report-from-md. Questions for the living are in that report.

## Records
log.md (chronology), vision/ (the living's words), reports/ (30 reports incl. handoff.md, night-2026-09-25.md), receipts/ (messages, locks, deletions, roots, GC). No Beads opened.
