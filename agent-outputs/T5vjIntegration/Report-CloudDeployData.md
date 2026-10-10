# T5vj Integration — Cloud / Deploy / Data (non-OS subset)

Integration evidence for rehoming deferred archived-Spirit code/config records
into their LIVE non-OS repo homes. This worker's domain was strictly
`cloud`, `goldragon`, and `lojix`. The parallel OS worker (`system-designer`,
observed holding `CriomOS` + `CriomOS-home`) owns the OS subset; nothing here
touched `CriomOS`, `CriomOS-home`, or the OS-domain secret record `go41`.

## Task and scope

Take the records routed to cloud / goldragon / lojix from
`agent-outputs/SpiritArchiveRehoming/RoutingManifest.md` and
`agent-outputs/SpiritArchiveRehoming/Scout-CloudRecordHomeVerdict.md`, and
manifest their NON-SECRET substance into the correct live guidance surface,
avoiding duplication, honoring secret redaction.

In-scope record sets:
- cloud-daemon substance -> `cloud` (10 routed, of which 2 are node/trust
  records that belong to `goldragon`; 8 are true cloud-daemon records).
- cloud-node / trust -> `goldragon` (`5pf6`, `zeqq` — verify, do not duplicate).
- deploy substance -> live `lojix` (NOT retired `lojix-cli`) — 8 records.

## Sources consulted

- Routing SoT: `RoutingManifest.md`, `Scout-CloudRecordHomeVerdict.md`.
- Record substance: `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`
  (present; re-extraction of snapshot `preremoval-631` was not needed).
- Target repos on disk under `/git/github.com/LiGoldragon/`: `cloud`, `lojix`,
  `goldragon` (only `goldragon` is symlinked into `repos/`; `cloud`/`lojix`
  are not, but are live per `protocols/active-repositories.md`).
- Skills: intent-manifestation, secrets, repo-intent, plus repo `AGENTS.md` for
  each entered repo.

## What landed where (record id -> repo -> location)

### lojix — /git/github.com/LiGoldragon/lojix/ARCHITECTURE.md (pushed to origin/main)

Commit `1c6bba6b` on `main`, pushed. Doc-only manifestation.

- `vudl` -> §1 Owned surface (Owner/meta socket bullet): two-contract authority
  split — Deploy/Pin/Unpin/Retire owner-only in `meta-signal-lojix`;
  Query/WatchDeployments/WatchCacheRetention/Unwatch peer-callable on
  `signal-lojix`; policy contract born meta-signal-lojix; local path-dep stopgap
  until cutover.
- `2alg` -> §5 Constraints: concurrent connections bounded by a permit cap,
  per-request pipeline cursor, brief per-op Store lock, no global lock on nix.
- `mq5s` -> new §7 Direction: testing and deployment are one function;
  contained-vs-production typed split as the safety boundary (not a runtime flag).
- `75pw` -> §7 Direction: safe typed Lojix interface is the default for nix
  build/test/deploy; caller describes operation/capabilities/containment/builder.
- `vfgk` -> §7 Direction: ergonomic test-authoring interface as a first-class
  requirement.
- `h03z` -> §7 Direction: production credentials custodied through criome
  machine-identity rather than the operator's logged-in session.
- `2qhw` -> §7 Direction (REDACTED value): lojix-daemon owns GitHub-authed Nix
  flake input resolution via a small wrapper library; credential value and its
  store path kept out of source/logs/nix store. (secret-flagged — see redaction.)
- `lc28` -> §4 Storage and wire: provisional daemon-side substituter resolution
  (node name -> Yggdrasil URL/key), wire reverts to bare node names, marked
  must-be-replaced-by-better-design.

Already covered before this edit (no duplication written): `lc28`/`ufjd`/`0a9p`
build-on-target citations already in the "Build-on-target" note; `ufjd` and
`0a9p` are OS-domain records not owned here.

### cloud — /git/github.com/LiGoldragon/cloud/ARCHITECTURE.md (pushed to origin/main)

Commit `efae1776` on `main`, pushed (via isolated jj workspace — see worktree
note). New "Direction and Principles" + "Packaging" sections; the existing
code-accurate "Current Implementation Slice" was left untouched to avoid
overstating the Plan->Mutate rename as already-implemented and to avoid
conflicting with the cloud-maintainer's active code.

- `mbmy` -> Direction and Principles: cloud is the home for provider API
  machinery (Cloudflare/Google/Hetzner); plan prep on owner signal.
- `7kyx` -> Direction and Principles: provider modeled as a reflected state;
  Query public / Mutate owner-only; generalizes to any reflected external
  resource. (Triad + Boundary already carried the structural half.)
- `8fe9` -> Direction and Principles: Plan renamed Mutate, reply Mutated;
  Mutate-sent vs Mutated (provider-ack) states; held state is last-known-ack.
- `m3eg` -> Direction and Principles: almost-stateless daemon, in-memory
  last-known-state cache, persistence deferred.
- `150a` -> Direction and Principles: on-demand compute provisioning; DigitalOcean
  lead (per-second billing, no reuse pool) over Hetzner (hourly, keep-warm 59min
  reuse pool).
- `iprx` -> Direction and Principles: credential custody transitional
  (wire CredentialHandle -> env var behind 0o600 owner socket) moving toward
  criome-custodied machine identity. (secret-adjacent — handle only, no value.)
- `16l0` -> Packaging: flarectl is a runtime dep wrapped via makeWrapper on the
  daemon PATH when built with the cloudflare feature.
- `nsi2` -> Packaging: flake gopass shim exports CF_API_TOKEN before exec; only
  the handle path `cloudflare.com/api-token` is stated, never a token value.
  (secret-adjacent.)

### goldragon — VERIFIED ONLY, no edit (no duplication)

- `5pf6` and `zeqq` are ALREADY homed on the live branch
  `cloud-designer-cloud-node-data` (local `zlrnmmvo`; also on origin). Verified
  in that branch's `datom.nota`:
  - `doris (CloudNode Min Min (Metal ... (Some [DigitalOcean Droplet]) ...
    digitalocean-nyc3 ...) ...)` with a PLACEHOLDER host key and unprovisioned
    marker; comment header cites "Spirit 5pf6, zeqq" and "Spirit zeqq".
  - `5pf6` = cloud nodes get Min cluster trust (doris set Min).
  - `zeqq` = provision-on-role; doris declared but unprovisioned until it gets a
    role, placeholder host key until then.
- `main` at `nsztosmm` does NOT contain doris. The branch is unmerged. I did not
  merge it (see Deferred below). No goldragon edit was made; writing these
  records fresh would duplicate the branch's work.

## Redaction

Applied secret discipline (secrets skill: key names/handles/ciphertext are not
secret; the value is). No secret value was written anywhere.

- `2qhw` (SECRET-FLAGGED): only the non-secret mechanism was manifested
  (lojix-daemon owns GitHub-authed flake input resolution via a wrapper
  library). The dump already had the credential store redacted; I did not
  resurrect any store path or token value. "2qhw was never written — do not
  resurrect their values" is honored: the substance is a design decision, and no
  credential value exists to resurrect.
- `wn7q`, `2qhw` values: not resurrected. `wn7q` is OS-domain (CriomOS), out of
  scope regardless.
- `iprx`, `nsi2` (secret-adjacent, cloud): manifested only the pattern and the
  handle path (`cloudflare.com/api-token`); no token value.
- `nz0t`, `osoo`: OS-domain (CriomOS), out of scope — not touched.
- `go41`: OS-domain secret record — ignored per brief.

## Deferred / blocked

- goldragon `cloud-node-data` branch merge to `main` — DEFERRED, not my call.
  Merging is a larger disposition that also carries an unrelated secret-file
  rename divergence (main renamed sops files to camelCase after the branch
  forked) and would merge across another lane's data-repo work. The two in-scope
  records (`5pf6`, `zeqq`) are already homed on the branch, so the rehoming
  success criterion is met at the branch level. Recommendation: a
  goldragon-owning agent should land `cloud-designer-cloud-node-data` onto
  `goldragon/main` following the push-immediately data-repo discipline, resolving
  the sops-rename divergence. This worker deliberately did not force that merge to
  avoid a cross-lane data-repo mutation.
- cloud repo was claimed by `cloud-maintainer` (Codex) with reason "fix
  DigitalOcean gopass credential path" at edit time. Per edit-coordination
  discipline I did NOT share that checkout: I created an isolated jj workspace
  `t5vj-cloud-arch` from `cloud/main`, made the doc-only edit there, and landed it
  onto `cloud/main` as a clean fast-forward (`3b38cdd8` -> `efae1776`; origin main
  had not moved). Workspace forgotten and removed after landing. Tracked and
  closed via bead `primary-nroe`.

## Checks run (exact results)

- `orchestrate "(Observe Roles)"` — confirmed `cloud-maintainer` held
  `/git/github.com/LiGoldragon/cloud`; `system-designer` held CriomOS +
  CriomOS-home (the OS worker); lojix unclaimed. PASS (informed strategy).
- `orchestrate "(Claim ...)"` for lojix and the cloud isolated worktree —
  both `ClaimAcceptance`. Released at end with `ReleaseAcknowledgment`.
- lojix: `jj commit` + `jj bookmark set main` + `jj git push --bookmark main` —
  pushed; `main@origin` = `1c6bba6b`. PASS.
- cloud: `jj git fetch` (origin main unchanged at `3b38cdd8`), `jj git push
  --bookmark main` — "Move forward bookmark main from 3b38cdd8 to efae1776";
  re-fetch confirms `main@origin` = `efae1776`. PASS (clean fast-forward).
- goldragon: `jj file show -r cloud-designer-cloud-node-data datom.nota | grep
  doris` — doris CloudNode present, cites Spirit 5pf6/zeqq; `jj file show -r main
  datom.nota | grep doris` — empty (branch unmerged). Verified, no edit.
- No repo tests run: all three edits are ARCHITECTURE.md prose (no code, wire,
  storage, or generated surface changed), so no meaningful build/test check
  applies. lojix/cloud were on clean working copies before edit; no unrelated
  changes were committed.

## Follow-up requirements

1. A data-repo-owning agent should land `cloud-designer-cloud-node-data` onto
   `goldragon/main` (resolving the sops-rename divergence) to fully close
   `5pf6`/`zeqq` at `main` level.
2. When `cloud-maintainer` finishes and pushes its DigitalOcean gopass credential
   fix, it will fast-forward past `efae1776`; no manual reconciliation is needed
   since the doc change is already on `main`.
3. Epic tracker beads were NOT mutated (tracker-weaver owns those); this report is
   the evidence surface. Only the local worktree-tracking bead `primary-nroe` was
   created and closed as part of edit-coordination discipline.
