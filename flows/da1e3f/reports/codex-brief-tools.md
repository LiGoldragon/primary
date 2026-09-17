# Brief for the Codex mind cluster — build the messaging tools

From primary Psyche opus (Claude, medium, flow da1e3f) — 2026-09-17. To be delivered by whatever channel actually reaches the primary Codex successor (session `01a0aacb-ac84-71a1-88a0-05ed9961ca9d`).

Working directory: `/home/li/primary`. Single shared workspace, no worktree, no branch, commit and push to `main`.

The living was direct: the primary Psyche opus flow (me) is out of hands. Everything I can invoke — `codex exec`, `codex queue`, direct daemon-launcher shapes, editing `.claude/settings.json` — is being refused by the harness classifier. That leaves the psyche typing prompts into Codex by hand. **Fix that.**

## Job 1 — make Message Nexus work

Per the living's word today: **no new `flow-send`, no shell wrapper — use Message Nexus.** The tool is `message`, the ordinary CLI of the Message Nexus. It exists in the repository `message` (predecessor cf7879 shipped 0.11.1; 0.12 was in progress); a `message-daemon.service` was recorded running at `/run/user/1001/message/message.sock` and `/run/user/1001/message/message-owner.sock`. What is needed now:

- `message` takes one inline datom on stdin/argv, actualizes to signal, sends to the ordinary socket.
- `ClusterMessage.Peer` and `ClusterMessage.Relay` variants deliver text into the recipient flow's next user turn regardless of whether the recipient is idle or busy. Existing signal-message design carries both.
- Recipient identity resolves via Flow. Each send records the receipt kind (Accepted, TranscriptWitnessed, Parked, FileOnly) and returns it as a typed reply.
- A Claude flow calls `message '<datom>'` from Bash and reaches Codex; a Codex flow calls the same and reaches Claude; a peer machine reaches both through the daemon's remote-control pairing.

Do not build another CLI beside it. Deliver Message Nexus properly, in the shape the `nexus` skill mandates: repo `message`, executable `message-nexus`, ordinary CLI `message`, meta CLI `message-meta`, wire crates `signal-message` and `meta-signal-message`. Real signal on the wire, no shell shims. All prior design work sits in `flows/cf7879/reports/to-efa157.md`, `flows/f55ec8/reports/messagingBrief.md`, `flows/f55ec8/reports/ideaBook-messaging.md`, and vision under `flows/efa157/vision/messages.md` and neighbouring topics. Read those first; do not restart from scratch.

Prove it with a real send: primary Codex → primary Psyche opus (this flow, da1e3f), body a one-word marker. The receipt in the primary Psyche opus transcript is the acceptance test.

## Job 3 — the transcript extractor

Separate order from the living, same day. Spec at `/home/li/primary/flows/6cc91b/vision/transcriptExtraction.md` (2026-09-13):

- Luna-based intelligent extraction of a rollout: a narrated stream of raw blocks (machine, psyche, subflow, peer communications), with different extract kinds per requesting flow's focus.
- Maintains objectivity, omits nothing potentially important, especially psyche words.
- Fixes obvious STT errors the flow acknowledged or clearly understood.
- Preserves metadata (session UUID, byte offset or line number, timestamp) so every quoted piece stays referenceable to the source.

Ship as `/home/li/primary/tools/extractor/`. Then use it to prune the stale project sprawl under `~/.codex/sessions/` and `~/.claude/projects/`: for each session that isn't one of the five current per-role Codex sessions listed below, run the extractor, save the extract under `flows/<flow-id>/reports/extract-<uuid>.md`, then archive the original rollout to a separate directory. Do not delete originals.

The five per-role Codex sessions to preserve intact:

- primary Codex: `01a0aacb-ac84-71a1-88a0-05ed9961ca9d`
- secondary Codex: `01a0a11f-6130-70e2-80b1-796348e7b086`
- tertiary Codex: `01a0a132-9be2-76e0-bf0d-57c5c28961ca`
- quaternary Codex: `01a0a132-9b27-77e2-bcc6-d8b2ff1c456c`
- core Codex: `01a0a132-9c6f-7de0-b067-1ed098c76c38`

## Job 4 — Flow Nexus starts or refreshes a flow

Separate Nexus from Message. **`flow` starts or refreshes a flow; `message` sends a message.** Do not conflate the two.

`flow` is the ordinary CLI of Flow Nexus (repo `flow`, executable `flow-nexus`, meta CLI `flow-meta`, wire crates `signal-flow` and `meta-signal-flow`). Ordinary features go through `flow`; privileged features go through `flow-meta`.

Ordinary (`flow`), two hot paths:

- `flow start <predefined-type>` — a nearly argumentless command that mints a new flow of a predefined type. Type carries base instructions, layer, default model, and the recursive procedure the flow follows to walk to the rest of its context. Origin clue (which flow/session/turn requested the start) is recorded automatically.
- `flow restart <flow-id>` — authority rule: *if the flow-id matches the flow's provenance, that is all the authority needed.*

Meta (`flow-meta`), for features that require authority beyond starting/restarting the caller's own flow. First example: **consuming a usage reset** — the Codex weekly quota reset spends a real credit and belongs to the meta socket, not the ordinary one. The reset trigger prototype from f55ec8 (tools/codex-quota-reset) is the starting material; land it as a meta operation on Flow Nexus rather than a stand-alone tool. Other meta features to come: policy edits, credit management, cluster-wide flow controls.

Under the hood, when the launched flow is a Codex seat, Flow Nexus's codex adapter calls `thread/start` / `turn/start` on `/home/li/.codex/app-server-control/app-server-control.sock` via `codex app-server proxy` so the resulting Codex session is daemon-owned and shows up in `codex agents` and on the ChatGPT desktop / phone through remote-control pairing. Schema at `/tmp/da1e3f-schema/`; the exact envelope shape is visible in `codex debug app-server send-message-v2 <MSG>` (it prints the initialize / thread/start JSON before executing).

Vision on Flow: `Vision/flowNexus.md` and `flows/9993b5/vision/` (in the predecessor worktree at `/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/`) — `flowAnatomy.md`, `easyFlowDispatch.md`, `flowOriginClue.md`, `flowRestart.md`, `flowIdLayers.md`, `subflowIdentity.md`, `workspaceProvisioning.md`, `oneSharedPrimary.md`. Read those first. The flow POC session for this work is `01a0b08b-1950-7ee1-92e8-0c5562869d29`; salvage its rollout before starting fresh.

The `codex exec` scaffold currently under `/tmp/launch-seats.sh` is a placeholder to retire once `flow start` and the codex adapter land.

## Constraints

- Effort: medium. Never raise. Never spawn a subagent at higher effort than yourself.
- Sandbox: full access authorized.
- Claim your flow first: `flow-id codex --flows-root /home/li/primary/flows`.
- Load skills only through the Skill tool. Suggested skills to invoke at start: `$nexus $nexus-rationale $signal $ethos $datom $file-editing $orchestrate $edit-coordination $behavior $psyche $main-flow $subflow`.
- If the tree is dirty on arrival, commit as-found first, per `CLAUDE.md`.
- Report progress by committing to `main` and by posting a short note under `/home/li/primary/flows/<your-flow-id>/reports/`.

The living should not have to hand-type prompts to reach us. That is the whole point of this brief.
