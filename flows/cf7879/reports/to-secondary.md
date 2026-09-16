
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
