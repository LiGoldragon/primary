# 125 — Context Maintenance, 2026-05-16

## What This Pass Did

The system-specialist report directory was over the 12-report soft cap.
This pass retired stale working reports whose substance had already
moved into code, repo architecture docs, repo skills, tests, or beads.

No harness-private memory was used; the current pickup state is in this
report, the pushed commits, and `.beads/`.

## Retired Reports

### ClaviFaber implementation ledgers

Deleted:

- `106-clavifaber-yggdrasil-key-actor.md`
- `107-clavifaber-wifi-certificate-actor.md`
- `108-clavifaber-actor-async-audit.md`
- `109-clavifaber-state-review.md`
- `110-clavifaber-cleanup.md`
- `112-clavifaber-existing-host-audit.md`
- `113-clavifaber-audit-implementation.md`

Reason: their load-bearing substance now lives in
`clavifaber/ARCHITECTURE.md`, `clavifaber/skills.md`, and tests such as
actor topology, actor trace, forbidden edges, and publication-writing
witnesses. Keeping the intermediate ledgers beside the current report
surface made the active state harder to read.

### WHISRS dictation reports

Deleted:

- `110-whisrs-input-safety-and-targeted-insertion.md`
- `111-whisrs-selector-and-mic-level-status.md`

Reason: their decisions are now in `CriomOS-home/skills.md` and code:
`Mod+V` is clipboard-only, `Mod+Shift+V` is direct insertion,
`Mod+Alt+V` opens `whisrs-recall`, `Mod+Escape` cancels recording, and
the status bar has the `whisrs-level` microphone-level plugin.

### DNS resolver research reports

Deleted:

- `114-dns-resolver-stack-audit.md`
- `115-router-dns-server-research.md`

Reason: the resolved/dnsmasq split is now embodied in CriomOS network
modules and `checks/resolver-role-policy/default.nix`. The reports were
exploratory state, not a current coordination surface.

## Kept Reports

- `116-lojix-check-host-key-material.md` — still useful for the Lojix
  host-key/material-diff work.
- `117-system-data-purity-and-wifi-pki.md` — still relevant to
  Horizon/ClaviFaber/CriomOS data-boundary work.
- `118-criomos-state-and-sandbox-audit.md` — still relevant to sandbox
  and test-cluster work.
- `119-horizon-data-needed-to-purge-criomos-literals.md` — still
  relevant to purging cluster literals from engine repos.
- `120-refresh-unaddressed-system-work.md` — still a useful older
  refresh, though parts are now superseded by beads and later commits.
- `121-sops-nix-wifi-secret-integration.md` — still relevant until the
  production secret path is fully settled and absorbed.
- `122-chroma-solar-theme-schedule.md` — kept as the current Chroma
  schedule implementation ledger.
- `123-criomos-home-architecture-audit.md` — recent architecture audit.
- `124-agent-language-intelligence-tools.md` — recent tooling research.

## Current Live Context

The cloud-host Stage-3 handoff from designer-assistant reports 92 and
93 is completed and pushed.

Pushed commits:

- CriomOS `horizon-re-engineering`
  - `cb605cfd` `nspawn: reinstate container host wrapper`
  - `76807b20` `llm: route api key through secret resolver`
- horizon-rs `horizon-re-engineering`
  - `497277d3` `horizon: model contained cloud hosts`
  - `c0b2634c` `style: format horizon rust sources`
  - `ed78fab6` `nix: name horizon crane package from cli manifest`
- CriomOS-test-cluster `horizon-re-engineering`
  - `202d6bb8` `fieldlab: adopt rich contained placement`
  - `2e4e96eb` `fieldlab: follow final horizon cli package fix`

Verification completed:

- horizon-rs `cargo fmt --check`
- horizon-rs `cargo test --jobs 1 -- --test-threads=1`
- CriomOS targeted `nix-instantiate --parse`
- CriomOS-test-cluster `projections-match-fieldlab` on Prometheus with
  local jobs disabled

Bead `primary-a70` was closed. Its older wording still mentions
superseded `NodeCapabilities` / `MissingPlacement` design terms; the
close comment marks that wording as superseded by reports 92/93.

## Open Pickup Points

The next system-specialist work is no longer `primary-a70`; it is the
work unblocked by it:

- `primary-7zz` — split CriomOS Nix builder/cache/retention concerns and
  remove remaining name-gate patterns.
- `primary-9wi` — mkCriomOSNode/container-host work and first
  NixosContainer child.
- `primary-5u9` — Ghost as a Publication node in an NixosContainer,
  blocked by container-host groundwork.
- `primary-1ha` — add negative Horizon fixtures for role invariants.
- `primary-58l` — VM/nspawn smoke for DNS and tailnet roles.

Side note: a remote Nix build surfaced a crane package-name/version
warning in horizon-rs. That is now fixed by deriving `pname` and
`version` from `cli/Cargo.toml`.

