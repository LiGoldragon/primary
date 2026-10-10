# Versioning, tags, releases, pins — records found

Question before the main flow: Flow's release tag `flow-0.17.4` and the Home
pin both name revision bc464e5; main has since moved ahead by commits that
change only tests and an evidence receipt (no production source, build
definition, lock file, or version). Must the tag/pin stay, with test evidence
recorded separately, or does policy require a new version/tag/pin whenever
main moves?

Search covered `Vision/`, `vision-raw/`, `flows/*/vision/`, `flows/*/notion/`,
the generated `.claude/skills/` tree (as evidence of standing rules, not
loaded as skills), and the local read-only checkouts at `/home/li/primary/flow`
and `/home/li/primary/design/CriomOS-home`. No `Intent/` directory exists in
this working copy. No `flows/*/notion/` file matched the search terms.

## The living's own words

### On versions living in a manifest, not the file — the standing rule for "what is versioned"

> I think I want to drop the version number altogether. datom doesnt have
> versions. if we version stuff it should be in a manifest of some kind. Lets
> drop the versionning everywhere for now. I guess any type would need an
> import section.

-- psyche, typed, 2026-09-04, flow e996e8, `flows/e996e8/vision/archive-ethos.md`
(archived on landing; distilled into `Vision/ethos.md` §"Declaration, File",
2026-09-05). Level: Vision, distilled (the archive page states the distilled
target; the archive itself is the raw record).

Distilled form, `Vision/ethos.md`:

> An ethos file carries no version; datom has no versions. What is
> versioned is versioned in a manifest of some kind, never in the file.

-- `Vision/ethos.md`, undated within the file (carries the 2026-09-04/09-05
provenance above).

### The record this superseded — version numbers as marking the first stable release

> version should be 0 1 0 - well keep version 1 for the first
> stable release

-- psyche, typed, 2026-08-14T15:24+02:00, Designer session ba906ae2,
`flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`. This page is
explicitly marked at its top: "Archived as superseded by 'drop the version
number altogether' (e996e8, 2026-09-04). The words are kept here." Level:
Vision, raw (archived, retained for its own words per the psyche skill's
retention rule — a later correction does not erase the older record).

### On "tag" as a word the living rejects for Datom / interfaces

> And I don't know what you mean by tag. Datom doesn't have tags, has
> variants.

-- psyche, speech-to-text (per the surrounding record's framing), no date
given in the passage itself, flow 93ba9f, `flows/93ba9f/vision/datomVocabulary.md`
(also carried in `flows/b7ba00/vision/messaging.md`). Level: Vision, raw.
Context recorded by 93ba9f: this was the living's response to being asked
whether a description of "tag, Flow ID, and text" (a speech-to-text record an
earlier flow attributed to the living, 2026-09-25) was the living's own
wording.

> Nobody said the word means nothing but you're talking about a tag when we
> were talking about [Clojure] so you're confusing things. It's not that I
> don't understand what the word means, it's that you're using it out of
> context.

-- psyche, same source and provenance, immediately following, correcting a
flow's summary that had dropped the earlier "tag" record as a likely
mishearing. This exchange concerns the word "tag" as used for a *message*
shape (Datom envelope vocabulary), not a version-control tag; it is included
because it is the only place the living is recorded using the word "tag" at
all, and it shows the living distinguishing contexts rather than ruling on
release tags.

### On release/deploy cadence in general terms (not specific to tags or pins)

> Oh yeah, deploy: horizontal deployment. Once things have been tested in one
> place, in the primary, in the sandbox, then they try to release that and
> fix it. They ask if they need clarity for fixes or if they need to send
> stuff to design. They send it back to primary.

-- psyche, flow 6cc91b, `flows/6cc91b/vision/pairHierarchy.md`. Level: Vision,
raw. Speaks to the order of testing-then-release across hosts; does not
address whether a tag may sit behind main, or whether tests-only commits
require a new tag/pin.

> Trying to fix something, release and deploy something, and debug something
> in the system is the field. That's all the field.

-- psyche, flow b81560, `flows/b81560/vision/operational-triadWorkDivision.md`.
Level: Vision, raw. Assigns release/deploy work to the field aspect; does not
speak to tag or pin mechanics.

### On version bumps for a messaging redesign (illustrative use of "version," not a general rule)

> Meanwhile let's have just a very primitive version, a proof of concept,
> with just a few different types of messages, like what we've been doing so
> far. A better version of message should be redone and redeployed with just
> a string as the basic form. We're going to maybe develop it a little bit
> and then release it in the next version but we can have a primitive version
> of that while we do the database rename and stuff.

-- psyche, flow 93ba9f / b7ba00, `flows/93ba9f/vision/messagingInterface.md`
and `flows/b7ba00/vision/messaging.md`. Level: Vision, raw. Uses "version" and
"release" colloquially for iterations of the messaging design; not a rule
about tags, pins, or what changes warrant a version bump.

## No living record found on

- Whether a release tag or a Home/flake pin may name a revision behind main.
- Whether a tag, once set, may be moved, or must be superseded by a new tag.
- Whether tests-only or evidence-only commits require a new version, tag, or
  pin.
- Whether test evidence must sit inside the tagged/pinned revision or may be
  recorded separately alongside it.

No `flows/*/notion/` entry on any of these topics was found either.

## Project rules found in documents (not the living's own words)

### Generated skill `versioning` (evidence of a standing rule, read only, not loaded)

> Update the version surface changed by public behavior, wire, storage,
> package, or deployment changes.
> Do not bump docs-only changes unless the docs are runtime-visible.

-- `/home/li/wt/primary/56ae53/.claude/skills/versioning/SKILL.md`. This rule
names the categories of change that warrant a version bump (public behavior,
wire, storage, package, deployment) and explicitly excludes docs-only changes
unless runtime-visible. Tests and an evidence receipt are not among the named
categories, nor are they addressed by name.

### Generated skill `breaking-upgrades`

> Document how to deploy each breaking change in the repository's
> `UPGRADES.md`. Land the documentation with the breaking change.

-- `/home/li/wt/primary/56ae53/.claude/skills/breaking-upgrades/SKILL.md`.
Ties documentation, not a tag, to the breaking change's landing; silent on
whether every version-worthy landing needs a new tag or pin, and silent on
tests-only commits.

### Generated skill `testing`

> When assigned as a testing worker, accept a bounded target, immutable
> revision, authority limits, and acceptance contract. ... Report what each
> witness proves, the exact revision and scope tested, and what remains
> unavailable.

-- `/home/li/wt/primary/56ae53/.claude/skills/testing/SKILL.md`. Frames a test
witness as reporting against "the exact revision ... tested" — consistent
with a tested revision being named and reported, but does not say the tag or
pin must be moved forward to the revision where the test evidence was
produced, nor that evidence must live inside the tagged revision.

### Flow repository's own `UPGRADES.md` (local checkout, `/home/li/primary/flow/UPGRADES.md`)

The document is a per-version changelog. Every entry ties a version bump to a
wire, storage, or CLI/contract change:

> Flow 0.9.0 speaks `signal-flow` 4.0.0 and `meta-signal-flow` 6.0.0. Both
> wires change: upgrade `flow`, `flow-meta`, and `flow-nexus` from one package
> closure.

> The privileged wire is not archive-compatible with Flow 0.3.0. Upgrade the
> `flow`, `flow-meta`, and `flow-nexus` binaries from one package closure.

No entry in this file ties a version bump to a tests-only or evidence-only
change; every entry names a wire, storage, or CLI-surface change as the
trigger. This is consistent with the generated `versioning` skill's rule but
is the repository's own document, not the living's word, and it is silent by
omission rather than by an explicit "tests alone never bump."

### Nix input upgrade skill, on tags versus revisions (a different question: verifying upstream fixes, not naming this project's own tag)

> A version number does not prove a specific fix is included. Verify the fix
> against upstream commit history, not the release tag.

-- `/home/li/wt/primary/56ae53/.claude/skills/nix-input-upgrade/SKILL.md`.
This concerns verifying *external* package fixes against upstream commits
rather than trusting an external release tag's version number; it does not
address whether this project's own pin may name a revision behind its own
tag, or whether pins must track main.

### Operational handoff records on Home/CriomOS pins (machine-origin, not the living's words)

`flows/b7da5d/vision/ouranosRedeploy.md` records several Field-Sol handoffs
(2026, undated exactly beyond the flow's own dates) describing Home and
CriomOS pins by full commit hash/revision rather than by tag, e.g.:

> Existing proof: Home 017916fc9dcaf269842ca450511b6b3fd88d509a and CriomOS
> 068e06e7de14f6001ac035f6ca37760d15a5be6e passed remote checks; coherent Flow
> is 54856835f88deacbede8e314286f10beb2cda15f; its closure is
> /nix/store/qm6cb0piaf8z90pvfnb4447x4j690m4d-flow-0.5.0. Pin locks 5389 and
> 5390 are released.

These are operational/handoff messages between flows (Field Sol coordination),
not psyche records and not a stated policy — they show *practice* (pins named
by revision hash, reconciled and "confirmed at origin" before activation) but
never state whether a pin may lag main, whether it must be a tag versus a raw
revision by rule, or how test-only commits factor in.

## What the records settle, and what they do not

**Settled by an explicit living ruling:** version numbers belong in a
manifest, never in the file/source itself (2026-09-04, superseding an
earlier 2026-08-14 ruling that had version numbers marking release
stability directly in an interface file's header). This is a rule about
*where* a version lives, for Ethos/Datom specifically — not a rule about
when a version must be bumped, when a tag must move, or how pins relate to
main.

**Not settled by any living record found:** whether main may sit ahead of
the latest release tag; whether a tag or pin may be moved after being set;
whether a Home pin must name a tag, a revision, or track main; whether
tests-only or evidence-only commits require a new version/tag/pin; whether
test evidence must be inside the tagged revision or may be recorded
separately. No Vision, Notion, Intent, or Spirit record answers these
questions directly, under any topic search term tried (version, versioning,
semver, bump, tag, release, pin, "next", stable).

**Closest applicable rule, from project documents rather than the living:**
the generated `versioning` skill and the Flow repository's own `UPGRADES.md`
practice both tie a version bump to production-behavior, wire, storage,
package, or deployment changes, and are both silent on — or by omission
exclude — tests-only or evidence-only changes as a bump trigger. Neither
document is the living's own word, and neither states the tag/pin-movement
question (whether main may be ahead of the tag, or whether a pin must
track main) at all.

**Tension surfaced, not resolved:** the two versioning rulings on file
(2026-08-14 and 2026-09-04) point in different directions about where
version identity is visible (in an interface file's header vs. only in a
manifest) and the later one is explicitly marked as superseding — but per
the psyche skill's own retention rule, the earlier record is not erased and
both are carried here. Separately, the "tag" exchange in
`datomVocabulary.md` shows the living rejecting "tag" as a Datom-message
term ("Datom doesn't have tags, has variants") in a Clojure-context
discussion — this is not evidence either way about release/version-control
tags, but a flow reading it out of context could wrongly extend it to mean
the living rejects tags generally; the record itself warns against exactly
that confusion ("you're using it out of context").

## Sources

- `flows/e996e8/vision/archive-ethos.md`
- `Vision/ethos.md`
- `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md`
- `flows/93ba9f/vision/datomVocabulary.md`
- `flows/b7ba00/vision/messaging.md`
- `flows/93ba9f/vision/messagingInterface.md`
- `flows/6cc91b/vision/pairHierarchy.md`
- `flows/b81560/vision/operational-triadWorkDivision.md`
- `flows/b7da5d/vision/ouranosRedeploy.md`
- `/home/li/wt/primary/56ae53/.claude/skills/versioning/SKILL.md`
- `/home/li/wt/primary/56ae53/.claude/skills/breaking-upgrades/SKILL.md`
- `/home/li/wt/primary/56ae53/.claude/skills/testing/SKILL.md`
- `/home/li/wt/primary/56ae53/.claude/skills/nix-input-upgrade/SKILL.md`
- `/home/li/primary/flow/UPGRADES.md` (local read-only checkout)
- `/home/li/primary/flow/README.md`, `/home/li/primary/flow/DESIGN.md` (read, no matching policy passages beyond those quoted/noted)
- `/home/li/primary/design/CriomOS-home/*.md` (read; no version/tag/pin/release passages found)
- Directories searched with no matching result: `Intent/` (absent), `vision-raw/` (matches were the ethos/version passages already covered), `flows/*/notion/` (no hits for the search terms)
