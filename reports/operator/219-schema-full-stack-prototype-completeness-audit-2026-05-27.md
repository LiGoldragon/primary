# 219 — schema full-stack prototype completeness audit

## Frame

Psyche asked for a working prototype mined from recent intent, reports, and
prototypes, then a critique that checks whether the prototype uses every
designed component fully enough to force the next implementation pass.

Sources mined this pass:

- Spirit records 935 and 963-973: schema-derived stack, Nexus as mail keeper,
  and the explicit completeness audit requirement.
- `reports/designer/392-vision-schema-driven-stack-canonical-2026-05-27.md`.
- `reports/designer/395-runtime-nexus-signal-sema-triad-manifestation-2026-05-27.md`.
- `reports/operator/215-nota-schema-nix-test-representation-2026-05-27.md`.
- `reports/operator/218-schema-runtime-actor-upgrade-vision/4-overview.md`.
- Current `spirit-next`, `schema-next`, `schema-rust-next`, and `nota-next`
  mainline prototypes.

## Implemented working slice

The previous `spirit-next` slice proved NOTA CLI input, rkyv socket framing,
generated Signal routes, generated Nexus dispatch, and in-memory SEMA writes.
This pass made the Nexus/SEMA seam more real by adding schema-declared mail and
state marker objects:

```nota
{
  SemaResponse ((Recorded SemaReceipt) (Observed ObservedRecords) (Missed ErrorReport))
  DatabaseMarker [CommitSequence StateDigest]
  SemaReceipt [RecordIdentifier DatabaseMarker]
  ObservedRecords [RecordSet DatabaseMarker]
  ErrorReport [ErrorMessage DatabaseMarker]
  MailLedgerEvent ((Sent SentMail) (Processed ProcessedMail))
}
```

The runtime now uses those generated nouns directly:

```rust
impl MessageProcessed<Output> {
    pub fn processed_mail_event(&self) -> MailLedgerEvent {
        MailLedgerEvent::Processed(ProcessedMail {
            mail_identifier: MailIdentifier(self.identifier().as_integer()),
            database_marker: self.reply.database_marker(),
        })
    }
}
```

The working path is now:

```text
NOTA CLI -> generated Input -> rkyv frame -> daemon
  -> Engine Nexus mail ledger
  -> generated SemaCommand
  -> Store single writer
  -> generated SemaResponse with DatabaseMarker
  -> generated Output
  -> rkyv frame -> NOTA CLI reply
```

## Nix witnesses

`spirit-next`:

- `./scripts/check-local-schema-stack --print-build-logs`
- Passed build, test, fmt, clippy, doc, generated-source freshness, binary
  boundary, generated-signal-plane, runtime-triad, no-old-signal-macro,
  no-production-free-functions, no-production-unit-structs, and local source
  patch checks.
- Process-boundary test passed with a real CLI and daemon over a Unix socket.

`schema-rust-next`:

- `nix flake check --print-build-logs`
- Passed, including the generated mail-event constraint that now requires
  `MessageIdentifier(pub Integer)` and `MessageSent.short_header: Integer`.

## Completeness Audit

| Designed component | Current status | Critique / next development pressure |
| --- | --- | --- |
| NOTA structure | Used as CLI input/output and schema source syntax. | Still lacks a richer object-block diagnostic surface in this prototype. |
| Schema macro lowering | `spirit-next/build.rs` lowers through `schema-next::SchemaEngine` and asserts macro registry coverage. | The macro registry is still Rust-owned; schema-authored macro definitions are not yet real. |
| Assembled schema | `schema-rust-next` emits from `Asschema`; generated source is freshness-checked. | The assembled schema is not persisted as `.asschema` and not inspected by a schema daemon. |
| Rust emission | Checked-in `src/schema/lib.rs` is regenerated from `schema/lib.schema`. | Emission should next split reusable core mail support from component schema. |
| Signal | Generated `Input`/`Output` own short headers, rkyv frames, NOTA conversion, and route rejection. | Signal roots still live in one repo rather than triad repos `signal-spirit` and `core-signal-spirit`. |
| Nexus | `Engine` records generated `MailLedgerEvent::Sent` and `MailLedgerEvent::Processed`. | Mail ledger is in-memory; no durable mail queue or async response manager yet. |
| SEMA | `Store::apply(SemaCommand)` is the only writer and replies with `DatabaseMarker`. | Store is in-memory, `StateDigest` is a deterministic placeholder, not content-addressed state. |
| Runtime Spirit | CLI/daemon process-boundary test passes with rkyv over socket and NOTA at CLI. | The prototype is not production Spirit 0.3 and does not migrate the live database. |
| Upgrade path | Generated `UpgradeFrom`/`AcceptPrevious` traits exist in emitter output. | No schema-diff-derived upgrade path is exercised by this Spirit slice yet. |

## Strongest next implementation targets

1. Make `RecordSet` a real vector by extending schema lowering/emission with an
   authored vector type instead of a single-entry newtype.
2. Move `MessageSent`, `NexusMail`, `MessageProcessed`, and the mail hook traits
   from emitter support code into a shared schema-authored core surface.
3. Replace in-memory `Store` and `mail_ledger` with redb-backed SEMA and durable
   mail state while keeping the generated `DatabaseMarker` shape.
4. Add a schema-diff witness that changes one generated Spirit type and proves
   `UpgradeFrom`/`AcceptPrevious` is required and used by a Nix test.
5. Split the current single `schema/lib.schema` into first-class Signal, Nexus,
   and SEMA schema planes once the file/module convention lands.

## Operator Judgment

This is a better prototype than the previous pass because Nexus and SEMA no
longer merely borrow generated Signal nouns: they now move generated mail and
state-marker nouns through the runtime. It is still not the complete system.
The next pass should treat every audit row above as a constraint: if a designed
component is mentioned, the test should force it to be used in runtime code, not
only declared in a report or fixture.
