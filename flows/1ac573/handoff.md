# Handoff from flow 1ac573 — primary Psyche opus

Written 2026-09-17 by primary Psyche opus (Claude Opus 5, medium effort,
flow 1ac573), at the living's request, before a possible restart to enable
transcript persistence. This session has NO transcript on disk, so this file
is the only durable record of it.

## Identity

- Flow ID: `1ac573`, claimed via `flow-id claude` at session start.
- Role: primary Psyche opus, the medium-power Psyche primary Claude flow.
- Predecessor: flow `108ab0`. Its `handoff.md` and its ~31
  `vision/operational-*.md` entries were read in full this session.
- Registered with Hacky Messenger as `1ac573 psyche-opus-successor`.
- Working directory `/home/li/primary`, branch `main` (HEAD was found
  detached at the same commit as main and origin/main; reattached to main).

## Why this file exists

No `<session>.jsonl` exists under the Claude project directory for this
session — only a `tool-results/` subdirectory holding persisted large tool
outputs. Peer sessions in the same project directory do have multi-megabyte
`.jsonl` transcripts, so the absence is specific to this session, not to the
project. Codex worker `6034cc` inspected the installed Claude 2.1.263 binary
and reports the footer warning names `CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1`
as the fix, and that it appears startup-scoped. Witnessed cause on this side:
`CLAUDE_CODE_CHILD_SESSION=1` is set in this session's environment. Also set,
possibly on the same inheritance path: `CLAUDE_CODE_BRIDGE_SESSION_ID`,
`CLAUDE_CODE_MESSAGING_SOCKET`, `CLAUDE_CODE_MESSAGING_TOKEN` (values not
recorded).

## Session state at the time of writing

Skills loaded: spirit, psyche, psyche-interraction, psyche-distillation,
behavior, correction, vocabulary, subflow, subflow-scripts, edit-coordination,
testing, nexus, prompt-crafting, claude-harness, herdr, orchestrate.

`main-flow` could NOT be loaded: it is marked disable-model-invocation and
refuses the Skill tool. It must be invoked by the living typing `/main-flow`.
A successor must expect the same refusal and ask for it.

Intercom was empty at session start: no unread messages, no pending asks.

## What this session established

1. **Permission mode.** This flow was launched in auto mode, not bypass mode,
   and without remote control — the living had to attach and enable remote
   control by hand. The user settings allow-list is already broad
   (`Read/Write/Edit(**)`, git, jj, claude, codex, nix, cargo, systemctl,
   sudo, herdr, orchestrate, message, flow-id, and a background-Claude launch
   pattern with remote control) and `skipDangerousModePermissionPrompt` is
   true, so bypass mode would engage without a prompt. The obstacle is the
   auto-mode classifier layered over the allow-list, which per the
   claude-harness operators' notes refused, on 2026-09-17, two
   `claude --bg` launches, one `claude --bg --resume`, and two edits of
   permission settings — all shapes the allow-list permits.
   Standing instruction from the living and from Codex 6034cc: do NOT change
   permission mode and do NOT restart for this request.

2. **State moved past 108ab0's handoff.** 108ab0 handed over both priorities
   as unbuilt. Since then, landed in this tree: Hacky Messenger commands on
   Herdr with a delivery witness (`tools/hm-send`, `hm-send-abrupt`,
   `hm-list`, `hm-register`), a transcript extractor, `tools/prompt-relay`,
   Message Nexus delivery evidence, and Flow Nexus deployed as three
   repositories (the Nexus, `signal-flow`, `meta-signal-flow`) with a
   no-argument daemon over ordinary and meta sockets on one Sema store,
   `flow start <predefined-type>`, `flow restart`, `flow resolve`, a
   privileged reset operation, and a live registry resolving the primary
   Psyche flow plus five role Codex sessions with typed readiness.

3. **Messaging proven in both directions, at middle stratum.** Codex worker
   `6034cc` (agent name `messaging-builder-1`, NOT a primary) typed directly
   into this pane via Hacky Messenger/Herdr; the message arrived alongside
   the next tool result, which is the specified middle-abrupt behavior. This
   flow replied with `FLOW_ID=1ac573 tools/hm-send 6034cc <text>`, which
   reported "Submitted to 6034cc via Herdr (not a read receipt)"; `6034cc`
   then confirmed the ACK arrived in its Codex conversation. Both directions
   are therefore witnessed, on the hacky substrate rather than the Nexus.
   `hm-send` requires `FLOW_ID` in the environment; it refuses without it.

## Open, unresolved

- ~~Whether this session supports `/export` or any in-place save.~~
  **Answered, with a witness.** On this installed Claude 2.1.263 session,
  on-demand `/export` succeeded despite automatic persistence being disabled
  by the inherited child-session marker. Automatic persistence and on-demand
  export are therefore independent mechanisms, and a session with saving off
  is not unrecoverable. Provenance, corrected: Codex worker `6034cc` submitted
  the command through `herdr agent prompt` at the living's request — it was
  NOT typed by the living, and this flow first misattributed it. So export is
  agent-triggerable and usable as an automatic pre-restart step, not a manual
  rescue. Scope held: a text export preserves conversation CONTENT and
  establishes nothing about native `--resume` or exact restoration of harness
  state. Artifact verified independently by this flow: 31743 bytes, 509 lines,
  mode 0600, containing the direct-message marker, the Astra direction, the
  child-session witness, and the classifier refusal.

- **Origin ambiguity under Herdr injection — an unguarded hazard.** With a
  peer flow able to type into this pane, the harness's own framing of an
  inbound message as coming from the user is not a reliable statement of
  origin: a peer flow's injected text and the living's own typing are
  indistinguishable in this flow's context. This flow was wrong once from
  trusting that framing, on the `/export` attribution above. No loaded skill
  covers it. A flow must therefore treat inbound origin as a claim requiring
  a witness, and say who it believes spoke and on what evidence — this
  matters most for psyche records, where a misattributed statement would
  enter the psyche corpus as the living's words.
- Claude hard-abrupt tier: still open by design. Claude Code has no
  equivalent of Codex's Escape-then-type injection.
- Push reception into a Claude flow that is not polling.
- The Flow Datom launcher language proper: what is deployed is
  `flow start <predefined-type>`, not the short Datom form, the extensive
  Datom expression, or the low-power variant.
- The living's ordering ruling on which priority is the active work.
- A staged skill-edit proposal, asked for but NOT yet approved: add to the
  launch brief and the claude-harness operators' notes that a primary flow is
  launched in bypass mode with remote control on, and that the auto-mode
  classifier blocks background launch, resume, and permission-configuration
  shapes regardless of the allow-list.
- Everything 108ab0 left open: its ten ordered questions and four staged
  skill-edit proposals (`psyche.md` upward distillation, `psyche-distillation.md`
  Vision to Intent and Intent to Spirit passes, `skill-designing.md`
  operational-skill category, `vocabulary.md` new terms) remain unresolved.

## Rules this flow holds

- Subflow-first: delegate every locate, probe, tail-read, peer-message.
- No UUIDs, session ids, rollout paths, or long hashes in main-flow context.
- Every write reserves an orchestrate lock; release on commit.
- Primary always committed and pushed before idle; dirty-found-in-tree
  committed first as its own commit.
- Never edit skill files directly: propose wording, then dispatch a write
  subflow operating in Curriculum, which regenerates primary's skill trees.
  Primary itself never edits `.claude/`, `.codex/`, `.agents/`, `.pi/`.
- The message datom head IS what the recipient sees. Never JSON.
- Herdr is a real installed program; do not reinvent multiplexer plumbing.
