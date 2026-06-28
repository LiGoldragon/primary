# Spirit Mentci Removal — Implementation Evidence

## Task and scope

Remove the stray `mentci` dependency from the spirit repo (CODE repo at
`/git/github.com/LiGoldragon/spirit`, jj-colocated) so the deploy artifact
`nix build .#packages.default` builds offline. Do NOT vendor mentci. Land to
`main` only after the offline build is green.

## Cleanup (prior agent's vendoring discarded)

- Spirit `main` HEAD at start: `3738eeab` (version 0.18.0). jj working-copy
  commit `pspokurw 171fe37b "vendor mentci family offline like its siblings"`
  carried uncommitted edits to `flake.nix` (+47) and `flake.lock` (+72) that
  ADDED `mentci`/`mentci-lib`/`signal-mentci`/`meta-signal-mentci` as flake
  vendor inputs + cargo `[patch]` stanzas.
- `jj abandon @` discarded that change; `@` reset to a fresh empty child of
  main. Verified clean: `jj st` = "no changes"; `git diff 3738eeab` (flake.nix,
  flake.lock) = empty. Tree == main before edits.

## Removed (mentci out of spirit)

Changed files in the working tree:

- `Cargo.toml`:
  - Deleted the `[[test]] mentci_criome_intercept_policy_e2e` block.
  - Deleted dev-deps `mentci`, `meta-signal-mentci`, `signal-mentci`.
  - Deleted dev-dep `meta-signal-criome` (see "meta-signal-criome" below).
- `tests/mentci_criome_intercept_policy_e2e.rs`: deleted (sole consumer of the
  mentci family + meta-signal-criome).
- `Cargo.lock`: regenerated offline (`cargo metadata --format-version 1
  --offline`). Diff vs `3738eeab` removes exactly the four packages
  `mentci`, `mentci-lib`, `meta-signal-mentci`, `signal-mentci`; no additions,
  no retained-pin changes.
- `flake.nix`: untouched. On clean main it had NO mentci references (the prior
  agent's vendoring was discarded). The `meta-signal-criome` vendor input +
  `[patch]` stanzas are intentionally LEFT: `criome` (0.4.2, still in the lock
  as an optional dep) declares meta-signal-criome, so it must stay vendored for
  any `mirror-shipper` build.

Grep clean: `grep -ri mentci` over the repo returns only `INTENT.md` lines
249/251/259 — design-doctrine prose about future mentci-mediated acceptance
gating. That is psyche-backed recorded intent, not load-bearing for the build;
left untouched (flagged below).

### meta-signal-criome (necessary scope note)

`meta-signal-criome` was a dev-dependency used ONLY by the deleted mentci e2e
test (`grep -rln meta_signal_criome tests/ src/` = only that file; no vendored
crate depends on it). It is also a pre-existing OFFLINE-build co-blocker: the
flake vendors meta-signal-criome `0.2.0` while `Cargo.lock` pins `0.3.0` (rev
4814625a) — a flake.lock-vs-Cargo.lock version skew. As a NON-optional dev-dep
it was always resolved under crane's `--all-targets`, so cargo tried to update
its git index and failed in the network-less sandbox (this is the second
blocker after mentci; mentci just failed first). Removing the now-dead dep
sidesteps the skew without touching flake.lock. `criome`/`signal-criome` carry
the same skew but are optional behind `mirror-shipper` (dormant in the default
build), and cargo reconciles them offline against the vendored sources.

## Build proof — `nix build .#packages.default` (offline)

`packages.default = combinedPackage` (links spirit, meta-spirit, spirit-daemon,
spirit-write-configuration, spirit-render, spirit-migrate-store). Deploy-binary
features: daemon `--features agent-guardian --bin spirit-daemon`; the others
`--features nota-text`/`production-migration`. None activate `mirror-shipper`,
so the criome family stays dormant.

Command: `nix build .#packages.x86_64-linux.default --print-build-logs`
(remote builder `prometheus.goldragon.criome`; crane `buildDepsOnly` runs in a
network-less sandbox = the offline proof).

Result: BOTH `spirit-deps-0.18.0` caches (nota-text + agent-guardian) compiled
and installed offline with NO git fetch — the meta-signal-criome
"unable to update ... github.com" failure is gone. The only remaining notice is
the benign `warning: patch meta-signal-criome v0.2.0 ... was not used in the
crate graph` (criome dormant). Test binaries compiled include
`criome_gate_1of1`, `guardian_live_scenarios`, `mirror_shipper`,
`process_boundary` — and NO mentci test. Final binary packages compiling/green.

FINAL: `NIX_EXIT=0` (green). Result store path
`/nix/store/ah6gjj99vwvml18k25qhc5zk3xzqcbfb-spirit`. `result/bin/` contains
`spirit`, `meta-spirit`, `spirit-daemon`, `spirit-migrate-store`,
`spirit-render`, `spirit-write-configuration`. `bin/spirit-daemon` is a
4.9 MB ELF resolving to
`/nix/store/qjy8hamy9zlzki6yn961i5nq06dlhml2-spirit-0.18.0/bin/spirit-daemon`.
This is the literal deploy derivation built through the network-less crane
sandbox — cargo-only evidence was not relied on.

## Versioning

No bump. This is a dev-dependency/test removal plus a regenerated lock; it does
not change the deployed daemon's behavior, wire contract, storage schema, or any
public surface (dev-deps never enter the daemon binary). Per the repo's
convention (recent bumps were all for behavior/contract changes), spirit stays
`0.18.0`.

## Coverage flag / blockers / follow-ups

1. COVERAGE: deleting `tests/mentci_criome_intercept_policy_e2e.rs` drops the
   e2e that witnessed "a guardian-allowed spirit operation parks in criome
   (ClientApproval) and is approved through mentci." The criome gate itself
   (`src/criome_gate.rs`) retains `tests/criome_gate_1of1.rs`; the guardian
   retains `tests/guardian_live_scenarios.rs`. The lost coverage is the
   criome-parking + mentci-approval integration, which inherently requires
   mentci (being removed). No replacement written (per brief).
2. INTENT.md mentci prose (lines 249/251/259): recorded design intent about
   future mentci-mediated gating. Left verbatim (not an implementer's call to
   rewrite psyche intent). Lead/psyche to decide whether to revise now that the
   mentci path is removed.
3. SCOPE: `meta-signal-criome` removal exceeds the literal "mentci-family" list
   in the brief. It was dead (only the deleted test used it) AND the active
   offline-build blocker, so removing it was necessary for the green build.
   Flag for lead confirmation. Alternative (not taken): keep it and re-pin the
   flake.lock `meta-signal-criome-source` input to rev 4814625a (version 0.3.0)
   to clear the skew.
4. PRE-EXISTING SKEW (recommendation): spirit's `flake.lock` vendors OLDER
   criome-family revs than `Cargo.lock` pins (meta-signal-criome 0.2.0 vs 0.3.0;
   signal-criome 0.3.0 vs 0.5.0; criome similar). Dormant for the default
   deploy, but an OFFLINE `mirror-shipper` build (the 1-of-1 criome-gate witness
   or a shipper-enabled daemon) would activate criome/signal-criome and hit the
   same fetch-on-skew failure. Recommend the lead reconcile spirit's flake.lock
   criome-family inputs with Cargo.lock before any offline mirror-shipper
   build/deploy.

## Land

Committed and pushed AFTER the green offline build (operator-bookmark-until-
green honored — remote main was unchanged at `3738eeab` before the push).

- New spirit `main` HEAD: `a6d69b467e80f4c61c0d2e345e80c3b0023098b3`
  (jj change `sxopyxsz a6d69b46`), message
  "spirit: drop mentci + meta-signal-criome dev-deps + e2e for offline default
  build". Confirmed on `origin/main` via `git ls-remote`.
- Version: `0.18.0` (unchanged, per versioning rationale above).
- No consumer/home deploy flake.lock re-pinned. No daemon restarted. Deployment
  is a separate stage.
- Session-end orphan check `jj log -r 'main..@ ~ bookmarks()'` shows only the
  empty working copy — clean.
