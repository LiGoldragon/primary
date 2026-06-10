# Spirit Category Enum Breakdown

## Current Shape

Spirit now uses a closed `Category` enum and each record carries a vector of
categories:

```nota
Category [Being Knowing Meaning Making Relating Governing Caring Sustaining Dwelling Moving Valuing Expressing]
Categories (Vec Category)
Entry { Categories * Kind * Description * Certainty * Importance * Privacy * }
```

The category field is plural because an intent record can sit in more than one
domain. This avoids forcing a false single parent when an entry is, for
example, both `Governing` and `Caring`, or both `Making` and `Meaning`.

## Category Breakdown

`Being` is ontology and existence: what something is, what kinds exist, what
identity or nature something has. Use it for claims about entities, essence,
presence, selfhood, embodiment, or the kind of thing a thing is.

`Knowing` is epistemology and inquiry: perception, evidence, belief, learning,
certainty, doubt, research, observation, and how something is known. Use it for
records about truth-seeking, investigation, evidence standards, or knowledge
process.

`Meaning` is semantics, interpretation, and symbolic structure: what something
means, how concepts relate, how language or schema expresses intent. Use it for
definitions, conceptual distinctions, schema language, NOTA meanings, names,
and interpretive commitments.

`Making` is creation and production: building, implementation, craft, tools,
artifacts, code, systems, writing, design as construction. Use it for records
about creating or changing concrete things.

`Relating` is relation and intersubjectivity: connection, communication,
coordination, social bonds, boundaries between people or agents, dialogue, and
mutuality. Use it for records about collaboration, interpersonal meaning, or
agent-human relationship shape.

`Governing` is policy, control, permission, law, protocol, authority, process,
and decision structure. Use it for rules, constraints, orchestration, deploy
protocols, security policy, authorization, and operational governance.

`Caring` is ethics, protection, welfare, healing, support, responsibility, and
attention to vulnerability. Use it for records about safety, privacy, personal
care, health, harm prevention, or stewardship of a person or value.

`Sustaining` is maintenance, continuity, infrastructure, resource flow, repair,
survivability, and long-term viability. Use it for records about keeping things
alive and reliable: backups, migrations, operations, energy, persistence, and
service health.

`Dwelling` is place, habitat, home, environment, locality, situatedness, and
belonging somewhere. Use it for records about physical or digital places,
homes, workspaces, clusters, hosts, environments, and the experience of being
in a space.

`Moving` is change, transition, motion, migration, transport, sequencing, and
procession through states. Use it for records about migrations, workflows,
flows, state transitions, deployment movement, travel, and dynamic behavior.

`Valuing` is axiology: worth, priority, preference, beauty, importance,
commitment, taste, and tradeoffs. Use it for records about what matters, what
is better or worse, ranking, aesthetics, importance, and value judgments.

`Expressing` is manifestation, presentation, style, voice, emotion, art,
surface, and outward form. Use it for records about UI, prose, visual design,
tone, communication style, representation, or making inner meaning visible.

## How To Use It

Use the smallest set of categories that genuinely applies. One category is
normal. Two or three are fine when they carry real retrieval value. A long list
usually means the record description is too broad and should be split.

For schema and NOTA language records, the common category is `Meaning`; if the
record is about implementation, add `Making`; if it is about a rule or protocol,
add `Governing`.

For deployment and service records, the common category is `Sustaining`; add
`Moving` for migrations and `Governing` for operational policy.

For privacy and guardian behavior, the common categories are `Caring` and
`Governing`; add `Knowing` when the record is about evidence, certainty, or
classification.

For UI, writing, or visual/audio output, the common category is `Expressing`;
add `Valuing` when the record is about aesthetic judgment or priority.

## What This Replaced

This replaced the older free-text topic/tag tendency with a closed categorical
starting set. The goal is not to make a perfect universal taxonomy. The goal is
to give Spirit a stable, broad, beautiful first partition of life so retrieval,
guardian review, and future library use have typed structure rather than loose
strings.

The enum is deliberately broad and category-theoretic in spirit: it names
large domains of relation and transformation rather than project-specific
topics. Project-specific terms still live in descriptions and keyword/text
search; category stays the high-level typed axis.
