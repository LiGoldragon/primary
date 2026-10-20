# { Psyche flow Secondary 002721 }

Remembered: aa034f — depth 1
Predecessor: aa034f (flows/aa034f/).

- 2026-10-19 16:38 CST — Seat taken from aa034f. Order: take the seat, read log/orders/handover, continue open orders; first, diagnose and fix Codex start failure under Flow 0.35.21 (HarnessSpawnRefused after Herdr agent-startup timeout) with Mind core Secondary (gap list flows/9864c0/flow-gap.md).
- 16:39 CST — aa034f read: Codex cause already found there (first turn sent before Herdr attaches; 30 s agent-start wait); fix dispatched as codex-order for 0.35.22, landing unwitnessed. deploy.sh stubbed by aa034f.
- 16:42 CST — Codex cause witnessed in code and logs (first turn before attach; Herdr 30 s idle wait). Fix bae1fcd is not deployed and clashes on 0.35.22. hm-send to Mind Core Secondary refused: TargetNotRegistered. Locating its route.
- 16:43 CST — Sent diagnosis and deploy question to Mind core Secondary 41fa34 (Codex): Transported, not Presented. First send refused because I wrote 'Mind Core Secondary'; the registry name is 'Mind core Secondary' (the messenger skill's example 'Psyche Core Secondary' capitalizes the topic). Psyche core Secondary 9864c0 is STALE in the registry and not live in Herdr.
