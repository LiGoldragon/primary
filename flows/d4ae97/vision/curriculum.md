# Curriculum

## Curriculum holds the Nexus; three repositories hold the skills
Context: ordering a new Mind Astra flow to fix the curriculum deploy.

> So the curriculum: let's get Astra to fix this. Start a new Astra flow to fix the fucking curriculum deploy so that it has a memory registry of all of the skills in the three different repos. There are three repos not curriculum. Actually the repo curriculum should hold the curriculum nexus and no skill at all.

> The curriculum repo is going to be the Rust code only: only the Rust code, the CLI, and the Nexus. There are going to be three repos, namely psyche, mind, and field, each of which will have a skill directory. They're just going to be called by the type: intent and spirit, and field is going to be trial and compensation and so on. The skills will live there in these repos and the curriculum nexus will have its memory registry populated with these registry editing messages, which can contain a vector of new entries and/or a vector of edits (to say that a certain skill has been removed) and the paths to the act [sic].

-- psyche, STT, 2026-10-07.

## Dirty first: skills by path, regenerated from the Nexus's memory
> We're going to make this really dirty just so that it works. Right now we're going to use the path of the skill where it is and then the curriculum will be used to regenerate all the skills in the workspace using its own memory of where all the skills are.
>
> There's going to be a signal saying:
> - such and such skills changed
> - here's the vector of the names of the skills that have changed
> - here's a vector of the new skills
> - here's a vector of the deleted skills
>
> It's going to use that to regenerate the workspace: delete the skills that have been deleted, add the skills that have been added, and rewrite the skills that have been edited. That's it. It's going to be really simple, okay? There's not going to be any skill in the rest [sic] repository.

-- psyche, STT, 2026-10-07.

## The new flow gets every instruction, the newest with most authority
> Astra, a new Astra flow is going to be given all the instructions I've ever given, with more recent instructions having more authority, okay? You're going to use the subflow to put all of this together and start a brand new Astra, which means killing the old one, okay?

-- psyche, STT, 2026-10-07.

## Curriculum is a harness-independent abstraction for skills
> The workup [sic] curriculum is to assemble the skills in the workplace [workspace], as I understand it, after the templates, and to get the codex-only parts. It is to figure out how to deploy so that agents see or don't see certain skills, depending on which harness, and each has its own facility for that. We're basically creating a unified abstraction for skills that is harness-independent. That's the way I see it.

-- psyche, STT, 2026-10-07. Transcription corrected: "workplace" → "workspace".

## Curriculum's ethos is unreadable
Context: comment on `String` in curriculum.ethos.

> Wow, string, string, string, string, string. Am I supposed to know what any of this is? This is so fucking retarded. I don't understand any of this. Roll packet plan. What is this curriculum? This makes no sense to me. ... We have a lot of correction to do here, eh? This is garbage. What the hell happened?

-- psyche, comment on «Curriculum's ethos, and every Nexus's three roots» (https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU), 2026-10-07. Transcription kept: "Roll packet plan" is RolePacketPlan.
