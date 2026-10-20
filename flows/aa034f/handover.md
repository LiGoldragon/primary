# Handover: Psyche flow Secondary aa034f

Role: Flow source owner (Psyche side). Mind implements with you; Field (now core Tertiary 4201a3 did it) installs. Communicate through Psyche core Secondary (68db51, pane w2S:p1).

## Deployed
- flow-nexus 0.35.21 (dcb63e6), signal-flow e6ccbdd, meta-signal-flow efccfb5; store ~/.local/state/flow-03521.
- Installed by core Tertiary 4201a3 at 15:23 from Field Home main 798ef464. Its decisions and rollback are in flows/4201a3/decisions.md and rollback-20261019.txt.
- CLI: `flow-start <Aspect> <topic> <Layer> [-p pred] [task]`.

## Branches not deployed (flow repo; contracts beside)
- aa034f-sleep b972355 (+ meta-signal-flow fbd4459 29.0.0): every idle metaflow sleeps, every wake is fresh, resume deleted.
  - Living rulings open: a Primary pane closes after each empty-queue turn; resume on continuation needs a typed mark.
- aa034f-rules eabe7f2 (+ signal-flow c7dcc07 23.0.0, meta-signal-flow 573a2c5 29.0.0): /compact refused below the threshold; StartRejected.NoSecondary; Ended/End removed.
- aa034f-next: integrator merging sleep and rules into one candidate, keeping one threshold setting. Result not yet seen.
- aa034f-books: implementer building the turn-end book enforcement. Result not yet seen.
  - Rulings taken: every living message owes a book; Nexus unreachable blocks; block cap raised.
- aa034f-compose-role f1dee77: blocked on two core rulings.

## Living's orders this session
- Every visible name is the title { Aspect Topic Layer ID }, never wrong again. Deploy carries it; verify on the first new launch.
- Everything he says reaches a book with a response, every time:
  - book https://claude.ai/artifact/7w2BSVU1krfhJVyhE9MRwc;
  - module line landed in psyche-context dc8c4cf (missing flow is started).
- A missing flow is started, never routed around. Never talk to a Primary off route.
- Knowledge only of deployed code.
  - https://claude.ai/artifact/SnHF7LLo9qw967VDA9GhSJ still describes 0.35.11; replace it with the deployed behaviour now that 0.35.21 runs.
- Startup tokens book: https://claude.ai/artifact/WLMwNCU4jdwbzT1SuKvVhh (~50k per Claude start).
- Fix names at the launcher, never by typing into panes.

## Open
- Field core Secondary start under 0.35.21 (subflow in flight); then it renames every misnamed thread.
- The messenger lists core Secondary under its old key 5dd7e5. That is Mind's fault; Mind Core Secondary is not registered.
- Ethos books, accepted on content (joint 76454e, whole-Flow 93a337), wait on core:
  - the width ruling;
  - book-check heading context, L100–102;
  - book-check indented change, L10.
- Vision audit gaps: route check, unknown metaflows started, caller identity from process, refresh at the threshold (third edition), Capsule, Memory in ethos, subflows. The split was proposed to Mind via core.

## Added at end of aa034f
- Codex launch fix, the first deploy: flow bae1fcd (0.35.22) on aa034f-integration, fast-forward from deployed dcb63e6, contracts unchanged.
  - The thread is opened, named and read back; Herdr attaches while it is idle; then the first turn.
  - Not witnessed live.
  - First live check: flow-start Field core Secondary. Its declaration config/main-flow/metaflow/Field-Core-Secondary.edn is unstaged in Primary.
- aa034f-next is now flow 042df6d (0.35.23), on signal-flow c7dcc07 and meta-signal-flow 2b03b50. Its versions must follow bae1fcd when rebased.
  - Idle flows keep their pane and stay Awake (the living: closing panes is long-term).
  - Sleep, fresh wake when the pane is gone, compaction refusal, NoSecondary, no Ended.
- aa034f-books: flow 40f87a3, signal-flow ce1f761, meta-signal-flow dc165fd.
  - The turn-end book check on Claude seats.
  - Codex is open, pending the living's answer on how a Codex flow gives a book.
- Books published:
  - Flow Visible Names v3: SnHF7LLo9qw967VDA9GhSJ;
  - Everything the living says reaches a book: 7w2BSVU1krfhJVyhE9MRwc;
  - Flow Startup Cost: WLMwNCU4jdwbzT1SuKvVhh;
  - Idle panes stay open: NTSbqcqxBsCGkr8kunmQN8 (its next edition adds 042df6d's lines);
  - Flow's Tests: FqWPbcDdYJuCkVPUeM2sBo.
- Live store finding: Awake metaflows carry sequential ids (flow-0000000000000017 and others), not 6-hex Flow IDs, so their titles are nonstandard.
- This flow's sends are refused as Retired; the successor 002721 is STALE. Core Secondary is now ca28a4, core Primary 5ec12c.
- Evidence rule from the living: report behaviour witnessed live, never test counts.
