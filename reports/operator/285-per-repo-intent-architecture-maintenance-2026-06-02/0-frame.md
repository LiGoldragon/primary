# Per-Repo Intent/Architecture Maintenance - Frame

*Kind: meta-report frame; topics: schema-rust-next, spirit-next, schema-next, nota-next, trace, triad; date: 2026-06-02*

## Request

Run an operator-lane maintenance pass after fresh intent-maintenance reading.
Audit recent Spirit intent and live implementation around typed trace objects,
schema-defined triad interfaces, generated trait trace hooks, zero-NOTA
daemon/text CLI separation, and directly related `schema-next` / `nota-next`
architecture files.

## Method

I read the required workspace files and skills before repo inspection:

- `ESSENCE.md`
- `INTENT.md`
- `AGENTS.md`
- `repos/lore/AGENTS.md`
- `skills/intent-maintenance.md`
- `skills/context-maintenance.md`
- `skills/repo-intent.md`
- `skills/architecture-editor.md`
- `skills/jj.md`

For each repo I inspected its `AGENTS.md`, `INTENT.md`, and
`ARCHITECTURE.md`. Each of the four repos currently lacks a root `skills.md`,
so there was no repo-specific skills file to read.

I queried Spirit records 1339-1450 as the fresh intent surface. The current
load-bearing records for this pass are 1339-1350, 1365, 1370-1375, 1386-1396,
1398, 1400-1401, 1405, 1408, and 1411.

## Coordination

`tools/orchestrate status` showed no active lane claims when this pass began.
I did not claim any repo because I made no edits inside the target repos.
Reports under `reports/operator/` are exempt from the claim flow.

## Output Shape

This directory is the requested meta-report:

- `0-frame.md`: method and coordination.
- `1-schema-rust-next.md`: Rust emitter findings.
- `2-spirit-next.md`: runtime pilot findings.
- `3-schema-next-and-nota-next.md`: adjacent substrate findings.
- `4-synthesis.md`: final actions, changed files, and checks.
