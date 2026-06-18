# 683 — design review (piece by piece) + the direct criome networking lane: frame and method

The psyche asked for two things in one prompt: review the design **most important
piece by piece**, and **talk about networking** — with the seed assertion that
*"criome will want to connect directly because of time-sensitive operations with the
other criome's."*

## The Spirit gate outcome

The networking assertion is genuinely new durable intent about criome's network
topology — but the gap-check found it **already captured** as Spirit `lt44` (operator
lane, the faster capturer): [CriomOS communication architecture has two transport
lanes … criome also has a direct criome-to-criome peer lane for time-sensitive
agreement operations with other criome daemons, especially quorum signing and
crystallized-time windows … that direct lane carries criome agreement and
authorization messages, not arbitrary component payload transport, so criome remains
auth/agreement-only while router remains the general transport fabric]. My duplicate
`Record` was correctly rejected by the guardian; `lt44` covers the psyche's statement
faithfully **and resolves the wckt tension** (it is the two-lane evolution of the
prior one-router `wckt` framing). So the networking work is **how the lane works**,
not whether to have it.

Two maintenance edits did land this turn: `eeeo` was **Clarified** to fold in the
ComponentPrincipal-collapse detail (closing the "psyche-decided" anchor gap operator
417 flagged), and `skills/structural-forms.md` was corrected to operator 417's
current schema-next struct grammar (the `1de72dde` parenthesized-composite role form,
alongside `af3705c`/`95f1ee7`).

## Method — concurrent grounding review + a networking design pipeline

| Phase | What | Grounding |
|---|---|---|
| Review | one Explore agent per design piece (9), ranked by importance, grounding each against current main — true landed/partial/designed/open state with a concrete citation | criome / signal-criome / router main + operator 410/417 + system-designer 133/135 |
| Networking | 4 research angles (current-transport inventory, BFT direct-validator p2p, time-attestation RTT bounding, partition/divergence) → synthesize the direct-lane design → adversarially critique it | code on main + web research |
| Synthesize | the consolidated report `3-review-and-networking.md` — piece-by-piece review + the two-lane networking design + the honest critique + operator-417 corrections + an intent-hygiene ledger | all of the above |

The review pieces and the networking pipeline run concurrently; the synthesis
consumes both. The networking design is constrained to keep criome auth/agreement-only
(it must not become a transport), and the critique stage is told to try to break
exactly that invariant. The report is `3-review-and-networking.md`; this file is the
frame.
