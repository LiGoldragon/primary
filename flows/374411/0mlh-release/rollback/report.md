# 0mlh step-five rollback preparation

Prepared without changing live runtime on 2026-11-13. Nothing live was switched, restarted, replayed, refreshed, launched, deployed, or built. The declared refresh program was rehearsed only against disposable snapshot-backed checkouts inside this bundle.

## Exact current rollback state

- Home Manager generation/profile: `/nix/store/sd47c969srp0gh5kz86c2v658nr81x84-home-manager-generation`; user profile `/nix/store/l38l3igqhdig1cvl5i8pa12wp86ivc4i-profile`; home path `/nix/store/9gxx8l784g2521r2h3m4ywxdzjhivnl9-home-manager-path`.
- Lojix deployment 527 independently records that generation as `Current`, `LiveActivation`, terminal `Some.Succeeded`, from immutable CriomOS `63c637845165288e2d438287becf00f9d75c08c3`.
- The current consumer locks CriomOS-home `0b430341a594f1b1ee31e986c4dbd0d537e6ffe7`, Curriculum `478cbc51878921a0668278120aacca0031a72f92`, and Flow `5d70c7b8a04c5119e978297668b2925b0c5e1186`. Lock nar hashes are retained in `raw/declared-source-pins.tsv`.
- `curriculum-nexus.service` is active/running, PID 12525, executable `/nix/store/6ibqv7ha5lj3k347w60a0falfsarpnww-curriculum-0.1.0/bin/curriculum-nexus`.
- `flow-nexus-0540.service` is active/running, PID 1016330, executable `/nix/store/fs53xwvgp9kbam4sbc25671hdrvnl37q-flow-configured-0.54.7/bin/flow-nexus-daemon`. `flow-configure-0540.service` is the matching active/exited declaration unit. Exact invocations, dependencies, declared unit-file store targets, process start ticks, and commands are in `raw/runtime-units.txt`, `raw/declared-unit-targets.txt`, and `raw/runtime-processes.txt`.

## Metaflows rollback

`metaflows-current.datom` is the exact current live family extracted from a fresh pinned-owner `Configuration` read. It structurally equals the post-3fhi readback. `metaflows-rollback-payload.datom` wraps that exact vector as the one-family `Configure.Metaflows` request. Neither file was applied.

## Lojix rollback input

`lojix-rollback-request.datom` is prepared, not submitted. It names goldragon/ouranos/li, the canonical user transport, `ActivateNow`, `RequireImmutable`, the current immutable consumer revision, and the existing proposal/secrets inputs. The proposal is a regular non-symlink with SHA-256 `d1ee23cef2706d3ab8cd9ad4e83df79ff062a059fb4cadc843aa750fdfac2457`; the secrets directory was checked only by type and no secret content was read. The prior consumer is present locally as a commit and is an ancestor of observed remote CriomOS main `583e727fb24701295d6a603ea34f9f1b43c504d4`. Deployment 527 is the independent proof that this exact immutable consumer produced and activated the captured current generation.

The request was derived from the retained proven UserEnvironment request by changing only its historical consumer revision to the current prior revision and `Realize` to `ActivateNow`; its target/action/revision assertions are in `raw/prepared-request-check.txt`.

## Curriculum context rollback

The three live source checkouts are clean and captured byte-for-byte plus as standalone pinned `main` repositories under `context-snapshots/`. Exact commits are psyche `d0b875…`, mind `09f129…`, and field `a3d1c9…`. The current declared startup refresh fetches main for each repository. `context-restore-procedure.md` gives and rehearses an executable pinned-old-name route that keeps the exact declared HTTPS origins while repository-local URL rewriting serves the retained pinned repositories. No live checkout or configuration was edited.

## Stopped runtime rollback

Opus pegm confirms the candidate changes no Memory schema. `stopped-runtime-backup-procedure.md` records the exact event-time procedure: stop Flow and Curriculum, copy the whole Flow store `/home/li/.local/state/nexus/main` and Curriculum persistent state `/home/li/.local/state/curriculum-context`, hash the stopped copy, then start the new cohort. Rollback stops the candidate, restores those whole directories without merging, switches through the prepared immutable prior Lojix request, starts the old declared units with pinned contexts, and replays the captured Metaflows family. No live running store was copied during preparation.

## Evidence

Exact readbacks, source lock, validity metadata, hashes, and commands are in this directory and `raw/`. Secret contents are absent.
