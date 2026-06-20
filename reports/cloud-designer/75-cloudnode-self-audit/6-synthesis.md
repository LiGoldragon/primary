# 75/6 — Synthesis: the CloudNode self-audit, deduplicated and ranked

cloud-designer, 2026-06-20. This file merges the five adversarial critics
(`1-rust`, `2-horizon`, the Nix pass that landed as raw findings F1–F8,
`4-design`, `5-process`) into one prioritized ledger, names the top five
fixes, sorts everything into fix-now / psyche-decides / won't-fix, and gives
an unsoftened verdict.

The critics overlap heavily because the same defect shows up at four layers.
Three meta-themes recur and account for most of the high-severity findings:

1. **`cloud_node` as bool-flag accretion** — the same fact (`species ==
   CloudNode`) is re-encoded as `BehavesAs.cloud_node` + `TypeIs.cloud_node`
   in horizon-rs, as `behavesAs.cloudNode` in Nix, as an all-ASCII-digit
   string sniff in the harness, and as an `/etc/os-release` grep in the
   deploy step. Five spellings of one closed choice, none typed across the
   seam. (H1, H2, MEDIUM-1/HIGH-3-design, HIGH-2-rust.)
2. **Invariants live in prose, not types** — "a CloudNode is Metal/Mbr/vda,
   not a Pod, has no super_node" is asserted in doc-comments and validated
   nowhere; an illegal CloudNode (on Pod, with empty disks → `iso=true`)
   passes proposal-time validation. (H3, M5, HIGH-3-design.)
3. **Fake data wearing production clothes** — a throwaway test node `doris`
   at trust `Max`, behind a real-looking ed25519 key whose self-identifying
   placeholder text was silently removed, with invented sizing that already
   forks three ways across datom/harness/mint. (HIGH-1/2/4-design.)

## Verification notes (this synthesis re-checked the load-bearing claims)

- **The ipv6/monitoring bug is LIVE in the current `cloud` worktree.**
  `digitalocean-provider/src/digitalocean.rs:445-446` still hardcodes
  `ipv6: true, monitoring: true` — the create-rejecting values, NOT the
  `false` the critics reviewed. The `9b41512` fix is not in this checkout,
  and `ServerSpec` (`:92-103`) has no `ipv6`/`monitoring` fields. The repo
  was also restructured (`digitalocean-provider/`, `do-deploy-test/`) since
  the audit branch, so the critics' `src/`/`tests/` paths are stale but the
  defects are intact. **Confirmed worse than reported.**
- **The covert ssh key is confirmed.** `grep -i placeholder` on the live
  `goldragon/cloud-node-data/datom.nota` returns nothing; the key blob
  `AAAAC3NzaC1lZDI1NTE5AAAAIDqIzfIew2Kt74D...` carries no self-identifying
  text, and `doris` sits at `Max` in the trust block. **Confirmed.**
- **All eight Nix findings confirmed verbatim** against
  `CriomOS/cloud-node-image/modules/nixos/disks/cloud-node.nix`: two
  `mkForce` (47, 49), one `mkForce` grub-devices (68), `grub.enable = true`
  (67), the redundant `systemd.network.enable = true` (48), seven `mkDefault`
  minimality knobs (35, 73-79), `or false` on line 16, `10-cloud-dhcp` unit.
- **`is_custom_image` and `until_running` confirmed verbatim** in the harness.

## The prioritized ledger (deduplicated)

Severity is the merged max across critics. "Sources" lists the originating
finding ids. Overlapping findings are folded under one row.

| # | Sev | Finding | Sources | Where |
|---|-----|---------|---------|-------|
| 1 | HIGH | `cloud_node` is bool-flag accretion: `BehavesAs.cloud_node` + `TypeIs.cloud_node` re-encode `species == CloudNode`; `TypeIs` is a hand-rolled one-hot of `NodeSpecies`. 22 bools, 2^22 type-check, 11 legal. The exact Form-3 smell `typed-records-over-flags.md` names. | H1, MEDIUM-1-design, NIT-2-design | horizon-rs node.rs:152-210 |
| 2 | HIGH | CloudNode species↔substrate invariants (Metal, Mbr, /dev/vda, no super_node, not Pod) live ONLY in doc-comments; no validator keyed on `CloudNode`. A CloudNode on Pod, or with empty disks → `iso=true`, passes proposal-time validation. | H3, M5, HIGH-3-design, N1 | horizon-rs node.rs:220-235, validation :668-731 |
| 3 | HIGH | `cloud_node` facet is write-only dead state: zero consumers in any repo. The doc-comment claims a CriomOS module gated on it that does not exist in tree. Serialized onto every node anyway. | H2 | horizon-rs node.rs:235,247 |
| 4 | HIGH | Throwaway TEST node `doris` committed into PRODUCTION cluster data at trust `Max`; projects into every real node's horizon as an admin-reachable phantom with no droplet. | HIGH-1-design | datom.nota:28-49,245 |
| 5 | HIGH | Self-identifying ssh placeholder silently swapped for a real-looking ed25519 key with no known private half. `grep placeholder` finds nothing — the only deploy-time safeguard removed. | HIGH-2-design | datom.nota:38 |
| 6 | HIGH | `ipv6:true/monitoring:true` (or post-fix `false`) hardcoded on the only create path — rejects EVERY custom image. Live in current tree. Belongs on `ServerSpec` as typed desired-state. | HIGH-3-rust, P-3 | digitalocean.rs:445-446, ServerSpec :92 |
| 7 | HIGH | `DeployCleanup` is a field-for-field, Drop-verbatim COPY of `LiveCleanup`; doc-comment lies that it "generalizes." The shared cleanup machine belongs in the crate. | HIGH-1-rust | deploy_live.rs:436-509 vs live.rs:163-224 |
| 8 | HIGH | Mode-1-vs-2 detected by "image string is all ASCII digits" — a parser masquerading as a predicate, dead-weight (only feeds a `println!`), fragile (numeric slug mislabels). Should be `enum ImageSource`. | HIGH-2-rust, MEDIUM-2-design | deploy_live.rs:163-165 |
| 9 | HIGH | `grub.enable=true` + `mkForce grub.devices=[/dev/vda]` reimplements and clobbers the existing horizon-keyed bootloader seam in preinstalled.nix. A UEFI-declared CloudNode self-contradicts and builds anyway. Comment claims it "asserts the contract"; it overrides it. | F1, HIGH-3-design | cloud-node.nix:67-68 vs preinstalled.nix:40-45 |
| 10 | HIGH | `10-cloud-dhcp` networkd unit is a byte-identical copy of `10-main-eth`; a third site (test-vm-host) documents the same broad `Type=ether` unit as a footgun. DRY on a load-bearing networking primitive. | F2 | cloud-node.nix:50-57 vs networkd.nix:20-27 |
| 11 | HIGH | The most important event — the first live mode-1 CriomOS deploy that found the create bug and burned DO resources — is recorded ONLY in a git commit body, in no report. Retroactively falsifies 74/6's "Next" framing. | P-1 | git 9b41512 vs reports 73/74 |
| 12 | HIGH | Placeholder sizing committed as fact, forked 3 ways: datom 2GiB/25GiB/nyc3 vs harness 512mb/10gb/nyc1 vs mint 2vcpu-2gb/nyc3. No marker says "invented." | HIGH-4-design | datom.nota:31 vs digitalocean.rs:28-30 vs mint:30-31 |
| 13 | HIGH | Possible leaked live DO resources: custom image 233618631 + droplet. Drop guard does NOT destroy custom images. Teardown unverified in any report; "account empty" asserted only for the mode-2 run. | P-2 | report 74/4:261 |
| 14 | MEDIUM | CloudNode is a near-duplicate of TestVm with a flipped substrate; the only difference (Pod vs Metal) is an independent field. The lean-leaf abstraction photocopied. | M4 | species.rs:23-44 |
| 15 | MEDIUM | "Metal substrate for a cloud VM" reads as a hack to dodge Pod/host-set validation. A droplet IS a guest; modeling it Metal overloads Metal to mean both real iron and pretend-iron. | M5 | species.rs:37-43 |
| 16 | MEDIUM | `DeployConfirmation::resolve` fuses three responsibilities (ssh-wait + remote switch mutation + os-release read); the mutation's failure leaks into `DeployLevel` as `DeployFailed`. | MEDIUM-1-rust | deploy_live.rs:241-267 |
| 17 | MEDIUM | Three coupled `mkForce` (useNetworkd, networkmanager, grub-devices) fight normalize/resolver instead of the CloudNode declaring `enableNetworkManager=false` in horizon. Symptom of wrong facet ownership. | F3, MEDIUM-5-design | cloud-node.nix:47-49,68 |
| 18 | MEDIUM | Image module gated on `behavesAs.cloudNode` conflates "is a cloud node" (species axis) with "wants a DigitalOcean image" (provider/format axis). Hetzner can't reuse it. | F4 | cloud-node.nix:16,23,27 |
| 19 | MEDIUM | flake probes `target.config.system.build ? digitalOceanImage` via `optionalAttrs` — output presence keyed on an import side-effect across three files; an upstream rename makes the output silently vanish. Should key on the horizon facet directly. | F5 | cloud-node.nix:23 → flake.nix:200-204 |
| 20 | MEDIUM | Mint script defaults to `nixos-infect` (the rejected bloated path), `curl\|bash -x` of an external `master`, swallowed `\|\| true`, then snapshots whatever survived. Non-reproducible in a reproducibility repo. | MEDIUM-4-rust, LOW-2-design | mint:33,80-86 |
| 21 | MEDIUM | Mint script is orphaned — zero flake references, no `writeShellApplication`, no pinned `runtimeInputs`. The only producer of the mode-1 image id is unmanaged ambient PATH. | MEDIUM-5-rust | flake.nix vs mint script |
| 22 | MEDIUM | `expect()`/panic as the error strategy at every fallible boundary in a money-spending test; setup failures and post-provision invariants are indistinguishable in CI logs. | MEDIUM-3-rust | deploy_live.rs:44,53,73,85,392-407 |
| 23 | MEDIUM | Two-mode harness couples image-provenance to a `println!`; mode-2-as-CriomOS silently depends on a second env var (`DEPLOY_FLAKE`). A Slug + no flake is a legal, green, useless run. | MEDIUM-2-design | deploy_live.rs:16-22,57-64,251-257 |
| 24 | MEDIUM | The CloudNode test is near-tautological — restates one-line `matches!` derivations, can only pass, silent on every H3 hole (Pod-rejection, empty-disks-iso, super_node). | M3, NIT-2-design | tests/horizon.rs:502-537 |
| 25 | MEDIUM | Four-repo seams untyped; `or false` turns a horizon contract violation into a silent no-op instead of a loud failure. | MEDIUM-3-design, F8 | cloud-node.nix:16 |
| 26 | MEDIUM | ipv6/monitoring bug found at live-deploy, not in the two review passes that claimed `[VERIFIED]` reads of the adapter. Verification confirmed field shape, missed an API-rejecting value. | P-3 | reports 72/5, 74/4:344-359 |
| 27 | MEDIUM | "Ran it live and green" + "CriomOS" in one breath when zero CriomOS bytes touched DO (mode-2 booted stock Ubuntu). Headline over-claims; the matrix is honest. | P-4 | report 73/6:1,14,18-20 |
| 28 | MEDIUM | Report sprawl: 5,680 report lines for a 682-line diff; 73 and 74 re-derive the same end-to-end twice; five planning sub-files per single-arm commit. | P-5 | reports 72/73/74 |
| 29 | LOW | `DeployLevel` carries two stringly representations (`as_witness_field` + `Display`) hand-kept in lock-step; `resolve` folds os-release-read-failure into `SshReachable`, losing data. | LOW-1-rust | deploy_live.rs:350-378 |
| 30 | LOW | ssh option `Vec<String>` rebuilt per call; `root@{ip}` formatted at four sites. Wants an `SshTarget` owning its formatting once. | LOW-2-rust | deploy_live.rs:332-345,253,288,313,327 |
| 31 | LOW | Remote steps return bare `bool`/`Option`, discarding the failure cause; the witness line can't say why a deploy failed. | LOW-3-rust | deploy_live.rs:269,281,310 |
| 32 | LOW | `until_running` returns the last non-running observation as `Some`, so the caller's `expect("reached Running")` succeeds on a non-running host and the harness ssh's a droplet that never ran. | LOW-4-rust | deploy_live.rs:203-220,85 |
| 33 | LOW | Seven `mkDefault` minimality knobs cargo-culted (lowest priority on the settings whose whole point is to suppress weight); the one genuinely-soft default (diskSize) is indistinguishable from them. | F6, LOW-1-design | cloud-node.nix:35,73-79 |
| 34 | LOW | `systemd.network.enable=true` redundant with `useNetworkd`; firewall port 22 re-set though sshd's `openFirewall` already opened it (author admits in comment). | F7 | cloud-node.nix:48,62 |
| 35 | LOW | Mint script is the only mode-1 image producer and is unpinned `curl\|bash` of a moving branch — while the headline declarative image is the reproducible one. Two producers, one not reproducible, and the live harness boots the bad one. | LOW-2-design | mint:82 |
| 36 | LOW | Doc-comment bloat: ~25 lines narrate two `let x = type_is.x;` lines and one `matches!`, asserting the unenforced invariant as fact. | L2 | species.rs:32-44, node.rs:164-235 |
| 37 | LOW | Copy-pasted fixture doc-comment describes the wrong species ("test-VM Pod hosted on prometheus" on a CloudNode-on-Metal fixture). False witness, evidence of copy-paste. | L1 | tests/horizon.rs:441-445 |
| 38 | LOW | "55× smaller" compares content-size to disk geometry; built 1.1 GB exceeds the predicted 0.5-1 GB band with no note. | P-6 | report 74/6:9-15 |
| 39 | LOW | "ssh reachable, 36.7s" presented as frictionless; first connection was refused, disclosed only in a matrix footnote. | P-7 | report 73/6:18-20,66 |
| 40 | NIT | `_directory` TempDir keep-alive: a load-bearing leading-underscore that signals "unused" while it keeps the private key on disk. | NIT-1-rust | deploy_live.rs:387 |
| 41 | NIT | `number_or` lives on `DeployParameters` but is called from `PollBudget`; a generic env-number reader owns it, not one of two consumers. | NIT-2-rust | deploy_live.rs:154,176,180 |
| 42 | NIT | Inconsistent defensiveness: `cloudNode or false` here, bare facet reads in every sibling module. Either the projection is total (drop `or false`) or siblings are unsafe. | F8 | cloud-node.nix:16 vs networkd/edge/dnsmasq |
| 43 | NIT | `doris.online = None` while sibling test node `vm-testing` is `(Some True)`; same intent, two spellings. | NIT-1-design | datom.nota:48 vs :200 |
| 44 | NIT | The 60 GB snapshot hack nearly shipped before the minimal design existed; minimality was reverse-justified against it ("55×"). Process order, not a code flaw. | P-8 | report 74/6:11 |

## Top 5 most deserving of a fix

1. **The covert ssh key + doris-in-production (ledger #4, #5).** A throwaway
   test node at trust `Max` behind a real-looking key whose only safeguard —
   its self-identifying placeholder text — was silently deleted, in a file
   the README calls production trust data. *Fix:* move doris to a
   test-cluster fixture (or provision it for real with real values); restore
   a non-decoding self-identifying placeholder, or carry NO key until the
   droplet exists and the host key is read back at first boot.

2. **The live ipv6/monitoring create bug (ledger #6).** Still live in the
   current worktree (`digitalocean.rs:445-446`), it rejects every custom
   image — the exact defect that burned a live droplet+image to discover.
   *Fix:* add typed `ipv6`/`monitoring` desired-state to `ServerSpec`,
   default them in the harness spec, read `spec.*` in `from_spec`. Both the
   hardcoded `true` and the patched `false` are wrong-by-default for some
   image.

3. **`cloud_node` bool accretion + unenforced substrate invariant (ledger
   #1, #2, #3).** Delete `TypeIs` (it IS `NodeSpecies`); make `BehavesAs` the
   Form-3 enum (`Substrate { Metal | Pod }` makes bare_metal/virtual_machine
   mutually exclusive by construction); derive substrate from species so a
   CloudNode-on-Pod / CloudNode-with-empty-disks-as-iso is unrepresentable;
   don't land the facet until its consumer lands. This collapses the
   canonical Form-3 smell, the dead-state, AND the H3 honesty hole at once.

4. **`grub.enable`/`mkForce grub.devices` clobbering the horizon bootloader
   seam (ledger #9).** Delete cloud-node.nix:67-68. Give the CloudNode a
   horizon with `io.bootloader = Mbr` and `io.disks` describing the vda root
   so preinstalled.nix produces grub-on-vda by the same path every other node
   uses. If you genuinely want a build-time guard, write a real
   `assertions = [{ assertion = io.bootloader == "Mbr"; ... }]` — which is
   what the comment falsely claims the `mkForce` does.

5. **The missing live-deploy record + unverified resource leak (ledger #11,
   #13).** Write the record: image 233618631, the rejection, the fix, and the
   account-empty-after state. Verify image 233618631 and any sibling droplet
   are destroyed (the Drop guard does not destroy custom images). The single
   most consequential event in the arc lives only in a git commit body, and a
   billable resource's teardown is unconfirmed.

## Triage

### Fix now (cheap, clearly right — no design judgment needed)
- Restore a non-decoding self-identifying ssh placeholder (or remove the key)
  — #5. Cheap, and the current state is a security smell.
- Delete the false "generalizes" doc-comment on `DeployCleanup` and the
  copy-pasted "test-VM Pod hosted on prometheus" fixture comment — #7 (the
  comment half), #37. Lying comments are worse than none.
- Delete `is_custom_image` and the dead `systemd.network.enable=true` and
  redundant firewall-port lines — #8 (deletion half), #34.
- Make `until_running` return only on true success (or a timeout error) so
  the `expect("reached Running")` stops lying — #32.
- Caveat or drop "55×"; add one sentence on the 1.1 GB-vs-0.5-1 GB overshoot
  and the ssh-retry; write the missing live-deploy record — #38, #39, #11.
- Drop `mkDefault` on the minimality knobs (plain `false`, authoritative) —
  keep it only on `diskSize` with a comment saying why — #33.

### Psyche should weigh (design decisions, not mechanical)
- **Collapse `cloud_node` into a typed substrate/profile enum and delete
  `TypeIs`** — #1/#2/#3/#14. This is the right shape but it breaks the
  one-hot projection contract and every facet reader; a deliberate schema
  move, not a quick edit. Pre-production, breaking all consumers at once is
  sanctioned, but the psyche owns the timing.
- **How to model an externally-hosted guest** — #15. Is a droplet `Metal`,
  `ExternallyHostedMetal`, or `Pod`-with-external-host? This is a genuine
  modeling question with downstream validation consequences.
- **Whether doris is a test node or a real cluster member** — #4, #12. Drives
  where it lives and whether the sizing is invented or measured.
- **Split the image module on the provider/format axis vs species axis** —
  #18, #19. Pays off only when Hetzner lands; worth deciding now so the seam
  is right, but it's a structural call.
- **`ServerSpec` desired-state for ipv6/monitoring** — #6. The fix is clear;
  whether the fields are typed (`Ipv6Networking`/`MonitoringAgent`) or bool
  is a judgment.
- **Whether to keep nixos-infect at all** — #20, #35. Report 73 rejected it;
  deleting vs pinning vs replacing with the declarative image is a call.
- **Whether to land the `cloud_node` consumer (the CriomOS gate) in the same
  change** — #3. The discipline says yes; the psyche may stage it.

### Won't-fix / accept with reason
- **Four repos is correct** (#25 is about typing the seam, not the count) —
  schema in horizon-rs, OS modules in CriomOS, data in goldragon, deploy in
  cloud matches workspace boundaries. Accept the spread; fix the untyped
  seam.
- **`expect`/panic in a test harness** (#22) — acceptable for genuine
  post-provision invariants; only the setup-vs-invariant conflation is worth
  fixing, and even that is a polish, not a correctness, issue. Lower-priority.
- **`number_or` placement, `_directory` naming, `online` spelling** (#41,
  #40, #43) — true nits; fix opportunistically, don't gate on them.
- **The os-release re-confirmation in the harness** (part of #25) — fine as an
  independent belt-and-suspenders end-to-end check; just don't call it the
  system's notion of "is this a cloud node."

## The unsoftened verdict

This body of work shipped a genuine artifact — a 1.1 GB content-sized
declarative DigitalOcean image, and a deploy harness whose witness-line
honesty mechanism (`as_witness_field` refusing to say `criomos-confirmed`
when no marker matched) is real and disciplined. But the work that surrounds
that artifact is the opposite of the beauty the workspace asks for: instead
of the special case dissolving into the normal case, CloudNode adds a fresh
special case at every layer — a new species variant, two redundant derived
bools, a hand-rolled one-hot encoder, an all-digit string sniff, a new image
module that `mkForce`s its way past three sibling modules and clobbers an
existing typed bootloader seam, and a deploy mode that's really a `println!`
label. Its central invariant exists only as prose that the type system never
checks, so an illegal CloudNode passes proposal-time validation and breaks at
deploy. Worse, the data is dishonest: a throwaway test node sits in
production trust data at `Max`, behind a real-looking key whose only
safeguard was silently stripped, with invented sizing already forked three
ways — and the create bug that this all exists to exercise is *still live in
the current worktree*, rejecting every custom image, never having reached the
fix the critics reviewed. The reports document the plan for this in 5,680
lines while the one event that mattered — the live deploy that found the bug
and spent real money — is recorded nowhere but a git commit body, and a
billable resource's teardown is unconfirmed. The engineering instincts are
sound and the honesty mechanism is admirable; the execution cut the corners
that matter most — types, data integrity, and the durable record — and called
the cuts "generalizes," "asserts the contract," and "ran it live and green"
when they were none of those things.
