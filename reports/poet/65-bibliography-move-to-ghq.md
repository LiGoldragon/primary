# 65 — Bibliography moved to ghq tree

*Closes report 62 P0 (path-correction). The standalone scholarly
library now lives at its ghq-managed canonical location with
backwards-compatible workspace symlink and updated path
references in the two repos that pointed at it.*

## What changed

**Move.** `/home/li/Criopolis/library/` → `/git/github.com/LiGoldragon/bibliography/`.
Single `mv` on the same filesystem; 2.5 GB total; atomic.
Git remote (`git@github.com:LiGoldragon/bibliography.git`),
jj working copy, prior commits (including report 64's "add: 9
Āyurvedic primary editions" landed at commit `oqwqkuzwxltt`)
all intact at the new path.

**Symlink.** `/home/li/primary/repos/bibliography` →
`/git/github.com/LiGoldragon/bibliography`. Matches the
workspace-wide `~/primary/repos/<name>` → ghq pattern visible
across the other 12 entries in `~/primary/repos/`.

**AGENTS.md path corrections** (closes report 62 P0):

| Repo | File | Change |
|---|---|---|
| TheBookOfSol | `AGENTS.md` | 6 occurrences of `~/git/bibliography` and `/home/li/git/bibliography` replaced with `~/primary/repos/bibliography` |
| caraka-samhita | `AGENTS.md` | 3 occurrences |
| caraka-samhita | `README.md` | 1 occurrence (Caraka primary-edition disk-path) |
| caraka-samhita | `notes/translation-sources.md` | 1 occurrence (Sharma 2014 path) |

Both repos committed and pushed:
- TheBookOfSol commit `qpnnkron 731df0ee` (this repo had no
  `.jj/` — initialized on the fly with `jj git init --colocate`
  and `jj bookmark track main@origin`, both standard fixes per
  `skills/jj.md`; rebased my AGENTS.md change on top of one
  origin-side commit that landed in parallel).
- caraka-samhita commit `nxoxvwrm fa04863d`.

Verification: zero remaining `~/git/bibliography` or
`/home/li/git/bibliography` references in the four touched
files. The canonical path
`/home/li/primary/repos/bibliography/sa/ayurveda/` resolves to
the nine new Āyurvedic primary-source files registered in
report 64.

## What was deliberately left alone

**`/home/li/Criopolis/library/` is now absent** (the path no
longer exists on disk). I did not create a backwards-compat
symlink at the old path. Reasoning: the move was an explicit
relocation per the user's instruction; leaving a symlink at
the prior location would re-anchor the wrong path as a
recognised location and undo the consolidation.

If anything in `/home/li/Criopolis/` (the parent jj repo, with
gas-city and Criopolis agent integrations) hard-references
`/home/li/Criopolis/library/`, it would now error. A grep across
Criopolis for that string would find any breakage. Out of scope
for this pass — flagging here for follow-up if breakage shows.

**Other `~/git/<repo>/` references** in AGENTS.md (TheBookOfSol's
AGENTS.md still has `~/git/lore/`, `~/git/caraka-samhita/`,
`~/git/TheBookOfSol/`; caraka-samhita's AGENTS.md still has
`~/git/TheBookOfSol/`). Those are the same conceptual problem
in different repos — none of those `~/git/<x>/` paths exist on
this machine; the actual repos are under `/git/...` (ghq tree)
or via `~/primary/repos/<x>/`. Out of scope for this pass — the
user asked specifically about *the library*, not the broader
path-convention consolidation. A second pass to update the rest
would touch every Li-repo's docs and warrants its own
coordination.

## Side effect — the carried-over peer-agent state

The library's working copy at the time of the move contained
several uncommitted files that were not mine:

- `.beads/config.yaml`, `.beads/metadata.json` (modified)
- `.claude/skills/core.gc-{agents,city,dashboard,dispatch,mail,rigs,work}` (added)
- `.codex/hooks.json`, `.gc/settings.json`, `.runtime/session_id` (added)
- `.gitignore` (modified)
- `library/.codex/hooks.json` (added; nested `library/` subdir)

These appear to be Criopolis / "gas city" agent-runtime
integration files. They came along with the move (they are
inside the moved directory) and remain in the new location's
working copy uncommitted. They were not authored by this
session and are not addressed here.

## Implications for report 62

Report 62 (`reports/poet/62-ayurvedic-source-audit.md`)
recommended **P0 — Path correction** as the single
highest-leverage action. P0 is now complete:

- The bibliography path is now the canonical
  `/git/github.com/LiGoldragon/bibliography/`, reachable
  workspace-side as `~/primary/repos/bibliography/`.
- The `AGENTS.md` files in TheBookOfSol and caraka-samhita
  point at the new path.
- Future agents reading either AGENTS.md will follow
  `~/primary/repos/bibliography/` and find what they expect.

Report 62's P1 (Sharma & Dash 7-vol Caraka), P2 (Devanagari
OCR on the 1922 Cakrapāṇi PDF), P4 (laghu-trayī Bhāvaprakāśa /
Śārṅgadhara), P5 (Meulenbeld HIML), P6 (concatenate IA-ZIPs),
and P7 (encode the API-key/aria2c distinction as a skill)
remain as named there; nothing in this pass changed their
status.
