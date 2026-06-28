---
name: skill-editor
description: 'Rules for pruning and editing skill files so they stay short, self-contained, settled, and operational.'
---

# Skill — skill editor

## Compression

- Keep only operational discipline that changes how an agent acts.
- Prefer 40-80 lines; stay below 120 unless every extra line prevents real misuse.
- Delete explanations of what skills are, how agents use them, and how markdown works.
- Each heading, paragraph, and bullet must carry a rule or necessary exception.
- Keep at most one compact example, only when prose alone leaves a likely mistake.
- Remove wrong/right galleries, generic manuals, motivational prose, and obvious filler.

## Scope

- One skill teaches one capability.
- Split unrelated disciplines instead of making one file a handbook.
- Keep workspace skills cross-repo and operational, not component design notes.
- Repo-specific skills are deprecated; do not create or expand them.
- Put durable repo guidance in AGENTS.md, ARCHITECTURE.md, or README.md, ordered from more agentic to less agentic.
- Do not duplicate universal workspace contracts or language manuals.

## Self-containment

- State the rule directly.
- Do not send readers elsewhere for authority, context, evidence, history, or status.
- Do not cite logs, chats, audits, or proposals.
- Do not mention local filesystem locations.
- Do not include cross-reference sections.
- Keep source and generator mechanics as editing instructions, not banners or changelog text.

## Form

- Use present-tense imperative prose.
- Describe what is true or required, not what changed.
- Prefer the positive canonical shape; name failures only to prevent immediate misuse.
- Keep a rule's reason only when the reason changes decisions.
- Put browsing trigger and identity in file metadata; keep the body rule-only.
- Avoid decorative structure, templates, and tutorial scaffolding.

## Source and active copies

- A skill may be generated from a source repo; when source exists, edit source first, then refresh active copies.
- If direct runtime edits are required, keep all active copies byte-identical and mirror the change back to source.
- Touch only this skill's metadata when updating generated copies by hand.

## Finish sweep

- Search for external references, local paths, broad tutorials, filler, history language, duplicate rules, and unrelated material.
- Delete questionable material instead of preserving it by default.
- Return any excluded material that may deserve explicit re-introduction as a question.
