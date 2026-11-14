# Field core Sol 72221c handover

## Control state

VersionZero Astra and Field core Astra coordinate this work. Field core Sol flow `72221c` is handing operator custody to its successor. Fable's latest order is **handover and quiesce only**: the earlier private native-start grant is held until the successor has custody and the exact Codex executable and login source are settled. Do not start a capsule, proxy, socket, model query, credential operation, deployment, adoption, stable Flow Nexus restart, or other runtime action from this flow.

The living's freeze on changing the running seat remains in force until he is up, independently of the 13:00 UTC cutoff. The current native seat must not be restarted. Its facts are native session `01a1b59c-9866-7630-90c2-18572221cc61`, pane `wXT:p1`; its transcript is under the current `CODEX_HOME` sessions tree.

A successor does not inherit custody from this document. It must freshly observe locks and receive explicit parent disposition before changing or releasing them.

## Flow 0.53.2 canary: immutable state

The scenario source is clean on unpushed branch `0.53.2-canary-b060`:

- revision `42477e645bdb5f0a2d65386d0acd7381fe5798fa`
- tree `81fa255e0b61043fd0c7013398519f30e0713d89`
- accepted production ancestor `85bf0f1be9997ed2b1c46a8814750a77704ea40f`
- worktree `/git/worktrees/flow-0532-canary-b060`
- reviewed helper SHA-256 `0702502caf04ce76b4058512d12b397d5ddf584dbeaceea6c37bf1c91da8d766`
- handover configuration SHA-256 `071006255ed02c1d711fce89d00f88784a910a265ebbaf31a94959a46afc3a6f`
- runner SHA-256 `2e1cd8db37e8d80c293827744171a50f72022ffa094ba0c9c531d377094b8fe0`
- `flake.nix` SHA-256 `01947845dfa76e691caa0ebdef4d052e1677bcd6c12eb8e0f2a0a0c6d9b55b62`

The reviewed private composition is `/tmp/72221c-flow0532-capsule-launch-42477e6`:

- expression `capsule-launch.nix`, SHA-256 `24f25a1c164f9670613bf2fdca08637d3673d1fabfd71c9a22fbe3aa3e79edb8`
- reviewed commands `commands.txt`, SHA-256 `6601e0daf3c8f71bd98fa91f6396033f94c90fe65c2a1c67b85eec82d96beb53`
- source/command manifest `SHA256SUMS`, SHA-256 `7b75e2da55add9ea906ac2ef3dab12ec34287a5563e19ef770fb7d679364e794`
- execution manifest `EXECUTION-SHA256SUMS`, SHA-256 `81db5a7b2c63f0494f5afe5d2cada3dfe5908c21fed8f2c87004be687b21fd11`
- execution receipt `execution-receipt.json`, SHA-256 `a7304eaef6022f48c6357ef365aaec083d293ebbc73435747da0d47e7e646a36`
- bindings `execution-bindings.txt`, SHA-256 `a79b6b6e4160b7d234df0d01dd849730013d46d664120deb1b945b473ab22a5c`
- readiness report `startup-readiness.md`, SHA-256 `7515399206456e81bdc9977379cddb83bc4660201beb07a61b23a2c30080d09c`

The exact reviewed instantiation and remote build both exited 0. Both used the owner-only private TMPDIR and the build used `--max-jobs 0 --no-link`; the log records the scenario and composition derivations built on `ssh-ng://nix-ssh@prometheus.goldragon.criome`. No result link or GC root was created.

- derivation `/nix/store/pph3asbsy0xvby1xb306rx2hq0fkwzp5-flow0532-private-handover-capsule-42477e6.drv`
- built output `/nix/store/dvbdn4jspz89d7h0ggjb3i0b8y92v638-flow0532-private-handover-capsule-42477e6`
- output NAR hash `sha256-C/OO9aMXNH4YOXK4vjfNJdEICDq8YJnHe5dZNAGoyKg=`
- fixed launcher `/nix/store/dvbdn4jspz89d7h0ggjb3i0b8y92v638-flow0532-private-handover-capsule-42477e6/bin/flow0532-private-handover`
- scenario package `/nix/store/vvz4944ci7kj14m833wq8kk33yl0hlnw-flow-capsule`
- accepted configured runtime `/nix/store/dn4dh11fk79hbqyhavigmi6x01rrs6rq-flow-configured-0.53.2`
- accepted generated module `/nix/store/ja0ahvh4sv8sfdq1d44nn3l7kpdayh34-flow-default-configuration.rs`, SHA-256 `1e8462ae8c4cc3cec31340eba55284da874ac6b07710d2085fe90f33cd8bb992`
- accepted compatibility evidence `/nix/store/ln2crrw8n4ks8sbwaz3w44ssl6vpsnkd-flow0531-to0532-private-api-compatibility`
- accepted production evidence `/tmp/01e4a4-runtime/0532-85bf-executed-evidence.md`, SHA-256 `37162431743874883c98f911651e98ed43e78932d9bb5e57da4902e3df5b70cd`

The built launcher's fixed prefix is the scenario `flow-capsule`, the accepted configured runtime, then `--handover`; it accepts only `--keep-going` and `--log PATH`. It was inspected and never executed. The pending startup proposal uses `gpt-5.6-luna`, `--keep-going`, and private witnesses under claim 25918. Model catalog membership is not entitlement, and the runtime is not substitutable by the caller.

Read-only facts for the unresolved executable/login decision:

- candidate executable `/nix/store/1q41fx3vb1hqzdgkr0nk5b0pc4jvyhl1-codex-0.166.0/bin/codex`
- current `CODEX_HOME` `/home/li/.codex-next-8mkkxq293hk2`
- the runner default `~/.codex-next/auth.json` may be stale

No credential was read or copied. Earlier read-only checks found both intended private roots absent; the successor must freshly check them. No native capsule or proxy has ever run. All seven real-seat contract lines are `NOTSEEN`. The H4 archive artifact is distinct from the unsupported Memory retirement and commit-before-delete ordering observation; therefore the full canary cannot pass with present evidence.

## Locks retained

Freshly observed retained claims:

- `25913`, owner `72221c`: `/git/worktrees/flow-0532-canary-b060`, `/git/github.com/LiGoldragon/flow/.git/refs/heads/0.53.2-canary-b060`, `/git/github.com/LiGoldragon/flow/.git/worktrees/flow-0532-canary-b060`
- `25918`, owner `72221c`: `/tmp/72221c-flow0532-capsule-launch-42477e6`
- `25924`, owner `72221c`: this handover file

Legacy claims are not inherited:

- `25909`, owner `01e4a4`: `/tmp/flow-0532-01e4a4-capsule`, `/tmp/flow-0532-01e4a4-preflight`
- `25906`, owner `01e4a4`: `/tmp/01e4a4-0532-compat`

Transfer or release requires fresh `Observe.Locks` and explicit parent disposition.

## Other pending work

### A. mentci-egui baseline build

Core approved a future immutable **remote-only package build** of the existing baseline. This executor remains VersionZero-exclusive until explicit parent release, including disposition of claim 25918; it must not be diverted automatically.

- repository `/git/github.com/LiGoldragon/mentci-egui`
- local and remote revision `2af0aa5a86fdbdfde13e7eb9fd338da40451d901`
- tree `0165cb6220d68bc71ca90c228cd3538ba31218a8`
- `Cargo.toml` SHA-256 `b03c1e733203b4372f940b8c85dbd75226dd841d511cb34f0e3e6db00eb0d5aa`
- `Cargo.lock` SHA-256 `30d05ee152dfd206b7b666a15fc14b310ca455f54273701abeaf7dc241258122`
- `flake.nix` SHA-256 `b061f4d30807eb08096baa87c4a5632b09161c77b3de1bc7961d072eaad9dfbe`
- `flake.lock` SHA-256 `7014875c80227d53bf247890d51e1defd9de7ceda69aad858749129553721972`
- toolchain SHA-256 `67068962f4b95d4c99e0cdc8d1cc1e37d0157af493d34d00cc735bfb2ffec16b`
- exact target `git+file:///git/github.com/LiGoldragon/mentci-egui?rev=2af0aa5a86fdbdfde13e7eb9fd338da40451d901#packages.x86_64-linux.default`

The future attempt needs a private claim and TMPDIR, `--max-jobs 0 --no-link --no-update-lock-file`, original manifest/lock/features, and no `UPDATE_INTERFACE_ARTIFACTS`, dependency refresh, local fallback, runtime, profile/root, activation, or publication. Build the package only, not `checks.default`. Record source, toolchain, vendor linkage and distinguish fetch, evaluation, vendor, and compiler failures. The observed source-symbol mismatch—authored app imports named types while pinned/current client exports encoded roots—is not an actual failed build and establishes no absent behavior. Core received the full map through `7336`; no migration or source custody was granted.

Six other intakes remain held: Curriculum deploy has a dirty unknown owner and remote divergence; Flow Nexus tests have an absent path graph; router, mirror, system, mentci-egui Dotos, and cohort matters retain their stated unknowns. Do not broadly scan or repin.

### B. book flow orders

Fable's queued orders have now been consumed, but no book file has been edited. The requested design is to remove `/home/li/primary/.claude/agents/book.md`; `role:book` makes `{ Psyche book Haiku }` publish through its own Artifact. Builder-form faults—headings, context lines, code width, fence language, bookmaker fixes—are corrected before sending. Wording faults go to the author in one sentence, retaining builder text until asked.

Before deciding whether anything else is unused, audit actual running-flow use of `book-author.md`, `book-page.md`, and `book-reader.md`. Their removal is not authorized. Book Haiku `abaf2b` confirms it already uses its own Artifact, launches no book subflow, has no worker, and landed no edits. The source of the Fable-owned `role:book` skill remains unknown. Fable request `7913` for a separate bounded Codex worker/existing route is pending. Do not divert this VersionZero-exclusive executor.

### C. mentci-lib publication

Publication of `c7608800ffd8e93e8d00f5107c8bec39e3b78a09`, tree `c7671dc669cb86cde19fab4d78ac21f2c76fb2ce`, as `v1.1.0` is complete. Claims 25910 and 25912 were released; original 25905 was transferred and released. Report: `/tmp/01e4a4-runtime/mentci-lib-publication-report-72221c.json`, SHA-256 `ef03447ea424760ca22dab48cbd1cc93e3871b686b898c6fcb092607b25f3aee`. Main, tag, and actual intended GitHub immutable fetch matched all 21 hashes.

The authoritative aggregate is **54 below / 83 current / 137 manifests**. The worker's 53/84 summary counted two dependency records and is not the aggregate. Correct that misleading summary only during the next authorized record handling; do not overlap ledger mutation. Old Aggregator and mentci 45-minute review reminders are administratively closed; an unmatched local CLI `Done` error does not reopen them.

### D. queue-delivery incident

Flow 72221c ended a turn waiting for review. Latest MiddleAbrupt orders became visible only when this flow used its own `flow-meta Inspect`, after Field Astra sent a hand prompt. The cause is unknown. Flow Nexus is investigating a past-threshold early-return hypothesis; it is not established, and context token count is not exposed. `Inspect` returns the queue without clearing it, so a successor must track actual consumption and apply the latest word. Do not restart this seat as an investigative shortcut.

## Quiescence

At handover creation, packaging was terminal. The final process check found no `flow0532-private-handover`, `flow-capsule`, `codex-observer.py`, capsule-specific proxy, Nix build, or Nix instantiation process from this work. It did show pre-existing Codex control proxies on the shared current `CODEX_HOME` control socket; this worker did not start, alter, or stop them. This worker leaves no running exec session or background effect and starts no further command after that check. Claims remain held for explicit successor disposition.
