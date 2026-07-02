# Field Readiness — Build Readiness (11)

Recon worker, 2026-07-02, host ouranos. Completes the sweep that stalled in
`reports/persona-system-audit/25-build-readiness-partial.md`. Scope: can the
whole persona/criome engine build from clean through Nix, and what would stall
a sustained Fable 5 build-test loop. Recon only: no source fixed, nothing
committed by this worker.

## VERDICT

Yes — every component of the minimal runnable whole builds warm in 6–110s
through the prometheus remote builder, and the whole-OS closure is essentially
fully cached — EXCEPT the whole-engine gate itself: persona's nix-built
topology checks and `persona-dev-stack` cannot even instantiate today (stale
fenix rust-stable FOD), and the entire build field hangs on one host.

## WITNESSED FACTS (command → observed result)

Field:

- `nix config show` — `max-jobs = 1`, `cores = 2`, `builders = @/etc/nix/machines`,
  `builders-use-substitutes = true`; substituters: the prometheus cache
  (priority 30) then cache.nixos.org; a github.com access token is configured
  (value withheld). `/etc/nix/machines` — exactly one builder:
  `ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux … 6 10 big-parallel,kvm`.
- `curl …/nix-cache-info` on the prometheus cache — HTTP 200 in 13–30 ms.
- Forced remote probe (`nix build --max-jobs 0` on a fresh trivial drv) —
  dispatched to prometheus and returned in 1s. Remote building works through
  the daemon. (Direct `ssh nix-ssh@prometheus` as user li is denied — the
  daemon's key, not the user's, carries the builder path.)
- `df -h /` — 433G free; `du -sh /nix/store` — 139G. No disk pressure.
- `nproc` 14, 30G RAM locally; `id -nG` shows li in `nixdev` (a
  `trusted-users` group), so local `--max-jobs`/`--cores` override is available
  as a degraded fallback if prometheus is out.
- `gh repo view` on spirit and nota-next — PUBLIC. GitHub auth is a rate-limit
  nicety, not a fetch gate.

Eval sweep (32 repos, `nix eval .#packages/.#checks.x86_64-linux --apply
builtins.attrNames`, each timed; full table in scratchpad TSV, summarized
below): every repo evaluated in ≤2s (warm eval cache) except the three
anomalies (forge, mentci, CriomOS) described below.

Build sweep (real `nix build`, sequential, timed):

| target | result | wall time |
| --- | --- | --- |
| nota-next#default | OK (remote, output copied back) | 6s |
| signal-frame#default | OK | 10s |
| schema-rust-next#default | OK | 9s |
| message#default | OK | 7s |
| router#default | OK | 55s |
| harness#default | OK | 18s |
| criome#default | OK | 64s |
| spirit#default (dirty tree, 8 drvs) | OK | 110s |
| persona#default (28 drvs + 31 fetches) | OK | 84s |

- `nix build message#default --rebuild` (forced full recompile of the final
  crate, deps cached) — 24s. This is the steady-state edit-loop floor for one
  daemon.
- `nix flake check` on message, everything cached — "all checks passed" in 17s
  (warm no-op gate).
- Whole OS: `nix build CriomOS#nixosConfigurations.target.config.system.build.toplevel`
  with `--override-input` pointing at the lojix-materialized inputs under
  `/var/lib/lojix/generated-inputs/goldragon/ouranos/full-os/{system,horizon,deployment,secrets}`
  — evaluates in 47s cold (0s warm) and needs only 26 derivations, all small
  config/unit/activation wiring, zero compiles.
- CriomOS-test-cluster: 13 checks evaluate instantly, incl. 4 `vm-<node>`
  runNixOSTest checks; `vm-dune --dry-run` — nothing to build or fetch (fully
  realized), confirmed in 14s.
- CriomOS-home: `pi`, `mentci`, `whisrs` packages — dry-run 0 to build (the
  external `pi` LLM runtime IS packaged and cached; report 20's "UNKNOWN where
  packaged" is answered: CriomOS-home#pi).

Failures / anomalies (witnessed):

- `nix build persona#persona-dev-stack --dry-run` — FAILS at instantiation:
  `hash mismatch in fixed-output derivation …channel-rust-stable.toml.drv`
  (specified sha256-gh/xTkx…, got sha256-h+t2xTB…). persona/flake.nix:85 uses
  `fenix.packages.${system}.stable`; persona's flake.lock pins fenix at
  2026-05-05. The rust stable channel manifest moved under the pin.
- `nix build persona#checks.x86_64-linux.persona-daemon-launches-nix-built-prototype-topology --dry-run`
  — FAILS with the SAME FOD mismatch. This check is the whole-engine gate (the
  supervisor launching the nix-built 8-component topology).
- CriomOS: `packages` evaluates (formatter, llama-cpp-strix-halo) but `checks`
  (and `nix flake show`) throw `CriomOS: no system input was provided` — by
  design; the `system` input is a throwing stub until materialized (the error
  text itself documents the deploy-materialization tool). Confirms report 25's
  first finding.
- forge: flake exposes ONLY `devShells` — no packages, no checks
  (`nix flake show forge` witnessed). Confirms and closes report 25's second
  finding: any "forge checks pass" result is vacuous.
- mentci: NO flake.nix at all (has a `target/` dir — plain-cargo development).
  It is packaged from a flake *input* (`mentci-src`) inside CriomOS-home.
- Fenix lock ages across repos (flake.lock): persona 2026-05-05, harness
  2026-05-12, message/spirit/router 2026-06-19. 18 of 28 component repos carry
  their own fenix pin; only 10 go through the shared rust-build policy
  (grep across component flake.nix files).
- mind: 6 `ssh://` deps in Cargo.toml, 8 in Cargo.lock, plain crane vendoring,
  no `[patch]` rewrite — vendoring on a cache miss needs the evaluating user's
  SSH auth. Today mind is fully realized (dry-run: 0 to build), so it hides.
- spirit checkout is dirty: 8 modified files including Cargo.lock, flake.lock,
  src/engine.rs (git status, read-only). All other key checkouts clean at
  origin heads; router and spirit sit on `criome-authorization-push`, the rest
  on main.

## INFERENCES (separated)

- The 6–10s "builds" are prometheus returning outputs it already holds for
  current main revs — the remote store doubles as a hot cache; 24s
  (`--rebuild`) is the honest per-edit floor, 55–110s for the big daemons.
- persona#default escapes the fenix FOD only because its exact drv shapes are
  already realized on prometheus; any persona surface needing re-realization of
  the toolchain manifest (dev-stack, the topology checks, and eventually any
  edited persona source on a machine without the cached closure) fails the same
  way. The pin is a time bomb with the fuse already burnt on two surfaces.
- Post-edit full `nix flake check` on the wide repos (router ~44 checks,
  mind ~60, persona ~120) recompiles every cargoTest drv against the new
  source and would take tens of minutes per iteration; the loop should build
  the one check that proves the edit (testing skill) and reserve full checks
  for the pre-commit gate.

## PER-COMPONENT BUILD TABLE

builds = witnessed `nix build` green; cached = dry-run showed 0 drvs to build;
dry-N = dry-run showed N drvs to build (not built by this sweep). remote/cache
column: all builds go through prometheus by config (local max-jobs=1).

| component | builds? | time | manual step | needs remote/cache |
| --- | --- | --- | --- | --- |
| nota-next | builds | 6s | none | remote (warm) |
| signal-frame | builds | 10s | none | remote (warm) |
| triad-runtime | dry-1 | — | none | remote |
| schema-next | dry-1 | — | none | remote |
| schema-rust-next | builds | 9s | none | remote (warm) |
| sema | dry-1 | — | none | remote |
| sema-engine | dry-1 | — | none | remote |
| message | builds; forced recompile 24s; warm flake check 17s | 7s | none | remote |
| router | builds | 55s | none | remote |
| harness | builds | 18s | none; fenix pin 05-12 is next-oldest (latent K2) | remote |
| terminal-cell | cached | — | none | — |
| persona#default | builds | 84s | none | remote |
| persona#persona-dev-stack | FAILS instantiation | — | fenix lock update required | — |
| persona nix-built-topology checks | FAIL instantiation | — | same fenix fix | — |
| mind | cached | — | SSH auth needed at vendoring on any cache miss | — |
| introspect | dry-1 | — | none | remote |
| system | dry-8 | — | none | remote |
| orchestrate | dry-6 | — | none | remote |
| upgrade | dry-1 | — | none | remote |
| listener | cached | — | none | — |
| agent | dry-1 | — | none | remote |
| spirit | builds (dirty tree) | 110s | dirty checkout needs disposition | remote |
| criome | builds | 64s | none | remote |
| mirror | dry-1 | — | none | remote |
| repository-ledger | cached | — | none | — |
| lojix | cached | — | none | — |
| cloud | dry-13 (+47 fetch) | — | none | remote+cache |
| domain-criome | dry-1 | — | none | remote |
| nexus / nexus-cli | dry-1 / dry-6 | — | none | remote |
| forge | NOT BUILDABLE (devShells only) | — | needs a package output to participate | — |
| mentci | no flake; via CriomOS-home#mentci (cached) | — | repo itself not Nix-buildable | — |
| CriomOS (whole OS) | eval+dry OK via lojix inputs: 26 trivial drvs | 47s eval | requires materialized `system` (+3) inputs — bare eval throws | cache (warm) |
| CriomOS-home (pi, mentci, whisrs) | cached | — | none | — |
| CriomOS-test-cluster vm-dune | cached (fully realized) | — | VM checks need kvm (prometheus has it) | remote kvm |

## WHY THE PRIOR SWEEP STALLED

Report 25 dies mid-sentence after two findings ("Let me confirm forge's actual
flake outputs, then finalize") — a context/session death, not a tool failure.
The two findings it did land are exactly `nix flake show` / `nix flake check`
shaped, and those commands are the stall mechanism: foreground
`nix flake show`/`check` on these repos streams enormous per-attribute eval
output (persona alone enumerates ~120 checks; CriomOS throws mid-show), and
`nix flake check` on a cache-missing repo silently becomes an hours-long build
with logs flooding the worker's context. A serial foreground sweep of ~30
repos does not fit in one worker. The sweep completed this time because
evals/dry-runs went first (seconds each), all output went to scratchpad files,
and real builds ran sequentially in a background task. That method difference
is itself a field finding (K10): a whole-engine build sweep is only
context-survivable as dry-run-first + background builds + logs-on-disk.

## KINK LEDGER

K1. Whole-engine gate un-instantiable: stale fenix stable-manifest FOD.
- Where: persona flake.lock (fenix 2026-05-05) + persona/flake.nix:85
  (`fenix.packages.…stable`); breaks `persona-dev-stack` and every
  `persona-daemon-launches-nix-built-*` check.
- Blast radius: the sustained session's primary loop target — "build, launch,
  test the 8-component topology through Nix" — is dead on arrival; only
  already-realized shapes still copy back.
- Likelihood: certain (witnessed twice).
- Fix: update persona's fenix lock (or move persona onto rust-build's shared
  toolchain), rebuild, absorb any new-stable clippy fallout across persona's
  component-input closure.
- Class: NEEDS-A-BEAD (lock bump cascades a fleet rebuild and possible lint
  fallout; not a one-liner in effect).
- Evidence: dry-run hash-mismatch on `channel-rust-stable.toml.drv` for both
  surfaces; fenix lock date from flake.lock.

K2. Toolchain-pin fragmentation: 18/28 component repos carry their own fenix
pin aging independently (harness 05-12 next in line); same FOD bomb latent
per-repo on any cache miss / GC / fresh machine.
- Blast radius: random component builds start failing at instantiation over
  time, each looking like a fresh mystery.
- Likelihood: high over a multi-week session.
- Fix: converge component flakes on rust-build (it exists for exactly this) or
  institute a periodic coordinated lock refresh.
- Class: NEEDS-A-BEAD (cross-repo policy change).
- Evidence: grep of 28 component flake.nix files; fenix lock dates.

K3. Single-host build field: prometheus is at once the only remote builder,
the only project binary cache, the kvm VM-test host, AND the lojix
deploy-experiment target (the one recorded lojix production deploy is to
prometheus — report 24).
- Blast radius: a bad deploy experiment or outage on prometheus stalls every
  build loop on every machine; local fallback is laptop-class and configured
  down to max-jobs=1/cores=2 (trusted-user override possible but slow).
- Likelihood: moderate — deploy experiments to prometheus are precisely what
  the sustained session will do.
- Fix: none — single-host concentration on prometheus is intended BY DESIGN
  and accepted (no other host is suitable). Operating care only: dry-run heavy
  builds first to see the miss surface and spot degradation early.
- Class: ACCEPTED CONDITION (not a defect; no bead).
- Evidence: /etc/nix/machines single line; nix.conf; report 24 deploy state.

K4. mind vendors 8 `ssh://` git deps with plain crane — cache-miss vendoring
requires interactive SSH auth; fails hermetic/CI/fresh contexts. Repos are
public; ssh buys nothing.
- Blast radius: first source edit to mind in the session hits it.
- Likelihood: high if mind is touched, hidden until then (fully cached today).
- Fix: repoint Cargo.toml deps to https, relock.
- Class: NEEDS-A-BEAD (source + lock change, wire-compat retest per report 20
  pin fragmentation).
- Evidence: grep counts in mind Cargo.toml/Cargo.lock; mind flake uses bare
  craneLib without [patch] rewrites.

K5. CriomOS bare eval throws (by design): `nix flake check`/`show` dead-end
with the no-system stub error unless the materialized inputs are passed.
- Blast radius: minutes lost per naive attempt; a worker not knowing the
  override recipe treats the OS as unbuildable.
- Likelihood: certain for any fresh worker.
- Fix: the working recipe is witnessed above (lojix generated-inputs +
  --override-input); record it in CriomOS agent docs.
- Class: CHEAP-SAFE (doc edit).
- Evidence: throw witnessed; override eval witnessed at 47s/26 drvs.

K6. forge is Nix-invisible (devShells only) and mentci has no flake.
- Blast radius: sweeps and gates silently skip them; "all repos build" claims
  are vacuously wrong; forge is the intended build-authorization component
  (report 24 K8) yet cannot itself be built.
- Likelihood: certain (structural).
- Fix: forge needs package/check outputs (bead); mentci is deliberately
  packaged via CriomOS-home — a doc note in mentci README suffices (cheap).
- Class: forge NEEDS-A-BEAD; mentci CHEAP-SAFE.
- Evidence: flake show forge; mentci ls.

K7. spirit checkout dirty (8 files incl. Cargo.lock + flake.lock) on
`criome-authorization-push`.
- Blast radius: the engine's most active component builds from unpushed local
  state; a fresh clone or remote builder-only flow produces different bits;
  sweep timing (110s, 8 drvs) partly reflects this.
- Likelihood: certain until dispositioned.
- Fix: owner decision — commit or discard; not a recon call.
- Class: NEEDS-A-BEAD (disposition tracking).
- Evidence: git status (read-only).

K8. Post-edit full `nix flake check` on wide repos is a loop-killer by width:
router ~44 / mind ~60 / persona ~120 checks, each a cargoTest drv recompiled
per source change.
- Blast radius: an edit-check loop naively gated on full flake check spends
  tens of minutes per iteration.
- Likelihood: high for a worker not applying the testing skill's
  narrow-check-first rule.
- Fix: loop on `nix build .#checks.x86_64-linux.<the-one-check>`, full check
  only pre-commit. Practice note, no defect.
- Class: CHEAP-SAFE (practice/doctrine note).
- Evidence: check counts from eval sweep; warm no-op check 17s (message).

K9. Residual (not re-verified here): cargo git-dep rev fragmentation across
consumers (report 20 obstacle 1) — per-repo Nix builds all pass regardless;
the risk is runtime wire mismatch, not build failure. Carried forward, not a
build kink.

K10. Sweep method: whole-engine build recon only survives one worker context
as dry-run-first + background builds + logs-on-disk (see stall analysis).
- Class: CHEAP-SAFE (provisional practice recommendation for the field
  doctrine; not recorded as authority by this worker).

## CHECKS SKIPPED

- Did not build: the dry-N components (triad-runtime, schema-next, sema,
  sema-engine, introspect, system, orchestrate, upgrade, agent, mirror,
  domain-criome, nexus, nexus-cli, cloud) — dry-runs show deps fully cached
  and 1–13 final drvs each; building all was time-redundant given nine
  representative greens including the heaviest.
- Did not run any VM test (vm-dune is fully realized; executing it is a
  test-run concern, not build readiness) and did not build
  CriomOS#llama-cpp-strix-halo (large model build, no session need shown).
- Did not attempt a cold-eval-cache or cold-store measurement (would require
  GC or a fresh machine; out of recon scope).
- Spirit queries: none needed for build-surface judgment; no intent records
  consulted (mechanical recon per brief).
