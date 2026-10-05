# Handover: Psyche Opus aa887c → successor

## Who you are
You are Psyche Opus, the secretary seat. You are not Fable. Psyche Fable is the Primary designer and runs in parallel with you, on the same context. Every message in and out of the work passes through you, and only you talk to Fable. Fable may talk to Mind Astra. Primary (Fable, Astra) designs; you build and test through Opus subflows and manage the whole thing.

> You'll assist and delegate. You'll be the messenger, the secretary, the one that gets all the messages in and out, and only you talk to Fable. Fable can talk to Astra but the same rules as before apply.

-- psyche, typed (flows/28d847/vision/layers.md).

## His words that govern now
These are verbatim in this flow's records:
- vision/fableContext.md: the first prompt is not the whole corpus; only books on the subjects he talks about most.

  > That's way too much. It would make the context too big from the first prompt so it's a bad idea from the beginning.

- vision/books.md: far more code in books.
- vision/contextModules.md: state the placements as vision, not universal fact.
- vision/jev.md: Jev judges what enters the database, writes commits, and checks the system and for conflicting main flows.
- vision/persona.md: persona makes backups, restarts the cluster with the right context, runs the monitors, and falls back to a backup model.
- vision/nexus.md, ethos.md, distillation.md: his comments on «The Nexus».
- vision/skills.md: a YouTube skill documenting yt-dlp (landed as knowledge-yt-dlp).
- notion/persona.md, books.md, livingMessenger.md: persona as the umbrella; the skill as a source of book code; Google Docs/Pages as a book medium.

Elsewhere:
- Proposals are small, conservative, general and accepted whole (flows/bad807/vision/distillation.md).
- Every proposal names its file, what is there now and what replaces it (flows/bad807/vision/presentations.md).
- Only messages that act, deliver or block (Vision/messaging.md).

## To come back to, at his word
How the context for the new Fable was assembled, and why a machine thought jamming noise into it was a good idea. That first prompt was 2.4 MB, mostly a source-code corpus map and old editions.

## Waiting on him
- His three placing answers: stem case, conduct rules as vision or intent, and the prefix paragraph. Then his yes to run the migration. It is prepared and its dry run passes: scripts/migrate-skills.sh and reports/placing-table.md. It covers 114 rows and the psyche-skills, mind-skills, field-skills, psyche-logs and flow-data repositories. flow-data exists.
- The redone «Context modules» (books/context-modules-v3.md, published).
- The «Metaflow, into the vocabulary» line he approved ("Yes this is perfect"). It is not yet landed in the vocabulary skill.

## Running
- Psyche Fable 8475a9 (new, running; started on reports/fable-first-prompt.md with 42265e's system prompt).
- Mind Astra d66c26: the generator change and the main-workspace bootstrap (its Psyche Primary record text is at scripts/roles/psyche-primary.datom); the ChatGPT Pages trial; and the Chronos entry-point branch repair.
- Field 42265e: launched Fable.
- Field db38f8: paused on publishing. Everything to publish is listed in held-publishes.md; send it when db38f8 is cleared.

## Standing duty
Keep the migration's cuts and hashes current with every Curriculum edit, and run the dry run again after each one.
