# 98 — Sema version control with remote: the grounded vision. Frame and method

The psyche asked the system-designer to step back before implementation:
absorb the drafted design (reports 91–97, operator 211/214/215, the Spirit
intent log), explore the actual code of every involved component, audit
whether the foundations really are what they are intended to be — NOTA fully
typed with no custom parsing outside it, schema 100% on NOTA, the triad
schema interfaces actually used — and come back with a vision of how the
version-control system should be built simply, elegantly, and beautifully,
including the server side. Implementation starts only after the psyche reads
the vision.

## Method

One background workflow (`sema-vc-vision-exploration`, run
`wf_a18d52f9-f89`, 2026-06-12, 13 agents, ~970k tokens): eight parallel
read-only explorers, five of them followed by independent adversarial
verifiers instructed to refute every key claim from the code. All claims in
the synthesis rest on file:line citations that survived that verification.

| Chapter | Subject | Verified |
|---|---|---|
| `1-spirit-pilot.md` | Spirit: persistence path, guardian, generated/hand split, migration, VC seam | yes — 12/12 confirmed |
| `2-sema-kernel.md` | sema + sema-engine: kernel, the existing versioned log, choke points | yes — 8 confirmed, 2 nuanced |
| `3-nota-foundation.md` | nota-next typed-codec audit + parsing-bypass sweep | yes — 10/10 confirmed |
| `4-schema-emission.md` | schema-next + schema-rust-next: emission state, generation seam | yes — 6 confirmed, 1 nuanced |
| `5-triad-conformance.md` | Triad-interface conformance across five components | yes — 9 confirmed, 3 nuanced |
| `6-prior-design.md` | Design corpus 91–97 + operator 211/214/215 decision ledger | reports-only |
| `7-intent-baseline.md` | Spirit intent log: binding set, stale candidates, gaps | log-only |
| `8-remote-surface.md` | Hosts, deploy surface, repository-ledger exemplar, mirror shape | reports+code |

The synthesis — the psyche-facing deliverable — is `9-the-vision.md`.

## Intent handled this session

Gate run on the psyche's framing prompt. Captured: `61lk` (Clarification —
all text code is pseudocode; Sema closes the correctness gap, NOTA/schema as
the deliberate half-step) and `zn2l` (Clarification — the endpoint is the
final software engine that self-improves to unimprovable). `6grf` (schema is
a NOTA dialect) was re-affirmed, importance bumped to VeryHigh rather than
duplicated. The remote-shape uncertainty and privacy-later scoping were
treated as task state, not intent. Manifestation of `61lk` into
`sema/INTENT.md` rides with the implementation branch (noted in 9 §10).
