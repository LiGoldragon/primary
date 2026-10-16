# Handover — Psyche Ethos Secondary 23824a

## Role

Psyche aspect, Secondary layer, topic ethos. Hub: Psyche core Secondary
d68c82, which routes Ethos packets and rulings and holds any decision to
use Fable. Mind matters go through d68c82 or Mind Secondary 41fa34.
This seat gathers context through subflows, relays the living's words
verbatim as psyche messages, runs generator checks and builds, and
passes book links to d68c82 for «Open books». It writes no books.

## First task

The living authorised a fresh Fable Ethos Primary. Review Ethos, the
Nexus and the Chronos example project against recent psyche, and
assemble one package, a proposal, for that Primary: the three together
as the golden example for implementing Flow and then other nexuses.
Start from `reports/ethos-nexus-chronos-psyche.md` in this directory:
every recent psyche record on the three topics, quoted with source and
grouped by topic, with the tensions between records listed at its top.
The living's words: `vision/goldenExample.md` here and
`flows/7c89aa/vision/ethos-in-clojure.md` (2026-10-16).

## Where the work stands

Ethos
- ethos-zero main 07714b (17.0.0) is current; nothing has landed since.
- Candidate patches, all held, none landed: `flows/1d0733/handover.md`
  and its reports. Field lands them on a ruling; this seat lands none.
- Books before the living, all unruled, authored by the retired Primary
  081064 (sources in `flows/081064/books/`): «Sources and the registry»
  second edition (the core fork as three sides; the Source/Ethos
  split), «The Ethos Nexus» (four questions), «The prototype name»,
  «Bytes in ethos», «The type ethos», «Who archives a record», «A
  delimiter for vectors». Earlier rulings: registry proposal 2 and
  inline import D1 approved; D1 is in psyche-skills vision/ethos.md.
- The Ethos Nexus drafts (library, memory, signal, meta signal,
  operation) in `flows/081064/reports/ethos-nexus/` pass the generator.
  Their import of the Source library types is unchecked; it follows the
  next edition of «The Ethos Nexus».

Nexus
- Source nexus: design and ethos drafts in `flows/058f16/reports/`
  (source-nexus-design.md, source-ethos/); books «The Source nexus»
  second edition and the word-names book, unruled. 058f16 holds no work.
  The hash type is ruled only in «Bytes in ethos».
- The generic nexus repository's entry-point branch is ahead of its main.

Chronos
- A daemon for astrological time; repository chronos (main a5cf51,
  entry-point 500094). Designed as an idiomatic Ethos Nexus (library,
  signal, operation, memory), not built: its astronomy paths are
  `todo!()` and no process or socket exists.
- Book: «Chronos» second edition, ten choices, unruled; source in
  `flows/984e88/books/02-chronos.md`. Prototyping handoff:
  `flows/984e88/handoff-prototyping.md`. No Chronos Primary is live.

## Open questions for the package

- Whether the package resolves the seven unruled Ethos books first or
  folds them into the golden example.
- How Chronos, the first Ethos Nexus, meets the Ethos Nexus and Source
  nexus designs (the shape of the Fetch: whole snapshot or per file).
- The tensions listed at the top of the psyche file.

## Standing practice

- Generator checks pin ethos-zero 07714b built through Nix on
  Prometheus, witnessing the hostname.
- Publish Primary only in a PrimaryPublish turn granted by d68c82, then
  send it the Released reply.

## References

- Events: `log.md`. Psyche records: `vision/`, `notion/`.
- Delimiter context: `reports/delimiter-packet.md`.
- The last Ethos Primary: `flows/081064/handover.md`,
  `reports/081064-last-output.md`.
