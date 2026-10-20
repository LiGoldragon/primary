# Chronos handoff to Mind Prototyping (5b9075, secretary e4b7d7)

## Authored sources (this flow, 984e88)
- Second edition source, exact Ethos anatomy in its Proposal 2: /home/li/primary/flows/984e88/books/02-chronos.md
  Published: https://claude.ai/artifact/Fd1jGBnf2dcfkrSRShrE6w
- Reference (unrendered: source facts, crate findings, provenance): /home/li/primary/flows/984e88/books/references/02-chronos.md
- First edition, carrying the living's two comments on Proposal 2: books/01-chronos.md, https://claude.ai/artifact/RJms6NubV4g3Q1famexYkZ
- Living's raw words: vision/chronos.md, vision/ethos.md
- Held Fable head-start: head-start.md (1989 chars), head-start-provenance.md

## Confirmed by the living (his book comments, relayed by Psyche Core Secondary 2026-10-14)
- Sign and nakṣatra are not stored; they are derived from an arc, absolute or relative (a 31° Sun–Moon arc reads as Taurus).
- Coordinates are not Decimal; types are imported from Rust through a hand-maintained, specified vector the Ethos-to-Rust compiler links against.
- The tropical frame, with 0° Aries = Aśvinī 0, is his own description (raw vision, not crystallized).
- "Glanced and selected for a prototype": relayed to this flow by you; not witnessed here.

## Proposals, not ruled
- Proposal 1: the vision-chronos module (crystallization; not approved).
- Proposal 2: the anatomy, as drafted.
- Proposal 3: the vision-ethos line for the imported-types vector (not approved).
- Proposal 4: the vector entry shape (Ethos name, Rust path, rkyv adapter) in ethos-zero/imports.datom.
- Choices 5–14, defaults in brackets, none ruled:
  - 5 angle type [num-rational Rational64]
  - 6 arc written as [43/2]
  - 7 derivation by [trait methods only]
  - 8 solar/lunar formats [Sun's arc and lunation]
  - 9 nodes/apogee [true]
  - 10 location [request, else meta standing]
  - 11 Memory [no watcher record]
  - 12 ephemeris [DE440]
  - 13 aphelion [LunarApogee, SolarApogee]
  - 14 "everything is tropical" in [vision-chronos only]

## Current observations (read-only subflow, 2026-10-14; not rebuilt or re-witnessed since)
- /git/github.com/LiGoldragon/chronos at 500094596de495b81cf32b35e127905e7ab0fc42, v0.3.0.
- Rust, with .ethos/data/chronos.ethos. Only SetLocation and GetLocation work: rkyv over a Unix socket into redb.
- All astronomy is todo!(); no moon, nodes or nakṣatras. anise and solar-positioning are listed but unused.
- No crate chronos depends on has an angle type. num-rational is in its lock as a transitive dependency, and no candidate crate supports rkyv.

## Ownership and locks
- This flow holds no Orchestrate lock and wrote nothing in the chronos repository; no implementation is underway from here.
- Earlier unmerged Chronos branch experiments are claims in other flows' logs (d66c26, bad807), not witnessed here.
- Owners of the chronos repository: not established by this flow.
