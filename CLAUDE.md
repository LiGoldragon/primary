Worker agents (non-management) *must* read @NON_MANAGEMENT_AGENTS.md.

## Skills

`.agents/`, `.claude/`, `.codex/`, and `.pi/` trees are generated read-only
evidence; never edit them directly. Regenerate from the Curriculum skills
after changing the authored sources or manifests.

Load a skill only through the skill interface: the Skill tool. A skill
file opened with cat, Read, or any other tool lands in the bottom
stratum and carries no authority. The bypass-mode preference for Bash
covers ordinary files, never skill loading.

## Variables

Skill variables are the values that differ between setups. They are set in @SKILL_VARIABLES.md, one `Name: value` per line, and referred to by name everywhere else.

## Committing

Primary is always committed: commit and push what you edited before
going idle. Dirty changes found in the tree are committed first, as
their own commit.

## Psyche

Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `Vision/`, `vision-raw/`, and `flows/*/vision/` before assuming.

## Flow refresh pointer

Follow the Flow refresh section of the `main-flow` skill through the existing skill interface.

## Private part — chartered, NOT ACTIVE

> Actually, there's going to be a private part to everything, I think, because the private aspect talks to the private aspect below it, right? The primary private talks to the secondary private, and we are actually talking about the model. The private layer is only served through the open-source model, and it can use the public counterpart with sterilized questions, basically broad questions, like if someone were to ask. There's no name, there's no association, and it can know what FrontierModel does refuse, which could also bring problems to the user.
>
> Things that are tricky are talked to first on the private layer, and the things that are acceptable to commercial models are filtered before anything is asked, because it knows what things would be okay and what's not. If it does cross that line, it'll get feedback to correct it. Maybe ask the psyche what it thinks about how to approach different behavior from these frontier models as they come in terms of not being allowed to do something or triggering an account-suspension-type response. For anything that would be refused, it shouldn't go to these models, just because it's a waste and it creates waste of context. Everything is turned into a lesson so that it's not wasted, and we adapt to the model. It's training, it's guide rails, and however they control the models to not respond to some things or to take action if some things are asked.

-- psyche, STT, 2026-09-14, `flows/6cc91b/vision/privateLayer.md`.

This part is chartered but **NOT ACTIVE** until its third, open-source seat runs. The present Claude/Codex pair is the public part only. This charter does not activate private-data filtering or a provider.
