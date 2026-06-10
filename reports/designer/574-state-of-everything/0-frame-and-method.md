# State of Everything — Frame and Method

Psyche asked (2026-06-10) for "a big state of everything": where every
component stands in light of intent, which use out-of-date or deprecated
dependencies and which are ahead, how much code is in each (and how much
is *production* — code that runs if the component is used, not test
scaffolding), an engine analysis on everything, the state of the schema
files now that the structural macros have been overhauled for terser
syntax, how the lojix→CriomOS migration is going, whether free functions
are lying around that violate the method-only rule, whether any NOTA
encode/decode is *cheating* (ad-hoc string-printing a fake NOTA shape
instead of encoding a real type), and a skills audit for files that have
become contradictory, too long, or winded.

This is the orchestrator frame. The numbered files hold each cluster's
findings; the highest-numbered file is the synthesis.

## Method

Two passes:

1. **Inline mechanical sweep** (deterministic, done by the orchestrator):
   per-repo production/test/schema line counts across all ~90 local
   checkouts, the foundation-crate HEAD revisions, and how dependencies
   are pinned (Cargo.toml tracks `branch = "main"`; the *real* pin lives
   in each consumer's `Cargo.lock` / `flake.lock`). The raw table below
   is mechanical truth — every later judgement rests on it.

2. **Workflow fan-out** (`state-of-everything`, 14 audit agents +
   1 skills agent): eleven component-cluster deep audits, one
   lojix/CriomOS migration deep-dive (reads the `horizon-leaner-shape`
   worktrees), one authoritative schema-engine + grammar-adoption
   verdict, and one skills-corpus audit. Each cluster agent judged, per
   repo: intent-fit, refined production LOC, daemon/engine shape (real
   actors counted, not READMEs trusted), foundation dependency lag
   (commits-behind, with the nota-next `d8862b6` encoding-bump flag),
   schema-file terseness and concept/triad staleness, free-function
   violations, and fake-NOTA violations — each with `file:line`.

### Production-LOC definition

"Production" = code that runs if the component is used: `src/**` plus
`crates/*/src/**`, **minus** inline `#[cfg(test)]` modules and the
`tests/` and `benches/` directories. Checked-in generated code
(`src/schema/*.rs` from `quote!` + `prettyplease`) is production-but-
derived and is reported separately where it exists. The table below is
the first-order split (everything outside `tests/` dirs vs. inside);
agents refined it per repo by excluding heavy inline test modules.

## Foundation HEADs — the "latest" every consumer is measured against

| Crate | HEAD | Date | Note |
|---|---|---|---|
| `schema-next` | `c8ebb39` | 2026-06-10 | terse grammar (52ro/yp29/qz6j/lm84) just landed |
| `schema-rust-next` | `eca4028` | 2026-06-10 | emits `FixedBytes<N>`, Bytes hex codec; pins nota-next `ae5c25cd` |
| `nota-next` | `d8862b6` | 2026-06-09 | **encoding bump** (`[[x]]`→`[x]`, bare atoms) — schema-rust-next deliberately lags it |
| `nota-config` | `ba689f0` | 2026-06-08 | |
| `sema` | `da96de2` | 2026-06-07 | |
| `sema-engine` | `ebee6e4` | 2026-06-08 | |
| `triad-runtime` | `6ea8316` | 2026-06-09 | |
| `signal` | `c4fbbfa` | 2026-06-08 | |
| `signal-derive` | `5d6c80c` | 2026-05-24 | |
| `signal-frame` | `166bda8` | 2026-06-09 | |
| `version-projection` | `f00b239` | 2026-06-08 | |

The fast movers are the three at the top: the grammar overhaul landed on
schema-next/schema-rust-next *today*, and nota-next carries an unmerged-
downstream encoding change. Any consumer is therefore measured mostly by
how far its lock files trail these three.

## Raw fleet code-count table (mechanical)

Production = `.rs` outside `tests/` dirs (includes inline `#[cfg(test)]`,
which agents net out per repo); Test = `.rs` under `tests/`; Schema =
total `.schema` lines; n = schema file count.

| Repo | Prod | Test | Schema | n | HEAD |
|---|---:|---:|---:|---:|---|
| spirit | 13266 | 5485 | 243 | 4 | `1373e04` |
| mind | 10188 | 3356 | 109 | 4 | `82bfbb4` |
| persona | 10044 | 4962 | 42 | 2 | `7d7adfa` |
| router | 9466 | 3507 | 150 | 4 | `ddc40dd` |
| terminal | 9120 | 1640 | 206 | 4 | `f264ea0` |
| schema-rust-next | 8859 | 13457 | 342 | 17 | `eca4028` |
| cloud | 8752 | 1046 | 118 | 2 | `0816895` |
| persona-spirit | 8374 | 5505 | 56 | 1 | `3701aac` |
| schema-next | 8290 | 4194 | 345 | 20 | `c8ebb39` |
| orchestrate | 7292 | 1888 | 502 | 7 | `c93233c` |
| upgrade | 6966 | 601 | 160 | 2 | `295e0e9` |
| lojix | 5214 | 644 | 160 | 2 | `f9be5df` |
| terminal-cell | 5095 | 1610 | 58 | 2 | `3c81cd2` |
| message | 4812 | 429 | 94 | 3 | `7fe45bf` |
| signal-frame | 4560 | 2214 | 28 | 1 | `166bda8` |
| nota-next | 4395 | 1804 | 0 | 0 | `d8862b6` |
| domain-criome | 4032 | 310 | 97 | 2 | `e6cac74` |
| triad-runtime | 3800 | 1408 | 0 | 0 | `6ea8316` |
| signal-terminal | 3675 | 946 | 131 | 1 | `0a11eb3` |
| agent | 3425 | 151 | 68 | 2 | `ae9e46d` |
| sema-engine | 3260 | 2572 | 47 | 1 | `ebee6e4` |
| criome | 3214 | 644 | 35 | 1 | `098d501` |
| signal-criome | 3152 | 914 | 360 | 1 | `86f00eb` |
| lojix-cli | 3000 | 1805 | 31 | 1 | `fc2ff02` |
| harness | 2981 | 2521 | 46 | 2 | `c9748d6` |
| signal-orchestrate | 2836 | 725 | 181 | 2 | `88c1fe6` |
| horizon-rs | 2714 | 1913 | 0 | 0 | `48df4bd` |
| signal-mind | 2712 | 1315 | 40 | 1 | `876be2c` |
| repository-ledger | 2562 | 619 | 67 | 2 | `4f86060` |
| signal-spirit | 2491 | 1164 | 0 | 0 | `87b45ed` |
| introspect | 2176 | 933 | 36 | 2 | `2605447` |
| mentci-lib | 2151 | 0 | 0 | 0 | `c68673e` |
| system | 1899 | 1046 | 42 | 2 | `ea7297c` |
| signal-cloud | 1781 | 153 | 92 | 2 | `d04437e` |
| message (signal) | 1733 | 432 | 114 | 1 | `6a29eb1` |
| signal | 1574 | 535 | 23 | 1 | `c4fbbfa` |
| meta-signal-cloud | 1498 | 188 | 104 | 2 | `a94066e` |
| signal-upgrade | 1467 | 497 | 106 | 2 | `6250077` |
| signal-domain-criome | 1432 | 164 | 82 | 2 | `0bebced` |
| meta-signal-orchestrate | 1332 | 286 | 111 | 2 | `74af12b` |
| signal-message | 1733 | 432 | 114 | 1 | `6a29eb1` |
| meta-signal-upgrade | 1290 | 511 | 90 | 2 | `44e747b` |
| signal-lojix | 1288 | 0 | 121 | 1 | `0b8a9e3` |
| meta-signal-domain-criome | 1169 | 114 | 40 | 1 | `a81268e` |
| signal-router | 1152 | 462 | 112 | 2 | `a014a33` |
| meta-signal-router | 1089 | 202 | 148 | 1 | `cc4f3e9` |
| meta-signal-lojix | 984 | 0 | 133 | 1 | `5cf4824` |
| nexus | 912 | 290 | 28 | 1 | `b9f904e` |
| signal-persona | 798 | 262 | 27 | 1 | `ae9cf26` |
| signal-harness | 672 | 706 | 32 | 1 | `75b01c1` |
| signal-repository-ledger | 665 | 114 | 35 | 1 | `bba8bc0` |
| signal-sema | 600 | 759 | 42 | 1 | `33f6284` |
| sema | 581 | 472 | 41 | 1 | `da96de2` |
| signal-system | 506 | 665 | 28 | 1 | `9d54591` |
| meta-signal-agent | 484 | 280 | 34 | 1 | `062e026` |
| signal-introspect | 482 | 472 | 32 | 1 | `6562579` |
| signal-agent | 456 | 330 | 38 | 1 | `e0ca33e` |
| version-projection | 439 | 145 | 24 | 1 | `f00b239` |
| signal-version-handover | 438 | 111 | 40 | 1 | `0032435` |
| meta-signal-version-handover | 330 | 252 | 32 | 1 | `78380dc` |
| meta-signal-persona | 325 | 216 | 35 | 1 | `e7f98a3` |
| nota-config | 279 | 229 | 23 | 1 | `ba689f0` |
| signal-derive | 268 | 0 | 24 | 1 | `5d6c80c` |
| meta-signal-terminal | 263 | 217 | 39 | 1 | `7a13ba0` |
| meta-signal-mind | 241 | 122 | 35 | 1 | `d10cbe9` |
| meta-signal-spirit | 160 | 282 | 47 | 1 | `07cd681` |
| meta-signal-repository-ledger | 134 | 130 | 33 | 1 | `e7e92e5` |
| meta-signal-message | 119 | 0 | 0 | 0 | `4fcf22a` |
| meta-signal-harness | 118 | 0 | 0 | 0 | `c8cd8b4` |
| meta-signal-introspect | 120 | 0 | 0 | 0 | `5518b8d` |
| meta-signal-system | 120 | 0 | 0 | 0 | `a819ba8` |
| meta-signal-criome | 98 | 0 | 0 | 0 | `1181edb` |
| nexus-cli | 87 | 0 | 27 | 1 | `8b7892a` |
| persona-pi | 0 | 0 | 38 | 1 | `d25cc43` |

### Non-Persona-core (adjacent / vendored — excluded from stack totals)

| Repo | Prod | Test | Note |
|---|---:|---:|---|
| kameo | 23242 | 0 | vendored actor-runtime fork |
| whisrs | 14925 | 0 | adjacent (speech) |
| chroma | 4472 | 1580 | system-operator visual/scheduler |
| substack-cli | 3053 | 468 | adjacent CLI |
| clavifaber | 2432 | 1137 | adjacent |
| hexis | 1987 | 1146 | adjacent |
| chronos | 1311 | 597 | adjacent |
| mentci-egui | 830 | 0 | adjacent |
| arca | 715 | 0 | adjacent |
| WebPublish | 564 | 0 | adjacent |
| brightness-ctl | 293 | 0 | adjacent |
| forge | 199 | 0 | criome-stack executor (future) |

## Cluster map (workflow fan-out)

1. **schema-core** — schema-next, schema-rust-next, nota-next, nota-config
2. **wire-storage** — sema, sema-engine, signal, signal-derive, signal-frame, signal-sema, version-projection, triad-runtime
3. **spirit** — spirit, signal-spirit, meta-signal-spirit, persona-spirit
4. **mind-orchestrate** — mind, signal-mind, meta-signal-mind, orchestrate, signal-orchestrate, meta-signal-orchestrate
5. **router-message** — router, signal-router, meta-signal-router, message, signal-message, meta-signal-message
6. **terminal-harness** — terminal, terminal-cell, signal-terminal, meta-signal-terminal, harness, signal-harness, meta-signal-harness
7. **introspect-system** — introspect, signal-introspect, meta-signal-introspect, system, signal-system, meta-signal-system
8. **persona-agent** — persona, signal-persona, meta-signal-persona, agent, signal-agent, meta-signal-agent, persona-pi
9. **criome-ledger-upgrade** — criome, repository-ledger, upgrade, their signal/meta-signal triads, version-handover signals
10. **cloud-domain** — cloud, domain-criome, their signal/meta-signal triads
11. **nexus-vocab** — nexus, nexus-cli
12. **lojix-criomos-migration** (special) — lojix, signal-lojix, meta-signal-lojix, lojix-cli, horizon-rs, criomos-horizon-config, CriomOS{,-home,-lib}, goldragon + `~/wt` worktrees
13. **schema-engine verdict** (special) — authoritative grammar-overhaul + nota-encoding-divergence read
14. **skills-corpus** — `/home/li/primary/skills/`
