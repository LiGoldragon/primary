# Audit — schema-operator's schema-help implementation

*schema-designer · report 3 · audits the implementation landed on the
five `schema-help` branches against the design (reports 1–2), my POC
(`reports/schema-designer/poc/`), and Spirit `6th4`.*

## Verdict

**Landed cleanly and faithful.** The two independent tracks converged on
**identical golden output strings** — the strongest signal the
double-implementation can give. Operator's `signal-spirit/src/help.rs`
(799 lines) realizes the agreed model exactly; my POC and their
implementation, written separately, render the same `(Help X)` for every
shared case. One minor follow-up (Stream/Family fidelity); nothing blocks.

## Independent convergence — identical golden outputs

| `(Help X)` | operator golden test | my POC golden test |
|---|---|---|
| `Record` | `(Record { Entry Justification })` | same |
| `Entry` | `(Entry { Domains Kind Description Certainty Importance Privacy Referents })` | same |
| `Domains` | `(Domains (Vec Domain))` | same |
| `Description` | `(Description String)` | same |
| `VerbatimQuote` | `(VerbatimQuote { QuoteText OptionalAntecedent })` | same |
| `RecordAccepted` | `(RecordAccepted RecordIdentifier)` | same |

Two people, two codebases, one output. That is the convergence the
parallel tracks existed to produce.

## What landed cleanly

- **Client-side, none in the daemon.** `help.rs` lives behind `nota-text`;
  `spirit.rs::help_response()` recognizes `(Help …)` via
  `HelpRequest::from_text`, builds the model, renders, and returns — all
  **before** the socket connect; non-Help returns `None` and falls
  through to normal `Input` parsing + transport. No `Input::Help` /
  `Output::HelpReported` in the contract. Matches `6th4` verbatim.
- **Runtime projection, the recommended path.**
  `HelpModel::from_signal_schema_source()` calls
  `SchemaSource::from_schema_text(SIGNAL_SCHEMA_SOURCE)` — no new codegen
  (`schema-rust-next` got only an `INTENT.md`), so Help *is* the parsed
  schema and cannot drift. The two traps from report 1 §5 are both
  handled: it uses `from_schema_text` (sidestepping `UnresolvedImportCrate`)
  and inserts imports as bare-name references; it projects from the
  **`Source*` AST** (`SourceRootEnum` / `SourceNamespace` /
  `SourceReference` / `SourceVariantPayload`).
- **Typed rkyv tree, actualized.** `HelpModel` / `HelpResponse` /
  `HelpEntry` / `HelpBody` / `HelpTypeExpression(Kind)` all derive rkyv
  (the recursive `Kind` uses the `omit_bounds` idiom). The round-trip test
  archives both the model **and** the rendered `HelpResponse` — the
  actualized typed tree, exactly as `6th4` requires.
- **The one-level asymmetry** is correct: a struct/enum payload inlines one
  level (`{ … }` / `[ … ]`); a newtype/scalar/undeclared payload shows the
  bare reference name; bare `(Help)` is every Input+Output root expanded
  one level. Container heads echo the source faithfully — `(Vec Domain)`
  flows through the `Application` arm (the `Vector` arm only fires for the
  canonical `Vector` spelling, which the spirit schema does not use).
- **Real NOTA codec for the recognizer.** `HelpRequest::from_text` parses
  with `nota_next::Document` (not a hand-rolled grammar — better than my
  POC's stand-in tokenizer) and is itself rkyv-derived.
- **Discipline clean.** Methods on data-bearing types throughout; typed
  `HelpError` (thiserror, `impl From`); no free functions, no ZST
  namespaces.
- **Verification (operator-run, all green):** signal-spirit help golden +
  rkyv model/response round-trip; no-default dependency boundary;
  meta-signal-spirit `--features nota-text`; spirit process-boundary Help
  **without a daemon socket** (proving offline / daemon-down works — the
  designer rationale for client-side, now a passing test); binary-only
  no-nota-next dependency surface; the ignored Nix-integration Help test
  (143.70s).

## Findings

1. **(Minor) Stream/Family fall back to raw schema text.**
   `HelpBody::from_declaration` maps `SourceDeclarationValue::Stream | Family`
   to `HelpBody::Text(value.to_schema_text())`, and an inline field
   declaration to `HelpTypeExpressionKind::Inline(String)`. So
   `(Help IntentEventStream)` renders the stream's raw schema text inline
   rather than a structured one-level shape with named slot references.
   It is correct and readable, but it is the one place the typed tree
   degrades to a string and the one-level rule is not uniform. *Follow-up:
   give Stream/Family a typed `HelpBody` variant (slots as named
   references — `token`/`opened`/`event`/`close`), so every node is typed.*
   Low priority; streams are few.

2. **(Note, not a defect) Container-head spelling is source-echoing, by
   construction.** Because `Vec` parses as an `Application` and `Vector` as
   the built-in, help shows whatever the source wrote. That is the right
   default. If a contract ever mixes both spellings, help will too — worth
   a one-line deliberate decision (echo vs canonicalize) if that ever
   arises. No action now.

3. **(Note) `6th4` certainty/importance = Medium/Medium.** Reasonable for
   a design decision refined across several turns; I am not churning it.
   The capture is faithful and complete — verified, not duplicated, per
   the one-capturer rule.

## Status and next

The pilot is **functionally landed** on operator's branches and verified.
My POC + golden specs (report 1 §7) are satisfied by the implementation —
identical outputs. Remaining is operator's integration of `schema-help` to
each repo's `main`, then broadening the *same generic projection* to
`signal-mentci` (one identical accessor — no mentci-specific logic). My
track's open contribution is the Stream/Family fidelity follow-up if the
psyche wants uniform typed help for those, and auditing the main
integration when it lands.
