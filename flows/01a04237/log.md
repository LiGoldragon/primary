# Codex archive lifecycle witness

This subflow investigates Codex 0.149.1 transcript archival, local storage,
and parent/subflow lifecycle. Direct filesystem, SQLite, installed-binary,
and matching OpenAI-source witnesses are recorded under this flow.

Settled: UI archive routes through `thread/archive`; local storage renames
rollouts into `archived_sessions` and updates SQLite metadata without invoking
compression or deletion. A separate optional cold-rollout worker can later
replace active or archived plain JSONL with verified `.jsonl.zst` and remove
the plain representation. Parent archive traverses persisted/live spawn
descendants and attempts their rollouts, with source tests covering partial and
missing-child behavior. Subflows have separate rows/files and parent edges.

Open: this home snapshot has no archived parent/child pair, so edge-row
preservation and post-archive child visibility remain source-based rather than
locally observed.
