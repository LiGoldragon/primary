# 96 — The federated key-gated Spirit: frame and method

This report develops the psyche's privacy direction (Spirit **`dun9`**) into
a design: rethink Spirit — and any private component — as a **federation of
key-scoped encrypted versioned stores** on the GoPass model. It realizes the
privacy/erasure spectrum of report `95/11` and answers the granularity
question (Q2) the psyche chose: **per-store keys**, where each store is
encrypted to a recipient set, access is key possession, and the per-store
key is the access boundary *and* the crypto-shred erasure unit.

## What the psyche directed

- "Breaking it up into multiple stores … seems like the most obvious and
  simple design … separate private stores for separate concerns." The
  **GoPass** model: multiple stores, each encrypted to a set of keys; access
  is which keys you hold.
- "Rethinking the entire way we've been designing the Spirit database. Maybe
  there's several databases, and queries are adjusted depending on which keys
  the particular Spirit daemon has access to … keep the files readable by
  many different instances … while ensuring privacy with encryption."
- Accountable content-erasure (Q1) is acceptable.
- Two questions returned to the psyche, still open: whether a single-root
  **nuclear option** should exist (Q3), and the **federation key
  distribution** shape (one-or-few keys per instance vs a primary holding
  most).

## Method

A background research Workflow (`multistore-keygated-spirit-research`, run
`wf_6aba9ed2-228`) — four web-verified agents → synthesis → adversarial
critic:

| Agent | Established |
|---|---|
| `gopass-pass-multirecipient` | GoPass/pass + the age/SOPS/git-crypt envelope; and the load-bearing distinction **revocation ≠ erasure**. |
| `capability-encrypted-storage` | Tahoe-LAFS read/verify/write **caps**, Cryptree, Keybase/KBFS, Matrix Megolm — cryptographic capabilities as the rigorous key-gating. |
| `willow-federated-encrypted-sync` | Willow + Meadowcap (3D areas, prefix-pruning, PIO/PAI), Ink&Switch Keyhive/Beelay/Sedimentree, p2panda — federated sync over ciphertext. |
| `spirit-federation-problems` | The new problems: store-existence metadata, cross-store atomicity, partial references, key-explosion, forward-secrecy-vs-late-joiner, routing determinism. |

The deliverable is the **visual design** (file 6): the federation model, the
capability triad, the KEK→DEK key hierarchy, privacy-as-routing,
revoke-vs-erase, existence-privacy via store-id-as-capability, cross-store
references and the saga model, zero-knowledge sync/compaction, the two store
classes, how it composes with the grand design (95), the new problems with
resolutions, and the open decisions (including the psyche's two). Research
chapters 1-4 and the synthesis (5) sit beneath it.

## Builds on

Report 95 (the grand design, esp. `11-privacy-retention-erasure-deep-design`),
system-operator 214/215 (the per-store privacy/retention matrix), and Spirit
`29pb` / `j487` / `i4ak` / `x0ja` / `dun9`.
