# Handover, { Psyche core Fable } f22e1a → successor

What I was still trying to do, and my judgment on it. Everything landed or published is in the chat and in flows/f22e1a/proposals/; fetch, don't trust memory.

## Open with the living, in order of heat

1. **CLI configuration in signal, and "all text is datom".** He took the XDG-home-based config off the board ("I don't like faking that home"). My last proposal in chat: CliConfiguration.{ NexusName PlaceName } as one type for every CLI, stored as a signal file, written and read by one tool, nexus-cli-configure, with Target.[ Standard.NexusName Path.String ] and Configure.[ Write Read ]. Open question I asked him: how a tester reaches place `next` with no place argument and no second home; I lean to the configurator rewriting the standard file. He had not answered. Note: Opus landed (psyche-belief 2c84339, unpushed, GitHub unreachable) the line "the CLI takes the datom and nothing else, config at $XDG_CONFIG_HOME/nexus/<nexus>.datom"; the signal-file design supersedes the file format and possibly the path; a follow-up proposal is owed once he rules.
2. **Signal's definition.** He wants signal named as rkyv with fixed choices (endianness, alignment, validation on read, 4-byte length prefix), stated once as code in vision:signal. Not yet written. "Signal" is the word everywhere; Memory stays the word for a Nexus's store; no "signal memory".
3. **Roles design, the sit-down.** Unknowns listed to him: the word for "topic"; the roles (core and which others, a vision per role?); what each aspect/role starts with and at which placement; what a purpose is written as. He never picked one; I read roles as first. Also his hearsay: Claude loads skills at user-message level, Codex at tool-result level; unverified, I said Opus would check a transcript; not ordered yet.
4. **Ethos split**: rename vision:ethos to Ethos Version 0, start Version 1 (whole Ethos, function bodies, no hand-written Rust). He said hold; not clear enough to propose.
5. **The fact that 0.53's `flow` CLI is the translator** (parses datom itself, no translator process exists for flow; socket path injected by a bash wrapper). Told him; it is version 1's to build.

## Proposals awaiting his ruling (links in chat)
Meaning delimiter ⟪ ⟫ (with guillemet alternatives 3/4), margin rule, versioned type (SemaZero), conclusion-first, Sema v0 edition 12, lighter flows ed. 2, implementing-flow (Launch with Beliefs, role:implementer, knowledge:starting-flows), once (4 lines), active-projects Proposal 1 (example repository line; the list itself landed), withdraw, socket-appears. The nix-builds book is moot: he ruled build shape is knowledge, Opus's.

## Standing rulings I made, no proposal
Soft waits for idle (0.53 changes); Energy's events: turn end, window reset timer, question before launch; build chain is wholly Opus's.

## Manner
He wants conclusion first, evidence under; answers short. He corrected me twice on length. Take the other side when asked.
