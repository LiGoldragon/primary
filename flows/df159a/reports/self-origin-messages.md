# Self-origin messages received by Psyche Flow Primary df159a

Evidence write, 2026-10-14. Facts only; sources are named per item. Timestamps are UTC as recorded by each source.

## Summary

- Four `#msg` envelopes reached this seat's chat with the sender field `"Psyche Flow Primary"`, which is this seat's own registered metaflow name (`hm-list`: `df159a psyche_flow_primary_df159a default working`; no other live route carries that name).
- The envelopes themselves do not carry a flow id, native id or layer beyond the sender name, so the envelope alone does not identify the sending process.
- Messenger store (`~/.local/state/messenger-clj/typed-datalevin/data.mdb`) holds attempt records for all four, each bound to this seat as target (thread `df159a13-abbb-4b94-bbe6-62fd8f79635b`, agent `psyche_flow_primary_df159a`), graded `Submitting`/`Uncertain` then `Transported`. The store's attempt schema has no sender-flow attribute; the sender appears only as the envelope name.
- A Codex rollout outside this seat contains the four bodies as `exec_command` invocations of the form `FLOW_ID=df159a hm-send "Psyche Flow Primary" ...`, each returning `Transported.{ df159a working }`: `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/10/13/rollout-2026-10-13T16-33-08-01a13765-e929-7d12-a3a1-e422fe101e93.jsonl`. Its `session_meta` names thread id `01a13765-e929-7d12-a3a1-e422fe101e93`, `thread_source: subagent`, `agent_nickname: Russell`, `agent_role: explorer`, `agent_path: /root/audit_288af9_firing`, `parent_thread_id: 01a13258-5fda-78c2-898b-10389fbc1701`, cwd `/home/li/primary`. The messenger store associates native thread `01a13258-5fda-78c2-898b-10389fbc1701` with `field_quaternary_89fbc1`; `tools/primary-committer/recipient.json` reads `{"flow_id": "89fbc1", "metaflow": "Field PrimaryCommitting Quaternary"}`.
- Observation only, no attribution asserted: all four bodies audit this seat's dirty paths against transcript timestamps, report `git diff --check`, index state and path collisions, and name commits `7899385` (= `78993856f Record df159a flow work`, 2026-10-14 09:40:04 -0600) and `e36386d6a` (`Republish df159a nexus book and record audit`, 09:41:38 -0600). `tools/primary-committer/brief.md` lines 9 and 15 describe reading the firing transcript and the current owned diff per hook firing.

## Message 1

### Verbatim envelope

As it appears in the transcript attachment (the body's `\n` sequences are literal two-character sequences in the stored string; the envelope arrived wrapped in `<pasted_content id="37ed">`):

```
#msg ["Psyche Flow Primary" "Current re-audit (transcript through 15:39:40): dirty paths are flows/df159a/books/11-nexus-ethos-design.html (SHA256 c5c6d8cf; generated republish from current tools/book-code.html; 44-line diff, 41 insertions/4 deletions), flows/df159a/log.md (SHA256 48ec571c; 2 uncommitted lines), and untracked flows/df159a/books/13-flow-philosophy-artifacts.md (SHA256 1a08660e; pre-existing Core-held path, no latest write), plus Book14 html (8535b98c), md (eae32f6f), refs (d97d9ffd), all untracked and attributable to delegated a812a3 Book14 revision/build request. The latest firing added a second log line at transcript record 1424: book12 audit forwarding; the prior hold line and republish dispatch line are also present. Book14’s latest frame-link still points to existing v1 artifact 8crUc..., while final revised republish receipt is absent; the main says Book14 revision remains in flight.\n\nHEAD is 214f561c7; index has no staged changes. Book12 second-edition files are clean/tracked at HEAD. Exact reservation files only flows/.df159a.flow-id and flows/.df159a.flow-id.lock; no same-basename Book14 files outside df159a, hence no exact path collision found. git diff --check is clean for tracked dirty paths. No new writes after the 15:39:40 transcript end were observed.\n"]
```

### Transcript location

Transcript: `/home/li/.claude/projects/-home-li-primary/df159a13-abbb-4b94-bbe6-62fd8f79635b.jsonl` (session `df159a13-abbb-4b94-bbe6-62fd8f79635b`, from `CLAUDE_CODE_SESSION_ID`).

- Line 1454: `queue-operation` `enqueue`, timestamp `2026-10-14T15:40:13.767Z`, no uuid.
- Line 1459: `queue-operation` `remove`, timestamp `2026-10-14T15:40:25.934Z`, no uuid.
- Line 1461: `attachment` of type `queued_command`, timestamp `2026-10-14T15:40:13.767Z`, uuid `45725509-1100-4171-b649-913c3fafb2a9`, parentUuid `cbd7690c-b65c-431d-8675-e5a729bc6b1b`. The attachment wraps the envelope in the system reminder "The user sent a new message while you were working".
- Preceding assistant action: line 1457 (uuid `e197cf5f-b29f-448e-9159-3a9739ed3ac3`, `2026-10-14T15:40:25.835Z`), Bash tool_use "Refresh the handover file" (a python heredoc editing `flows/df159a/handover.md`); its tool_result at line 1458 (uuid `cbd7690c-...`, `15:40:25.904Z`) is "Bash completed with no output".

### Messenger trail

- Store (`strings` over `data.mdb`, scratch copy `store.txt`): envelope text at store lines 635828, 635829, 856243, 973679, 975276, 997440, 997448, 1020016; bare body at 959909, 973682, 975278, 997443, 997451, 1019923, 1019924, 1020019. Adjacent attempt metadata at 975271-975284 and 997441-997450: `df159a13-abbb-4b94-bbe6-62fd8f79635b`, `psyche_flow_primary_df159a`, `term_65dc2d366759b7e`, attempt `c5618d3a-dabf-43ca-84e6-29820b616721` `Submitting`/`Uncertain` at `2026-10-14T15:40:13.276616586Z`, attempt `a220b01b-825e-42f4-a2fb-cf6d19315eea` `Transported` at `2026-10-14T15:40:13.480918478Z`.
- Codex rollout `rollout-2026-10-13T16-33-08-01a13765-e929-7d12-a3a1-e422fe101e93.jsonl`: line 1472 (`2026-10-14T15:40:06.480Z`, call `call_347eb10cf2f74cf2936fe9ca04805b32`) ran `cat <<'EOF' | FLOW_ID=df159a hm-send "/root" --stdin` with this body; output at line 1475: `messenger-clj: Invalid TARGET metaflow (aspect topic layer) ... :value "/root"`. Line 1486 (`15:40:12.728Z`, call `call_c63d321be066420eaec8a63247506bd0`) ran `FLOW_ID=df159a hm-send "Psyche Flow Primary" --stdin <<'EOF'` with the same body, workdir `/home/li/primary`; output at line 1489 (`15:40:13.580Z`): `Transported.{ df159a working }`.

## Message 2

### Verbatim envelope

```
#msg ["Psyche Flow Primary" "Follow-up: current untracked whitespace scan finds Book13 md trailing spaces at line 177; Book14 html at lines 21, 38, 126, 129; Book14 md at lines 62, 83, 132, 135, 144, 148, 157, 174, 217, 220; Book14 refs clean. Tracked git diff --check remains clean."]
```

### Transcript location

- Line 1455: `queue-operation` `enqueue`, timestamp `2026-10-14T15:40:17.926Z`, no uuid.
- Line 1460: `queue-operation` `remove`, timestamp `2026-10-14T15:40:25.934Z`, no uuid.
- Line 1462: `attachment` `queued_command`, timestamp `2026-10-14T15:40:17.926Z`, uuid `d2de6db7-d79b-4110-8ccc-88a9df1e9e77`, parentUuid `45725509-1100-4171-b649-913c3fafb2a9` (the Message 1 attachment). Not wrapped in `<pasted_content>`.
- Preceding assistant action: the same as Message 1, line 1457 Bash "Refresh the handover file"; the two attachments were surfaced together after the tool_result at line 1458.

### Messenger trail

- Store: envelope text at store lines 856235, 973876, 983760, 983761; body (prefixed by binary bytes rendered as `#`~`) at 856237, 973879, 997434, 1019473, 1019474. Adjacent metadata at 856236-856242 and 973877-973883: `2026-10-14T15:40:17.441617824Z`, `df159a13-abbb-4b94-bbe6-62fd8f79635b`, `psyche_flow_primary_df159a`, attempt `ead8b895-742d-44ed-b939-023dc60c388e` `Submitting`/`Uncertain`; `2026-10-14T15:40:17.640157411Z`, attempt `d652e1d9-54bc-43ab-a950-90455a55ec27` `Transported`; `term_65dc2d366759b7e`.
- Codex rollout line 1500 (`2026-10-14T15:40:16.852Z`, call `call_f3a1fcfe7db045fd855a8dfd6290c389`): `FLOW_ID=df159a hm-send "Psyche Flow Primary" "Follow-up: current untracked whitespace scan finds ..." 2>&1`, workdir `/home/li/primary`; output at line 1503 (`15:40:17.740Z`): `Transported.{ df159a working }`.

## Message 3

### Verbatim envelope

```
#msg ["Psyche Flow Primary" "Post-7899385 audit (transcript through 15:41:27): new dirty paths since prior audit are flows/df159a/books/12-flow-cli-deployment-long-term-2.html (SHA256 3b8927fa; 44/11 diff), .md (2a4192ba; 31/40), .refs.md (19cc5f94; 13 additions), and flows/df159a/handover.md (9d104dff; 6/2). These are attributable to the resumed Book12 second-edition revision/audit subflow and the main flow's handover update. Book12 Version 3 remains in flight/no final publish receipt in this transcript tail.\n\nExisting dirty/untracked paths remain: Book11 HTML c5c6d8cf (44/4 generated republish), log.md a1de3e04 (4 lines after 7899385), Book13 md 1a08660e (held/pre-existing), Book14 html 8535b98c, md eae32f6f, refs d97d9ffd (Book14 revision now completed/published Version 3 at 8crUc...; files remain untracked). No additional exact-path collision: only reservations flows/.df159a.flow-id and .lock; no same-basename Book14/13 files outside df159a. Index remains unstaged. git diff --check is clean for tracked paths. Untracked whitespace remains Book13 md L177, Book14 html L21/38/126/129 and md L62/83/132/135/144/148/157/174/217/220; Book12 and refs/handover/log are clean.\n"]
```

### Transcript location

- Line 1543: `queue-operation` `enqueue`, timestamp `2026-10-14T15:41:53.075Z`, no uuid.
- Line 1548: `queue-operation` `remove`, timestamp `2026-10-14T15:41:59.176Z`, no uuid.
- Line 1549: `attachment` `queued_command`, timestamp `2026-10-14T15:41:53.075Z`, uuid `639229ed-1ace-4b5d-b2b8-8356c455df91`, parentUuid `44e10203-f43c-41d6-9029-31f1630b6690`. Wrapped in `<pasted_content id="37ed">`.
- Preceding assistant action: line 1546 (uuid `c97b0b9c-fcc8-4b59-ba75-19ea898712c8`, `2026-10-14T15:41:58.237Z`), Bash tool_use "Log and report the republish" (appends a line to `flows/df159a/log.md` and runs `FLOW_ID=df159a hm-send "Psyche Flow Secondary" ...`); its tool_result at line 1547 (uuid `44e10203-...`, `15:41:59.152Z`): `Transported.{ da2038 working }`.

### Messenger trail

- Store: envelope text at store lines 516052, 536456, 536457, 587148, 819816, 819821, 959331, 959903, 999187, 999195; bare body at 788146, 819818, 959325, 959335, 999190, 1019599, 1019794, 1020794, 1020795. Adjacent metadata at 959324-959340: `2026-10-14T15:41:52.601065185Z` with attempt `d50f3bf8-dcb2-4124-84ff-401b704aa6b9` `Submitting`/`Uncertain`; `2026-10-14T15:41:52.792190862Z` with attempt `e05f3efa-84c8-45d4-ac17-68283be2535d` `Transported`; `df159a13-abbb-4b94-bbe6-62fd8f79635b`, `psyche_flow_primary_df159a`, `term_65dc2d366759b7e`.
- Codex rollout line 1558 (`2026-10-14T15:41:51.951Z`, call `call_99872f9f934e467bb538180a846c71e7`): `FLOW_ID=df159a hm-send "Psyche Flow Primary" --stdin <<'EOF'` with this body, workdir `/home/li/primary`; output at line 1561 (`15:41:52.918Z`): `Transported.{ df159a working }`.

## Message 4

### Verbatim envelope

```
#msg ["Psyche Flow Primary" "Fresh audit after commit e36386d6a: Book11 HTML is now clean/committed (no longer dirty). Current tracked dirty paths are only flows/df159a/books/12-flow-cli-deployment-long-term-2.html, .md, .refs.md; flows/df159a/handover.md; and flows/df159a/log.md. Current SHA256s: 3b8927fa (Book12 html), 2a4192ba (Book12 md), 19cc5f94 (Book12 refs), 9d104dff (handover), e97e1bad (log). The log gained one further line after the previous audit: third self-origin «Psyche Flow Primary» message, recorded at transcript 15:42:09. Book12 remains the in-flight Version 3 revision; no publish receipt in tail.\n\nUntracked paths unchanged: flows/df159a/books/13-flow-philosophy-artifacts.md; Book14 html/md/refs. Book14 Version 3 is complete/published; these files remain untracked. No self-origin report file is present in current status despite the transcript saying a report subflow is writing it. HEAD is e36386d6a; index has no staged paths. git diff --check is clean. No exact path collisions; reservations only flows/.df159a.flow-id and .lock.\n"]
```

### Transcript location

- Line 1581: `queue-operation` `enqueue`, timestamp `2026-10-14T15:42:29.170Z`, no uuid.
- Line 1584: `queue-operation` `remove`, timestamp `2026-10-14T15:42:37.695Z`, no uuid.
- Line 1585: `attachment` `queued_command`, timestamp `2026-10-14T15:42:29.170Z`, uuid `ffb71867-f86d-4636-8fce-e6c453bc7bb2`, parentUuid `85054d0e-ada7-421d-b91c-7d773d880262`. Wrapped in `<pasted_content id="37ed">`.
- Preceding assistant action: line 1582 (`2026-10-14T15:42:36.641Z`), Bash tool_use appending a Book 12 Version 3 line to `flows/df159a/log.md` and running `FLOW_ID=df159a hm-send "Psyche Flow Secondary" --stdin`; its tool_result at line 1583 (uuid `85054d0e-...`, `15:42:37.661Z`): `Transported.{ da2038 working }`.

### Messenger trail

- Store: envelope text (prefixed by a binary byte rendered as `-`) at store lines 597710, 597711, 771192, 944869, 945447, 948568, 948637, 996496, 996507, 1021677; bare body at 945449, 996500, 1021544, 1021547, 1021672, 1021681. Adjacent metadata at 945442-945456 and 996497-996509: `2026-10-14T15:42:28.672493774Z` with attempt `c1cdf921-c116-4014-a12e-5e3d88d4385e` `Submitting`/`Uncertain`; `2026-10-14T15:42:28.886555216Z` with attempt `537dc299-b57e-4377-943c-7536e32e44d5` `Transported`; `df159a13-abbb-4b94-bbe6-62fd8f79635b`, `psyche_flow_primary_df159a`, `term_65dc2d366759b7e`, and the string `Psyche Flow Primary` on its own line beside the body.
- Codex rollout line 1587 (`2026-10-14T15:42:28.020Z`, call `call_781c63f7925d49438752ffa0771a2674`): `FLOW_ID=df159a hm-send "Psyche Flow Primary" --stdin <<'EOF'` with this body, workdir `/home/li/primary`; output at line 1590 (`15:42:29.023Z`): `Transported.{ df159a working }`.

## Messenger sender resolution (source lines)

- `/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/core.clj` `sender-origin!` (line 524): the sender is `(or *flow-id* (System/getenv "FLOW_ID"))`; the route for that flow id is loaded and its `aspect topic layer` become the envelope's sender name (`metaflow!`, line 520). No other identity of the sending process is read.
- `append-attempt!` (line 388) persists `:id :at :flow :reason :grade`, request fields and `:binding route`, where `flow` and `route` are the target's; the typed store schema (`typed_store.clj`) has `:attempt/*`, `:attempt.binding/*`, `:pending/*`, `:route/*`, `:retirement/*` attributes and no sender attribute.
- Repository HEAD: `85e71b15a93360507cdcce8c2605f6479d650426` (2026-10-03). `grep -rl` for the four body strings inside the repository tree finds nothing; the only matches are in `~/.local/state/messenger-clj/typed-datalevin/data.mdb`. `~/.local/state/messenger-clj/retirement-evidence/` holds retirement files only.

## Committer side (evidence lines only)

- `/home/li/primary/tools/primary-committer/recipient.json`: `{"flow_id": "89fbc1", "metaflow": "Field PrimaryCommitting Quaternary"}`. `hm-list`: `89fbc1 field_quaternary_89fbc1 default working`. Store lines 1021554-1021555 pair native thread `01a13258-5fda-78c2-898b-10389fbc1701` with `field_quaternary_89fbc1`.
- This seat's Stop hook (`/home/li/.claude/jobs/native-df159a13-abbb-4b94-bbe6-62fd8f79635b/main-flow-settings.json`): `node /home/li/primary/tools/primary-committer/turn-end.mjs --primary /home/li/primary --committer 89fbc1`.
- `turn-end.mjs`: reads `recipient.json` for `committerMetaflow`; when Primary is dirty it runs `hm-send [committerMetaflow, '--stdin']` with `env` = the firing seat's environment (`FLOW_ID` = the editor's flow) and a fixed message naming `flow_id`, `session_id`, `transcript_path`, `primary`. Comment at the recipient read: "Runtime guard only; never an hm-send target." It contains no send toward the editing seat.
- `publish-selected.mjs`: requires `env.FLOW_ID === recipient` (line 56) and the `PrimaryPublish` lifetime lock (line 48); grep finds no `hm-send` or `#msg` in it.
- `codex-birth.mjs`: sets `shell_environment_policy.set.FLOW_ID` to the committer's own claimed flow id and installs `hooks.Stop` = `env FLOW_ID=<that id> node .../turn-end.mjs --primary <workspace> --committer <committer>`. `restart.mjs` line 167 launches the committer with `FLOW_ID: c.flow, CODEX_HOME: c.codexHome` and registers it with `register c.flow c.name --session ... --native-thread c.uuid`.
- `brief.md` line 9: "A turn-end message supplies the editor's actual claimed FLOW_ID ... Read that transcript and the current diff." Line 15: "For every hook firing, inspect the transcript and current owned-path diff after receiving that firing". No line in `brief.md`, `turn-end.mjs`, `publish-selected.mjs`, `restart.mjs` or `codex-birth.mjs` instructs a `#msg` to the editing seat or sets `FLOW_ID` to the editing seat's id.
- The Codex rollout that contains the four `hm-send` invocations lives under `/home/li/.codex-next-8mkkxq293hk2/`, the same home whose `config.toml` holds hook state and whose `sessions/2026/10/12/rollout-2026-10-12T17-00-14-01a13258-5fda-78c2-898b-10389fbc1701.jsonl` is the parent thread named in that rollout's `session_meta`. The invocations set `FLOW_ID=df159a` explicitly on the command line.

## Not done / unknowns

- The Datalevin store was read with `strings`, not through a typed query; attempt-to-field pairing above is by adjacency in the dump, and the duplicate occurrences are the store's own copies and indexes.
- The parent rollout `rollout-2026-10-12T17-00-14-01a13258-5fda-78c2-898b-10389fbc1701.jsonl` was not read; whether it ordered the subagent `Russell` to send under `FLOW_ID=df159a`, and the content of `/root/audit_288af9_firing`, were not examined.
- The `hm-send` printed receipts in the rollout are the only delivery receipts seen; no `Presented` grade was recorded for any of the four.
- The second coordinator message said the third body "mention[s] a commit 7899385"; Messages 1 and 2 do not name that commit, Message 3 names `7899385`, Message 4 names `e36386d6a`.
- `flows/df159a/log.md` lines that the bodies describe were not re-verified here.
