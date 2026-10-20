# Session inventory, Ouranos and Zeus, 2026-10-19 12:40 CST

Observed read-only by a subflow of d68c82. Sources: `ps` and `/proc/<pid>/cmdline|environ`;
`herdr session list`, `herdr workspace list`, `herdr pane list`, `herdr agent list`,
`herdr pane process-info`; `flow 'Metaflows'` (Flow registry); messenger routes read through
the installed messenger-clj 0.4.0 library (`messenger-clj.core/route-records`), because `hm-list`
and `hm-heartbeat-state` refuse with `MetaflowMetadataRequired`; `journalctl --user -u flow-nexus`;
transcript mtimes under the Claude and Codex active transcript roots. Last activity is the
transcript's mtime. Harness and model come from the process argv, not the title.

## Installed

| Part | Version / state | Witness |
|---|---|---|
| flow, flow-nexus, flow-hook | 0.35.11 (`kg2ivz…-flow-0.35.11`; source flow-da2038-firsttool 67b80b3) | readlink of PATH binaries |
| flow-nexus.service | running since 10-17 06:26, pid 727912 | systemctl |
| Flow store | ~/.local/state/flow-production/flow.sema | ExecStart |
| message-nexus.service | message 0.19.1, running since 10-17 06:26 | systemctl |
| messenger-clj (hm-*) | 0.4.0 | wrapper script |
| Herdr | 0.8.2; session `default` running; session `--help` stopped | herdr session list |
| Codex | app-server 0.161.0-alpha.2 (active home), plus 0.153.4 and codex-next 0.158.0-alpha.9 servers | ps |
| Integration Flow 0.35.19 | branch-only, not deployed (claim, d68c82 log 18:37) | not witnessed here |

## Ouranos: live seats

Layer table (knowledge-layer-models as quoted in the base context): Psyche on Claude — Primary Fable, Secondary Opus, Tertiary Sonnet, Quaternary Haiku; Mind/Field on Codex — Primary Astra, Secondary Sol, Tertiary Luna, Quaternary Luna low. Medium effort except the OpenAI Quaternary.

| Pane | Pane title | Herdr agent name | Flow id | Harness / model / effort (argv) | Aspect, topic, layer | Herdr state | Last activity | Flow registry | Messenger route | Ghost |
|---|---|---|---|---|---|---|---|---|---|---|
| w1:p1F | `Field.{ Sol 42265e }` | field_sol_42265e | 42265e | codex / gpt-6.1-sol / medium | Field Core Secondary | working | 10-19 12:40 | absent | Field Core Secondary | title form |
| w1:p1G | `Mind.{ Sol 41fa34 }` | mind_sol_41fa34 | 41fa34 | codex / gpt-6.1-sol / medium | Mind Core Secondary | working | 10-19 12:40 | absent | Mind Core Secondary | title form |
| w1:p29 | `{ Field Primary 44cda5 }` | field_primary_44cda5 | 44cda5 | codex / gpt-6-astra / medium | Field Core Primary | idle | 10-16 10:45 | absent | Field Core Primary | title lacks topic |
| w1:p2D | `{ Mind Primary 0c85a3 }` | mind_primary_0c85a3 | 0c85a3 | codex / gpt-6-astra / medium | Mind Core Primary | working | 10-19 12:40 | absent | Mind Core Primary | title lacks topic |
| w1:p31 | `{ Psyche Spirit Primary d55c56 }` | psyche_spirit_primary_d55c56 | d55c56 | claude / claude-fable-5-1 / medium | Psyche Spirit Primary | idle | 10-19 11:57 | absent | Psyche Spirit Primary | — |
| w1:p33 | `{ Psyche core Secondary d68c82 }` (argv `--name { Psyche Secondary d68c82 }`) | psyche_core_secondary_d68c82 | d68c82 | claude / claude-opus-5-5 / medium | Psyche core Secondary | working | 10-19 12:40 | Awake.d68c82, 36 queued orders | Psyche Core Secondary | 36 undelivered Flow orders |
| w1:p35 | `{ Psyche Nexus Secondary 058f16 }` | psyche_nexus_secondary_058f16 | 058f16 | claude / claude-opus-5-5 / medium | Psyche Nexus Secondary | done | 10-19 12:29 | absent | absent | duplicate role (handover.md written; successor a275c0) |
| w1:p3F | `{ Psyche Spirit Secondary ee57fb }` | psyche_spirit_secondary_ee57fb | ee57fb | claude / claude-opus-5-5 / medium | Psyche Spirit Secondary | done | 10-19 12:02 | absent | Psyche Spirit Secondary | — |
| w1:p3J | `{ Field PrimaryCommitting Quaternary 89fbc1 }` | field_quaternary_89fbc1 | 89fbc1 | codex / gpt-6-luna / low | Field PrimaryCommitting Quaternary | done | 10-19 11:46 | absent | Field PrimaryCommitting Quaternary | — |
| w1:p3M | `{ Psyche InstructionWitness Quaternary 19d9f2 }` | psyche_instructionwitness_19d9f2 | 19d9f2 | claude / claude-haiku-5-5 / medium | Psyche InstructionWitness Quaternary | done | 10-19 12:03 | absent | Psyche InstructionWitness Quaternary | purpose unknown (witness seat; possibly test) |
| w1:p3N | `{ Mind Tools Secondary 47d946 }` | mind_tools_secondary_47d946 | 47d946 | codex / gpt-6.1-sol / medium | Mind Tools Secondary | done | 10-15 23:19 | absent | Mind Tools Secondary | stale 4 days |
| w1:p3P | `{ Mind Tools Primary 0430eb }` | mind_tools_primary_0430eb | 0430eb | codex / gpt-6-astra / medium | Mind Tools Primary | done | 10-14 09:47 | absent | Mind Tools Primary | stale 5 days |
| w1:p3X | `{ Psyche Communication Secondary 3960eb }` | psyche_communication_seco_3960eb | 3960eb | claude / claude-opus-5-5 / medium | Psyche Communication Secondary | done | 10-19 12:26 | absent | Psyche Communication Secondary | no Primary live for the pair |
| w1:p41 | `{ Mind Prototyping Secondary e4b7d7 }` | mind_prototyping_secondar_e4b7d7 | e4b7d7 | codex / gpt-6.1-sol / medium; system prompt from flow-evidence/42265e/codex-clojure-birth-20261014 | Mind Prototyping Secondary | done | 10-15 19:10 | absent | Mind Prototyping Secondary | testing leftover |
| w1:p42 | `{ Mind Prototyping Primary 5b9075 }` | mind_prototyping_primary_5b9075 | 5b9075 | codex / gpt-6-astra / medium; same test birth packet | Mind Prototyping Primary | done | 10-15 19:02 | absent | Mind Prototyping Primary | testing leftover |
| w1:p4B | `{ Psyche nexus Secondary a275c0 }` | psyche_nexus_secondary_a275c0 | a275c0 | claude / claude-opus-5-5 / medium | Psyche Nexus Secondary | done | 10-19 12:34 | absent | Psyche Nexus Secondary | duplicate role with 058f16 (holder) |
| w1:p4C | `{ Psyche core Primary 39bd0c }` | psyche_core_primary_39bd0c | 39bd0c | claude / claude-fable-5-1 / medium | Psyche core Primary | done | 10-19 11:46 | absent | Psyche Core Primary | — |
| w1:p4D | `{ Psyche chronos Secondary 504f11 }` | psyche_chronos_secondary_504f11 | 504f11 | claude / claude-opus-5-5 / medium | Psyche chronos Secondary | done | 10-19 11:55 | absent | Psyche chronos Secondary | — |
| w1:p4E | `{ Psyche core Tertiary 4201a3 }` | psyche_core_tertiary_4201a3 | 4201a3 | claude / claude-sonnet-5-5 / medium | Psyche core Tertiary | done (pane list: working) | 10-19 12:39 | absent | Psyche core Tertiary | — |
| w1:p4H | `{ Mind flow Primary 9896d8 }` | mind_flow_primary_9896d8 | 9896d8 | codex / gpt-6-astra / medium | Mind flow Primary | done | 10-18 16:27 | absent | Mind flow Primary | — |
| w11:p1 | `{ Mind ethos Secondary 66f2bb }` | mind_ethos_secondary_66f2bb | 66f2bb | codex / gpt-6.1-sol / medium (Flow-launched) | Mind ethos Secondary | done | 10-18 17:39 | Awake.66f2bb, 0 queued | Mind ethos Secondary (route name codex-6679f6…) | — |
| w12:p1 | `{ Mind context Secondary 877549 }` | mind_context_secondary_877549 | 877549 | codex / gpt-6.1-sol / medium (Flow-launched) | Mind context Secondary | done | 10-18 18:57 | Awake.877549, 7 queued | Mind context Secondary (route name codex-7570bd…) | registered but unreachable: 7 orders undelivered, FlowUnreachable reported |
| w13:p1 | `{ Mind nexus Secondary a6689e }` | mind_nexus_secondary_a6689e | a6689e | codex / gpt-6.1-sol / medium (Flow-launched) | Mind nexus Secondary | done | 10-18 19:33 | Awake.a6689e, 5 queued | Mind nexus Secondary (route name codex-40b780…) | 5 orders undelivered |
| w14:p1 | `{ Mind books Secondary 3c49f5 }` | mind_books_secondary_3c49f5 | 3c49f5 | codex / gpt-6.1-sol / medium (Flow-launched) | Mind books Secondary | idle | 10-18 13:17 | Awake.3c49f5, 0 queued | Mind books Secondary (route name codex-4f2a0c…) | idle since launch |
| w15:p1 | `{ Mind flow Secondary 442bd9 }` | mind_flow_secondary_442bd9 | 442bd9 | codex / gpt-6.1-sol / medium (Flow-launched) | Mind flow Secondary | idle | 10-18 13:17 | Awake.442bd9, 1 queued | Mind flow Secondary (route name codex-a339f1…) | first order never delivered |
| w2E:p1 (workspace label `claude-c8c263b451abff0a9ccb0d94`) | `{ Psyche flow Secondary aa034f }` | claude-c8c263b451abff0a9ccb0d94 | aa034f | claude / claude-opus-5-5 / medium; --remote-control, flow-hook (Flow-launched; pane respawned 12:38) | Psyche flow Secondary | working | 10-19 12:39 | Awake.aa034f, 2 queued, past 17c364 | Psyche flow Secondary, pane recorded w16:p1 (now w2E:p1) | raw Herdr name; stale messenger pane id |
| w1:p2N, w1:p3D | `~/primary` | — | — | zsh only | — | unknown | — | — | — | idle shells |

## Registry rows with no live seat

| Registry | Row | State | Ghost reason |
|---|---|---|---|
| Flow | Field message Primary, Awake.flow-0000000000000013, 18 past ids flow-…01..12 | no pane | test fixture rows in the production store |
| Flow | Field send-proof-03510 / startup-codex-0355 / startup-proof-0355 / proof / flow Quaternary | Asleep | testing leftovers |
| Flow | Psyche ethos Secondary, past 804eb9 | Asleep | none (asleep by design) |
| Messenger | 804eb9 Psyche ethos Secondary, pane wV:p1 | pane gone | stale route |
| Messenger | 3ff3fe Field send-proof-03510 Quaternary, pane wN:p1 | pane gone | test route |
| Messenger | 75f438 Field startup-codex-0355 Quaternary, pane wK:p1 | pane gone | test route |
| Messenger | 127d95 field_quaternary_127d95, pane w1:p3E | pane gone, no aspect/topic/layer | stale; blocks hm-list and hm-heartbeat-state |
| Messenger | 8b084b field_quaternary_8b084b, pane w1:p3A | pane gone, no aspect/topic/layer | stale; blocks hm-list and hm-heartbeat-state |
| Herdr | session `--help` | stopped | created by a mistyped command |

## Zeus

Reached by `ssh zeus` as li. li's Herdr session `default` is stopped. bird's Herdr sessions could not be listed (ssh as bird refused; li cannot read bird's /proc environ), so models are unread.

| Process | Label | Harness / model | Age | Ghost |
|---|---|---|---|---|
| bird herdr `claude-remote-1/2/3` | `Zeus Claude 1/2/3` | claude, model not in argv | 5 days | not flows; the living's cloud panes |
| bird herdr (default), 4 claude, three `--resume` | — | claude, model not in argv | 20 h | not flows |
| bird herdr `codex-recovery-20261014`, `-2`, `-3` | — | zsh only, no agent | 5 days | leftover recovery sessions |
| bird codex app-server 0.163.0 and 0.153.4 | — | codex servers | 19 h / 15 days | 0.153.4 server is the superseded one |

## Rollout evidence

- Flow 0.35.11 launched the five Mind topic Secondaries (66f2bb, 877549, a6689e, 3c49f5, 442bd9) on 10-18 13:15–13:17 through its own Codex app-server proxies (children of flow-nexus 727912), on the right model (Sol, medium); and aa034f (Opus, --remote-control, flow-hook) as Psyche flow Secondary, its pane respawned at 12:38 today.
- Titles: Flow's starter set raw Herdr names (codex-…, claude-…); the five Mind seats were relabelled by hand (d68c82 log, "labels to titles"); aa034f still carries `claude-c8c263…` as workspace label and agent name.
- Messaging: Flow delivers queued work at wake (877549 received "Work queued for this metaflow…" at 18:57 on 10-18), but orders queued to a live idle or working seat stay queued: 877549 7, a6689e 5, 442bd9 1, aa034f 2, d68c82 36. The Message Nexus returns FlowUnreachable when Flow's meta socket refuses or cannot resolve the peer (message-nexus service.rs:39–45, 150); d68c82 recorded FlowUnreachable for 877549.
- Journal: launch refusals on 10-17 (ModelOrEffortDiffers, PartDiffers, NotForHarness(ClaudeAiConnectors)); Codex send-tool reconnects with "WebSocket message exceeds limit"; aa034f and 804eb9 repeatedly "kept at its Stop: NotResting".
- Every other live seat was started by the earlier launchers, outside Flow; Flow does not hold them (no rows), so Flow cannot route to or retire them.
