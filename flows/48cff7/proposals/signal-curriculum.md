# proposal · signal-curriculum

*Flow 48cff7 · 2026-09-16 · pending living review*
*Kind: new Ethos wire type repo draft; carries the wire for the `curriculum-nexus` (proposed).*
*Source records: flows/48cff7/vision/visionAsSkillSource.md, skillKindsTaxonomy.md, skillPromotionAndLayering.md, mind.md, transcriptNexus.md*

---

This is a first draft of the Ethos-flavoured signal vocabulary for the `curriculum-nexus` that reads vision subjects and generates the deterministic-named skill files. The purpose: the same vocabulary the living named for vision anatomy becomes the closed enum positional shape of a typed record on the wire.

Codex is expected to (a) fit this to the current `nexus` and `datom` skills' conventions, (b) surface any question this flow could not answer to the living rather than fabricate, (c) return the finalised Ethos repos as commits on a proposal branch.

## Sketch

Records:

```
VisionSubject := { subject: Symbol
                   core: String
                   rationale: String
                   extended: String
                   experimental: String
                   undecided_proposal: String
                   raw_records: Vector<RawRecord>
                   open_questions: Vector<String>
                   custom_sections: Vector<CustomSection> }

RawRecord := { date: Date  quote: String  provenance: Provenance }

Provenance := Typed | Stt | Relay.{ via: Symbol }

CustomSection := { name: Symbol  content: String }

Kind := Core | Rationale | Extended | Experimental | UndecidedProposal | RawRecords | OpenQuestions | Custom.{ name: Symbol }

Segment := Unchanged.{ text: String }
        | Added.{ text: String  since: Ref }
        | Removed.{ text: String  since: Ref }
        | Changed.{ before: String  after: String  since: Ref }

Ref := Commit.{ sha: String } | Version.{ major: Integer  minor: Integer  patch: Integer } | Latest
```

Ordinary-socket operations (paired requests → typed replies):

```
Get.{ subject: Symbol  kind: Kind }                          → Got.{ content: String  version: Ref } | NotFound.{ subject: Symbol  kind: Kind }

Put.{ subject: Symbol  kind: Kind  content: String  witness: Ref }
                                                             → Written.{ subject  kind  version } | Rejected.{ reason: RejectReason }

List.{ subject: Symbol }                                     → Listed.{ subject  kinds: Vector<Kind> } | NotFound.{ subject  kind: Core }

Highlighted.{ subject: Symbol  since: Ref }                  → HighlightedView.{ subject  segments: Vector<Segment> } | NotFound.{ subject  kind: Core }

Generate.{ subject: Symbol }                                 → Generated.{ subject  files: Vector<GeneratedFile> } | Rejected.{ reason }

GeneratedFile := { path: String  kind: Kind  sha: String }

RejectReason := MissingCore | InvalidSection.{ name: Symbol } | ConflictingWitness.{ current: Ref } | UnknownSubject
```

Meta-socket operations (privileged):

```
SetGenerationPolicy.{ suggested_kinds: Vector<Kind>  strict: Bool }   → PolicySet.{ }
RegisterCustomKind.{ name: Symbol  description: String }             → Registered.{ name } | Rejected.{ reason }
Repoint.{ subject: Symbol  new_source: SourceRef }                    → Repointed.{ subject } | Rejected.{ reason }
```

## What Codex should read first

1. The `nexus` skill (loaded here, applies verbatim).
2. The `datom` skill for the textual CLI form.
3. `flows/48cff7/vision/transcriptNexus.md` — for the sibling shape (a Nexus this one talks to for `Highlighted` diff work when the source is elsewhere).
4. `flows/48cff7/vision/visionAsSkillSource.md` — the anatomy this signal encodes.
5. `flows/48cff7/vision/skillKindsTaxonomy.md` — the taxonomy the generator produces.
6. `flows/48cff7/vision/mind.md` — a possible peer or fused component; if fused, this repo's wire covers both.

## Questions Codex should surface, not answer

1. Whether `mind` and `curriculum` are two Nexuses or one — the signal repos merge or stay separate accordingly.
2. Whether the `custom_sections` variant stays open in the wire vocabulary (a `Custom.{ name }` `Kind`), or the vocabulary is fully closed and custom sections live only in the source file.
3. Whether `Generate` is idempotent (the same subject at the same version always produces the same files), or version-tagged.
4. Whether `Ref` needs a `Branch.{ name }` variant, or `Commit` + `Latest` suffice.
5. What section boundaries look like in a source Markdown file — H2 heading names matching `Kind` variants, HTML-comment markers, or a datom preamble at the top of the file.

## Deliverable

Codex should return two authored Ethos repos on a proposal branch:

- `signal-curriculum/` — the ordinary-socket wire types plus their round-trip test examples.
- `meta-signal-curriculum/` — the privileged-socket wire types plus their examples.

Plus a short report on the answers to Questions 1–5 above, or a list of the ones surfaced to the living.
