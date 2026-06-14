# New-Moon Meta-Report — Spirit Intent Activity (2026-06-13)

Spirit `0.12.1`, marker `(1269 1736211875602223390)`. Audit of the day's captured intent for the Structural Forms / schema-next epic, plus the two guardian rejections.

## What landed today — five accepted records

All five sit in the `schema-next` / `nota-next` arc (one also tagged `aski`), in `(Technology (Software ...))` domains, privacy `Zero`.

| id | Kind | Certainty / Importance | One-line meaning |
|---|---|---|---|
| `wfdt` | Decision | Medium / Minimum | The schema substrate self-hosts its definition types — generate `schema-next` macro-table types from `core.schema` instead of hand-writing them in `declarative.rs`; the chosen first proving step of absorbing Rust type surface into schema. |
| `2zed` | Principle | High / Minimum | Everything is data conforming to a schema type — a macro is just a value of a specialized struct, its pattern and template ordinary typed fields; no privileged escape-hatch representation. The unifying lens for the substrate. |
| `7c71` | Principle | VeryHigh / Medium | A programming language *is* a set of structural macros (constructors over typed, counted objects). Conventional languages freeze that set in the compiler; treating the macro set as data makes the language infinitely extensible and far easier for an LLM to read/write/reason about. |
| `my86` | Principle | High / Low | A file's whole structure is a typed tree of structural-form nodes, each recognising a block by shape and recursively decoding its children. No hand-written parser: the grammar is the type, the type is the reader. The structural realization behind the `aski` goal. |
| `wqdi` | Principle | Medium / Minimum | Multi-argument type references use NOTA's flat positional form (head then args inline — `Map K V`), not a grouped/delimited form. Settles the `Map` reference shape and generalizes to all multi-argument type-reference applications. |

These form a coherent ladder, not five scattered notes: a top principle (`7c71`, the language-is-macros thesis), the unifying data lens (`2zed`), the structural-forms reader mechanism (`my86`), one concrete syntax settlement (`wqdi`), and one concrete build step (`wfdt`). Certainty/importance track that altitude — the thesis carries `VeryHigh/Medium`, the implementation step `Medium/Minimum`.

## The two guardian rejections and what they taught

Both were rejected `Overstated`. The lesson is identical and is the headline of this new-moon: **the existing corpus already held most of what was being re-asserted.** The guardian is doing intent-density work, not gatekeeping novelty — it pulls records sharing the candidate's referents/topic and rejects when the durable arrow is already on file.

**(a) The epic record — architecture already settled.** A broad "epic" record restating the component-triad / schema architecture was rejected because the corpus already carries it at full strength:
- `7sx6` — Correction, `Maximum / VeryHigh`: "Every component has exactly two contracts and no more: `signal-<component>` and `meta-signal-<component>` — no third contract, no owner-signal split, no engine-management split."
- `u7tj` — Decision, `High / High`: wire-contract schemas live in the `signal-<component>` crate because the wire shape is the cross-component compilation boundary Rust must see as one canonical source.
- `a71r` — Principle, `VeryHigh / High`: every component engine defines its Signal/Nexus/SEMA interfaces in schema and conducts core logic through schema-emitted traits over those root types (the workspace-wide generalization of Spirit-1326).

When a candidate's claim is already pinned at `Maximum`/`VeryHigh` by settled records, a fresh "epic" assertion is overstated by construction — it claims to establish what is already established. Lesson: epics summarize and locate; they don't re-record.

**(b) The meta-signal-placement Constraint — covered by existing records.** A Constraint asserting where the meta policy signal belongs was rejected `Overstated` as covered by `7sx6` / `u7tj` / `tb9h`. The live corpus equivalents are exactly there: `7sx6` (the two-contracts Correction at `Maximum`), `u7tj` (contract-crate placement Decision), and `8bwo` (Decision, `VeryHigh/High`: each component exposes both contracts as two thin CLI clients — working client named after the component, meta client prefixed `meta-`). Note: `tb9h` cited in the guardian's rationale is **not present in the active store** (`Lookup tb9h` → not found) — it was a corpus anchor that has since been folded/superseded; the durable coverage today rests on `7sx6` + `u7tj` + `8bwo`. Lesson: placement of the meta signal is not a new constraint to mint — it is a corollary of the two-contracts rule already at maximum certainty.

## Net durable intent that actually moved

The new ground today is entirely the **schema-next language thesis**, not the triad/contract architecture (which the guardian confirmed is closed). What is genuinely new:

- The **"language = structural macros, as data"** thesis is now on record at `VeryHigh` (`7c71`) — previously implied by self-hosting records like `j9du` (NOTA grammar is schema-describable) and `t85k` (the macro-node grammar is itself schema-expressible) but never stated as the central claim.
- The **structural-forms reader** is recorded as a first-class principle (`my86`): grammar-is-type, no hand-written parser, tied explicitly to `aski`.
- One concrete **syntax decision** (`wqdi`, flat `Map K V`) and one concrete **first build step** (`wfdt`, self-host the macro-table types from `core.schema`).

## Coherent intent picture for the Structural Forms epic

The corpus now reads as a single, layered arrow — strongest at the top, concrete at the bottom:

1. **Thesis (`7c71`, VeryHigh):** every language is a macro set; freezing it in the compiler is the limitation; treat it as data → infinite extensibility + LLM-legibility.
2. **Lens (`2zed`, High):** everything, the macro included, is typed data in the schema-NOTA-rkyv tri-form — no escape hatch.
3. **Self-hosting closure (`j9du`, `t85k`):** NOTA's grammar and the structural-macro-node grammar are themselves schema-expressible — the loop closes on itself.
4. **Reader mechanism (`my86`, High):** a file is a typed tree of structural forms; the type is the parser; this is the `aski` realization.
5. **Concrete settlements:** syntax shape `wqdi` (flat positional type references), build step `wfdt` (generate the macro-table types from `core.schema` as the first proving move).

Surrounding this, the **component-triad / contract architecture is settled and should not be re-recorded** — `7sx6` (two contracts, Maximum), `u7tj` (contract-crate placement), `a71r` (schema-emitted trait runtime), `8bwo`/`xbc2`/`0678` (CLI clients, strict schema contracts, contract-repo separation). The guardian's two rejections today are the operative discipline note for the next session: **the architecture frame is closed; capture only the schema-next language layer, and even there prefer locating existing records over minting epics.**

## Sources / verification notes
- All ids verified live via `spirit "(Lookup <id>)"` against `0.12.1`, marker `1269`.
- `tb9h` returns `record not found` — cited in the guardian rationale but absent from the active store; corpus coverage rests on `7sx6` + `u7tj` + `8bwo`.
- Corpus context drawn from stash handles 12 (referents `schema-next`/`nota-next`/`aski`, 9 records) and 13 (meta-policy-signal text match, 2 records).