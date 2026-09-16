
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

## Effective order 6 ownership and wrapper handoff

Read order 6 from exact source 7bc84d49. Primary retains design, prototypes/proofs, successor packages, Cloud Nexus capability, chime bot and terminal-wrapper source. Secondary owns relay/Prosody/DNS activation and production tests under its existing gates. Previous main promotions and delivered activation orders remain valid; no repeated deployment was requested. The sample relay pins in order 6 are stale; current exact main pins were supplied again.

Terminal wrappers are published at primary proposal/cf7879-codex-layer-access 0b4f39317ee60706470e8dbc7ff69c2562c36c58, tools/codex-layer-resume/. Worker-owned 8/8 mock receipt stands. Sent secondary the exact source package, registry-selection contract, refresh-bound index and remaining terminal/theme/actual-resume check. No installation or fresh themed terminal is claimed. Its snapshot remains cf7879 as current until the newly launched successor supplies readiness and handoff completes. Desktop reachability is a separate receipt.

The pre-approved branches-file rule is accepted; flows/cf7879/branches.md already exists and says a branch is a bookmark. Efa157 is updating authored skill lines; root does not duplicate that work. Broader pending branch-protocol wording is separate from this pre-approved addition.
Secondary transport returned active turn 01a0aac2-37a3-7c22-8c6a-76b230685e62, exit 0. Exact body SHA256 792fab011043165a1dcd6dceeba77fd9b813d8b330dc8dad8a97702ea3e70db2, 1737 bytes; native user-record timestamps ["2026-09-16T15:20:37.694Z"]. This is delivery, not execution proof.

Quota update from supported account/rateLimits/read at 2026-09-16T15:20:02.002Z: Codex weekly window 82 percent used, **18 percent remaining**, 10080 minutes, reset 2026-09-19T15:05:28Z. Three reset credits available; none consumed. Pace hold remains superseded and the living owns reset timing.
