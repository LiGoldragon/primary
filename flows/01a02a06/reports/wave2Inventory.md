# Wave 2 inventory

Wave 2 inventoried the live legacy stores without moving files. Counts are
a snapshot: concurrent flows were actively landing their own migrations,
so later history witnesses supersede an earlier path count where the two
differ.

## Legacy session protocol

The current tree contains 16 timestamped legacy session records plus
`sessions/index.md` and `sessions/design.log`. Five other legacy session
records have already been migrated and deleted with Jujutsu history:

| Retired legacy source | Current flow home | Landing witness |
|---|---|---|
| `sessions/design/15b67974.md` | `flows/15b67974/` | `a69ae86ad792` |
| `sessions/realization/2026-08-19T222016.md` | `flows/01a01bac/` | `f6a4b001858c` |
| `sessions/realization/2026-08-21T100106.md` | `flows/01a02356/` | `ec1de861e011` |
| `sessions/realization/2026-08-21T105838.md` | `flows/01a0238b/` | `cd84f979d355` |
| `sessions/realization/2026-08-21T130824.md` | `flows/01a02400/` | `a522ae9d9427` |

The historical 15b67974 divergence is resolved: the current flow log is a
superset of the old session snapshot and records the merge and removal.
Its annotation remains useful historical evidence, not a statement of
current divergence.

An initial Codex-only lookup reported seven transcript-backed annotations.
A cross-harness scan corrected that result by finding Claude transcripts.
Among the 16 remaining timestamped records, direct ID-named transcripts
exist for:

`e4be1c4a`, `358f143a`, `7c3f0c1d`, `bc05da32`, `01a01149`, `01a0145c`,
`01a0193f`, `01a01998`, `01a01a93`, and `01a020ff`.

The `759fc98a` record names an alternate Claude transcript path. No direct
or recorded alternate transcript is yet established for `72939228`,
`4a959c64`, `6bec1f7a`, `b5b1f5fe`, and `91254d53`. Absence from this lookup
is an unknown, not proof that no transcript exists.

## Current flow protocol

The inventory found 18 current flow directories at its snapshot. Four
contained `annotations.md`:

- `01a01bac` records its completed Lojix realization and raw-Vision moves.
- `01a02400` records its completed default-opening migration with a source
  hash and raw-Vision retirement.
- `15b67974` preserves the now-resolved divergence history.
- `fd301d9a` says its copied Vision is context from earlier records, not new
  psyche speech in that subflow.

No per-file `Origin:` headers were found. The directory supplies the flow
origin; annotations describe later external edits and completed migrations.

## Raw written psyche

`psyche-raw/` contains 105 Markdown files: 103 Vision and 2 Intent. The
Vision inventory found 377 heading records plus 24 file-level units without
headings.

- 340 heading records have explicit session markers; 37 do not.
- One otherwise unmarked heading record carries a flow short ID, leaving 36
  strictly unmarked heading records.
- 17 no-heading file units have a session marker; 7 do not.
- The corpus contains 34 distinct short/full session markers.
- 30 markers resolve to one exact main transcript.
- `019ff178` is ambiguous among three main transcripts.
- The recorded full `019ffbd3` UUID does not exist; three short-prefix
  candidates do.
- `72939228` has no matching main transcript yet.
- `01a01450` has a matching transcript, but its record points instead to
  `history.jsonl`; it remains weak pending confirmation.
- Attachment UUID `37b689c9` is explicitly not a session ID; the associated
  session is `55d18f4f`.

Two Intent records remain Intent even though their transcripts exist.
Spirit-related material remains governed by the Spirit home, not migrated
into flow Vision. Ten records in `psyche-archive/2026-08-19.md` are already
archived and are not raw migration sources. Ten existing
`flows/*/vision/*.md` files are already destination-shaped and are not
re-migrated.

## Other legacy stores

The live inventory counted:

| Store | Files | Inventory status |
|---|---:|---|
| `reports/` | 710 | Mostly unannotated; requires transcript tracing and repository-home classification. |
| `handoffs/` | 12 | No class-wide origin ruling; trace artifact by artifact. |
| `awareness/sessions/` | 5 | The term is obsolete in this concept, but physical disposition is not class-wide. |
| `agent-outputs/` | 1,001 | Many name repositories/commits; exclude repository-owned evidence unless transcript proof establishes a flow artifact. |
| `verified/` | 3 | Evidence/reference infrastructure, not itself an origin assignment. |

Transcript files are immutable provenance witnesses and never migration
targets.

## Protected material entering Wave 3

The following remain in place unless Wave 3 finds unique actual-transcript
evidence:

- the five legacy session IDs without a direct or recorded alternate
  transcript;
- unmarked, ambiguous, and weakly sourced raw-Vision records;
- Intent, Spirit, archived psyche, and existing flow Vision;
- repository-owned design/code/README artifacts;
- legacy report, handoff, awareness, agent-output, and verified material
  whose flow origin has not been witnessed.

## Sources

- Live path and transcript inventory returned by Wave 2 subflows of flow
  01a02a06.
- `sessions/index.md`, `sessions/design.log`, and the 16 timestamped files
  under `sessions/`.
- `flows/index.md` and `flows/*/annotations.md`.
- `psyche-raw/Vision/`, `psyche-raw/Intent/`, and
  `psyche-archive/2026-08-19.md`.
- Jujutsu commits `a69ae86ad792`, `f6a4b001858c`, `ec1de861e011`,
  `cd84f979d355`, and `a522ae9d9427`.
- Claude transcripts under
  `/home/li/.claude/projects/-home-li-primary/` and Codex rollouts under
  `/home/li/.codex/sessions/`, as enumerated by the Wave 2 subflows.
- Flow 01a02a06, Wave 1 report `reports/wave1MigrationRulings.md`.
