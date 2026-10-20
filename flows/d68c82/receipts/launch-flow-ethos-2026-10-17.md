# Launch receipt: fresh Psyche flow and ethos Secondaries, 2026-10-17

Launcher: production Flow 0.35.11 Start (/nix/store/kg2ivzfy344gdc0hrw7z7vdif55f1iid-flow-0.35.11), through submitStart/startRequest of /home/li/primary/tools/flow-start-adapter.mjs, called from /home/li/primary/flows/d68c82/launch/flow-ethos-2026-10-17/start.mjs. The old launcher was not used. Modules from /home/li/primary/config/main-flow (Psyche aspect plus row); pinned refs psyche-context 53f68b69c3f9a7628e804dcd69cb47cd5db9bb33, mind-context e3fcd4f36d4f75e8c546e5e9596f5a48a5d8592b, field-context 95121c6727052941f7e5f0c1125f8118d737e561.

## Ethos: 804eb9
- Request d68c82-ethos-secondary-20261017-02; native 804eb927-4185-5e72-9f8d-a83a88a5c12f; Claude, claude-opus-5-5, medium; predecessor 65f93a.
- Modules 34 of 34: system 9/9, user 25/25. System prompt sha256 61edfbb013ca02a712ceab5a86bab866060dcabf24d4161d96c570bc27d6fe2f equals the text rebuilt from the 9 pinned sources plus "Predecessor: 65f93a". The user part's 25 bodies equal their pinned sources (compensation-main-flow after Claude rendering); part sha256 1ad0c7a02dc70c53917f1998a0386c7717c055818fa73b5c316187200c5a14cc, LaunchStatus PromptObserved.
- First message carries `Address.{ Psyche ethos Secondary }`. Pane wS:p1 was titled `{ Psyche ethos Secondary 804eb9 }`. It answered, claimed 804eb9 with flow-id, and presented its context at 17:01:16Z.
- Then Flow ended the pane at rest. Observe.Agent.804eb9 = Gone; Current.{ Psyche ethos Secondary } = Asleep, Past [ 804eb9 ].
- hm-register failed: MetaflowAlreadyRegistered: Psyche ethos Secondary (still held by 65f93a). No brief was sent; it was not verified on hm-send. 65f93a is not retired.
- Earlier attempt -01 was refused StartRejected.NativeLaunchRefused.{ Receipt PartDiffers }; native bcdce238-ed56-5d4c-abf1-54af8d4cf932, pane closed by Flow. Cause, witnessed by hash: the brief ended in "\n" and Claude's pasted_content wrapper drops that final newline. The stripped text hashes to 1ad0c7…, the intent part to 38f87c… (= text + "\n"). Retried with the brief trimmed.

## Flow: 17c364
- Request d68c82-flow-secondary-20261017-03; native 01a14acf-8089-7873-abaf-bad17c364db0; Codex, gpt-6-astra, medium; predecessor da2038; explicit Codex leave-outs [ CodexAgentsMd CodexSkillListing CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions ].
- Modules 34 of 34: base_instructions holds 9/9 system bodies equal to their pinned sources, plus "Predecessor: da2038". The user message holds 25/25 bodies equal to their pinned sources (compensation-main-flow after Codex rendering). turn_context gpt-6-astra medium. A 688-byte <recommended_plugins> developer block is still present.
- First message carries `Address.{ Psyche flow Secondary }`. Pane wT:p1 is titled `{ Psyche flow Secondary 17c364 }`. It answered (task_complete) and is Awake (Current.Awake.17c364).
- The adapter's hm-register exited 0.
- Brief NOT delivered: `FLOW_ID=d68c82 hm-send "Psyche flow Secondary" --psyches --stdin` returned MessageRefused.{ «Psyche flow Secondary» Unidentified }. The address is Flow-managed, so messenger-clj routes it through Message. Message identifies the sender through Flow, and flow 'ResolveCaller.None' from d68c82 answers CallerResolutionRejected.CallerUnknown. By flow id the send returned MetaflowRequired. da2038 is not retired.
- Attempt -02 was refused StartRejected.LeaveOutRefused.NotForHarness.ClaudeAiConnectors: with leave-outs None, Flow applies the configured Claude leave-outs of { Psyche flow Secondary }.
- flow-meta Configuration gives Psyche flow Secondary only Claude leave-outs, and Secondary claude-opus-5-5. A wake of this address after it sleeps would therefore not be Astra (inference from configuration, not witnessed).

## Prepared, unsent
- Psyche payload: /home/li/primary/flows/d68c82/launch/flow-ethos-2026-10-17/psyches.edn (three records, verbatim checked against flow.md, ethos.md and log.md).
- Flow brief: /home/li/primary/flows/d68c82/launch/flow-ethos-2026-10-17/flow-msg.txt (includes both coordinator additions on the unrelayed comments).
- Continuation records written: /home/li/primary/flows/17c364/continuation.json, /home/li/primary/flows/804eb9/continuation.json.

## Sender binding and briefs (after Field imported d68c82's binding)
- Ran bind-from-own-flow.py once (it only Binds, sends nothing): `Bound.d68c82`; `ResolveCaller.None` → `CallerResolved.{ d68c82 Psyche Medium claude-opus-5-5 }`.
- To "Psyche flow Secondary": psyches.edn → `Queued.{ «Psyche flow Secondary» }`; flow-msg.txt → `Queued.{ «Psyche flow Secondary» }`.
- To "Psyche ethos Secondary": psyches.edn → `Queued`; ethos-msg.txt → `Queued`. The address woke as `Current.Awake.804eb9` (the same native session, resumed in pane wV:p1). At 17:16:47Z the transcript shows Flow's "Work queued for this metaflow…" turn carrying both items, sent by Psyche core Secondary. 804eb9 logged the brief, dispatched two subflows, and answered at 17:17:18Z: accepted.
- 65f93a: `hm-retire "Psyche ethos Secondary"` → `Retired.{ «Psyche ethos Secondary» }`; evidence ~/.local/state/messenger-clj/retirement-evidence/65f93a-20261017T171919880930143Z.json. Its pane w1:p4A is still open.
- 804eb9: `hm-register "Psyche ethos Secondary" claude-61cb0ed513fad007a1c51c89 --session default --native-thread 804eb927-4185-5e72-9f8d-a83a88a5c12f --aspect Psyche --topic ethos --layer Secondary` → `Registered.{ «Psyche ethos Secondary» }`.
- 17c364 NOT accepted. Flow's Metaflows still shows both items in the queue of { Psyche flow Secondary }, Awake.17c364. Pane wT:p1 has stayed idle from 11:08 to at least 11:18:58 -06:00, and the brief is absent from its rollout. Possible causes: Flow drains a queue only when it settles a turn's Stop, and 17c364 finished its last turn before the items arrived; or the Codex seat's turn-end report path does not reach Flow. Neither is witnessed. No replay was made. da2038 is not retired, and 17c364 is not registered under "Psyche Flow Secondary".

## Flow acceptance and retirement
- Field delivered the queued items. The 17c364 rollout shows task_complete at 17:24:29Z ("The joint brief is received. I'm gathering the Flow evidence and have requested the Ethos portion…") and at 17:26:50Z (unrelayed comments being checked before logging): accepted and working.
- da2038: `hm-retire "Psyche Flow Secondary"` → `Retired.{ «Psyche Flow Secondary» }`; evidence ~/.local/state/messenger-clj/retirement-evidence/da2038-20261017T172720627368094Z.json.
- 17c364 under "Psyche Flow Secondary": `hm-register … --topic Flow` → `RegistrationIdentityConflict: runtime identity already has another metaflow name`. It is already registered as "Psyche flow Secondary", the name of its Flow-managed address.
- Flow's queue for { Psyche flow Secondary } again holds an undelivered item, sent by Psyche ethos Secondary, while 17c364 is Awake.
