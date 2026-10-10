# Phase 2 Append — criome + CriomOS-home ARCHITECTURE integration

## Task and scope

Integrate archived Spirit records into two sub-repos, each processed
independently with its own commit and push:

- `repos/CriomOS-home/ARCHITECTURE.md` — 20 records
- `repos/criome/ARCHITECTURE.md` — 18 records

Repos live at `/git/github.com/LiGoldragon/<name>` with their own git+jj.
Records were synthesized into existing sections (not raw-dumped), grouped
thematically, deduped against what was already captured. One `[SECRET]`-flagged
record (`go41`) redacted to non-secret substance.

## Inputs consulted

- Routing manifest: `/home/li/primary/agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`
- Dump: `/tmp/spirit-archive-extract/archived-spirit-records.dump.md` (full record blocks extracted by id)
- Both target `ARCHITECTURE.md` files and their `AGENTS.md`; CriomOS-home `docs/pi-extensions.md` + `docs/ROADMAP.md`

## Edit coordination

Claimed each `ARCHITECTURE.md` path on the `maintainer` lane via `orchestrate`
before editing; released after each push. No active claims existed on either
repo at start. `system-designer` (Claude) holds CriomOS/clavifaber/lojix etc.
but neither criome nor CriomOS-home — no conflict.

## criome — 18 records integrated

Commit `3091f404` (change `wvspxxwr`); pushed: `main` fast-forwarded
`b996f937` -> `3091f404`. `main@origin` confirmed at `3091f404`.

Sections touched:

- **Scope note (new "Place in Telos" para)** — `pviw` (Telos umbrella; criome =
  agreement-and-authorization organ; quorum = universal primitive).
- **Authorization model, policy classes** — `mzfj` (first cluster quorum
  contract mirrors SSH authorized-keys, one-of-any, incremental tightening).
- **Authorization model, "many criome daemons" bullet** — `a4i6` (per-Unix-user
  trust boundary, no shared multi-user daemon, no embeddable library, system
  tier peers with home, per-agent identity recorded in persona-mind,
  Criome-not-SSH authorization).
- **§6 Trust model, identity bullet** — `3fm6` (public key IS the identifier,
  SignalCore primitive) + `dx10` (3-byte prefix `shortest_id()`).
- **§8 Constraints** — `32wj` (error-kind subtyping is an ongoing first-class
  design surface; typed Error enum grows).
- **New §8.2 "Future direction"** — `m3ms` (universal guard substrate, typed
  policy language, orchestrate executes, provenance split), `ic4o` (guard
  workflow two planes), `z9d6` (content-addressed composable contracts),
  `ay3y` (crystallized-PAST time, AttestedMoment window-proposition mechanics),
  `i6ih` (last-known-acknowledgment / quorum-of-agreement), `lt44` (two
  transport lanes: Router general, criome auth-only; microVM/tailnet/tap-L3),
  `crlc` (domain-criome content-addressed DNS for .criome), `ermr`
  (cluster-root admission gate; cross-ref existing §9 enforcement), `7let`
  (criome/lojix VM-test substrate, three substrates, spirit gate, first
  witness with fail-closed negative control).

Already captured before this session (no new edit, deduped):

- `burk` — already cited in §6.1 ("Spirit `burk`").
- `psc6` — already in §2 (master keypair, encryption) + §9 ("psyche
  key-custody choice `psc6`").
- `p43g` — already covered by Authorization model + §6 (criome owns key
  custody, is the decider, SO_PEERCRED submitter authentication).

No `[SECRET]` records in the criome set.

## CriomOS-home — 20 records integrated

Commit `47a6b38c` (change `omnotzrl`); pushed: `main` fast-forwarded
`f5ae705b` -> `47a6b38c`. `main@origin` confirmed at `47a6b38c`.

Sections touched:

- **Desktop survivability + new "Activation safety" subsection** — `ok16`
  (core interactive programs higher priority, rescue terminal separate,
  survey Linux mechanisms), `mz16` (research-first smallest-safe shape),
  `bev5` (activation persists across reboot, older-Claude-on-reboot is a bug,
  keeps session, confirm disruption window; Pi safety proceeds on dirty repo).
- **Dictation + new "Recording-system data flow" subsection** — `4fao` (DJI
  keepalive keeps mic hot, no lost first seconds), `p675` (laptop-mic ->
  large-AI-node hop explicit). `1vj5` already covered by existing Dictation.
- **Boundaries, Rust toolchain bullet** — `jtos` (newest nightly via fenix
  lock, per-crate routes through shared rust-build fromToolchainFile).
- **New "Emacs native compilation"** — `9xwr` (.eln at Nix build, runtime JIT
  forbidden).
- **New "Agent and browser tooling"** — `51u8` (Pi extensions via flake
  inputs, browser-use wrapper on local Gemma, HF model fetcher utility, video
  tooling in medium profile), `wp91` (pi-subagents mined selectively), `wvgh`
  (three-tier browser control, CDP, supervised scout mode).
- **New "Update synchronization"** — `11m7` (Claude Code/Codex/Pi updated
  together via CriomOS-home + full CriomOS lock), `ud6l` (Bird/Zeus authority
  uses main by default), `bc6f` (Bird Zeus redeploy via root/maintainer SSH).
- **New "Networking and media"** — `87ts` (Android Criome-WiFi name
  resolution), `vgon` (Syncthing excluded from phone mirror, Immich uploader).
- **New "Secrets scoping"** — `go41` [SECRET, redacted] (secret paths
  zone-scoped vs provider-scoped; zone-scoped local-LLM token survives role
  host moves), `bdse` (Playwright Chrome token in gopass, read without
  printing).
- **New "Firmware gating"** — `qmsh` (reuses existing policy, no broad Horizon
  schema).

Already captured before this session (deduped, minimal/no new edit):

- `zdie` — already fully in §"Spirit deployment" (build startup archive at
  Nix build).
- `1vj5` — already thoroughly in §Dictation.

## [SECRET] redactions

- `go41` — non-secret substance written only: "secret paths scoped to the
  resource they serve... zone-scoped local-LLM API token survives the
  large-AI role moving between hosts." **No gopass path value written.** The
  dump itself carried `<REDACTED-GOPASS-PATH>` placeholders; none reproduced.
- `bdse` — not SECRET-flagged, but the actual gopass entry path
  (`chrome-browser/playwright-mcp-extension-token`) was deliberately NOT
  written; the doc says only "lives in gopass" + "read without printing."

Verified post-edit: no `REDACTED`, no token/path strings, and no `---`
horizontal rules in either file.

## Checks run

- jj pre-flight gate per repo, twice each (before edit, before commit):
  `@` empty/on-top-of `main`; `main` == `main@origin` (fetch "Nothing
  changed"); not divergent; not a sibling-of-main. Both fast-forward pushes.
- `grep '^---$'` -> none in both files. `grep -i REDACTED` / token paths ->
  clean in both files.
- Push verification: `main@origin` == local `main` at the new commit for both
  (criome `3091f404`, CriomOS-home `47a6b38c`).

## Blockers / unknowns / follow-up

- None. Both repos processed and pushed; no repo skipped. Claims released;
  `maintainer` lane empty at close.
- `orchestrate` claim grammar note for future workers: the working shape is
  `(Claim (<lane> [(Path <abs>)] [reason]))` — the Path must be wrapped in its
  own `[...]` vector and the reason is a separate trailing `[...]` vector.
