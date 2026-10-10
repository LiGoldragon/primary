<!-- to-the-living:start -->
Presentation.{ «What the new Message does with the old store» }

## The case

The Message in production keeps its store at the default location, and the new Message, in development, looks for its store at that same location. The two shapes differ. The old store holds a configuration of five fields: the ordinary and meta sockets, Flow's ordinary and meta sockets, and the list of meta aspects. It holds no record of whether a meta Configure was ever done. The new Message's Memory holds one `Standard` record: a Configuration of three paths (ordinary, meta, Flow) and the `MetaConfigured` marker. Message's buildable design says a store that exists holds the configuration and a store created new is seeded from the constant (message-design.md:99-100 at e275b6), and that the store starts fresh with no migration (685-686), the latter marked as its own inference. It does not say what happens when the store that exists is the old one. Astra's reading of the two designs sets this question (flows/73ada7/reports/astra-runtime.md:31); the old source was read there, not here. Starting fresh in place would erase the old store without a word, and giving the old store a marker would invent what it never recorded, so no option below does either. The startup payloads re-send all three paths on every start (message-design.md:105-111), so the old configuration looks redundant once the new Message is configured; that is this flow's inference.

## Distillation

### D1. A Nexus that finds a store of an older shape, in vision-nexus

Target: `psyche-skills/skills/vision-nexus.md`, a new section after «First configuration» (line 96-105) and before «Repositories» (line 107). The section «Configuration» above it (line 87-94) stands as: A Nexus starts with no arguments and there is no bootstrap binary. Its executable holds a default configuration as a constant. On start it looks for its Sema database at the default location: a database that exists holds the configuration; a database created new is seeded with the defaults. The meta socket carries a Configure interface, and changed values are accepted through it. Nothing is removed; one section is added, and any source line is appended under «Sources» (line 199).

**Option (a), the Nexus refuses to start.**

Added, under the heading «A store of an older shape»: A Nexus that finds at its default location a database whose record types are not its own does not start. It names that database and the shape it found, and the owner moves or removes it before the Nexus starts again.

Sources added: none; the option rests on statements already landed.

Rests on: psyche-skills/skills/spirit.md:17 (landed 2026-10-07), that an older shape is replaced and never kept through a compatibility path; psyche-skills/skills/vision-nexus.md:91-93 (landed 2026-10-07), where a database that exists holds the configuration and one created new is seeded. That an old-shape store is neither of those two cases, so the Nexus has no ruled path to take with it, is this flow's reading. The skill field-skills/skills/compensation-breaking-upgrades.md:6-8 (landed 2026-10-07; machine-authored from flows/01a02b46/vision/zeusUpdate.md:112-116, 2026-08-23) asks that the deploy of a breaking change be written in the repository's UPGRADES.md; that the owner's step would be written there is this flow's inference.

**Option (b), the Nexus moves the old store aside and starts fresh.**

Added, under the heading «A store of an older shape»: A Nexus that finds at its default location a database whose record types are not its own moves it aside under a name that says so, and starts with a database created new, seeded with the defaults. Its first-configuration record is unset, so Configure is accepted until a meta Configure is done.

Sources added: 836818 flowNexus.

Rests on: flows/836818/vision/flowNexus.md:47-51 (2026-09-24, STT, raw, heard by d8df70 and forwarded), that old stores of Flow and Message need not be kept and that this is not a migration, said because nothing was live yet. Whether those words still hold now that the old Message runs in production is unknown; this option reads them as holding. The skill field-skills/skills/compensation-design.md:21-23 (landed 2026-10-07) asks that useful content be kept or shown redundant before it is deleted; moving the store aside keeps it. Then psyche-skills/skills/vision-nexus.md:98-101 (landed 2026-10-07), where the first-configuration record says whether the meta Configure was done on this Nexus; that a new database records it as not done is this flow's reading, and the design implies it without writing it (astra-runtime.md:28).

**Option (c), the Nexus migrates the old configuration.**

Added, under the heading «A store of an older shape»: A Nexus whose record types change ships the migration with the change. On finding a database of the older shape, it carries each value its new configuration still has into the standard metadata tree, drops the rest, and replaces the old records. The first-configuration record stays unset, since the older database never recorded a meta Configure.

Sources added: none; the option rests on statements already landed.

Rests on: psyche-skills/skills/vision-sema.md:10-11 (landed 2026-10-07), that operational editing should yield the migration with the edit; psyche-skills/skills/vision-nexus.md:98-103 (landed 2026-10-07), the standard metadata tree that holds the socket paths. That a one-time migration which replaces the old records is not the parallel compatibility path that psyche-skills/skills/spirit.md:17 forbids is this flow's reading. For Message, the ordinary, meta and Flow paths would carry over and Flow's meta socket and the meta aspects would drop, since the new Configuration has no field for them (message-design.md:172-175, 124-127); which old Flow path matches the new Flow edge was not read here and is unknown. The record flows/836818/vision/flowNexus.md:47-51 (2026-09-24, raw) speaks against migrating Flow's and Message's stores.

**Ruling D1.** (a) Refuse to start. (b) Move aside and start fresh. (c) Migrate into Standard. (d) Amend, by line.

## Voice

One choice. The new Message will find the old Message's store where it looks for its own. A refuses to start and names it, so you or the owner clear it. B moves it aside and starts clean, waiting for a Configure, as you said on 24 September that old stores need not be kept. C carries the three paths over into the new record, with the marker unset, the way vision-sema asks a change to carry its migration. Which one? This flow's reading: your 24 September words were said before anything was live, and the old Message is live now, so whether they still stand is yours to say.
<!-- to-the-living:end -->
