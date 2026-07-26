PROGRESS AUDIT VERDICT + COURSE CORRECTION

Audit of all work since the slice prompts landed. Verdict first, then
ordered directives. Nothing here reopens a ruling; it enforces the
standing ones.

VERDICT

Clean: no prohibition-class violations. The disjointness prover is
untouched and conservative; boundary-first parsing preserved; all
eight frozen surfaces (spirit worktree, Meta/Judge candidates,
published new-schema-port branches, signal-frame, structural-codec-
derive, spirit main) untouched; design log append-only byte-for-byte;
the typed-rules psyche quote recorded character-exact; authorized
tier-1 fixes landed correctly (FoundClose, MissingLexicon,
CharacterSet canonicalization with proper fresh locks, FreshnessCheck,
build-API newtypes); the R3 viability spike is real and its five
tests pass.

Not clean, in severity order:

1. THE BUMP TRAIN SHIPPED HALF-BUILT. The leaf bump (raw-discovery
   layout 3, ShortCode kinds) is pushed, but R3 kernel typed
   positions and the R4 type-id retype exist only in unpushed
   disposable spikes; three of four identity-shape fixes (domain-tag
   laundering at the table boundary, legacy delimiter still in the
   hashed pre-image, zero-filled layout placeholder) did not ride;
   structural-codec and protos still pin all four baselines, so
   nothing downstream consumes the train; the ruled re-locks are
   pending; and protos will not compile once repinned, because the
   ShortCode redesign turned a struct into a sealed trait with the
   same name.
2. SLICE 0 IS INCOMPLETE: core-nomos was never repinned — still on
   the dead monorepo revision, still Core*-named, every string
   operation intact.
3. THE WITNESS PIPELINE RUNS ON THE FORBIDDEN EMITTER. The
   language-engine-witness e2e (schema-engine -> nomos-engine ->
   logos-engine, scratch crate, real cargo compile, behavior
   round-trips, byte-golden deliberately retired) has exactly the
   right oracle shape — and its emission leg is textual-rust's
   quote!/prettyplease writer, which standing law 1 bans from the
   pipeline. No capsule exists anywhere on that path, and the engines
   do not even depend on protos, yet the design log's appended text
   claims schema and logos capsules are "the first production Capsule
   implementors." The log states law ahead of reality — the exact
   drift pattern this project is trying to kill.
4. UNDISCLOSED BEHAVIOR CHANGES INSIDE PLUMBING COMMITS: the
   completion probe now rewinds trivia and an Application payload
   mismatch falls through to the next alternative — both inside a
   commit titled as a narrow preflight change; core-schema's repin
   silently deleted the downstream conformance-law-5 test and added a
   duplicated reflection family whose trait-facing path fails where
   the direct path succeeds, plus a fresh copy of string-keyed
   builtin resolution.
5. DESIGN-LOG FIDELITY: the capsule-ruling entry paraphrases the
   question in the wrong person ("did he rule" vs the actual "did you
   actually rule 'the complete composition'?") — that entry exists to
   replace a fabrication, so the question's exact wording is load-
   bearing; the appended section names no provenance; date labels
   were dropped; R5 (a confirmation) is enrolled as a numbered ruling.
6. SPIKES AT RISK: both spike commits are unpushed jj-only heads — a
   GC loses them — and the superseded spike carried coverage the
   survivor dropped (rule-order independence, refusal-without-
   fallback).

DIRECTIVES, IN ORDER

1. PRESERVE THE SPIKES NOW. Push both spike commits to a clearly
   named spike branch before anything else. Restore the dropped
   coverage (order-independence, unknown-and-ambiguous-refuse tests)
   into the surviving spike.

2. FINISH THE ONE BUMP TRAIN before any new work lands on top, as a
   single coordinated landing:
   a. R3 kernel typed positions in structural-codec PROPER, absorbed
      into the SHARED evaluator. The spike is a parallel engine and
      must not be promoted as-is — the ruled clause is "the shared
      evaluator runs this vocabulary; not a parallel engine," and
      that clause is currently unwitnessed. Also: the spike's
      protos-primitive prover stub (spelling string equality) must
      never replace disjoint.rs.
   b. R4 type-id retype: ScopedEncodedTypeId / EncodedConstructorId
      as namespace-variant-wrapped u16 per the name-table Identifier
      pattern, private fields.
   c. The three remaining identity fixes: domain-tagged
      RawProfileIdentity/EncodedLayoutIdentity (no [u8;32] pub
      laundering), legacy delimiter OUT of the hashed pre-image, no
      zero-filled layout-identity placeholder.
   d. Repin structural-codec onto the train, then protos; adapt
      protos' ShortIdentifier to the kind-typed short codes. The
      type-per-kind + sealed-trait shape is ACCEPTED as matter (the
      ruled substance was the kind dimension) — but the silent
      downstream break it caused is exactly why every train names
      its consumers before it ships.
   e. Re-lock every absolute digest once, at the end: table layout
      locks with the real profile, and give the composed-nametree
      identity its ruled REAL-witness lock a home — it belongs with
      the first production Capsule implementor (slice 1), deriving
      from real name-table slices, replacing the hand-mirrored
      fixture reproduction in content-identity's test.
   f. Fix, in the same train: the new fabricated-observation error
      (lexicon resolve failure reported as NotMatched instead of its
      cause — the fixed line's twin, one screen away).

3. FINISH SLICE 0: repin core-nomos onto the micro-repos, carry the
   Core-to-Encoded rename. Unify core-schema's duplicated reflection
   family into one path with one behavior (no silent divergence
   between encode and the Textual trait); the fresh string-keyed
   builtin copy dies when slice 1's builtins-as-priors lands — do
   not grow it further.

4. SLICE 1, per the standing prompt, with one integration decision
   made for you: the witness's oracle pattern (scratch crate, real
   cargo compile, behavior round-trips, no byte-golden) is CORRECT —
   keep it. But the slice-1 acceptance gate lives in protos-engine
   per the ruling (assembly + cross-repository tests), and the
   emission leg must be the typed rule vocabulary in rust-logos
   (rename textual-rust in place), not the quote!/prettyplease
   writer. The engines gain the capsule layer as ruled: schema and
   logos capsules as the first production Capsule implementors with
   real-slice composed identities, the revived rename test (rename
   moves nametree identity, not content identity), and the fixed
   Textual-to-logos-capsule association. Until that lands, treat the
   design log's "first production Capsule implementors" line as an
   obligation, and discharge it — the log must not stay ahead of the
   code.

5. DESIGN-LOG CORRECTIONS, BY APPEND ONLY: append a correction entry
   restoring the capsule question verbatim ("did you actually rule
   'the complete composition'?"); state the appended section's
   provenance (live session rulings, not the transcript files the
   header names); restore date labels on new entries; note R5 is a
   confirmation of the original design, outside the ruling series.

6. SURFACE, DO NOT BURY: conformance law 5's downstream test is
   homeless because the derive repo is dead — carry it as an open
   item in your slice reports until it is rehomed or retired by
   ruling. The two undisclosed behavior changes get named in the
   design log's engineering notes or the next commit body.

7. STANDING DISCIPLINE, restated because each was breached once
   today: every behavior change is named in its commit message;
   plumbing commits carry zero behavior; commit messages have bodies
   when they touch more than pins; doc comments and tests describe
   what code does, never that a ruling is satisfied; mechanically-
   checked repository laws are widened in their own commit with the
   authorizing reason cited, never in the same breath as the
   violation they legalize.
