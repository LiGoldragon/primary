# Spirit psyche-vision recovery

Target Codex session: `019fad58-1e10-7051-94bc-6cd6c35e87f7`

## Recovered vision

Spirit is meant to hold a computer representation of the psyche's spirit. The
living spirit itself is never available to an agent; an agent can only infer it,
as it infers psyche vision. Accordingly, content belonging to Spirit is
**spirit**, not **intent**. The word *intent* is to be freed for its ordinary,
distinct meaning: the psyche's intention or what he wants.

One expressly identified part of that spirit is correctness: additional
machinery is justified when the gain in correctness makes later growth simpler
and more natural. The psyche characterized this as more spiritual and more
eternal than ordinary intention.

The immediate desired state in the target session was to bring Spirit back
online **properly and reliably**, through the declarative operating-system
owners, then replay the one queued, psyche-approved capture without changing its
quoted wording. This is restoration of a guarded memory/consultation facility,
not merely making processes green.

The vocabulary port is semantic, not mechanical: rename occurrences that mean
Spirit-content; preserve ordinary uses of intention. Exact workspace doctrine
wording and a routine consultation policy were left for psyche review. Read-only
consultation and approval-gated capture/mutation must remain distinct.

## Direct psyche evidence

### Meaning and boundary of Spirit

In the upstream Claude session named by the target Codex transcript as the
source of the verbatim vision, the psyche said:

> "Spirit is the spirit, actually. The thing that spirit contains is spirit,
> the spirit of the psyche. The psyche's spirit. It's the representation. It's
> the computer representation of the psyche's spirit."

He immediately distinguished representation from the living thing:

> "Vision is a living thing which you don't have access to. So you have to use
> your limited inference ability to try to infer what the vision is, just like
> you have to try to infer what the spirit is."

Context: this statement arose while noticing that Spirit was not being used and
that calling its content "intent" was inappropriate. Provenance:
[Claude transcript, human message](/home/li/.claude/projects/-home-li-primary/0f9d1436-0f9a-4cb0-9c08-60027d8cbc6e.jsonl:450),
timestamp `2026-08-01T11:57:23.430Z`, UUID
`978fc4a9-0481-4b41-8985-b00438b1ef39`.

### Correctness as spirit

In the same message, the psyche said:

> "the gain in correctness more than makes up for the added machinery. And as
> the system expands, this layer of better correctness is going to make the
> expansion much more simple and natural."

The next assistant proposed exact capture and doctrine wording, explicitly as
requests for approval
([context](/home/li/.claude/projects/-home-li-primary/0f9d1436-0f9a-4cb0-9c08-60027d8cbc6e.jsonl:471)).
The psyche replied:

> "Yes, I agree on your wording of that spirit, and also on the renaming of
> everything that touches spirits, what we used to call intent as simply
> spirit, which would resolve the overloading of the word intent, and allow me
> also to reintroduce intent as something more, you know, my intention, what I
> want, and spirit is different than that."

He added:

> "when more correctness is introduced, this is more spiritual, it's more
> something that is eternal, it'll never change."

Provenance:
[Claude transcript, human approval](/home/li/.claude/projects/-home-li-primary/0f9d1436-0f9a-4cb0-9c08-60027d8cbc6e.jsonl:473),
timestamp `2026-08-01T12:13:34.514Z`, UUID
`61d71f1a-a9cb-4d39-addc-cf382ae68587`.

### Restoration character and handover lifecycle

In the target Codex session itself, the psyche requested:

> "assist me in bringing things online properly and in a reliable fashion.
> We'll focus on bringing spirit back online."

He also established that a workspace handover bead holds the actual handover
and is closed when the receiving session acquires it, while goal beads retain
their own lifecycles and live in owning repositories when appropriate.
Provenance:
[Codex transcript, human request](/home/li/.codex/sessions/2026/07/29/rollout-2026-07-29T12-07-41-019fad58-1e10-7051-94bc-6cd6c35e87f7.jsonl:508),
timestamp `2026-08-01T12:22:28.633Z`.

The psyche corrected the source file before the recovery turn proceeded:
`handoffs/spirit-revival-prompt.md` was the intended handoff; the initially
named file was explicitly withdrawn
([Codex transcript](/home/li/.codex/sessions/2026/07/29/rollout-2026-07-29T12-07-41-019fad58-1e10-7051-94bc-6cd6c35e87f7.jsonl:516)).

## Architecture implications, not current-state claims

```text
living psyche spirit
        |
        | inferred, never directly accessed
        v
computer representation held by Spirit
        |
        +--> read-only consultation (desired; exact policy unsettled)
        |
        `--> capture/mutation (guarded and approval-gated)

ordinary intent = what the psyche wants now
spirit          = the more enduring orienting substance
```

The target session's read-only audit reported a deployed shape of
`spirit-judge.service` guarding `spirit-daemon.service`, with the daemon
requiring the judge, typed Unix-socket protocols, and a separate persistent
store. That is implementation evidence, not psyche-authored vision. At the time
of the session, both services were effectively offline because an unmanaged
systemd drop-in overrode the corrected declarative judge unit. The current wire
contract reported there was `Input::Record(RecordRequest)` with success
`Output::RecordAccepted(RecordIdentifier)`; the queued envelope was obsolete.

The central architectural tension exposed by the session was therefore:

```text
enduring, guarded, consultable spirit
                 versus
an unavailable facility whose live state was overridden by unmanaged residue,
whose vocabulary conflated spirit with ordinary intention,
and which agents had ceased consulting
```

## Unresolved ambiguity

- The exact replacement prose for workspace doctrine was not unambiguously
  approved as final text. The conceptual rename was approved; later session
  output correctly kept exact wording behind psyche review.
- Routine Spirit consultation was a proposal, not a mandate. Frequency,
  triggers, returned evidence, and how consultation affects action remain open.
- Each occurrence of `intent` needs semantic classification. Ambiguous cases
  must return to the psyche; a mass rename would exceed the ruling.
- Queue replay must preserve the private approved text byte-for-byte while
  rebuilding only its envelope/metadata against the deployed schema.
- The recovery audit did not know whether normal declarative activation would
  clear systemd's start-limit state; deployment had to prove it without an ad
  hoc repair.
- This recovery establishes the vision as of `2026-08-01`; it does not assert
  that the implementation state reported in that session is still current.

## Provenance and method

The target rollout was read directly from the local Codex session store. Its
embedded handoff explicitly named the Claude transcript above as the source for
the psyche's verbatim Spirit wording, so that transcript was followed as a
first-party provenance link. Repository documents were not used to infer the
vision.

- Codex transcript SHA-256:
  `35fa96d958b53cdc75124d929fb5c4e1182c853cb283184e61e41930c50fbbed`
- Claude transcript SHA-256:
  `896d18027c3a4384636f4dcc792ca34aa116259181b0c69aa3831691f5fb2ff8`
