# Flow 0.17.4 stage-one preflight (read-only; zero seats started)

Method: Bash probes from harness-native child (Sonnet 5), 2026-09-26. Source read at the tag; one `nix build` into a scratchpad result link. No flow-nexus daemon, Start, Stop, List, Replace or pane run. Stage two NOT run, per Field Sol 9ac67c and Fable 8904b1.

## 1. Built binary (WITNESSED)
- Source: /home/li/wt/flow-0174-independent-test-407811, HEAD bc464e5e1b94fcc179af73111f43b69db1f69fc5 "Release Flow 0.17.4", tag `flow-0.17.4`, on origin/main, tree clean, Cargo version 0.17.4. Unambiguous.
- Build: `nix build .#default --out-link <scratchpad>/flow-result` (not installed/activated). Store path /nix/store/7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4 (drv vfv1g24y...-flow-0.17.4.drv); bins flow, flow-meta, flow-nexus. Cache (nix.prometheus) timed out, so it built locally.
- `<scratchpad>/flow-result/bin/flow --version` -> `flow 0.17.4`. (flow-nexus --version is a pure version answer: `flow-nexus 0.17.4`, not run.)
- PATH `flow` is still 0.12.2; use the store path explicitly.

## 2. Scratch instance isolation (proved from source, not run)
Daemon = `flow-nexus` (crates/flow-nexus/src/main.rs, store.rs). It has NO flags; config is env only:
- `HOME` -> state dir `$HOME/.local/state/flow`, store `$HOME/.local/state/flow/flow.sema`, launch bundles beside it.
- `XDG_RUNTIME_DIR` -> sockets `$XDG_RUNTIME_DIR/flow/flow.sock` and `flow-meta.sock`.
- Clients: `flow` reads `FLOW_SOCKET`; `flow-meta` reads `FLOW_META_SOCKET`. Both DEFAULT to the LIVE /run/user/1001/flow/*.sock, so an unset var falls back to production.
- Fallbacks to live paths: HOME unset/relative -> /etc/passwd home (/home/li); XDG_RUNTIME_DIR unset/relative -> /run/user/1001. Both must be set absolute.
- `FLOW_SOURCE_ROOT`, `FLOW_CODEX_{STABLE,NEXT}_{CLIENT,SOCKET,HOME,MODELS}` are accepted (absolute only); unset Codex ones default under HOME (so scratch HOME), source_root default `primary` (relative, unresolved: set FLOW_SOURCE_ROOT explicitly).
Live paths (witnessed): /run/user/1001/flow/{flow,flow-meta}.sock; /home/li/.local/state/flow/flow.sema (1056768 B, real store); /run/user/1001/flow-next, /home/li/.local/state/flow-next (next channel).
Scratch plan: fresh dir e.g. /tmp/claude-1001/.../scratchpad/f174/{home,run}; run `env HOME=.../home XDG_RUNTIME_DIR=.../run FLOW_SOURCE_ROOT=<abs> flow-nexus`; clients `FLOW_SOCKET=.../run/flow/flow.sock`, `FLOW_META_SOCKET=.../run/flow/flow-meta.sock`. Paths differ from all live ones by construction; emptiness holds because flow-nexus creates the store fresh (not yet created; scratch dir not made). Emptiness to be shown at stage two with `ls` and `List.{}` before any Start.

## 3. Proof-gate items
- HERDR_ENV and socket: WITNESSED (HERDR_ENV=1, HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock, pane w1:pF, workspace w1). Herdr sessions: default(running), recovery-56ae53(running), messaging-build(stopped).
- FLOW_ID/FLOW_DIRECTORY: ABSENT from ambient env; allowed to be exported explicitly per command (38f337, /home/li/wt/primary/opus-sonnet-56ae53/flows/38f337). Not proved by running.
- pty: ABSENT in this shell (previous witness: not a tty). Wrapper `script -qc '<cmd>' /dev/null` proposed; not tried (would be a run).
- Scratch socket + store: PROVED FROM SOURCE (section 2); not run.
- Typed shapes (README): `flow 'Stop.<flowid>'`, `flow 'List.{}'`, `flow-meta 'Deliver...'`. Start is a typed `Start` datom with LaunchProfile+OriginClue (source descriptors with SHA-256, skill names, aspect, power, harness, model, effort, predecessor, remembered flows, Herdr target session, first instruction). The exact Start datom text is NOT yet derived; must be generated from signal-flow types (README says do not assemble by hand). ABSENT.
- Budget: 3 Starts, claude-sonnet-5 medium, 300 s each, 15 min total. Set by the brief; no CLI flag enforces timeout/turn cap, must be wrapper `timeout 300`. Not proved as enforced.

## 4. Risks for stage two (uncovered by source)
1. HERDR: Start opens a pane in the Herdr session the profile names via `herdr --session <name>`. Overriding HOME moves herdr's config/sessions dir (~/.config/herdr) too, so a scratch HOME would see none of the live sessions, but the pane host then needs its own Herdr server; and inherited `HERDR_SOCKET_PATH`/`HERDR_ENV` env point at the LIVE default session. Unset/override them for the daemon, or panes could open in the live workspace. Unproved.
2. Claude auth: scratch HOME has no ~/.claude credentials; pointing CLAUDE_CONFIG_DIR at the live one shares live credentials/config (read/write of transcripts/history) - a leak of isolation. Decision needed.
3. Live seat skill roots derive from FLOW_SOURCE_ROOT/CLAUDE_CONFIG_DIR; the Start writes launch bundles under scratch state dir (fine).
4. No timeout flag; a hung Start needs an external kill and Stop.
5. Known intermittent defect: Soft letter to a Claude seat graded Presented but unsubmitted (0.17.1 fix attempted; scenario 4 on Haiku failed). Not exercised.
6. Nix build spent local CPU; no model spend so far.

## 5. Cleanup plan
Stage two: typed `Stop.<id>` then `List.{}` per Start against scratch socket; kill scratch flow-nexus; close any scratch Herdr session; `rm -rf` scratch dir; remove result link. Now: only the result link exists in scratchpad (built store path stays in /nix/store, GC-able); nothing else created.

Spend: 0 model tokens spent on Starts; 0 Starts.
