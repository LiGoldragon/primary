# Skill Edits Round 4

Three directed edits applied to authored skill sources in Curriculum, consumer trees regenerated.

## Edit 1: psyche-distillation.md — distillation sources file

Replaced the sentence "A distilled statement stands on its own words, referring to no beads, files, or flows." with the ruled paragraph establishing the sources file: `Vision/sources/<topic>.md`, one line per reference in the form `e06e4c07 nexus`, appended after every distillation. The path reconstructed from the line resolves to the `archive-` file since distillation archives the source.

The psyche ruled this format on 2026-08-27T16:38:50Z and approved the rest of the proposal with that change.

## Edit 2: nexus.md — nexus domain line

Replaced "One capability, one Nexus. A Nexus is sized to be held whole in one mind — human or model; when it outgrows that, it splits." with: "A Nexus deals with a domain. When its features grow too many, splitting one or more nexuses out of it is considered."

The psyche ruled the original wording too strong on 2026-08-27T15:38:13Z.

## Edit 3: nexus.md — observation by subscription line

Replaced "Observation flows up, authority flows down: state is observed through push subscriptions — a typed snapshot on open, typed deltas after — and commanded through the owner's mutation vocabulary. `Observe.Locks` is a one-shot typed Lock snapshot, not a subscription." with: "State is observed by subscription: the subscriber receives the state on open, then each change as it happens." The sentence "Polling is forbidden; a correct system goes quiet when nothing changes." is unchanged.

The psyche asked for the core idea made dead simple on 2026-08-27T15:38:13Z.

## Verification

- `.claude/skills/psyche-distillation/SKILL.md`: sources-file paragraph present; "carries what the psyche said" line from round 3 still present.
- `.claude/skills/nexus/SKILL.md`: "A Nexus deals with a domain" sentence present; "State is observed by subscription" sentence present; "One capability, one Nexus" and "Observation flows up, authority flows down" sentences absent.

## Sources

- flows/acbb6006/vision/distillation.md — "A sources line is the id and the topic, nothing else" (psyche, 2026-08-27T16:38:50Z)
- flows/acbb6006/vision/nexus.md — "A nexus deals with a domain; when its features grow too many, splitting nexuses out of it is considered" (psyche, 2026-08-27T15:38:13Z)
- flows/acbb6006/vision/nexus.md — "Observation by subscription: make the core idea dead simple" (psyche, 2026-08-27T15:38:13Z)
- Curriculum commit 3bc94e50 (`/git/github.com/LiGoldragon/Curriculum`)
