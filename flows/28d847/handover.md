# Handover: Psyche Opus 28d847 → successor

## Your first work, his order of 2026-10-04 (verbatim in vision/skills.md and vision/workspace.md)
Restart on the three skill repositories psyche-skills, mind-skills and field-skills: migrate all vision (Vision/, and the unprefixed skills that imply psyche) into them, merged with the current skills, each statement split to its right home across psyche, mind and field. Bootstrap a new workspace named main workspace (not primary: that word is a layer), with Mind Astra, and implement the better workspace design on that new repository. Inputs: reports/skill-kinds.md (69 skills by kind), reports/distill/merged-1.md and the book «Distilled vision for your approval» (54 entries awaiting his comments), curriculum-deploy 0.9.0 (generates from declared psyche/mind/field sources, byte-identical), the three repositories (README only; layout undecided).

You are the Psyche Opus seat (Secondary). The living's latest words on your role (verbatim in vision/layers.md): you are the secretary — every message in and out of the work passes through you, and only you talk to Fable; Fable may talk to Astra. Primary (Fable, Astra) designs and passes down; you implement and test through Opus subflows and manage the whole thing.

## His words that govern now
Recorded verbatim in this flow's vision/: publishing (one Field flow publishes for all), infrastructure (code does mechanical work; models judge), skills (three repositories psyche/mind/field; vision distillation writes skills; small skill-edit proposals), subflows (tailor-made subflows, never skills named in briefs), curriculum (workspace edits regenerate per harness), books (a maintained series of vision books; presentations show high-level code and ethos/datom), quotas (one call; time left; use per time), layers (Primary designs, Secondary builds; Quaternary Sonnet low / Luna low; secretary seat), nexus (a standard entry point enforcing signal → operation → memory → operation → signal).

## Running now
- Field Sonnet db38f8 holds the Primary publish lock permanently and publishes any paths a flow messages it; its procedure is briefs/publisher-procedure.md. Publish only through it.
- Psyche Fable bad807 (Primary): context-module standard (redone book with exact targets), deep distillation of Ethos, datom and the nexus. It speaks to other flows only through you; you relay its publish requests to db38f8 (db38f8 accepts your relay as its word).
- Mind Astra dea0ba: Flow context-build contract (flows/dea0ba/reports/context-build-contract.md); by Fable's ruling all six increments are built and tested by you, starting once increment 1's authored Ethos roots exist.
- Mind Astra d66c26: quota snapshot designer; the snapshot is accepted and live (harness-usage).
- Field 42265e: deploys (Lojix); owns knowledge-layer-models (landed, deployed).
- Mind 41fa34: reviewer.

## Landed today
harness-usage (one-call quotas and context, installed); curriculum-deploy 0.9.0 (declared psyche/mind/field sources; OpenCode tree); Primary on Curriculum main (70 skills incl. knowledge-layer-models); hm-retire takes only a flow id (deployed); OpenCode third harness on Ouranos with a local model, flow-id opencode form (deployed); book skill: drawings are SVG, never Mermaid.

## Waiting on him
- The operation-book line: every proposal names its file, quotes what is there now, shows the proposed text, vision marked apart; explanation labelled as such.
- The 54 distillation entries (book «Distilled vision for your approval»); entries 52 and 54 touch Intent.
- His proposed design for order messages (hm-send --order): whether tracked until done, handed on intact, who may mark one.
- Names for the skill kinds (operation, compensation) and for the whole set of context modules.
- OpenCode model: hosted Kimi K3 or DeepSeek through keys already held, or the slow local model (deployed on Ouranos with local Qwen3.6-35B-A3B).
- Which skills go to psyche, mind, field (reports/skill-kinds.md), and the layout inside each repository.
- The commit-skill line: never a work tree or second checkout; on push conflict resolve in place or stop and report.
- Whether db38f8 publishes from its own clone (a rule now on Curriculum main says so) or the shared copy.
- Quota planning: a declared plan of his quota hours; how unattended hours count.
- The presentations line for the book skill (proposed in the last turn).
- His ruling on Fable's Ethos book, gating ethos-zero fixes (one-field structs accepted, Name.String an alias, comments dropped).
- The checks book republished concretely (reports/checks-concrete.md is written; not yet booked).

## Open issues
primary-rkr (new user services don't start on Home activation), primary-b6s, primary-vnd, primary-ptw (quota follow-ups). Primary's working copy holds many unpublished changes of other flows; they should send them to db38f8. A permission prompt marks a seat blocked and the messenger then holds every message to it.

## Landed since
Claude PermissionRequest hook denying the dangerous-removal prompt with his approved message (deployed); the app-used Codex home never asks (deployed); hm-retire takes one argument (deployed); launcher takes --system-prompt-file and --effort; Fable bad807 launched; standard Nix home setup for Claude and Codex is his vision (vision/harness.md; reports/harness-settings.md is the inventory).
