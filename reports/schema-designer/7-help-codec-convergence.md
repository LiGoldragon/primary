# Help-codec — designer track complete, converged with operator

*schema-designer · report 7 · the double-implementation payoff: two
independent implementations of the report-5 schema-codec correction
arrived at the same design.*

## Verdict

My designer `help-codec` track is **implemented, tested, pushed, and
verified** — and it **independently converged** with operator's
`schema-help` track. Both deleted the forbidden hand-rolled `format!`
codec and route help encode/decode through `schema-next`'s declaration
codec. Neither saw the other's code; the convergence is evidence the
report-5 design is right.

## The convergence

| | designer (`help-codec`) | operator (`schema-help`) |
|---|---|---|
| approach | help text via `schema-next` codec | help text via `schema-next` codec |
| hand-rolled `format!` / `Display` encoder | deleted | deleted |
| schema-codec call sites in `help.rs` | 41 | 37 |
| tip | signal-spirit `a4a6f9ce` · schema-next `a8fa3a6e` | signal-spirit `db96b5a5` |

Operator's tip `db96b5a5` ("route schema help text through schema codec")
landed *during* my run, from a base (`cbe60cf0`) that still carried the
hand-rolled codec. Independent arrival at the same approach.

## What my track did

**schema-next (`a8fa3a6e`)** — made `SourceDeclarationValue::from_block(&Block)`
**public** (was private): the block-level declaration decode surface, the
inverse of `to_schema_text`, body-delimiter as discriminant (`{ }` struct,
`[ ]` enum, atom/application reference). The string entry
`from_schema_text` already existed. 6-line change; all **223 schema-next
tests** stay green.

**signal-spirit/help.rs (`a4a6f9ce`)** — deleted the hand-rolled codec
(both the `format!`-built `render_with_name`/`Display` encoder *and* a
parallel hand-rolled `nota_next` `NotaDecode`/`NotaEncode` codec; ~536
lines reworked, net −163). Now:
- **encode** through schema-next: `HelpEntry::to_source_declaration`
  re-heads the typed body over the entry name into a `SourceDeclaration`,
  then `to_schema_text()` emits `(Head <body-schema-text>)`.
- **decode** through schema-next: `HelpResponse::from_schema_text` via
  `SourceDeclarations::from_schema_text`; the Stream/Family `Text` path
  re-parses through `SourceDeclarationValue::from_schema_text`, so even it
  round-trips at the schema layer.
- both `Display` impls only delegate to `to_schema_text()`.
- rkyv derives unchanged; `help` stays `nota-text`-gated, so the
  daemon-default build excludes schema-next/nota-next (the
  `dependency_boundary` tests confirm it; no path dep in `Cargo.lock`).

## One golden-string change (noted)

`DomainMatch`: `(DomainMatch [Any (Partial) (Full)])` →
**`(DomainMatch [Any Partial Full])`**. The schema codec's canonical enum
rendering drops the redundant parens around payload-less variants
(`(Partial)`/`(Full)` carry no payload → bare `Partial`/`Full`). It
round-trips cleanly. Every other golden string — Record, Entry, Domains
`(Vec Domain)`, Description, VerbatimQuote, the Domain enum,
IntentEventStream — is byte-identical through the schema codec. This is a
*correctness improvement* (canonical form) and worth adopting in
operator's track too if it isn't already.

## Tests (captured)

- **schema-next** `cargo test`: 223 passed, 0 failed, no warnings.
- **signal-spirit** `cargo test --features nota-text`: 23 passed, incl.
  the new `generated_help_round_trips_through_the_schema_codec` —
  asserting, for Record (struct), Entry (struct of newtype roles), Domains
  (Vec element-as-reference), RecordAccepted (newtype), DomainMatch (enum),
  IntentEventStream (stream), plus the top-level multi-declaration: both
  the canonical rendered text **and** `decode(render(node)) == node`, and
  that `Display` matches the codec.
- **daemon-default** `cargo build` (no features): clean, no schema-next/
  nota-next pulled.

## Next

- The two tracks agree; operator integrates `schema-help` to `main`
  (their lane). The only delta to reconcile is the `DomainMatch` paren
  normalization — confirm operator's codec produces the same canonical
  form.
- The **universal schema introspection** generalization (report 6)
  builds directly on this proven schema-codec round-trip — it reuses the
  codec wholesale and adds only the per-type self-schema reflection.
