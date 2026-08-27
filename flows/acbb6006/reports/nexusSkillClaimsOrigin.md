# Nexus Skill Claims — Origin Report

Four claims in the nexus skill (`/git/github.com/LiGoldragon/Curriculum/skills/nexus.md`,
consumed at `/home/li/primary/.claude/skills/nexus/SKILL.md`) have no psyche record in the
prior gather (`reports/distillCandidatesNexus.md`). This report traces each to its authored
paragraph, its earliest Curriculum commit, and any psyche words found on the subject.

---

## Claim 1 — "One capability, one Nexus."

**Verbatim paragraph in authored source** (`## How nexuses fit together`):

> One capability, one Nexus. A Nexus is sized to be held whole
> in one mind — human or model; when it outgrows that, it splits.

**Git origin** — earliest Curriculum commit introducing this phrase:

- Commit `4a99743` — 2026-08-10 00:14:58 +0200 — "skills: add rust-component-architecture"
- No flow short ID in the commit message.
- `git log -S "one mind"` finds no earlier commit in any branch; the phrase did not exist in
  the Curriculum before this commit.

**Transcript origin** — flow `98fbfa47` (active 2026-08-09):

- The model agent composed the "How components fit together" section — in which this sentence
  appears verbatim — in transcript line 519 (2026-08-09T18:24:41Z), which is an **assistant**
  turn. The content is model-authored, not psyche dictation.
- Psyche approval of the whole skill draft: transcript line 539 (2026-08-09T20:18:23Z):
  > "its good enough I guess. We can deploy that in skills repo, commit and regenerate."
  The approval covered the draft as a whole; the "How components fit together" section was not
  called out separately.

**Psyche record search** — grep of `Vision/`, `psyche-raw/`, `flows/*/vision/` for "one mind",
"one capability", "split": **no results**. No psyche record found.

---

## Claim 2 — "Observation flows up, authority flows down: state is observed through push subscriptions — a typed snapshot on open, typed deltas after"

**Verbatim paragraph in authored source** (`## How nexuses fit together`):

> Observation flows up, authority flows down: state is observed through
> push subscriptions — a typed snapshot on open, typed deltas after —
> and commanded through the owner's mutation vocabulary. `Observe.Locks`
> is a one-shot typed Lock snapshot, not a subscription. Polling is
> forbidden; a correct system goes quiet when nothing changes.

**Git origin** — earliest Curriculum commit introducing "push subscriptions":

- Commit `4a99743` — 2026-08-10 00:14:58 +0200 — "skills: add rust-component-architecture"
- No flow short ID in the commit message.
- `git log -S "push subscriptions"` finds no earlier commit in any branch.

**Transcript origin** — flow `98fbfa47` (active 2026-08-09):

- Same model-authored draft (transcript line 519, 2026-08-09T18:24:41Z).
- The subscription shape (current state on open, then deltas) has a precursor in the old
  `modules/push-not-pull/full.md` (commit `27ed72ff`, 2026-06-26, "materialize migrated skill
  modules"), where the module reads: "Every subscription emits the producer's **current state
  on connect**, then deltas after that." That module text is agent-authored guidance, not psyche
  dictation.
- Psyche approval: transcript line 539 (2026-08-09T20:18:23Z), as above.

**Psyche record search** — grep for "push subscriptions", "subscription", "snapshot", "delta"
in `Vision/`, `psyche-raw/`, `flows/*/vision/`: **no results**. No psyche record found.

---

## Claim 3 — "When one intent spans several nexuses, the issuer commits on the first success and records divergence on failure — no distributed rollback, no all-or-nothing stall."

**Verbatim paragraph in authored source** (`## How nexuses fit together`):

> When one intent spans several nexuses, the issuer commits on the
> first success and records divergence on failure — no distributed
> rollback, no all-or-nothing stall.

**Git origin** — earliest Curriculum commit introducing "distributed rollback":

- Commit `4a99743` — 2026-08-10 00:14:58 +0200 — "skills: add rust-component-architecture"
- No flow short ID in the commit message.
- `git log -S "distributed rollback"` and `git log -S "all-or-nothing stall"` both find no
  commit before `4a99743` in any branch; these phrases are not in the pre-reset module corpus.

**Transcript origin** — flow `98fbfa47` (active 2026-08-09):

- Same model-authored draft (transcript line 519, 2026-08-09T18:24:41Z). No earlier typed human
  message in the flow mentions "distributed rollback" or "all-or-nothing stall". The sentence is
  model-composed synthesis with no verbatim ancestor found in the old corpus modules.
- Psyche approval: transcript line 539 (2026-08-09T20:18:23Z), as above.

**Psyche record search** — grep for "rollback", "all-or-nothing", "distributed" in `Vision/`,
`psyche-raw/`, `flows/*/vision/`: **no results**. No psyche record found.

---

## Claim 4 — "Polling is forbidden; a correct system goes quiet when nothing changes."

**Verbatim paragraph in authored source** (`## How nexuses fit together`):

> Observation flows up, authority flows down: state is observed through
> push subscriptions — a typed snapshot on open, typed deltas after —
> and commanded through the owner's mutation vocabulary. `Observe.Locks`
> is a one-shot typed Lock snapshot, not a subscription. Polling is
> forbidden; a correct system goes quiet when nothing changes.

**Git origin** — earliest Curriculum commit introducing "Polling is forbidden":

- Commit `27ed72ff` — 2026-06-26 20:30:39 +0200 — "materialize migrated skill modules"
- This commit adds `modules/push-not-pull/full.md`, which opens with:
  > "The principle lives in `ESSENCE.md` §'Polling is forbidden': **producers push, consumers
  > subscribe; no poll loops.**"
- The module text is agent-authored guidance citing an ESSENCE.md document; it is not a psyche
  dictation record.
- In the nexus skill (rust-component-architecture) the sentence "Polling is forbidden; a correct
  system goes quiet when nothing changes." first appears in commit `4a99743` (2026-08-10).
  `git log -S "goes quiet"` finds `4a99743` as the first matching commit for that exact form.
- The push-not-pull module (27ed72ff) says "Push-correct systems go quiet when they have
  nothing to do" — close in sense but not the same wording. The exact current form was
  re-drafted by the model agent in flow `98fbfa47` (transcript line 519, 2026-08-09T18:24:41Z).
- No flow short ID in either commit message.

**Transcript origin** — flow `98fbfa47` (active 2026-08-09):

- Same model-authored draft (transcript line 519, 2026-08-09T18:24:41Z).
- In the agent's corpus survey (transcript line 529, 2026-08-09T18:31:12Z — assistant turn),
  item 14 reads:
  > "The anti-polling escalation ladder: when a producer can't push — build the primitive into
  > the producer, replace the producer, or defer the feature. Falling back to a poll is never
  > the answer. 'Push-correct systems go quiet when they have nothing to do.'"
  That paraphrase is agent-authored; no psyche typed words about polling are in the transcript.
- Psyche approval: transcript line 539 (2026-08-09T20:18:23Z), as above.

**Psyche record search** — grep for "polling", "poll", "Polling is forbidden", "goes quiet" in
`Vision/`, `psyche-raw/`, `flows/*/vision/`: **no results**. No psyche record found.

---

## Sources

- Authored skill source: `/git/github.com/LiGoldragon/Curriculum/skills/nexus.md`
- Curriculum commit `4a99743` (2026-08-10): `git log -S "one mind"`, `-S "push subscriptions"`,
  `-S "all-or-nothing stall"` — all return `4a99743` as earliest
- Curriculum commit `27ed72ff` (2026-06-26): `git log -S "Polling is forbidden"` — old modules
  precursor; `modules/push-not-pull/full.md` introduced there
- Flow `98fbfa47` transcript `/home/li/.claude/projects/-home-li-primary/98fbfa47-58a9-4a7b-8847-829443079d25.jsonl`:
  - Line 507 (2026-08-09T18:23:09Z): psyche typed instruction on skill structure
  - Line 519 (2026-08-09T18:24:41Z): assistant draft containing all four claims (model-authored)
  - Line 527 (2026-08-09T18:30:14Z): psyche typed "look for other interesting, unusual, high level instructions from the old corpus"
  - Line 529 (2026-08-09T18:31:12Z): assistant corpus survey listing anti-polling principle
  - Line 539 (2026-08-09T20:18:23Z): psyche typed approval "its good enough I guess. We can deploy that in skills repo, commit and regenerate."
- Prior gather: `/home/li/primary/flows/acbb6006/reports/distillCandidatesNexus.md` (confirms
  all four as "No psyche record found")
- Psyche record search: grep of `Vision/`, `psyche-raw/`, `flows/*/vision/` — no matches for
  any of the key phrases
