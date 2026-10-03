# Memorable sketch

Provenance: Mind Astra dea0ba, messenger, 2026-10-02. Delivered to main flow 3ec648 (session 3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3, transcript line 1989). Copied verbatim below.

```text
Mind Astra dea0ba — light Memorable sketch. Design proposal, not existing generator support or implementation authorization. Ruling 9's Signal / Operation / Memory division is the right boundary here.

1. Memorable is a capability of a stored record type: apply its typed change, or refuse it without changing memory. The result has three distinguishable branches: Changed carries the durable commit receipt; Refused carries that record's typed reason; Failed carries a structured storage failure. A domain refusal is not a string in the engine error enum. A timeout with uncertain commit must remain distinguishable from a confirmed no-change failure; a stable change ID lets Operation resolve the receipt instead of replaying blindly. Signal carries the request/outcome; Operation orders and commits; Memory declares the record, permitted changes and conversions. Pure validation/conversion returning a value is not yet a durable Changed result.

Compact proposed notation, intentionally schematic (not accepted ethos-zero grammar):

Note implements Memorable {
  change Rename { title String }
    -> Changed { receipt CommitReceipt }
     | Refused { EmptyTitle | RevisionConflict { expected U64 actual U64 } }
     | Failed StorageFailure

  upgrade_from prior.Note
    -> Ready Self
     | Refused { InvalidLegacyTitle { note_id Uuid } }
}

The small operation-specific payloads stay inline; reusable Receipt/StorageFailure types are imported. Record revision numbers here are concurrency tokens, not format versions.

2. Versions live in the manifest, as vision-ethos specifies. Each new version names the exact predecessor record definition and its upgrade_from implementation; the example's prior.Note import is pinned there. The predecessor is immutable and remains available to decode old data. The generated descriptor maps that declared version edge to the actual old/current schema hashes used by sema-engine. A hash identifies physical layout; it does not substitute for the authored version and conversion. Missing edges, ambiguous routes or incompatible keys stop admission. Downgrades and arbitrary historical jumps are not inferred.

3. The ethos edit is the migration declaration. An explicit rename or an added field with an explicit default can generate its transformation. A split, lossy conversion or changed meaning needs a typed conversion body attached to that edit. The generator emits old/new record definitions, typed conversion, descriptor registration and tests from the same edit; it must report an unresolved conversion rather than invent meaning from a textual diff. Concrete example: v1 Note.text becomes v2 Note.title plus Note.body. The edit must state the split rule and the empty/invalid-input outcome. Only then can it generate upgrade_from. This makes the edit executable without pretending arbitrary semantics can be derived automatically.

Boundary over today's engine: the report describes with_prior(SchemaHash, Fn(Prior)->Current), so it can host the declared hash edge but not the proposed fallible typed upgrade as-is. Replace/extend that conversion contract deliberately and update consumers; do not flatten a refusal into a panic or string. A conversion may produce a candidate, but new-format bytes and their version marker must commit together, or old bytes/marker stay valid. Eager migration versus lazy per-record conversion needs an explicit engine guarantee; the atomic open stamp alone proves neither. Its current proof covers declared with_family catalog/layout/policy rows, not later register_table calls or arbitrary data rewrites. Identified families also lack the reported predecessor hook.

Smallest implementation target: one ordinary family, two manifest versions, one typed domain refusal and one explicitly authored fallible conversion. Witness successful change, refused change with unchanged bytes, conversion failure with old bytes/format still readable, and interrupted commit/reopen without mixed format markers. That yields the first working Memorable slice; broader migration scheduling can follow evidence. No claim that current ethos-zero supports a Memory root: the bounded read found Library/Signal/Sema today.

Grounding: flows/3ec648/reports/sema-engine-reads-and-stamp.md:26,54–55; flows/91ea9f/vision/ethos.md:44; current vision-ethos and knowledge-ethos. My subflow read those sources; I did not run sema-engine or test this proposed syntax.
```

## Sources

- /home/li/.claude/projects/-home-li-primary/3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3.jsonl:1989
