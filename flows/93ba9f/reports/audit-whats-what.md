## Summary (≤300 words)

**Flow / Message.** Three lines coexist on ouranos (the only host with evidence of either). Production: Flow 0.12.2 + Message 0.14.0, systemd-declared. "Next": Flow 0.17.0 + Message 0.17.0, running as *transient* `systemd-run` units under their own HOME/XDG_RUNTIME_DIR and `-next` socket tree — not declared in Home, one commit behind the 0.17.1 branch head. Clients take one inline Datom, no flags, no `--help`. Ordinary Flow: Start, Restart, ResolveRecipient, Stop, List, Replace, LaunchStatus, Observe, ResolveCaller. Meta Flow: Configure, ConsumeReset, RegisterFlow, MetaBindExisting, Retire, **Deliver**, **Vet**, **Command**, ResolvePeer — pane writing is meta-only. Ordinary Message: Send, Withdraw, Acknowledge, QueryReceipts, Observe. Meta Message: Configure, Send (stamped Owner), Redeliver. Production Message 0.14.0 speaks a wholly different, now-retired contract. Letters render as the typed datom itself, priority head first: `Soft.{ m-… Flow.e167d8 Text.«…» }`. Because production Flow cannot write panes at all, real production letters still go through messenger-clj as `#msg [...]` / `#psyche [...]`. messenger-clj installed 0.2.5, repo head 0.2.6.

**Field tool.** `field-clj` has exactly three operations: `#commit`, `#commit-to`, `#observe`. No version file — git-rev only; installed build is two commits behind head. **No Field Nexus exists** — no repo, no Ethos, nothing deployed. Mind Sol a676b3's safe-`#commit` rebuild has *not* landed and the seat has no flow directory at all. Redeploy pins are already current upstream; blockers are a stuck Lojix deployment, three disagreeing profile records, and an unresolved remote-builder defect.

**Transcripts.** The `transcript` CLI is confirmed missing from PATH; the repo exists (two commits, 2026-08-19) and is a flake input nowhere. `.flow-id` markers resolve flow → session → transcript reliably.

**Identifiers.** Almost every one carries far less entropy than its shape suggests; details below.

---

# Audit: what's what

Host: ouranos. Date: 2026-09-26. Grades: **[W]** witnessed (ran it, saw output), **[S]** source-read, **[I]** inferred.

---

## 1. Flow and Message

### 1.1 What they are

**Flow** (`/git/github.com/LiGoldragon/flow`) — the Flow Nexus. Starts, restarts, delivers to, stops, lists and resolves flows (agent seats), and from 0.15.0 onward is **the only writer into a pane**. Binaries: `flow-nexus` (long-running, no arguments), `flow`, `flow-meta`. [S]

**Message** (`/git/github.com/LiGoldragon/message`) — the Message Nexus: durable messages and receipts, delivered *through* Flow. Owns the message record, Priority, sender identity (named via Flow's `ResolvePeer`, never taken from the payload), the receipt ledger, parking until a recipient is at rest, and Read. Binaries: `message-nexus`, `message`, `message-meta`. **Message never touches Herdr** — it reaches a pane only through Flow's typed `Deliver`. [S]

### 1.2 Which versions run where

| Line | Flow | Message | Status |
|---|---|---|---|
| Production | **0.12.2** | **0.14.0** | running on ouranos [W] |
| Next | **0.17.0** | **0.17.0** | running on ouranos [W] |
| Working checkouts | 0.16.0 | 0.16.0 | detached HEAD, not deployed [S] |
| Branch heads `s1/s2-e167d8` | 0.17.1 | 0.17.0 | [S] |

Both repos sit on detached HEADs, not on `main`; `main` in each is still the 0.14.0-era commit. The 0.17 work lives only on `s1-e167d8` / `s2-e167d8`. [S]

**The "Next" pair is a second, parallel installation of the same pair on the same host**, isolated by its own HOME, XDG_RUNTIME_DIR and socket tree. The four scripts in `/home/li/.local/bin` are three-line shell wrappers: [S]

    # flow-next
    export FLOW_SOCKET="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/flow-next/flow/flow.sock"
    exec /nix/store/…-flow-0.17.0/bin/flow "$@"

Live on ouranos [W]: production `flow-nexus` 0.12.2 and `message-daemon` 0.14.0 from declared home-manager units; Next `flow-nexus` and `message-nexus` 0.17.0 from **transient** units (`flow-nexus-next.service`, `flow-configuration-next.service`, `message-nexus-next.service`) created by `systemd-run` in `/run/user/1001/systemd/transient/`, each labelled "(next, transient until Home deploy)", started 10:29 today. Herdr 0.8.2 runs as the terminal substrate underneath both.

Registries [W]: production `flow 'List.{}'` reports 17 flows; `flow-next 'List.{}'` reports 3 (93ba9f, b7ba00, e167d8), all Claude, all Active, all in Herdr session `messaging-build`.

Declared Home (`CriomOS-home` HEAD `4a9d85d7`) still pins the **old** pair. So what runs as Next is not declared anywhere; it exists only as transient units and evaporates on reboot. [S]

**No evidence Flow or Message runs on any host but ouranos.** I did not reach prometheus or zeus, so absence there is unconfirmed.

A stale figure to correct: `flows/e167d8/reports/status-2026-09-26-morning.md` says production Message is 0.12.0. The running daemon is 0.14.0, restarted 09:24 today. [W]

### 1.3 What each exposes — ordinary vs meta

The clients take **exactly one inline Datom** of their contract's `Query` type. No subcommands, no flags. `flow --help` is itself refused with a typed variant error. [W]

**Flow ordinary** (`flow`, `FLOW_SOCKET`) — contract `signal-flow` 7.0.0: [S]

> `Start` · `Restart` · `ResolveRecipient` · `Stop` · `List` · `Replace` · `LaunchStatus` · `Observe` · `ResolveCaller`

Replies: `Started`, `LaunchPending`, `StartAmbiguous`, `Restarted`, `RecipientResolved`, `Stopped`, `Listed`, `Replaced`, `CallerResolved`, `AgentObserved`, and the matching `*Rejected`. **Nothing on the ordinary socket writes into a pane.**

**Flow meta** (`flow-meta`, `FLOW_META_SOCKET`) — `meta-signal-flow` 10.0.0 in the 0.16 line, **11.0.0** in the 0.17 Next pair: [S]

> `Configure` · `ConsumeReset` · `RegisterFlow` · `MetaBindExisting` · `Retire` · **`Deliver`** · **`Vet`** · **`Command`** · `ResolvePeer`

`Command`'s `HarnessCommand` is `[ Compact Interrupt ]`; its outcome grade is `[ Transported Observed Uncertain ]`. The 11.0.0 bump adds `FlowRetired` and `FlowExited` to `DeliveryRejection` and `CommandRejection`. `flow-meta` also carries three argv conveniences on top of the datom form (`reset`, `register-codex`, `register-claude`). [W]

This is the concrete answer to the psyche's "a raw flow send should be a meta socket operation, and a more lock-enabled deliver message for messages": **it already is.** `Deliver` and `Command` are meta-only; the ordinary socket cannot write a pane.

**Message ordinary** (`message`, `MESSAGE_SOCKET`) — `signal-message` 7.0.0 (0.16) / **8.0.0** (0.17): [S]

> `Send` · `Withdraw` · `Acknowledge` · `QueryReceipts` · `Observe`

Replies: `Submitted`, `SendRejected`, `Withdrawn`, `Acknowledged`, `Receipts`, `ReceiptObserved`, `MessageRejected`.
`Priority.[ HardAbrupt MiddleAbrupt Soft ]`.
`Grade.[ Submitted Parked Transported Presented Uncertain Read Withdrawn Refused ]`.

**Message meta** (`message-meta`, `MESSAGE_META_SOCKET`) — `meta-signal-message` 0.7.1 (0.16) / **0.8.0** (0.17): [S]

> `Configure` · `Send` (stamped `Owner`) · `Redeliver`

The meta socket answers only the configured owner and flows whose aspect is in `MetaAspects`; anyone else gets `MetaRefused`. `Redeliver` is the only way out of `Uncertain`.

**Production Message 0.14.0 is a different contract entirely** — `signal-message` 5.0.0: `Submit`, `SubmitStamped`, `QueryInbox`, `AssignAgentIdentity`, `BindAgentEndpoint`, `QueryAgentRegistry`, `QueryThread`, `SubscribeThread`, `QueryThreads`, `FlowDeliver`, `FlowAnnounceIdle`, `Deliver` (carrying `ClusterMessage.Peer` / `.Relay`), `QueryDeliveryReceipts`. Threads, inbox, agent registry and cluster relay were **retired in 0.15.0**. This is a rewrite, not an increment. [S]

### 1.4 How letters look in panes today

Flow renders the typed `Message` as its own datom text, so the pane text's first byte is always the Priority head and no harness can read a leading capital as a command. The whole rendering is one line, in `flow/crates/flow-nexus/src/delivery/body.rs`: [S]

    impl RendersPaneText for Message {
        fn pane_text(&self) -> PaneText {
            PaneText { text: self.datomize(Vec::new()).protosize().textualize() }
        }
    }

Shape: `<Priority>.{ <MessageId> <Sender> <Content> }`, where `Sender` is `Owner` or `Flow.<flow-id>`, and `Content` is `Text.«…»` or `Psyche.{ context verbatim }`. Guillemets wrap any string containing a space.

Real letters, witnessed in Claude transcripts [W]:

    Soft.{ m-18d8ebe325f53059000 Flow.b1b544 Text.«Reply with only the word pong-78e335.» }
    MiddleAbrupt.{ m-18d8ebf3539045cf006 Flow.b1b544 Text.«Reply with only the word steer-8916cf.» }
    Soft.{ m-18d8ebf6d76a13da009 Owner Text.«Run the shell command sleep 90 …» }

Note the real MessageId is long — `m-18d8ebf6d76a13da009` — not the short `m-7f3a2c` used in the docs and the unit test. This is exactly the noise the psyche objected to.

Three refusal layers at the writer [S]: (1) priority head must be first; (2) no C0 control but LF/TAB, no DEL, no C1 — which is what keeps CR, ESC and an embedded bracketed-paste terminator out, since Herdr 0.8.2 `agent prompt` was witnessed passing them through unchanged; (3) a first line that is a harness command for the recipient's harness (`/compact`, `!ls`, `#remember`) is refused as `HarnessCommand`, telling the sender to use `Command` instead. Paths, later-line commands, and other harnesses' sigils pass.

The `DeliveryId` is Message's own per-attempt key and is **not** in the pane. The MessageId is, because it is what a recipient acknowledges by — it is the sole route to grade `Read`. That is the tension to resolve for the design book: the psyche has ruled "we shouldn't get the message ID" and "we're going to develop a different kind of interface to get message history", while the current Acknowledge path needs the recipient to hold it.

**The other letter form still in panes today** is messenger-clj's, because production Flow cannot write panes at all [W]:

    #msg ["e71dab" "Audit result: …"]
    #psyche ["93ba9f" "CONTEXT" "VERBATIM"]

Both forms appear in current transcripts. The typed `Soft.{…}` form appears only in the Next/sandbox flows.

### 1.5 messenger-clj

Repo `/git/github.com/LiGoldragon/messenger-clj`, detached HEAD, 2026-09-26. **Repo head 0.2.6** (bumped by "Add plural psyche and socket-safe large input"); **installed 0.2.5**, in two store paths — one behind `~/.local/bin/hm-*`, one behind `~/.nix-profile/bin/hm-*` from home-manager. [W]

**What it is still used for: everything real.** Production Flow 0.12.2 has no pane-writing code at all and production Message 0.14.0 speaks the retired ClusterMessage contract, so every actual inter-flow letter in production still goes through `hm-send`. Eleven commands live on PATH: `hm-send`, `hm-send-abrupt`, `hm-list`, `hm-register`, `hm-repair`, `hm-deregister`, `hm-rebind`, `hm-move`, `hm-retire`, `hm-heartbeat-state`, plus `messenger-clj`. It is a babashka script dispatching on `$0`, with a Datalevin pod for the typed ledger. [W][S]

It submits the complete `agent.prompt` through Herdr's typed Unix socket API — no cap, no splitting, no truncation — computing the exact serialized request size against Herdr 0.8's 1,048,576-byte limit and holding an oversized send durably as `RelayOverflow`. When no exact valid route exists it stores the envelope as pending and returns `Held.{ FLOW RepairRequired PENDING_ID }` with candidate evidence for a thinking flow to judge. Its grades — `Transported`, `Presented`, `Held`, `Uncertain` — are the direct ancestor of what Flow 0.15+ absorbed into typed `Deliver`.

**The Next pair is the replacement for messenger-clj; it is not yet the replacement in production.**

---

## 2. The field tool

### 2.1 What `field-clj` is

Repo `/git/github.com/LiGoldragon/field-clj`. Clojure, ~5 source files, built to an AOT JVM uberjar through `clj-build`. [S]

It takes exactly one inline EDN argument (datom-emulating tagged literals), makes a fail-closed, path-scoped Jujutsu commit for the calling flow, moves `main`, pushes, verifies the commit is present at the real remote URL, and prints one EDN result validated against a Malli `Output` schema. Caller identity comes from `FLOW_ID`; unset gives `#refused :no-caller`, which is why a bare run refuses. Exit 0 on `#success`/`#observed`, 1 on `#refused`, 2 on schema breach. [S][W]

**Complete operation list — three, no more** (`schema.clj`: `(def Command [:or Commit CommitTo Observe])`): [S]

| Input | Meaning |
|---|---|
| `#commit [message [path ...]]` | scoped commit + bookmark + push + remote verification |
| `#commit-to [message [path ...] remote-url]` | same, naming the URL verification reads |
| `#observe []` | read-only: `systemctl --user is-active flow-nexus.service`, `flow 'List.{}'`, `herdr api snapshot` |

No flags, no subcommands. Legacy forms are refused as `:invalid-command`. I ran `#observe` only; it returned `#observed` with all three surfaces `:available`. [W]

**Versions.** There is **no version file** — `field-clj` is versioned by git revision alone. Real remote head is today's "clj-build 8cc9991 (CLI-independent deps FOD)" commit. The local checkout is detached, on no branch, one commit behind, and its `origin/main` ref is stale too. The **installed** uberjar is from "Add read-only runtime observation" (2026-09-25), **two commits behind head** — proven by comparing the deps FOD's `deps.edn` byte-for-byte against each candidate revision, not inferred. So `#observe` is installed and works, but the CLI-independent deps pin and the clj-build bump are not. [W]

### 2.2 Is there a Field Nexus?

**No. It does not exist as code.** [W][S]

- No `field-nexus` repo, no `signal-field`, no `meta-signal-field` — despite dozens of `signal-*` / `meta-signal-*` pairs existing for mind, psyche, flow, orchestrate, lojix and others.
- `/git/…/field` is not a nexus: Node.js read-only inventory scripts plus systemd units its own README calls "installation artifacts only… not enabled or deployed by this repository."
- `/git/…/nexus` is the generic Rust Nexus library (0.5.0). No field code.
- **Ethos: zero** `*.ethos` files and zero `ethos/` directories in `field`, `field-clj`, or `nexus`. This matches the 2026-09-25 Field audit: "no field ethos exists."
- **Deployed: nothing.** No field socket, no field-nexus process. There are four `field-*.timer` units, but they run the Node scripts.

Status of the idea: `flows/1ac573/reports/field-nexus-concept.md` (2026-09-18) states at the top "Requested by the living as concept only. Nothing implemented, nothing deployed", and ends with seven open questions that appear still open. The 2026-09-25 Field audit says plainly "No Rust Field tool exists. The Field tool is `field-clj`", framing field-clj as the `-clj` prototype of a Field Nexus, to be rewritten in Ethos and Rust later.

So when the psyche says "either Field Nexus or the Field CLJ, whichever is most ready", today that can only mean field-clj.

### 2.3 Who is working on it — Mind Sol a676b3

a676b3 is a real, registered, live Codex flow, but it is **not** visibly working right now.

- Flow registry: state **Pending**, not Active. Herdr shows the pane `agent_status: "done"`, `interactive_ready: true`, tab "Mind Sol a676b3". Idle and waiting. [W]
- **It has no flow directory anywhere on disk** — no lane, no reports, no witnesses of its own. Everything known about it is second-hand from other flows' logs. This is the single biggest evidence gap in this audit. [W]
- It holds **no Orchestrate lock** now; its earlier locks are all released. [W]

Timeline, reconstructed from other lanes [S]:

- 2026-09-25 19:57Z — launched by Mind Sol 00f95a through the native-seat launcher, for field-clj.
- 2026-09-25 night — pushed the `#observe` commit plus consumer pins in CriomOS-home and CriomOS; 34 tests / 167 assertions passing, offline flake check green. Explicitly reported **no activation, no PATH change, no builder evidence**.
- 2026-09-26 — b7da5d's Lojix deployment 34 failed on a `field-clj-deps` FOD hash mismatch. That is what the "pin clojure 1.12.6 so the deps hash is CLI-independent" commit fixes.
- 2026-09-26, before ~10:15 — b7ba00 witnessed via `jj op log` that a `#commit` refusal ran `jj op restore` and **rewound four refused commits plus every other flow's operations since the mark**, and an `import-git-head` replaced b7ba00's working copy. e167d8 then ordered **every flow to stop using `field-clj #commit` in primary** until a676b3's rebuild lands — broadcast to nine live registrations.
- Same day — a676b3 reported its plan: owned landing workspace, per-path three-way merge from the caller's disk, per-repo Datalevin lease plus landing records, fetch-and-remote-equality check, bounded push retry, fast-forward only, refusal cleaning only its own commit, `#observe` kept; unit plus two-process race tests. ETA 2–3 h. It confirmed the current head unsafe.

The written spec it is working to is `flows/e167d8/reports/per-flow-workspaces-design.md` §4 and §4a (authored by e167d8, not a676b3): `--ignore-working-copy` for every read of the caller's workspace, a dedicated `field-land` jj workspace, a Datalevin LMDB landing lock, and an explicit note that the chosen Datalevin API's cross-JVM atomicity is unverified and must be proven by racing two processes.

**Actual state: the safe-`#commit` rebuild has not landed.** Remote head is only a clj-build bump; `commit.clj` and `jj.clj` still contain the `jj op restore` design. Latest recorded a676b3 activity is 2026-09-26 before ~10:15. Whether it is still working, stalled, or finished-and-idle **could not be established** — it has no lane to read, and I did not message it.

### 2.4 What "redeploy it at the latest version" would take

The chain: `field-clj` git → pinned in `CriomOS-home/flake.lock` → consumed at `modules/home/profiles/med/cli-tools.nix` → `CriomOS/flake.lock` pins criomos-home → Lojix deploy (cluster `goldragon`, node `ouranos`) → UserEnvironment / HomeManagerNixProfileV1 → `~/.nix-profile`.

| Link | vs latest |
|---|---|
| field-clj real remote main | **latest** |
| CriomOS-home real remote main | pins field-clj head — **already current** |
| CriomOS real remote main | pins a criomos-home that pins field-clj head — **already current** |
| local `/git/…/CriomOS-home` | **stale, 3+ commits behind** |
| local `/git/…/CriomOS` | **stale** |
| Lojix deployment 39 (`Evaluate`, Succeeded) | one field-clj commit behind |
| Lojix deployment 38 (`TestActivation`) | **stuck in `Copying`, never terminal** |
| live `~/.nix-profile` | **two commits behind** |

**So the work is not "bump the pin" — the pins are already done upstream.** What redeploying needs:

1. Refresh the stale local checkouts. Anyone reasoning from the on-disk copies of field-clj, CriomOS-home or CriomOS is reading yesterday's state.
2. A Lojix `UserEnvironment` deploy against current CriomOS main: cluster `goldragon`, node `ouranos`, user `li`, backend `HomeManagerNixProfileV1`, action `Realize` then `ActivateNow`, source revision policy `RequireImmutable`, explicit builder for Prometheus offload. This is an **owner-socket** operation and was not run.

What is blocking or stale:

- Deployment 38 has been in `Copying` and never reached terminal; host generation is unchanged.
- **Three records disagree.** Lojix's recorded "Current" UserEnvironment generation points at a store path that **does not exist locally**; `~/.local/state/nix/profiles/home-manager` is at a generation from 2026-09-24 whose home-path has no field-clj at all; and the live `~/.nix-profile` was updated 2026-09-26 15:24 UTC by an unknown route. Who performed that activation could not be established.
- **The remote-builder route is a known, unassigned defect**: the `max-jobs=0` offloader could not authenticate as `nix-ssh`, so a messenger-clj build ran by direct ssh on Prometheus.
- The deps FOD mismatch is fixed in source but has not been proven on a builder — no Lojix deployment exists at a revision pinning the current head.
- **The standing rule cuts against the redeploy.** Every flow was told to stop using `field-clj #commit` in primary until a676b3's rebuild lands. Redeploying the current head puts the *same unsafe `jj op restore` `#commit`* on PATH: it is a deps/build fix, not the safety rebuild.

---

## 3. Transcripts

### 3.1 The `transcript` CLI — confirmed missing

`/home/li/primary/.claude/skills/transcript-search/SKILL.md` names `transcript show <session>`, `transcript search <pattern> --recent <n>`, `transcript raw <session> <lines>`, plus `--assistant`. [S]

**It is not installed.** `which transcript` → not found; nothing named `transcript` anywhere on PATH; not in `~/.nix-profile/bin` or `~/.local/bin`. [W]

The repo `/git/github.com/LiGoldragon/transcript` exists: `flake.nix`, `flake.lock`, `README.md`, and a single dependency-free `transcript.py`. The flake does build a binary of exactly that name. **Two commits, both 2026-08-19; nothing since.** [W] Its README self-describes as "Temporary, pending a Nexus", and it is Claude-only — the code contains zero occurrences of "codex" or "rollout".

**It is not packaged anywhere.** Grep for "transcript" across CriomOS `*.nix` → no hits at all. In CriomOS-home the only hits are prose comments. `github:LiGoldragon/transcript` is **not a flake input** and is in no profile — unlike its sibling shims `substack-cli`, `claude-answers`, `listener`, `harness`, `spirit`, `agent`, `aggregator`, `orchestrate`, `message`. [W]

The generated skill is byte-identical to its authored Curriculum source, last touched 2026-08-26. So the skill is faithful to its source; the source has simply never been reconciled with the fact that the tool was never packaged. **The skill instructs every flow to use a command that has never existed on this machine.**

It does work when run directly, today [W]:

    python3 /git/github.com/LiGoldragon/transcript/transcript.py search "psyche" --recent 2
    python3 /git/github.com/LiGoldragon/transcript/transcript.py show 93ba9ff6 -n 1 --cap 80
    python3 /git/github.com/LiGoldragon/transcript/transcript.py raw  93ba9ff6 41

Its resolver accepts an absolute path, a full UUID, or **any prefix** — so a 6-hex flow ID resolves directly for Claude sessions.

### 3.2 What tooling actually exists

| Tool | Harnesses | State |
|---|---|---|
| `transcript.py` (repo path) | Claude only | works via `python3 <path>`; not on PATH [W] |
| `claude-answers` 0.5.1 | Claude only | **installed, working** [W] |
| `/home/li/primary/tools/extractor/` | **Claude + Codex** | `inventory` works; `extract` needs a model [W] |
| `/home/li/primary/tools/field-census.mjs` | both | has a flow→transcript resolver [S] |
| subflow-scripts | — | **catalogued only, not implemented** [W] |

- `claude-answers` is narrow: it recovers *your answers to Claude Code's interactive questions*, not general transcript text. One Datom query argument: bare (`Latest`), `All`, `Session.<substring>`, `File./abs/path.jsonl`, `Grep.{ … }`. Output is canonical Datom. No `--help`. [W]
- `tools/extractor` is the only thing that reads **both** harnesses: `_codex_block` handles `response_item`/`message`, `function_call`, `function_call_output`, `inter_agent_communication_metadata`; `_claude_block` handles `user`/`assistant`. It emits source-addressable blocks carrying session UUID, timestamp, JSONL line, byte interval, path and SHA-256 of the source. But `extract` calls `select_with_luna` — it needs a model, it is not a grep. Witnessed inventory: **5967 rollouts, 12.64 GB, ~3.16 B estimated input tokens at full text.** [W]
- `.claude/skills/subflow-scripts/SKILL.md` catalogues `find-codex-session`, `queue-to-codex`, `read-transcript-tail` — the directory contains **only SKILL.md**. These are briefs for subflows, not executables. [W]

**No installed binary searches Codex transcripts.** The only Codex-capable reader on disk needs a model to select.

### 3.3 Where transcripts live

**Claude — `/home/li/.claude/projects`**: 2.3 GB, 46 project dirs, 2964 `.jsonl`. Layout `<encoded-cwd>/<session-uuid>.jsonl`, where encoded-cwd is the absolute cwd with every non-alphanumeric character replaced by `-`, case preserved. Worktrees get their own dirs. JSONL, mixed record types (`mode`, `permission-mode`, `bridge-session`, `custom-title`, `agent-name`, `system`, `attachment`, `user`, `assistant`, `file-history-snapshot`). `user`/`assistant` records carry `parentUuid, isSidechain, type, message{role,content}, uuid, timestamp, sessionId, cwd, gitBranch, version, userType, entrypoint, promptId`. `sessionId` equals the filename stem. [W]

**Codex — `/home/li/.codex/sessions`** (11 GB, 2997 files) and **`/home/li/.codex-next/sessions`** (1.1 GB, 306 files). Layout for both: `<YYYY>/<MM>/<DD>/rollout-<YYYY-MM-DD>T<HH-MM-SS>-<thread-uuid>.jsonl`. **The filename timestamp is local time; the timestamp inside is UTC.** Every record is `{timestamp, ordinal, type, payload}`; types include `session_meta`, `turn_context`, `response_item`, `event_msg`, `token_usage_record`, `world_state`, `inter_agent_communication_metadata`. `session_meta.payload` carries `id` (the thread UUID in the filename), `session_id`, `parent_thread_id`, `cwd`, `originator`, `cli_version`, `thread_source`, `agent_nickname`, `agent_role`, `agent_path`, `model_provider`, and the full `base_instructions.text`. [W]

**Trap:** for a subagent rollout, `payload.session_id` ≠ `payload.id` — `session_id` is the *parent* thread. Match on `payload.id` / the filename UUID. Current flows write to `.codex-next`; `.codex` holds the older, larger history. **Both are live roots and both must be searched.** [W]

### 3.4 Flow ID → session → transcript

**The authoritative mechanism is the `.flow-id` marker file, and it works end to end.**

Files are `flows/.<alias>.flow-id` — dot-prefixed, *beside* the `flows/<alias>/` directory, not inside it — each with a sibling `.lock`. 202 such files. Plain `key=value`: [W]

    version=1
    harness=claude
    identity=<32-hex undashed session uuid>
    alias=93ba9f
    uuid-version=uuid-v4

`identity` is the undashed 32-hex native session/thread UUID. Codex records have no `uuid-version` line.

Working procedure, witnessed on three real flows: read `harness` and `identity` from the marker, re-dash the identity into canonical UUID form, then for Claude `find /home/li/.claude/projects -name "$U.jsonl"`, for Codex `find /home/li/.codex/sessions /home/li/.codex-next/sessions -name "*$U*.jsonl"`. Resolved 93ba9f (Claude), b7da5d (Codex, `.codex-next`) and 553901 (Codex, `.codex`) correctly. [W]

**Do not derive the identity from the alias** — for Codex the alias is a slice from the middle, not a prefix (see §4.1).

The writer is `/home/li/.nix-profile/bin/flow-id`, from the `harness` flake input:

    usage: flow-id codex  --flows-root ABSOLUTE_DIRECTORY
           flow-id claude --flows-root ABSOLUTE_DIRECTORY --parent-session UUID

Codex self-identifies from `$CODEX_SESSION_ID`; Claude is claimed by its *parent* passing the session UUID. [W]

Three other registries exist; rank them below `.flow-id`:

1. `/home/li/.local/state/hacky-messenger/<flow-id>.json` — 43 files, 38 with `native_thread`, and when `readiness_proof` is present it gives the rollout path outright. **But it is stale**: no entry for 93ba9f, b7ba00 or e167d8, three flows `hm-list` currently reports as live. Legacy, superseded. [W]
2. `hm-list` — lists live flows as FLOW / AGENT / SESSION / STATE. **It never prints a UUID or a path**, and `--json` is rejected. Good for liveness, useless for resolution. [W]
3. messenger-clj's Datalevin store (100 MB) does hold the full UUID, but **no CLI verb exposes it**. [W]

`tools/field-census.mjs` implements this mapping in code, with two limitations: it indexes only `~/.codex/sessions`, **not** `~/.codex-next/sessions`, and it hardcodes the Claude project dir as `-home-li-primary`, so it misses worktree sessions. [S]

**Herdr is not a resolver.** Its session.json maps panes → agent names, with no session UUIDs anywhere.

**Gap:** 305 flow directories vs 202 markers. The unmatched ones are mostly full-length ids under an older convention (see §4.1).

---

## 4. Hash-shaped identifiers in daily use

The through-line: **almost every identifier in daily use looks like a hash and is not one.** Most are clocks or counters. The ones with real entropy have less than their width suggests.

### 4.1 Flow IDs

Source: `harness/src/flow_id.rs`, `pub fn claim(harness, flows_root, identity)`; CLI `flow-id`; called by the Flow Nexus at `flow/crates/flow-nexus/src/herdr/launch.rs` (`claim_flow_identity`). [S]

**It is not a hash and not random. It is a substring of the harness's own session UUID.**

    const FIRST_CANDIDATE_LENGTH: usize = 6;
    const CODEX_CANDIDATE_START:  usize = 23;

`claim()` normalizes the UUID to 32 lowercase hex, then walks candidates `identity[start .. start+6]`, `[start .. start+7]`, … up to 32, taking the first it can claim.

- **Claude:** `start = 0` → the first 6 hex of the Claude session UUIDv4. [W]
- **Codex:** `start = 23` → hex chars 23–28 of the Codex session UUIDv7. Verified programmatically against **all 202 markers**; only 3 exceptions, each explained below. [W]

Format: `^[0-9a-f]{6,32}$`, lowercase hex, enforced twice. In practice always 6.

**Entropy:**

| Harness | Real randomness |
|---|---|
| Claude (UUIDv4) | **24 bits** — chars 0–5 are pure CSPRNG output |
| Codex (UUIDv7) | **~24 bits** across sessions in different milliseconds; **20 bits guaranteed** if two are minted in the same millisecond (char 23 is the last nibble of the `uuid` crate's 42-bit `ContextV7` counter, reseeded from 41 random bits each new ms) |

Measured, not assumed: per-position Shannon entropy over the 131 v7 identities on disk gives ≈3.94 bits at position 23 and ≈3.93 at 24–28, summing to ≈23.6 bits. [W]

The Codex offset of 23 is deliberate and correct: chars 0–11 of a v7 are the millisecond clock and char 12 is the literal `7`, so a prefix-derived alias would be a timestamp, not an identifier.

**Why three lengths exist on disk.** 159 six-char, 145 eight-char, one twenty-one-char. (The "12-char" in the brief is wrong — `019fe121` is 8 chars.) [W]

- **The 145 eight-char lanes are legacy, and every single one is markerless** — exactly `Lane::Legacy`. They were minted by a pre-`flow-id` convention taking the first 8 hex of the session UUID. Of these, 83 begin `01a0`/`019f` — Codex v7 **timestamp prefixes** carrying **≈0 bits of entropy**, a clock reading with 65.536-second granularity. The other 62 are Claude v4 first-8, 32 bits.
- **Seven-char aliases** arise from the loop extending on collision — but not from a birthday collision. `.836818c` exists because lane `836818` is one of the 11 markerless legacy 6-char lanes, which `claim()` skips via `Lane::Legacy => continue`.
- **Two Claude markers carry offset-23 aliases**, minted before the harness commit that introduced the `start = 0` branch for Claude.
- `flow-0000000000000001` is a **test fixture leaked into the real tree** — the literal appears only inside `#[cfg(test)]` in `codex.rs`. Its directory holds only an empty `reports/`.

**Collisions.** 24 bits = 16.78M. At the current ~148 live flows, P ≈ 0.06%; at 1000 flows ≈ 2.9%; expected first collision around n ≈ 4822. The *design* handles it — `claim_candidate` returns `Candidate::Collision` and lengthens the alias — but the *convention* everywhere else (skills, lock names, agent names, titles) assumes exactly 6, so a 7-char flow id will surprise anything pattern-matching `[0-9a-f]{6}`.

Worth noting for the book: marker decode cross-checks the recorded `uuid-version=` against the identity's version nibble and **rejects an untyped v5 claim**, because a v5 Claude session id would be SHA-1-derived rather than random. The code refuses to silently inherit that provenance. No v5 marker exists on disk.

### 4.2 Message and delivery IDs

Three unrelated systems. Flow mints none of them.

**MessageId** (`message` 0.17) — `message-nexus/src/ledger.rs`, `RecordsReceipts::new_message_id`: [S]

    let count = self.message_count.fetch_add(1, Ordering::Relaxed);
    format!("m-{:x}{:03x}", Self::now(), count % 0x1000)

`now()` is `SystemTime::now().as_nanos()`. `message_count` is a **per-process** AtomicU64, not persisted. Regex `^m-[0-9a-f]{16}[0-9a-f]{3}$`, 21 chars at the current epoch. Witnessed: `m-18d8eb22e06706ef001`. **Entropy: 0 bits** — nanosecond clock plus a 12-bit counter that resets on every Nexus restart. Fully predictable. The store uses the raw id as record key with **no duplicate check on insert**, so two Nexus processes on one store could silently collide. [W][S]

**DeliveryId** — `message-nexus/src/delivery.rs`, `Addressee::delivery_id`: `format!("{}:{}:{attempt}", message_id, flow_id)`. Witnessed: `m-18d8eb22e06706ef001:e167d8:0`. Purely derived, **0 bits**. It is an idempotency key — Flow looks it up for replay/dedup. Attempt increments only via `Redeliver`. [S][W]

**messenger-clj has no message id at all.** Its only minted identifier is the DeliveryAttempt id: `(str (java.util.UUID/randomUUID))` — **UUIDv4, 122 bits** from SecureRandom. Flows see a truncated `attempt-<first 12 chars>`. Its Orchestrate lock name is `"MessengerCljDelivery-" + dashless uuid4`. [S][W]

**Not established:** the writer of `flows/*/messages/<ns-timestamp>-<flowid>-<uuid4>.md`. Two filename generations are witnessed on disk, but **no code in `message`, `messenger-clj`, `flow`, or any repo under `/git/github.com/LiGoldragon/` constructs that path**. Most likely an agent-side convention, but no skill prescribes it either.

### 4.3 Launch request IDs

**The Nexus does not generate these — they are caller-supplied free text.** Validation only, in `flow/crates/flow-nexus/src/composition.rs` (`ValidatesLaunchProfile::validate`): non-empty, every byte in `[A-Za-z0-9._:-]`. `LaunchRequestId` is `pub type = String`. Witnessed real values: `fable-successor-b860be`, `opus-successor-e167d8`, `mind-astra-of-f5a74e` — human-authored, embedding 6-hex flow ids, uniqueness by convention only. **Entropy: 0 bits** in the general case. [S][W]

**The derived short form is a real hash** — `composition.rs`, `impl ShortensLaunchRequest for str`: [S]

    const SHORT_FORM_LENGTH: usize = 16;
    let digest = format!("{:x}", Sha256::digest(
        format!("flow-remote-control-v1\0{self}").as_bytes()));
    digest[..Self::SHORT_FORM_LENGTH].to_owned()

**First 16 hex chars (64 bits) of SHA-256 over the literal `flow-remote-control-v1\0` followed by the launch request id.** Used for the Claude remote-control name `flow-<16hex>` and the per-launch bundle copy `launch-<16hex>.md`. Deterministic, **0 bits of randomness** — it inherits exactly the entropy of the caller's string. It is a collision-avoidance device between distinct ids, not a secret.

**Documentation drift:** `/home/li/primary/flow/README.md` and `UPGRADES.md` still say "first eight hex digits". The code and the real repo README say sixteen; it was raised in 0.10.5. `/home/li/primary/flow` is a stale copy of the repo. [W]

**Herdr identifiers** (adjacent, also in daily use) [W]: `terminal_id` = `term_` + 15 hex, whose **leading 13 hex are microseconds since the Unix epoch** — verified against pane creation time. The trailing 2 hex are counter or randomness [I]. Effectively **0 bits**: it is a timestamp. `workspace_id` = `w` + a short base-36-ish counter; `pane_id`/`tab_id` are `<workspace>:p<n>` / `:t<n>`. Agent `name` is role-and-flow-id text, except Claude's default `claude-` + 24 hex, whose generator was not established (Herdr is third-party, no source on disk).

### 4.4 Orchestrate Lock IDs

Source: `orchestrate/crates/orchestrate-nexus/src/store/transition.rs`, `impl Locks :: fn lock` — `request.into_lock(allocator.next_lock_id)`, incremented and asserted in one atomic commit. Allocator seeded to 1. [S]

Format: bare decimal `i64`, `1 ..= i64::MAX`. Wire form `Release.7359`. **Entropy: 0 bits** — a monotonic counter; no RNG, no clock, no PID anywhere on the path. Persisted in family `lock_id_allocator_v2`, key `"next"`, in the Nexus's sema store.

**It does not reset on Nexus restart** — the anticipated ambiguity does not exist. There is a named test for it, and live ids span 440 → 7558 while the current process started 2026-09-12. Ids are never reused within a store; release retracts the row without rolling the counter back. **Across stores they are meaningless** — a rebuilt store restarts at 1 and re-mints 1, 2, 3 for different Locks, and nothing in the id names its store. [W][S][I]

**Security finding worth raising separately.** `Releases::release` looks up **by id alone** and does not compare the caller's `flow_id` to the Lock's owner. Combined with a 0-entropy, densely packed, trivially enumerable id space and an ordinary socket that admits any peer the filesystem allows (socket is `srw-rw----`, group `users`), **any flow can release any other flow's Lock by guessing its number.** The Lock id is an index, not a capability. [S]

Orchestrate mints nothing else. `FlowId` and `LockName` are caller-supplied strings never validated for shape — live Locks currently carry a 6-hex id, a full UUID, and bare prose side by side. [W]

### 4.5 Commit ids shown to agents

**field-clj `#commit` prints a full 40-char git SHA-1.** `jj.clj`: [S]

    (def ^:private commit-id-template "commit_id ++ \"\\n\"")

Bare `commit_id` — no `.short()`, no `.shortest(n)`. It runs `jj log -r @- --no-graph -T` with that template and the result reaches the agent untruncated via `(println (pr-str result))`. The schema only requires `^\S+$`. Witnessed in a real receipt: `#success ["38de5b" "<40-hex>" ["README.md"] :main :pushed :present]`. [W]

**jj change ids appear nowhere in field-clj.** The only other id it handles is the jj *operation* id, full length, for rollback.

**What `jj log` shows in primary** (colocated `.jj` + `.git`, jj 0.44.0): left column is the **jj change id** — 128 bits, 32 chars, alphabet **k–z** (16 letters, 4 bits/char) — displayed as **8 chars** via `format_short_id(id) = id.shortest(8)`. 8 is a *floor*; the actually-disambiguating prefix is often shorter (3 in one witnessed case). Right column is the **git commit id in hex, 8 chars**, same rule. `jj st` prints no ids at all. [W]

**git:** SHA-1, 160 bits, hex. `core.abbrev` is unset in every scope; with ~162.7k objects git abbreviates to **9 chars** here. That is 36 bits, and it is **not stable** — it grows with the object count. [W][I]

**No rule in the repo prescribes a commit-id length**, and the two rules that exist point in opposite directions: [W]
- `testing-push-landed/SKILL.md` mandates comparing **full 40-char** values (`jj log -T 'commit_id'` vs `git ls-remote`).
- `subflow-scripts/SKILL.md` forbids a subflow script from returning "any hex run of 16 or more characters".

**A subflow proving a push cannot satisfy both.** Every other "N characters" rule in the repo is about flow ids or session ids, not commits.

### 4.6 Codex thread UUIDs

3198 distinct UUIDs across 2996 live + 201 archived rollouts, **zero collisions**, spanning 2026-07-24 → 2026-09-26. [W]

**Version: UUIDv7, uniformly, with no v4 era.** Version nibble `7` × 3198; variant nibble uniform over `{8,9,a,b}`. A further 784 distinct ids in `history.jsonl` back to 2026-02-04 are all v7, across cli_version 0.142.5 → 0.153.4. (The Electron side does use v4 — a different generator.) [W]

**Timestamp verified:** first 48 bits are big-endian milliseconds Unix time. 61/61 sampled files decoded to within 1–28 ms (median ~6) *before* the session's own recorded timestamp. [W]

**Entropy: 72 bits, not the nominal 74.** `rand_a`'s low nibble (hex position 15) is restricted to `{0,1,2,3}` in **all 3198** UUIDs — two bits are structurally zero. Cause found in the vendored generator: [S]

- `timestamp.rs`: `const USABLE_BITS: usize = 42;` — a 42-bit monotonic counter
- `RESEED_MASK = u64::MAX >> 23` — reseeded from **41 random bits** each new millisecond, incremented within a millisecond
- `v7.rs::new_v7` shifts the counter around the variant field, inserting the two zero bits that land in `rand_a`
- randomness is `getrandom::fill` (OS CSPRNG), non-`fast-rng` path

So **10 effective rand_a bits + 62 rand_b bits = 72 random bits.** The bit signature also proves Codex calls `Uuid::now_v7()` with the shared `ContextV7`, not `NoContext`. The same signature holds for internal `turn_id`, `thread_id`, `root_turn_id`, `window_id` and item `id` (270 sampled). `thread_id == session_id ==` the filename UUID. Server-side ids in the same file (`msg_…`, `rs_…`, `resp_…`) are opaque and not UUIDs. Nothing here is configurable. [W][S]

**The 65-second prefix result** — why 8-char Codex lanes were a bad identifier: [W]

| leading hex | distinct over 3198 | change period |
|---|---|---|
| 4 | **2** | ~49.7 days |
| 6 | 195 | ~4.66 h |
| **8** | **2237** | **65.536 s** |
| 10 | 3183 | 256 ms |
| 12 | 3198 | 1 ms |

630 prefix groups hold 2+ sessions; the largest holds 7, minted over 56.0 s. **Maximum observed span inside any shared 8-char prefix: 61869 ms — under 65536, exactly as the arithmetic requires.** This is the direct measurement behind `CODEX_CANDIDATE_START = 23`.

### 4.7 Cross-namespace confusability

Ranked by how likely it is to actually bite.

1. **6-hex flow id vs abbreviated git commit — already collided in the real tree.** `f55ec8` is a live flow lane **and** resolves in primary to a real commit. `git cat-file` will happily accept a flow id. (It is the only one of the 159 six-char lanes that currently resolves.) [W]
2. **8-hex legacy flow lanes vs jj's 8-hex commit column.** Identical alphabet, identical width, both appear in flow logs. None currently resolves as a commit, but the shapes are indistinguishable by inspection. [W]
3. **Flow ids sitting adjacent to commit ids in the same `jj log` line** — a bookmark *named after a flow id* one word from a commit id, two hex-ish tokens from different namespaces. [W]
4. **jj change id vs git commit id, both 8 chars in adjacent columns.** The easy pair: change ids are k–z only (no digits, no a–j). Trivially separable once you know the rule, invisible if you don't.
5. **`01a0…` legacy lanes vs Codex UUID prefixes** — 83 lanes share it; it means "minted in this ~49-day window", not an identity.
6. **Launch-request short form (16 hex) vs the subflow-scripts rule** that strips any hex run of 16 or more characters — a `launch-<16hex>` name sits exactly at that threshold and will be scrubbed from subflow output. [S]
7. **Orchestrate Lock ids vs anything numeric.** Small decimals with no prefix or sigil; `7359` in prose is indistinguishable from a count.
8. **MessageId's 16-hex nanosecond body vs a truncated digest.** `m-18d8eb22e06706ef001` looks hash-like and is pure clock.

---

## 5. Word identifiers — the name-based hash the living asked for

*(Added at the coordinator's request.)*

### 5.1 What the living asked

> Let's do the name-based hash thing in the signal library. Give it a sensible name, give it a sensible anatomy, and then show me everything. We can always change it and rewrite it later. It's fine.

— psyche, typed, `flows/fd0f97/vision/identifiers.md` [S]

Earlier and later rulings in the same line of work:

- **692df8** — identifiers are real types, not strings: an Ethos library of identifier types on datom's own hashing types; a UTF-8 base legal in datom; bit-typed ids ("this ID is a 36-bit identifier"). Then: a readable alphabet, **perhaps words**, since the only cost is the LLM token cost; **three security levels by how bad a collision is** — local/private vs cluster vs public namespace; and Signal is the right home ("sema is storing Signal, so it's all Signal").
- **05c604** — "This is genius when we use this word-based system, BIP39. Is there a newer one that has more bit density?"; and ids should be visually distinguishable at a glance, with **camelCase for ids against PascalCase for typed objects**, if the LLM tokenizes it efficiently.

### 5.2 It was built — on a branch, not on main

**Repo:** `/git/github.com/LiGoldragon/signal`, crate `signal` 7.0.0.
**Branch:** `proposal/5f4fea-word-identifiers` (pushed to origin), checked out as the worktree `/git/github.com/LiGoldragon/signal-5f4fea-word-identifiers`. Head "Correct identifier proof grammar and validation", 2026-09-15. A second, **local-only** branch `proposal/cf7879-word-identifiers-validation` carries two further commits ("Validate archived word identifier references", "Conform identifier schema and decode checks") plus build-input tracking. [W]

**`signal` main does NOT contain it.** `git merge-base --is-ancestor` → NOT-MERGED; `main`'s `src/` is `accord.rs, exchange.rs, frame.rs, generated/, lib.rs, portable.rs, taxonomy.rs, transport.rs` — no `identifiers.rs`. [W]

**Nowhere else either.** No BIP39, `NameDigest`, `NameReference`, `word_list` or blake3 usage in `datom-codec`, `ethos-zero`, `core-ethos`, `protos` or `signal-frame`. The only other match is a transitive Cargo.lock entry. [W]

### 5.3 The Ethos declaration, verbatim

`ethos/identifiers.ethos`, in full: [S]

    Library
    []
    [ LocalNameReference.{ Integer Integer Integer }
      ClusterNameReference.{ Integer Integer Integer Integer Integer Integer }
      PublicNameReference.{ Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer } ]
    []
    []

Three fixed-width forms — **exactly the three security levels 692df8 asked for**: local/private, cluster, public.

### 5.4 The anatomy

`src/identifiers.rs`, whose header states the design rationale plainly: [S]

    //! Readable, nominal identifiers for local, cluster, and public references.
    //!
    //! `ethos/identifiers.ethos` is the schema for the three fixed-width forms.
    //! Datom's available intrinsics at this revision are `String` and `Integer`,
    //! with no standard hash primitive. `NameDigest` is therefore a Signal-owned
    //! BLAKE3 adapter, not a claim about a Datom hash type or authentication.

| Constant | Value |
|---|---|
| `BIP39_WORDS` | 2048 |
| `BITS_PER_WORD` | 11 |
| `LOCAL_WORDS` | 3 |
| `CLUSTER_WORDS` | 6 |
| `PUBLIC_WORDS` | 12 |

**Word list: BIP39 English** (`bip39` crate v2, `Language::English.word_list()`), 2048 words, 11 bits each. The "is there something denser?" question was asked and the answer landed on BIP39.

**Bits: 33 local / 66 cluster / 132 public.**

`NameDigest([u8; 32])` is `blake3::hash(bytes)`. `NameDigest::of_bytes` hashes arbitrary input; `.local()`, `.cluster()`, `.public()` project it. The projection is a straight MSB-first bit walk over the digest — `words()` takes `count * 11` bits from the front of the 32-byte hash, big-endian within each word. So **local/cluster/public are nested prefixes of the same digest**: the first 3 words of a cluster name are its local name.

Types are rkyv `Archive/Serialize/Deserialize`, `Copy`, `Eq`, `Hash` — real types, not strings, as 692df8 ruled. Parse errors are a closed enum: `Empty`, `NonCanonical`, `UnknownWord(String)`, `WrongLength { expected, actual }`, `InvalidIndex(u16)`.

**Display answers the camelCase ruling directly:** `display()` writes the first word lowercase and capitalizes the first letter of each subsequent word, concatenated with no separator. A local name renders as e.g. `wordWordWord` — camelCase, visually distinct from PascalCase typed objects, exactly as 05c604 asked. Round-trip parsing rejects a non-canonical spelling.

Cargo deps: `bip39 = { version = "2", default-features = false, features = ["std"] }`, `blake3 = "1"`. [S]

### 5.5 Its own status disclaimer

`DESIGN.md` on the branch carries four sections of the archived legacy `signal` repository's architecture verbatim, and states: "Nothing here is ruled for the current Signal layer — the protocol on top of portable rkyv is still to be decided. Read it as inherited reasoning, not as specification." `ARCHITECTURE.md` echoes it: "The protocol on top of the rkyv archive is to be decided." [S]

One of those inherited sections is directly relevant to §4.2 above — the **origin route**: "a short, statistically-unique identifier acting as a return address… It is internal to each component and need not be a long hash — just an echoed return address." That is the inherited reasoning for why a MessageId need not be what it currently is.

### 5.6 Where this leaves the design book

The word-identifier work **exists, is coherent, answers each of the psyche's rulings point by point, and is used by nothing.** It sits on an unmerged proposal branch, eleven days old, while every identifier in daily use (§4) remains a hex substring of a clock or a counter. `NameDigest` is explicitly scoped as a Signal-owned BLAKE3 adapter, not a Datom hash primitive — so adopting it for flow ids or message ids would be a decision, not a migration.

---

## 6. What could not be established

- Whether Flow or Message runs on any host other than ouranos (prometheus and zeus were not reached).
- Why the Next pair is 0.17.0 rather than the 0.17.1 branch head — deliberate or simply not rebuilt.
- Whether a live `Deliver` through the Next pair works; the "first live letter Acknowledged" claim is second-hand from `flows/b7ba00/log.md`, not witnessed.
- a676b3's live working state, or any of its own evidence — it has no flow directory anywhere on disk, and it was not messaged.
- Who performed the 2026-09-26 15:24 UTC home-manager activation that put the current field-clj on PATH, and by what route.
- Whether anything has been tested on the Prometheus remote builder since the current field-clj head; no Lojix deployment exists at a revision pinning it.
- Whether `nix run github:LiGoldragon/transcript` completes — the build was cut at 180 s after successfully fetching the flake.
- The exact rule by which the Codex alias offset was chosen in source — chars [23:29] fits every sample and matches the constant, but the constant's derivation was read from the binary's constant, not from a design note.
- Whether one flow identity can map to several rollout files (a resumed Codex thread).
- Whether the ~103 flow directories with no `.flow-id` marker are resolvable at all.
- The writer of `flows/*/messages/<ns-timestamp>-<flowid>-<uuid4>.md` — no code anywhere constructs that path.
- The generator of Herdr's default Claude agent name and of `terminal_id`'s trailing 2 hex (Herdr is third-party; no source on disk).
- Whether a Field Nexus design has been ratified anywhere beyond the 2026-09-18 concept report; its seven open questions appear still open.

## 7. Three findings worth acting on independently of the book

1. **Orchestrate `release` has no owner check** against a 0-entropy, enumerable id space on a group-accessible socket. Any flow can release any other flow's Lock by guessing a number.
2. **`testing-push-landed` requires full 40-char hashes; `subflow-scripts` forbids any 16+ hex run in a subflow's return.** A subflow proving a push cannot satisfy both rules.
3. **The `transcript-search` skill instructs every flow to use a CLI that has never been installed on this machine.** The working invocation is `python3 /git/github.com/LiGoldragon/transcript/transcript.py …`, and it is Claude-only.

## Sources

- Live probes on ouranos, 2026-09-26: `flow 'List.{}'`, `flow-next 'List.{}'`, `systemctl --user`, `ss -lx`, `ps`, `hm-list`, `orchestrate 'Observe.Locks'`, `field-clj '#observe []'`, `jj log`, `git`, `readlink -f` over `~/.nix-profile` and `~/.local/bin`, `lojix 'Query.ByDeployment…'` / `'Query.ByNode…'`, `herdr agent list`, `gh api` reads of remote `flake.lock`.
- Repository sources under `/git/github.com/LiGoldragon/`: `flow`, `message`, `messenger-clj`, `field-clj`, `field`, `nexus`, `orchestrate`, `harness`, `transcript`, `signal` (+ the `5f4fea-word-identifiers` worktree), `name-table`, `CriomOS`, `CriomOS-home`, and the vendored `uuid` crate in the codex vendor store path.
- Transcript roots `/home/li/.claude/projects`, `/home/li/.codex/sessions`, `/home/li/.codex-next/sessions`; state roots `/home/li/.local/state/{flow,message,message-next,messenger-clj,hacky-messenger,orchestrate-nexus}`.
- Primary lanes: `flows/{b7ba00,e167d8,b860be,b7da5d,b80e55,38de5b,1ac573,05c604,692df8,fd0f97}/`, `Vision/{messaging,flowNexus,nexus,committing,deployment}.md`, `.claude/skills/{messaging,herdr,nexus,orchestrate,transcript-search,compensation-messenger-clj,subflow-scripts,testing-push-landed,flow-aspect}/SKILL.md`, `SKILL_VARIABLES.md`.
