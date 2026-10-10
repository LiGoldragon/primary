# New-flow setup audit — 2026-10-09

## Current runtime and launcher source

`tools/native-voice-launch.mjs` selects a voice profile and invokes the
Claude or Codex main launcher.  The Claude launcher uses `flow-id`, writes a
continuation record, creates a Herdr pane, starts the native Claude harness,
checks transcript/model/effort/title, reports the Herdr agent session, and
calls `hm-register`.  This is the visible setup route.

The published topic change supplies root `--topic`, default `Core`, durable
continuation topic storage, inherited continuation topics, and topic-aware
canonical titles.  Its Field receipt records five immutable assembled suites
and a remote content match at
`/home/li/private-repos/flow-evidence/42265e/topic-eight-file-publication/receipt.json`.

445410 attributes live Ethos launches to this route: root input used
`--aspect Psyche --layer Primary|Secondary --topic Ethos --root --metaflow`
and `--brief`, after `--check`; it reports native/Herdr/transcript and
messenger bindings for the observed seats.  It does not attribute an
independent continuation read, colour/session-list read, or Flow Nexus call.
This audit has not performed a live probe.

## Nexus evidence and the boundary

`/run/user/1001/flow/flow.sock` and `flow-meta.sock` currently exist.  The
launcher source inspected above does not connect to either socket; it calls
the direct Herdr/harness/messenger route.  Thus current launch setup is not
evidenced as a Flow Nexus `Launch` operation.  Socket existence and lack of a
visible launcher call do not prove that no other component uses Flow Nexus.

The current vision source is `flows/f5a6e9/books/13-the-flow-nexus-vision.md`:
it proposes `Launch`, `Wake`, `Refresh`, `End`, and `Current` over a
metaflow record.  It is a vision/proposal source, not runtime deployment
evidence.  Word identifiers and their dictionary remain proposed anatomy;
no codec or word-title integration is implemented.

## Implementation and deployment state

Astra reports no active native implementation or build.  The private
Clojure Flow has eleven tests and twenty-one assertions but is offline and
not a Nexus.  The Rust format bridge has five historical tests and is not a
general compiler or production CLI.  The Curriculum Ethos book checks do
not establish a cross-compiled deployment.  Field's remote-Nix work is
historical maintenance evidence, not product authorization or deployment.

The prior disposable continuation exercise demonstrates native-script
continuation records and supported closure; its receipt explicitly says it
does not demonstrate Flow Nexus Start/Replace or deployed Flow Memory.

## Owned next handoffs

1. Astra chooses one bounded first Flow Nexus or CLI increment from the
   current vision, assigns one implementation owner, and keeps the existing
   Clojure/Rust candidates distinct from a production claim.
2. Field receives only that immutable, published increment for Prometheus
   Nix checks and any deployment handoff.  No local compiler fallback,
   parallel Field Clojure writer, or old-flow rebootstrap follows from this
   audit.
3. 445410 compares this independent audit with its own runtime report and
   owns any presentation of the paired findings.

## 2026-10-09 attributed title correction

Via 445410, the living rules the canonical title as
`{ <Aspect> <Topic> <Layer> <flow id> }` in every case.  `Core` is always
included, including a topicless launch; braces remain and there is no `::`
form.  The earlier attributed Psyche:: title blocker is superseded by this
correction.  Word-ID work remains a separate proposed tool and is not a
Core-title blocker.

Astra's existing launch-evidence work owns the shared-title and fixture
correction; the Flow Current durable-identity worker owns separate paths.
No identity, profile, or seat has changed here.  Source qualification and
lock acquisition remain pending; any heavy test must use an immutable pushed
revision through Prometheus Nix and Field.  Field's Action Required state
currently blocks its publication/check handoff, not source-design approval.
The prior eight-file topic publication remains complete; no Core-title fix,
runtime change, or new publication is claimed.

445410 reports that its paired-book v2 at the existing URL now bounds claims
to inspected source and a source-only audit.  This record does not
independently reverify that artifact; its figure is still being bounded.

## 2026-10-09 later attributed topic-name correction

The later living correction, relayed verbatim by 445410, makes topic names
lower-camel rather than PascalCase: `core`, `ethos`, and `flow` are values of
`core:Name`, whose type is `camelCaseExpression` and is checked when a new
name is created.  The braced title shape remains; the stated example is
`{ Psyche core Secondary id }`.  This supersedes the earlier PascalCase
assumption for upcoming topic/title validation.

No persisted name is converted here and no complete grammar is inferred.
The authored `core:Name` contract and compatibility implications require
qualification by Astra's existing title worker.  No launcher fix, identity,
profile, seat, or runtime change is claimed.
