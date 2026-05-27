# 396 — Nexus mail-keeper consolidation manifestation: record 970 + cloud branch

*Kind: Synthesis · Topics: nexus, mail-keeper, runtime, signal, sema, cloud · 2026-05-27*

*Follow-up manifestation pass for intent record 970 (Maximum,
2026-05-27) which CONSOLIDATES records 935 + 963 + 964 + 965 into
one unified runtime picture: Nexus is the MAIL KEEPER +
Signal-to-SEMA translator; the daemon has THREE EXECUTION CENTERS
(Signal / Nexus / SEMA); complete flow Signal IN → Nexus accepts
mail (BEING-PROCESSED) → SEMA query → SEMA reply with database
marker → Nexus translates → Signal OUT. Also addresses the cloud
INTENT.md skip from report /395 by creating the missing
`designer-intent-manifestation-2026-05-27` branch on cloud.*

## Workspace files updated

| Path | Commit | Substance |
|---|---|---|
| `/home/li/primary/INTENT.md` + `/home/li/primary/skills/component-triad.md` | `wllrmppm 8f57f71f` | New §"Nexus is the MAIL KEEPER — runtime flow consolidation" added to INTENT.md's three-schema-types section with the consolidation framing + complete flow diagram. component-triad.md retitled the Nexus subsection, named the three execution centers, updated the flow to the consolidated form, and reworked the table to show "execution center" terminology. |
| `reports/designer/390-wire-runtime-canonical-direction.md` + `/392-vision-schema-driven-stack-canonical-2026-05-27.md` + `/395-runtime-nexus-signal-sema-triad-manifestation-2026-05-27.md` | `zxzmszvv ba25d1d0` | /390's frame extended with record 970 + a new §"Consolidation — Nexus is the MAIL KEEPER" with mermaid diagram. /392's runtime-triad section gets a record 970 paragraph + flow diagram + source-records table entry. /395 gets a status banner pointing forward to this report. |

## Per-repo branches updated

All commits ON TOP of existing `designer-intent-manifestation-2026-05-27` branches (per the "don't rewrite history" instruction).

| Repo | Commit | What landed |
|---|---|---|
| `signal-frame` | `qwvxkyrz f84be394` | INTENT.md adds §"Nexus is the MAIL KEEPER — signal-frame is the wire side"; ARCHITECTURE.md extends the three-runtime-planes section with the record 970 three-execution-centers framing — signal-frame sits on Signal center. |
| `signal-spirit` | `yoqxprtz 431cad41` | INTENT.md adds §"Nexus is the MAIL KEEPER — signal-spirit sits on the Signal center"; ARCHITECTURE.md §5d gets a "Three execution centers" subsection. |
| `core-signal-spirit` | `zumomvsz b0b4111b` | Same shape as signal-spirit, with daemon-side privileged-channel trust enforcement noted. |
| `spirit` | `qrvysvxu 180d1298` | INTENT.md adds §"Nexus is the MAIL KEEPER — three execution centers"; ARCHITECTURE.md §8c gets a Nexus-mail-keeper subsection with the complete flow. |
| `spirit-next` | `zqnszlom ad10dd4c` | INTENT.md adds §"Nexus is the MAIL KEEPER — three execution centers" between signal-protocol and continuous-manifestation; ARCHITECTURE.md retitles the Nexus section to "Nexus (renamed from Executor per record 964; MAIL KEEPER per record 970)" with detailed flow paragraph. |
| `schema-next` | `loplxvnr 30e19d25` | INTENT.md adds §"Three schema types ↔ three execution centers" subsection. |
| `schema-rust-next` | `yzzozlmx fe84123d` | INTENT.md adds a paragraph naming the per-plane emission surfaces (NexusMail, on_sent hook surface, database-marker reply layer). |
| `nota-next` | `uxyoqzmt b4bf86b1` | INTENT.md adds a paragraph reaffirming NOTA's position below the three execution centers. |

## Cloud branch CREATED (yes — closing the /395 skip)

| Action | Result |
|---|---|
| Worktree created | `/home/li/wt/github.com/LiGoldragon/cloud/designer-intent-manifestation-2026-05-27` (via `jj workspace add`) |
| Branch created | `designer-intent-manifestation-2026-05-27` at commit `ommnxurm db211e89` |
| Commit | `INTENT (new) + ARCHITECTURE: cloud as Nexus-IO component; three execution centers (records 965 + 970)` |
| INTENT.md | NEW file — full goals / constraints / principles synthesised from cloud-topic spirit records (281-296, 325, 342, 679-689); large §"Cloud is a Nexus-IO component (record 965)" + §"Nexus is the MAIL KEEPER — cloud-daemon flow (record 970)" with the cloud-specific flarectl flow. |
| ARCHITECTURE.md | NEW §"Cloud is a Nexus-IO component (records 965 + 970)" — three-execution-center table mapping cloud's signal-cloud/owner-signal-cloud to Signal, flarectl shell-outs to Nexus mail keeper, accounts/plans/cache to SEMA. |
| Push | `jj git push --bookmark designer-intent-manifestation-2026-05-27 --allow-new` — successful. |

## Skills updated

`skills/component-triad.md` — runtime-triad subsections refined. The
top of §"Runtime triad" now names the **three execution centers**
explicitly. The Nexus subsection retitled to "execution — IO,
external calls, UI, mail keeper, translator" with record 970's
consolidation framing, basic-Nexus-actions vocabulary
(submit-query, get-reply), and the on_sent / database-marker
mechanics. The flow subsection rewritten to record 970's complete
shape (Signal IN → Nexus accepts → SEMA query → SEMA reply with
database marker → Nexus translates → Signal OUT).

## Surprises and open questions

1. **Cloud's INTENT.md was created from scratch** because cloud
   had no INTENT.md at all (not just a missing branch). The new
   file synthesises ~14 cloud-topic spirit records (281, 282,
   283, 284, 294, 295, 296, 325, 342, 679-689) into goals /
   constraints / principles / anti-patterns alongside the
   nexus-IO framing. This may have surprises if other
   designer/operator agents reach cloud with different
   expectations; the file is 100% backed by recorded psyche
   intent.
2. **mencie repo still does not exist** (per `ls /git/github.com/LiGoldragon/ | grep mencie` — no match). Record 970 reinforces records 965's mencie-as-nexus framing; landing is still pending mencie repo creation.
3. **File-extension question still open** per record 964; record 970 does not close it. Captures preserve the openness across all branches.
4. **ESSENCE.md still not edited.** Record 970 is Maximum-certainty and now CONSOLIDATES four earlier records (935/963/964/965). The three-execution-centers framing has graduated from a refinement to the load-bearing runtime architecture vocabulary — this may warrant essence-tier promotion. Per `skills/intent-manifestation.md`, ESSENCE promotion is the psyche's call. Flagged for psyche review.
5. **/395's status banner now points forward to this report (/396).** If /395 is later retired or renumbered, /396 should pick up its role as the canonical Nexus/Signal/SEMA manifestation report (with /395 as an intermediate step that gap-filled records 963-965 before 970 consolidated).
6. **Verbatim-quoting convention applied** in the new cloud INTENT.md and the consolidation section additions per `skills/intent-manifestation.md` §"The verbatim-quoting convention" — markdown italics for inline psyche quotes, blockquote-with-italics for multi-paragraph verbatim.
