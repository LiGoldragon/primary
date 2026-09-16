
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
