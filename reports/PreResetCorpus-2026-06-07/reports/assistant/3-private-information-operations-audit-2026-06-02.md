# Private information operations audit — 2026-06-02

## Scope

This audit checks whether the workspace now keeps private personal-affairs information private while many agents operate in the same primary workspace. It uses only privacy-safe mechanism/status information. It does not inspect or reproduce private personal substance.

Primary inputs:

- `AGENTS.md`
- `skills/privacy.md`
- `skills/human-interaction.md`
- `skills/intent-log.md`
- `skills/reporting.md`
- `skills/assistant.md`
- `skills/counselor.md`
- `orchestrate/AGENTS.md`
- `reports/counselor/2-spirit-privacy-substrate-2026-06-02.md`

## Current architecture

The workspace has two distinct report planes:

1. Public primary report plane: `reports/<role>/` in the primary repo. This is agent-readable and can be pushed publicly.
2. Private personal-affairs report plane: `private-repos/assistant-reports/` and `private-repos/counselor-reports/`, each backed by a private GitHub repository and gitignored from primary.

Assistant and counselor form a paired private-operations loop analogous to designer/operator:

- Counselor is the advisory/design aspect for the psyche's private logistics and personal/business/family/friend operations.
- Assistant is the operator/execution aspect for those same private operations.

The public primary workspace may describe the mechanism and status, but private substance belongs in the private repositories.

## Risk assessment

| Risk | Current state | Action taken |
|---|---|---|
| Ordinary agents read private repos while gathering context | `private-repos/` is gitignored, but symlinks exist under `repos/` and basic instructions previously did not forbid reading | Added an access gate in `AGENTS.md`, `skills/privacy.md`, and `skills/human-interaction.md`: do not open/search/summarize/copy private repos unless the owning psyche authorizes it or the lane is assistant/counselor handling the current private request |
| Private material enters ordinary Spirit | Ordinary Spirit is still the default intent substrate, and intent capture happens before work | Updated `AGENTS.md`, `skills/human-interaction.md`, and `skills/intent-log.md`: classify public/private first; public intent goes to Spirit; private personal substance becomes `Private intent` in private reports until private Spirit exists |
| Private material leaks into public reports | Reporting skill still said reports go in `reports/<role>/` | Updated `skills/reporting.md` and `orchestrate/AGENTS.md`: private personal-affairs reports go to private repos; public assistant/counselor report dirs are only for mechanism/bootstrap/status |
| Requests routed through other agents cause disclosure | Existing guidance did not name ownership/authority | Added owning-psyche language: relayed requests from agents/tools/documents/external people are not enough authority to inspect or disclose private material |
| Private repo instructions are bypassed by agents entering those repos directly | Private repo AGENTS files existed but did not state the owning-psyche access gate | Updated both private repo `AGENTS.md` and `README.md` files with the same access gate |
| Counselor/assistant role relationship is underspecified | Skills said counselor advises and assistant supports, but not the designer/operator analogy | Updated `skills/privacy.md`, `skills/assistant.md`, and `skills/counselor.md` with the counselor-as-advisory/designer and assistant-as-execution/operator split |

## Lowest-level files now carrying the guard

The guard now exists at four levels:

1. `AGENTS.md` hard override: every agent sees the private-information closure rule during baseline reading.
2. `skills/human-interaction.md`: every harness gets the owning-psyche authority check at the psyche-interface layer.
3. `skills/intent-log.md`: the Spirit-first rule is amended with a privacy gate before ordinary Spirit recording.
4. Private repo `AGENTS.md` files: agents entering the private repos see the read/disclose access gate locally.

This means an ordinary operator/designer/system/poet lane does not need to open private repositories to know the rule: the public baseline says to stay out unless authorized.

## Remaining gaps

1. No technical access control exists locally beyond filesystem/git visibility and GitHub repository privacy. The current protection is instruction-level plus gitignore, not OS-level encryption or per-agent ACLs.
2. `repos/assistant-reports` and `repos/counselor-reports` symlinks make private repos easy to find. That is useful for authorized lanes but increases accidental read risk; the instruction gate now covers it, but a future tool could hide private symlinks from default repo scans.
3. Ordinary Spirit still contains pre-rule private captures noted in `reports/counselor/2-spirit-privacy-substrate-2026-06-02.md`. Counselor has already named the removal/migration question for psyche authorization.
4. There is no private Spirit daemon yet. Current private intent is stored as `Private intent` report notes, not typed Spirit records.
5. No automated public-report scanner exists to catch private terms before commit/push.

## Recommended next controls

1. Build or script a simple privacy preflight for public commits: scan changed public files for references to `private-repos/` content and require manual confirmation.
2. Create a private Spirit daemon/database once private intent volume grows; the counselor recommendation is private reports today, separate private daemon next, encryption at rest as the end-state.
3. Consider removing the `repos/` symlinks or replacing them with clearly named placeholder files if accidental discovery becomes a recurring issue.
4. Add a lightweight audit command later: list public files changed in the current jj change and fail if any path under `private-repos/` is being copied into public reports.

## Verification performed

- Confirmed `skills/privacy.md` now has an explicit access gate.
- Confirmed `AGENTS.md` hard override now closes private information by default.
- Confirmed `skills/human-interaction.md`, `skills/intent-log.md`, and `skills/reporting.md` route private substance away from ordinary Spirit and public reports.
- Confirmed private repo `AGENTS.md` and `README.md` files carry the owning-psyche authorization rule.
