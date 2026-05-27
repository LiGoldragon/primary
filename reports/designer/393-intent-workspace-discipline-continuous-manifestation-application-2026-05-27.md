# 393 — Continuous per-repo intent manifestation: discipline + application

*Kind: Synthesis · Topic: intent-workspace-discipline · 2026-05-27*

Per spirit record 944 (Maximum, 2026-05-27): intent must be manifested in
per-repo `INTENT.md` and `ARCHITECTURE.md` files **at all time**, not just
at the workspace level. This report records the discipline strengthening
plus the first comprehensive manifestation pass applying recent session
intent (records 894-944) into the active repos.

## Skill edits applied

**`skills/repo-intent.md`** — added §"Continuous manifestation
discipline" stating: (a) when an agent starts working in a repo, the
first verification step is whether recent psyche intent affecting that
repo is reflected in its `INTENT.md` / `ARCHITECTURE.md`; (b)
manifestation happens BEFORE or AS PART OF the work cycle, not as a
deferred pass; (c) discipline applies whenever ANY new intent record
affects a specific repo's design/implementation/test direction, not
just intent specifically scoped to that repo.

**`skills/architecture-editor.md`** — added §"Continuous manifestation
discipline" as the architectural companion: architectural intent
captured in Spirit reflects into the repo's `ARCHITECTURE.md` as part
of the work cycle. Trigger is wider than repo-specific intent — any
record whose architectural shape binds the repo (recent records 922,
882/712, 894, 902, 909, 932-940, 935 listed as examples) is in scope.

## AGENTS.md required-reading update

Bullet 7 of the required-reading list now extends to include the
repo's `INTENT.md` and `ARCHITECTURE.md`, and states the maintenance
obligation explicitly: read them on entry AND update them as relevant
intent lands. The bullet cross-links to the two new §"Continuous
manifestation discipline" sections.

## Per-repo manifestation pass

All commits land on designer feature branches `designer-intent-manifestation-2026-05-27` in worktrees under `~/wt/github.com/LiGoldragon/<repo>/`, pushed to origin. None push to operator main.

| Repo | Commit | What was reflected |
|---|---|---|
| `nota-next` | `f04c38f8` | Records 894 (brace = key/value map at NOTA layer), 927 (textual structure header), 922 (no `\n` inline NOTA), 895/902 (single-colon symbol qualification), 712/882 (methods on non-ZST). New §"Structural rules at the NOTA layer", §"Whitespace and inline-string discipline", §"Colon-qualified symbols", §"Methods on non-ZST types" in INTENT.md; ARCHITECTURE.md extended with StructureHeader description + structural rules + code shape section. |
| `schema-next` | `2b14062e` | Records 886 (schema self-description), 887 (built-in core schema), 888-890 (real macro system + binding), 891-894 (brace = key/value, dynamic enum), 901 (future enum-table compilation), 902 (single-colon namespace), 925-926 (macro expansion structural matching, brace namespace as macro), 928 (enum-like entry), 932 (sugar syntax, multi-criteria), 933-934 (schema-as-struct, input/output tag-space), 936-940 (recursive struct down to scalars), 938 (typed-string scalars), 942 (logic-on-objects). INTENT.md gained eight new sections; ARCHITECTURE.md gained schema-as-recursive-struct, macro engine multi-criteria, and input/output tag-space partition sections. |
| `schema-rust-next` | `c1453758` | Records 909/910 (src/schema emission target locked, not OUT_DIR), 902 (literal wording of src/schema path), 712/882 (methods on non-ZST). INTENT.md gained §"Emission target — src/schema in the consumer crate" and §"Methods on non-ZST types"; ARCHITECTURE.md constraints extended with the load-bearing emission target + impl-block-only emitted functions. |
| `spirit-next` | `2d7b942e` | Records 902/909 (schema folder + src/schema), 935 (signal-frame Communicate trait + async unique IDs + handshake), 934 (input/output tag-space partition), 712/882 (methods on non-ZST), 922 (no `\n` inline NOTA), 942 (logic-on-objects). INTENT.md restructured around the schema-folder + src/schema emission load-bearing constraint; ARCHITECTURE.md gained signal-frame mechanism + tag-space wire-encoding notes plus methods-on-non-ZST rule. |
| `signal-frame` | `736eabdf` | NEW INTENT.md created (the repo previously had none). Manifested records 935 (Communicate trait substrate: framing + async IDs + handshake; mail manager + database marker layer above), 934 (input/output one tag namespace at wire level), 712/882 (methods on non-ZST), 922 (no `\n` inline NOTA). ARCHITECTURE.md constraints section extended with three new bullets covering the same intent. |
| `spirit` | `68f009bf` | Records 935 (Communicate trait wire interface + mail state manager + database marker), 712/882 (methods on non-ZST), 944 (continuous manifestation). INTENT.md gained §"Wire mechanism — Communicate trait over signal-frame" and §"Continuous manifestation"; ARCHITECTURE.md gained §8a mail-manager + database-marker section, §8b methods-on-non-ZST, and signal-frame boundary cell extended with the spirit record 935 reference. |
| `signal-spirit` | `92b9d1a8` | Records 935 (Communicate trait wire), 902/909/910 (src/schema emission target), 934 (input/output partition), 712/882 (methods on non-ZST), 944 (continuous manifestation). INTENT.md gained five new sections; ARCHITECTURE.md gained §5a/5b/5c covering schema emission target, wire input/output partition, and methods-on-non-ZST. |
| `core-signal-spirit` | `00053e40` | Same record set as signal-spirit, scoped to the privileged channel. INTENT.md gained §"Wire mechanism", §"Schema emission target — src/schema", §"Methods on non-ZST types", §"Continuous manifestation"; ARCHITECTURE.md gained §7a (src/schema target) and §7b (methods-on-non-ZST), plus signal-frame boundary cell extended with record 935 reference. |

Workspace primary repo `main` carries the skill + AGENTS.md edits at commit `67e0f807` (`workspace: continuous manifestation discipline for per-repo INTENT.md + ARCHITECTURE.md (intent 944)`).

## Repos skipped

- All other repos under `protocols/active-repositories.md` were checked against the named intent records. None of the records in the 894-944 range affect those repos' design/implementation/test direction in a way requiring new manifestation beyond what is already present.
- `cloud`, `domain-criome`, and their signal triads carry intent in records 914-919 / 923-924 — those belong to operator + cloud-designer manifestation, outside this report's scope.

## Coordination notes

- `a326...`'s operator-audit + re-port slot is at `reports/designer/389-...` (not touched). My slot is `reports/designer/393-...`.
- No designer-intent-manifestation-2026-05-27 branch existed in any repo before this pass; each branch was created fresh from operator main. No coordination conflict observed.
- Existing designer feature branches for separate topics (`designer-no-free-fns-2026-05-27` in nota-next, `designer-pair-style-namespace-2026-05-27` and `designer-schema-namespace-and-folder-2026-05-27` in schema-next, `designer-emit-to-src-schema-2026-05-27` in schema-rust-next and spirit-next) remain untouched. Manifestation lives on the new `-intent-manifestation-` branches; operator integration is operator's choice.

## What this changes

Future agents entering any of the above repos read the `INTENT.md` + `ARCHITECTURE.md` and see the current intent reflected — they no longer need to query Spirit + cross-check old intent against stale repo files. The discipline is now lived in workspace skill + AGENTS.md required-reading, so the same expectation applies to all future intent landings.
