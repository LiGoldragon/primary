# uwh5 — keep currently awake non-Astra seats awake

Completed 2026-11-15 17:21 UTC by actual4aa030 using deployed pinned qpsb flow-meta, paired signal83. Deployed daemon PID3543089 remains qpsb; reviewed source37980e10 worktree clean. No restart, launch, refresh, source edit, threshold change or message to an Astra address.

## Source judgment

store.rs6525–6594 amends only the declaration; lib.rs2111–2130 commits/applies it. apply_configuration (lib.rs1728–1795) reconfigures launcher/composer/retention as needed, not launches. Therefore Continuity.Maintained on an asleep declaration does not itself launch it. waking.rs4201 returns Idle for Maintained, keeping the harness; continuity is read from the declaration at each rest. Threshold/replacement logic runs earlier and remains enabled.

There is no narrower exposed sleep-only setting. `closable` (waking.rs4103–4142) is calculated from native turn/rest and background work; it is not a configuration value and must not be falsified to suppress sleep. Maintained also changes successor behavior after unexpected exit/refresh; this is the available existing capability, not a claim of an isolated sleep flag.

## Applied smallest awake-only change

Fresh Current.Awake checked immediately before each individual setter; each exact Configured.Amend echo matched:
- { Field inventory Sol } OnDemand → Maintained, same flow Awake.ad72ed.
- { Psyche book Haiku } OnDemand → Maintained, same flow Awake.bd378a.
- { Psyche comments Haiku } OnDemand → Maintained, same flow Awake.08fc5d.

Final Configuration: 40 declarations, 9 Maintained/31 OnDemand. Exactly these three declaration fields changed. All other policy/configuration fields, including thresholds and absent warning policies, are identical. Activity counters changed from {28920 7598 7272} to {28925 7599 7274}; these were observed, not written by this work. Metaflows before/after has identical states and native FlowIds for every listed seat: no asleep seat was launched by these amendments. Six already-Maintained declarations and every Astra declaration were left unchanged.

## Exact declarations left unchanged

- { Field protosConsumers Sonnet } — OnDemand; Asleep
- { Field core Astra } — OnDemand; not present in runtime Metaflows
- { Field core Sol } — Maintained; Awake.374411
- { Field protos Opus } — OnDemand; Asleep
- { Field protos Sonnet } — OnDemand; Asleep
- { Field semaV0 Astra } — OnDemand; not present in runtime Metaflows
- { Field semaV0 Opus } — OnDemand; Asleep
- { Field upkeep Sol } — OnDemand; Asleep
- { Field heartbeat Sol } — OnDemand; Asleep
- { Mind curriculum Astra } — OnDemand; Asleep
- { Mind curriculum Opus } — OnDemand; Asleep
- { Mind curriculum Sol } — OnDemand; Asleep
- { Mind datomCodec Sol } — OnDemand; not present in runtime Metaflows
- { Mind herdrNexus Sol } — OnDemand; Asleep
- { Mind nixCriomos Sol } — OnDemand; not present in runtime Metaflows
- { Mind beliefNexus Astra } — OnDemand; not present in runtime Metaflows
- { Mind orchestrate Sol } — OnDemand; not present in runtime Metaflows
- { Mind sourceNexus Opus } — OnDemand; Asleep
- { Mind versionZero Astra } — OnDemand; not present in runtime Metaflows
- { Mind versionZero Sol } — OnDemand; not present in runtime Metaflows
- { Mind researchTools Sol } — OnDemand; Asleep
- { Mind core Astra } — OnDemand; Asleep
- { Mind core Sol } — Maintained; Awake.1541ef
- { Mind lojix Sol } — OnDemand; not present in runtime Metaflows
- { Mind survey Sol } — OnDemand; Asleep
- { Mind research Sol } — OnDemand; Asleep
- { Mind flowNexus Astra } — Maintained; Awake.71e1c6
- { Mind flowNexus Opus } — OnDemand; Asleep
- { Mind flowNexus Sol } — Maintained; Awake.4aa030
- { Psyche beliefReview Fable } — OnDemand; Asleep
- { Psyche beliefReview Opus } — OnDemand; Asleep
- { Psyche nexusVariations Fable } — OnDemand; Asleep
- { Psyche core Fable } — Maintained; Awake.655f27
- { Psyche core Opus } — Maintained; Awake.65c59d
- { Psyche core Sonnet } — OnDemand; Asleep
- { Psyche criomos Opus } — OnDemand; Asleep
- { Psyche restart Opus } — OnDemand; not present in runtime Metaflows

## Scope and cost

A changed Maintained seat stays awake when it next rests, subject to unchanged threshold refresh and explicit lifecycle orders. An unchanged asleep OnDemand seat, if subsequently woken, still uses the old fresh-start wake path and may sleep again. Thus this implements the ordered currently-awake subset, not a global remedy for every future wake. No asleep declaration or Astra address was amended. Durable source replay still declares the original continuities; no source persistence was implied or performed by these live amendments.

An idle harness generates no model tokens merely by remaining open; panes, harness/app-server process memory, native session and context remain resident. Future messages continue accumulating context toward the unchanged refresh threshold. Tool/background work and an active turn can still incur their own costs. No resource-volume measurement was made.

Private evidence: /tmp/flow-4aa030-uwh5/ (before/after paired typed Configuration, Metaflows, per-amendment UTC/Current/command/exact echo, roster, reproducible structural audit). Audit excludes only recorded activity counters; no hidden semantic delta is asserted.
