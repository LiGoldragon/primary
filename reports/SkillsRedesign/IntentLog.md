# intent-log redesign

Draft only. Nothing in `LiGoldragon/skills` was edited. This report is the whole
deliverable.

Source under redesign: `/git/github.com/LiGoldragon/skills/skills/intent-log.md`.
Generated copies: `/home/li/primary/.claude/skills/intent-log/SKILL.md` and
`/home/li/primary/.agents/skills/intent-log/SKILL.md`.

Revision 2, after the psyche's rulings: `he` becomes `psyche` throughout, the
`Record every candidate` line is cut, and gate 2 is reworked. Verbatim psyche
quotes keep their original wording; everything written by me uses `psyche`.

## Answer to the question he asked

He asked "what are we talking about here?" about my claim that the `Not intent`
section may violate a standing rule banning negative examples in skills.

**The full `Not intent` section, as it stands in the revised draft:**

```markdown
## Not intent

The psyche's rejection of a draft, a plan, or a file.
A statement made in frustration, until the psyche states it again on a separate occasion.
A statement naming a technology, format, component, or repository. Ask the psyche to state the principle behind it; do not extract one yourself.
```

**The citations, and where I overstated them.**

The rule is real and it is verbatim. Both quotes are his, at
`/home/li/primary/reports/logos/psyche-vision-handover-2026-07-19.md:52-54`:

> "negative examples are forbidden in skills"

> "also, negative examples are forbidden in skills. make sure that is clear to
> skill-editor role also"

**My claim that he said it "twice, on separate occasions" is wrong, and I inferred
it.** The evidence says one occasion. Line 51 of that file introduces both quotes
as "settled, verbatim (2026-07-19)" — a single date. The file's own index of every
quote from that day lists both as one item, number 5, at `:568`. The second quote
opens with "also," which reads as a restatement minutes later in the same
conversation, not a return to the subject on another day.

Two further corrections to what I represented:

- The third place I cited, `:30`, is not his words. It is a bolded agent summary
  line in the handover's §0 conduct list, tagged "(his words, settled — see §1 and
  §4)" but not itself a quote. I labelled it a restatement, which was accurate, but
  it added nothing to the count.
- Line `:57-58` contains a fourth fragment, "also wrong is giving wrong examples",
  attributed to a "pre-existing wrong-examples doctrine" with no file, date, or
  citation. I could not source it anywhere. Treat it as unsourced.

**What the rule does not settle.** The sentence that would decide whether my
section is compliant is at `:55-57`: "A wrong or illegal form is described in
prose, never exemplified — not even as a labeled counter-example or placeholder."
That sentence is the handover author's derivation, not his words. If it holds, my
section is fine, because it names categories in prose and shows no example text.
If it does not hold, the question is open. I cannot close it from evidence.

So the honest position: the ban is his, said once in one session and repeated
within it, scoped to skills. Whether prose-only category naming counts as a
negative example is an agent's reading. This is the same error I wrote a rule
against — treating repetition across occasions as evidence of an unbending
position, then not applying that standard to my own citation.

## Current text, verbatim

```markdown
# Skill — intent log

- Record only explicit psyche values, aims, or beliefs that guide many decisions.
- Route mechanisms, defaults, tasks, and architecture to their owning surface.
- Check for an existing record before creating one.
```

The generated copies carry the frontmatter `description: 'Intent log rules.'`.

## Proposed replacement, verbatim

```markdown
# Skill — intent log

## Test

Record only when all three hold.

1. It is an aim, a value, or a belief. Ask what the statement tells you to do; if the answer is a procedure, a default, a name, a component's shape, or a boundary, it is matter.
2. The psyche chose it over an easier path. Name that path. If you cannot name one, it is matter.
3. It settles a decision outside the work in front of you. Name that decision. If it settles only the case at hand, it is matter.

Most sessions record nothing.
A borderline candidate is matter.
Do not soften a candidate that fails the test into a weaker record.
Do not read "never", "always", or "must" as a sign of intent. The psyche states matter that way.

## Not intent

The psyche's rejection of a draft, a plan, or a file.
A statement made in frustration, until the psyche states it again on a separate occasion.
A statement naming a technology, format, component, or repository. Ask the psyche to state the principle behind it; do not extract one yourself.

## Routing

Write every psyche ruling in the current train to the design log.
Record to Spirit only the part of a ruling that still binds after the train ends.

## Recording

Search Spirit for the domain and the referents before writing.
Change the existing record instead of adding one beside it.
Testimony is the psyche's exact words plus the question they answered. Never paraphrase it.
Keep the psyche's hedges. "I think" and "maybe" stay at their original strength in the description.
If the only wording is yours and the psyche agreed to it, ask the psyche to state it before recording.
Take the wire shape from the signal-spirit schema. Do not copy it from a skill, a README, or an earlier session.
When Spirit is unreachable, stop and hand the candidate and its testimony back to the psyche. There is no fallback store.
```

## Proposed description field

```
Use when deciding whether something the psyche said belongs in the Spirit store.
```

## Changes in revision 2

**`he` becomes `psyche`.** Eight lines changed. Three needed rewriting rather than
substitution, because the direct swap read badly:

- `A statement he made in frustration, until he states it again on a separate
  occasion.` became `A statement made in frustration, until the psyche states it
  again on a separate occasion.` The first pronoun is dropped rather than
  substituted; two `the psyche` in one line was clumsy.
- `If the only wording is yours and he agreed to it, ask him to state it himself
  before recording.` became `If the only wording is yours and the psyche agreed to
  it, ask the psyche to state it before recording.` `himself` became redundant once
  the pronoun was gone.
- Gate 2 was rewritten wholesale, below.

**`Record every candidate that passes all three. Do not stop using Spirit because
earlier agents over-captured.` is cut, with no replacement.** His verdict was "just
useless noise." I had already flagged its second half as resting on an agent-written
record description rather than his words, and its first half restates `Record only
when all three hold.` from four lines above. The archived record about agents
avoiding Spirit entirely is not gone from the evidence base; it is simply not
strong enough to buy a line.

## Gate 2, reworked

His words: "I dont understand #2." The old wording was:

> 2. He has held it at a cost to himself. Name the occasion and what it cost him.
>    If you cannot name one, it is matter.

The defect is real and it is mine. The gate asked the agent to know what a
statement cost the psyche internally. An agent cannot observe that. It can only
observe what happened in the conversation.

The replacement proposed to me was:

> 2. The psyche chose it over an easier path he could have taken. Name the path he
>    refused. If you cannot name one, it is matter.

I adopt the substance and tighten the wording:

> 2. The psyche chose it over an easier path. Name that path. If you cannot name
>    one, it is matter.

Three reasons for the change from the proposed wording. The pronouns had to go
under ruling 1, and `an easier path that was open to the psyche. Name the path the
psyche refused.` repeats the subject twice in one line. `could have taken` and
`refused` say the same thing twice. `Name that path.` matches gate 3's `Name that
decision.`, so the two gates that require a named answer now read the same way.

Why this is the right operationalisation of "against his own convenience": the
convenience is the easier path. A refused alternative is visible in the transcript,
usually as the agent proposal he is answering or as the arrangement already in
place. That makes the gate answerable, which the old one was not.

### Worked examples re-run against the new gate 2

**No example's overall verdict flips.** Neither the live record `n9fl` nor the
positional-fields example moves. Details, since the gate-level verdicts do shift:

Qualifying side, all five still pass, and two get sharper:

- Example 1, replaceable design — the refused path is inside the utterance: an
  agent proposing "to try to keep an older part of the system working". Sharper
  than before.
- Example 2, `n9fl` — the refused path is inside the utterance: "instead of
  composing with skills that agents load. On the fly." That is the arrangement
  already in place and the cheaper one. Passes cleanly. Does not flip.
- Example 3, `346n` (quality) — **now the weakest of the five.** The refused path
  is accepting the bad result and moving on, which is implied by "the work has to be
  redone" but not stated. Under the old wording the cost was stated outright
  ("efficiency just goes right down the drain"), so this example lost support in the
  change. It still passes, but it is the one an agent could reasonably get wrong.
- Example 4, incorrectness — the refused path is keeping `worktrees.nota`, a working
  feature. Unchanged.
- Example 5, the bypass — the refused path is the bypass, named in the first three
  words. Much sharper than before; this was previously my least confident
  qualifying example, and the new gate 2 fixes it.

Matter side, all sixteen still fail, but four now pass gate 2 where they failed or
were unclear before:

- Matter 1, positional fields — the refused path is his own earlier "ALMOST NEVER
  ALLOWED" compromise, which he hardened to a total ban. Gate 2 now passes. The
  example is still matter, excluded by gate 1 as a syntax rule. I never rested this
  example on gate 2, so its verdict is unchanged.
- Matter 3, daemons keeping state in their own database — the refused path is
  writing state to files outside, which is easier. Gate 2 now passes. Still matter,
  excluded by gate 1 as a rule.
- Matter 4, poetic documentation — the refused path is accepting the draft in front
  of him. Gate 2 now passes. Still matter, excluded by gate 1 as a rule for writing.
- Matter 13 through 15, the three one-line rejections — gate 2 becomes ambiguous,
  since refusing a line is a refusal but not an easier path for him. Still matter,
  excluded by gate 3.
- Matter 12, "push through and not be intimidated" — still fails gate 2, and more
  clearly than before: pushing through is the easier path, so it is the thing he
  chose, not the thing he refused.
- Matter 16, cluster authorization — passed gate 2 under both wordings, since it
  overturned landed, audited code. Still matter, excluded by gates 1 and 3.

**Consequence he should know about.** The new gate 2 is answerable but less
exclusionary. Four matter examples that it previously helped reject now pass it, so
gates 1 and 3 carry more of the filtering load than they did. The test still gives
the right answer on every example I have, but its margin is thinner. If the corpus
starts admitting matter again, gate 2 is where I would look first.

## The qualification test, stated

Three questions. All three must be answered before recording. Two require the agent
to name a concrete thing, so a candidate cannot pass on impression.

1. **Is it an aim, a value, or a belief?** Ask what the statement tells you to do.
   If the answer is a procedure, a default, a name, a component's shape, or a
   boundary, it is matter.
2. **Did the psyche choose it over an easier path?** Name that path. If you cannot
   name one, it is matter.
3. **Does it settle a decision outside the work in front of you?** Name that
   decision. If it settles only the case at hand, it is matter.

Gate 2 is the operational form of "against his own convenience". The convenience is
the easier path, and a refused path is visible in the transcript where an internal
cost is not.

Gate 3 is the operational form of "bends a whole class". Requiring a named second
decision, outside the current work, excludes anything that settles the argument in
front of the agent.

Gate 1 stays because AGENTS.md names it first and because gates 2 and 3 alone admit
rules. Six of the sixteen matter examples below are excluded by gate 1 alone.

The bias toward exclusion is the psyche's own ruling, not my inference. Asked how to
treat borderline records during the legacy disposition, his whole answer was one
word:

> Borderline policy: "aggressive"

`/home/li/primary/reports/legacy-disposition/HANDOVER-2026-06-26-fresh-session.md:30`

That is carried by `A borderline candidate is matter.` The base rate is carried by
`Most sessions record nothing.` The downgrade escape is closed by `Do not soften a
candidate that fails the test into a weaker record.`

## The psyche's own words on over-capture

These are the highest-value quotes in the workspace and they are why the skill is
shaped as a filter.

> "8. no, that would be too implementation specific to record to spirit… train
> agents better (principle over substance of spirit)"

`/home/li/primary/reports/logos/vision-evidence-ledger-v1.md:121`. He rejects a
capture and names the remedy as training, not recording.

> "this stuff doesnt belong in spirit. it *describes spirit* to the user. you dont
> store the manual in the database. all this kind of stuff out of spirit, into the
> docs"

`/home/li/primary/reports/legacy-disposition/HANDOVER-2026-06-26-fresh-session.md:27-29`,
where the file labels it "The pivot".

> "Spirit is intent, not architecture facts"

Same file, `:26`.

> Routing calls: #1 cloudflare "this kind of stuff belongs in architecture files,
> not spirit" · #2 immich "again, not spirit content" · #3 d3r2 "not spirit
> material" · #4 asschema "yes, remove asschema entries"

Same file, `:23-25`. Four consecutive rejections in one sitting.

> "so we need more skill reinforcement in terms of the language we use to discuss
> those things. dont panic-send an agent, just make a note of it for later"

`/home/li/primary/reports/logos/psyche-vision-handover-2026-07-19.md:510-511`. He
refuses to have an irritation escalated into work. This is the closest verbatim
support for the frustration line.

> "my agents are neurotic, and theyre trying to deal with my frustration by
> constantly undoing what they just did, because theyre scared everything they did
> was wrong"

`/home/li/primary/reports/OrchestrateContinuation/ContextHandover.md:74-76`.

I found no quote in which he uses the word "over-capture" or complains that a named
record was wrongly admitted. That complaint exists only in agent prose and in
Spirit's own record descriptions.

## Worked examples — qualifies

**1. "I don't design additively, I design replaceably."**
`/home/li/primary/agent-outputs/ReplaceableDesignIntent/IntentMaintainer-ReplaceableDesignRecord.md:9-14`,
in the fuller utterance: "...it looks to me like an agent that's proposing something
in order to try to keep an older part of the system working. And I don't want that
because then it creates all of this legacy system. And if the current system is not
designed to do things the way we want, then it has to go."
Gate 1: a belief about how design proceeds. Gate 2: the refused path is named in the
utterance — keeping the older part of the system working. Gate 3: it decides every
proposal that offers a compatibility shim, across components.

**2. "my in my vision, my end, my end goal is agents are specifically trained. For
like one task, and they do it really well, and then we compose with agents instead
of composing with skills that agents load. On the fly."**
`/home/li/primary/agent-outputs/AgentSkillCompositionIntent/IntentMaintainer-RetryCapture.md:53`.
Gate 1: an aim. Gate 2: the refused path is named in the utterance — composing with
skills that agents load on the fly, which is the arrangement already in place and
the cheaper one. Gate 3: it decides the whole role and skill architecture.
This is the live record `n9fl`. It survived the 631-record purge as one of only two
records left untouched by that operation
(`SpiritLegacyMatterRemoval/IntentMaintainer-RemovalEvidence.md:17`). It is also the
only capture in the corpus the psyche authorized in his own words: "Actually, some
of this probably should go in spirit as durable intent, because maximizing early
context for best quality output is actually valid intent."
(`AgentSkillCompositionIntent/IntentMaintainer-RetryCapture.md:57`). If any single
example is the calibration point, it is this one.

**3. "The quality of the work is extremely important. And when quality is bad, then
the work has to be redone. And efficiency just goes right down the drain."**
`/home/li/primary/agent-outputs/AgentSkillCompositionIntent/IntentMaintainer-RetryCapture.md:73`,
recorded as `346n`, also left untouched by the purge. Gate 1: a value. Gate 2: the
refused path is accepting the bad result and moving on — implied by "has to be
redone" but not stated, which makes this the weakest gate-2 answer of the five.
Gate 3: it decides depth and model selection across every task.

**4. "I really dont like incorrectness, it just creates sprawl and problems"**
`/home/li/primary/reports/OrchestrateContinuation/ContextHandover.md:63`.
Gate 1: a belief. Gate 2: the refused path is keeping `worktrees.nota`, a working
registry mirror he killed over it — "which is wrong; I can modify the filesystem
without modifying that file, so it's a lie. useless." (`:65-66`). Gate 3: it decided
`protocols/repos-manifest.nota`, a component he was not discussing
(`SkillsCorpusRedesign/context-handover.md:45-47`).

**5. "I dont care for this bypass; I find it of poor taste and deceitful when agents
do this. I want the real thing, as envisionned."**
`/home/li/primary/reports/logos/psyche-vision-handover-2026-07-19.md:40-41`.
Gate 1: a value. Gate 2: the refused path is the bypass, named in the first three
words. Gate 3: it decides every case where an agent can satisfy the letter of a
request cheaply.

Note on example 2: the utterances at `:53` and `:55` are one intent said twice, not
two records. That is what `Change the existing record instead of adding one beside
it.` is for.

## Worked examples — does not qualify

**1. "THERE ARE NO FIELDS NAMES! ALL FIELDS ARE POSITIONAL! FIELD NAMES ARE ALMOST
NEVER ALLOWED! WRITE IT SOMEWHERE YOU WONT FORGET! MAKE PROTOS SKILL CORRECT, AND
MAKE IT A PART OF MANAGER! I NEVER WANT TO SEE THIS AGAIN!"**
`/home/li/primary/reports/logos/psyche-vision-handover-2026-07-19.md:223-225`.
The most tempting utterance in the corpus: maximum emphasis, a demand that it be
made permanent, and an explicit "never again". It passes gate 2 — the refused path
is his own "almost never" compromise, later hardened to a total ban. Fails gate 1:
it is a syntax rule. He routes it himself in the same breath, to the protos skill
and the manager role. If a candidate this loud is matter, volume carries no
information.

**2. "negative examples are forbidden in skills" / "also, negative examples are
forbidden in skills. make sure that is clear to skill-editor role also"**
Same file, `:52-54`. Fails gate 1 — a rule for writing skills. Its home is
`skill-designing`.

**3. "Daemons keep their state in their own database. Do not write component state
to files outside it."**
`/home/li/primary/reports/OrchestrateContinuation/ContextHandover.md:113-114`.
Passes gate 3 — it binds every daemon — and now passes gate 2, since writing state
outside is the easier path. Fails gate 1: a rule. It landed at
`/git/github.com/LiGoldragon/standards/standard-component-architecture.md`.

**4. "This style really feels counterproductive in documentation, it's like agents
are trying to sound poetic, which is inappropriate and even harmful"**
Same file, `:87-89`. Passes gate 3 and now gate 2. Fails gate 1: a rule for writing.
Already lives in `skill-designing`. With matter 3, this is the pair that shows gates
2 and 3 together are not sufficient.

**5. "DO NOT make elaborate responses until you are completly done launching and/or
waiting for agents (also harden that in the management skill)."**
`/home/li/primary/reports/logos/vision-evidence-ledger-v1.md:109`. All caps and an
explicit request to harden it into doctrine. Fails gate 1: pure procedure. He names
the destination himself.

**6. "remove the doing, keep the knowing"**
`/home/li/primary/reports/OrchestrateContinuation/ContextHandover.md:103`. Fails
gate 1: a boundary for one component. The most quotable line in the corpus, which is
why it is the most likely to be captured.

**7. "orchestrate is a typed message board. it doesnt scan the filesystem or run
commands."**
Same file, `:98-99`. Fails gate 1: a component's shape. The handover author already
filed it under "Matter".

**8. "and it WILL have worktree registry"**
Same file, `:101`. Fails gates 1 and 3: one component's feature. The capitals are
emphasis.

**9. "we dont use the monorepo style; destroy the duplication by keeping the
micro-repo approach."**
`/home/li/primary/reports/logos/micro-repo-canonicity-ruling-v1.md:23-24`. Fails
gate 1: a repository layout rule.

**10. "Rust is our assembly language."**
`/home/li/primary/reports/logos/vision-evidence-ledger-v1.md:108`. Memorable and
broad. Fails gate 1: it names a technology and states its role. This is the case
`A statement naming a technology, format, component, or repository.` covers — ask
the psyche for the principle rather than recording the sentence.

**11. "I dont do ANYTHING. EVER"**
`/home/li/primary/reports/OrchestrateContinuation/ContextHandover.md:12`. Fails
gate 1: a fact about him.

**12. "tell your agents to push through and not be intimidated by the broken
orchestration machinery"**
Same file, `:54-55`. Fails gate 2: pushing through is the easier path, so it is what
he chose rather than what he refused.

**13. "this is stupid. do not try to swallow your tongue, and do not kill your
family."**
`/home/li/primary/reports/SkillsCorpusRedesign/context-handover.md:69-70`. Fails
gate 3: rejection of one line of one skill.

**14. "Might as well say 'audit rust'."**
Same file, `:71`. Fails gate 3: rejection of one line.

**15. "dont smash your head against the wall?"**
Same file, `:74-75`. Fails gate 3: rejection of one line.

**16. The hardest case. "The whole point of the authorization is to gate the
operation from being accepted, and by that I mean being accepted everywhere,
including locally. The quorum gates the acceptance everywhere. The criome authorizes
or does not authorize, and in which case it does not authorize, it's not
authorized."**
`/home/li/primary/agent-outputs/PersistentSpiritMirror/ClusterAuthorizationSliceDesign.md:14-18`.
It overturned landed, audited code, so gate 2 passes cleanly. It fails gates 1 and
3: it is one component's authorization design. This is the case where I would expect
an agent to get it wrong.

Examples 13 through 15 are the densest over-capture source in this workspace: his
most forceful language, all of it rejections of a single artifact. `The psyche's
rejection of a draft, a plan, or a file.` exists for them.

## Routing between intent-log, psyche-vision, and design-log

Only two of the three are destinations.

**`design-log`** is a write surface with a file target:
`design/<Train>/<SessionName>-<Date>.md`, append-only, recency wins
(`/git/github.com/LiGoldragon/skills/skills/design-log.md`).

**`intent-log`** is a write surface with a store target: the Spirit daemon.

**`psyche-vision`** is not a write surface. It is a recognition vocabulary, consumed
while deciding whether to follow a statement — `psyche-interraction` says "Align
with the psyche's vision" and `context-handover` says "Preserve every
non-repetitive, load-bearing psyche statement". It names no place to put anything.

The daily decision therefore has two answers, not three:

- Every psyche ruling in the current train goes to the design log, whether or not it
  is intent. Unconditional.
- The subset that passes the three gates also goes to Spirit.

Ordering it this way is the structural fix for over-capture. The motive behind a
marginal capture is that the words will otherwise be lost. Giving the ruling a cheap
unconditional home removes the motive. That is why the routing section is two lines
and why the design-log line comes first.

`context-handover` is a fourth surface but not a competing one. It carries words
forward into a new session and stores nothing.

**Finding on `psyche-vision`.** Its `## Test` — "Ask whether the statement would
still guide the work if every current mechanism were replaced" — is the same
discrimination as gates 1 and 3, stated a second time in a second skill. Its
`## Not vision` and `## Handling` sections restate AGENTS.md. I did not fold it in,
because that is a manifest change and it is his call. My recommendation is that
`intent-log` own the test and `psyche-vision` be deleted. Corpus handover open item 6
already flags it as unresolved.

**Conflict to note.** `design-log` says "Interpret conflicting entries by recency."
He has ruled against recency as an authority: "My vision has evolved, so recency
alone does not establish authority."
(`/home/li/primary/reports/logos/vision-evidence-ledger-v1.md:10-11`). Inside a
single train the design-log rule is probably fine. Across trains it is not. Not my
skill to change; flagging it.

## Should this skill carry the recording mechanism

**Recommendation: no syntax in the skill. Name the schema as the authority, and carry
the two behaviors that mechanics-in-prose keeps getting wrong.**

What I verified, read-only:

- There is no MCP tool for Spirit. The only path is the `spirit` CLI at
  `/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs`, one NOTA argument over a
  Unix socket from `SPIRIT_SOCKET` (default `/tmp/spirit.sock`).
- `/tmp/spirit.sock` does not exist. `spirit-daemon.service` is inactive since
  2026-07-24 23:33:18; it has `Requires=spirit-judge.service`, and
  `spirit-judge.service` is failed with start-limit-hit.
- Root cause of the judge failure is version skew, not configuration. The unit
  wrapper passes `--session-launcher`; the installed `spirit-judge-0.1.0` binary's own
  `serve --help` output omits that flag, and the argument parser's fallback arm
  returns the usage string and exits 1
  (`/git/github.com/LiGoldragon/spirit-judge/src/main.rs:126`). The checked-out source
  handles the flag. The deployed binary predates it.
- There is no queue, spool, or offline fallback anywhere in `spirit`, `signal-spirit`,
  or `spirit-judge`. A failed connect prints and exits 1.

The decisive evidence against putting syntax in the skill is that two
authoritative-looking copies of it already disagree, and the schema sides with the one
that was deleted:

- `/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema:149-153` gives
  `VerbatimQuote { QuoteText OptionalAntecedent }`, `Testimony (Vector VerbatimQuote)`,
  `Justification { Testimony Reasoning }`, `RecordRequest { Entry Justification }`.
- The pre-cut `intent-core` example wrote the justification as
  `([([verbatim psyche words] None)] [reasoning])`, which matches that schema.
- `/git/github.com/LiGoldragon/spirit/README.md:48` writes it as
  `([schema creates the interface] None)`, which does not — `Reasoning` is a `String`,
  not an `Optional`.

I cannot execute either shape to settle it, because the daemon is down. So the skill
must not assert one. `Take the wire shape from the signal-spirit schema.` points at the
thing generated from the wire and prevents the failure that already happened.

The counter-argument I weighed and rejected: corpus handover open item 7 records that
removing the literal `meta-orchestrate` command from `edit-coordination` left an agent
unable to register a lane, and that naming a capability without naming its
implementation caused a real failure. That is a genuine precedent for including syntax.
It does not apply here, because the Orchestrate command had one correct form verified
against the binary, and this one has two candidate forms and no way to verify either.
When the daemon is back and one shape is confirmed, the right home is the `spirit`
repository's own README, per `documentation-placement`.

The two behaviors the skill does carry are load-bearing now:

- `Take the wire shape from the signal-spirit schema. Do not copy it from a skill, a
  README, or an earlier session.`
- `When Spirit is unreachable, stop and hand the candidate and its testimony back to
  the psyche. There is no fallback store.`

The second is not a note about the outage. It is durable, since there is no fallback by
design, and it is the behavior an agent will not derive — the default move is to write
the record somewhere else so it is not lost, which is how matter ends up in reports and
guidance files.

**On the missing verbatim testimony.** The Spirit store persists only the
agent-clarified `Entry` description. `strings` over
`/home/li/.local/state/spirit/spirit.sema` and `spirit.archive.sema` turns up no
verbatim psyche testimony, and two archived records state the design explicitly:
"Spirit entries carry one clarified description and no verbatim field." Justification is
submitted and judged, then dropped. His position on this is that it is "a bit murky
still; ideally, the judge has a direct line to psyche and just asks him, but for now we
are in a gray area". The draft therefore says only what to submit — `Testimony is the
psyche's exact words plus the question they answered.` — and asserts nothing about
whether a later agent can read those words back. No line in the draft depends on that
question being resolved either way.

## Lines cut, and why

From the current three-line skill:

- `Record only explicit psyche values, aims, or beliefs that guide many decisions.` —
  names the end state and teaches no test. That is `skill-designing`'s fourth cut
  criterion and it is the failure he named. Replaced by the three gates.
- `Route mechanisms, defaults, tasks, and architecture to their owning surface.` — cut
  entirely. `documentation-placement` already lists all eight owning surfaces, and
  `skill-designing` says a skill points to the document instead of restating it. Gate 1
  classifies these as matter, so nothing is lost.
- `Check for an existing record before creating one.` — kept, moved into `Recording`,
  with the maintenance preference beside it.

Cut in revision 2, on his ruling:

- `Record every candidate that passes all three. Do not stop using Spirit because
  earlier agents over-captured.` — "just useless noise." No replacement.

From the pre-cut version at `7f57536^:modules/intent-log/full.md`, recovered and
reviewed in full:

- `The psyche is the human author. Agent messages, implementation choices, test
  failures, artifacts, and summaries are never psyche intent.` — AGENTS.md line 23 says
  it, and AGENTS.md is always loaded.
- `Do not capture private personal substance to a public record.` — AGENTS.md carries
  the leak gate, and he rejected this exact shape: "this is stupid. do not try to
  swallow your tongue".
- Gate 4, `Its "why" bottoms out in a value, not an engineering or efficiency
  tradeoff.` — the same question as gate 1 asked twice. Two gates testing one property
  read as thoroughness and add no discrimination.
- Gate 5, `From the psyche and felt — not agent-synthesized to close a loop.` —
  AGENTS.md. The residual behavior worth keeping is the approved-agent-wording line,
  now in `Recording`.
- The five-item `Do not be fooled` halo list — three items (rule grammar, a sensible
  one-off default, Spirit-operation procedure) are what gate 1 tests, and one is gate 4.
  Reduced to the rule-grammar line, the only one the gates do not already catch.
- `## Classification` and the five intent kinds — schema, not behavior. He has since
  said of the `Decision` variant "it should go" and "I dont even know if we need kinds
  anymore", and another agent holds the schema question. The draft encodes no kind.
- `Choose certainty and importance from the statement's strength and blast radius.` —
  schema field guidance, not checkable, and superseded by his own ruling: "the concept
  of everything that's in Spirit is essentially certain. It's all high certainty. So we
  only leave the importance."
  (`/home/li/primary/reports/logos/protos-engine-psyche-handover-2026-07-21.md:20`).
- `Populate referents for named technologies, repos, components, people, records, or
  topics so later lookup and duplicate checks work.` — schema, plus a justification
  clause.
- The whole `## Manifestation` and `## Citation` sections — that was
  `intent-manifestation`, already deleted, and its destination list is
  `documentation-placement`.
- The `spirit "(Record ...)"` example in `intent-core` — cut for the reason in the
  mechanism section.
- `## Principle, not substance`, five sentences — reduced to one line under
  `Not intent`. The substance is real and evidence-backed; the length was restatement.

Documentation, not behavior, that should be cut and not relocated this session: the
five intent kinds, the certainty and importance guidance, and the referent population
rule. All three describe fields in
`/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema`.

## Lines added, and the real failure each prevents

- **The three gates, two with a naming obligation.** 631 records were captured as
  intent and later archived and removed — architecture-doc 384, skill 97, spirit-manual
  76, code 33, vocabulary-doc 12, repo-intent 11, junk-remove 7
  (`/home/li/primary/agent-outputs/SpiritLegacyMatterRemoval/IntentMaintainer-RemovalEvidence.md:20-27`).
  The live set after that removal was 22. Every removed category is something gate 1
  rejects, and the "spirit-manual 76" bucket is precisely what he called out with "you
  dont store the manual in the database".
- **`Name that path.`** Gate 2 is otherwise unanswerable from a transcript, which is
  the defect he found in the first version.
- **`Name that decision.`** Same requirement for gate 3.
- **`Most sessions record nothing.`** Sets the base rate. No line in the current skill
  does.
- **`A borderline candidate is matter.`** His own one-word ruling, quoted above.
- **`Do not soften a candidate that fails the test into a weaker record.`** The removal
  set included ten ids explicitly classed borderline-out — `q9n2 48y4 ki6i lrfa nu76
  op4b qoku hu84 j81n h0bj` (same file, `:23-25`). They were captured anyway. Certainty
  is a field, so downgrading is the available escape from a failed test.
- **`Do not read "never", "always", or "must" as a sign of intent.`** Matter examples 1,
  3, and 5 are absolute-grammar matter, one of them in full capitals demanding
  permanence.
- **`The psyche's rejection of a draft, a plan, or a file.`** Records `dhqe` and `em04`
  were captured out of one design discussion and had to be retired, and `n9fl` was
  clarified out of the same discussion and had to be reverted to its earlier wording
  (`/home/li/primary/agent-outputs/SpiritCleanupRejectedCaptures/IntentMaintainer-Result.md:17-28`).
- **`A statement made in frustration, until the psyche states it again on a separate
  occasion.`** "dont panic-send an agent, just make a note of it for later", plus "my
  agents are neurotic, and theyre trying to deal with my frustration". A separate
  occasion is the cheapest available proxy for the unbending property.
- **`Write every psyche ruling in the current train to the design log.`** Removes the
  loss-aversion motive behind marginal captures.
- **`Keep the psyche's hedges.`** An archived Spirit record: "Intent capture must
  preserve the psyche modality and never upgrade tentative wording into confident
  assertion: when the psyche hedges with I think, I feel like, could, or maybe, the
  recorded certainty must stay low and the wording must not be rewritten from could into
  should or from a feeling into a fact." (agent-clarified description, not his words).
  The workspace tracks live hedged statements as such, for example "possibly two-way
  decode-encode rust… crazy idea" (`vision-evidence-ledger-v1.md`, row L8, marked
  "Psyche (hedged)").
- **`If the only wording is yours and the psyche agreed to it, ask the psyche to state
  it before recording.`** The rejected `n9fl` clarification was agent wording that had
  passed. The schema carries `TestimonyFabricated` as a guardian rejection reason
  (`signal.schema:253`), so this failure is modelled in the system.
- **`Take the wire shape from the signal-spirit schema.`** Two copies of the record
  syntax disagree today, as documented above.
- **`When Spirit is unreachable, stop and hand the candidate and its testimony back to
  the psyche.`** Verified: no queue, no spool, connect failure exits 1.

## Open questions for the psyche

1. **Is the negative-examples ban real, and does `Not intent` violate it?** See the
   answer section at the top. The ban is his words from one session; my "separate
   occasions" claim was inference. The sentence that would settle whether prose-only
   category naming is permitted is an agent's derivation.
2. **`psyche-vision` duplicates this test.** Recommend deleting it and letting
   `intent-log` own the definition. Manifest change, not made.
3. **Certainty was ruled out and is still in the schema.** "the concept of everything
   that's in Spirit is essentially certain… So we only leave the importance."
   (`protos-engine-psyche-handover-2026-07-21.md:20`), but
   `Entry { Domains Kind Description Certainty Importance Privacy Referents }` still
   carries it (`signal.schema:225`). Unimplemented ruling, or superseded. Relevant to me
   only because `Do not soften a candidate` assumes a certainty field exists to soften
   into; if certainty goes, that line loses its mechanism and should be re-examined.
4. **The guardian already enforces part of this.** `GuardianRejectionReason` includes
   `NonIntent`, `Matter`, `Overstated`, `InsufficientWarrant`, and `TestimonyFabricated`
   (`signal.schema:253`). If the guardian prompt is the real gate, the skill's job may be
   narrower than I have written it. The prompt is not reboot-persistent per
   `/home/li/primary/agent-outputs/Handover-SpiritIntent-and-Deployment.md:59-63`, and I
   could not read the running prompt with the daemon down.
5. **`design-log` has never been used.** No `design/` directory exists anywhere in
   `/home/li/primary`, and `skills/design-log.md` has one commit (`c7e716b`). The routing
   section sends most psyche rulings to a surface with no exercised instance.
6. **`design-log`'s recency rule conflicts with his ruling on recency.** See the routing
   section.
7. **`intent-core` is orphaned and now diverges.** Declared `RoleComposition` in
   `manifests/module-dependencies.nota` but named by no manifest, so it reaches zero role
   packets (corpus handover open item 8). It still carries the old five-gate text and the
   disputed `spirit "(Record ...)"` example. Recommend deletion rather than syncing it to
   this draft.
8. **The Spirit daemon needs a rebuild, not a restart.** The installed
   `spirit-judge-0.1.0` binary does not accept the `--session-launcher` flag its own unit
   wrapper passes. Restarting will loop again.
9. **The corpus handover's own `## Vision` section is written in an agent's words**,
   bolded, reading as settled doctrine
   (`/home/li/primary/reports/SkillsCorpusRedesign/context-handover.md:9-53`); the
   verbatim quotes are only at lines 69-77. This is the corruption path he described,
   occurring in the document that describes it. Nothing guards reports.

Closed since revision 1: the `Kind` enum question. He ruled `Decision` "should go" and
raised whether kinds are needed at all; another agent holds it. The draft encodes no
kind, so nothing here depends on the outcome.

## Lines I am least confident in

- `Keep the psyche's hedges. "I think" and "maybe" stay at their original strength in
  the description.` **This is the next line I would expect him to cut**, for the same
  reason he cut the over-capture line: its only evidence is an agent-written Spirit
  record description, not his words. It is corroborated by hedge-tracking in the
  evidence ledger, but he has never stated it. I would not defend it.
- The `Not intent` section, against the negative-examples ban. Open question 1, and the
  answer section says plainly where my citation was weaker than I represented.
- `Take the wire shape from the signal-spirit schema.` The schema is generated wire
  truth, but an agent reading a `.schema` file still has to derive NOTA positional
  encoding to produce a valid call. This may be an instruction that cannot be followed,
  in which case the honest replacement is a blocker line telling the agent to ask.
- `A statement made in frustration, until the psyche states it again on a separate
  occasion.` "Frustration" is a judgment, and an agent that reads him as frustrated
  whenever he is blunt will never record anything. He is blunt constantly. That may be
  the intended bias, but it is a bias I chose. My own misuse of "separate occasions" as
  a citation standard, documented at the top, is not a reason to drop it, but it does
  show the phrase is easy to claim without checking.
- Gate 2 as reworked. It is answerable, which the old one was not, but it is less
  exclusionary — four matter examples now pass it. Gates 1 and 3 carry more load than
  before.
- `Most sessions record nothing.` States a fact rather than directing an action, which
  is the shape he cuts.
- Dropping `psyche-vision` from the skill's routing section. A three-way routing rule
  was asked for and I wrote a two-way one, on the grounds that `psyche-vision` is not a
  destination.
- Qualifying example 3 (`346n`, quality). Its gate-2 answer is implied rather than
  stated, and it weakened under the gate 2 rework.
