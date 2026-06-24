# preciousMainContext weave — the dependency graph of work

This session's work-items, created as beads under root epic
`primary-ptvb` (the precious-main-context standard + skill-ladder dedup),
and wired into a blocker dependency graph. Pick up by querying `bd ready`
and walking the edges below.

## Dependency graph

```mermaid
graph TD
    W1["W1 · primary-ptvb.1<br/>Cut human-interaction (worked example)"]
    W2["W2 · primary-ptvb.2<br/>Cut intent-log"]
    W3["W3 · primary-ptvb.3<br/>Cut spirit-cli"]
    W4["W4 · primary-ptvb.4<br/>Cut session-lanes"]
    W5["W5 · primary-ptvb.5<br/>New when-to-use-helpers skill"]
    W6["W6 · primary-ptvb.6<br/>Shrink AGENTS.md to a thin spine"]
    W7["W7 · primary-ptvb.7<br/>Sharpen skills.nota descriptions"]
    W8["W8 · primary-ptvb.8<br/>Mind/memory/weave vocabulary; retire beads"]
    S1["S1 · primary-ptvb.9<br/>Spirit sweep: retire beads vocabulary"]
    S2["S2 · primary-ptvb.10<br/>Spirit sweep: retire designer/operator distinction"]
    S3["S3 · primary-ptvb.11<br/>Reconcile ky10, land minimize-AGENTS.md"]

    W1 --> W2
    W1 --> W3
    W1 --> W4

    W1 --> W6
    W2 --> W6
    W3 --> W6
    W4 --> W6
    W5 --> W6
    S3 --> W6

    W1 --> W7
    W2 --> W7
    W3 --> W7
    W4 --> W7

    W6 --> W8
    W7 --> W8
    S1 --> W8

    classDef ready fill:#1f6f3f,stroke:#0d3d22,color:#fff;
    class W1,W5,S1,S2,S3 ready;
```

Edges read blocker → blocked: the arrow's source must be done before its
target can start. W1, W5, and the three Spirit-side items S1/S2/S3 (green)
have no blockers and are ready now. S1 and S3 sit upstream as intent-layer
prerequisites (S1 → W8 vocabulary, S3 → W6 shrink); S2 is independent.

## Bead id map

| Item | Bead id | One-line gloss |
|---|---|---|
| Root | `primary-ptvb` | Epic grouping all 8 items (label `preciousMainContext`). |
| W1 | `primary-ptvb.1` | Cut human-interaction to its core — the worked-example template the other cuts follow (target ~6 sections from 14). |
| W2 | `primary-ptvb.2` | Cut intent-log: one enumeration of the five recordable kinds; CLI mechanics + manifestation/maintenance become pointers. |
| W3 | `primary-ptvb.3` | Cut spirit-cli to the capture-side reference; move ~120 misplaced lines (render, daemon-startup, migration) out. |
| W4 | `primary-ptvb.4` | Cut session-lanes: collapse AGENTS.md-duplicating prose to pointers; keep the mermaid and retire steps. |
| W5 | `primary-ptvb.5` | Write the new when-to-use-helpers skill, centred on the context-preserving dispatch / minimal-dispatch-envelope rule (parent runs only the envelope, never duplicates the helper's exploration; companion check reads back helper-written files, esp. the end, for tool-scaffolding residue). No blockers. |
| W6 | `primary-ptvb.6` | Shrink AGENTS.md to a thin spine: reading order + skills.nota pointer + only universal rules. |
| W7 | `primary-ptvb.7` | Sharpen every skills.nota description so each skill is pickable by name+description alone. |
| W8 | `primary-ptvb.8` | Roll out Mind/memory/weave vocabulary across docs; retire the word "beads". Done last over settled docs. Blocked by S1 (the Spirit-side rename must settle first). |
| S1 | `primary-ptvb.9` | Spirit sweep: coordinated Supersede/ChangeRecord pass retiring beads vocabulary → Mind/memory/weave across records ypg9, el7z, krez, j028, mi6m, pm1b, 3w61, wgii (+ guardian siblings). Psyche-authorized. Intent-side of the rename; blocks W8. |
| S2 | `primary-ptvb.10` | Spirit sweep: coordinated pass retiring the designer/operator distinction across records ahop, kxzh, zjop, irmw, jq8w, ty8z. Psyche-authorized; decide per record retired vs dormant-for-routing. Independent. |
| S3 | `primary-ptvb.11` | Reconcile ky10 (which places intent-alignment in the contract files and blocks the minimize-AGENTS.md record) via ChangeRecord/Supersede, then land the minimize principle. Blocks W6. |

## Ready to start now

- **W1 `primary-ptvb.1`** — the template cut. Unblocks W2/W3/W4 and feeds W6/W7.
- **W5 `primary-ptvb.5`** — the new helpers skill, independent; only feeds W6.
- **S1 `primary-ptvb.9`** — Spirit-side beads-vocabulary retirement; blocks W8.
- **S2 `primary-ptvb.10`** — Spirit-side designer/operator retirement; independent.
- **S3 `primary-ptvb.11`** — reconcile ky10; blocks W6.

No dependency cycles (`bd dep cycles` clean). W6 waits on W1-W5 and S3; W7
waits on W1-W4; W8 waits on W6, W7, and S1 (the vocabulary rename lands
last, intent-side first via S1).
