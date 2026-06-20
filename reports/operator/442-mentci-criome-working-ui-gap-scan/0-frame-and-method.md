# 0 — Frame and method

## Why this scan

The psyche asked, as operator, for a **wide scan of what must be developed**
to have a *working mentci UI*: a `mentci` CLI connected to `mentci-daemon`,
which interacts with a **running** `criome` daemon. criome runs in *client
approval mode* — a submission to criome is **parked** for mentci to approve —
and the end-to-end loop must actually run over two live Unix sockets, not only
as a single-process integration test. The brief named three lenses: **design
gaps, ugly code, and unported work.**

This lands directly on top of the previous operator's 440/441 slices
(`reports/operator/440`, `441`): criome's `AuthorizationMode [Quorum
AutoApprove]`, the meta-socket `Configure` + `SubmitAuthorizationApproval`,
and `CriomeApprovalBridge`. That predecessor's stated remaining boundary —
encrypted key custody / live verdict signing — is folded in here as one
dimension among eight, so it is placed in the full gap picture rather than
treated as the sole gap.

## Method

A background fan-out workflow
(`mentci-criome-working-ui-gap-scan`, run `wf_fbf49ee9-bb8`) over the two
component triads — `mentci` / `signal-mentci` / `meta-signal-mentci` and
`criome` / `signal-criome` / `meta-signal-criome`:

1. **Scan** — 8 dimension-readers, each reading the actual code against the
   goal and emitting structured findings (kind, severity, `file:line`
   evidence, goal-impact, direction):
   1. mentci CLI as UI
   2. mentci daemon state & SEMA
   3. the criome↔mentci bridge loop
   4. criome authorization & parking
   5. signal contract coherence (4 repos)
   6. key custody & verdict signing
   7. unported / stub sweep
   8. ugly code / discipline sweep
2. **Verify** — every finding handed to an independent adversarial verifier
   that re-opened the cited code and decided `isReal` (default to *false* if
   the evidence did not hold up or the gap was already built elsewhere),
   correcting severity and dropping the unreal.
3. **Synthesize** — the confirmed set folded into one prioritized report and
   a concrete build sequence.

54 agents, ~2.06M tokens, 8 dimensions. **45 raw findings → 38 confirmed**
(7 dropped on verification). Counts per dimension:

| Dimension | Confirmed / raw |
|---|---|
| 1 — mentci CLI as UI | 6 / 7 |
| 2 — mentci daemon state & SEMA | 4 / 5 |
| 3 — bridge loop | 5 / 6 |
| 4 — criome authorization & parking | 5 / 5 |
| 5 — signal contract coherence | 6 / 6 |
| 6 — key custody & verdict signing | 1 / 4 |
| 7 — unported / stub catalog | 5 / 6 |
| 8 — ugly code / discipline | 6 / 6 |

## How to read this directory

- `1-…` through `8-…` — each dimension's confirmed findings (plus, at the
  end, the findings that were *dropped* on verification, kept for honesty
  about what was checked and rejected).
- `9-synthesis.md` — the prioritized gap report, the build sequence, the
  open questions for the psyche, and the chat items. **Start there.**

## The one-line conclusion

Two things are the whole job, and both are *absent*, not buggy: (a) the
**parked, addressable-by-id `AuthorizationEvaluation`** — criome never
persists it, never puts it on the wire, never threads it through a contract;
and (b) the **`mentci` CLI is not a UI** — a one-shot raw-NOTA-in /
raw-binary-out pipe with no verbs. The cross-daemon loop exists today only
inside one `#[test]` that hand-carries the evaluation as a shared Rust
variable. Notably, mentci's own `nexus.schema` already *names* the entire
intended bridge (`FrameEscalation`, `RouteVerdict`, `InterfaceFanOut`); the
design is drawn, none of it is built.
