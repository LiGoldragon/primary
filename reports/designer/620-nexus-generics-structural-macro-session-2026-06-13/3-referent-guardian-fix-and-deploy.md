# Referent-guardian fix + deploy — exact resumable state (Task #406)

In-flight when the session paused. This is the precise state to resume from.

## CORRECTION (restart 2026-06-13): the deploy path below is WRONG for ouranos

A deploy subagent verified the actual topology. `ouranos` does NOT deploy
spirit via standalone home-manager — `nix eval .#homeConfigurations` is empty
(CriomOS-home's `horizon` input defaults to the stub `path:./stubs/no-horizon`
with `horizon.users = {}`, so `homeConfigurations = mapAttrs ... horizon.users`
is empty). The live spirit user service is wired through the **NixOS system**
`CriomOS` (`/run/current-system` = `nixos-system-ouranos-26.05`), which consumes
CriomOS-home as flake input `criomos-home` and supplies the real `horizon`
(`CriomOS/modules/nixos/userHomes.nix`: `home-manager.users = mapAttrs ...`).
`CriomOS/flake.lock` pins `criomos-home` at `852ad939` (CriomOS-home main HEAD),
which resolves spirit at the OLD `a4cc858`.

The **real deploy path** (replaces "Resume steps" 1-2 below):
1. Commit + push the spirit-0.12.1 pin bump on **CriomOS-home main** (jj:
   commit → `jj bookmark set main -r @-` → `jj git push --bookmark main`).
   `nix flake lock --update-input spirit` moves spirit `a4cc858` → `f4635c3`
   and 5 spirit-only private sub-inputs (`agent-source`,
   `meta-signal-agent-source`, `schema-rust-next-source`, `signal-agent-source`,
   `signal-spirit-source`); no unrelated top-level input moves. NOTE
   `signal-spirit-source` changed → the daemon startup-config contract MAY have
   changed, so a bare systemd override reusing the old 269-byte config.rkyv is
   genuinely unsafe; regenerate the config (home-module path does this, or run
   `spirit-write-configuration` with the module's exact ConfigurationWriteRequest).
2. Bump `criomos-home` in **`CriomOS/flake.lock`** (`nix flake lock
   --update-input criomos-home`); verify spirit resolves to `f4635c3` there.
3. Rebuild + switch the **ouranos NixOS system** (`nixos-rebuild switch --flake
   /git/github.com/LiGoldragon/CriomOS#<target>` or the project deploy tool).
   This restarts the spirit user service with config regen + `spirit-migrate-store`.
4. Verify 5a/b/c (Version 0.12.1, read works, healthy). Rollback is a NixOS
   generation rollback (`nixos-rebuild switch --rollback`), not a home-manager
   activate — plus the `~/.local/state/spirit.bak-predeploy/` store restore.

This is `cluster-operator`/`system-operator` production-deploy territory (a full
system rebuild on the host the session runs on). The referent.md fix IS already
committed + pushed to spirit `origin/main` at `f4635c3` (that part is done).
Deploy-path choice is pending a psyche decision at restart.

## The flaw

Recording the universal-frame Principle with referent `[triad-runtime]` drew:
`(ReferentGuardianRejected (NonReferent … [triad-runtime is presented as a
design principle about shared canonical frames, not a concrete nameable
particular]))`. `triad-runtime` is a concrete repo/crate — a valid referent.
The referent-guardian judged the **record's abstraction** (a principle) instead
of the **name's denotation** (a crate), and clean-context it can't know
triad-runtime is real. This is a genuine referent-admission flaw (and a live
example of the guardian over-strictness the corpus-health work targets). The
psyche directed: don't drop the referent — fix the flaw, redeploy, re-submit.

## The fix (applied)

`spirit/src/guardian-prompts/referent.md` — the prompt is `include_str!`'d
(`guardian_prompt.rs:377`), so the fix needs a daemon rebuild. Added a paragraph
after the definition (the exact text is in the main-working-copy edit and was
also applied to the build):

> Judge the candidate NAME on its own denotation, not the record it appears in.
> A record may state an abstract principle, decision, or rule; the referent it
> tags is still concrete whenever the NAME denotes a particular thing. An
> identifier-style or kebab-case name that reads as the proper name of a
> workspace artifact — a repository, crate, component, daemon, tool, schema,
> file, host, or person (for example triad-runtime, schema-rust-next,
> sema-engine, nota-next, signal-spirit) — IS a concrete nameable particular:
> admit it, even when the surrounding record is abstract. Reserve NonReferent
> for a candidate whose NAME is itself a verb, an abstract concept, or an intent
> (validate, sharing, modularity, the-principle-of-X); never reject a concrete
> component name merely because the record about it states a principle. The
> psyche tagged the referent deliberately — when the name plausibly proper-names
> a workspace artifact, default to admitting it.

NOTE: this edit is on the spirit **main working copy** (uncommitted, dirty).
`referent.md` is unchanged across the deployed→main delta, so the fix is
identical whether based on 0.12.0 or main.

## Build (done)

`nix build .#daemon` from the main working copy produced
`/nix/store/64n5pj7rrm1d6r992fpx7dm7jalild2d-spirit-0.12.1/bin/spirit-daemon`
(= main 0.12.1 + the referent fix). Built on the remote builder (prometheus),
copied back. Holds a GC root via the repo's `./result` symlink (verify still
present, or rebuild).

## Deploy decision (psyche-directed)

Psyche said **"work on top of main"** — deploy main (0.12.1), not an isolated
0.12.0+patch. The live daemon is the **stale** 0.12.0; main carries the
operator's wanted improvements (guardian-scoping `c1952d1`, contract-import
`92dc509`). So deploying main is correct, not a side-effect risk.

Facts established:
- local spirit `main` (`92dc509`) == `origin/main` (pushed). So main is at origin.
- `.sema` intent store backed up: `~/.local/state/spirit/` copied to a
  `.bak-referentfix-*` sibling before any restart. Store files: guardian
  v1/v2/v3 .sema + a pre-0.12 recovery backup + schema-1-backup. The daemon
  handles versioned stores (migration); 0.12.1 is the "versioned store pilot"
  rev family.
- CriomOS-home pins spirit (input among `*-source` inputs); deployed pin =
  `a4cc858`. To deploy main: bump the spirit pin to main (+ the referent-fix
  commit) and `home-manager switch` (regenerates the systemd unit + the
  `spirit.config.rkyv` from the new schema — important: a bare systemd override
  reusing the old 269-byte config.rkyv is RISKIER because the config could fail
  to decode if the startup schema changed; the home-manager path regenerates it).

## Resume steps (in order)

1. **Commit the referent fix.** It's on the spirit main working copy (dirty,
   only `referent.md` modified). Commit on top of main (psyche: "work on top of
   main"). NOTE lane: operator owns spirit main; this was psyche-directed, so
   commit + (push or hand to operator to land). Suggested message: `spirit:
   referent guardian admits concrete component names regardless of record
   abstraction`.
2. **Deploy main.** Preferred: bump CriomOS-home spirit pin to the new main rev,
   `home-manager switch` (regenerates config + unit, handles store migration).
   Lighter (riskier on config): systemd drop-in override `ExecStart=` →
   `/nix/store/64n5…/bin/spirit-daemon <config.rkyv>`, keep `ExecStartPre`,
   `daemon-reload`, `restart`. Either way, VERIFY after: `spirit Version`
   (expect 0.12.1), a test `spirit "(Observe …)"` read, daemon healthy. If
   broken: restore the `.sema` backup, revert override, restart the old binary.
3. **Re-submit the principle WITH the referent:**
   ```sh
   spirit "(Record (([(Technology (Software (Engineering SoftwareArchitecture)))] Principle [The Signal, Nexus, and SEMA reaction-frame types Work, Action, and the canonical five-variant action set are workspace-universal and must be declared once and applied or bound per component, never hand-re-authored in each component schema; re-authoring universal types per component is a design failure.] High Minimum Zero [triad-runtime]) ([([if theyre rewritten for every component, something has been badly designed] (Some [discussing NexusWork NexusAction and NexusEffectCommand re-declared across every component schema]))] [Psyche, reviewing the reaction-frame types repeated in every component schema, judged per-component re-authoring of universal types a design failure; a durable architecture principle that the canonical frame is shared, adjacent to but distinct from the no-ancestry-prefix naming rule and DRY.])))"
   ```
   Expect `(RecordAccepted …)` with `[triad-runtime]` now admitted.
4. **Remove the referent-less version `n6fz`** (recorded under the guardian
   friction): `spirit "(Remove (n6fz ([([<psyche authorization quote>] None)] [superseded by the same principle recorded with the triad-runtime referent after the referent-guardian fix])))"`. Needs a psyche authorization quote for the destructive op (or set certainty Zero as the recoverable nomination first).
5. **Durable deploy follow-up.** If step 2 used the override, the home-manager
   pin update is still needed so the live daemon matches declared state (operator
   / system-operator territory) — flag it.

## Caveat

Deploying the live shared intent daemon (0.12.0→0.12.1) is consequential and
touches the operator's in-flight main work. The `.sema` backup is the rollback.
Confirm with the psyche/operator if anything looks off before the restart.
