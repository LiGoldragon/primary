<!-- to-the-living:start -->
Presentation.{ «Flow ids in words, and seats launched by Flow» }

# Flow ids in words, and seats launched by Flow

You asked for the Flow id in words, for sessions named only by aspect and layer, and whether Flow can launch the seats now. Here is what exists, the path I propose, and two choices that need your word.

## What exists today

- **The id.** A flow id is the first six characters of the session's random number, for example `5578cc`. Flow did not choose it.
- **A word converter, unmerged.** A branch of the shared message library turns ids into words from the BIP-39 list: 2048 common English words, each carrying 11 bits. Three words carry 33 bits and are written like `abandonAbilityAble`. Nothing uses it yet.
- **Who launches seats.** A script in Primary launches every seat, me included. It writes the pane title `Psyche.{ Opus 5578cc }`. No running Flow launches seats.
- **Flow on main.** It can launch a Claude seat with hooks that report to Flow. It is built but not deployed, and its sandbox test of a seat in a real pane is being fixed. Codex launching needs its revised route tested first.

## The path I propose

1. Flow names each session by its voice, a real type made of an aspect and a layer, so the pane reads **Psyche Primary**. The voice prints itself; no datom is involved.
2. Flow makes each flow's id itself and writes it in words. The words go into Flow's ledger and the archive, never into the pane title.
3. Once the pane test passes, Claude seats launch through Flow and the script retires. Codex follows when its route passes.
4. Mind Astra designs it, Mind Sol reviews it, and Field builds and deploys it. Switching your machine to it waits for my word after the tests pass.

## Your choices

**1. What the words are.**
- **1a. The words are the id.** Flow picks a random 33-bit number, checks no flow already has it, and writes it as three words. Words and number convert both ways exactly.
- **1b. The words start a fingerprint.** The words are the first 33 bits of a hash of the flow's launch record, the way the unmerged converter works. The words can't be turned back into the record, so Flow's ledger looks them up.

**2. The word list.**
- **2a. BIP-39, three words.** The list already has working code.
- **2b. A denser list first.** You once asked for a list with more bits per word, so two words might be enough. Someone researches it before building.

## On datom

Titles need no datom: a voice can print "Psyche Primary" by itself. The real datom case is a message Flow types into a pane. Today Flow's service links the datom code to write that text, which breaks the rule that a service never handles text. Mind Astra designs how text reaches a pane without that, for example by having a small client write it.

Answer by commenting with the numbers, for example "1a, 2a".
<!-- to-the-living:end -->
