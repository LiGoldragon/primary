# Bead staleness audit — 2026-06-19

## Scope

The psyche asked to close stale beads and bring forward uncertain items. I audited the open BEADS queue in primary, closed only beads with direct evidence that the work was shipped, superseded, duplicated, or content-free, and left ambiguous / partially-complete items open.

Initial open count from `bd list --status open --limit 0`: 132.
Final open count after closures: 116.

The BEADS backend was pushed with `bd dolt push`; `bd dolt commit` reported nothing to commit, indicating the close operations had already been committed by the tool.

## Closed as stale, shipped, duplicate, or superseded

| Work | Reason closed |
|---|---|
| `ready` placeholder x3 (`primary-0yq7`, `primary-err8`, `primary-mwvt`) | Each bead had only the title `ready`, no description, no notes, and no recoverable work definition. |
| SEMA single-writer gap (`primary-7hro`) | The notes record the single-writer mutex + O(1) chain-head work as done and carried into the later deployed sema-engine / Spirit rollout. |
| SEMA rebuild-from-log deploy gate (`primary-lmf3`) | The notes record rebuild-on-layout-skew as done and later deployed with Spirit 0.13.0. |
| Duplicate spirit-next internal rename (`primary-f8gf`) | Duplicated the still-open broader cross-repo rename bead; internal rename itself is recorded there as landed. |
| SEMA migration diagnostics / typed errors (`primary-12r5`) | Notes say the diagnostics and typed-error polish landed on the vc-followups/schema-next-polish work. |
| SEMA/mirror naming cleanup (`primary-h3ll`) | Notes say the naming/copy-paste cleanup landed on vc-followups and mirror arc-shipper. |
| RecordKey closed-sum cleanup (`primary-sean`) | Notes say RecordKey became `Domain | Identifier`; remaining integration context lives on broader integration beads. |
| v1-v6 migration witness-or-narrow (`primary-sd7n`) | Psyche chose delete/reject; notes say v1-v6 paths were deleted and probing narrowed. |
| v7-to-v9 referent fold bug (`primary-im1l`) | Notes say v7 referent reading and a non-empty-referent witness landed; later audit notes say it no longer blocks deploy. |
| Spirit prototype storage (`primary-q2au`) | Superseded by current `.sema` / sema-engine storage. Current `spirit` has sema-engine wiring, `.sema` tests, DatabaseMarker surfaces, and a test preventing direct redb runtime dependency. |
| VersionReport store-schema/hash (`primary-dmy4`) | Notes say VersionReport was widened with store schema version and hash on vc-followups. |
| TypeReference structural macro (`primary-xzzf`) | Notes say nota-next/schema-next converted TypeReference to StructuralMacroNode and deleted duplicated hand-rolled dispatch. |
| Agent stale schema-rust pin (`primary-opzy`) | Current `agent`, `signal-agent`, and `meta-signal-agent` locks no longer reference the failing old schema-rust-next rev; schema-rust-next now handles `TypeReference::Application`. |
| Nexus stale Signal dependency blocker (`primary-36iq.6.2`) | Current `nexus` no longer locks the old Signal rev, and current Nexus/Signal trees no longer reference removed `nota_codec::NotaSum`. |

## Left open because I am unsure or the bead still carries real residue

| Work | Why I did not close it |
|---|---|
| SEMA VC-hardening integration (`primary-qu28`) | Many comments show deployment success, but the original definition included repinning every sema-engine consumer. I did not verify router/criome/mind/current fleet state deeply enough to close the broad integration bead. |
| Chroma config parser + sema-engine adoption (`primary-n1ao`, `primary-y0ec`) | Notes say the work is done on Chroma `next` but not landed per the bead. I did not verify current main integration, so these remain open. |
| NOTA bracket-string epic and residual children (`primary-36iq`, `.3`, `.6`, `.7`, `.7.1`, `.7.2`) | Several slices are complete, but live Spirit CLI/profile support, Persona/signal examples, and horizon/lojix guidance may still be unresolved. I only closed the Nexus blocker child. |
| Router/criome networking and BLS beads (`primary-9x9f`, `primary-kr40`) | Notes show large completed chunks plus remaining cluster-root signing/key-custody/live-forward residues. These need split/retitle or owner decision, not blind closure. |
| Spirit daemon runner extraction (`primary-es8u`) | Notes show several slices landed, but the bead explicitly says full runner extraction/cutover parity and production deployment migration remain. |
| Spirit store/engine file-size split (`primary-x178`) | Substantive decomposition landed, but the notes say over-thousand-line files remain and the next split is a psyche judgment. Left open. |
| SEMA follow-ups after integration (`primary-s22j`) | Most subitems were closed in comments; one native item remains: guardian-journal v2 fold-forward, marked as a psyche call. This probably wants a narrower replacement bead, but I did not close it. |
| Legacy orchestrator retirement (`primary-mt02`) | The bead itself says retirement needs psyche/owner confirmation and a system/profile deploy action. Left open. |
| VM-host test node (`primary-dw95`) | It has no description, but the title is specific and matches currently-active VM-test work. Not stale enough to close. |
| Lojix deployment identifier (`primary-766g`) | It has no description, but the title is a concrete implementation task; I did not have enough evidence that it is stale or done. |

## Follow-up recommendations

1. Split or retitle broad mostly-done beads whose remaining residue is narrower than the original title, especially the router/criome and sema follow-up clusters.
2. Ask the relevant owner before closing any bead that explicitly says “awaiting operator integration”, “awaiting psyche decision”, or “pending confirmation”.
3. Run a second pass focused by repo owner/claim state rather than global staleness: Chroma, NOTA bracket-string, router/criome, and sema-engine each need different evidence.
