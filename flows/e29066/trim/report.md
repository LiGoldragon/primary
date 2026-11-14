# Trim: permaflow module lists applied

Order: /home/li/primary/flows/f22e1a/lighter-flows-order.md (Psyche core Fable, on the living's word).
Running Flow 0.53.1 (fc27dd86). Backup of the configuration before: before.datom; after: after.datom.

## SystemModules rule
- Curriculum `system_module()` (Curriculum/src/startup.rs:221) admits only `spirit:` and `intent:`. Its ComposeStartup refuses any other module in the system list ("module has the wrong startup placement") and any module named in both lists.
- Flow (flow-nexus/src/composition.rs, `validate` at ~l.409 and `placed_in_system_prompt` at ~l.786) does not refuse a vision/knowledge/role module in SystemModules: it requires SystemModules non-empty, well-formed, duplicate-free, and disjoint from UserModules, and at launch re-partitions both lists by kind (spirit and intent to system, all else to user), "whichever list of the launch names it". So the old configuration was tolerated, not valid for Curriculum.
- Applied: spirit and intent in SystemModules; every vision, knowledge and role module in UserModules, each in the file's order (D first, then the listed extras).

## Wire shape
`Configure.Metaflows.[ ConfigureMetaflow ... ]` (meta-signal-flow ethos). Configure replaces the whole Metaflows family atomically: an entry absent from the declaration is removed. One ConfigureMetaflow alone would have deleted the other 24. So all 25 declarations were sent in one input, with every field kept byte-for-byte except the two module lists. (Deviation from "one input per permaflow", forced by that contract.)

Witnesses:
- Sending the unchanged vector first answered `Configured.Unchanged` (syntax and reconstruction proven, nothing written).
- All 50 distinct module names in the order resolve in Curriculum (`ResolveSources`); none unresolved.
- Each of the 23 new lists passed a Curriculum `ComposeStartup` dry run (read-only) for its harness.
- The real input answered `Configured.Replaced`; resending it answered `Configured.Unchanged`.
- Afterwards `Configuration` differs from before only in the 23 entries' module lists and the live Counters.

## Applied (23)
Field core Astra, Field core Sol, Field protos Opus, Field protos Sonnet, Field protosConsumers Sonnet, Field semaV0 Astra, Field semaV0 Opus,
Mind core Astra, Mind core Sol, Mind datomCodec Sol, Mind herdrNexus Sol, Mind beliefNexus Astra, Mind flowNexus Opus, Mind flowNexus Sol, Mind nixCriomos Sol, Mind orchestrate Sol, Mind lojix Sol, Mind versionZero Astra, Mind versionZero Sol,
Psyche core Fable, Psyche core Opus, Psyche core Sonnet, Psyche restart Opus.

Psyche core Opus: Fable's list with intent:opus in place of intent:fable, plus vision:account appended to UserModules.

## Left alone
- Listed "unchanged": Psyche book Haiku, Psyche criomos Opus.
- Addresses in the configuration the order does not list: none. (Mind beliefNexus Sol has a harness profile but no Metaflows declaration, so there was nothing to change.)

## Refused
None. No flow was refreshed, restarted or messaged; no Rust built.
Scratch: tool/plan.py (builds the vector), tool/new.datom (the sent input), tool/plan.json.
