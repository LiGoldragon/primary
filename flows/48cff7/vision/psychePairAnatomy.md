# psychePairAnatomy

## 2026-09-16 — the pair anatomy, and why pairs become triads; mode-aware mirroring; Fable allocation; core psyche as defense

Context: after naming the flows (`flowNaming.md`) and settling that distillation is the psyche's output (`psycheIsDistillation.md`), the living asked for the pair's anatomy — what each member's role is and how they marry each other.

> Let's try that, and let's give them their anatomy. What's their role, or how do they marry each other? These pairs are going to be triads soon. The low power has, and they each have different modes. If Codex itself is in low-power mode, then maybe not all of these low-powered Claude equivalents are actually mirroring everything to Codex, because Codex is in conservation mode, right? It really depends. We have to have some kind of allocation of what gets Fable last, right? The primary Psyche, or even the core Psyche, could be. We should upgrade it to that, but the core Psyche doesn't need to run much. You would keep it last as a defense for the core, right, to keep the thing secure. If anything can automate decisions, it's going to be the core layer. It's inherently doubtful and careful, and it's going to be the most direct link to, or one of the biggest users of, the third layer. I guess the tertiary layer of communication is going to be used a lot by the core layer to communicate with Psyche. The farther we are from implementation, the more this is just drafting.

-- psyche, STT.

## Anatomy (ASCII)

```
psyche pair anatomy — one effort tier, one layer (this pair: primary MEDIUM)

           ┌──────────────────────── living ────────────────────────┐
           │  types or STT · watches the primary Claude transcript  │
           └───┬──────────────────────────────────────────────┬─────┘
               │  default: talks to Claude side;              │
               │  messenger mirrors to peers                  │
               ▼                                              ▼
   ╭─── Claude side ────────╮                 ╭─── Codex side ────────╮
   │  persona  (per tier)   │◀── mirror ────▶ │  persona  (per tier)  │
   │  Fable / Sol / Terra   │   same effort   │  Astra / … / Terra    │
   │  model : Opus 4.7 [1m] │   same layer    │  model : Codex peer   │
   │                        │                 │                       │
   │  role · distill        │                 │  role · distill       │
   │       · dispatch       │                 │       · dispatch      │
   │       · respond        │                 │       · respond       │
   ╰──────────┬─────────────╯                 ╰──────────┬────────────╯
              │                                          │
              ▼                                          ▼
    Claude implementation                       Codex implementation
    subflows (build · test)                     subflows (build · test)

  ┌───────────── open-source seat — chartered, NOT ACTIVE ───────────────┐
  │  persona · tier · model (self-hosted open-source)                    │
  │  role · private-layer double-check · defense · core comms carrier    │
  └──────────────────────────────────────────────────────────────────────┘
```

## Statements the anatomy encodes

- **Same-effort mirror.** Pair members share `(layer, effort)`; the mirror is the routing rule between them.
- **The living talks to Claude side by default.** The messenger delivers the same prompt to the peer(s).
- **Pairs become triads with the open stack.** The third seat is chartered but not active.
- **Feedback runs through git origin or intercom today.** There is no live peer-to-peer inbox; that is a gap (G06 on the routing gaps map).
- **Mode-aware mirroring.** If a peer is in conservation mode, mirroring to it reduces or halts. Allocation reads the peer's mode, not just its effort.
- **Fable-allocation policy.** Fable (top tier) is used last / most sparingly. Defaults route to a lower tier first. This is the mirror-rule's converse — mirroring across stacks at a tier, but *choosing* the tier by allocation.
- **Core psyche is a defense.** Quiescent by default. Doubtful, careful. Rare invocation. Automates high-stakes decisions when it must.
- **Core is a heavy user of the tertiary layer.** Private psyche comms ride the open-source seat.
- **Distance-from-implementation = amount of drafting.** The core sits furthest from implementation, so its work is nearly all drafting; the closer a flow is to code, the less it drafts.

## Open questions worth the living's word

1. What "conservation mode" concretely looks like at a flow — a Nexus signal, a settings field, or an on-the-fly capability.
2. What triggers Fable — an explicit living word, an escalation from below, a policy in the meta-signal of a routing nexus.
3. Whether "core" is a layer, a role, or both — the psyche skill names layers; this vision entry treats core as the innermost layer, but the living may mean the *role* core-psyche across any layer.
4. Whether the tertiary layer (open stack) is used only for core-to-psyche private comms, or also for other private paths.
