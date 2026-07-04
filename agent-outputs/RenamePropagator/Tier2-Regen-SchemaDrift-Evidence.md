# Tier2 Regen — SCHEMA-DRIFT set — evidence (extends primary-5kxh / primary-qipw)

Session: RenamePropagator. Role: General Code Implementer (Claude Opus 4.8, 1M).
Date: 2026-07-04. Scope: regenerate the CHECKED-IN generated artifacts
(`src/schema/*.rs`) for W1's schema-drift set (the 11 + the 2 swept), which W1
left stale on purpose after fixing only the schema SOURCE. Those stale artifacts
trip each crate's `build.rs` freshness gate (`StaleGeneratedArtifact`). This is
the regen slice that closes the coupling gap the Cloud-Stage evidence proved
(`cloud` composed build failing on `signal-domain-criome@00f43ba8` +
`signal-cloud@988c769d` StaleGeneratedArtifact).

Producer baseline (regenerated against): `schema-rust@drop-next 7f746c02`,
`schema@drop-next a393c8c8`, `nota@main bea7e284`. Same regen mechanism W2 used.
NO migration `main` touched anywhere. `drop-next` only.

## Mechanism (identical to W2 / primary-qipw)

Each crate's `build.rs` runs `schema_rust::…GenerationDriver…generate()` and
gates the checked-in `src/schema/*.rs` via `write_or_check("<CRATE>_UPDATE_
SCHEMA_ARTIFACTS")`. Per repo:

1. `jj new drop-next -m '…'` — fresh commit on top of W1's schema-source fix.
2. Regenerate: `<VAR>=1 cargo build --locked` (writes the artifact).
3. Idempotency: second `<VAR>=1 cargo build --locked` (byte-stable) — and, more
   authoritatively, the drift check below re-derives the artifact in check mode.
4. DRIFT CHECK (own freshness gate, check mode): `cargo clean -p <crate> &&
   cargo build --locked` with the var UNSET → exit 0, no `StaleGeneratedArtifact`
   panic. This is the direct proof the OWN gate clears: the gate only exits 0 if
   the checked-in artifact is byte-identical to the generator's output.
5. `jj bookmark set drop-next -r @` → `jj git push --bookmark drop-next`.
6. Confirm `main@origin` unchanged.

Each repo claimed via Orchestrate lane `schema-drift` before editing, released
after. All work in the canonical `/git/github.com/LiGoldragon/<repo>` checkouts;
no stray workspaces.

## Cascade structure (why lock bumps were needed, roots first)

W1's cascade consumers still pinned the PRE-fix producer sibling revs in their
`Cargo.lock` (the synchronizer had NOT re-locked them since W1's schema fixes):
e.g. `signal-domain-criome@3aca3282`, `signal-cloud@c50af899`,
`signal-lojix@4db768af`, `meta-signal-lojix@74a7c71e`,
`meta-signal-upgrade@92825f31`, `signal-upgrade@e88082ed`. A plain
`cargo build --locked` on a consumer therefore fails FIRST on the stale sibling
(retired schema at the pre-fix rev). So — exactly as W2 did — I regenerated the
ROOTS first, pushed them, then bumped each consumer's `Cargo.lock`
(`cargo update -p <dep>`) to the regenerated root tips (now the `drop-next`
HEADs) before regenerating the consumer's own artifact. With fresh checked-in
sibling artifacts, the sibling gates pass in check mode and only the consumer's
own gate is under test.

Dependency tiers (in-scope siblings only):
- Roots: signal-domain-criome, signal-cloud, signal-upgrade, meta-signal-upgrade,
  signal-lojix.
- Tier 1: meta-signal-domain-criome→SDC; meta-signal-cloud→SC,SDC;
  meta-signal-lojix→SL.
- Tier 2: domain-criome→SDC,MSDC; lojix→SL,MSL; upgrade→SU,MSU.
- meta-signal-persona: own lock already at the producer baseline; its dep
  signal-persona@9d03892f compiles clean against schema-rust@7f746c02 (checked-in
  artifact coincidentally already fresh), so NO lock bump was needed.

## Per-repo disposition — REGENERATED + OWN GATE CLEARS (drop-next only)

Every artifact below was GENUINELY stale (md5 changed on regen). Every OWN
freshness gate now passes (drift check `cargo clean -p X && cargo build --locked`,
no var → exit 0). Every `main@origin` UNCHANGED.

| repo | tier | drop-next before (W1) → after (regen) | artifact md5 stale→fresh | Cargo.lock bump | own gate (drift check) | main (unchanged) |
|---|---|---|---|---|---|---|
| signal-domain-criome | root | 00f43ba8 → **ce3b2a6d** | lib.rs 301e93ef→4a1ea9b5 | none | exit 0 | 44af33cf |
| signal-cloud | root | 988c769d → **3f1e7321** | lib.rs 5130e2c9→7981d517 | none | exit 0 | 3482cbeb |
| signal-upgrade | root | b8b3f818 → **ad93b007** | lib.rs 3ce2698a→b75b4ae8 | none | exit 0 | 571bc8b8 |
| meta-signal-upgrade | root | 003bef5b → **69431bff** | lib.rs 8e1f3e0a→ae2f278d | none | exit 0 | 91e78ad9 |
| signal-lojix | root | 43a97e15 → **64d714dc** | lib.rs 4a54001c→550b7500 | none | exit 0 | fbb28cf4 |
| meta-signal-domain-criome | 1 | 2d7f63a4 → **8266c2ec** | lib.rs 13f940ff→1e3dff46 | SDC→ce3b2a6d | exit 0 | 4f12e3a4 |
| meta-signal-cloud | 1 | 4b95bc7e → **d3802cde** | lib.rs 67d5b296→82bbf606 | SC→3f1e7321, SDC→ce3b2a6d | exit 0 | f4cf84e5 |
| meta-signal-lojix | 1 | 381f71b6 → **546910d0** | lib.rs 938ff6db→0b3012ba | SL→64d714dc | exit 0 | 4a8e7911 |
| domain-criome | 2 | 9ed98cc2 → **fcc8284b** | daemon 53ed8a7b→bd62d6a0; nexus 5273a204→49dbbaa1; sema abfe6c86→c6bbfc30 | SDC→ce3b2a6d, MSDC→8266c2ec | exit 0 (crate compiled FULLY green) | ac77e3fd |
| lojix | 2 | c9344e1b → **7a7ffabf** | nexus 6994da6a→4ca48196; sema b0586160→b942f1ef | SL→64d714dc, MSL→546910d0 | exit 0 (crate compiled FULLY green) | 9f42435f |
| upgrade | 2 | 70d15dcb → **66f8d01c** | lib.rs e3a490d4→48d06ee2 | SU→ad93b007, MSU→69431bff | exit 0 (crate compiled FULLY green) | 5098cbae |
| meta-signal-persona | (baseline) | 2cfc27a5 → **4133f1e9** | lib.rs c0599c43→3921a721 | none (already baseline) | exit 0 | 62944272 |

`persona` — **SKIPPED, confirmed out of scope.** Its `schema/daemon.schema` is
empty (`{}` imports / `[]` `[]` / `{}` structs → no schema-derived types), and its
`drop-next` tip `f2149c0e` still pins `nota-next` + `schema-rust-next@main`
(cad9ec27) — i.e. persona's drop-next is PRE-rename and is NOT a
`schema-rust@drop-next` consumer at all. There is no artifact to regenerate
against the producer baseline; regenerating it would be wrong. `main@origin`
ac629103 unchanged.

## No further pre-existing issues surfaced

Unlike W2's pass (which surfaced `terminal`'s WirePath/ComponentName `.as_ref()`
gap and `meta-signal-orchestrate`'s stale schema-contract test counts), clearing
the artifact gate on THIS set surfaced NO additional non-rename defect. Every
repo's regen was a clean artifact rewrite (plus the necessary Cargo.lock sibling
bump on cascade repos); three of the tier-2 crates (domain-criome, lojix,
upgrade) compiled FULLY green (past their own gate AND all deps) in the local
drift check, and every tier-0/1 repo's own gate cleared. Honest statement: I did
not observe any masked-through problem on this set.

## W1's lojix BLOCKER — RESOLVED

W1 flagged that `lojix` could not reach green because its cascade dep
`signal-lojix` (and `meta-signal-lojix`) carried the same retired drift and were
masked. The sweep worker fixed those schema sources (signal-lojix 43a97e15,
meta-signal-lojix 381f71b6). This pass regenerated their artifacts
(signal-lojix→64d714dc, meta-signal-lojix→546910d0) and bumped lojix's lock to
them; `lojix` then compiled FULLY green (exit 0). The lojix blocker is cleared.

## Cloud-Stage gap — the two named deps now clear their gate

Cloud-Stage-Evidence proved `cloud`'s composed build failed on
`signal-domain-criome@00f43ba8` + `signal-cloud@988c769d` StaleGeneratedArtifact.
Both are regenerated here (SDC→ce3b2a6d, SC→3f1e7321) and clear their own gate.
Durable authoritative confirmation: prometheus nix build of
`signal-domain-criome@ce3b2a6d#packages.x86_64-linux.default` — see below.
NOTE (out of my edit scope): `cloud`'s own `Cargo.lock` still pins the pre-regen
SDC/SC tips (00f43ba8 / 988c769d); cloud will go composed-green once its lock is
bumped to ce3b2a6d / 3f1e7321 at the convergence re-lock. I did NOT touch `cloud`.

## Authoritative nix build (durable evidence)

`nix build github:LiGoldragon/signal-domain-criome/ce3b2a6d#packages.x86_64-linux.default`
driven from THIS credentialed machine with prometheus as the remote builder
(local FOD vendor fetch → remote compile), matching the mentci-egui/cloud
workaround for the prometheus private-repo credential gap.

RESULT: **GREEN, exit 0.** In the clean crane sandbox the crate's `build.rs`
ran fresh with NO `StaleGeneratedArtifact` panic (the OWN freshness gate clears
authoritatively), buildPhase + checkPhase (`cargo test`) + install all green,
output `/nix/store/qfc1i2ap76kcmjvmjca6chsicci28sqa-signal-domain-criome-0.1.0`
built on prometheus (remote builder) and copied back. This durably closes the
StaleGeneratedArtifact gate on the exact dep Cloud-Stage named first.

`signal-cloud@3f1e7321#packages.x86_64-linux.default` (the second Cloud-Stage dep)
prometheus nix build: **GREEN, exit 0** — build.rs fresh, no StaleGeneratedArtifact,
checkPhase green, output
`/nix/store/whpv9scczgry7wf00k442p7k8bk5h6zg-signal-cloud-0.1.0` (built on
prometheus, copied back). Both deps Cloud-Stage named now durably clear their gate.

## Build-environment note

All regen + drift checks were LOCAL `cargo build --locked` in each canonical
checkout (the regen writes the artifact into the working copy; the freshness gate
is self-contained in build.rs and needs only schema-rust + the crate's own
schema/ sources). The authoritative composed green is the prometheus nix build,
driven from this machine as remote builder (a direct `ssh prometheus nix build`
of uncached private deps fails on the known prometheus credential gap).

## Safety

No migration `main` moved. Every push was `jj git push --bookmark drop-next`.
All 12 repos' `main@origin` verified byte-identical to session-start recon
(sweep at closeout). Each repo claimed via Orchestrate lane `schema-drift`,
released after. `cloud` (peer claim, just done), `mind`/`spirit` (peer-held),
W2's 6 regen repos, and `repository-ledger`/`signal-repository-ledger` were NOT
touched. Zero project data on any public surface.
</content>
</invoke>
