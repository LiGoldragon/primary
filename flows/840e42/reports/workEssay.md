# How much work the program in motion is, and what it looks like built

An essay for the living psyche. Flow 840e42, 2026-09-15.

Sizes are for one Codex or Claude flow working steadily: **small** is a
day, **medium** a week, **large** a month. Every size is this flow's own
judgment. Every fact is marked **witnessed** (this flow read the file or
ran the command) or **claimed** (a report asserted it).

The program is nine components, about seven flow-months of work — but
the ordering matters far more than the total, because six of the nine
are blocked behind the same missing thing.

---

## 1. Flow — launch, recycle, hooks as notifications, a thin event log

**Size: large.**

What exists: nothing named Flow. Witnessed — there is no `flow` repository
under `/git/github.com/LiGoldragon`; `Vision/flowNexus.md` describes the
component and Codex 5f4fea lists item 31 as "in progress, pending" in
`overview-facts.md`. Witnessed — Claude's own `claude --bg` contract
ignores a caller-supplied `--session-id`, mints its own, and records
`dispatch.isolation: "none"`, so fixed successor identity is unavailable
through that path (Codex, `to-fd0f97.md`). Claimed — `~/.claude/daemon/roster.json`
holds 3 workers against 8 live sessions, so sessions launched outside the
daemon are permanently unreachable; 93 `.<alias>.flow-id` markers exist
and the relay chain does not read them (secondary, `messageRelayNexusPocs.md`).
Claimed — the current session is parented to a terminal, not a supervisor,
and dies on logout; linger is off for the user (secondary, `sessionPersistence.md`).

Built, it looks like this. A Nexus with the ordinary/meta socket pair the
`nexus` crate already defines (witnessed: `ConfigurationState<C>`,
`SocketAuthority`, `Situation`). One durable launch record per flow:
requested alias, harness, daemon-minted identity, the per-flow systemd
scope it owns, the working directory, the vision files injected. A
launch is one datom value naming a flow *type* — the psyche's
`flows/fd0f97/vision/flowTypes.md` asks for exactly that, preprogrammed
types that need no behavioural instruction. Recycle is a state machine
on that record: the predecessor emits the recycle signal and stops; a
small model confirms the successor answers; only on failure is the
predecessor woken, with "unable to recycle your flow"
(`flows/fd0f97/vision/flowLifecycle.md`, witnessed). Harness hooks are
registered by Flow at launch and arrive as notifications it may act on
(`flows/840e42/vision/flow.md`, witnessed). The log is the psyche's
enum log: integers, scalars, booleans, enum variants, a string only
where a string is unavoidable, garbage-collectable
(`flows/840e42/vision/logging.md`, witnessed).

The month is mostly the launch record and the supervision, not the log.

## 2. Psyche — four levels, a domains enum, migrating the files

**Size: medium.**

Witnessed: the `psyche` repository exists at 872K and its README says
plainly "There is no supported runtime or public Rust API yet" — an
isolated scaffold. Witnessed: the four levels are already named and
ordered in the psyche skill — Spirit, Intent, Vision, Notion, descending
authority — and the file layout is `Vision/<topic>.md`,
`Intent/<topic>.md`, `flows/<id>/vision/<topic>.md`,
`flows/<id>/notion/<topic>.md`, plus the draining legacy `vision-raw/`.
Witnessed: 13 Vision files and 6 Intent files, 1320 lines together;
flow 840e42 holds 16 raw vision files, fd0f97 holds 15.

Built: a Sema-backed Nexus whose schema is those four levels as one
enum and the topic names as a **domains** enum — so `Vision.Quota` is a
typed address, not a path string. Each record carries the verbatim
words, who heard them, which flow, whether typed or spoken, and the
context paragraph the current files carry by convention. Migration is
mechanical because the convention is already uniform across every file
this flow read; the week is schema design plus the reader that replaces
`grep -rn flows/*/vision/`. The psyche asked for exactly this
substitution — "components like Psyche instead of this makeshift file
system", "everything with easy, minimal Datom object syntax"
(`flows/fd0f97/vision/psyche.md`, witnessed).

## 3. The message relay Nexus — flow delivery, receipts, the persona MCP bridge

**Size: medium.**

This is the nearest-finished component and the most painfully mis-wired.
Witnessed: `message` is 3.2G on disk with `message`, `meta-message`,
`message-daemon` and a `messenger.sema` ledger, inbox, thread index,
agent registry and delivery outbox. Claimed: the running daemon is
version **0.11.1** while the repository is 0.12.0, and the store schema
moved 3→4 with no migration, so the deployed daemon and the source
disagree on the wire (secondary, `messageRelayNexusPocs.md`). Claimed:
the store holds no registered flow and no real message; both delivery
legs terminate at processes that are not running. Claimed: delivery is
refused in practice — `session 942914a6 is not uniquely witnessed idle`
(secondary, `thirdMember.md`). Witnessed, from the psyche:
"I feel like I don't see my messages being passed along to the other
parts of the cluster. It's like there's a cluster failure"
(`flows/fd0f97/vision/flowLifecycle.md`).

Built: the agent registry is populated by Flow at launch, so a flow is
addressed by its alias and never by a session UUID. Every message
carries an identity and a parent on the wire, not only in the store. A
receipt returns to the sender when the target actually consumed the
turn — today `SubmissionAccepted` acknowledges submission only
(claimed). And the psyche's bridge: one MCP tool taking a single
string that is a datom value, `orchestrate` or `message` as the head and
the variant as the payload (`flows/840e42/vision/messages.md`,
witnessed), so a flow prints its instruction in its own response and the
tool carries it — cheaper than starting a subflow, which is what the
psyche asked for (`flows/fd0f97/vision/messages.md`, witnessed).

## 4. Cloud — a provider object per provider, Cloudflare first; the Git server on Prometheus

**Size: large** (the provider refactor medium, the Git server small, the
build-and-review pipeline medium).

Witnessed: `cloud` is 7.5M and already ships `cloud-daemon`, `cloud`,
`meta-cloud`, ordinary and meta sockets, a `PreparePlan`/`ApprovePlan`/
`ApplyPlan` ceremony, and a Cloudflare DNS path through a packaged
`flarectl` wrapper that loads its token from `gopass`. So the psyche's
"an object for every provider, like Cloudflare, we should do that first"
(`flows/840e42/vision/cloud.md`, witnessed) is a refactor of a working
runtime, not a new build: lift the Cloudflare path into a provider trait
with DNS, zones, records, and the DigitalOcean adapter (claimed to exist
at `cloud/src/digitalocean.rs`) as the second implementation.

The Git server is the psyche's stated reason for the whole component —
"we have all the repositories anyway, and we have a domain name, so it's
taking control with the cloud component"
(`flows/840e42/vision/repositories.md`, witnessed). Built: a Git service
on Prometheus defined as a CriomOS module, one repository per web-app
mapping, the `webapi:` namespace of
`flows/840e42/vision/namespace.md` resolving by longest match, and a
change to a mapping arriving at the psyche as a proposal to approve or
review. The pipeline builds the Slint app on Prometheus and presents it
for the living's review (`flows/840e42/vision/prometheus.md`, witnessed).

## 5. Persona — the meta-harness keeper: ledger, quota-driven operation, model fallback

**Size: large.**

Witnessed: `persona` is 27M with a daemon directory, schema, and a
minimal datom client over an in-process engine-manager stub; its README
names itself "the engine manager and integration repository". Claimed:
item 13 produced a pinned Nexus/Sema adapter draft whose five tests use
fake storage with no live engine, deployment held (Codex,
`overview-facts.md`). Claimed: a live quota collector succeeds with 12
tests passing, but there is no scheduler and no hook, and the
accounting policy is provisional.

Built: Persona holds the ledger of every model call — inputs, model,
what it had access to, what it produced — reviewable before the data is
erased, which is the psyche's rating design
(`flows/840e42/vision/rating.md`, witnessed). It reads quota against the
five-hour window, treats unused daily and hourly quota as slack, and
spends slack on light encouragement to keep concepts materialised so
they can be tested; when Fable is overused it falls back to Opus; when
Codex is abundant it thinks out loud through Codex subagents
(`flows/840e42/vision/quota.md`, witnessed). It decides when to start a
flow and asks Flow to start it. The month is the ledger schema and the
policy engine; the quota reading is already a working day's worth.

## 6. Mentci — the thin mobile client on Slint embedding a minimal CriomOS

**Size: large, and this flow judges it the one likely to exceed a month.**

Witnessed: `mentci` is 8.9M and is already the daemon for "the
programmable human approval surface" — `mentci-daemon`, a thin `mentci`
client, `observe`/`answer:approve`/`answer:reject`/`answer:defer` atoms,
a preflight-launch datom schema. Witnessed: `CriomOS` is 133M of Nix
modules, packages, gates and checks. Claimed: CriomOS has zero
occurrences of `disko`, `nixos-anywhere`, `nixos-install` or
`nixos-generate-config` — no install-from-scratch path exists
(secondary, `clusterSpinup.md`).

Built: an Android/Linux Slint app, a thin asynchronous client holding a
foreground job so the OS keeps it alive, no LLM on the phone, the
harness part running to the cloud, a debug mode with a small local
server, and enough local function to work with the upstream unreachable
(`flows/840e42/vision/mobile.md`, witnessed). "A very minimal CriomOS"
is the part that is not a month: deciding the minimum is a design
question the psyche left open, and the packaging path does not exist
yet. This also answers the channel question — the psyche's own
alternative to XMPP and Matrix was "just straight up write our own app
as a Slint Android project"
(`flows/840e42/vision/notification.md`, witnessed).

## 7. Identifier types in signal

**Size: small.**

Witnessed: `signal` is 6.6M and owns exactly three things — the portable
frame, the four-byte length framing, and the taxonomy generated from
`ethos/signal.ethos`; its source is eight files. Witnessed: there is no
identifier module in it today. Claimed: Codex measured both tokenizers
across nine separator forms and three- and four-word identifiers, and
produced a real tiktoken sample table, with the production form not yet
selected (Codex, `overview-facts.md`, items 9, 15, 26, 27, 32). The
psyche's instruction is direct: the name-based hash goes in the signal
library, sensible name, sensible anatomy, shown whole, rewritten later
where it does not fit (`flows/fd0f97/vision/identifiers.md`, witnessed).

Built: a type in `signal` that mints a word identifier from a name, a
round-trip proof, and the whole thing shown to the psyche in one
screen. A day, because the measurement work is done and only the
decision and the type remain.

## 8. The third seat on Prometheus

**Size: small.**

Claimed, and unusually well-witnessed by the secondary: the Prometheus
llama router is an active systemd unit answering OpenAI-shaped JSON at
`10.18.0.1:11434`; `qwen3.5-122b-a10b` at 131072 context is the
load-on-startup preset, already resident; `gpt-oss-120b` is the
fallback. Claimed: Codex accepts an arbitrary `model_providers` entry —
a `--strict-config` probe naming Prometheus exited 0 — so a
`~/.codex/prometheus.config.toml` profile and `codex -p prometheus` is
the whole client side. Claimed: the one real blocker is the bearer key,
which exists only on Prometheus, mode 0400, owned by `llama`; running
the seat *on* Prometheus removes both the key problem and the network
hop. Claimed: `dsh` is documented by a skill but installed nowhere.

Built: a third flow in the cluster, on the house model, costing nothing
per token — which is what makes the quota design of §5 affordable, and
what the private layer chartered in CLAUDE.md will eventually need.

## 9. Zeus and Prometheus deploys under boot counting

**Size: medium.**

Claimed, from Lojix source: `HostDeployAction` has six verbs and
**no rollback**; `GenerationSlot::Rollback` is declared in two places and
never written or read. The one real primitive is `ScheduleBootOnce` —
it reads the current entry from `bootctl`, sets the new closure, then
sets the old entry as default and the new as one-shot, so reboot 1 lands
new and reboot 2 returns to old, dispatched under `systemd-run --wait`
so it survives ssh death (secondary, `countdownRollbackAnatomy.md`).
Claimed: Ouranos and Zeus are UEFI/systemd-boot; Prometheus is
systemd-boot by partition layout but unconfirmed by one `bootctl status`;
DigitalOcean droplets are BIOS/GRUB and cannot use BootOnce at all.
Claimed: Zeus's only recovery today is the physical boot menu on
someone's daily driver.

Built: an armed countdown around that primitive. A transient PID-1-owned
unit fires the return reboot unless a witness on a peer host cancels it,
the witness proving it is answering from the candidate closure by
returning the store path of `/run/current-system`; the generation slots
move on bless. Proved first on a VM guest through CriomOS's existing
test substrate, never on Zeus first.

---

## The order

**What unblocks the most.** Flow, decisively. Six of the other eight
wait on it: the relay cannot address a flow that no registry seats
(§3); Persona cannot start flows it cannot launch or supervise (§5);
recycle, remote control, and the coloured terminal are all the same
missing launch record (§1); the psyche's messages do not reach the
cluster for this reason and no other (witnessed, `flowLifecycle.md`).
Second is the relay, which unblocks the psyche's own bandwidth into the
system. Third is Persona, which cannot exist before either.

**What is cheap and unblocks something.** The identifier types (§7, a
day, and everything else is named by them) and the third seat (§8, a
day, and it makes the quota policy affordable). Both are worth doing in
the first week regardless of order, because neither blocks on anything.

**What can wait.** Mentci (§6) and the cloud Git server and pipeline
(§4) are the longest and the least blocking. Boot counting (§9) is
medium and urgent only in the sense that Zeus currently has no recovery
but a physical boot menu — it should precede any Zeus deploy and no
other work.

**The most sensible part to implement now: the launch half of the Flow
component — the durable launch record.** Not the whole Nexus, not
recycle, not the log. One record per flow, written by the launcher and
read by everyone: requested alias, harness, the daemon-minted identity,
the per-flow scope, the working directory, the injected vision files.

The reason is that it is the smallest thing that stops a witnessed,
recurring, psyche-visible failure. The evidence is unusually
converging: `claude --bg` mints its own identity and refuses the
caller's (witnessed); the roster holds 3 of 8 sessions (claimed); 93
flow-id markers exist and nothing reads them (claimed); the relay
refuses delivery for want of a uniquely witnessed idle session
(claimed); the psyche reports a cluster failure in his own words
(witnessed). One record reconciles all five. It is two or three days,
not a month, and every one of the six blocked components can start
against it the moment it exists — which is precisely what the psyche
asked for when he said to put the pieces together and bring it online.

---

## Sources

- Witnessed by this flow: `/home/li/primary/Vision/*.md`,
  `/home/li/primary/Intent/*.md` (line counts, `flowNexus.md`,
  `orchestrate.md`, `signal.md`, `highLevelView.md`, `anatomy.md`,
  `context.md` read in full).
- Witnessed: all 16 files of
  `/home/li/primary/.claude/worktrees/flow-840e42/flows/840e42/vision/`
  and all 15 of `/home/li/primary/flows/fd0f97/vision/`, read in full.
- Witnessed: `/home/li/primary/.claude/skills/psyche/SKILL.md` (four
  levels, psyche file layout).
- Witnessed: repository sizes by `du -sh` and README/tree inspection
  under `/git/github.com/LiGoldragon/` — `orchestrate` 34M, `message`
  3.2G, `lojix` 46M, `nexus` 3.3M, `persona` 27M, `cloud` 7.5M,
  `CriomOS` 133M, `signal` 6.6M, `mentci` 8.9M, `psyche` 872K.
- Claimed, read by delegated subflows and relayed here as claims:
  `/home/li/secondary/flows/57a7aa/reports/messageRelayNexusPocs.md`,
  `clusterSpinup.md`, `sessionPersistence.md`, `thirdMember.md`,
  `countdownRollbackAnatomy.md`; `layerNames.md` read directly by this
  flow.
- Witnessed by this flow, read in full:
  `/home/li/wt/primary-5f4fea/flows/5f4fea/reports/to-fd0f97.md` and
  `overview-facts.md` — their contents are Codex's claims.
- All sizes and the ordering are this flow's own judgment, inferred from
  the above.
