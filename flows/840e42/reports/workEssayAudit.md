# Audit of workEssay.md

Written by a Fable audit subflow of flow 840e42 on 2026-09-15; placed here verbatim by the main flow because the subflow ran read-only. Everything marked witnessed was read or run by that subflow on 2026-09-15.

**Verdict**
1. Of 41 claims marked witnessed, 34 confirmed, 4 contradicted, 3 mislabeled (relayed claims marked witnessed).
2. The "six of nine blocked behind Flow" count is unsupported by the essay's own enumeration; two components (relay, Persona) are named, and the relay is already being built against a marked Flow seam.
3. The seven-flow-month total does not follow from the essay's own scale (four large, three medium, two small is about five).
4. The "most sensible part now" verdict rests on stale numbers (3 of 8 rostered; today 7 of 12) and a cause stated as witnessed that no source witnesses.
5. My verdict: the launch record is the right shape but is already Codex item 31's stated design; what is sensibly built now is what is actually building: the Prometheus services (item 47) and the relay PoC, with the launch record folded into item 31 rather than started fresh.

## Witnessed-claim check, by section

**§1 Flow.** No `flow` repository: confirmed (`ls /git/github.com/LiGoldragon/flow` fails). `flowNexus.md` exists, item 31 "in progress, pending": confirmed (`overview-facts.md`). "Witnessed: `claude --bg` ignores a caller-supplied `--session-id`": **mislabeled**. The source is `to-fd0f97.md`, Codex's claim; the essay read the report, not the contract. The roster is ambiguous on it: worker `6cc91bd5` was launched with `--session-id 6cc91bd5-...` matching its sessionId. Nexus types `ConfigurationState<C>`, `SocketAuthority`, `Situation`: confirmed (`nexus/src/configuration.rs:9`, `authority.rs:18`, `situation.rs:139`). All fd0f97 and 840e42 vision quotes: confirmed verbatim, including "Unable to recycle your flow" (`flowLifecycle.md:11`). Roster "3 workers against 8 live sessions": correctly marked claimed, but **stale**: `roster.json` today holds 7 workers; live `claude` sessions number 12 (8 daemon `bg-pty-host` pairs, 4 terminal-launched). 93 `.flow-id` markers: confirmed. "The relay chain does not read them": **contradicted today**. `message/src/flow_registry.rs` resolves `TargetFlowName` from `.flow-id` markers (secondary stage 3, commit 243eb82, 7 tests, its claim; the file is in the working tree, witnessed).

**§2 Psyche.** README sentence, 872K, four levels in the psyche skill, 13 Vision and 6 Intent files, 1320 lines, 15 fd0f97 vision files: all confirmed. "16 raw vision files" in 840e42: 17 today (`core.md` landed 16:08, the essay at 16:10; a drift, not an error).

**§3 Relay.** Version 0.12.0 in `Cargo.toml`: confirmed. Bins `message_daemon`, `meta_message`, `message` (`main.rs`): confirmed. The five arrangements: confirmed in `tables.rs:98-103`. **Size contradicted**: `du -sh message` is 4.4G today, not 3.2G (target growth plausible; the number is unstable and mostly `target/`). `SubmissionAccepted`: confirmed (`engine.rs:186`). "Not uniquely witnessed idle": confirmed in `thirdMember.md:122` and, unmentioned, witnessed by 840e42's own log line 43 against the secondary.

**§4 Cloud.** 7.5M, three bins, `PreparePlan` in `lib.rs`, `flarectl` wrapped with `gopass show cloudflare/api-token` (`flake.nix:36-41`): confirmed. `digitalocean.rs` is marked claimed but exists, and so does `hetzner.rs`, unmentioned: the provider trait already has three concrete paths to lift, not two.

**§5 Persona.** 27M, README "engine manager and integration repository": confirmed. "A daemon directory": **contradicted**. `persona/daemon` is a stale unix socket file (srwxr-xr-x, May 11), as is `persona/v config`; only `schema/` is real. Codex items 11 and 13: confirmed as claims.

**§6 Mentci.** 8.9M, `mentci-daemon`, `answer:approve`/`answer:defer` (`client.rs:190,199`), `schema/preflight-launch.datom.md`, CriomOS 133M: confirmed. Zero `disko`/`nixos-anywhere`/`nixos-install`/`nixos-generate-config` hits: confirmed by my own grep. The notification quote drops the word "Unity" ("write our own Unity app right now as a concept, as a Slint Android project"); the meaning survives.

**§7 Identifiers.** Three-thing ownership, `ethos/signal.ethos`, no identifier module in `signal`: confirmed (source is 9 `.rs` files counting `generated/`, "eight" is loose). **Omitted**: `/git/github.com/LiGoldragon/signal-5f4fea-word-identifiers` (created 14:44 today) already carries `src/identifiers.rs` with `NameDigest`, `LocalNameReference`, `ClusterNameReference`, `PublicNameReference`, BIP-39 alphabet, round-trip tests and `reports/identifier-poc.md`. The "type and round-trip proof" the essay budgets a day for exists as Codex's proof; what remains is the living's review and the merge.

**§8 Third seat.** Router at `10.18.0.1:11434`, `--strict-config` exit 0, key mode 0400 owner `llama`, `dsh` not found: confirmed as the secondary's witnesses. "Already resident": the report's own witnessed `/v1/models` shows every preset `status.value: "unloaded"` (`thirdMember.md:60`); residency is the secondary's inference and the essay relays it as fact.

**§9 Boot counting.** Six verbs, no `Rollback` action (`runtime_model.rs:445-452`), `GenerationSlot::Rollback` declared twice and never used (`adapters.rs:246`, `runtime_model.rs:133`, no other hits): confirmed by my own grep. `ScheduleBootOnce` anatomy, Prometheus unconfirmed by `bootctl status`, droplets BIOS/GRUB, "daily driver": confirmed in `countdownRollbackAnatomy.md`.

## Sizes

By the essay's own scale (large = month, medium = week, small = day) the nine sum to about five flow-months, not seven. Where I size differently: §7 is not a day of building but a review, since the type exists; §3 is medium only if the 0.11.1 to 0.12.0 deploy (Codex item 35 migration, secondary deploy under countdown) is counted, and that deploy gates everything on the wire; §5 Persona is large but its "working day" of quota reading is Codex's collector, uninstalled; §1 is large as written, but the launch half is under a week and is item 31's scope, not a new lane. §6 and §4 sizes are reasonable. §9 medium is right but carries the untested VM-first proof; the countdown skill is a proposal (`5f8c389`), not landed.

## The verdict, judged

The essay's "launch record" is a good shape and matches Codex's own design conclusion in `to-fd0f97.md` ("a persisted typed launch record mapping requested alias to daemon-generated identifier, daemon-owned per-flow unit/cgroup creation, and persisted hook configuration"). The essay does not credit that, nor Codex's launcher prototype (`proposal/5f4fea-item30-launcher`, `tools/flow-component` proposed), nor that this very session was launched by that path and its launch witness (log line 13) found the living's gates met.

The disconfirming evidence for "most sensible now": (a) the relay is not blocked; the secondary's PoC reads `.flow-id` markers through a marked seam, stage 3 green; (b) the delivery failures 840e42 witnessed today are approval-held cross-session messages (log lines 17, 25, 33) and an unreliable intercom route (line 61), neither cured by a launch record; (c) the living's own priorities today are the Prometheus services with the Git server (item 47, already ordered "built now"), the XMPP chime (item 48), the core layer (item 49, "set it up now"), and the relay (approved: "Yes, extend the message Nexus, go ahead"). The essay's alternatives section never weighs these three, which are what the living said and what is in motion.

My verdict: build the launch record inside item 31, not as a new "most sensible part"; let the Prometheus services and the relay PoC proceed as the parts already chosen; the identifier work is a review, do it this week.

## Quackery

- "For this reason and no other (witnessed, `flowLifecycle.md`)": the file witnesses the living's words, not the cause. Inference dressed as witness.
- "Six of the other eight wait on it": the enumeration names two components plus three sub-parts of §1.
- "About seven flow-months": no arithmetic supports it.
- "Two or three days, not a month": no source, and Codex has already spent days in this area.
- "Already resident": contradicted by the source's own data.
- "3 of 8" reused in the verdict as if current; the roster today reads 7 of 12.
- "Witnessed" on the `claude --bg` contract, a relayed claim.

## Sources (this audit)

Witnessed: `/git/github.com/LiGoldragon/{nexus,message,cloud,persona,mentci,signal,signal-5f4fea-word-identifiers,lojix,CriomOS,psyche}`; `~/.claude/daemon/roster.json`; `pgrep` on ouranos; all vision files cited; `flows/840e42/log.md`; `/home/li/secondary/flows/57a7aa/{log.md,reports/*}`; `/home/li/wt/primary-5f4fea/flows/5f4fea/reports/{overview-facts,to-fd0f97,to-840e42}.md`. The secondary's and Codex's contents are their claims.
