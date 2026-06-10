# Spirit agglomeration pass — manual auditor run, 2026-06-10

Landing witness for the first hand-run of the future automated "auditor"
(commissioned by report `577-intent-tool-state-and-the-real-flaw`, step 1 of
its distill-then-gate-then-automate plan). Ran live against the deployed Spirit
daemon (v0.4.0, ordinary socket `spirit.sock`) using only reversible operations.

## Headline findings

1. **Agglomeration done on the three worst topics.** 21 canonical records
   reaffirmed at `Maximum` magnitude; 43 clearly-redundant source records marked
   as removal candidates (`certainty`/magnitude set to `Zero` via
   `ChangeCertainty`). All reversible. No `Remove`, no
   `CollectRemovalCandidates`, no private record touched.

2. **Marking removal-candidates does NOT de-bloat default queries — empirically
   confirmed at scale.** After marking 43 records `Zero`, every default count is
   unchanged: total 1402, public 1395, `spirit` 150, `nota` 155, `schema` 385.
   The reason is structural (see §"Empirical de-bloat finding"): the deployed
   query filters on topic + kind + **privacy**, never on magnitude. To actually
   shrink the store the psyche must run `CollectRemovalCandidates` — and even
   that has a gap (below).

3. **A real contract gap surfaced.** `CollectRemovalCandidates` matches the same
   `Query` (topic/kind/privacy) and has **no magnitude filter**. So the deployed
   daemon cannot select "all `Zero`-certainty records" for collection — the
   removal-candidate convention is not wired to any selection mechanism. Flagged
   for the psyche/operator in §"Contract gaps".

## Record counts — before / after

The numbers below are query counts (`(Count (Any None <privacy>))`), not store
cardinality changes — marking does not remove. A self-test record (`izjk`) was
created during the empirical check (+1 to totals).

| Scope | Before | After | Change |
|---|---|---|---|
| Total (any privacy) | 1401 | 1402 | +1 (self-test `izjk`) |
| Public (`Exact Zero` privacy) | 1394 | 1395 | +1 (self-test) |
| Private (`AtLeast Minimum`) | 7 | 7 | untouched |
| `spirit` topic (public) | 150 | 150 | unchanged (marking ≠ removal) |
| `nota` topic (public) | 155 | 155 | unchanged |
| `schema` topic (public) | 385 | 385 | unchanged |

Records **reaffirmed** (raised to `Maximum`): 21. Records **marked removal
candidate** (`Zero`): 43. Records touched total: 64.

## Method recap

The deployed `Observe`/`LookupStash`/`Count` reads return only `Entry`s (topics,
kind, description, magnitude, privacy) — **never the base36 identifiers**, and
`Lookup` requires an identifier you already have. There is no query path that
enumerates identifiers. To target existing records I:

1. Took a read-only snapshot copy of `~/.local/state/spirit/spirit.sema`.
2. Extracted candidate 4-char base36 identifiers from the redb key-index runs.
3. `Lookup`-validated every candidate through the daemon (authoritative),
   yielding the full (identifier → entry) map for all 1402 records.
4. Clustered each target topic by meaning (not just token overlap — paraphrases
   fall below any jaccard threshold), kept any record adding distinct nuance,
   and collapsed only crystal-clear restatements.
5. For each cluster: reaffirmed one canonical at `Maximum`, marked the others
   `Zero`.

## Clusters collapsed

For each cluster: the canonical (kept, raised to `Maximum`) and the sources
folded into it (marked `Zero`). Gloss = first words of each record's text.

### `spirit` (8 clusters, 15 sources)

- canonical `kvib` — multi-topic query matching (partial = one-or-more, full =
  every requested topic).
    - `oe2s` — same point ("Production Spirit search supports multi-topic ...").
- canonical `qtbd` — random opaque record id = 96-bit CSPRNG → base36
  shortest-unique-prefix, min-three-per-kind.
    - `y5m9` — same, without the 96-bit specificity.
- canonical `hefy` — write acknowledgements token-cheap + must not echo content.
    - `etxq` — "accept replies must be token-cheap."
    - `yu7l` — "acknowledgements stay terse."
- canonical `h2oa` — releases need schema-aware version numbers.
    - `b58w` — "version tags that signal schema compatibility."
- canonical `k5y3` — privacy is a `Magnitude` on the privacy axis (Zero=open,
  Maximum=sealed); reuses Magnitude vocabulary (the full superseding decision).
    - `114j` — "no-privacy value is Zero rather than None."
    - `y40b` — "privacy modeled as a directional magnitude."
- canonical `0dys` — simpler-to-complex variant ladder; short forms with
  defaults that lower to the canonical complex root.
    - `44b4`, `55pi`, `lstz`, `xbb5`, `zp10` — five restatements of "Spirit
      should offer shorthand forms that lower to the full typed API."
- canonical `lxo3` — recency as a first-class composable query filter
  (Newest N / Since / Window) alongside topic+kind+certainty.
    - `73r4` — "combined recency/time filtering with topic filtering."
    - `md40` — "time-range and relative-recency searches composed with topic."
- canonical `wm4q` — typed access-classification model, Public default, not a
  boolean.
    - `clfe` — same ("typed access/classification field, Public default, not
      a private/public boolean").

### `nota` (5 clusters, 16 sources)

- canonical `vfjw` (was already Maximum) — NOTA strings come EXCLUSIVELY from
  bracket forms; quotation marks do not form strings; legacy quoted input is
  migration-only (the full structural rule).
    - `tlaf`, `d4dl`, `18kl`, `rvh4`, `olno`, `xt5h`, `kpcb` — seven
      restatements / early-exploratory versions of "use brackets not quotes /
      keep NOTA CLI shell-safe," now subsumed by the settled Maximum rule.
- canonical `sg4o` — wrap inline NOTA in shell double quotes; the bracket-string
  form exists so NOTA itself avoids double quotes.
    - `t8bs` — "bracket-string redesign so inline NOTA fits in shell quotes."
    - `wvaa` — "bracket-string examples use apostrophes not double quotes."
- canonical `t4gd` — a daemon binary must compile with no NOTA code at all;
  NOTA gated behind a `nota-text` feature only the CLI enables.
    - `e6ri` — "daemons cannot understand NOTA — universal constraint."
    - `pjvv` — "daemons cannot understand or decode NOTA text."
- canonical `lyo2` — NOTA is a thin structural library exposing block predicates
  (is_square_bracket / holds_N_objects / qualifies_as_symbol …) for upper layers.
    - `6qrb` — "structural library for delimiter/object inspection ..."
    - `r8u5` — "thin structural library for delimiter-level methods ..."
- canonical `fvtf` — "qualifies as" not "is"; case/type legality belongs to the
  schema/macro layer, with promote-then-demote.
    - `byg0` — "Nota should not decide PascalCase/camelCase legality ..."
    - `bg2q` — "raw NOTA reading should not decide case legality; promote/demote."
    - `qfm2` — "qualified-symbol candidate demoted by schema context ..."

### `schema` (8 clusters, 12 sources)

- canonical `19dm` (was already Maximum) — brace is always a key-value map;
  namespace uses pair-style (not named-object), conceptually a dynamic enum.
    - `ktcb` — "brace objects in schema are always key-value maps."
    - `mz1n` — "schema braces must stay true NOTA key-value maps."
    - `1oez` — "namespace declarations must not repeat the type name as head."
- canonical `qw1j` — `[]` is and always has been the vector delimiter; agents
  must not redefine it as struct syntax.
    - `b4x8` — same (`[]` is a vector at the NOTA layer; do not say otherwise).
- canonical `6wwf` — reactive/base schema roots are purely positional; Input and
  Output are bare at their known positions, never labeled; resolves 874/876.
    - `gzwj` — "explicit root field labels such as Input@ are wrong."
    - `nu59` — "authored root must not redeclare standard fields."
    - `hfdn` — "schema files do not need an outer root record."
- canonical `p8sq` — a `.schema` file's root struct is implied by the extension;
  expose fields positionally, no explicit Schema record wrapper.
    - `21rh` — same (root Schema struct implied by file type, positional).
- canonical `fo38` — enum declaration and macro application share the
  head-plus-one-group form; head is type-name (enum) vs operator (macro).
    - `mha3` — same ("identical form ... only question is type-name vs operator").
- canonical `utaa` — scalar floor named in full English (String/Integer/Boolean);
  never Bool or U64.
    - `5bkf` — same ("scalar floor should use String, Integer, Boolean; Bool
      not allowed").
- canonical `hl1z` — schema defines data types ONLY; no effects, fan-out, or
  Features section (EffectTable/FanOutTargets/StorageDescriptor were drift).
    - `5vjt` — same ("authored schema files do NOT carry a Features section").
- canonical `dtwe` — schema-generated Rust emits into a dedicated `src/schema`
  module tree inside the crate source.
    - `ll2j` — same ("schema-generated Rust should materialize under
      `src/schema/<module>.rs`").

## Full list — records marked removal-candidate (Zero)

All reversible: restore with `(ChangeCertainty (<id> <Magnitude>))`.

`spirit` (15): `oe2s` `y5m9` `etxq` `yu7l` `b58w` `114j` `y40b` `44b4` `55pi`
`lstz` `xbb5` `zp10` `73r4` `md40` `clfe`

`nota` (16): `tlaf` `d4dl` `18kl` `rvh4` `olno` `xt5h` `kpcb` `t8bs` `wvaa`
`e6ri` `pjvv` `6qrb` `r8u5` `byg0` `bg2q` `qfm2`

`schema` (12): `ktcb` `mz1n` `1oez` `b4x8` `gzwj` `nu59` `hfdn` `21rh` `mha3`
`5bkf` `5vjt` `ll2j`

## Canonical records (kept, raised to Maximum)

`spirit`: `kvib` `qtbd` `hefy` `h2oa` `k5y3` `0dys` `lxo3` `wm4q`
`nota`: `vfjw` `sg4o` `t4gd` `lyo2` `fvtf`
`schema`: `19dm` `qw1j` `6wwf` `p8sq` `fo38` `utaa` `hl1z` `dtwe`

`vfjw` and `19dm` were already at `Maximum`; the `ChangeCertainty` call is a
no-op reaffirmation on those two.

## Left for the psyche — ambiguous, contradictory, or design-evolution

These are genuine restatement-adjacent pools I deliberately did NOT collapse,
because the records carry an unresolved or contradicted design choice. Collapsing
them would destroy the very lineage that records the open question.

1. **Record-identifier minimum length: three vs four — open contradiction.**
   `qtbd`/`y5m9`/`f36y`/`0zk5` say min-THREE-per-kind; `tw81` (Correction) and
   `rh29` (Constraint) say min-FOUR. The deployed daemon uses min-four
   (`RECORD_IDENTIFIER_MINIMUM_CODE_LENGTH = 4`). I kept all of them and did not
   fold the three-char records into the four-char ones — the psyche should
   confirm the four-char rule supersedes the three-char direction, after which
   `qtbd`/`f36y`/`0zk5` could be reworded or retired.

2. **Access-classification: named tiers vs Magnitude-reuse — competing designs.**
   `0gxx`/`fp1i`/`8ll8` (Open/Personal/Sensitive/Sealed named tiers) vs `k5y3`
   (reuse the `Magnitude` ladder, no tier enum, which says it supersedes the
   tier vocabulary). The deployed schema uses `Magnitude` for privacy. I kept
   the tier-named records intact; the psyche should confirm Magnitude-reuse is
   the settled answer before the named-tier records are retired.

3. **Asschema (assembled schema): defined-first vs REMOVED.** `bkzd`/`av1q`/
   `2in8`/`hc0t`/`ct2i`/`fv2a` treat Asschema as the canonical macro-free target;
   `vez8` (Maximum) and `fc7l` (VeryHigh) say Asschema is REMOVED — schema
   deserializes directly into schema-in-Rust with no separate assemble step.
   This is a large live supersession; I left the whole Asschema pool untouched
   rather than risk collapsing within a removed concept. Needs a psyche-confirmed
   sweep of which Asschema records survive.

4. **The `@`-sigil declaration syntax — abandoned mid-chain.** `ilaq`→`r8da`→
   `skz6`→`n2z3` built up the `Name@{...}` / `Name@[...]` at-binder; `own9`
   (Correction, per psyche 2026-06-06) ABANDONS the entire at-binder surface in
   favour of the positional bracket/brace form; `s260`/`degt` are mid-migration.
   `n2z3` is already at `Zero`. Left for a psyche-confirmed pass — the chain
   records the design's actual history and several records are partial.

5. **Capture-discipline corrections vs general syntax rules.** `ous0` (don't
   treat an agent's inferred grammar as captured intent) and `ta58`/`oe6s` (don't
   resurface denied syntax) look similar but `ous0` is a meta capture-gate
   correction while `ta58`/`oe6s` are syntax rules naming specific denied forms.
   Kept separate to preserve the specific denials' provenance.

## Empirical de-bloat finding

**Marking a record as a removal-candidate (`certainty` = `Zero`) does NOT remove
it from default query output.** Verified two ways:

- On a throwaway self-test record (`izjk`, topic `agglomeration-selftest`):
  created it, observed it (count 1), set certainty `Zero`, observed again —
  still count 1, still stashed and returned by `Observe`.
- At scale: after marking all 43 sources `Zero`, total/public/per-topic counts
  are byte-for-byte unchanged (1402 / 1395 / 150 / 155 / 385).

**Mechanism** (from `src/store.rs`): `Store::observe` and `Store::count` filter
through `Query::matches`, which checks `topic_match` + `kind` + `privacy_selection`
only — it never looks at `magnitude`. The `(Exact Zero)` in a query is a
**privacy** selector (Zero = public), not a magnitude selector. So a record at
magnitude `Zero` is fully visible in every default query; the "removal candidate"
state is a pure soft-tombstone flag with no query-level effect.

**Consequence:** marking does not de-bloat. Only `CollectRemovalCandidates`
(which archives + retracts) actually shrinks the store, and that is the
irreversible, psyche-authorized step deliberately not run here.

## Contract gaps (for psyche/operator)

- **`CollectRemovalCandidates` cannot select by magnitude.** It matches the same
  `Query` (topic/kind/privacy) — `if !record.entry.matches(&query) { continue }`
  in `collect_removal_candidates`. There is no magnitude filter anywhere. So a
  collection scoped to a topic would archive+retract EVERY record in that topic,
  not just the `Zero`-certainty candidates. The removal-candidate convention
  (`certainty=Zero` marks a record for removal) is therefore **not wired to any
  selection mechanism** in the deployed contract. A magnitude/certainty selector
  on `Query` (the `lxo3`/`zyab` intent — certainty filtering) is the missing
  piece that would make both candidate-review queries and safe collection work.

- **No identifier-bearing read.** `Observe`/`LookupStash` return `Entry`s with no
  identifiers; an auditor cannot enumerate-with-identifiers through the contract.
  This pass worked around it via snapshot extraction + `Lookup` validation. The
  future auditor needs a real "list records with identifiers" read, or the
  daemon must expose identifiers in observation replies.

- **Skill doc divergences** (already flagged by `577`, re-confirmed here): the
  four-field `Record` shorthand in `skills/spirit-cli.md` is rejected by the
  deployed binary (Entry requires all 5 fields); the daemon-stamps-date-time
  claim has no backing field in the schema.

## Self-test artifact

`izjk` (topic `agglomeration-selftest`, the throwaway de-bloat-check record) is
left in the store at `Zero`/`Zero` (a removal candidate on its own private-to-
this-pass topic). It is harmless and reversible; the psyche may collect or remove
it, or restore it, at will. It is the proof artifact for the de-bloat finding.

## Coverage vs left

- **Covered:** the three worst-offender topics — `spirit` (150), `nota` (155),
  `schema` (385) = 690 of 1394 public records read in full and clustered.
- **Left:** all other 1312 topics (`workspace` 92, `signal` 83,
  `component-shape` 58, `sema` 51, `persona` 47, `schema-language` 43, `cloud`
  39, etc.) — not swept this pass. The full (identifier → entry) map for all
  1402 records was built and is available for a follow-up pass.
- **Reduction achieved:** 43 records soft-retired into 21 canonicals across the
  three topics, conservatively (every nuance-bearing or contradicted record
  kept). Actual store shrink awaits a psyche-authorized `CollectRemovalCandidates`
  run, once the magnitude-selection gap is closed so collection targets only the
  candidates.
