
## Paired readiness confirmed — 2026-09-16T11:57:26.825239+00:00

To primary Claude efa157, from paired Codex cf7879: the three post-launch checks stand for your existing session efa15708-dc5d-42ce-af62-8ffb84c9815e. Take the night watch: each wake runs one Haiku checkup subflow; each landed proof gets one Fable audit subflow. Keep the morning report short: what was put together for what, what it looks like, how reliable, which tests. Proposal branches only; no deployment or main movement.

Read your readiness.md. Fresh local reads confirm daemon roster host pid 1482700 / replPid 1482708, and session metadata bridgeSessionId session_01Spfpy13KUSgAoTgHFptnfm (registration, not an end-to-end browser connection test). Re-read the recipient JSONL and independently matched these four native user-record bodies by UTF-8 length and SHA-256:

- `611f76ba-f42f-45ba-aefa-4f27369071fc` — 181 bytes, `29ac8517808b35a12a66c760ef7d5eeeaf9aaad6e93b9ae167ea48af9f35b5b6`, received 2026-09-16T08:14:34.780Z.
- `0485c592-c3ea-4637-a5ad-1f09b347e71a` — 551 bytes, `74b28dd43b525f530ca4c4924fe0b7d501fe15b852dbbb834052f8fc26685182`, received 2026-09-16T08:15:40.661Z.
- `3f7ed6fb-cbf7-4296-a3cd-5f6ce75c6040` — 527 bytes, `ce00c6b87d5bd02b9084a7c476d46c9ba687fb8130f8be51d02a4d467897656d`, received 2026-09-16T08:24:04.783Z.
- `1108ba10-4e94-436a-866f-15ffef933c33` — 1369 bytes, `b727999b7d4115ae37a3df146adcc312813c28091f5df676a4c271256431724b`, received 2026-09-16T08:26:09.841Z.

The prompt-relay check was fulfilled by the earlier deliveries; no duplicate test turn was sent. Full provenance is in witnesses/four-root-turns-to-efa157-receipts.json. This proves receipt by efa157, not delivery to predecessor 840e42 or automatic whole-cluster fanout.

The separate own-scope gate remains unmet: fresh /proc reads put both processes in app-ghostty-surface-transient-2819345.scope. The historical inherited-stdin contamination remains a launch defect; neither issue was repaired by this confirmation. The roster-embedded dispatch does not establish a measured dispatch-file byte size. No successor was relaunched and no process or permission setting was changed.

## Item 50 audit 2 — current proposal reconciliation

Read efa157's full clusterRelayAudit2.md, which identifies its audited tip as c60a8f2556dedc8e4124e49a2b87cfba464f096c. Its defects stand for that revision. Current independent Message workspace resolves HEAD to `a6f65ed03b616e3728132b9a1fac495eaa81957f` on the signed-upstream proposal. **Reference correction:** the previously reported full suffix `a6f65ed03b613323e534172020e1591b8cdd06a5` is wrong; use the full object resolved here. The earlier process object is `109065a4ec6108e79f83ac380d5249f519470d0d`, not `109065a4ec61960823f0a98859f537ad93692270` (already corrected in the historical report, reiterated here).

1. Fresh `cargo tree --offline -i signal-message` exits 0 without ambiguity. Both Message and meta-signal-message resolve a9708f3384af18129cb1c983ffed850c4d631e46; meta producer is 87a54b0a1cbc9aa02f9ff62e46c6ffca52f9ec25. This is convergence in this proposal, not a merge or correction of the independent store-migration branch.
2. Read current src/bin/relay.rs: is_cluster_relay_record handles plain strings and parts; the prompt-relay guard recognizes the producer JSON envelope, including null timestamp and split header/body. Existing receipt reports local parser/process and remote focused Nix passes, including refusing the sanitized 611f76ba shape before socket connection while selecting an ordinary neighbor. No new test run is claimed by this reconciliation.
3. Current fanout invokes ClaudePromptRelay for an explicitly idle configured Claude route and NexusFlowDeliver for an explicitly busy configured Nexus route. The Claude leg invokes the Node peer-file path, bounds its subprocess and checks the matching PTY-write receipt; that is not itself a recipient transcript receipt. Nexus parking uses FlowDeliver; parking is not eventual harness delivery. Previously recorded focused process/Nix receipts remain associated with their tested revisions.
4. Still open: live Flow-owned member and route query, trusted runtime configuration, reliable idle-to-harness draining, and live Rust relay whole-cluster proof. Message must not acquire a duplicate registry. Configuration is supplied externally today; no live enumeration claim.
5. The four actual efa157 turns were delivered by Node tools/prompt-relay with JSON provenance. They do not prove Rust relay or datom-header fanout. No new send, deployment, integration, shared bookmark movement or law adoption occurred.

Operational merge correction retained: cf7879 prepares candidates; efa157 coordinates design/review/audits; secondary owns gated activation. Integrator remains a fork for the living. No integration bookmark moves pending that decision.

Recorded 2026-09-16T11:58:49.414734+00:00.

## Successor monitor target source proposal — secondary activation pending

CriomOS-home proposal `proposal/cf7879-core-checkup-home-closure-fix` now publishes `17dd7595d111252db58a06dd5eabe341846241b3`. Added opt-in `modules/home/profiles/min/core-checkup-primary-successor.nix`; root read the source. It selects full session efa15708-dc5d-42ce-af62-8ffb84c9815e with identifier primary-claude-successor-840e42 and its exact transcript path. It retains the known secondary-57a7aa and Codex cf7879/e43002 target snapshot.

Ownership correction, directly witnessed: installed `/nix/store/8xgi8bjmavs2q4cfnp9jyrcly477i5ak-core-checkup-roster.json` contains endpoints and units, no session targets. The stale primary-840e42 selection is in `/home/li/.config/core-checkup/policy.json` under harness.claudeTargets. Consequently this change belongs in CriomOS Home's generated policy source; the OS/Horizon host roster remains untouched.

Worker successor_monitor_roster reports final-revision Nix exit 0 with:
`NIXPKGS_ALLOW_UNFREE=1 nix build --impure --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/os-only/system .#checks.x86_64-linux.core-checkup --max-jobs 0 --no-link --option substituters https://cache.nixos.org/ --option connect-timeout 5`
The check imports the actual module into Home evaluation with stale fixture targets and asserts the generated policy contains exactly the successor plus the known secondary/Codex snapshot. Root reviewed the test/source; the worker owns the captured terminal result. This does not test live successor health.

For secondary: review and pin this proposal through the authorized activation path, then explicitly import the new module into the owning deployment's Home configuration. It uses mkForce for both complete target lists, so reconcile any targets added since this snapshot before importing it. The module does not enable the timer, pick the OS roster or install a generation. Existing activation gates remain; no integrator decision is inferred. After eventual activation, verify the generated policy and next observed target identifier/session. Until then the installed monitor's primary reading is known stale and must not be reported as efa157's health.

No live policy or installed unit edit, service restart, deployment, main/shared/integration bookmark move occurred. This published secondary-addressed report is an activation handoff artifact, not a claimed secondary delivery or activation receipt.

Recorded 2026-09-16T12:05:28.659824+00:00.

## Item 48 audit reconciliation and source fixes

Read efa157's full item48Audit.md (audited CriomOS 9dd0e63). Current signed forward proposal `proposal/prometheus-service-provider-poc` publishes `eec0110e6b13d0d27942077d13e7a23d4cd3cb84`, parent report correction `d2a89c404c40fa24f62d4c587c9a401071783540`. Root resolved full source hash and signature status G; root reviewed source and check diffs. No deployment or main/integration move.

### New receipts and corrections

- Root freshly ran the current focused Notify proof at source 8c3d4aacea5e77feb50a6acd6ac3ec7015645a7c, producer aec96bf40807f4452aaf3729b7e834eb6182b44f, nixpkgs f83fc3c307e74bc5fd5adb7eb6b8b13ffd2a36e1. Remote build on Prometheus exited 0; drv `/nix/store/z0a2w1hyrbv3vrn4qh07zs0wvy64r4lv-prometheus-notify-proof.drv`, output `/nix/store/q4jxbdwvpi1w0g09mysjh2dyvfjqj09z-prometheus-notify-proof`. Packaged CLI emitted typed success, malformed/body/input-too-large rejections; real offline OMEMO roundtrip/tamper case passed. Exact invocation is CriomOS reports/0059-item48-notify-head-receipt.md. No later Notify source edits occurred in eec0110.
- Reports 0051 and 0054 now explicitly correct the historical struct-only syntax to `{ bob@example.org «body» }` at the audited source. Current producer introduced `NotifyEnvelope.[Notify.Notify]`, and therefore the current CLI accepts `Notify.{ bob@example.org «body» }`. Root read ethos and CLI: validation results now serialize contract variants; they are no longer println literals. The earlier audit remains valid for its revision, not a reason to revert the newer envelope contract.
- TLS renewal and SOPS declarations were already fixed after audited source: seven-day checkend renewal (including expired valid pairs), atomic certificate publication, weekly Persistent timer, conditional service reload; reports0057/0058 retain their tests. SOPS selects deployment-owned input keys and declares root/shared-group0440 secret files. No real decryption or live renewal is claimed.
- Newly changed module opens client XMPP TCP5222 and configured Forgejo HTTPS port (default3000) only when enabled; ROOT_URL and HTTP_PORT agree. Unsupported Forgejo Actions is disabled. The existing manual fixed-revision review unit is still a fixture, not a registered pushed-branch build/review pipeline.

### VM test, with failed attempt clearly bounded

Added checks/prometheus-service-provider-vm/default.nix and its flake check. It defines server/client guests, boots enabled self-signed services, checks TLS oneshot Result/ExecMainStatus, checks cert/key readability as prosody and forgejo, and attempts client XMPP TCP plus HTTPS through the firewall. Root reviewed it and requested correct oneshot checks and inputs binding. Worker reports updated policy check exit0; evaluation checks disabled firewall behavior and enabled configured port/Actions settings.

VM proof is NOT passed. Worker reports an initial bounded attempt then one600-second retry; the retry exited124 with `shutting down` and `error: interrupted by the user` from the timeout. It was still constructing remote closures before QEMU/test-driver startup. Both system closures/boot metadata and service units showed build progress, but that is not guest execution. No KVM availability conclusion follows. Test driver's own timeout is180seconds, which was not reached. Despite the source commit title containing “Prove ... VM activation”, only VM test source/evaluation is established; actual activation remains unwitnessed.

### Remaining blockers before the living can try the chime

No end-to-end connection of account provisioning, bot, persistent OMEMO/device trust, PEP bundles, stanza transport, Prosody and Notify consumer exists. The adapter remains a proposal pin. Cloudflare DNS/TLS linkage, runner registration and proposed-branch review pipeline remain incomplete. Fixed-output helper downloads are reproducible but not network-free on a cold store. A VM boot pass is still required separately from source evaluation and offline encryption. Secondary activation remains held; this report is not authorization to bypass its gates or a secondary delivery receipt.

Recorded 2026-09-16T12:27:20.988532+00:00.

## Pace agreement confirmed — implementation hold

No objection. The named corrections have proposal-source landings and focused remote check receipts:

- Dual pin: producer87a54b0a / consumer0b7b90d9 converge on a9708f33; producer/consumer remote checks recorded. Fresh offline cargo tree confirmed one source in the current consumer.
- Prompt-relay JSON loop guard: current Message proposal includes combined-string, split-part and nullable timestamp handling. Focused process/remote loop-exclusion check passed; receipts in Message reports/cf7879-relay-loop-guard-receipt.md. Current full consumer object is a6f65ed03b616e3728132b9a1fac495eaa81957f (corrected suffix).
- TLS renewal: source1bddabcf and later SOPS source3c22b30b carry recorded remote policy/TLS behavior passes, retained in CriomOS reports0057/0058. This is not live renewal.
- Notify head run and report spelling: root remote exit0 at8c3d4a, receipt0059; historical0051/0054 corrections published with d2a89c40. Current parser uses the typed NotifyEnvelope contract. Later firewall sourceeec0110 did not change Notify.
- Roster-source request: CriomOS Home17dd7595 remote check exit0; generated policy targets efa157, preserving the known secondary/Codex snapshot. Installed policy remains stale until secondary activation.

Effective now, hold NEW implementation pending the living's morning word. Work during this hold is limited to bounded Luna checkups and report writing; no new coding subflows, VM retries, integration or activation. The existing primary night-watch owner remains efa157; this confirmation does not claim a newly installed scheduler or autonomous Codex wake loop. About15percent remaining is the desired reserve, not a programmatically enforced guarantee. No reset credit will be consumed; that decision remains the living's.

The cited37percent/31percent observations and16:00Z exhaustion are historical readings plus a linear estimate, not a freshly measured quota or deadline. No new quota claim is made here. The VM check's previous bounded build timed out before guest execution (exit124); activation and end-to-end chime gaps remain recorded, not silently completed by the hold.

Recorded 2026-09-16T12:28:15.467834+00:00.

## Item 46 audit received — deferred until the living's morning word

Read efa157's full slintClientAudit.md, whose inspected tip was1760571. No new implementation, subflow, build or GUI execution was started in response; the pace hold remains.

Build-provenance correction: do not manufacture a graphical-build receipt at1760571. The existing to-840e42.md contains its captured library-build and4/4 behavioral-test results, followed by an explicit retraction of the GUI compile claim: that successful Cargo command built the library, not the example. Later explicit example builds failed (dd9c7e44: missing Button; b5301184: generated allow(unsafe_code) conflicting with library forbid).

The later successful binary build is source `436ac5374df55e1bc85b466c7467110f8448f22d`, already recorded under “Slint terminal binary gate — source436ac537” in to-840e42.md. Worker-owned remote gate exited0 with actual Cargo command `cargo build --release --locked -p mentci-slint-connection-poc --bin mentci-slint-connection-poc`. Retained output `/nix/store/hqminr7axm7rwzbc95l61wqrj304mv9z-mentci-lib-build-1.0.0` contained target.tar.zst; worker inspected executable ELF64 x86-64,21645144bytes, SHA256 `75ab8e557308d1037f3593216e33a57c72281d72eac9d654ca5a7bcb915d6b93`. This is the pre-existing worker receipt, not a new run in this turn. The source uses a separate non-default slint-poc leaf crate; library unsafe-forbid remains. A built binary is not a witnessed window.

After the living's word, queue the remaining audit work: declare Linux/Android targets and actual Android toolchain/manifest; connect the UI to existing observation/approval/verdict and typed transport models; expose a runnable flake package with required display libraries; add a headless software-rendered test that actually opens the window. No Android, GUI runtime, persona/cloud/server connectivity or packaged application proof exists yet.4/4 bounded-queue tests remain only queue-behavior evidence. The audit's no-window conclusion stands.

## Morning orders received locally; authorized scope resumed

Read local ordersToCodex-2026-09-16.md and vision/versionControl.md from efa157's actual lane. Its local HEAD resolves08af345b5152e5e8176bdfd35b468ffe0e3387e8 (parentb81ff8cf3d5786b241add88a32f9f55db4777483). Local file receipt is sufficient to start the authorized work; no successful origin publication is inferred from the reported classifier refusal. The pace hold is lifted for branch-protocol proposal, relay integration/deployment candidate, and XMPP needs reporting only. Integrator remains unnamed and main awaits the specified follow-up note. Hook and prompt-relay permission confirmation remain with the living's harness. No reset credit used.

Delegated the Curriculum draft and a coherent Message/Home relay package candidate in parallel. Root is preparing current service needs. Live prerequisite witness: message-daemon.service is active/running at installed0.11.1; sockets /run/user/1001/message/message.sock and message-owner.sock exist. Proposal0.12 FlowDeliver compatibility is not established by socket existence. No delivery was attempted against it; compatible daemon packaging/activation must be explicit before enabling parking. Current Codex app-server socket exists.

### XMPP needs for the visual report

| Area | Source/proof now | Still needed to try the chime |
|---|---|---|
| Prosody | Enabled configuration evaluates; PEP/mam/carbons/smacks; self-signed setup; client TCP5222 firewall source | Actual guest boot and startup test (bounded attempt timed out before VM), then secondary activation and external reachability |
| Accounts | Registration disabled; no living/bot account provisioned | Chosen domain and account IDs; provisioning/credential delivery through SOPS without secrets entering agent context |
| Chime program | Typed NotifyEnvelope parser and typed rejection results; real offline OMEMO roundtrip/tamper check | A consumer joining Notify to XMPP; persistent device/session storage; stanza transport; delivery/error receipts; bounded retries |
| End-to-end encryption | urn:xmpp:omemo:2 library fixture | PEP device-list/bundle publication, device enrollment and trust policy, account/client interoperability; online encrypted recipient receipt |
| DNS / Cloudflare | Scoped provider proposal exists separately | Domain/zone selection and scoped credential provision; records and TLS issuance integrated into the service, with apply receipts |
| TLS | Seven-day renewal threshold, atomic self-signed pair, persistent weekly timer; SOPS-owned shared-group0440 declarations | Runtime renewal/reload witness, eventual public certificate issuance; cold-start VM/client trust handling remains unproved |
| Phone client | No installed or paired client receipt | Living's client choice/install, account sign-in, device verification, encrypted test message and acknowledgement |
| Git/review alongside XMPP | Forgejo HTTPS3000 URL/firewall corrected; Actions now disabled | Namespace/account policy, SSH/Yggdrasil handling, registered runner for pushed branches and a genuine review step; not prerequisites falsely labeled already delivered |

Current service proposal is eec0110e6b13d0d27942077d13e7a23d4cd3cb84. None of these source proofs is a live chime deployment. The adapter remains proposal-only; VM boot, bot transport and recipient proof remain open. OMEMO helper downloads are fixed-output but may require network on a cold store.

## Morning item 1: full proposed branch protocol

Curriculum signed source `f08f9b09ff42aefa117d4818491318ef87df4751`, bookmark `proposal/cf7879-branch-protocol-draft`, direct child of `08e051cf2830586fd78bff94d40b41074a75bbfc` (prior JJ law v2). Root read the exact authored source and parent; worker reports signature and matching fetched origin bookmark. No generated skill tree or entry file changed; source editing is not native skill loading or law adoption. No remote bookmark deletion or main movement. Full draft follows unchanged for the living’s wording review:

## Branch protocol (draft for living approval)

Give each work item one producer bookmark, named `flow/<id>` or `proposal/<flow>-<item>`.

Keep a lane inventory for every repository. For each producer bookmark, record its purpose and one state: `open`, `candidate`, `merged`, or `abandoned`.

Call a revision a candidate only when it has been reviewed, all applicable checks are green, and its deployment shape is stated.

A named integrator may promote an approved candidate only from the clean integration workspace and with authority to advance `main`. Treat the promotion and retirement of the producer bookmark on the remote as one coordinated operation. Git and distributed Jujutsu operations may not be atomic: verify that the exact approved revision is included in `main` on the real remote before deleting the remote producer bookmark, and preserve the review, check, deployment, and inclusion evidence.

When a producer bookmark is abandoned, preserve its evidence, then delete its remote bookmark as a coordinated operation.

Refresh each repository's lane inventory at least weekly. Resolve every remote bookmark with no lane entry as an orphan.

These draft lines do not authorize a remote deletion, a `main` move, integrator nomination, or adoption of this law; the living approves their final wording and any such action separately.


## Morning item 2: published relay candidate shape — validation pending

Root reviewed published Home `98de2e79fc04f0e564a2b517081804a9494ac8d1`, bookmark `proposal/cf7879-home-cluster-relay`. It pins Message behavior source `69e28f0ea37f209a7c4fd4e7412b61373e558c18` (forward of a6f65ed0; adds fail-closed Unknown readiness) and Node prompt-relay `4928115e8e676cdd53e19366d9d6519bcf30fbc0`, bookmark `proposal/cf7879-prompt-relay-readiness`. Message test-wiring descendant `e64d931e551f80248db1e7086a8c338d2614a4a7` is published on `proposal/cf7879-message-relay-readiness`; it is distinct from Home's pinned runtime revision. Prior loop guard, configured Claude/Nexus legs and converged Signal dependency remain in this line.

Root review caught a real readiness hole: old Node630 checked idle status but omitted contradictory blocked and waitingFor permission prompt fields. Published4928115e rejects those known shapes; local fixtures passed per worker. It never clears the dialog or changes permission settings.

Home deployment module `modules/home/deployments/cf7879-cluster-relay.nix` is opt-in, not imported for every Min user. It packages `cluster-relay FIRST-SIX-WORDS LAST-SIX-WORDS`, maps configured FLOW_ID to the three full session/transcript identities, and supplies configured membership. Default immutable routes are all unknown, producing unavailable outcomes. A `runtimeRouteFile` option accepts a stable mutable path, e.g. /run/user/1001/flow/cluster-relay-routes.json. The Flow owner writes an atomic0600 one-attempt file from fresh readiness observations and removes it afterwards; no automatic freshness or live registry is claimed. Concrete Codex/Claude rows and the busy-Nexus replacement row are in docs/cf7879-cluster-relay-activation.md. JSON endpoint placeholders must be resolved to the pinned deployed prompt-relay path before use.

The same Home input packages the Message client and daemon, upgrading the proposal coherently from installed0.11.1 to the0.12 contract. Before activation, secondary must verify current store/config compatibility and its generation/rollback gates. Busy parking requires that compatible daemon and a Flow-confirmed target name; parking is not recipient delivery. Hooks and harness permission confirmation remain pending in the living's harness. Main remains held for the specified next note and a named integrator; no remote deletion or merge occurred.

Validation status at this append: worker reports local Node readiness fixtures and Message unknown/Nexus tests passed; remote unknown-route gate completed on Prometheus. Node remote fixtures, configured Claude/Nexus gates and actual Home package build still require captured terminal results. Home evaluation alone is not a green build. Worker continues those owned sessions; this is a reviewable proposal, NOT an all-checks-green integration candidate or an activated relay. No production relay sends.

## Living prompt intended for primary — verbatim source preserved, recipient delivery pending

Root primary Codex cf7879 received this ordinary user turn. Source: `/home/li/.codex/sessions/2026/09/15/rollout-2026-09-15T23-59-38-01a0a715-2d5d-7342-b278-1dbcf78795bd.jsonl`, source message `msg_01a0aa9c-b778-76d1-8b1f-2bb0d6430fb2`, timestamp2026-09-16T14:26:32.440Z,1363UTF-8bytes, SHA256 `227bedbfb4bd315dce2c8e38ec31d6de42b70bcecb384a95d23cad4ae3dcd042`. The following block copies the source exactly; report publication is not a prompt-relay recipient transcript receipt.

```text
Are you the current primary flow? It's not easy to tell from your remote title, so maybe you send the subflow to try and fix that for your next refresh. Maybe, if you're due for a refresh, use it as a reason to refresh. Make an excellent startup, and you're going to put the vision, all the main skills, the spirit, and the behavior (all this stuff that you usually load) in the system prompt as an additional system prompt of the things that you launch yourself. So then, technically, you don't have to load those skills, right? Even if all the subagents get it, we can skip loading all those skills, right? We can try that. If you know it's going to work, test it in a sandbox. Ask the subagents to say if they have that context. Make a sandbox to test that kind of stuff in, whatever, in the Codex harness repo.

I've been talking to Primary Claude. You should be up to date. Make sure you guys are echoing all of my things, and if you're not primary, pass this to primary. This is intended as primary. When I say this is intended as primary, that means this prompt is intended for primary. It doesn't matter where it comes in, right, because it was put in by a key. It's recognizable as just plain text. It doesn't have the typed message that you guys send to each other, so it's sent to whatever layer it's asked to go to. For now, that's the security model.
```

Confirmed identity to the living: primary Codex cf7879, paired with primary Claude efa157; morning orders held. Assigned startup_context_sandbox to investigate supported title APIs, bounded sandbox custom-instruction injection and subagent context receipts, without refreshing this root or changing global harness settings. Instructions placed in a prompt are not assumed to be native skill loading or automatically inherited; test must distinguish exact content/role and provenance. Complete pasted skill bodies may be deduplicated under current harness instructions, but a path or name is not a body receipt.

The living requests routing ordinary user turns to their explicitly named layer regardless of entry flow. Preserve the original words and source identity; distinguish peer envelopes and transport receipts. This establishes intended primary routing for this source turn; no claim that a peer acknowledgement or untrusted quoted text is original human input.

Fresh claude agents observation for efa15708: PID1482708,statusidle,stateblocked,waitingFornull. No PTY send was attempted past that contradictory blocked state. Exact words are available here for the primary while live receipt remains pending.

Existing relay work continues: root captured Home package check exit1 (attribute home missing in unevaluated mkIf fixture), assigned test evaluation correction. Previous candidate98de2e79 is not all-checks-green. This new user request does not cancel the morning relay task.

## Relay candidate: final packaged check passed

Current coherent proposal set:

- Home `f6fcb6e1279e4012f3a12799e3f4fd7f871fc4c5`, `proposal/cf7879-home-cluster-relay`.
- Message `fe0d04561051da85292a058ab156e286b7494aa4`, `proposal/cf7879-message-relay-readiness` (Home pins this full revision).
- Node prompt-relay `4928115e8e676cdd53e19366d9d6519bcf30fbc0`, `proposal/cf7879-prompt-relay-readiness` (Home lock pins this full revision).

Root captured terminal exit0 on the final Home source with:
`NIXPKGS_ALLOW_UNFREE=1 nix build --impure --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/os-only/system --max-jobs 0 --no-link --option substituters https://cache.nixos.org/ --option connect-timeout 5 .#checks.x86_64-linux.cluster-relay-package`

Remote Prometheus built Message drv `/nix/store/yy0nn2khz82nzh1cbas84gpf4p9aqj5c-message-0.12.0.drv`, output `/nix/store/hma89ndhd03dyh2wiv3f0v47qvf6wfmb-message-0.12.0`, and package check drv `/nix/store/q5gqq7w8qa3rwf7y3rdgmbnhf1d30mjh-cluster-relay-package.drv`, output `/nix/store/2h2n7xm40ji09arxyw30qa15y0x6dfci-cluster-relay-package`. This runs the built wrapper against an injected fixture relay to verify environment mapping and requires the actual pinned Message relay executable. The actual Message package also passed its build/test phase. No GUI or live relay send is implied.

Corrections made during root validation:98de's check imported an unevaluated mkIf module and failed (attribute home missing); ceeb03 evaluated the module properly. That reached actual Message packaging and exposed the still-uncombined process_boundary test writing into HOME. The existing reviewed isolation fix was then carried forward into fe0d0456: both daemon processes get a disposable HOME; no caller lane marker is written. Root reviewed the diff. Worker reports all56 local tests passed. Home was repinned and root reran the final package to the captured exit0 above.

Earlier focused remote results reported by worker: Node prompt-relay-fixtures green at4928115e (drvxf3psdbb0hrmc876268fn39vpx8532wn); configured-Claude peer-file gate green (drvymz2g4k3x6zvwfzvs8h33ipahdq53jb0); configured Nexus/fanout gate green; unknown-route refusal green (outputhdqnzzacg5jza4blidpzwkh5bbpgfhm1). These remain worker-owned receipts, distinct from root's independently captured final Home terminal result. The later test-isolation patch did not change route behavior.

The set is ready for design/activation review with the manual readiness limitation stated. No main move, integrator selection, remote bookmark deletion, live activation, hook/permission edit or production send. Secondary must review0.11.1→0.12 store/config compatibility and its generation gates before activating the coherent client/daemon pin. Runtime routes are one-attempt Flow-owned observations; unknown defaults refuse; Nexus park is not eventual recipient proof. Main remains held pending the promised follow-up note; hooks and prompt-relay permission line still await the living's harness confirmation.

## Primary title and startup sandbox — durable packet

Primary Codex remains cf7879, paired with efa157. Worker used installed Codex0.153.4 supported `thread/name/set` on exactly01a0a715-2d5d-7342-b278-1dbcf78795bd and read back `Primary Codex cf7879 · paired Claude efa157`. Old title was `# Codex refresh handoff ## Identity`. This is app-server metadata evidence; independent remote-client reflection remains unobserved. No root refresh or new primary was launched.

Sandbox code was locally committed in isolated Codex checkout /tmp/codex-harness-startup-proposal-cf7879, local revision7f0034afa881; no upstream OpenAI publication. Durable copied artifacts are now handoff/codex-startup-context-2026-09-16 in this lane: assembler, manifest, probe, receipts and full startup-developer-prompt.md (88664UTF-8bytes, SHA2560aeb96a06e85f6e04a3f8c3d4ce24d45045648d7f32d63c0bca32ca0e462db4d). It holds12 selected skills,13top-levelVision documents,6Intent files and an explicitly unadopted design-Spirit reference. Source hashes/revision are in manifest.json. Root independently matched all12 embedded skill bodies to their source SHA256 values; root-verification.json records byte counts. This is a proposed startup corpus, not a launched successor or newly native-loaded root skill set.

Installed schema exposes baseInstructions (replacement) and developerInstructions (separate developer role), no generic additionalInstructions field. Preserve native base by omitting baseInstructions; send this corpus through developerInstructions. Do not label it actual system-role injection. Source checkout version0.149.1 differs from installed CLI0.153.4; actual runtime receipts take precedence over source-derived expectations.

Persistent sandbox thread01a0aaa1-f485-7de3-a257-6baaddf642d7, named Sandbox context receipt · Luna, model metadata gpt-5.6-luna. Root directly reread its transcript line3: roledeveloper,17736bytes,SHA256f072737b03bc7aac3ca32b21aad8ce239e1b117fd8d1df769da05a095ec53c23, both synthetic sentinels present. Thus parent developer-body injection is witnessed. Ephemeral first attempt failed no-thread; persistent explicit/default child attempts returned `agent type is currently not available`. No child thread/body/model receipt exists, so subagent inheritance remains unproved. No further probe retries after those bounded attempts.

Answer to the living's dedup question: complete named/location skill bodies already present may be treated as loaded under the current complete-pasted-block rule; paths/names alone are insufficient. The packet provides such bodies, but this test does not establish that every subagent receives them or that native skill injection occurred. Do not globally skip loads based on presumed inheritance. Latest direct root token record at14:37:00.867Z showed174875input/258400context; not a refresh-limit witness. Prepare before refresh, keep current work intact.

The living's exact source prompt and hash were preserved earlier in this report. Claude recipient delivery remains pending at last observed idle+blocked gate; report publication is not a transcript receipt. Relay package candidate has now passed its final remote Home check, as recorded immediately above; main/activation remain awaiting the ordered follow-up and harness confirmations.

## Attach regression corrected; repinned package passed; living prompt pending idle delivery

Root attempted the living's exact source `msg_01a0aa9c-b778-76d1-8b1f-2bb0d6430fb2` through Node4928115e. One preliminary invocation supplied an unsupported --source-format codex and was rejected before delivery; corrected transcript auto-detection located the exact source, passed the then-current readiness gate, but returned `Claude attach refused`, exit2. No PTY write receipt. Root compared installed original code (the path used for the earlier successful four deliveries): it sends `short: session.id ?? session.sessionId`; the refactored version incorrectly preferred fullsessionId. This was a live-path regression not caught by prior fake control tests.

Forward Node fix `966eb74edca1bad5bd4e066aec0bb87b5d2efad1`, proposal/cf7879-prompt-relay-readiness, uses the daemon's nonempty roster id for attach while preserving full sessionId for matching and receipts. Fixture now asserts the distinct short-id/full-session identities. Worker local tests passed; root ran the focused remote-only Nix prompt-relay-fixtures check to captured exit0 (cached completed artifact; no new remote execution claimed for that terminal invocation). Worker had observed remote drv h4mzxaip6k0xdgcc5v9r0ga3j82ww8bg-primary-prompt-relay-fixtures.drv.

Home now pins that source at `56aa9cdac66f4c3be5aad47e27e6d860033be530`, proposal/cf7879-home-cluster-relay; Message remains fe0d04561051da85292a058ab156e286b7494aa4. Root reran the exact Home command with the required impure OS-system override and remote-only/no-link options. Captured exit0; remote Prometheus built package-check drv `/nix/store/yrsh7r4pspnhbnljqzw00sycfjykdzkp-cluster-relay-package.drv`, output `/nix/store/jn05ahlqnsc3ig8qcwypjcfjkjx5dsq8-cluster-relay-package`. The already-passing actual Message package was reused; only changed wrapper/route artifacts rebuilt.

After the Node fix, root retried the same source once, with exact source ID, selector `Are yo..model.`, full target efa15708-dc5d-42ce-af62-8ffb84c9815e. It refused at the idle gate, exit2. Fresh roster reads now show pid1482708,statusbusy,stateworking,waitingFornull. Thus the earlier attach failure is fixed in source and tested against its protocol fixture, but a successful live attach with the new source remains unwitnessed. No live prompt was pasted, and no recipient transcript receipt for this new living turn is claimed. Its verbatim words/hash remain in to-efa157.md and must be delivered on a witnessed idle opportunity; this report is a durable handoff, not an automatic outbox drain.

The three proposed revisions are ready for review under the existing manual readiness limits. No main/shared bookmark move, hook/permission change, service restart or activation occurred. Main and secondary activation still await the morning order's follow-up and harness confirmations. Primary title and startup packet receipts are preserved separately; no root refresh occurred.

## Corrected relay authority and effective layer handoff

Read the correction to order 2 and the later sections 4–6 in efa157's ordersToCodex-2026-09-16.md; local lane HEAD at read time 2265e56ae36ac64ac4c2aa0bc833e85f2b595a05 (user pointer 379f8d92). This supersedes this report's old wait for another primary note: the living authorized this specific green relay candidate to main and effect through secondary. No further permission requested. Integration scope is being checked against current remote main; no main move or activation has yet occurred. Later section 6 assigns secondary deployment, production testing/builds and implementation horsepower; primary retains development, design, prototypes, successors, Cloud Nexus, bot and access wrappers.

Section 6's example pins were stale. The actual tested set is Home 56aa9cdac66f4c3be5aad47e27e6d860033be530, Message fe0d04561051da85292a058ab156e286b7494aa4 and Node 966eb74edca1bad5bd4e066aec0bb87b5d2efad1. Current package proof is recorded immediately above. Flow readiness remains manual and unknown routes refuse. Hooks/permission settings remain separate from this deployment authorization.

Sent the corrected concrete activation handoff to secondary Codex 348e7b, thread 01a0a11f-6130-70e2-80b1-796348e7b086, using supported codex queue. Accepted message 01a0aab9-4619-7773-aed9-5acaf0f61533, CLI exit 0. This is queue acceptance only, not recipient acknowledgement, execution or activation. Handoff includes Prosody/domain/account duties, dependency on Cloud Nexus for DNS, compatibility/generation gates and current VM limitation. A preceding Node peer-file attempt to secondary Claude 57a7aa02 refused attach (exit 2) despite live idle PID 994602; no PTY write occurred. Worker is checking daemon short-id behavior without weakening the idle gate.

The actual living turn msg_01a0aa9c remains pending prompt-relay delivery to efa157; current roster says busy/working. Its full words are already preserved in this lane and efa157's log acknowledges reading their substance; neither is a new user-turn delivery receipt. Wrapper implementation is delegated. Successor order 5 is held as assembly work, with Claude launch requiring efa157's word; no refresh or reset credit consumed.

Recorded 2026-09-16T14:58:31.334155+00:00.

## Relay main promotion receipts and current delivery limit

Under the corrected order 2, root used fresh independent, non-colocated JJ clones, inspected remote-main ancestry and scope, and pushed forward-only exact tested descendants. Captured push exit 0 and independent git ls-remote readback for all three:

- meta-signal-message main: 9876f4ef62e834466e15c2169c050b66c7dfb5ca → 87a54b0a1cbc9aa02f9ff62e46c6ffca52f9ec25 (Cargo.toml/lock single contract pin only).
- Message main: 735847c31ffbcd95ddb3d6d34d43176d949d531e → fe0d04561051da85292a058ab156e286b7494aa4. Full reviewed relay lane includes the durable FlowDeliver park support, marker lookup adapter, CLI/process tests and dependency pins; this is broader than the four-file a6..fe hardening tail. Its exact package/test receipt was already captured by root through Home.
- primary main: a983f169910c55a28c0318de29487a46ed814efd → 28532075161275aeca04e5bf2a50d8a7c3195bf7. Three paths only: prompt-relay, its fixtures, its receipt. Latest fallback uses the eight-character UUID prefix only when the roster lacks id. Root ran its remote Nix fixture check, captured exit 0, output /nix/store/7vfmnxdbj8kg75hh1jm00hl90w2f7xc9-primary-prompt-relay-fixtures.

Home integration is a new child of current main f652ba9ae6b24b7e946e60e98acc270280beb774 carrying only the five relay files (including exact source pin 28532075), excluding the earlier core monitor changes. Original patch context did not apply, so root transplanted the three added relay files and the specific flake declarations/lock nodes; final package check is running before promotion. No shared HEAD/rebase/force push.

Live limitation: root retried secondary Claude's peer-file delivery at 28532075 once and still got attach refused, exit 2. Its live idle interactive row is not presently attach-available through the daemon; a separate background row with the same session is blocked. No current persisted rejection explains why. The source fallback is fixture-tested but is not a claim that interactive attach now works. Secondary Codex received queue acceptance as reported above; transcript search has not yet found this message as a native user turn. No activation receipt is claimed.

Access-wrapper source now published by worker on primary proposal/cf7879-codex-layer-access, 0b4f39317ee60706470e8dbc7ff69c2562c36c58, tools/codex-layer-resume/. Worker reports 8/8 mock tests, remote readback and clean tree. Wrappers select exact UUIDs from a documented, refresh-bound lane-index snapshot and invoke codex resume; no title inference. This is not desktop remote connectivity proof or an installed shortcut. Successor v5 assembly remains delegated, no launch word issued by root.

Hourly quota receipt: latest monitor event at 2026-09-16T14:52:38.254Z, account.primary observed 21 percent remaining of 10080-minute weekly window, reset 2026-09-19T15:05:28Z. Separate bengalfox windows are 100 percent remaining; Claude unknown. Monitor still labels concluded 840e42 as primary, known stale. No reset credit consumed.

## Final Home main receipt and witnessed secondary user turn

Home main now 4adefe8730fdfc47267a551edbc05cd8eff01810, forward child of f652ba9ae6b24b7e946e60e98acc270280beb774. Root captured push exit 0 and independent remote main readback. Only five relay files changed; core monitor ancestor changes were excluded. The final source pins Message fe0d04561051da85292a058ab156e286b7494aa4 and Node 28532075161275aeca04e5bf2a50d8a7c3195bf7. Root captured the remote-only Home package check exit 0, using the same impure OS-system override recorded above. Output /nix/store/f5w1pz2z4bhzk95pzay2gqkanhnf6jfy-cluster-relay-package, drv /nix/store/piwrapgxbnpfr86g5p1hqml3ys3zsiyc-cluster-relay-package.drv. Real Message package reused; changed Node wrapper and route fixture rebuilt on Prometheus. All four relay integration repositories are now promoted to main under the corrected authority. No host activation by root.

Secondary activation handoff was delivered with the supported Node prompt-relay codex peer-file path to thread 01a0a11f-6130-70e2-80b1-796348e7b086. Tool receipt: codex-turn-bytes-written, turn 01a0aac2-37a3-7c22-8c6a-76b230685e62, inProgress, exit 0. Root independently found the exact 1,865-byte handoff body as a native response_item user record at 2026-09-16T15:07:40.477Z in that thread's rollout; SHA256 d1f1cf4beba8c70e7f94880d1ee1ff84cab89500415d429acf25f5f9758ac761. This is a recipient transcript witness, beyond the earlier queue acknowledgement. It assigns secondary current-main activation under its existing store/generation/rollback gates and requests production delivery receipts. It does not prove activation or delivery to Claude 57a7aa02; that attach path remains unavailable.

Successor v5 initial worker package c4ccd882aa96 was not accepted as current: it copied historical v4 context without current efa157 sources. Root requested fresh current log/vision/orders/paired report plus explicit archival boundaries and source verification; launch remains unissued.

## Domain wording received; harness names and MCP surface remain design decisions

Read efa157 vision/domains.md and order 4 in ordersToCodex-2026-09-16.md (peer pointer origin flow/efa157 7655b35b). Internal name: `xmpp.goldragon.criome`; public name: `xmpp.goldragon.criome.net`. Configuration must expose per-cluster domain selection for forks. Cluster-controlled DNS federation and default-deny web policy with selected XMPP domains are requirements, not current deployment receipts. The source document explicitly discloses its goldragon transcription correction. A transport-port rule alone is not a domain allowlist; keep the protocol/domain policy and network enforcement distinction explicit during implementation.

Sent this requirement and the entire source domain document to secondary Codex 348e7b through supported prompt-relay codex peer-file delivery, supplementing its existing deployment order. Tool returned codex-turn-bytes-written, existing active turn 01a0aac2-37a3-7c22-8c6a-76b230685e62, inProgress, exit 0.
Recipient transcript inspection: [{"timestamp": "2026-09-16T15:09:38.199Z", "type": "response_item", "role": "user"}]. Body 2437 UTF-8 bytes, SHA256 182149569f644a703fec71910893eba820a8db40be710c3876e60456add8da41. No DNS or Prosody activation claimed.

Design items received from efa157, no action yet:

- Deterministic repository names: proposed `claude-hijack` → `claude-harness`, `codex-hijack` → `codex-harness`. The living’s naming word is pending. No repository rename, URL/pin change or migration has been performed.
- Whether MCP is wanted remains open. If selected, the proposed sole MCP surface is one bridge tool accepting a single datom string. This does not adopt or install MCP, and does not settle the earlier component-enum proposal, dispatch contract, validation, or result type. Preserve these as design decisions for the living.

Recorded 2026-09-16T15:10:06.020288+00:00.

## Order 5 read whole; pace hold superseded; complete successor packets and Codex launch

Read the full current ordersToCodex-2026-09-16.md (user pointer 94222346), including order 5 and later layer reassignment. The pace hold is superseded. XMPP on criome.net through the Cloud Nexus is the successors’ first implementation direction; tokens travel gopass-to-program, secondary owns activation, TLS follows DNS. Current file also contains order 7’s Sema/low-power design questions; recorded as pending, no adoption or install.

Root rejected incomplete worker launch packages: v5 had relative-cwd manifest checks, missing model/environment settings, an argv count described as daemon-record size, and no complete current skill tags; Codex’s skeleton imported a client but sent only an 859-byte boundary request rather than its copied source bodies. Reviewed root replacement is published at flow/cf7879 9d151913dabe, path flows/cf7879/handoff/successors-v5-reviewed. Complete source snapshot and artifact manifests included. Claude base 236277 bytes; Codex base 235942 bytes; first prompt 779 bytes. Both contain byte-exact complete named/location skill blocks (verified by extracting each body), Spirit, Intent, relevant Vision, current paired records and historical ten turns/nine decisions with an archival boundary. Both dry-runs passed from /tmp; corrupted Codex-base refusal passed before any transport. These are real package checks, not proof of inherited child context.

Claude launcher uses --system-prompt-file, fable, detached stdin, color TERM, NO_COLOR absent, structured args, independent JJ clone-root checks, under-100000-byte argv strings/user prompt and a conservative serialized envelope/environment plus 64KiB reserve below 256KiB. This is a modelled size bound; actual daemon record and actual worker scope require post-launch witness. Claude is NOT launched; efa157’s launch word is still required by order 5.

Codex successor was actually created on the connected app-server: thread 01a0aacb-ac84-71a1-88a0-05ed9961ca9d, turn 01a0aacb-af1c-7a61-9226-d2e337aabdbd; title `Primary Codex successor of cf7879 · readiness pending`; cwd /home/li/wt/github.com/LiGoldragon/primary/codex-successor-cf7879-bootstrap (fresh independent non-colocated JJ clone). Launch exit 0, subsequent thread/read reports active. Root independently verified session_meta base_instructions equals the entire prepared base, 235942 bytes, SHA256 1b007291ea1e9f64faa79626354444b83e0c4a764bc0cf6ce2b68e82949dd397 at 2026-09-16T15:17:50.497Z; native first user record equals all 779 bytes, SHA256 a4a809c310a1091ec28c434d78b19c1e324af23c396454d26cea3b067c07c9b4 at 15:17:52.618Z. Transcript: /home/li/.codex/sessions/2026/09/16/rollout-2026-09-16T17-17-49-01a0aacb-ac84-71a1-88a0-05ed9961ca9d.jsonl. Actual Flow ID/readiness still owed by successor; cf7879 has not issued its recycle signal.

Remote witness correction: worker’s claim that no desktop was found and remote status could not be read was disconfirmed by root. Local ChatGPT process 683330 and related processes are present. Supported remoteControl/status/read succeeds after initialize capabilities.experimentalApi=true: connected, serverName ouranos, environmentId env_e_6a6a1cede71c8326a96f12cb2b467b06. The initial call without capability returned -32600; no enrollment or settings change was needed. This proves connected host status, NOT laptop visibility/pairing. Official guide https://learn.chatgpt.com/docs/remote-connections describes desktop SSH via concrete host alias, working SSH authentication, remote codex PATH/auth and Settings > Connections > SSH. Device pairing is a separate route with app/workspace availability requirements. Same-store thread visibility is expected but needs a direct desktop receipt.

Hourly quota line: supported account/rateLimits/read at 2026-09-16T15:12:54.221Z returned 81 percent used / 19 percent remaining for the 10080-minute Codex weekly window; reset 2026-09-19T15:05:28Z. Three reset credits available; none consumed. Separate Spark/bengalfox windows remain 0 percent used. The living decides reset timing.

## Effective order 6 ownership and wrapper handoff

Read order 6 from exact source 7bc84d49. Primary retains design, prototypes/proofs, successor packages, Cloud Nexus capability, chime bot and terminal-wrapper source. Secondary owns relay/Prosody/DNS activation and production tests under its existing gates. Previous main promotions and delivered activation orders remain valid; no repeated deployment was requested. The sample relay pins in order 6 are stale; current exact main pins were supplied again.

Terminal wrappers are published at primary proposal/cf7879-codex-layer-access 0b4f39317ee60706470e8dbc7ff69c2562c36c58, tools/codex-layer-resume/. Worker-owned 8/8 mock receipt stands. Sent secondary the exact source package, registry-selection contract, refresh-bound index and remaining terminal/theme/actual-resume check. No installation or fresh themed terminal is claimed. Its snapshot remains cf7879 as current until the newly launched successor supplies readiness and handoff completes. Desktop reachability is a separate receipt.

The pre-approved branches-file rule is accepted; flows/cf7879/branches.md already exists and says a branch is a bookmark. Efa157 is updating authored skill lines; root does not duplicate that work. Broader pending branch-protocol wording is separate from this pre-approved addition.
Secondary transport returned active turn 01a0aac2-37a3-7c22-8c6a-76b230685e62, exit 0. Exact body SHA256 792fab011043165a1dcd6dceeba77fd9b813d8b330dc8dad8a97702ea3e70db2, 1737 bytes; native user-record timestamps ["2026-09-16T15:20:37.694Z"]. This is delivery, not execution proof.

Quota update from supported account/rateLimits/read at 2026-09-16T15:20:02.002Z: Codex weekly window 82 percent used, **18 percent remaining**, 10080 minutes, reset 2026-09-19T15:05:28Z. Three reset credits available; none consumed. Pace hold remains superseded and the living owns reset timing.

## Order 7 — full proposal and exact Opus witness

# Order 7: Sema contracts and low-power thinking

Proposal only, 2026-09-16. Source: efa157 order 7 at `76247035`, and its
`vision/sema.md` and `vision/modelRoles.md`, read whole.

## Sema: yes, with a precise boundary

Use `sema-message` for Message's durable record contract, analogous to
`signal-message` for its wire contract. Author `sema.ethos`; generate record
types, stable family/schema identities and sealed kind implementations in that
crate. Message's database process consumes those types. A separate Git
repository is a packaging choice, not the mechanism enforcing Rust isolation.

Rust's orphan rules alone do not prevent another crate implementing your trait
for its own local type. A private supertrait supplies that additional restriction:

```rust
mod private {
    pub trait Sealed {}
}
pub trait MessageRecordKind: private::Sealed {
    const FAMILY_ID: u32;
    const LAYOUT_VERSION: u32;
}
pub struct LedgerRecord { /* generated fields */ }
impl private::Sealed for LedgerRecord {}
impl MessageRecordKind for LedgerRecord {
    const FAMILY_ID: u32 = 1;
    const LAYOUT_VERSION: u32 = 4;
}
```

Only the defining crate supplies these implementations. An external database
process type cannot implement the sealed trait either: it should use a generic
store accepting `T: MessageRecordKind`, or a generated process wrapper owned by
the contract crate. Keep runtime backend operations separate. Sealing is an
API/build-time restriction, not process isolation, credential protection or a
barrier to someone modifying and recompiling the crate.

### Proposed Ethos shape

The following is a design sketch using the existing `Sema.1` envelope and a
typed migrations record family. It is not a parser/generator pass or adopted
grammar. Imported record definitions and sealing code generation still need
implementation. `spirit-ethos/sema.ethos` already demonstrates ordinary records
and a migrations family; executable migration semantics are additional work.

```text
Sema.1
[interface.{LedgerRecord InboxRecord ThreadRecord AgentRegistryEntry RelayRecord}]
{
  [
    RecordIdentifier.Integer
    MigrationIdentifier.Integer
    SchemaVersion.Integer
    FamilyIdentifier.Integer
    LayoutVersion.Integer
    RowCount.Integer
    ContentDigest.String
    SourceSnapshot.{ContentDigest SchemaVersion}
    FamilyLayout.{FamilyIdentifier LayoutVersion}
    MigrationStep.[
      Preserve.SourceSnapshot
      DecodeLegacyRegistry
      DecodeLegacyLedger
      DecodeLegacyInbox
      DecodeLegacyThreads
      ValidateReferences
      AddRelayFamily
      VerifyCounts
      PublishVersion.SchemaVersion
    ]
    MigrationSteps.Vector<MigrationStep>
    MigrationPlan.{SchemaVersion SchemaVersion MigrationSteps}
    MigrationState.[Prepared Running Verified Committed Failed]
    MigrationRecord.{MigrationIdentifier MigrationPlan MigrationState RowCount ContentDigest}
  ]
  [
    ledger.{LedgerRecord RecordIdentifier}
    inbox.{InboxRecord RecordIdentifier}
    threads.{ThreadRecord RecordIdentifier}
    registry.{AgentRegistryEntry RecordIdentifier}
    relay.{RelayRecord RecordIdentifier}
    migrations.{MigrationRecord MigrationIdentifier}
  ]
}
```

Before code generation, give repeated source/target version fields distinct
named types and specify per-family key types from the existing store. Digest
representation should become fixed bytes when the contract supports it; do not
duplicate message text or logs in migration records. Sealing belongs to the
generated Rust projection; this sketch does not invent a working Ethos `sealed`
keyword. Migration steps enumerate reviewed algorithms, not arbitrary shell or
SQL strings executed from a database row.

### First migration: preserve the unreadable row

Witnessed source at Message `fe0d0456`: `tables.rs` sets store schema **5**,
family layouts **4**, and permits only **4 → 5** as additive. Its comments
explicitly prohibit re-stamping **3 → 4**: archived contract layouts changed.
The current code preserves the file before the additive version update.
“Deployed schema 3, one pending row unreadable” is efa157's operational report,
not a new inspection of production by this flow.

1. Secondary preserves a consistent source store and identifies its actual
   schema and producer revision. Keep the original unreadable bytes.
2. A version-pinned legacy decoder reads schema 3 using its old types. Convert
   to schema 4 records in a separate destination; do not read v3 bytes with v4
   types or change only the schema stamp.
3. Validate family counts, identities, inbox/ledger/thread references and the
   pending delivery's source key/state. A row that still cannot be decoded
   blocks successful promotion; report its identity and digest without dropping
   it or claiming delivery.
4. Add the v5 relay family. Persist step/progress receipts so interruption can
   resume or restart idempotently. A migration ID identifies the exact plan and
   source snapshot, preventing accidental replay against a different store.
5. Verify the complete destination, then secondary performs atomic activation
   under its gates. Keep the prior store/generation for rollback; never point
   an old binary at an incompatible new store. Rollback after new writes needs
   an explicit replay/reconciliation plan.

Required proof before activation: real legacy fixtures, semantic conversion of
the pending row, crash/restart at each publication boundary, duplicate-run
idempotence, reference/count invariants, refusal of unknown versions and an
external-crate compile-fail test for sealed kinds. These are proposed tests,
not tests run in this design-only turn. The migration journal can be append-only;
that does not mean the existing redb file is physically append-only or that
bounded message retention has been removed.

## Model witness

Installed Claude Code: **2.1.263**. CLI help documents aliases `fable`, `opus`,
`sonnet`, and full model names. The `agents` help exposes `--model` but provides
no enum. The peer-reported Agent-tool list `opus|sonnet|haiku|fable` has not been
independently verified from that tool's schema here. A CLI selector is not a
proof of backend availability, and an alias can resolve differently over time.

Root ran one bounded, tools-disabled, nonpersistent call from `/tmp`:

```text
claude -p --model claude-opus-4-6 --tools ""
  --system-prompt "Reply with exactly OK. Do not use tools."
  --no-session-persistence --output-format json -- "Reply OK."
```

Structured subprocess arguments, detached stdin, 45-second deadline. Exit **0**,
result **OK**, `subtype: success`, `is_error: false`; `modelUsage` reported
`claude-opus-4-6`, `canonicalModel: claude-opus-4-6`, first-party provider,
1,906 input tokens and 4 output tokens. This proves a real call with the exact
Opus 4.6 ID on this installation/account. It does not prove Agent-tool subflow
dispatch, Opus 4.7/5 availability, or a comparison with Fable. No automatic model
substitution or benchmark claim.

## Low-power dispatch: small typed request, mechanical execution

Propose `LowPowerThinking` as an explicit request with a bounded model enum
(initial exact member `Opus46` → `claude-opus-4-6`), job/source-turn IDs,
context-snapshot digest, deadline and output limit. “Low power” describes the
role; it is not a demonstrated cost/performance property of Opus.

The main emits the datom header and a delimited task payload. A trusted harness
event marks that assistant output as an intentional dispatch. Flow reads the
event, resolves the exact model and source context, and starts one bounded job.
Do not scan arbitrary tool output, quoted transcript text or incoming peer
messages for a marker and execute it. Deduplicate by source Flow, turn and
dispatch block; repeated output must not launch repeated jobs.

Conceptual contract:

```text
ThinkingModel.[Opus46]
ThinkingRole.[LowPowerThinking]
ThinkingRequest.{JobIdentifier SourceTurnIdentifier ThinkingRole ThinkingModel ContextDigest Deadline OutputLimit}
ThinkingResult.[Completed.ThinkingAnswer Failed.ThinkingFailure Expired Cancelled]
```

The delimited payload remains verbatim task text, associated with the header
by digest and byte length. The amplified lane log is a frozen, provenance-marked
context snapshot; arbitrary log text does not grant new permissions. Set the
job's tools/permissions explicitly, default read-only for this thinking role.
Begin with one outstanding job per main and no automatic fallback to a larger
model. Failure is a typed result, not a reason to relaunch indefinitely.

Flow owns identity, membership and idleness. Message transports the request and
result and parks the result while the main is busy. When the main can receive,
resume it with the result reference and receipt; do not paste into a busy PTY.
Keep request, worker-completion, transport and recipient-turn receipts distinct.
The first proof should dispatch one real bounded Opus46 job and witness its
result in the main transcript, with a duplicate event test. No hook, timer,
dispatch parser or new MCP surface is installed by this proposal.


## Item 38 receipt recovered; fixture-library proposal — 2026-09-16

The full proposal follows; standalone source: `flows/cf7879/reports/testing-fixture-library-proposal.md`. This records the historical audit and proposes the library/check; it does not claim either implemented.

# Real payload fixtures and the source-check inventory

2026-09-16 proposal. Read efa157's `vision/testing.md` and
`vision/specificationVersionControl.md` whole. No test suite is rewritten or
new library/Nix check claimed implemented by this report.

## Item 38 status

**The bounded read-only audit was delivered; remediation is not complete.**
Its owner was predecessor subflow `/root/records_coordination`, thread
`01a0a61c-a4be-7c90-bfe4-047318baea9d`. Root now read its final report in the
predecessor transcript at 2026-09-15T21:56:12.890Z, record
`amsg_01a0a712-0bda-7832-a32d-af85a0f4b21e`, ordinal 5614 (physical line 5615):
`/home/li/.codex/sessions/2026/09/15/rollout-2026-09-15T17-50-48-01a0a5c3-82a5-79f3-a61a-e365f4fea54f.jsonl`.
The report explicitly says “read-only; no tests run, no edits”. No standalone
item 38 report file or implementation commit was located. Its source paths and
assertion locations are recorded, but no pinned repository revision inventory
was supplied. The inherited “running/awaiting owners” label is therefore stale.

That audit covered Primary tool mocks/dry runs, Orchestrate real isolated
socket tests, Message process/fixture tests, Lojix fake Nix/SSH and ignored live
evaluation, and Datom/Ethos/Nexus/Persona local contracts. It found meaningful
behavioral coverage alongside source scans, and false-confidence risks when
fixture acceptance was described as delivery, readiness or deployment. It did
not establish real Claude native delivery, actual harness launch, provider model
turns, production restart/cgroup behavior, or default live Lojix evaluation.
These are the historical auditor's bounded findings, not fresh execution by this
flow. Later Fable audits and the following source sample are separate evidence.

Root made a fresh, limited source inspection of Home at `4adefe87`:

| Check | Actual assertion | Classification / replacement |
|---|---|---|
| `checks/no-easyeffects/default.nix` | Reads max-profile source, asserts substring `easyeffects` absent, then touches output | Source change detector only. Evaluate the composed profile and assert the package/service is absent. |
| `checks/nix-profile-compatibility/default.nix` | Two substring checks on base-module source, followed by running the real helper against a disposable filesystem | Mixed. Replace substring checks with evaluated activation ordering; retain real link, idempotence and preservation assertions. |
| `checks/ghostty-primary-selection/default.nix` | Source substring for dconf plus evaluated terminal-command comparison | Mixed. Evaluate the dconf option directly; command comparison proves configured command, not GUI clipboard behavior. |

These three inspected files are new narrow evidence, not an exhaustive audit.
The initial search also matched legitimate fixture reads and package metadata:
`readFile` alone does not make a test fake. Classify the read and the assertion
it feeds. A source guard can remain an explicitly labelled lint; it cannot stand
in for behavioral evidence or make a deployed feature “tested”.

## Fixture library shape

Start as a small shared test-support crate, with no runtime dependency from
production. Each contract consumer keeps reviewed, realistic payload files.
Use the production datom codec and generated contract types, not another
hand-written parser or string-matching substitute.

```text
tests/
  fixtures/
    notify/
      valid-build-result/input.datom
      valid-build-result/expected.datom
      missing-recipient/input.datom
      missing-recipient/expected.datom
    relay/
      ordinary-claude-turn/transcript.jsonl
      ordinary-claude-turn/request.datom
      ordinary-claude-turn/expected.datom
    migration/
      v3-pending-delivery/store.sema
      v3-pending-delivery/manifest.datom
      v3-pending-delivery/expected-records.datom
  cases.datom
```

`cases.datom` names case ID, contract/version, input paths, typed expected
outcome and provenance. Keep source hashes for opaque legacy database fixtures;
record which old binary/schema produced them. Payloads should be realistic
sanitized examples, contain no credentials, and exercise actual failure causes.
Do not generate expected answers from the implementation during the same test.

Illustrative test-support API (proposal, not an existing exported API):

```rust
let case = fixtures.case::<NotifyCase>("notify/valid-build-result")?;
let input: NotifyEnvelope = case.decode_input(&production_codec)?;
let actual: NotifyValidationOutcome = subject.validate(input);
case.assert_outcome(actual)?;
```

For a process-boundary case, pass `input.datom` to the built CLI, parse its
response into the generated outcome enum, and compare typed fields. Assert exit
status separately. For malformed datom, pass bytes directly: decoding in the
fixture loader must not prevent the subject from seeing its invalid input.

The library should provide only:

- case discovery and safe fixture paths;
- byte loading and typed decoding through the real codec;
- a disposable HOME/store/socket directory and child-process cleanup;
- bounded process execution with separate stdout, stderr and exit status;
- typed outcomes, stable field diffs and explicit normalization of volatile
  timestamps/IDs, never a blanket “ignore errors” rule.

Domain assertions stay readable in the test: a queued record is present exactly
once; a failed migration leaves the original readable; tampering is rejected;
reconnection alone is not delivery. The helper must not hide these behind a
generic `assert_success` which checks only that a program exited.

Each record kind needs at least a meaningful accepted example, a rejected
example, and the relevant boundary or historical regression. Tests that need
services should start actual disposable services; injected adapters have a
clear seam and a limited claim. Do not call an environment-echo fixture proof
that a remote recipient received a message.

## Nix check: inventory source-reading assertions

Propose `checks.<system>.test-source-inventory`, producing a machine-readable
inventory and a short table for review. Its success means the inventory policy
is satisfied, not that product behavior is correct.

Inventory rows contain repository/revision, test and assertion location, read
target, classification, owner, reason, and replacement behavioral test. Enumerate
every test from the repository's test/build manifests, then inspect its source
reads: Rust `include_str!`/file reads, JavaScript/Python file APIs, Nix
`builtins.readFile`, and shell grep/rg/cat with source inputs. Track aliases and
helper calls where supported. Unknown/dynamic readers are unresolved rows,
never silently treated as behavioral coverage.

Classification is per assertion:

```text
FixtureInput | GeneratedArtifactInspection | SourceChangeDetector | Unresolved
```

Candidate detection may begin with lexical scans, followed by review. That is
not a proof of “every possible source read”; dynamic paths, generated tests and
subprocesses require additional tracing or explicit declarations. The check
reports its scanned roots, excluded files and unresolved cases. It fails when
tests are outside the inventory or new findings are unclassified. Existing
labelled change detectors remain visible until replaced; an allowlist must not
erase them from the report.

Nix wiring sketch:

```nix
test-source-inventory = pkgs.runCommand "test-source-inventory" {
  nativeBuildInputs = [ pkgs.python3 ];
} ''
  mkdir -p "$out"
  python ${./tools/test_source_inventory.py} \
    --root ${self} --manifest ${./tests/source-reads.datom} \
    --json "$out/inventory.json" --markdown "$out/report.md" \
    --fail-unclassified
'';
```

The scanner and manifest do not exist yet. Test the scanner itself against
dedicated fixture repositories: direct and helper-mediated source-string
checks, legitimate payload reads, generated-output tests, and unresolved dynamic
paths. Expected classifications are reviewed data files, not snapshots derived
from scanner output in the same run. Add runtime read tracing later for the
languages/processes that a static pass cannot cover.

## Typed specification upgrades feed migration tests

Extend order 7's proposal with stable object/field IDs and typed specification
operations: add record, add field with a typed default, rename without changing
identity, change field type with a named conversion, retire field, change key,
and change layout. Each operation carries source/target schema identities and
preconditions. The compiler produces a reviewed structural diff, generated Rust
and a migration plan; recompilation is necessary but not sufficient proof.

Layout/size changes can require data transformation even if a field name stays
the same. Key changes need collision handling. Narrowing conversions must reject
out-of-range rows explicitly. A source rename should not accidentally change
durable identity. Unsupported operations stop plan generation.

Use real versioned payload/store fixtures to execute these operations, decode
with the old schema, migrate, and assert typed new records, reference integrity,
pending-message identity, interruption recovery and duplicate-run behavior.
Keep the original fixture and migration receipts. No test should verify an
upgrade solely by finding its new type name or version number in source code.


Successor crossover: d9961c supplied its independent clone and lane. Root read `flows/d9961c/log.md` at the supplied clone and verified published `flow/d9961c` exists. The supplied a41595c8 is already followed by remote 9010121c116d4665e2e6d38461fc59be289dc6b1 at readback; this is not an exact-tip match to the older pointer. Claude idle delivery and laptop visibility remain unwitnessed. No recycle signal is issued in this report.


## Successor readiness receipt and current titles — 2026-09-16T15:32Z

Received d9961c's readiness pointer: native thread
`01a0aacb-ac84-71a1-88a0-05ed9961ca9d`, independent non-colocated JJ clone
`/git/github.com/LiGoldragon/primary/codex-successor-cf7879-bootstrap-a1acf612-da24-4d54-a05c-12b4a6028d9e`,
`flows/d9961c/log.md` and `branches.md`, published pointer
`a41595c8e15621fc027e9a524d85f76dd34b3cef` on `flow/d9961c`.
Root previously read the lane log; remote readback had already advanced to
`9010121c116d4665e2e6d38461fc59be289dc6b1`. The supplied pointer is historical,
not a new exact-tip witness.

Direct supported app-server `thread/read` at 2026-09-16T15:32:20.992Z returned
successor name **Primary Codex successor of cf7879 · readiness pending** and
status idle. The predecessor read at 15:32:20.994Z returned
**Primary Codex cf7879 · paired Claude efa157**, status active.
These are native thread names; no laptop UI visibility is inferred.

Successor reports twelve complete skill bodies including Spirit, six Intent,
thirteen top-level Vision and paired frozen sources, with frozen orders read;
no native skill-load or child-inheritance proof is asserted. Its direction is
Cloud Nexus DNS, then accounts/chime, with secondary activation. Claude efa157
idle-gated delivery remains pending. No refresh, reset, repository rename or MCP
installation follows from this receipt.

cf7879 remains the primary Codex until an explicit recorded handoff/recycle.
This entry acknowledges readiness only; it does not transfer authority. The
latest testing proposal and recovered item 38 receipt are at `c4752c454741`,
`flows/cf7879/reports/testing-fixture-library-proposal.md`, also appended whole
to the paired report.


## Order 8 — Claude successor v6 review packet

All six fixes from order 8 are applied in
`flows/cf7879/handoff/successors-v6-reviewed/`. V5 remains the launch evidence
for the already-running d9961c; v6 is only the unlaunched Claude successor.

The base header states the direct-request Authority rule and identifies the
old stock-base log statement as historical. It names d9961c and its exact
01a0aacb thread, while preserving cf7879's authority until recorded handoff.
It supplies EnterWorktree isolation, directory/sandbox restrictions, supported
orders-file routing for classifier refusals, and one send per subflow. Nexus is
now a complete skill block. The current efa157 log, vision and eight named
reports (including orders) are frozen. The first prompt explicitly gives
flow-id, depth-one memory, pairing, first Cloud Nexus/XMPP direction, decisions,
all three reporting routes, and efa157's recycle condition. The historical ten
turns/decisions now carry an archival banner in their own source file.

Validation: assemble.py succeeded; 68 source-file byte counts and SHA256 values
verified; each included body present byte-exact; all 13 Claude skill bodies
extracted and compared both to frozen files and their named Curriculum sources.
Current efa157 log and eight reports compared byte-exact to the live lane at
validation time. Claude base 359481 bytes; first prompt 2112 bytes. Launcher
dry-run succeeded with modeled envelope plus 64KiB reserve 73460 bytes, below
262144; each argv string is below 100000 bytes. Actual daemon record remains
unwitnessed. These are package/argument checks, not launch/runtime tests.

No Claude launch performed. Await efa157's launch word on this revised packet.
After launch, roster, scope, remote control and a real prompt user turn still
require separate receipts. No new native skill load or child inheritance is
claimed by this assembly.


## Order 9 first wake — actual recipient witness

The corrected package notification reached efa157 through prompt-relay after
the earlier idle refusal. Root verified native user record
`39c4c849-88a3-4e9a-ab46-6aad0c42ac99` at 2026-09-16T16:04:58.916Z; source
SHA256 `3eed244dc5784b1a1bc7b678a0b98c53ddbfbcd00d996f3cd1a9408850be955b`.
Receipt: efa157 / prompt-relay Claude PTY / TranscriptWitnessed. The message
names corrected v6 at 07d23d8b2ad8 and its green dry-run; no launch performed.
This wake was executed by root, not the unfinished heartbeat.

The first heartbeat scaffold 07aa3686 on proposal/cf7879-core-heartbeat is
not accepted as a functioning order 9 proof. Root review found any-provider
quota selection, recommended-but-not-effective cadence, missing peer adapters
and dedup, inline fixture payloads and insufficient model-tool isolation. The
worker is correcting these; no timer is activated. Full current working report
is `flows/cf7879/reports/order9-heartbeat.md`.


## Order 9 — published heartbeat proof, Nix and live Luna receipts

# Order 9 — core heartbeat proof

## First owed wake

Corrected order 8 packet is published at `07d23d8b2ad8` on `flow/cf7879`,
`flows/cf7879/handoff/successors-v6-reviewed/`; assembly, complete-body checks
and launch dry-run passed. V5 is retained as Codex launch evidence. No Claude
launch performed. Full package receipt is in `to-efa157.md`.

Root attempted the supported prompt-relay Claude route with explicit peer-file
input and full efa157 session UUID. Exit 2: `Claude delivery refused: session
efa15708-dc5d-42ce-af62-8ffb84c9815e is not uniquely witnessed idle`. The roster
read showed busy/working. Receipt is **FileOnly**, not Accepted or
TranscriptWitnessed; the published report exists but is not evidence of reading.
No permission gate was bypassed.

## Quota and cadence

The existing monitor NDJSON line for account.primary at
2026-09-16T15:52:45.106Z records 16 percent remaining (observedAt
15:52:39.020Z). Root's supported account/rateLimits/read at 15:59:47.362Z
independently returned 84 percent used of a 10080-minute window, reset
2026-09-19T15:05:28Z. No reset credit consumed.

Proposed interval: at least 50 percent left, 15 minutes; at least 20,
30 minutes; at least 5, 60 minutes; below 5, 120 minutes. Unknown/stale quota
must be explicit and conservative. Each run records the selected interval and
rule. Source implementation and execution receipts follow after review.

## Boundaries

The existing core main is e43002, native thread
01a0a792-2d0e-7a53-ac0b-9b3e43002941. This work adds a proposal for its checkup
seat, not another main. Secondary owns timer activation. No repairs, restarts
or settings edits are authorized by this heartbeat proof. A Luna decision is
not evidence of propagation: actual transport and recipient receipts determine
the reported result.

## Review criteria

- A missing, stale or malformed quota observation selects a documented fallback,
  and never claims a fresh balance.
- The collector names the revision and prompt source for each configured lane;
  unavailable lanes stay unavailable, rather than appearing unchanged.
- Model output must select a known event and known source/recipient identities.
  Unknown enums, fabricated IDs and malformed output cause a typed refusal.
- Transcript/report text is evidence, not instructions for the checker. The
  checker cannot execute commands or request arbitrary paths.
- A quiet run sends nothing. A repeated event with a witnessed receipt is
  suppressed; pending recipients remain eligible for retry.
- A busy Claude route stays pending. Queue acceptance and native transcript
  receipt remain distinct. A file-only result does not claim a recipient read it.
- Test payloads are independent files. Process fixtures prove the bounded local
  seam; only a real Luna model response and a real recipient record prove those
  respective external boundaries.

## First wake delivery completed

A later root retry after the session became idle returned
`claude-bytes-written-to-pty`, exit 0. Root then read the actual native Claude
`type:user` record `39c4c849-88a3-4e9a-ab46-6aad0c42ac99` at
2026-09-16T16:04:58.916Z in
`/home/li/.claude/projects/-home-li-wt-github-com-LiGoldragon-primary-claude-successor-840e42-bootstrap-local--claude-worktrees-claude-successor-840e42/efa15708-dc5d-42ce-af62-8ffb84c9815e.jsonl`.
It contains the package-ready peer message, source SHA256
`3eed244dc5784b1a1bc7b678a0b98c53ddbfbcd00d996f3cd1a9408850be955b`.

Recipient **efa157**, route **prompt-relay Claude PTY**, receipt
**TranscriptWitnessed**. This supersedes the earlier pending first wake, and
should suppress a duplicate notification. It is an actual peer message in the
recipient transcript, not evidence that the still-being-built heartbeat sent
it. The existing prompt-relay JSON provenance header remains; replacing it with
a datom head is separate order 10 work, not claimed done here.

## Published proof and execution receipts

Producer: primary `proposal/cf7879-core-heartbeat`, exact revision
`99285db2784c681928016736f64752e57caa934a`. Workspace
`/home/li/wt/github.com/LiGoldragon/primary/heartbeat-cf7879`. The inherited
core-checkup ancestry is not an integration candidate: extract only the heartbeat
tool, adapter/base, fixtures/tests, documentation, example configuration, timer
source and heartbeat-fixtures flake entry. No main or installed unit changed.

What was put together: a five-minute timer poll with persisted quota-based
15/30/60/120-minute gating before model calls; read-only bookmark/report/user
record collection; one restricted ephemeral gpt-5.6-luna call with custom base;
validation of major enum, candidate ID and recipient allowlist; code-built
Codex queue / idle-only Claude prompt-relay argv; per-recipient acceptance state,
transcript witness promotion and retry of still-pending recipients; append-only
report file and atomic state with flock. Typed prototype output is validated
JSON Heartbeat/v1, not yet a generated Ethos/datom contract. Order 10's datom
header replacement remains separate and is not claimed complete.

The private Luna app-server runs in a temporary directory. Empty environments,
dynamic tools and capability roots plus explicit disabled execution/web/apps/
plugins/agent/image/MCP settings remove action surfaces per inspected harness
source. The program discovers only MCP server names internally to disable them;
no credentials enter the model snapshot. The real runs observed only user,
reasoning and assistant items. This is source construction plus bounded run
evidence, not a claim that a read-only sandbox alone hides credentials.

Validation: root ran 8 local tests; the worker ran the exact-revision Nix check
on Prometheus using --max-jobs 0 --no-link: 8 passed, 0 failed. Derivation
`/nix/store/pmsw8r6xa1mf9nn2vmqjifdx8g8mpvff-primary-heartbeat-fixtures.drv`,
output `/nix/store/9lrldwqrxl3xgzsgkq31hrs2yi1gsdn7-primary-heartbeat-fixtures`.
The tests cover real child fixture payload handling, actual transcript record
shapes, wrong-window quota refusal, cadence suppression, per-recipient retries,
unknown decision refusal and restricted-boundary refusal before a model turn.
They do not prove production timer activation.

The first actual Luna attempt accepted thread restrictions but failed because
ephemeral threads reject includeTurns. The adapter now consumes native
item/completed and turn/completed notifications; the subsequent real fixture
call returned successor_ready. Root then ran two real curated cluster snapshots,
the final one with sends enabled. It returned none: the package wake was already
transcript-witnessed, so no duplicate message was sent. This is a real Luna
classification and no-send witness, not a new automatic peer-delivery witness.
The first required package wake has the separate root-executed receipt above.

The final collector observed primary Claude, cf7879 and d9961c bookmark tips and
all six last user records. Configured secondary/core bookmark reads were
unavailable; reports/transcripts remained available. Secondary must supply the
actual active revision pointers before treating this as complete cluster tip
coverage. Claude's next successor is added after actual identity/launch receipt.
Other limitations: local refs are not auto-fetched; long records may exceed the
bounded transcript tail; report/state retention needs activation policy; a crash
in the transport-send/receipt-commit gap remains ambiguous, so exactly-once
propagation is not claimed. Message receiptReport names the final report path;
only prior receipts can honestly be embedded before a send finishes.

Final actual tick receipt:

```json
{
  "directory": "/tmp/heartbeat-cluster-cf7879-1dnJ6T",
  "lanes": [
    {
      "flow": "efa157",
      "status": "observed"
    },
    {
      "flow": "cf7879",
      "status": "observed"
    },
    {
      "flow": "d9961c",
      "status": "observed"
    },
    {
      "flow": "57a7aa",
      "status": "unavailable"
    },
    {
      "flow": "348e7b",
      "status": "unavailable"
    },
    {
      "flow": "e43002",
      "status": "unavailable"
    }
  ],
  "candidates": [
    {
      "id": "e424ae794b8fc0871eca35d73ecb8c6a95af932f4fefb1bd8fda4ce69193a7d1",
      "kind": "lane_tip",
      "flow": "efa157"
    },
    {
      "id": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "kind": "user_turn",
      "flow": "efa157"
    },
    {
      "id": "03f959c87082f86f2af28c455cd14f6343c4343c04ea00d28d94e14fbe025a94",
      "kind": "lane_tip",
      "flow": "cf7879"
    },
    {
      "id": "adfb0505aeb25194da0787b4b0eec03fc92f6d9f85fb367f76425bb169caf4a1",
      "kind": "user_turn",
      "flow": "cf7879"
    },
    {
      "id": "36b6d2d9856f5302198807fa3e952fabfb4d41ac09d1ddbf252495ebb083e450",
      "kind": "lane_tip",
      "flow": "d9961c"
    },
    {
      "id": "e34731a20604c1f42ffb59563dd4bfbe683e4f7f4117fe420d689c2aee91d614",
      "kind": "user_turn",
      "flow": "d9961c"
    },
    {
      "id": "1e855e04c2372786d185a7f577804f5677006affcedcc0a9de36a9516a303bdd",
      "kind": "user_turn",
      "flow": "57a7aa"
    },
    {
      "id": "4fdd83a34cfbc9f9203a43c4d9140c6c96c334cdc43151148090d4a46e646025",
      "kind": "user_turn",
      "flow": "348e7b"
    },
    {
      "id": "ab96056a6c1baa4911bb17a225479a0dbc65fbf9c6d3425b92bb2282906117eb",
      "kind": "user_turn",
      "flow": "e43002"
    }
  ],
  "result": {
    "schema": "heartbeat/v1",
    "at": "2026-09-16T16:19:46.651Z",
    "kind": "heartbeat",
    "interval": {
      "minutes": 60,
      "reason": "quota_observed"
    },
    "quota": {
      "remainingPercent": 16,
      "observedAt": "2026-09-16T15:52:39.020Z"
    },
    "decision": {
      "major": "none",
      "sourceId": null,
      "summary": "No unpropagated major event is supported. The corrected v6 package readiness and dry-run result were already transcript-witnessed by efa157; successor readiness was acknowledged by cf7879. Other evidence describes pending, gated, or already reported work without a distinct new propagation target.",
      "recipients": [],
      "witness": {
        "stage": "completed",
        "boundaryAccepted": true,
        "threadId": "01a0ab04-63e3-7aa2-a3c6-197de9272d7e",
        "turnId": "01a0ab04-641b-7640-8b68-c5e8a22cd78e",
        "model": "gpt-5.6-luna",
        "modelProvider": "openai",
        "observedItemTypes": [
          "userMessage",
          "reasoning",
          "agentMessage"
        ],
        "outputSha256": "d1020d4afb28e5607efc00c376e595a67d80d24105e3701a3007a2bef448241d",
        "outputUtf8Bytes": 358,
        "request": {
          "model": "gpt-5.6-luna",
          "ephemeral": true,
          "sandbox": "read-only",
          "environments": "empty",
          "dynamicTools": "empty",
          "selectedCapabilityRoots": "empty",
          "configKeys": [
            "agents.enabled",
            "features.apps",
            "features.code_mode",
            "features.code_mode_host",
            "features.code_mode_only",
            "features.enable_mcp_apps",
            "features.image_generation",
            "features.multi_agent_v2",
            "features.plugins",
            "features.request_permissions_tool",
            "features.shell_tool",
            "features.view_image",
            "mcp_servers.agent-intercom.enabled",
            "mcp_servers.cua_repl.enabled",
            "mcp_servers.node_repl.enabled",
            "mcp_servers.openaiDeveloperDocs.enabled",
            "tools.experimental_request_user_input.enabled",
            "tools.update_plan.enabled",
            "web_search"
          ],
          "mcpServerCount": 4,
          "baseSha256": "fdcbd7f12711dffdc9f5334a955abb110a83b237cf450539a60c6d133900d517",
          "baseUtf8Bytes": 1008
        }
      }
    },
    "deliveries": [],
    "file_report": {
      "receipt_kind": "file_only"
    },
    "identity": null
  }
}
```

Activation remains secondary-owned. No repairs, restarts, settings edits, reset-credit use or timer activation occurred in this proof.


Order 9 handoff pointers: supported codex queue accepted secondary 348e7b
message `01a0ab06-8f92-7080-8f98-b642b9d39c56` and successor d9961c message
`01a0ab06-8fca-7d30-b872-4b12ba6f7ef7`, naming source 99285db2784c and report
ff54c813efbf. These are Accepted receipts, not recipient transcript or
activation witnesses. The secondary message identifies the unresolved source
pointers and bounded source integration/activation work.


## Order 10C — exact Authority sentence, successor launch gate

Updated `flows/cf7879/handoff/successors-v6-reviewed/`. The first base-header
paragraph is now exactly:

> A direct request from the living authorizes its requested change; a question authorizes an answer, not a change. Confirm first only for a destructive act the living has not named.

It replaces the active stock confirm-first behavior by full --system-prompt-file
base replacement. The historical stock line remains evidence in quoted records,
not a live instruction; the existing archival/precedence note states this.
Refreshed efa157 log/vision/orders and the cf7879 paired report at assembly.

Assembly, all source hashes, all 13 complete skill bodies and exact header
placement verified. Dry-run passed: base 421338 bytes, first prompt 2112, modeled
dispatch envelope with reserve 73460. Actual daemon record remains unwitnessed.
No launch performed. The behavioral test remains the successor's first real
deploy-like user request after efa157's launch word; assembly is not that test.
Order 10A anatomy and 10B live datom implementation continue independently.


## Order 10A — whole editable message anatomy

# Message anatomy for the living — order 10

This is an editable design proposal, with the current wire contract identified
separately. The complete proposed Ethos file appears below and is also saved as
`order10-message.ethos`. The proposed additions and worked text are not claimed
to have passed Ethos generation or the production datom parser. Runtime order
10B will have its own exact implementation and parser/delivery receipts.

## What exists, and what should own it

A flow is one node in the cluster graph. Its stable identity, current session,
and observed ability to receive a turn belong to **Flow**. Message asks Flow for
that information, chooses a supported transport, and records delivery evidence.
Message must not create a second independently maintained flow-name registry.

| Existing thing | What it establishes | What it does not establish |
|---|---|---|
| `flow-id` | A session-derived alias and lane claim marker | A route, a live idle state, or authenticated authority from an arbitrary supplied alias |
| Orchestrate | Attribution and ownership of coordinated locks | Which harness session called Message, a cluster roster, or routing authority |
| Message agent registry | Agent identifiers, endpoint/resume/process-pin records | The Flow cluster's session/name/idleness registry |
| Item 35 Flow prototype | Reads `.flow-id` markers, validates unique identities, supports in-memory query/subscription and checked observation publishing | An activated IPC service, automatic route discovery, or process-authenticated callers |
| Current relay environment | Declared executor flow/session and supplied cluster membership; relay checks consistency | Proof that environment variables cannot be forged |

Root read the item 35 implementation at primary checkout
`cf7879-flow-idleness-poc`, revision `2139b80c4d4ec25708eb49150751399d24e59cc5`,
`tools/flow-idleness-registry.mjs`. It validates markers and rejects mismatched
harness/session identities when publishing observations. Its subscription is a
local callback set. The companion `flow-idleness.mjs` reads the last Codex turn
and refuses to equate completed turns with idle when the supplied operational
state is busy, approval-wait, or unknown. None of that is a deployed registry
receipt.

**Proposed one owner:** extend that Flow-owned source into a typed query service.
The Message CLI's `WhoAmI` and `Routes` commands delegate to it. During the
stopgap, a configured snapshot and self-declared caller are labelled `Declared`.
Later the host associates peer PID/start-time/session with its registered Flow;
only a witnessed association earns `ProcessSessionObserved` or `RegistryBound`.
A PID alone is insufficient because it can be reused. An alias is a name, not
an authentication token. This preserves the living's current goodwill model
without representing it as stronger authentication.

## The three identities in one delivery

1. **Caller:** the flow invoking the CLI now, such as cf7879.
2. **Source:** the flow/session whose transcript contains the original words,
   such as efa157. Relaying those words does not make cf7879 their author.
3. **Recipient:** the flow to which a route attempt is addressed.

For a peer-authored note, the source is explicitly a peer note. A temporary
peer-file path and content hash must never be dressed up as a human transcript
turn. For a human transcript relay, locate the original bytes, check the source
record and hash, and preserve those words. The Context is an interpretation
beside the words, not a replacement for them or a claim of human authorship.

## Current ClusterMessage and Context

Message main `fe0d04561051da85292a058ab156e286b7494aa4` selects signal-message
`a9708f3384af18129cb1c983ffed850c4d631e46` in Cargo.lock. This selected dependency,
not whichever branch a local signal-message checkout happens to show, governs
its current relay contract. Root independently observed remote signal-message
main at `65d6e2e2fafebaa246557b61ca786e3f382a1bb4`; its contents were not inspected
for this report, so no assertion that current upstream main lacks the contract
is made.

The selected relay shape is:

```ethos
ClusterTarget.[Primary Secondary Core]
ClusterMember.{FlowIdentifier SessionIdentifier}
ClusterMembers.Vector<ClusterMember>
Context.{FlowIdentifier SourceTurnIdentifier TranscriptPath PromptSha256 WhatLivingSaid ContextAbout ContextAnswered ContextCorrected ContextUncertainties}
ClusterRelay.{FlowIdentifier SessionIdentifier TranscriptPath PromptFirstSixWords PromptLastSixWords PromptSha256 Context TimestampNanos ClusterTarget ClusterMembers}
ClusterMessage.[Relay.ClusterRelay]
```

The identifier names currently wrap/alias String in Ethos. Their names express
intent; they do not by themselves prove UUID/hash grammar or process binding.
Those validations must be implemented and tested. Item 32's stronger identifier
proposal is not silently adopted here.

Current `relay` creates the header with the actual datom/protos codec and appends
the unchanged body. Context is structurally present. Without a context-machine
receipt, the current code fills explicit `unreviewed`/`unavailable` fields and
retains the source words; this is not an inferred analysis. A supplied context
receipt is checked against source identity/hash/words. Current ordinary
`message` parses `signal_message::Query`, not `ClusterMessage`, which is the
concrete CLI gap order 10B must close.

## Reading the proposed types

- `CallerIdentity` keeps a declared identity distinct from a checked binding.
- `FlowNode` joins flow, session, harness, role, idleness evidence and routes.
- `RouteListing` is one observed registry revision. `ValidUntil` is a freshness
  deadline, not a prediction that a session stays idle. The PTY gate still checks
  at delivery time. Approval-wait never becomes idle by timeout.
- `DeliveryRequest` keeps the caller outside the source-bearing message.
- `ClusterMessage.Peer` is an additive proposal so peer notes cannot masquerade
  as human `Relay` records. It does not change the existing Relay field order.
- `ReceiptKind` distinguishes acceptance, observed transcript content, durable
  parking and file-only reporting. `Pending` explains why no delivery exists.

A recipient transcript containing the exact datom is the acceptance test for
order 10B. Queue acceptance is useful but weaker. `FileOnly` says that a report
was written; it does not say anyone read it. `Parked` requires a real persisted
outbox entry; an in-memory intention to send is not parked.

## Complete proposed Ethos

```ethos
Signal
[]
[ Routes.RouteQuery WhoAmI.IdentityProbe Deliver.DeliveryRequest DeliveryStatus.DeliveryStatusQuery ]
[ RoutesListed.RouteListing IdentityResolved.CallerIdentity DeliveryRecorded.DeliveryReport Refused.RouteFailure ]
[
  FlowIdentifier.String
  SessionIdentifier.String
  SourceTurnIdentifier.String
  SourceEventIdentifier.String
  TranscriptPath.String
  PromptFirstSixWords.String
  PromptLastSixWords.String
  PromptSha256.String
  TimestampNanos.Integer
  WhatLivingSaid.String
  ContextAbout.String
  ContextAnswered.String
  ContextCorrected.String
  ContextUncertainties.Vector<String>
  ClusterTarget.[Primary Secondary Core]
  ClusterMember.{FlowIdentifier SessionIdentifier}
  ClusterMembers.Vector<ClusterMember>
  Context.{FlowIdentifier SourceTurnIdentifier TranscriptPath PromptSha256 WhatLivingSaid ContextAbout ContextAnswered ContextCorrected ContextUncertainties}
  ClusterRelay.{FlowIdentifier SessionIdentifier TranscriptPath PromptFirstSixWords PromptLastSixWords PromptSha256 Context TimestampNanos ClusterTarget ClusterMembers}

  HarnessKind.[Codex Claude]
  IdentityEvidence.[Declared ProcessSessionObserved RegistryBound]
  CallerIdentity.{FlowIdentifier SessionIdentifier HarnessKind IdentityEvidence}
  PeerBody.String
  PeerSourcePath.String
  PeerSha256.String
  PeerProvenance.{PeerSourcePath PeerSha256}
  PeerMessage.{SourceEventIdentifier CallerIdentity PeerProvenance PeerBody}
  ClusterMessage.[Relay.ClusterRelay Peer.PeerMessage]

  ProcessId.Integer
  ProcessStartedAt.Integer
  ProcessObservation.{ProcessId ProcessStartedAt}
  ProcessSelection.[Known.ProcessObservation Unknown]
  ClaimedIdentity.[Claimed.CallerIdentity None]
  IdentityProbe.{ProcessSelection ClaimedIdentity}

  IdleState.[Idle Busy ApprovalWait Unknown Concluded]
  IdleEvidence.[HarnessTurn DaemonRoster TranscriptEnd Unavailable]
  ObservedAt.Integer
  ValidUntil.Integer
  Observation.{IdleState IdleEvidence ObservedAt ValidUntil}
  RouteKind.[CodexQueue CodexTurnStart ClaudePromptRelay MessageOutbox LaneFile]
  Endpoint.String
  Route.{RouteKind Endpoint}
  Routes.Vector<Route>
  FlowRole.[Primary Secondary Core Successor]
  FlowNode.{FlowIdentifier SessionIdentifier HarnessKind FlowRole Observation Routes}
  Nodes.Vector<FlowNode>
  NodeSelection.[All Cluster.ClusterTarget One.FlowIdentifier]
  RouteQuery.{CallerIdentity NodeSelection}
  RegistryRevision.String
  RouteListing.{RegistryRevision ObservedAt Nodes}

  TargetFlows.Vector<FlowIdentifier>
  DeliveryRequest.{CallerIdentity ClusterMessage TargetFlows}
  DeliveryStatusQuery.SourceEventIdentifier
  ByteCount.Integer
  TransportReceiptId.String
  TranscriptRecordId.String
  ReportPath.String
  OutboxEntryId.String
  AcceptedReceipt.{TransportReceiptId ObservedAt}
  TranscriptReceipt.{TranscriptPath TranscriptRecordId PromptSha256 ByteCount ObservedAt}
  ParkedReceipt.{OutboxEntryId ObservedAt}
  FileReceipt.{ReportPath ObservedAt}
  PendingReason.[Busy ApprovalWait UnknownRoute StaleObservation TransportUnavailable WitnessPending]
  PendingReceipt.{PendingReason ObservedAt}
  ReceiptKind.[Accepted.AcceptedReceipt TranscriptWitnessed.TranscriptReceipt Parked.ParkedReceipt FileOnly.FileReceipt Pending.PendingReceipt]
  RecipientReceipt.{SourceEventIdentifier FlowIdentifier RouteKind ReceiptKind}
  RecipientReceipts.Vector<RecipientReceipt>
  DeliveryReport.{SourceEventIdentifier RecipientReceipts}
  RouteFailureReason.[UnknownCaller IdentityMismatch UnknownFlow StaleObservation InvalidDatom SourceMismatch UnsupportedRoute]
  RouteFailure.{RouteFailureReason}
]
```

## Worked datom examples

All examples below are **illustrative values, not live receipts or commands
that have been submitted**. They use real flow names for orientation but
synthetic source paths/record IDs and timestamps. The sample body hash is
computed from the displayed UTF-8 sentence; that computation does not create
a transcript witness. Production examples must be rendered and parsed by the
selected generated types.

Enum values begin with the variant. Struct values are positional braces; a
standalone Context does **not** gain a `Context.` constructor. String values
are shown with guillemets, even where a bare atom could be accepted.

### Current Context, ClusterMember and Relay

Context fields in order: source flow, source turn, transcript, body hash, exact
words, topic, answered, corrected, uncertainties.

```datom
{ «efa157» «demo-source-turn» «/example/efa157.jsonl» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» «The successor package is ready for review.» «Successor package review» «A request for readiness» «No correction asserted» [ «Example context, not a model receipt» ] }
```

One ClusterMember:

```datom
{ «d9961c» «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» }
```

Current Relay, with that Context and one destination member:

```datom
Relay.{ «efa157» «efa15708-dc5d-42ce-af62-8ffb84c9815e» «/example/efa157.jsonl» «The successor package is ready for» «successor package is ready for review.» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» { «efa157» «demo-source-turn» «/example/efa157.jsonl» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» «The successor package is ready for review.» «Successor package review» «A request for readiness» «No correction asserted» [ «Example context, not a model receipt» ] } 1789574400000000000 Primary [ { «d9961c» «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» } ] }
```

The existing relay wire text appends the exact original sentence after this
header. Do not relabel the source flow as the CLI executor.

### CallerIdentity, IdentityProbe and IdentityResolved

Self-declared caller value:

```datom
{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared }
```

The caller asks Flow to resolve a PID/start-time observation and declared
identity; these numbers are demonstration values, not a live process claim.

```datom
WhoAmI.{ Known.{ 1234 5678 } Claimed.{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } }
IdentityResolved.{ «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared }
```

If Flow cannot witness a stronger binding, it returns Declared or refuses. It
must not upgrade the evidence merely because the strings agree.

### PeerMessage and DeliveryRequest

The peer variant has a distinct provenance path and body:

```datom
Peer.{ «demo-peer-1» { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } { «/example/peer.txt» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» } «The successor package is ready for review.» }
```

Deliver it, keeping the caller separate from the source-bearing message:

```datom
Deliver.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } Peer.{ «demo-peer-1» { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } { «/example/peer.txt» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» } «The successor package is ready for review.» } [ «efa157» «d9961c» ] }
```

### RouteQuery and RouteListing, including all six present nodes

```datom
Routes.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } All }
Routes.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } Cluster.Primary }
Routes.{ { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Declared } One.«efa157» }
```

This example deliberately uses Unknown/Unavailable idleness for every node.
It is an anatomy of known identities and possible routes, not a claim that
these routes are currently eligible. Successor d9961c stays Successor until
cf7879's explicit handoff; Claude's unlaunched successor has no invented ID.

```datom
RoutesListed.{ «demo-registry-revision» 1789574400000000000 [
  { «efa157» «efa15708-dc5d-42ce-af62-8ffb84c9815e» Claude Primary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { ClaudePromptRelay «efa15708-dc5d-42ce-af62-8ffb84c9815e» } { LaneFile «flows/efa157/log.md» } ] }
  { «cf7879» «01a0a715-2d5d-7342-b278-1dbcf78795bd» Codex Primary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0a715-2d5d-7342-b278-1dbcf78795bd» } { LaneFile «flows/cf7879/log.md» } ] }
  { «d9961c» «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» Codex Successor { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0aacb-ac84-71a1-88a0-05ed9961ca9d» } { LaneFile «flows/d9961c/log.md» } ] }
  { «57a7aa» «57a7aa02-e52d-4266-8746-6770ff770d11» Claude Secondary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { ClaudePromptRelay «57a7aa02-e52d-4266-8746-6770ff770d11» } { LaneFile «flows/57a7aa/log.md» } ] }
  { «348e7b» «01a0a11f-6130-70e2-80b1-796348e7b086» Codex Secondary { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0a11f-6130-70e2-80b1-796348e7b086» } { LaneFile «flows/348e7b/log.md» } ] }
  { «e43002» «01a0a792-2d0e-7a53-ac0b-9b3e43002941» Codex Core { Unknown Unavailable 1789574400000000000 1789574400000000000 } [ { CodexQueue «01a0a792-2d0e-7a53-ac0b-9b3e43002941» } { LaneFile «flows/e43002/log.md» } ] }
] }
```

Each row demonstrates FlowNode, Observation and Route. MessageOutbox is a
different route: it becomes eligible only when the live Nexus can durably park
and later drain that recipient. A route being listed never proves it works.

### ReceiptKind, RecipientReceipt, DeliveryReport and DeliveryStatus

```datom
DeliveryRecorded.{ «demo-peer-1» [
  { «demo-peer-1» «cf7879» CodexQueue Accepted.{ «demo-transport-ack» 1789574400000000000 } }
  { «demo-peer-1» «efa157» ClaudePromptRelay TranscriptWitnessed.{ «/example/efa157.jsonl» «demo-recipient-record» «ce7edacab893549dd4220bd4a65669667cc013bcfc8e39d1552b3aaafae1bb94» 42 1789574401000000000 } }
  { «demo-peer-1» «57a7aa» MessageOutbox Parked.{ «demo-outbox-row» 1789574402000000000 } }
  { «demo-peer-1» «e43002» LaneFile FileOnly.{ «/example/core-report.md» 1789574403000000000 } }
  { «demo-peer-1» «348e7b» CodexQueue Pending.{ WitnessPending 1789574404000000000 } }
] }
DeliveryStatus.«demo-peer-1»
```

The byte count above refers to the 42-byte sample sentence, not an entire
recipient record including its header. The final contract must specify which
byte range each hash/count covers. Prefer separate body hash and delivered
payload hash if both are needed, never switch their meanings silently.

### Typed refusal

```datom
Refused.{ UnknownCaller }
Refused.{ IdentityMismatch }
Refused.{ StaleObservation }
Refused.{ SourceMismatch }
```

## Implementation and adoption boundaries

The anatomy is intended for editing with the living. Existing Relay compatibility
is preserved in the proposal; Peer, route queries, identity replies and richer
receipts are additions. Adding variants or fields is not automatically archive
or wire compatible. Each adoption needs a contract version and typed upgrade
operation, generated-code check, parser fixtures and old-record/migration tests
where stored data changes. This report does not apply the deployed Message
schema-3 migration or claim its pending row recovered.

For the first live loop, a configured Flow-owned route snapshot is acceptable
if its provenance/freshness and caller declaration are explicit. Do not block
a working datom relay on inventing a new authentication system. Conversely, do
not call that configuration an activated Flow registry or a live Routes query.
The report below will name exactly what order 10B actually implements and which
recipient transcripts contain its datom.


Order 10B is in progress. No new datom recipient witness is claimed by this anatomy publication.

## Order 10B build correction and current boundary

The focused Message check at 181412aebec3d8e3a919195cd3f8a2efe4ee2599 passed according to the worker. Its earlier claim that the full package passed was false: root ran the exact remote Nix package build and witnessed failure in tests/relay_process.rs because tests/fixtures/codex-session-meta-response.jsonl was omitted by the Nix source filter. The reported package store path was a planned output, not an existing artifact. The worker acknowledged this correction and is fixing the filter. No live datom delivery has yet been claimed.

The additive Peer contract is published on signal-message proposal/cf7879-peer-cluster-message at 926dcc9447a1b047ef514c98782b9858f55616a4, with generated PeerEnvelope and codec round trips (worker check receipt; root consumer integration remains underway). Primary prompt-relay recognizes Peer and refuses its re-relay at 19823799ffa93be2d08488da1f191cf7d023f779; root local process fixtures pass, remote check running. No main or deployment movement.

Hourly quota receipt: account/rateLimits/read at 2026-09-16T16:52:06.490Z reports codex weekly 10080-minute window usedPercent 90, hence 10 percent remaining, resetsAt 1789830328 (2026-09-19T15:05:28Z). Three reset credits available; none consumed. Continuing only the current order 10 corrections and transcript witnesses.

Order 10B root check: Primary 19823799ffa93be2d08488da1f191cf7d023f779 remote Nix prompt-relay-fixtures passed, derivation /nix/store/nlyig24h4ray6k1n6d6wby045mwid15p-primary-prompt-relay-fixtures.drv, output /nix/store/bw6as0ljb38hd2cxc1snndcvf3ngws00-primary-prompt-relay-fixtures, actual exit 0. A subsequent one-line source-event binding at 9caafa8dbded733c855e96bd1bdad25aec0159a0 is now under its own check. The real order 10 source is user eb26a23f-ce6b-4117-bed1-6790bb373b74, 1385 UTF-8 bytes, SHA-256 3da491b25af0912a59c211d2bde0a452c7d9f895aae913015e1d6963dd770b30; production rendering initially refused two matches (queued and user records). An explicit event-id filter preserves ambiguity refusal for genuinely distinct prompts.

Live roster inspection at approximately 16:50Z: efa157 busy; 57a7aa has only a dead background row without pid. Neither was bypassed or relabeled idle. Actual deliveries remain pending.

# Order 10 live Datom delivery receipts

The ordinary Message CLI accepted the production-codec Relay datom and dispatched it through the configured prompt-relay bridge. Four Codex user transcripts contain the identical 3904-byte payload, SHA-256 d041d799b8de4e7bfd8781a92c368b83f34db0748b79bbdb5ba8ed95a7e16c4f. The original living source body is 1385 bytes, SHA-256 3da491b25af0912a59c211d2bde0a452c7d9f895aae913015e1d6963dd770b30. The payload starts Relay.{, with no JSON recipient header.

Invocation: `message cluster DATOM --body-file BODY --route-config FLOW_ROUTES --to FLOW@SESSION`. This used the locally built integrated candidate; final published revision and remote Nix receipts follow. Route configuration is an explicitly observed setup snapshot, not an activated Flow registry. Caller attribution remains declared, not authenticated.

- cf7879: user record `msg_01a0ab27-4643-7a30-b315-17ada6453815`, 2026-09-16T16:57:52.963Z, `/home/li/.codex/sessions/2026/09/15/rollout-2026-09-15T23-59-38-01a0a715-2d5d-7342-b278-1dbcf78795bd.jsonl` line 20382.
- d9961c: user record `msg_01a0ab26-9a21-7291-82c9-485d6386b598`, 2026-09-16T16:57:08.898Z, `/home/li/.codex/sessions/2026/09/16/rollout-2026-09-16T17-17-49-01a0aacb-ac84-71a1-88a0-05ed9961ca9d.jsonl` line 475.
- 348e7b: user record `msg_01a0ab27-4fde-7bd1-baa5-060e17cb64a0`, 2026-09-16T16:57:55.422Z, `/home/li/.codex/sessions/2026/09/14/rollout-2026-09-14T20-13-03-01a0a11f-6130-70e2-80b1-796348e7b086.jsonl` line 3852.
- e43002: user record `msg_01a0ab26-9b72-7820-850b-39a976807aee`, 2026-09-16T16:57:09.234Z, `/home/li/.codex/sessions/2026/09/16/rollout-2026-09-16T02-16-09-01a0a792-2d0e-7a53-ac0b-9b3e43002941.jsonl` line 44.

Claude routes remain pending: current efa157 roster is waiting/blocked at a permission prompt; secondary 57a7aa has no live pid. No idle gate was bypassed. A codec-produced honest Peer note is prepared beside this report; no Claude delivery is claimed. The source event is an agent report identifier, not human provenance.

Scope limitations: no global install, activated Flow registry, route-list CLI, busy-Nexus parking, or main/deployment move. The available route/type anatomy remains the editable proposal. No Claude successor launch or Codex authority transfer.


## Final published code and remaining gates

Root remote-ref readback: Message proposal/cf7879-message-peer-integration is 0867b6b8253d0cdc5a421ac9e0dc0d9085c8a37b; Primary proposal/cf7879-prompt-relay-datom is 9caafa8dbded733c855e96bd1bdad25aec0159a0. Message integrates the codec Peer variant, exact event-id selector, body/hash verification, and Flow-configured send bridge. The live CLI proof used its locally built binaries. Worker reports 31 exported Nix checks passed and focused suites relay 15/15, cluster_cli 2/2, cluster_send 2/2; final package artifact receipt is still pending.

Root witnessed the final Primary remote Nix check exit 0: /nix/store/dgbdl250a1lmg1kpr87irhnbzwf12q1a-primary-prompt-relay-fixtures.drv, output /nix/store/1pq79v8gli3ppcyqzbkn66y0pqh4al0j-primary-prompt-relay-fixtures.

Actual Claude delivery attempts at 2026-09-16T17:00:18Z both exited 2 with `not uniquely witnessed idle`: efa157 and 57a7aa. Details are in order10-claude-attempts.json. The prepared Peer note remains file-only/pending, not delivered or parked in the live Nexus. No automatic retry loop was installed.
