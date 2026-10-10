# Suspect Ruling

Task: rule on unresolved verifier-ledger suspects for epic `primary-5rzf`, bead `primary-5rzf.8`.

Scope: read-only ruling over the six items in `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md` under `SUSPECTS / UNRESOLVED FOR .8`. This report does not authorize deletion. It classifies each suspect and identifies the missing evidence that keeps it off the confirmed kill tracks.

Authoritative inputs consulted:

- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/TrackerSweep-Candidates.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/DocsSkillsSweep-Candidates.md`
- `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/CodeSweep-Candidates.md`
- `bd show primary-5rzf.8`
- Targeted read-only checks named below.

Boundaries observed:

- No destructive action was taken.
- No Spirit intent records were queried or swept.
- `/home/li/primary/private-repos` was not inspected.
- Suspects were not converted into kill actions.
- The worker brief explicitly requested this file at `agent-outputs/WorkspaceStalenessSweep/SuspectRuling.md`; the bead body names the older expected path `SuspectRuling-ForPsyche.md`.

## Category Counts

- Needs human decision: 0
- Needs private-scope authorization: 0
- Needs source-owner investigation: 2
- Likely not stale: 2
- Follow-up verification candidate: 2

## Rulings

### S1. `primary-36iq.7.1` quote-delimited NOTA examples after rename lock

Classification: follow-up verification candidate.

Evidence observed:

- Verifier locator: `primary-36iq.7.1`.
- `bd show primary-36iq.7.1 --long` shows the bead is still `OPEN`.
- Its description says the remaining quote-delimited authored NOTA examples were found in locked Persona/signal repos and says: after the Persona/signal rename lock clears, claim specific repos, convert ordinary string-like positions to bracket strings, preserve deliberate legacy-decode compatibility tests, and run each repo's Nix check or named witness.

Why not safe for kill beads:

- The new thing is unclear in the verifier ledger.
- There is no evidence that the rename lock cleared.
- There is no evidence that this tracker item is dead; the bead reads like a still-live migration task with explicit acceptance criteria.

Recommended follow-up:

- Create or use a follow-up verification bead to check whether the Persona/signal rename lock has cleared and whether `primary-36iq.7.1` should remain a tracker migration item, split into repo-specific work, or be closed after repo witnesses pass.

### S2. `subagent-session-workflow` obsolete/deleted skill

Classification: needs source-owner investigation.

Evidence observed:

- Verifier locators: `/home/li/primary/repos/skills/ARCHITECTURE.md:75-77`; `/home/li/primary/repos/skills/manifests/skills-roster.nota:76`.
- `repos/skills/ARCHITECTURE.md` says archived modules have no active manifest entry, deleted modules are modeled by compatibility checks and emit no surfaces, and `subagent-session-workflow` is obsolete and remains deleted.
- `repos/skills/manifests/skills-roster.nota` line 76 lists `subagent-session-workflow skills/subagent-session-workflow.md Deleted NoEmission []`.

Why not safe for kill beads:

- The old thing is named and deletion state is visible, but the replacement/new thing is not explicitly named at the hit.
- The roster entry may be an intentional compatibility/check surface rather than stale prose.
- Removing it without a skills source-owner decision could break the compatibility model described in the architecture.

Recommended follow-up:

- Ask the skills source owner to determine whether the compatibility record should remain, and if docs need cleanup, name the explicit current replacement surface before any removal bead is filed.

### S3. `router Wi-Fi` and `persona-engine-sandbox` absent from scoped docs/skills

Classification: likely not stale.

Evidence observed:

- Verifier reports no scoped docs/skills locator and says targeted `rg` over scoped docs/skills surfaces returned no hits.
- The only docs/skills evidence is the handoff's mention that these were mystery items; the verifier also notes tracker/code have separate live or suspect evidence.

Why not safe for kill beads:

- The evidence-anchored rule lacks a locator in docs/skills.
- The rule also lacks a replacement/new thing for the docs/skills surface.
- There is no docs/skills item to remove from this suspect.

Recommended follow-up:

- Do not create a docs/skills kill bead from this item. If the psyche wants mystery-item provenance beyond the already surfaced tracker/code evidence, file a separate non-destructive provenance bead.

### S4. Router Wi-Fi code/config surface

Classification: likely not stale.

Evidence observed:

- Verifier locators: `/git/github.com/LiGoldragon/CriomOS/checks/router-wifi-secret/default.nix:7-12`; `/git/github.com/LiGoldragon/CriomOS/checks/router-wifi-horizon-policy/default.nix:7-17`; `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:91-93`.
- `bd show primary-a61 --long` shows `primary-a61` is `IN_PROGRESS`.
- `primary-a61` comments explicitly say not to remove the current password Wi-Fi yet, then later say Wi-Fi remains intentional transitional debt and the bead should not close because SSID/country policy and test-cluster Wi-Fi constraints remain open.
- The CriomOS checks assert that inline Wi-Fi password/country/name forms are absent and that router Wi-Fi uses the projected/resolved surfaces. The router module still asserts the secret reference exists.

Why not safe for kill beads:

- Tracker evidence says the surface is live transitional debt, not dead stale code.
- There is no complete replacement/new thing proven landed.
- Deleting this surface could break the stated router migration path.

Recommended follow-up:

- Keep this out of kill beads. Continue through `primary-a61` or a source-owner migration bead until the dual-radio/EAP-TLS or successor path is complete and the old password Wi-Fi surface has explicit deletion evidence.

### S5. `schema-rust-next` migration status disagreement

Classification: follow-up verification candidate.

Evidence observed:

- Verifier locators: `/home/li/primary/protocols/active-repositories.md:37`; `/git/github.com/LiGoldragon/schema-rust-next/INTENT.md:106-114`; `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs`.
- `protocols/active-repositories.md:37` still says the old `RustWriter` string emitter is mid-migration out and the remaining string surface is transitional.
- `schema-rust-next/INTENT.md:106-115` says the string-emission migration is complete, the former `RustWriter` is gone, and only the leading generated header comment is direct text.
- The verifier found code evidence for `RustModuleRenderer` and token routing, while noting a remaining `line` method for the generated header.

Why not safe for kill beads:

- This is not a code deletion item for `.7`; it looks like a possible docs correction in `protocols/active-repositories.md`.
- The old code shape appears already replaced, but the active-map wording disagreement needs confirmation before any tracked docs edit.
- The exception for the generated header means a raw string-search result is not enough evidence for deletion.

Recommended follow-up:

- File a follow-up verification/docs bead to reconcile `protocols/active-repositories.md` with `schema-rust-next/INTENT.md` and current source. If confirmed, the action should be a docs correction, not a code kill.

### S6. `terminal` versus `terminal-cell`

Classification: needs source-owner investigation.

Evidence observed:

- Verifier locators: `/git/github.com/LiGoldragon/persona/flake.nix:59-62` and `:213-216`; `/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:312-315`; `/home/li/primary/protocols/active-repositories.md:32`.
- `protocols/active-repositories.md:32` names `terminal-cell` as the active terminal primitive for V1 harness work and Claude/Codex tests and says to use it directly, not as subordinate to `terminal`.
- `persona/flake.nix` still imports both `persona-terminal` from `github:LiGoldragon/terminal` and `terminal-cell`, and creates `persona-terminal-prototype-launcher`.
- `harness/ARCHITECTURE.md:314` still links `../terminal/ARCHITECTURE.md`.

Why not safe for kill beads:

- The active map deprecates routing V1 harness terminal tests through `terminal`, but `persona` still carries a broader supervised terminal topology.
- The evidence conflicts on whether all `terminal`/`persona-terminal` uses are dead or only a specific V1 harness route is superseded.
- Source-owner judgment is needed to separate dead test-routing references from live topology references.

Recommended follow-up:

- Ask the `persona`/`harness` terminal owners to rule which `terminal` uses remain live. If only V1 harness routing is dead, file a narrow docs/code follow-up for that route rather than a broad removal.

## Checks Run

- `sed -n '1,220p' /home/li/primary/.agents/skills/beads/SKILL.md`: read tracker closeout doctrine.
- `sed -n '1,220p' /home/li/primary/.agents/skills/privacy/SKILL.md`: read private-scope boundary doctrine.
- `sed -n '1,220p' /home/li/primary/.agents/skills/reporting/SKILL.md`: read report-output doctrine.
- `sed -n '1,260p' /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`: read epic scope and evidence rule.
- `sed -n '1,320p' /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`: read verifier ledger.
- `sed -n '/^## SUSPECTS \\/ UNRESOLVED FOR \\.8/,/^## REJECTED/p' /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`: isolated the six suspect items for `.8`.
- `bd show primary-5rzf.8`: bead is open, depends on closed verifier bead, and acceptance asks for a non-destructive suspect list.
- `bd show primary-36iq.7.1 primary-a61 --long`: confirmed `primary-36iq.7.1` remains open and `primary-a61` remains in progress with explicit no-remove/transitional-debt comments.
- `sed` reads of `TrackerSweep-Candidates.md`, `DocsSkillsSweep-Candidates.md`, and `CodeSweep-Candidates.md`: checked original suspect evidence and missing-rule notes.
- `nl -ba /home/li/primary/repos/skills/ARCHITECTURE.md | sed -n '68,82p'`: confirmed deleted-module compatibility wording and obsolete `subagent-session-workflow` statement.
- `nl -ba /home/li/primary/repos/skills/manifests/skills-roster.nota | sed -n '72,78p'`: confirmed `subagent-session-workflow` is `Deleted NoEmission`.
- `nl -ba /home/li/primary/protocols/active-repositories.md | sed -n '28,42p'`: checked `terminal-cell` and `schema-rust-next` active-map wording.
- `nl -ba /git/github.com/LiGoldragon/schema-rust-next/INTENT.md | sed -n '104,116p'`: checked completed string-emission migration statement and header exception.
- `nl -ba /git/github.com/LiGoldragon/persona/flake.nix | sed -n '54,66p;208,218p'`: checked coexistence of `terminal` and `terminal-cell` inputs and `persona-terminal` launcher.
- `nl -ba /git/github.com/LiGoldragon/harness/ARCHITECTURE.md | sed -n '308,318p'`: checked remaining `../terminal/ARCHITECTURE.md` reference.
- `nl -ba /git/github.com/LiGoldragon/CriomOS/checks/router-wifi-secret/default.nix | sed -n '1,18p'`: checked router Wi-Fi secret assertion surface.
- `nl -ba /git/github.com/LiGoldragon/CriomOS/checks/router-wifi-horizon-policy/default.nix | sed -n '1,24p'`: checked router Wi-Fi horizon policy assertions.
- `nl -ba /git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix | sed -n '86,96p'`: checked remaining router Wi-Fi secret-reference assertion.
- `bd close --help`: checked close command syntax before bead closeout.

Checks not run:

- No tests or builds were run; this was a read-only ruling.
- No broad workspace sweep was run beyond the verifier inputs and narrow suspect evidence checks.

## Blockers and Unknowns

- No private-scope authorization is needed for the six current rulings because no item requires entering `/home/li/primary/private-repos`.
- No item is ready for a kill bead from this report alone.
- S2 and S6 need source-owner rulings before destructive work can be scoped.
- S1 and S5 need follow-up verification beads if the orchestrator wants to turn them into actionable cleanup.
- S3 and S4 should remain off the kill tracks unless new evidence proves a replacement/new thing and dead old surface.
