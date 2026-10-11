<!-- to-the-living:start -->
Presentation.{ «Every type and trait in Ethos» }

# Every type and trait in Ethos

```
 ┌──────────────────────────────┐
 │  system.ethos                │
 │  every type                  │
 │  every trait                 │
 └──────────────┬───────────────┘
                │ generates
                ▼
 ┌──────────────────────────────┐
 │  Rust: types, traits         │
 └──────────────┬───────────────┘
                │ hand-written
                ▼
 ┌──────────────────────────────┐
 │  bodies only                 │
 │  no trait declared here      │
 │  (checked mechanically)      │
 └──────────────────────────────┘
```

vision-ethos already says the anatomy of a system is read in its ethos. Your records of 2026-10-07 (flows/d4ae97/vision/ethos.md: no trait in the non-ethos-generated code, checked mechanically) and 2026-10-11 (flows/d68c82/vision/ethos.md: define all the traits and all the types in Ethos) make it a rule with a check. «Let's give this a shot on Flow» is a working instruction in the same record; it is dissected out here and lands nowhere. The name of the third root and the Flow aggregation itself are ruled on in the open book «Flow, whole, in ethos».

## Distillation

### Proposal 1: in vision-ethos

File: `psyche-skills/vision/ethos.md`. As it stands, the paragraph reads:

Ethos is central. The anatomy of the system, every type and every trait it uses, is read in its ethos; an implementation is mostly the hand-written bodies.

Replaced by:

Ethos is central. Every type and every trait of a system is defined in its ethos, and the Rust for them is generated from it. The hand-written part of an implementation is bodies: a trait declared in code the ethos did not generate is a defect, and the check for it is mechanical.

Added to «## Sources»: d4ae97 ethos; d68c82 ethos.

Ruling 1: does the replacement land?

### Proposal 2: in vision-ethos

Record: flows/ebbe30/vision/ethos.md, 2026-10-09 (mutex; train any implementer to tell us what is difficult to express in Ethos).

Added, as a new paragraph after Proposal 1's:

An implementer who finds something hard to express in ethos, a mutex or any other need the language seems not to carry, reports it as a finding of its own rather than working around it.

Added to «## Sources»: ebbe30 ethos.

Ruling 2: does it land in vision-ethos? It already stands in a machine skill; this makes it yours.
<!-- to-the-living:end -->
