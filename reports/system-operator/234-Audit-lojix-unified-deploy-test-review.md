# Audit: lojix unified deploy/test review

System-operator audit of `reports/system-designer/158-lojix-unified-deploy-test-poc-contracts-and-verification-2026-06-21.md`, with report 157 and the live `lojix` / `signal-lojix` / `meta-signal-lojix` sources checked as evidence.

## Bottom line

Report 158 is directionally right and materially better than report 157. The reframe is real: contained testing belongs on the ordinary face; production deployment belongs on the meta face; the current daemon has the test machinery already built on the owner socket.

The strongest correction is that report 158 overstates its type-safety claim. Its proposed ordinary `DeployClosure` still carries `ClusterName` and `NodeName`, so an ordinary caller can still name a real cluster node as the profile being built. The unrepresentability property must be narrower and more precise: ordinary callers must be unable to use a real node name as the effect target or generation-promotion target. That likely requires a distinct typed noun for "configuration/profile to build" versus "production node to mutate."

## Source-verified facts

- `meta-signal-lojix/schema/lib.schema` currently has request roots `[Deploy Pin Unpin Retire Test]`; `Test` is owner/meta today.
- `lojix/src/daemon.rs` authorizes owner peers before decoding meta frames, then special-cases `Deploy` and `Test` into daemon-owned job actors.
- `signal-lojix/schema/lib.schema` currently owns ordinary reads and shared test-record types, not production mutation roots. Its source comments already say `Deploy` / `Pin` / `Unpin` / `Retire` live in `meta-signal-lojix`.
- `signal-lojix/INTENT.md` and parts of `signal-lojix/ARCHITECTURE.md` still describe `Deploy` / `Pin` / `Unpin` / `Retire` as ordinary operations. That is documentation drift against the source schema.
- Spirit record `vudl` names exactly `Deploy`, `Pin`, `Unpin`, and `Retire` as owner-only. It does not mention `Test`.
- Spirit record `cgd8` is about daemon configuration through meta-signal and is not about testing.
- Spirit record `mq5s` already captures the reframe and explicitly says cpip's reusable testing interface is lojix's ordinary contract.

## Findings

### 1. Critical: the proposed type boundary still lets ordinary name a node

Report 158 says an ordinary caller "literally cannot construct a request naming a production node." But the POC sketch defines:

`DeployClosure { ClusterName * NodeName * DeploymentKind * source ProposalSource flake FlakeReference ... }`

and ordinary `DeployContainedRequest` carries that `DeployClosure`. That means ordinary requests still name a `ClusterName` and `NodeName`.

That may be correct for "build the mercury configuration inside a contained target," but it means the safety property is not "ordinary cannot name a production node." The actual property is: ordinary can name a node profile/configuration, but cannot name that node as the live mutation target and cannot promote a generation on it.

Implementation consequence: split the nouns.

- `ProductionNode { ClusterName NodeName }` means live mutable cluster target and stays meta-only.
- A different ordinary type should name the configuration to instantiate, such as `NodeProfile`, `DeploymentProfile`, or `ClusterNodeProfile`.
- `DeployClosure` should not blur those roles under the same `NodeName` field.

This is not wordsmithing. It is the difference between type-unrepresentable authority and a runtime promise that the daemon will interpret the same `NodeName` safely.

### 2. High: `AssertAgainst` is probably the wrong public root

The workspace contract-repo discipline explicitly warns against using Sema class words like `Assert` as public wire roots. Report 158 proposes `AssertAgainst` as an ordinary operation root.

The action is domain-level verification against a contained handle, not a Sema `Assert` command. Better root candidates:

- `VerifyContained`
- `CheckContained`
- `ProbeContained`
- `EvaluateContained`

`AssertAgainst` can remain an internal daemon command or a payload noun if needed, but it should not be the public contract root unless the contract-repo rule is intentionally changed.

### 3. High: cloud droplets are not just a cost footnote

Report 158 correctly flags the cloud tier as the one soft spot, but the issue is stronger than "cost containment is daemon policy." It is a confused-deputy boundary: an unprivileged ordinary caller would cause the lojix daemon to use meta-cloud authority on the caller's behalf.

The minimum acceptable shape before `EphemeralDroplet` becomes runnable:

- typed lease or quota credential on the ordinary request;
- daemon-level spend cap and droplet count cap;
- persisted lease table in SEMA;
- restart reconciliation that lists provider state and reaps expired or orphaned droplets;
- a negative test proving ordinary callers cannot exceed quota by request splitting.

Until those exist, `EphemeralDroplet` should return `SubstrateUnavailable`.

### 4. Medium: "smart constructor clamp" is not really schema-level type safety

Report 158 says `LeaseSeconds NonZeroInteger` is required and "daemon clamps to a configured maximum at decode (smart constructor, not a runtime if)." The nonzero property can be a schema/domain newtype. The configured maximum cannot be purely schema-level because it depends on daemon policy state.

The honest split:

- schema/type: positive nonzero duration;
- daemon policy: maximum lease, quota, and expiry validation;
- SEMA: persisted lease and reaper state.

Calling the max clamp a smart-constructor property risks hiding policy as type safety.

### 5. Medium: cpip probably does not need a Spirit edit

Report 158 recommends a possible `cpip` Clarify. But `mq5s` already says the reframe and explicitly states cpip's reusable testing interface is lojix's ordinary contract. `cpip` itself does not contradict that; it says there should be one reusable testing interface and names the substrates.

A `cpip` Clarify would improve direct lookup discoverability, but it is not a correctness requirement. I would avoid it unless the psyche wants cpip itself to carry the reframe inline.

### 6. Medium: vudl extension is optional, but source docs need synchronization

Report 158 is correct that `vudl` is not a conflict. It owner-gates Deploy/Pin/Unpin/Retire and does not mention Test. Extending it to mention contained testing on ordinary is optional.

The concrete synchronization issue is not Spirit; it is repo docs:

- `signal-lojix/INTENT.md` still says ordinary requests include `Deploy`, `Pin`, `Unpin`, and `Retire`.
- `signal-lojix/ARCHITECTURE.md` has the same old table.
- `signal-lojix/schema/lib.schema` and `meta-signal-lojix` already embody the newer split.

Those docs should be updated when the implementation wave begins, and before another agent treats them as source of truth.

### 7. Medium: report 157 should not remain a co-equal design report

Report 157 is useful history but has three stale parts:

- it proposes an ordinary `Test` shape rather than 158's stronger `DeployContained` / verify / release decomposition;
- it says `vudl` / `cgd8` conflict with the reframe;
- it lacks the wave-0 codegen and critique corrections.

Keep report 158 canonical. Retire or supersede 157 rather than leaving both as a pair future agents must reconcile.

## Greatest insight

The reframe does not merely move `Test` between sockets. It forces a vocabulary split between these three nouns:

- profile/configuration to build;
- contained throwaway target to realize it inside;
- production node whose live generation may be mutated.

Report 158 has the second and third nouns, but its `DeployClosure` still uses `NodeName` for the first noun. That is where the design can accidentally smuggle the old production target shape back into the ordinary face.

The right implementation sequence is therefore:

1. wave 0 proves schema/codegen can keep unrelated ordinary/meta target types separate;
2. wave 0 also proves the daemon can share pipeline mechanics by accepting a target-agnostic "closure profile" noun, not by sharing a target supertype;
3. wave 1 moves hermetic contained execution to ordinary and deletes meta `Test`;
4. only after that should VmHostGuest and cloud substrates land.

## Questions for the psyche

1. Do you want the safety invariant to be "ordinary cannot name a production node at all," or the narrower invariant "ordinary can name a node profile to build, but cannot use it as a live mutation target"? The current POC only supports the narrower invariant unless the profile noun is split from `NodeName`.
2. Should unprivileged ordinary callers be allowed to cause bounded cloud spend through lojix, or should `EphemeralDroplet` require a typed quota/lease credential issued by an owner/meta approval path?
3. Is owner-socket `SO_PEERCRED` enough authority for production `Deploy`, knowing it means "same Unix uid/gid as the daemon," or should production deploy require an additional criome/mentci verdict before promotion?
4. Do you want report 157 retired/superseded now, with 158 as canonical, or preserved as historical context until the first implementation wave lands?

## Verification notes

This was a read-only audit. I did not run cargo or Nix tests because `system-designer.lock` currently claims `/git/github.com/LiGoldragon/lojix` and related repos for active work. Evidence came from report 157, report 158, the three repo intent/architecture/schema files, the daemon source, and direct Spirit `Lookup` of `cpip`, `vudl`, `cgd8`, and `mq5s`.
