# Flow-next 0.17.1 MetaBindExisting preflight — Mind Astra 6fe957 (preparation only)

Method: direct, read-only queries against the live running services and Herdr,
plus a read-only byte inspection of the stable Flow store file. No mutation,
no typed `MetaBind`, no `Send`, no build, no service action, no Home
activation was performed. Witnessed 2026-09-27, this session (subflow of
56ae53, FLOW_ID=38f337, THREAD_ID=38f33758-72c0-4c2a-ad49-8ffeb8e310fa).

This is a brand-new task, independent of flow id 139366. No conclusion from
139366's own prep witness was read or reused; every value below was
re-derived fresh against 6fe957 and this store.

## Skill receipts

Loaded through the Skill tool (not `cat`/`Read`, so each carries authority):
`subflow`, `orchestrate`, `nexus`, `flow-evidence`, `behavior`, `herdr`.
`NON_MANAGEMENT_AGENTS.md` was read per CLAUDE.md's worker-agent requirement.

## Claim provenance

Every value below started as a claim relayed by 56ae53 in the dispatching
brief — unverified by me until witnessed. Each row states what I actually
queried and what came back; nothing here is taken on 56ae53's word.

## Verification results

| # | Claimed value | Result | How witnessed |
|---|---|---|---|
| 1 | Role/power Mind/High | **PASS** | Stable store raw bytes (`/home/li/.local/state/flow/flow.sema`) contain, contiguous and in FlowRecord field order, the flow_type string `Mind:High:gpt-6-astra` immediately followed by origin `meta-bind-existing`, session id `01a0dfdc-a500-7271-8f54-e446fe9578dd`, and flow id `6fe957`. Corroborated by Herdr's own `terminal_title` for the pane: `MindV2.{ Astra 6fe957 } | primary` (Mind aspect). Byte-level string extraction is interpretive, not a typed decode — noted as the weaker leg of this result, but the field sequence is exact and unambiguous. |
| 2 | Model gpt-6-astra | **PASS** | Same store string as above (`Mind:High:gpt-6-astra`); Herdr `agent get w1:p2` names the agent `mind-astra-6fe957`; `flow-nexus-next.service`'s own `FLOW_CODEX_NEXT_MODELS=gpt-6-sol,gpt-6-luna,gpt-6-astra` env lists `gpt-6-astra` as a valid Next model. |
| 3 | Harness Codex | **PASS** | Live `flow 'ResolveRecipient.6fe957'` against the stable socket returned `HarnessKind` field `Codex`. Herdr `pane get w1:p2` / `agent get w1:p2` both report `"agent":"codex"`. The pane's actual foreground process is the `codex` binary (see row 6). |
| 4 | Native thread id `01a0dfdc-a500-7271-8f54-e446fe9578dd` | **PASS** | Same `ResolveRecipient` reply's `session_id` field. Herdr's `agent_session.value` for pane w1:p2 is the identical string. The pane's live foreground process argv is literally `codex resume 01a0dfdc-a500-7271-8f54-e446fe9578dd`. Three independent sources agree exactly. |
| 5 | Persisted PowerLevel/role row exists for 6fe957 (unlike 139366, which reportedly has none) | **PASS, and the asymmetry with 139366 is real, re-verified fresh here** | In the stable store's raw layout, table-name headers precede runs of flow ids they hold rows for. `6fe957` (and `56ae53`, `c56100`) appear in a run headed by the concatenated three-table name `flow_nexus_flows` + `flow_nexus_herdr_routes` + `flow_nexus_roles` (each id repeated 3×, one per table). `139366` (with `184bd8`, `8904b1`, `9ac67c`, `22e12b`, `dc53b4`, `38f337`) appears only in runs headed by the two-table name `flow_nexus_flows` + `flow_nexus_herdr_routes` (each id repeated 2×) — no `flow_nexus_roles` membership. This matches the flow_type content directly: 6fe957's flow_type is the role-shaped `Mind:High:gpt-6-astra`; 139366's flow_type (found separately in the same file) is the generic, roleless `codex-registered`. Both facts point the same way. |
| 6 | Stable-side lifecycle Active | **PASS** | Live `flow 'ResolveRecipient.6fe957'` (against `/run/user/1001/flow/flow.sock`, the stable `flow-nexus` pid 1937, build `flow-0.12.2`) returned `flow_lifecycle` = `Active` as the reply's last field. |
| 7 | Herdr route Available + an actual live process | **PASS** | `ResolveRecipient`'s `herdr_route_selection` field read `Available.{ default mind-astra-6fe957 w1:p2 term_65c6a758e81952 }`. Independently, **not just trusting Flow's cached row**, I queried Herdr directly: `herdr pane get w1:p2` and `herdr agent get w1:p2` show the same pane/terminal live, agent `codex`, name `mind-astra-6fe957`, `agent_status: done`/`herdr agent explain w1:p2` → `state: idle` (alive, not exited). `herdr pane process-info --pane w1:p2` shows a real foreground process, pid 17334, cmdline `codex resume 01a0dfdc-a500-7271-8f54-e446fe9578dd`, cwd `/home/li/primary`. Confirmed still running via `ps -p 17334`: elapsed ~40,101s, same cmd. |
| 8 | Next's pre-state UnknownFlow for 6fe957 | **PASS** | Live `flow-next 'ResolveRecipient.6fe957'` (wrapper resolves to `/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow`, socket `/run/user/1001/flow-next/flow/flow.sock`, the running `flow-nexus` pid 90750) returned `RecipientResolutionRejected.UnknownFlow`. |
| context | "Endpoint Unavailable is normal imported state, not a Send gate" | **Consistent, informational only, not acted on** | The stable `ResolveRecipient` reply's `endpoint_selection` field does read `Unavailable` for 6fe957, matching UPGRADES.md's own documented behavior for `MetaBindExisting`-imported Codex flows ("`MetaBindExisting` stores its Codex endpoint as `Unavailable`; nothing on the ResolveRecipient or Send path consults [it]"). Not treated as a gate; no action taken on it. |

## Meta client / next-service build parity

- `flow-next` wrapper (`~/.nix-profile/bin/flow-next`, and the `flow-next-clients` package copy): `exec /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow`.
- `flow-next-meta` wrapper: `exec /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-meta`.
- Running Next service: `flow-nexus-next.service`, `ExecStart=/nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/flow-nexus`, live pid 90750 confirmed via `/proc/90750/exe` → the identical store path.
- **PASS**: all three (ordinary CLI, meta CLI, running Nexus) resolve to the exact same Nix store derivation output, `flow-0.17.1` at hash `zscrhhfyhkwa0qfvbkpg1piklfaahfa4` — same build, redone fresh in this task, no old snapshot reused.
- For contrast, the stable side's running service is a different build entirely: `flow-nexus.service` → `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus`, live pid 1937, `RUNTIME_DIRECTORY=/run/user/1001/flow`.

## Stable-store baseline (read-only)

File: `/home/li/.local/state/flow/flow.sema` (the store the stable `flow-nexus` 0.12.2 opens; `RUNTIME_DIRECTORY=/run/user/1001/flow` on that unit, `FLOW_SOURCE_ROOT=/home/li/primary`).

- Size: 1,056,768 bytes
- SHA-256: `9eb3487ca4f918dea2ee22bd67bd8be7af96bd6a49facae9d2da2222ab5e1887`
- mtime: 2026-09-27 01:07:12.478174047 -0600

## Next-store baseline (read-only, for completeness — this is the store the pending MetaBindExisting would write into)

File: `/home/li/.local/state/flow-next/.local/state/flow/flow.sema` (Next's `HOME=/home/li/.local/state/flow-next`, `XDG_STATE_HOME=/home/li/.local/state`, so the store lands nested under Next's own `HOME`).

- Size: 581,632 bytes
- SHA-256: `ece72cc1d9567ada317b0a3451893d293d524e39418860cc13651ddd8d35e06e`
- mtime: 2026-09-26 20:30:18.934853531 -0600

Both hashes/sizes/mtimes were captured fresh in this task; neither was carried over from any other flow's evidence.

## Orchestrate lock

Acquired for this preparation only, released is NOT yet done (see below —
subflow protocol releases it before returning):

    Locked.{ 8489 FlowNextImport6fe957Prep 38f337
      [ /home/li/wt/primary/opus-sonnet-56ae53/flows/38f337/witnesses/flow-next-import-6fe957-prep.md ]
      «Read-only verification and baseline for a possible future Flow-next
      0.17.1 MetaBindExisting of Mind Astra 6fe957; no mutation» }

Exact scope: the one witness file this task writes. Nothing else was claimed
— no store file, no service unit, no Home path — because nothing else was
written; the store reads were read-only inspection under this session's own
authority to read, not a claimed write path.

## Undo plan — precise about reversibility

There is **no delete verb** on either the ordinary (`signal-flow`) or the
privileged (`meta-signal-flow`) wire for a flow's row. This is stated
explicitly in the `flow` repo's own design record (`DESIGN.md`): "`Stop`
changes the durable lifecycle... `Retire`... None is a deletion." A row, once
written, is never removed by any documented operation; only its lifecycle
state changes.

If a `MetaBindExisting` of 6fe957 into the Next store is executed (out of
scope for this task, and not performed here):

1. **What would be writable.** `MetaBindExisting` on an unheld FlowId
   registers a new `FlowRecord` in the Next store: the flow row
   (`flow_nexus_flows`), a Herdr route row (`flow_nexus_herdr_routes`), and a
   role row (`flow_nexus_roles`) built from the binding's aspect/power/model
   (`Mind`/`High`/`gpt-6-astra`), with `endpoint_selection = Unavailable` and
   lifecycle beginning `Pending`/promoted per the Send/List path described in
   UPGRADES.md.
2. **The only forward-lifecycle verb that touches it afterward is `Retire`**
   (privileged, one `FlowId` in, `FlowRetired` or `RetireRejected` out). It
   marks the row `Retired` — a terminal, one-way state — not a removal and
   not a restoration of `UnknownFlow`. `ResolveRecipient` after a `Retire`
   would answer something other than today's clean `UnknownFlow`; it would
   answer that a retired flow exists.
3. **There is no supported way to make Next's state for 6fe957 read exactly
   `UnknownFlow` again once written.** The only mechanism that removes rows
   outright is direct surgery on the `.sema` file (a `redb` table) outside
   the Nexus's own wire contract entirely — stopping the service, editing the
   store's tables by hand or replacing the file with a pre-write copy of it.
   That is not a supported operation, carries real risk to other flows' rows
   in the same file (the Next store already holds other flow ids, per the
   next-store baseline above), and was not attempted or even trialed here.
4. **Honest bottom line, re-verified for this flow and this store rather than
   assumed from 139366's case:** the only clean, low-risk "undo" available
   before any write happens is not writing at all, or restoring the whole
   `.sema` file from the byte-identical backup captured in this baseline
   (size + SHA-256 above) taken *before* any mutation. After a
   `MetaBindExisting`, the only in-contract move is `Retire`, which is
   irreversible beyond that — it does not undo the import, it only ends the
   row's forward lifecycle. This mirrors the shape of 139366's own earlier
   lesson but is not assumed from it; it follows from the same `DESIGN.md`
   and `UPGRADES.md` text read fresh for 6fe957's flow_next store in this
   task.

## Scope discipline

No `MetaBind` was issued. No `Send`. No build. No service action. No Home
activation. The one lock taken is exactly the witness file above. All queries
were `ResolveRecipient`/read-only Herdr calls and raw-byte reads of existing
store files; nothing was written to either `.sema` file.

## Sources

- Live queries: `flow 'ResolveRecipient.6fe957'` (stable), `flow-next 'ResolveRecipient.6fe957'` (Next), both run in this session.
- Herdr: `herdr pane get w1:p2`, `herdr agent get w1:p2`, `herdr agent explain w1:p2`, `herdr pane process-info --pane w1:p2`, `ps -p 17334`.
- Processes/units: `ps aux`, `/proc/1937/environ`, `/proc/90750/environ`, `systemctl --user cat flow-nexus.service`, `systemctl --user cat flow-nexus-next.service`.
- Wrappers/builds: `cat $(which flow-next)`, `cat $(which flow-next-meta)`, `ls /nix/store/zscrhhfyhkwa0qfvbkpg1piklfaahfa4-flow-0.17.1/bin/`.
- Store bytes: `sha256sum`/`stat` on `/home/li/.local/state/flow/flow.sema` and `/home/li/.local/state/flow-next/.local/state/flow/flow.sema`; `strings -n6` on the stable store.
- Repo text: `/git/github.com/LiGoldragon/flow/DESIGN.md`, `/git/github.com/LiGoldragon/flow/UPGRADES.md`, `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/store.rs`, `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/delivery.rs`, `/git/github.com/LiGoldragon/signal-flow/src/generated/signal.rs`, `/git/github.com/LiGoldragon/meta-signal-flow/src/generated/signal.rs`.
- Orchestrate: `orchestrate 'Observe.Locks'` (before acquiring), `orchestrate 'Lock.{ ... }'` (lock 8489).
