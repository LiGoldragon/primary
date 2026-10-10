# Compact retention for Codex transcripts

This is an investigation/design report, not an implementation or retention ruling. The useful shape is a small, directly searchable working record backed by lossless compressed evidence. Human recall, agent continuation, audit/debugging, and exact provenance have different minimums and should not be forced into one representation.

## Observations

The local archives are JSONL, but not one stable schema. Claude stores root and nested subagent conversations plus tool-result files and metadata. Codex stores event envelopes whose payload discriminator and fields vary across generations. Pi and Pi-subagent artifacts use additional schemas and sidecars. Current local totals are approximately 6.98 GB across Claude, Codex, Pi, and Pi-subagent artifacts; the flow layer is only 2.54 MB. See the inventory witness for methods and exact class totals.

The bulky classes are not uniformly disposable:

- Tool stdout/result payloads dominate several samples and are often the material needed to reproduce a failure. They are good compression and external-blob candidates, not automatically safe deletion candidates.
- Repeated token counters, envelope fields, injected context, and some world-state snapshots are structurally repetitive. They are candidates for header/delta encoding or recomputation, subject to resume tests.
- An older Codex schema duplicated `stdout` and `aggregated_output` exactly in all 184 sampled command events, yielding 16.2 MB of removable duplicate in that one file if one canonical value is retained. Other fields such as formatted output were not proved equivalent.
- Reasoning/encrypted content can be large and cannot be treated as inspectable audit evidence. A summary is useful for continuation, but replacing encrypted evidence with it is lossy.
- Flow logs, index entries, and reviewed psyche records are already a compact human-facing layer. Prior psyche records say distilled material should be self-standing and explicitly reviewed while raw material remains archived/referable.
- Commentary and final are distinct phases of the same assistant output stratum. Phase matters for replay and interpretation. Source records establish some compaction behavior, but not a general rule that commentary is safe to discard.

## What each audience must retain

| Audience | Minimum directly accessible material | Backing requirement |
| --- | --- | --- |
| Human recall | Flow/index entry; short outcome and decisions; open questions; reviewed vision/intent; links to source | Keep raw psyche words and source links; summaries are not authority by themselves |
| Agent continuation | Task/want; current state; next action; touched paths/revision; parent and child flow IDs; latest final outputs; failures and unresolved forks; searchable source references | Preserve enough typed user intent, assistant commitments, tool result excerpts, and event ordering to avoid re-derivation |
| Audit/debugging | User-origin request, relevant assistant/tool events, errors, commands, outputs, environment/schema, timestamps, phase, and failures | Exact bytes or a verifiable immutable blob, with access control and a stable event/line map |
| Exact provenance | Session/thread UUID, event ordinal and original physical line, parent/turn links, timestamp, role/origin/phase, harness/schema version, cwd/revision, content digest, and byte offsets | Immutable original or lossless reconstruction; storage digest is not a psyche authority/record ID |

## Proposed shape

1. Keep a small hot “recall card” per flow. It should contain the index-facing summary, decisions/rulings, current state, next action, open forks, parent/child flow IDs, and links to reviewed vision and reports. Keep it short enough to read at session start.

2. Keep a continuation card separate from prose reports. Store the latest user intent, agent commitments, touched paths/revisions, failures, latest subflow final results, and source references. A report can explain reasoning, but continuation should not require reading a report or a whole transcript.

3. Store exact evidence as immutable, content-addressed chunks compressed with a random-access-friendly codec. A compact transcript manifest maps each event to its session UUID, ordinal, original line/byte range, role/origin/phase, parent/turn relation, schema, and blob digest. Preserve the original JSONL digest and a line map so a `transcript raw <session> <lines>`-style operation can return the original lines exactly.

4. Deduplicate only with an equality witness and scope-aware references. Move invariant session/cwd/schema data to a header; delta-encode repeated IDs and timestamps; retain one canonical copy of proven-identical command output; and retain references for repeated injected context, parent/subflow mirrors, or identical tool results. The reference must carry session/event context and access-control identity, because identical bytes can occur in different private sessions.

5. Treat semantic distillation as a second, reviewed product. Ordinary tool chatter can become a continuation card plus exact artifact references. Psyche records require preservation of raw words and explicit review of any distilled replacement; archives must retain chain of origin. Never allow an unreviewed summary to overwrite the raw authority record.

6. Preserve assistant phase (`commentary` versus `final`) and event order in any replayable compact layer. Post-close commentary/reasoning may be moved to cold evidence or summarized only after a tested hold/reference path exists; the available evidence does not settle universal safe omission.

## Plausible retention tiers

These are candidate tiers, not approved policy or TTLs.

- Hot/live: exact current session and all active parent/subflow evidence, with the recall and continuation cards indexed. No automatic expiry while a flow or child remains active.
- Warm/recent: closed flows retain cards, typed user messages, assistant finals/commitments, compact event ledger, and searchable metadata. Exact tool blobs remain compressed and externally referenced. A 30–90 day window is a policy question, not a recommendation settled by this investigation.
- Cold/archive: immutable compressed blobs plus manifest, checksums, ACLs, and event/line maps. Keep metadata searchable and restore exact evidence on demand. Psyche raw and incident/authority material belong here at minimum, rather than in a lossy summary-only store.
- Expirable/ephemeral: only after reference and hold checks, candidates include recomputable token counters, superseded world-state snapshots, duplicate rendered copies, temporary tool-result mirrors, and unpaired backups. Expiry needs explicit authority, an audit record, and a tested recovery path.
- Incident/authority hold: no automatic expiry for user/psyche words, security/privacy/deployment decisions, failures, disputed provenance, generated artifacts, or evidence needed for an active audit.

## Bounded savings indicated by local measurements

- Lossless gzip-1 retained 21–74% of representative files, i.e. 26–79% savings; zstd and chunking may differ, and these are not corpus averages.
- Removing one proven duplicate `stdout`/`aggregated_output` copy in the sampled old Codex file would save 16,226,340 bytes, about 40.2% of that file’s serialized bytes.
- Collapsing 524 repeated current-parent token-count events (417,614 bytes, 11.7% of that sample) could be meaningful if resume/audit semantics permit one final counter or a compact per-turn ledger.
- Pi artifact sidecars are only 16.1 MB beside 1,190.2 MB of transcript JSONL. Keeping sidecars alone would be a 98.7% size reduction for that class, but it is continuation metadata, not exact provenance.
- Claude auxiliary backup/tool-result files total 253.5 MB (32.2% of the Claude project). This is a candidate for reference-aware cold storage, not a safe deletion estimate.

## Risks and tradeoffs

Summaries can hallucinate, omit a failed attempt, or drift as a design changes. A compact card should therefore identify its source event ranges and confidence/review status. Distillation can improve signal-to-noise while losing modality, chronology, or the living psyche’s exact words.

Repacking breaks physical line numbers and naive transcript search unless the original digest, event ordinal, and line map are retained. A dangling external blob silently turns a provenance record into a claim. GC must first establish complete inventory, no truncation/failure, valid references, permissions, and all active holds.

Cross-harness schema drift makes a single deduplication rule unsafe. Dedupe can conflate equal bytes with different meaning or authorization. Compression adds CPU, latency, and random-access index complexity. Search indexes themselves can expose private prompts even when raw blobs are protected.

Dropping tool output harms debugging; dropping user-origin context harms continuation; dropping phase or ordering harms replay; dropping encrypted reasoning may reduce size but cannot yield exact inspectable reasoning. A child flow may still be active after its parent appears closed. Current short-ID collisions also show that an eight-character prefix is not a universal provenance key in this workspace; identity and storage-address namespaces should be explicit.

## Unknowns requiring a later ruling or experiment

- Which exact records each Codex/Claude/Pi client requires for resume, replay, search, and billing; whether token counters and old `item_completed` envelopes are recomputable.
- Whether old `formatted_output` differs semantically from `stdout`/`aggregated_output`, and duplicate prevalence across the corpus.
- Exact corpus-wide compression/dedup ratios, chunk size/index overhead, and acceptable restore latency.
- The canonical mapping among parent flows, subflows, imported sessions, artifact sidecars, and transcript UUIDs.
- Retention authority, legal/privacy holds, TTLs, deletion approval, encryption, ACLs, and recovery testing.
- Server-side compaction semantics and model/version sensitivity for commentary, final, reasoning, and encrypted payloads.
- Coverage and trust of human-origin markers across harnesses; an agent-injected task prompt is not automatically a definitive live-human marker.
- Whether the absent local `transcript` executable is expected in this setup and where the intended search index lives.
- Whether the collision-extended child flow ID used here should become a general identity convention; no such change is proposed.

## Remembered prior flows (depth 1)

The requested remembering pass read each flow’s log, pertinent vision, and last model response.

- `e06e4c07`: the relevant transcript/search practice was typed prompts first, nearby model responses, and line-addressable retrieval; its last response dealt with focused tests and a testing-skill proposal. For retention, preserve a compact typed-intent surface plus exact source ranges rather than requiring a whole transcript.
- `cff271af`: its reports/vision record psyche concern that parent context is valuable while subflow/file-read churn is lower-stratum, and that distillation should be compact, self-standing, explicitly reviewed, and raw-archived. Its last response merged a design draft. For retention, continuation cards should carry parent context and reviewed distillations should link—not replace—raw evidence.
- `aa4c7747`: its session-log vision says transcripts already carry time and flow logs should expose main points; its ethos vision separates mental model from code noise. Its last response rebuilt an ethos-first prompt. For retention, timestamps remain transcript provenance while the flow log remains the short human recall view.
- `01a03d6e`: its flow vision says a subflow is also a flow and a parent remains active through subflows; flow identity is a short session-derived ID. Its last response corrected a Datom proposal around missing projections/codecs. For retention, lifecycle and identity metadata must be explicit; do not expire child evidence merely because the parent looks done, and do not assume the short-ID projection is collision-free.

## Sources

- Local measurement witness: `flows/01a042376379/witnesses/retentionInventory.md`.
- Authored guidance: `.agents/skills/transcript-search/SKILL.md`, `.agents/skills/flows/SKILL.md`, `.agents/skills/psyche/SKILL.md`, and `.agents/skills/behavior/SKILL.md`.
- Harness/search design: `reports/HarnessTranscriptSearch-2026-08-19.md` and `reports/SessionSearchTools-2026-08-19.md`.
- Inventory/GC safety record: `reports/criomeFableSessionRecovery/session-inventory-health-situation.md`.
- Psyche records: `psyche-raw/Vision/psycheLogStructure.md`, `flows/15b67974/vision/psycheLogStructure.md`, `flows/06196cc7/vision/psycheLogStructure.md`, `flows/4ddc321d/reports/codexChannels.md`, and `flows/4ddc321d/reports/commentaryDiscouragement.md`.
- Remembered prior flows: `flows/e06e4c07/`, `flows/cff271af/`, `flows/aa4c7747/`, and `flows/01a03d6e/`, including each requested log, pertinent vision, and last model response.
