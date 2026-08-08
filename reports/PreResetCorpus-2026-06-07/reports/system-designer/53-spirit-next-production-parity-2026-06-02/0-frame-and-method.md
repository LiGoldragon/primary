# Spirit Next → production parity audit + path-to-ship — 2026-06-02

Kind: meta-report directory (frame + four sub-agent audits + overview).
Role: system-designer (orchestrator).

## Frame

Psyche directive: research, audit, and test how to bring `spirit-next`
into production — even incrementally, even side-by-side with the current
`persona-spirit v0.3.0` deployment. Fork latest main of any component
that needs to change. Use sub-agents.

The deployed Spirit today is `persona-spirit v0.3.0`, served via
`~/.nix-profile/bin/spirit` resolving to
`/nix/store/n0pi3ahjv5s766lnxyvv0z7qyvy7aaw8-spirit-v0.3.0/bin/spirit-v0.3.0`.
The next-stack authoring target is `spirit-next`, the canonical engine-
trait worked example (per `skills/component-triad.md:819`). The deploy
slot `spirit-next` is reserved in the model per
`skills/spirit-cli.md` §"Deployment slots".

The side-by-side model means we don't have to wait for full parity —
spirit-next can ship into its own slot, with its own state directory
and sockets, while persona-spirit v0.3.0 remains the production binding.
The user explicitly accepts incremental progress.

## Questions this audit answers

1. **Wire-shape parity** — which Signal operations does production
   spirit serve that spirit-next does not yet? What's the minimum
   wire shape for spirit-next to be useful?
2. **Buildability and behaviour** — does spirit-next build today?
   What tests pass? What happens when you actually run the daemon
   and round-trip a Record → Observe?
3. **Deployment configuration** — how is production persona-spirit
   wired into the deployed Nix profile? What's the path to add a
   `spirit-next` slot beside it? Is anything already in place?
4. **Data and storage compatibility** — production has a redb at
   `~/.local/state/persona-spirit/<version>/` with all current
   records (1-1375+). Can spirit-next read that data, or does it
   need a fresh database? What's the eventual cutover path?

## Sub-agent dispatch

Four read-and-test sub-agents in parallel. Each inherits the
system-designer lane per Spirit 920. Each writes a numbered report
inside this directory. Orchestrator synthesises into `5-overview.md`.

### Sub-agent 1 — Wire-shape parity audit

Map production spirit's wire shape (from the pinned `signal-persona-
spirit` source per `skills/spirit-cli.md` §"The deployed wire shape").
Map spirit-next's current wire shape (from `signal-spirit-next` or
its in-repo schema). Identify gaps: which operations does production
serve that spirit-next doesn't, and vice versa?

### Sub-agent 2 — Build, test, run spirit-next end-to-end

Build the spirit-next daemon and CLI from current main. Run the test
suite. Try invoking the CLI against a daemon instance (smoke test:
Record, Observe, Remove). Report what works and what doesn't with
concrete evidence (commit IDs, test output, wire interactions).

The production daemon stays untouched — spirit-next has its own slot
per the side-by-side model. Use temp paths for state directory and
sockets if needed.

### Sub-agent 3 — Deployment configuration audit

How is production `persona-spirit` deployed today? Trace from
`~/.nix-profile/bin/spirit` back through the Nix profile, the home-
manager configuration in `CriomOS-home`, the systemd user service (if
any), and into the package definition. What does the deploy chain look
like? Is anything already in place for a `spirit-next` slot beside it?
What concrete changes are needed to ship spirit-next as its own
side-by-side deployment?

### Sub-agent 4 — Data and storage compatibility

Production carries persona-spirit's record store at
`~/.local/state/persona-spirit/<version>/` (redb). Does spirit-next
use a compatible storage shape? If we deploy spirit-next side-by-side,
does it start with an empty database or can it bootstrap from the
production store? What is the eventual cutover plan — exported and
re-imported, format-compatible direct read, or migration tool? Per
Spirit 1249 (discriminant stability) what would break if the encoded
shape has drifted between versions?

## Constraints for sub-agents

- READ-ONLY for production daemon's state. Don't write to
  `~/.local/state/persona-spirit/v0.3.0/` or restart the production
  daemon.
- Building spirit-next is allowed (uses Nix store; no production
  side-effects).
- Running a spirit-next daemon for testing is allowed if it lands its
  state under `/tmp` or a new slot dir, not in the production slot.
- Each sub-agent inherits this lane per Spirit 920.
- Output goes into this directory, file name per the dispatch list.
- Cite paths, commit IDs, Spirit record numbers as evidence; surface
  uncertainties as uncertainties.
- Markdown: section structure via `##`/`###` headings. No `---`
  horizontal rules.
- NOTA strings come EXCLUSIVELY from bracket forms.

## Output structure

```text
53-spirit-next-production-parity-2026-06-02/
├── 0-frame-and-method.md          # this file
├── 1-wire-shape-parity-audit.md   # sub-agent 1
├── 2-build-test-run-audit.md      # sub-agent 2
├── 3-deployment-configuration-audit.md  # sub-agent 3
├── 4-data-and-storage-compatibility.md  # sub-agent 4
└── 5-overview.md                  # orchestrator synthesis
```
