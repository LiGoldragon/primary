# 40 — lojix production cutover plan: frame & method

cloud-designer, 2026-06-11. Psyche prompt: *"create a report detailing what is
needed for production cutover, things to watch for, constraints that must be
met, etc. you can do some worktree branch testing to ground your report in
truth if needed."* Spirit gate: working order (task directive; the cutover
constraints derive from existing intent, no new durable psyche intent) →
**no capture**. The open decisions this surfaces are the psyche's to settle, not
records I write.

## What this report is

The forward-looking companion to reports 38 (production-readiness audit —
*verdict: not ready*) and 39 (the Stack-A production baseline — *the parity
bar*). 38 said what's wrong; 39 said what the bar is; **40 says what it takes to
cross it**: the gate list to implement, the constraints that must hold, the
subtle production behaviors to watch for, the consumer-migration path, and a
staged cutover sequence.

## Grounding (psyche-authorized worktree testing)

Where 38/39 rest on source reads, this report grounds the load-bearing claims in
**real runs** (workflow `lojix-cutover-plan`):

- build + test the new daemon as it stands on `lojix` main (`triad-port/`);
- empirically confirm the **secrets gate** — that a CriomOS router node throws at
  `nix eval` without the `secrets` override, **and** that a secret-free node
  evaluates past that point (the escape hatch for a first cutover);
- confirm the **OsOnly firmware-field divergence** (new daemon emits
  `includeAllFirmware`, lojix-cli emits only `includeHome`);
- trace the **consumer-invocation model** — how CriomOS/CriomOS-home actually
  drive lojix-cli today, to scope what "migrate a consumer" means.

Testing is non-mutating (builds/evals) and stays in worktrees / read-only
checkouts; no code-repo `main` is touched (designer discipline).

## Method

Five parallel ground/analysis agents → one synthesis agent (staged plan + gate
ranking), then this orchestrator assembles the report. Grounded findings land in
the numbered files here; the synthesis (the staged cutover plan) is the
highest-numbered file. Inputs: reports 38 & 39, the `lojix`/`signal-lojix`/
`meta-signal-lojix` triad-port source, `lojix-cli`, `CriomOS`/`CriomOS-home`,
`goldragon/datom.nota`, `horizon-rs`, and the workspace hard-overrides.

Dimensions: (1) build/test ground truth, (2) secrets-gate grounding,
(3) firmware-divergence grounding, (4) consumer-migration path,
(5) constraints + watch-fors, (6) synthesized staged plan.
