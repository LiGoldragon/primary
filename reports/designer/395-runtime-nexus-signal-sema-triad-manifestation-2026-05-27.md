# 395 — Runtime triad refinement manifestation: Signal / Nexus / SEMA

*Kind: Synthesis · Topics: runtime, nexus, signal, sema, schema · 2026-05-27*

*Manifestation pass for intent records 963 (signal protocol named; universal mail mechanism with hookable lifecycle events), 964 (three schema types — Signal / Nexus / SEMA — corresponding to three runtime planes; Executor renamed to Nexus), and 965 (Nexus covers IO + external calls + ALL user interfaces; Mencie implemented as nexus schemas; supersedes record 880's scope-restriction). Per record 944's continuous-manifestation discipline.*

> **Follow-up consolidation** — Record 970 (Maximum, 2026-05-27)
> CONSOLIDATES records 935 + 963 + 964 + 965 into one unified
> picture: **Nexus is the MAIL KEEPER + Signal-to-SEMA translator**;
> the daemon has THREE EXECUTION CENTERS (Signal / Nexus / SEMA);
> complete flow Signal IN → Nexus accepts mail (BEING-PROCESSED) →
> SEMA query → SEMA reply with database marker → Nexus translates →
> Signal OUT. UI / external-IO uses of Nexus from 965 are specific
> instances of the more fundamental in-between translator role. The
> follow-up manifestation lands in
> `reports/designer/396-nexus-mail-keeper-consolidation-2026-05-27.md`.

## Workspace files updated

| Path | Commit | Substance |
|---|---|---|
| `/home/li/primary/INTENT.md` + `/home/li/primary/skills/component-triad.md` | `yuptzsyr 8a99a2af` | New §"Three schema types, three runtime planes" + §"Signal protocol — universal mail mechanism" in INTENT.md; component-triad's runtime-triad section rewritten as Signal / Nexus / SEMA with the three planes' schema-driven framing. |
| `reports/designer/371-…runtime-triad-and-federation-2026-05-26.md` + `/390-wire-runtime-canonical-direction.md` + `/392-vision-schema-driven-stack-canonical-2026-05-27.md` | `ytyyyxuz 64d993ef` | /371 carries a status banner noting record 964 renames Executor→Nexus and pointing forward to /392 + skill; /390 adds nexus naming to the topics + frame, mentions signal protocol name; /392's vision adds three-schema-types triad subsection, signal-protocol naming in the wire-stack section, and records 963/964/965 in the source-records table. |

## Per-repo branches updated

All on existing `designer-intent-manifestation-2026-05-27` feature branches (per record 944's continuous-manifestation discipline; per the instruction, no new branches).

| Repo | Commit | What landed |
|---|---|---|
| `schema-next` | `vsyxwzrr e966aaa7` | New §"Three schema types — Signal, Nexus, Sema" in INTENT.md (verbatim records 964 + 965); ARCHITECTURE.md adds parallel section naming schema-next as the shared substrate for all three schema types. |
| `schema-rust-next` | `oyykrvto 46420f9b` | INTENT.md + ARCHITECTURE.md both extended: this crate emits Rust for all three schema types (Signal / Nexus / Sema); file extensions remain open. |
| `signal-frame` | `xzyvrntl 41d0dfe1` | INTENT.md adds signal-protocol + mail-mechanism + Signal-is-one-of-three-schema-types sections; ARCHITECTURE.md adds parallel sections at the top under TL;DR. |
| `signal-spirit` | `pwrkpwqx 2253e618` | INTENT.md + ARCHITECTURE.md: signal-spirit is a Signal schema (one of the three types); root-type framing; mail-mechanism live in daemon. |
| `core-signal-spirit` | `wwrztqkk 3770831c` | INTENT.md + ARCHITECTURE.md: core-signal-spirit is the privileged Signal schema; same mail-mechanism with daemon-side trust enforcement. |
| `nota-next` | `qlmlpkox 6d7142e9` | INTENT.md adds §"NOTA is below the three schema types" — NOTA is the universal substrate underneath all three schema-type documents; §"Continuous manifestation" added (was missing). |
| `spirit-next` | `rnksotqx b8f445ba` | INTENT.md adds three-schema-driven-planes section + signal-protocol section; ARCHITECTURE.md's runtime-triad section retitled Signal / Nexus / SEMA with Executor→Nexus renamed; Signal section gets record 963 mail-mechanism paragraph. |
| `spirit` | `xnroplrq b2a6037b` | INTENT.md adds three-schema-driven-planes section + signal-protocol section before continuous-manifestation; ARCHITECTURE.md's §8a (mail manager) extended with record 963 + new §8c on the three planes. |

## Skills updated

`skills/component-triad.md` — runtime-triad section rewritten end-to-end. Each plane now has its own subsection (Signal / Nexus / SEMA), Executor naming retired, the schema-type ↔ plane mapping is at the top of the section, and the record 965 framing (Nexus covers IO + external calls + all UI; Mencie is the canonical UI example) lands inline.

## Surprises and open questions

1. **Cloud worktree**: the `cloud` repo has a `designer-cloudflare-cli-prototype-2026-05-27` branch but no `designer-intent-manifestation-2026-05-27` branch. Per the instruction "don't create new branches", cloud's INTENT.md was not updated despite record 965 specifically calling out `cloud-to-Cloudflare CLI` as the canonical nexus-IO example. Recommend creating the manifestation branch for cloud in a follow-up.
2. **No mencie repo exists yet** (per `ls /git/github.com/LiGoldragon/ | grep mencie` — no match). Records 965's mencie-as-nexus framing is captured in workspace INTENT.md + the skill + reports; it lands in `repos/mencie/INTENT.md` (or wherever the UI panels live) when the repo is created.
3. **File-extension question remains open** per record 964. The manifestations preserve the openness: `.signal.schema` / `.nexus.schema` / `.sema.schema` OR first-record-as-variant. No file gets locked to one form.
4. **ESSENCE.md not edited** — the three-schema-types framing IS Maximum-certainty (record 964), which suggests it might warrant essence-tier promotion. Per `skills/intent-manifestation.md` §"When the destination is missing", promotion to ESSENCE is the psyche's call, not the agent's. Flagged here for psyche review.
5. **signal-spirit INTENT.md had an orphan section heading** (`## Continuous manifestation` line 108) created during my first edit pass — fixed by removing the duplicate; only the existing one near the bottom remains.
6. **Record 371's runtime-triad framing is now superseded on terminology** (Executor → Nexus) but the federation framing and the migration plan remain valid. The status banner explicitly limits supersession to the naming.
