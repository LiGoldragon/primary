# System-Operator Report Inventory

Read-only audit for the dispatcher meta-report at
`reports/system-operator/169-context-maintenance-2026-05-28/`.

## Executive Recommendation

System-operator can retire most stale reports after confirming the cloud
forwarding boundary. The recommended action set is:

| Reports | Action | Dispatcher note |
|---|---|---|
| `156`-`160` | Forward then drop | Forwarding is effectively complete into cloud-designer/cloud-operator reports; ask cloud lane to confirm absorption before deletion. |
| `162`, `163`, `165` | Drop | Superseded by the schema-next re-grounding: system-designer `40`, `42`, cloud-operator `11`, and current prototype `167`. |
| `164` | Forward then drop | Its production-vision substance is now carried by system-designer `40`, cloud-operator `11`, and prototype/audit reports `167`/system-designer `42`. |
| `161` | Drop | Superseded by `166` on the same DJI mic keepalive problem. |
| `166`, `167`, `168` | Keep | Current operational/handoff artifacts. |
| `139` | Migrate, then drop | Arca is live enough that this belongs in Arca docs, but current `arca/ARCHITECTURE.md` has not fully absorbed it and partly conflicts with it. |
| `1`, `2`, `3`, `4`, `5`, `6`, `7` | Mostly drop, with two migration checks | `1`/`2` are old STT design rationale; migrate only if Whisrs/per-repo docs lack durable-first state. `7` is old Spirit deployment history superseded by `skills/spirit-cli.md` and current Spirit work. `4`-`6` are absorbed into NOTA guidance/INTENT. `3` is external-video notes, not system-operator context. |

If the dispatcher wants the lane under the 12-report soft cap without waiting
on cross-lane confirmation, the safe immediate drops are `161`, `162`, `163`,
and `165`. The cloud and Arca actions should wait for their named landing
checks.

## Cloud Reports `156`-`160`

Recommendation: **forward then drop**.

Evidence:

- `reports/cloud-designer/4-fully-working-prototype-cycle-2026-05-27/8-overview.md`
  says the cycle mined "the 13 settled-design reports", explicitly including
  `system-operator/156-160`, then implemented and audited the cloud component.
- `reports/cloud-designer/4-fully-working-prototype-cycle-2026-05-27/2-reports-working-solutions.md`
  extracted the concrete design buckets from the source reports: operation
  routing, owner-vs-ordinary split, provider gating, credential handling, and
  prototype constraints.
- `reports/cloud-operator/9-cloudflare-dns-tool-2026-05-27.md` landed the
  Cloudflare DNS path on `cloud/main`, including ordinary observation,
  owner `PreparePlan`/`ApprovePlan`/`ApplyPlan`, flarectl execution, and
  redirect deferral.
- `reports/cloud-operator/10-audited-cloud-domain-prototype-2026-05-27.md`
  landed the domain-criome/cloud handoff path and explicitly closed several
  designer-cycle gaps.

Per-report action:

| Report | Action | Evidence |
|---|---|---|
| `156` Cloudflare API surface research | Forward then drop | API/DNS/redirect facts are now current in cloud-designer `4` and cloud-operator `9`/`10`; redirects remain future work there. |
| `157` provider API scope research | Forward then drop | Provider family/gating shape is carried by cloud-designer `4`; later provider support is still intentionally deferred. |
| `158` signal foundation for cloud triads | Forward then drop | The triad split is embodied in `cloud`, `signal-cloud`, and `owner-signal-cloud`; stale `system-specialist` framing and the bad intent-capture note should not remain the working source. |
| `159` cloud repo scaffold prototype | Drop after confirmation | Its pre-repository scaffold plan is superseded: repos exist and current code is represented by cloud-operator `9`/`10`. |
| `160` cloud-domain criome birth design | Forward then drop | The component boundary is now absorbed by cloud-designer `4` and cloud-operator `10`; current implementation has advanced beyond the birth report. |

Cloud-lane confirmation is still useful because the older cloud-operator
recap (`cloud-operator/8`) previously said "do not retire system-operator
cloud reports yet"; the newer cloud-designer `4` and cloud-operator `9`/`10`
are the evidence that condition has mostly changed.

## Lojix / Horizon / CriomOS Reports

Recommendation: **drop `162`, `163`, `165`; forward then drop `164`; keep
`167`**.

`162` is a production-to-lean drift snapshot. `163` already critiques it after
the schema-next refresh and says it is stale as architecture guidance. The
cross-lane system-designer report `44/2-lojix-horizon-criomos.md` confirms both
are superseded by system-designer `40` and `42`.

`165` implemented source staging in the `lojix/schema-deep` prototype. It is
valuable event history, but the source-staging step is now absorbed into the
broader schema-next port feasibility and iteration-merge line:
system-designer `37` says `/165` should merge with the iteration-2 Nexus/SEMA
work, and system-designer `40`/`42` re-ground the whole Horizon/Lojix stack.

`164` is stronger than the others because it contains the broad production
vision. Do not drop it merely because it is older. Drop it only after the
dispatcher accepts that its substance is now forwarded into:

- system-designer `40` for the schema-next port feasibility and production
  replacement direction;
- cloud-operator `11` for the newest cross-cutting Lojix/Horizon/CriomOS audit;
- system-operator `167` plus system-designer `42` for the Horizon pure-schema
  prototype and divergence audit.

`167` should stay. It is the current artifact report for the Horizon
pure-schema concept prototype, and system-designer `42` reviews that artifact
rather than replacing it.

## DJI Mic Reports

Recommendation: **drop `161`; keep `166`**.

`161` repaired the original keepalive service by creating a visible sink and
bridging DJI Bluetooth source audio through `pw-loopback`. `166` is the newer
report on the same operational issue. It explains the remaining profile-churn
failure mode, changes the service to reassert the Bluetooth profile in place
without tearing down the loopback, and records live verification after
activation.

`166` is the current device-state report. If a system-operator runbook exists
later, migrate the final behavior there and retire `166`; for this pass, keep.

## Spirit Report `168`

Recommendation: **keep**.

This is the newest Spirit signal-surface audit in the system-operator lane.
System-designer `43` validates it and says the findings are real; it extends
the recommendation toward the schema-derived migration. Keep `168` as the
current production-surface audit until the naming pass and structural
schema-derived migration land.

## Arca Report `139`

Recommendation: **migrate to Arca docs, then drop from system-operator**.

`139` is not really cloud context. It is an Arca architecture report with
substance that belongs in Arca's permanent docs:

- full BLAKE3 digest is object identity;
- filesystem locator is daemon-allocated and stable once exposed;
- short-prefix collision policy extends later objects rather than renaming
  old locators;
- `/arca` is recommended as the system-service root for CriomOS/Lojix use;
- `signal-arca` names the daemon verbs;
- the daemon owns writes, full-hash verification, locator allocation, state,
  replication, garbage collection execution, and capability enforcement.

Current `/git/github.com/LiGoldragon/arca/ARCHITECTURE.md` has partially
absorbed the broad component shape, but not this full report:

- it already says Arca is a content-addressed filesystem hashed by BLAKE3;
- it already names a library plus privileged daemon, write-only staging,
  multi-store, read-only consumers, and `signal-arca`;
- it still uses `~/.arca/<store-name>/` as the store root, while `139`
  argues the deployment role should start at `/arca`;
- it stores objects directly under `<blake3>`, while `139` separates full
  identity from stable human-facing locators.

Because there is no `arca/INTENT.md` in the checkout, the clean action is:
migrate the load-bearing design into `arca/ARCHITECTURE.md` and create or
update `arca/INTENT.md` if backed by recorded psyche intent. Until then, keep
`139`; after migration, drop it.

## Old Reports `1`-`7`

Recommendation: **drop `3`, `4`, `5`, `6`, `7`; migrate-or-drop `1` and `2`
depending on Whisrs docs**.

Per-report action:

| Report | Action | Evidence |
|---|---|---|
| `1` Whisrs durable-first STT research | Migrate or drop | It carries real design: durable `RecordingSession`, artifact-first capture, attempt ledger, retry after restart/network/backend failure. If Whisrs/CriomOS-home docs do not state this, migrate a compact runbook/design note first. Otherwise drop. |
| `2` persona speech component brainstorm | Migrate or drop | The component-boundary decision (`persona-transcription` separate from synthesis, raw audio as data-plane carve-out) is durable design if still desired. Migrate only if no current Persona speech design doc carries it. Otherwise drop with `1`. |
| `3` Mario Zechner AI agent points | Drop | Useful external-video notes, but not system-operator state and no clear permanent workspace home from this pass. |
| `4` NOTA mixed-enum support vision | Drop | Absorbed by current NOTA/schema direction and workspace hard rules; no longer a system-operator handoff. |
| `5` NOTA syntax exception audit | Drop | Map/tuple/bracket discipline is now in `skills/nota-design.md`, `AGENTS.md`, and `INTENT.md`; the report is implementation event history. |
| `6` NOTA family audit | Drop | Absorbed by NOTA guidance and current schema-stack INTENT; residual gaps should live in NOTA repo tasks/docs, not system-operator reports. |
| `7` persona-spirit production user session | Drop | Superseded by current `skills/spirit-cli.md`, versioned Spirit deployment reports, and active production Spirit work. |

The one caution is STT. `system-designer/44/4-persona-runtime-spirit-upgrade.md`
already flags `system-operator/1` and `/2` as historical STT research. They
should not stay in system-operator merely as old research, but their
durable-first substance is specific enough that the dispatcher should check
Whisrs/CriomOS-home docs before deletion.

## Final Action List

Immediate safe drops:

- `161`
- `162`
- `163`
- `165`
- `3`
- `4`
- `5`
- `6`
- `7`

Forward-confirm then drop:

- `156`
- `157`
- `158`
- `159`
- `160`
- `164`

Migrate before drop:

- `139` to Arca docs.
- `1` and `2` only if Whisrs/persona speech docs lack the durable-first and
  transcription-boundary design.

Keep:

- `166`
- `167`
- `168`
- `169/` current context-maintenance meta-report.
