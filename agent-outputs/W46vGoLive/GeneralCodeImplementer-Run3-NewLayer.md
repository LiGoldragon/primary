# w46v final layer — STOP: nota-next→nota staleness is system-wide, not 2 repos

Session W46vGoLive. Greenlight was to fix nota-next on introspect+persona,
re-run, and land behind a green gate. While applying it, a genuinely NEW,
LARGER layer surfaced. Per directive #4 (new layer → STOP, touch no main,
report scope+classification), I stopped.

## What I applied this round, then reverted

- Edited `introspect/Cargo.toml`: `nota-next = { package = "nota", … }`. Then
  regenerated the lock (`cargo metadata`) to confirm the churn is contained.
- The regen FAILED: `error: no matching package named nota-next ... required by
  package meta-signal-introspect v0.1.0`. So a TRANSITIVE dependency of
  introspect (`meta-signal-introspect`) ALSO declares the stale `nota-next`
  package and blocks resolution.
- I **reverted** the introspect Cargo.toml edit (jj restore). introspect working
  copy is clean; **no component main touched this round.** (B = persona main
  ac629103 and C = goldragon main e8b658fa from the prior round remain landed and
  correct.)

## The new layer: nota-next→nota is a SYSTEM-WIDE migration

nota-next.git renamed its crate `nota-next`→`nota` at `96e64bc`. **~35 repos**
still declare `nota-next = { git=…nota-next.git }` (package `nota-next`) and lock
a pre-rename rev. Because cargo resolves ONE rev for `nota-next.git@main` across
a crate's entire unified lock, the moment any producer forces the post-rename
crate (`nota`), EVERY stale consumer in that lock graph conflicts at once. So the
fix is not 2 repos — it is every stale nota-next consumer in the build graph.

### Precise gate-critical subset (blocks the whole-engine gate)

persona's own Cargo lock graph (one unified resolution — all must be fixed
together):
- persona
- meta-signal-persona
- meta-signal-upgrade
- triad-runtime
- signal-system
- signal-upgrade
- upgrade

introspect flake-input graph (separate unified lock — both must be fixed):
- introspect
- meta-signal-introspect

= **9 repos minimum** to green the gate. (Plus any additional stale flake-input
graph the topology checks build — orchestrate/terminal/system are stale and are
persona flake inputs; whether the launched topology builds them determines if
they are also required.)

### Full system-wide stale set (~35 repos)

chroma, chronos, clavifaber, cloud, domain-criome, horizon-rs, lojix,
meta-signal-cloud, meta-signal-domain-criome, meta-signal-introspect,
meta-signal-lojix, meta-signal-mind, meta-signal-orchestrate, meta-signal-persona,
meta-signal-repository-ledger, meta-signal-system, meta-signal-terminal,
meta-signal-upgrade, meta-signal-version-handover, nexus, nota-config, orchestrate,
persona, repository-ledger, signal, signal-cloud, signal-domain-criome,
signal-lojix, signal-orchestrate, signal-repository-ledger, signal-system,
signal-upgrade, signal-version-handover, system, terminal, triad-runtime, upgrade.

Already migrated / OK (declare `nota-next = { package = "nota", … }`): criome,
harness, mentci-egui, mentci-lib, mind, terminal-cell. (introspect is STALE — the
scan momentarily showed it OK only because my in-flight, now-reverted edit was in
its working copy.) The producers signal-router, signal-harness, signal-frame,
message, router use the `nota` package key already, which is why they verified
GREEN in run 2.

## Classification

- **Per repo: MECHANICAL, no source edits.** `nota-next = { package = "nota",
  git=…, branch=main }` (keep the key `nota-next` so `use nota_next::` still
  compiles) + regenerate the lock so the nota-next entry resolves to package
  `nota` at nota-next main. `use nota_next::` source refs exist widely but are
  preserved by the key.
- **Aggregate: JUDGMENT / COORDINATION, not bounded autonomous work.** It is a
  ≥9-repo (gate-critical) / ~35-repo (system-wide) cross-repo migration with
  per-repo lock regens and landing order. It is effectively a PREREQUISITE
  refactor for the entire w46v contract sweep: no consumer can be bumped onto the
  new signal-router/harness contracts (which pull package `nota`) until its whole
  nota-next graph is migrated. This is its own tracked work item, above the
  2-repo greenlight and above "bounded."

## Terminal state

- Gate: RED (unchanged from run 2; not re-run — re-running is futile until the
  ≥9-repo migration lands).
- Landed to NO component main this round. All mains at prior values (persona
  ac629103, signal-router 30be9b0f, signal-harness 52cd2ed, message d7dfb005,
  router 14f8557, introspect 7b53b37e, signal-frame 0027ea3c). Run-2 synchronizer
  staging branches remain unmerged.
- primary-w46v: OPEN.

## Recommendation

Treat the nota-next→nota migration as a distinct tracked item (a mechanical but
system-wide sweep). Do the 9 gate-critical repos first (producers→consumers:
meta-signal-* / signal-system / signal-upgrade / upgrade / triad-runtime /
meta-signal-introspect, then introspect, then meta-signal-persona /
meta-signal-upgrade, then persona), each: manifest `package = "nota"` + lock
regen (verify no unrelated branch=main cascade) + land. THEN the synchronizer
re-run + whole-engine gate should go green (router already proved the daemons
build at signal-frame 0.3.0). A repo-lock rev-drift + crate-rename scan would
find these mechanically.
