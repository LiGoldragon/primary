# 2 — NOTA discipline manifestation

*Subagent B's pass: manifest the NOTA-discipline intent records
(690, 698, 703, 704, 705) captured this session into the right
permanent docs — skills, AGENTS.md hard override, INTENT.md,
per-repo INTENT.md. Retire the source report.*

## §1 What was found

### Intent records walked

Queried `spirit-v0.2.0 "(Observe (Records ((Some nota) None DescriptionOnly)))"`. The records in scope, in chronological order:

| Record | Kind | Magnitude | Substance |
|---|---|---|---|
| 690 | Principle | Maximum | Authoring preference: schema/signal/CLI NOTA should be authored without quotation-mark strings. Bare token for no-space; `[text]` for ordinary; `[|text|]` for bracket-safe / code / macro text. Introduces the single-letter bare/bracket distinction. |
| 698 | Clarification | Maximum | Strengthens 690 from authoring preference to **structural rule about the format**: brackets ARE the string form; quotation marks do NOT form string types. Legacy quoted-string acceptance is non-canonical and slated for removal. Test imperative: latest NOTA must behave per this rule. |
| 703 | Decision | Maximum | Authorises removal of legacy double-quoted-string acceptance from `nota-codec` lexer. Migrate all emitters (CriomOS-home Nix modules, `lojix-cli`, examples, downstream consumers). Excludes legacy `intent/*.nota` files which migrate via a separate programmatic extractor. |
| 704 | Decision | Maximum | Legacy `intent/*.nota` migration uses a separate programmatic extractor that preserves original psyche timestamps. Separate from the legacy-quote-removal heresy sweep. |
| 705 | Principle | Maximum | NOTA's bracket-only string discipline makes a complete NOTA expression embedding-safe inside any host language whose string syntax uses double quotes (JSON, Rust, Nix, YAML, TOML, shell, env vars, DB columns, XML, HTTP bodies). NOTA-in-anything-with-doublequote-strings is escape-free. Load-bearing design property, not incidental. |

Also touched: record 700 (Spirit CLI shell-double-quote correction), 701 (CLI examples wrap inline NOTA in shell double quotes). Already manifested in `skills/spirit-cli.md` and `skills/nota-design.md` shell-invocation section pre-sweep; no additional work needed there from this subagent's lane.

### Existing state of destinations

- **`skills/nota-design.md`** — already carried "two bracket-string forms" (records 26-27 era) and the shell-double-quote-wrapping convention. Did NOT carry: (a) the **structural** rule that quotation marks do not form string types (record 698's strengthening), (b) the legacy-input-only / migration-toward-canonical asymmetry, (c) the **embedding-safety principle** (record 705), (d) the single-letter `a` vs `[a]` distinction (record 690).
- **`AGENTS.md`** Hard Overrides — carries the "NOTA is the only argument language" override which includes one line on inline NOTA shell calls. Does NOT carry: the structural rule (record 698), the embedding-safety principle (record 705).
- **`INTENT.md`** (workspace) — no dedicated NOTA section; the language layer's design rationale isn't synthesised at the workspace-prose level.
- **`repos/nota/INTENT.md`** — has "Language shape" section but does NOT carry the bracket-strings-exclusively rule or the embedding-safety principle.
- **`repos/nota-codec/INTENT.md`** — **did not exist**. `nota-codec` had `ARCHITECTURE.md` but no per-repo INTENT.md synthesis.

## §2 Migration table — record → destination

| Record | Substance | Destination(s) | Action |
|---|---|---|---|
| 690 | Bracket forms + bare-token shorthand for short strings | `skills/nota-design.md` "Strings come EXCLUSIVELY from bracket forms" + bare-token paragraph | Applied |
| 698 | Structural rule: brackets ARE the string form; quotation marks do NOT form string types | `skills/nota-design.md` (primary), `AGENTS.md` Hard Override refinement (proposed), `repos/nota/INTENT.md` (verbatim quote), `repos/nota-codec/INTENT.md` (encoder-side enforcement narrative) | Applied to skills + per-repo; AGENTS.md proposed below |
| 703 | Legacy `"..."` acceptance authorised for removal; migration sweep across emitters | `skills/nota-design.md` "Quotation marks are strongly disfavored and never emitted by canonical encoding" paragraph (names the sweep targets), `repos/nota-codec/INTENT.md` "Decoder accepts legacy quoted strings for migration" | Applied |
| 704 | Legacy `intent/*.nota` separate-extractor path | `skills/nota-design.md` (one sentence in legacy paragraph), `repos/nota-codec/INTENT.md` | Applied |
| 705 | Embedding-safety: NOTA-in-double-quote-host is escape-free | `skills/nota-design.md` "Embedding-safety is the load-bearing consequence" paragraph, `repos/nota/INTENT.md` "Strings come exclusively from bracket forms" §2, `repos/nota-codec/INTENT.md` "Embedding-safety is a contract the codec preserves", `INTENT.md` workspace section (proposed) | Applied to skill + per-repos; workspace INTENT.md proposed below |

One record → multiple destinations is normal per `intent-manifestation.md` §"The decision tree".

## §3 Edits applied directly

### `/home/li/primary/skills/nota-design.md`

Replaced the prior "Bracket and bare strings" + "Two bracket-string forms" + "Shell invocation uses outer double quotes" three-paragraph block with a single expanded section. The new content:

- **"Strings come EXCLUSIVELY from bracket forms"** — opens with the structural rule (record 698 framing). Lists the two canonical bracket forms + the bare-token shorthand. Calls out the single-letter `a` vs `[a]` case (record 690).
- **"Quotation marks are strongly disfavored and never emitted by canonical encoding"** — new paragraph. Names the `read_legacy_quote_string` lexer path as explicitly legacy. Names the `write_string` three-branch encoder shape and the structural-impossibility of emitting `"`. Calls out the migration sweep targets (CriomOS-home Nix modules, `lojix-cli`, downstream consumers) per record 703; mentions the separate `intent/*.nota` extractor per record 704.
- **"Shell invocation uses outer double quotes"** — preserved (was already correct).
- **"Embedding-safety is the load-bearing consequence"** — new paragraph. Names every host language where NOTA embeds escape-free. Frames JSON-in-JSON's escape cascades as the contrast. Per record 705.

No code excerpts to specific lines (skill files don't pin to line numbers). No report references (skills don't cite reports per `skill-editor.md`).

### `/home/li/primary/repos/nota/INTENT.md`

Added new section **"Strings come exclusively from bracket forms"** before the "Language shape" section. Carries:

- The structural rule with verbatim psyche quote (record 698) in italics.
- The two canonical forms + bare-token shorthand summary.
- The legacy-non-canonical-and-slated-for-removal disposition.
- The embedding-safety principle (record 705) as the load-bearing consequence, with verbatim quote in italics.

Voice matches the file's existing descriptive-synthesis voice. No mention of specific reports (architecture/intent files don't cite reports).

### `/home/li/primary/repos/nota-codec/INTENT.md`

**Created** (file did not exist). Synthesises the codec-side intent:

- **"Encoder is the canonical-emission engine"** — verbatim psyche quote (record 698). Names the three-branch structural impossibility.
- **"Decoder accepts legacy quoted strings for migration"** — explains the asymmetry (strict-on-emit / lenient-on-input). Migration is the path. Per record 703.
- **"Embedding-safety is a contract the codec preserves"** — verbatim psyche quote (record 705). Names what would break the contract.
- **"Macro-pattern integration"** — short bridge to `ARCHITECTURE.md` §"Macro-pattern integration" without duplicating it.

Cross-references `repos/nota/INTENT.md` and `skills/nota-design.md`.

## §4 Proposed shared-file edits

These need orchestrator consolidation (subagents propose; orchestrator applies for workspace-shared files where multiple subagents may have contributions).

### AGENTS.md — refine the existing NOTA hard override

Current text (lines 167-175):

```
- **NOTA is the only argument language.** Every component binary
  (CLI and daemon) takes exactly one argument: a NOTA string, a path
  to a NOTA file, or a path to a signal-encoded (rkyv) file. No flags
  (`--verbose`, `--format`, `--config=path`) — ever. If a binary
  needs new configuration, the contract's NOTA schema gets a new
  field. Inline NOTA shell calls wrap the whole NOTA object in
  double quotes — `spirit "(Record (...))"` — because NOTA strings
  use bracket strings, not `"` delimiters. Full rule:
  `skills/component-triad.md` §"The single argument rule".
```

The existing "Inline NOTA shell calls" tail-sentence implicitly carries the bracket-string rule but doesn't make it structural. Per record 698 (Maximum-certainty Clarification strengthening), the rule should land as an explicit structural fact, and per record 705 the embedding-safety implication is worth one line in the hard override because it is a per-keystroke design constraint on every emitter.

**Proposed addition as a separate hard-override bullet** (cleaner than appending to the existing one, which is about the single-argument rule):

```markdown
- **NOTA strings come EXCLUSIVELY from bracket forms; never emit
  quotation marks.** Brackets ARE the string form — `[text]` for
  inline, `[|text|]` for bracket-safe / multi-line, bare camelCase
  or kebab-case at `String` schema positions. Quotation marks do
  NOT form string types in NOTA. The `nota-codec` encoder
  structurally cannot emit `"`; legacy quoted-string input is
  accepted as migration only and slated for removal. Inline NOTA
  shell calls wrap the whole NOTA object in shell double quotes —
  `spirit "(Record (...))"` — because NOTA never contains `"`.
  The same property scales up: NOTA embeds escape-free inside any
  host whose string syntax uses double quotes (JSON, Rust, Nix,
  YAML, TOML, shell, env vars, DB columns) — NOTA-in-anything-with-
  double-quote-strings is escape-free. Full discipline:
  `skills/nota-design.md` §"Strings come EXCLUSIVELY from bracket
  forms".
```

Orchestrator: insert this new bullet immediately after the existing "NOTA is the only argument language" bullet (between lines 175 and 176 of current `AGENTS.md`), so the two NOTA hard overrides sit together. Optionally trim the tail-sentence about shell double quotes from the existing "NOTA is the only argument language" bullet since the new bullet covers it more thoroughly.

### INTENT.md (workspace) — add a NOTA section

The workspace `INTENT.md` currently has no NOTA section. Per record 705 being a load-bearing design principle of the universal-data-format the workspace builds on, and per record 698 being a Maximum-certainty structural correction that shapes how every emitter writes, a synthesis section is warranted.

**Proposed addition** — insert after the "Workspace truth lives in files every agent can open" section (around line 200), before "The Nix store is not a search surface":

```markdown
## NOTA is the universal embedding-safe payload

NOTA is the workspace's text data format for typed records — used
for `.schema` files, for signal payloads on the wire, for `intent`
records in Spirit, and for inline CLI arguments to every persona
component. The format's load-bearing design property is that
**NOTA never contains a double quote character.** Brackets are the
string form (`[text]` inline; `[|text|]` for bracket-safe and
multi-line content); quotation marks do not form string types.
*"nota uses brackets for strings, not quotation marks. safe nota
is free of unescaped quotation marks, they are strongly disfavored,
and do not surround string types - that is what [ and [| do."*

The consequence is **universal embedding-safety**: a complete NOTA
expression embeds escape-free inside any host whose string syntax
uses double quotes — JSON, Rust string literals (including raw
`r"..."`), Nix attribute values, YAML scalars, TOML strings, shell
double-quote arguments, HTTP request bodies, database string
columns, environment variable values, XML attributes. *"JSON-in-
JSON requires escape cascades; NOTA-in-anything-with-doublequote-
strings is escape-free. This is a load-bearing design property of
NOTA, not an incidental side effect."* The shell-double-quote
wrapping convention (`spirit "(Record (...))"`) is the same
principle at the CLI scale; design new emitters and storage paths
to take advantage of it.

`nota-codec` enforces the discipline structurally on the emitter
side: the encoder's `write_string` has three branches (bare
identifier, `[|...|]` block, `[...]` inline) and no quote branch
exists. Legacy quoted-string input is accepted as migration only
(record 703) and is authorised for removal once all emitter sites
migrate. Legacy `intent/*.nota` files get a separate programmatic
extractor that preserves psyche timestamps (record 704), kept
distinct from the legacy-quote-removal heresy sweep across
emitters.

Full discipline: `skills/nota-design.md` §"Strings come EXCLUSIVELY
from bracket forms".
```

Orchestrator: this consolidates with whatever Subagent C surfaces about Spirit deployment (since the shell-double-quote-wrapping convention is downstream of this property). If C's spirit-deployment section also wants to mention shell double quotes, it can reference back to this NOTA section rather than restating.

## §5 Reports retired

- **`reports/designer/348-nota-string-discipline-empirically-confirmed-2026-05-25.md`** — deleted. Substance landed:
  - The psyche rule (§1 of /348) → `skills/nota-design.md` "Strings come EXCLUSIVELY from bracket forms" + workspace `INTENT.md` proposed addition + `repos/nota/INTENT.md` new section.
  - The spec citation (§2 of /348) → already in `repos/nota/README.md`; the skill summarises rather than cites lines.
  - The implementation evidence (§3 of /348) → `repos/nota-codec/INTENT.md` "Encoder is the canonical-emission engine" + skills/nota-design.md paragraph naming the three encoder branches.
  - The empirical proof (§4 of /348) → not preserved as line-by-line output (that's run-once test evidence, not load-bearing rule); the discipline statements derived from it ARE preserved in the skill and INTENT files.
  - The /187 heresy diagnosis (§5 of /348) → preserved as known migration debt in `skills/nota-design.md` legacy paragraph (names CriomOS-home Nix modules + lojix-cli as sweep targets) and in `repos/nota-codec/INTENT.md` migration section. The /187 operator report still exists in `reports/operator/` and is operator territory.
  - The §6 emitter survey → encoded as the migration-sweep target list in `skills/nota-design.md`.
  - The §7 action items → these are operator/system-specialist work items (1, 2, 3) and a future designer decision (4). The discipline they implement is now in the skill; the work-item routing should land as beads if the orchestrator agrees (note for orchestrator: consider opening beads for items 1-3 against operator and system-specialist labels).
  - The §8 validation summary → captured as the "asymmetry: strict on emit, lenient on input" framing in `nota-codec/INTENT.md`.

- **`reports/operator/` reports referenced** — NOT touched. Operator territory per the frame's HARD RULES item 11.

## §6 What's still open

- **Beads for the migration sweep work items** — Subagent B did not open beads for /348 §7 action items 1-3 (system-specialist update of CriomOS-home Nix modules; operator migration of `lojix-cli`; operator-wide heresy-scan sweep). Orchestrator's call: open in `5-overview.md` or defer to next-session work. The discipline is captured in the skill; the work is downstream.
- **Designer decision on legacy-quote-removal timing** — /348 §7 item 4 asked whether the lexer's `read_legacy_quote_string` path can collapse once all emitters migrate. Per record 703 the answer is "yes, authorised" — but the actual collapse needs all emitters done first. No new intent capture needed; the discipline already says "after all emitter sites migrate".
- **`AGENTS.md` and workspace `INTENT.md` proposed edits** — pending orchestrator consolidation in §4 above.

## §7 Discipline observations

- The structural-rule strengthening (698 from 690) is a textbook example of why authoring-preference statements graduate to format-level structural rules over time. The skill now carries the structural framing, not the authoring-preference framing.
- The embedding-safety principle (705) is the kind of "load-bearing design property" that deserves multiple homes: the skill (because emitters need to honour it on every keystroke), the per-repo INTENT (because it's the value proposition of the nota language), and the workspace INTENT (because it shapes how new persona components store data). This three-destination landing matches `intent-manifestation.md` §"The decision tree" — one record can manifest in multiple places.
- Creating `repos/nota-codec/INTENT.md` from scratch is on-policy: `repo-intent.md` calls for INTENT.md per-repo when the repo has psyche-intent substance worth synthesising; `nota-codec` clearly does — it's the structural enforcer of the language's bracket-only rule.
- No changes proposed to `ESSENCE.md`. The NOTA bracket-string rule is structural-and-topic-specific; it lives in the skill + per-repo INTENT + workspace INTENT prose, not in the gold-of-the-gold layer.
