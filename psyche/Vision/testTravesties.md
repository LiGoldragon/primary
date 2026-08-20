# Test travesties

## 2026-08-10 — "is not a test, its a travesty"

> is not a test, its a travesty. we have to put a guardrail against
> making such travesties, and prentending we're testing anything. I
> have no words to describe how stupid this "test" is. There must be
> many more.

> Well do this on the next session.

— psyche, 2026-08-10T10:37Z (Designer session 98fbfa47), on the
skills-repo unit test `management_is_subagent_scoped_and_has_no_
psyche_interaction_doctrine` (it asserts doctrine placement in a
skill's text and currently blocks the repo's check binary from
building).

Context, kept apart from the quotes: ordered for the next session — a
guardrail against writing such tests, and a sweep for the many more
the psyche expects exist. The pre-reset witness doctrine is the
likely seed: every test names an observable witness; a positive
witness plus a negative shortcut-must-fail test; "a test that builds
a miniature copy of the logic inside the test... is not a witness. It
is a self-contained story."

## 2026-08-10 — "make it beats for somebody else to pick up"

> Creating beats for somebody else to take care of that is stupid and
> you shouldn't have to deal with this.

> Clean out the garbage about the Travis T-test and just make it beats
> for somebody else to pick up.

— psyche, 2026-08-10T12:12Z (Designer session 13cfc23f), superseding
the prior entry's "Well do this on the next session."

Context, kept apart from the quotes: the guardrail and sweep work
moves to beads for a worker agent; the Designer refocuses on the
Protos engine. Transcription: "beats" = beads, "Travis T-test" =
travesty test. The first sentence is ambiguous on its own; the second
carries the operative order.

## 2026-08-19 — a test cannot bring in its own data and test it against production; remove the crap

Design session `7c3f0c1d`, typed (captured 2026-08-19T14:45+02:00), on the
report that Curriculum's `nix flake check` fails on `role-cross-product-manifests`
because the check hardcodes model names that `role-depths.dotos` no longer has:

> most of those tests are complete garbage. we should remove the crap. a test
> cannot bring in its own data and then test it against production. and the
> notion of testing if the production code conforms to itself is so stupid it
> can hardly be expressed in words. Im stunned at the stupidity of many tests
> that agents seem to conceive. I havent tackled this problem, but I will once
> we have a hold of the top stratum and more properly trained flows.

## 2026-08-20 — prose-pinning assertions are not tests; hunt them down, remove at the root; train agents to never design this again

Design session `e06e4c07`, typed (captured 2026-08-20T12:58+02:00).
The Designer had reported that Curriculum's tests/generation.rs
hardcodes skill prose verbatim (an assertion on "…provenance from the
originating session.") and had to be realigned when the approved
wording changed:

> you mean you fixed the monstrous ugliness that even the most
> depraved man on earth wouldnt even dare to call a test?

> those "things" should be hunted down, removed at the root, and
> agents should be trained to never try to "design" anything so
> stupid ever again.

## 2026-08-20 — testing skills means scenarios: the skilled flow against the unskilled one; "the source code says X" is repulsive

Design session `e06e4c07`, typed (captured 2026-08-20T12:59+02:00),
on the proposed testing-skill line against prose-pinning assertions:

> if we test skills, that means creating scenarios and running an
> agent flow to see how the skilled flow fares against the unskilled
> one. I dont want to get into this now, but testing that "the source
> code says X" is repulsive to the mind of the sane.

## 2026-08-20 — anything that searches the text of a skill is complete nonsense; the skill line is not bad; a general point against source-searching tests; no grep-style tests; research directed

Design session `e06e4c07`, typed (captured 2026-08-20T13:55+02:00).
The Designer had surfaced a kept test asserting that technical API
field names do not appear in the subflows skill, and the proposed
testing-skill line:

> anything that searches the text of a skill is complete nonsense.

> the skill line is not bad. I think we should also make a general
> point against tests that search or compare the source code itself,
> as opposed to running an actual machinery which tests something
> under load. I dont want grep style tests. do a research into this;
> there must be a scourge of this nonsense infecting the world right
> now Im sure some well worded and respected people have something to
> say about it and how they deal with it

## 2026-08-20 — the testing lines approved, land them; first deeper bad-tests research, compared against our repos' tests; the cleanup prompt after

Design session `e06e4c07`, typed (captured 2026-08-20T14:32+02:00),
on the proposed testing-skill lines (a test runs the machinery; a
source-text-searching test is a change-detector, never written; text
asserted only where text is the product):

> its good. land it and give me a prompt I can give a flow to go
> clean up all our tests from this scourge. No, actually, first let's
> go deeper in bad tests research land, show me what you find (you
> can compare your findings with my repos' tests to find examples of
> the bad patterns you may be able to articulate after your research)
