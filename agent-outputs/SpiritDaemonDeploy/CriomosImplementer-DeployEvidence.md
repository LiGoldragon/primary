# Spirit Daemon Deploy — Implementer Evidence

Artifact: deployment evidence for the attempted spirit 0.16.0 -> 0.18.0
production deploy on `goldragon/ouranos` (user `li`) via the lojix orchestrator
(`meta-lojix` direct, no `n`/`lojix-run` wrapper).

OUTCOME: **HALTED-AT-BUILD.** The non-activating Build validation failed with a
genuine build error. No backup, no daemon stop, no activation occurred. The live
spirit daemon is fully untouched (still 0.16.0, 650 records). CriomOS-home main
was restored to green (spirit pin reverted to 0.16.0).

## Scope / mechanism

- Deploy repo: `repos/CriomOS-home` -> `/git/github.com/LiGoldragon/CriomOS-home`.
- Spirit store: `/home/li/.local/state/spirit/`.
- Orchestrator: `lojix-daemon.service` (active), client `meta-lojix`
  (lojix-0.3.10) -> `/run/lojix/owner.sock` (default). `lojix` ordinary client
  -> `/run/lojix/ordinary.sock`.
- Deploy schema verified against
  `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema`:
  `DeployRequest [(System …) (Home …)]`,
  `HomeDeployment { ClusterName NodeName UserName source flake HomeMode builder substituters }`,
  `HomeMode [Build Profile Activate]`, `builder (Optional Builder)` (so `None`
  valid), `substituters (Vec …)` (so `[]` valid). Submitted NOTA shape matched.

## 1. Baseline re-confirm (read-only) — MATCHES BRIEF

| Fact | Value | Command |
|---|---|---|
| Version | `0.16.0` | `spirit Version` -> `(VersionReported 0.16.0)` |
| Live non-Zero count | `650` | `spirit "(Count (Any Any Any Any None Any (AtLeastCertainty Minimum) Any))"` -> `(RecordsCounted 650)` |
| Total incl zero | `1389` | `(Count (Any Any Any Any None Any Any Any))` -> `(RecordsCounted 1389)` |
| Marker | `(4502 11798222239588764778)` | `spirit Marker` |
| Daemon | `active` | `systemctl --user is-active spirit-daemon.service` |

Note on marker: brief recorded `(4499 9109844853594107580)`; observed
`(4502 11798222239588764778)`. Counts (650 / 1389) are identical to the brief;
the marker advanced by 3 commit-sequence steps from intervening read/stash
activity before this session. The marker was unchanged across the whole session
(same value at start and end) — no spirit writes occurred.

## 2. Re-pin + push — DONE, THEN REVERTED

- `nix flake update spirit` in CriomOS-home updated only the `spirit` input.
  Verified pins (via `nix eval` of `flake.lock` nodes):
  - `spirit` -> `a6d69b467e80f4c61c0d2e345e80c3b0023098b3` (= a6d69b46, 0.18.0) ✓
  - `signal-spirit-source` -> `5d0905a7aa8c43951253b86193d76be67a89a945` (= 5d0905a, 0.9.0) ✓
  - `meta-signal-spirit-source` -> `83415f2203cccde02290258f28dfac8152857f82` (= 83415f2, 0.2.0) ✓
- Committed on CriomOS-home `main` and pushed; pushed rev
  `4c2af96380b282ab293acfbc3a762a26ecbf38ec` (local main == origin/main). This
  rev filled `?rev=<REV>` for the deploy.
- After the Build failure (below), the re-pin was **reverted** on main to keep
  main green: flake.lock restored to spirit `0dec3710d1e0203492a97f7b40e3e5dbbb09c5c5`
  (0.16.0); pushed rev `12b0973841dd6a66b7f33761ecd09ed1d00e133b`
  (origin/main confirmed). Rationale: spirit 0.18.0 makes
  `homeConfigurations.li.activationPackage` fail to build (see §3), so leaving
  main pinned at 0.18.0 leaves main's home build red. The running daemon is
  unaffected by either pin. Re-pinning is trivial once the home module is fixed.

## 3. Build-validate (NON-ACTIVATING) — REJECTED (build failure)

Build mode confirmed NON-ACTIVATING from deployed daemon source (lojix 0.3.10 =
checked-out source), `src/schema_runtime.rs`:
- `fn activates()` (line 857) doc: "`Eval` and `Build` (and Home `Build`) stop
  at the realised closure." Home arm matches only `Profile | Activate`;
  `HomeMode::Build` -> `false`.
- Pipeline `ClosureBuilt` handler (lines 2217-2229): `if activates() { CopyClosure
  -> ActivateGeneration } else { finish_deploy_pipeline() }`. For Home `Build`,
  `activates()` is false -> finishes after the build with NO copy, NO activate, NO
  home-manager activation, NO service restart. Zero live impact.

Submitted (owner.sock, exit 0):
`meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=4c2af96380b282ab293acfbc3a762a26ecbf38ec Build None [])))"`
-> immediate admission reply `(Deployed (21 (367 367)))` =
`AcceptedDeploy{deployment_identifier=21, marker=(367 367)}`.

The reply is the async admission only; the deployed daemon runs eval+build
asynchronously and logs the authoritative terminal outcome to the
`lojix-daemon.service` journal. Observed pipeline for deployment 21:

- Source RESOLVED and flake ref + attribute RESOLVED: the pipeline materialized
  the horizon (from the `goldragon/datom.nota` source) and successfully eval'd
  `github:LiGoldragon/CriomOS-home?rev=…#homeConfigurations.li.activationPackage`,
  producing `home-manager-generation.drv` and starting `nix build`. => NOT
  ProposalSourceUnreachable, NOT FlakeReferenceMalformed at the ref level. The
  source path is correct.
- `spirit-0.18.0` itself BUILT green (built on / copied from
  `ssh-ng://nix-ssh@prometheus.goldragon.criome`).
- The build FAILED downstream. Root failing derivation:
  `spirit-daemon-configuration.drv`, builder exit 1, error:

  `spirit-write-configuration: expected ConfigurationWriteRequest to hold 7 root objects, found 6`

  Cascade: `spirit-daemon-configuration.drv` -> `spirit-daemon.service.drv` ->
  `home-manager-files.drv` -> `home-manager-generation.drv` all "1 dependency
  failed".
- Daemon terminal output (journal): `DeployRejected(RejectedDeploy {
  deploy_rejection_reason: FlakeReferenceMalformed, database_marker: (371 371) })`.
  (The deployed daemon maps any eval/build failure to the `FlakeReferenceMalformed`
  terminal reason; the real cause is the nix build error above.)

This is the same error seen historically (journal Jun 24 14:12:57) — a known,
reproducible configuration-schema incompatibility, not a transient failure.

Root cause (precise): spirit 0.18.0 added a new field to the daemon startup
configuration. `SpiritDaemonConfiguration` fields:
- 0.16.0 (signal-spirit 7ae038e), 5 fields: `socket_path`, `MetaSocketPath?`,
  `database_path`, `TraceSocketPath?`, `GuardianAgentConfiguration?` -> 6
  `ConfigurationWriteRequest` root objects (incl. output path).
- 0.18.0 (signal-spirit 5d0905a / 0.9.0), 6 fields: inserts
  `AuthorizationMode [Gating Observing]` as the 5th field (between
  `TraceSocketPath` and `GuardianAgentConfiguration`) -> 7 root objects. This is
  the "reconciled guardian Matter boundary / 0.18.0 rework" surface.

CriomOS-home's generator at
`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`
(`daemonConfiguration`) emits the 6-object 0.16.0 shape and is missing the new
`AuthorizationMode` value (e.g. `Gating`). The `ConfigurationWriteRequest` it
writes is:
`(<socketPath> (Some <metaSocketPath>) <databasePath> None <guardianAgentConfiguration> $out/<configurationPath>)`
— it needs `Gating` (or `Observing`) inserted as the 5th positional field:
`(<socketPath> (Some <metaSocketPath>) <databasePath> None Gating <guardianAgentConfiguration> $out/<configurationPath>)`.

Per the brief, a build-validate rejection => STOP. No backup, no daemon stop, no
activation.

## 4. Backup — NOT REACHED

Not performed (halted at Build before any host-side mutation). The daemon was
never stopped; `spirit.sema` / `spirit.archive.sema` were not copied or modified.

## 5. Activate + Verify — NOT REACHED

No activation. The guardian Matter-probe (verify step) was NOT submitted, so the
store has zero probe pollution. Final read-only confirmation of the untouched
live daemon:

| Fact | Value |
|---|---|
| Version | `0.16.0` (unchanged) |
| Non-Zero count | `650` (±0) |
| Total incl zero | `1389` (unchanged) |
| Marker | `(4502 11798222239588764778)` (unchanged across session) |
| Daemon | `active` |
| `spirit.sema` mtime | `17:50` (pre-deploy; deploy submitted 18:13) — untouched |
| `spirit.archive.sema` mtime | `15:33` — untouched |

## 6. Outcome

**HALTED-AT-BUILD.** The non-activating lojix Build validation caught a genuine
configuration-schema incompatibility (spirit 0.18.0 requires a 7th
`ConfigurationWriteRequest` root object, `AuthorizationMode`, that CriomOS-home's
spirit home module does not emit). This is exactly the failure the Build-first
discipline exists to catch: it surfaced with ZERO live impact — the production
spirit daemon remains 0.16.0 with all 650 records intact, store files untouched.

CriomOS-home `main` was restored to green (spirit pin reverted to 0.16.0
`0dec371`, pushed `12b0973841dd`).

## Required follow-up (blocking the 0.18.0 deploy; not done — out of halt scope)

1. **CriomOS-home home module fix** (the blocker): in
   `modules/home/profiles/min/spirit.nix`, update the `daemonConfiguration`
   `ConfigurationWriteRequest` to insert the new `AuthorizationMode` field
   (`Gating` for enforcing, or `Observing`) as the 5th positional field, matching
   signal-spirit 0.9.0 `SpiritDaemonConfiguration`. This is a code change to the
   home module, not a lock bump. (Cross-check the analogous agent/mind
   configuration line in the same file if it also feeds a bumped contract.)
2. After the home-module fix lands and builds, re-pin spirit to 0.18.0
   (a6d69b46) on CriomOS-home main, push, and re-run the lojix Build validation;
   only on a green Built outcome proceed to backup -> Activate -> verify per the
   brief.
3. **CriomOS system repo** `criomos-home` input re-pin for lock consistency
   remains pending and is moot until step 1/2 land (was noted in the brief as a
   non-blocking follow-on).

## Commands / evidence surfaces consulted

- `meta-signal-lojix/schema/lib.schema`, `signal-lojix/schema/lib.schema`
  (deploy + query/phase contracts).
- `lojix/src/schema_runtime.rs` (`activates()`, pipeline `ClosureBuilt` gate),
  `lojix/src/bin/{lojix,meta-lojix}.rs` (one-shot clients).
- `journalctl -u lojix-daemon.service` (authoritative deploy terminal outputs +
  build error).
- `signal-spirit` schema at revs 7ae038e (0.16.0) and 5d0905a (0.9.0) for the
  `SpiritDaemonConfiguration` field diff and `GuardianRejectionReason` (`Matter`
  token present in 0.9.0).
- `spirit` checkout at a6d69b46 (`guardian-prompts/checklist.md`,
  `README.md` ConfigurationWriteRequest example).
- `CriomOS-home/modules/home/profiles/min/spirit.nix` (configuration generator).
- `spirit Version` / `Count` / `Marker` (baseline + final live-daemon checks).

No secrets, tokens, or private host credentials were exposed. Store paths are
referred to by name, not frozen hashes.
