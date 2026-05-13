# 07 — CriomOS stack deep audit

Date: 2026-05-12
Role: system-assistant
Scope: CriomOS, CriomOS-home, horizon-rs, lojix-cli, goldragon, clavifaber,
       nota-codec, the recent reports cluster, and the workspace skills that
       constrain the above.
Method: parallel surveys (CriomOS structure, Rust workspace coherence,
        report/decision narrative arc) synthesised against ESSENCE.md, AGENTS.md,
        and recent commits across the active CriomOS-cluster repos.
Builds on but does not supersede:
        `reports/system-assistant/02-04` (cloud-host plan),
        `reports/system-assistant/05` (workload decision),
        `reports/system-assistant/06` (post-slice-1 status).

## 0 · Why this report exists

The stack is in a fast-moving week: Wi-Fi PKI is being rebuilt, NodeServices
just replaced node-name gating, ZST actors just got collapsed, P1 of the
cloud-host plan just landed types, clavifaber just dropped IdentitySetup
and merged host-key ownership into sshd, contract crates are mid-transition
to owning both wire and text derives. Across all that motion the user
asked for a step-back: what's working, what's broken, what should the
shape look like that we aren't yet committing to.

This report is opinionated. Its job is to find friction.

## 1 · State of the union

### 1.1 The narrative arc, last seven days

| Theme | Resolution status | Key reports |
|---|---|---|
| Wi-Fi PKI migration (policy/key/distribution three-layer) | architecture set | system-specialist/117, designer/139, designer-assistant/29 |
| Contract types own wire AND text derives | rule reversed and codified | designer/138, designer-assistant/28 |
| Workload is native NixOS, not OCI | resolved (`skills/nix-discipline.md`) | system-assistant/04–05, designer-assistant/27-response |
| NodeServices replaces node-name gating | landing in commits across repos | designer/139, system-specialist commits on CriomOS + horizon-rs |
| ZST actor collapse (lojix-cli) | done, pushed | system-assistant primary-q3y |
| Cloud-host plan slice 1 (types-exist) | done, pushed | system-assistant/04, 06, primary-a70 |
| ClaviFaber drops IdentitySetup; sshd owns host key | done | clavifaber commits |
| Terminal-cell speaks signal | designed | designer/127 |
| Cluster identity vs sshd identity | resolved (decoupled) | clavifaber, designer/139 |
| Persona daemon work | active but contract-blocked | operator-stack reports |

Every one of those is **typing what used to be implicit**. The week's
unifying move is "promote a name-based or flag-soup convention into a
typed record with a closed variant set." Wi-Fi role: was a node-name match,
now `NodeServices.tailscale: Option<TailscaleMembership>`. Cache identity:
was `is_nix_cache: bool`, now `Option<BinaryCache>`. Workload choice: was
"figure out per service," now nailed to native NixOS. Contract format:
was "wire-only, schema-mirrors text," now one type owns both.

The corollary is a workspace-wide pattern worth naming explicitly: **closed
typed records replace implicit name/flag overloading.** I'll come back to
this in §5.

### 1.2 Repo health snapshot

| Repo | Heat | Health | Standing risk |
|---|---|---|---|
| clavifaber | very hot (40+ commits, 7-day) | excellent — witness-driven | none structural; PKI design widening |
| CriomOS | hot (22 commits) | mid-refactor; clean trajectory | data-neutrality violations still in network/wifi |
| horizon-rs | active (13 commits) | strong type discipline | Node struct fan-out (43 fields), migration coherence |
| lojix-cli | cooling post-collapse | clean | crate split (P5) deferred behind merge of q3y |
| goldragon | light (6 commits) | stable | none |
| CriomOS-home | hot (compositor/UX churn) | mid-tier | profiles/min mixes 9+ concerns; flake input bloat |
| nota-codec / nota-derive | stabilising | strong | tier-0 token set explicit; numeric types deferred |
| signal-persona-* family | dirty (5 crates uncommitted) | blocked | persona lock-file cannot stabilise; mind crate NOTA coverage weakest |

Clavifaber is the reference for what a healthy repo in this stack looks
like right now. The actor count (5) matches what the actors actually
*hold* (gpg-agent sessions, yggdrasil binary invocations, certificate-
issuance pipeline state, trace recording, runtime supervision); none are
zero-sized wrappers around a single method call. The test count (7 test
files, 1109 lines) and shape (forbidden_edges.rs scans source for
constraint violations; idempotency tests assert "doing X twice ≡ doing X
once"; witness tests assert publication ≡ fs::read of the on-disk key) is
the discipline other repos can learn from.

## 2 · What's working

### 2.1 Concern separation is converging in the right places

CriomOS just split `nix.nix` (one 223-line file mixing client, builder,
cache, dispatcher) into `nix/{default,client,builder,cache,retention-agent}.nix`
gated on role-projected flags (`isNixCache`, `isDispatcher`,
`isRemoteNixBuilder`). The split is structurally clean. The same approach
applies to upcoming `infrastructure/` (per my plans 03–04).

horizon-rs's projection layer (`NodeProposal::project`) is **pure**: input
proposal → output Node with all derived fields populated. No I/O, no
wall-clock, no env reads. Tests can exercise the full projection on
synthetic clusters. This is structurally beautiful and the reason cluster
behavior can be derived rather than configured.

ClaviFaber's actor topology is **observable**: `tests/actor_topology.rs` +
`tests/forbidden_edges.rs` make the actor graph a tested artifact. If
someone adds a forbidden edge, a test fails. This is what
`skills/architectural-truth-tests.md` calls for, and clavifaber is the
clearest concrete example of it in the workspace.

### 2.2 Workspace discipline is paying off

Several skills the workspace declared months ago are now showing real
returns:

- **`skills/abstractions.md`** ("verb belongs to noun") just earned its
  keep in the lojix-cli collapse. Six "actors" couldn't name the data
  they owned, because they didn't. The collapse was therefore the right
  diagnosis — not a port to Kameo, but a deletion.
- **`skills/contract-repo.md`** is being actively edited (designer/138)
  to reflect the discovery that *contract types should own both wire and
  text derives*. The rule isn't being broken; it's being updated by
  reality. That's healthy.
- **`skills/nix-discipline.md`** §"Services are NixOS modules" (added
  this session) closes a question that would have come up again at every
  service decision. The OCI escape hatch is now a typed exception, not
  a peer option.
- **`skills/system-specialist.md`** §"Cluster Nix signing" is teeth
  every time a deploy fails — the standing diagnosis is the rule.

### 2.3 Repository boundaries are mostly correct

The Rust workspace audit found no circular dependencies and no
boundaries that obviously want to be merged or split. nota-codec and
nota-derive stay separate (proc-macro boundary). horizon-rs is a
two-member workspace (lib + cli) because that's literally what it is —
library and binary driver. clavifaber stands alone because it's a
specialized host-side tool, not a foundational library. goldragon is
data (no Cargo.toml at all) because that's what it is — the cluster
proposal source-of-truth.

The boundaries are honest. None of them is "where a refactor stopped";
all of them name a real seam.

## 3 · What's bad / shaky / wants reshaping

### 3.1 Data-neutrality has known violations and they're stuck

The audit found:

- `modules/nixos/network/headscale.nix:16` — `tailnetBaseDomain =
  "tailnet.${cluster.name}.criome"`. The string `"criome"` is the cluster
  TLD baked into a CriomOS module instead of projected from horizon.
- `modules/nixos/network/dnsmasq.nix:23` — same.
- `modules/nixos/network/wifi-eap.nix:20,26,52,75,78` — SSID literal
  `"criome"` and the connection file name embedded in a NixOS module.
- `modules/nixos/router/wifi-pki.nix:34` — error message says
  `<host>.criome`.
- `modules/nixos/router/default.nix:95` — `ssid = "criome"`.

These are the same class of violation as the just-removed `node.name ==
"prometheus"` / `node.name == "ouranos"` gates. The pattern is the same
("a network identity got hardcoded into a NixOS module that should be
horizon-neutral"), the fix shape is the same (project from horizon), and
yet the cluster-TLD literal "criome" survived the round that killed the
node-name gates. It survived because there's no obvious place to put it
yet — there is no `cluster.tld: String` field, no `Cluster::tld()` method,
no equivalent projection.

**Recommendation:** add `Cluster.tld` (newtype `ClusterTld(String)`,
default `"criome"`) to the horizon cluster record, project it into
modules that need it, and grep-fail in `checks/literal-tld-policy/` if
the string `"criome"` appears in `modules/`. This is structurally identical
to the node-name regression scan from plan 04 §P2.4.

The Wi-Fi SSID is a subtler case: it's a horizontal identity, not just a
TLD. SSID-broadcast-name is policy data that belongs in the Wi-Fi profile,
which is exactly what designer/139's `WifiAuthentication` typed enum is
for. The fix lands when Wi-Fi PKI does — same migration phase.

### 3.2 The "Node has 43 fields" question

`horizon-rs/lib/src/node.rs:27-124` defines `Node` with 43 fields after
my P1 slice 1, and slice 2 will add `placement` and `capabilities`
making it 45. Is this a problem?

Tactically: no. Every field is either input pass-through, viewpoint-only
(populated by `fill_viewpoint`), or computed via projection. There are no
"forgotten" fields, no fields that look like they should be on a
different type. The struct is the projection's output shape, and the
shape is rich because the cluster vocabulary is rich.

Structurally: yes, but not the way it first looks. The smell isn't field
count, it's **mixed scope**. A `Node` carries:

- identity (name, system, ssh_pub_key, ygg_pub_key, …)
- topology (link_local_ips, node_ip, wireguard_pub_key, …)
- role-derived booleans (is_remote_nix_builder, is_dispatcher,
  is_nix_cache, is_large_edge, …)
- capability/placement (the new fields)
- viewpoint-only collections (builder_configs, cache_urls,
  ex_nodes_ssh_pub_keys, dispatchers_ssh_pub_keys, admin_ssh_pub_keys,
  …)
- policy decisions (handle_lid_switch and friends)
- "behaves_as" / "type_is" / "computer_is" boolean bundles

Once the capability records land in slice 2 and CriomOS modules consume
them instead of the legacy `is_*` flags, the legacy flag bundle becomes
strictly redundant. A future cleanup pass can delete the entire row of
booleans (`is_remote_nix_builder`, `is_nix_cache`, `is_dispatcher`,
`is_large_edge`) once every reader has migrated. Same for the
`behaves_as` bundle once placement covers it.

**Recommendation:** add a deliberate **field-retirement phase** to
P1 slice 5 (a fifth slice in my plan, not yet planned). Once
`capabilities` is consumed by CriomOS, delete the derived flags and
clean `behaves_as` down to what's still load-bearing. The Node struct
shrinks naturally as redundancy retires.

### 3.3 The `modules/nixos/metal/default.nix` and `profiles/min/default.nix` smell

`CriomOS/modules/nixos/metal/default.nix` (~200+ lines, three undescribed
`# TODO`s) mixes firmware loading + ACPI + cpufreq + lid-switch handling +
battery management + screen-lock coordination. Five distinct concerns,
gated on different horizon flags, in one file.

`CriomOS-home/modules/home/profiles/min/default.nix` (~280+ lines) mixes
shell setup + fzf + Emacs doom init + niri keybinds + dconf theming +
screen locking + systemd user services. Nine areas in one file.

These are not the same problem nix.nix had (where one role's concern was
duplicated across multiple files). These are **profile defaults** — a
"min profile" reasonably has many things in it. The smell is that
**inside `default.nix`, the concerns aren't named or sectioned**. A reader
opening the file can't tell at a glance which line is "the screen-lock
policy" vs "the niri keybind" vs "the fzf config".

**Recommendation:** within the profile directories, split by concern
rather than by size. `modules/home/profiles/min/{shell.nix, editor.nix,
compositor.nix, theme.nix, screenlock.nix, services.nix}` — each one
small, each one easy to swap. The `default.nix` becomes an aggregator
that imports the concern files. Same shape as the nix.nix split.

For `metal/default.nix`, split into `metal/{firmware.nix, acpi.nix,
cpufreq.nix, lid.nix, battery.nix, screenlock.nix}` and let the
aggregator pull them based on horizon flags.

These splits are not urgent; they are debt that compounds slowly.

### 3.4 CriomOS-home flake input fan-out

CriomOS-home has 50+ flake inputs. The audit notes this without
analysis. The cost is concrete: every `home-manager switch` evaluates
every input's `flake.nix`. The boot-up time of a fresh evaluation grows
roughly linearly with input count. A garbage-collect of `~/.cache/nix`
followed by a switch can take 2–5 minutes longer with 50 inputs than 20.

Looking at the list: stylix, niri-flake, noctalia (compositor/theme
stack — keep), hexis (mutable config — keep), gascity / orchestrator /
codex-cli / llm-agents / annas-mcp / substack-cli (agent/CLI stack —
several plausibly stale), crane (Rust build — keep), claude-code-vsix /
visualjj-vsix (file inputs to bypass unfree gate — keep but verify they
still represent the user's actual editor preference), browser-use (used
for which workflow currently?), pi-src (which Pi work is alive today?),
chroma (in active use — keep), whisrs-src (active — keep).

**Recommendation:** an explicit input-bookkeeping pass that asks "is the
output of this input actually wired into a current homeConfiguration?"
for each of the 50. Inputs that no current `homeConfigurations.<user>`
references should be removed. The bookkeeping should be a small NixOS
test in `checks/unused-inputs/` that fails if a declared input has zero
consumers.

This is the same shape as `checks/literal-tld-policy/` above — a small
static-grep check that prevents future drift.

### 3.5 The persona contract-crate dirtiness is contagious

Five signal-persona-* crates are uncommitted (per designer-assistant/28
findings). Persona's `flake.lock` cannot stabilise to remote SHAs until
they land. Operator-side work (persona daemon, EngineManager, ManagerStore)
is contingent on contract stability. This is the chain reaction that
hits hardest in a typed-record-everywhere workspace: one crate that
doesn't compile, doesn't push, blocks everything below.

The recovery shape is mechanical: commit + push each crate. The friction
is that they're inter-dependent (one consumes another's types), so the
push order matters and the commits have to be approximately
atomic-from-the-flake-consumer's-perspective. signal-core, then
signal-persona, then the leaf crates. None of this is high-effort; it's
just sequenced.

**Recommendation:** the workspace would benefit from an explicit
"contract-crate commit train" discipline — when multiple inter-dependent
contract crates have pending work, push in dependency order with paired
commit messages so consumers know which set of pushes constitutes one
contract-version transition. Not a skill yet; could be a section in
`skills/contract-repo.md`.

### 3.6 The `signal-persona-mind` test gap

The mind crate is the largest contract crate and has many manual NOTA
impls (per designer-assistant/28). It does not yet have round-trip
NOTA tests comparable to the other relation crates. The risk is
representative: this is the contract for `persona-mind`, which is the
intended home for the work-graph that replaces `.beads/` per
`reports/designer-assistant/17` §2.2. A NOTA round-trip bug in this
crate misroutes work items at the mind-daemon boundary.

**Recommendation:** before signal-persona-mind merges, add NOTA
round-trip tests for **every record variant** (every typed message the
mind speaks). One test file per relation. Use the round-trip pattern
from nota-codec's tests as the template.

### 3.7 The "today's piece" trap

`ESSENCE.md` and recent commits have been sharpening the language: most
of the high-concept work in this workspace has a "today's piece" and an
"eventually" form. Sema-today is a redb+rkyv typed db; Sema-eventually
is "the universal medium for meaning." Criome-today is a sema-ecosystem
validator daemon; Criome-eventually is "the universal computing
paradigm." Persona-today is a small actor stack; Persona-eventually is
the full mind-state federation.

The recent ESSENCE.md commit (7d4c18c, "reframe pragmatic-vs-ideal as
scope discipline (today vs eventually); explicit guard against reading
'today's piece' as license to cut corners") names a real failure mode:
"today" can become an excuse for a stub that never grows up. The guard
is good. The actual operational discipline is harder.

Two concrete cases:

- **Sema rename** (active-repositories.md notes: "rename pending →
  `sema-db`"). The rename hasn't happened. As long as the repo is
  called `sema`, every reference to "Sema" is ambiguous (today's db or
  eventually's medium?). Until the rename lands, the workspace is
  carrying that ambiguity in every doc.
- **Mind work graph** (intended to replace `.beads/`). The intent is
  clear and documented. The actual replacement work is not visible in
  the current commit stream. `.beads/` is still the operational truth.
  This is fine as a transitional state, but the longer it sits, the
  more bd-shaped patterns calcify into the workspace's coordination.

**Recommendation:** the workspace would benefit from a small "today vs
eventually" tracking discipline. Each big concept with a today/eventually
split could carry a one-line **migration status** in its repo's
ARCHITECTURE.md: where on the path is today's piece, what's the next
concrete step toward eventually, and what would the workspace stop
doing once eventually arrives.

### 3.8 Sentinel files are growing as a pattern; should it generalise?

ClaviFaber recently added a `.disabled` sentinel file in its state
directory (operator touches it to lock clavifaber out, e.g. for HSM-backed
identity investigation). This is a new pattern in the stack and a good
one: explicit, observable, no daemon API needed to invoke it.

The same shape might generalise: a node-wide `disabled` sentinel that
lojix refuses to deploy against; a per-service sentinel that the home
manager refuses to activate; a Persona daemon sentinel that the harness
respects. The constraint would be uniform: a sentinel file in a
documented location turns off automatic activation for that scope.

**Recommendation:** if a second component reaches for the same pattern,
add a workspace skill `skills/sentinel-control.md` describing the
convention (location, file format, what "respects" means in terms of
exit codes / refusal messages). One-off uses are fine; two-off should
become discipline.

## 4 · Repository boundaries — questions

### 4.1 The Rust workspace shape is right

After auditing the dependency graph there is no merge or split I would
recommend. nota-codec/nota-derive stay separate (proc-macro boundary).
horizon-rs stays a two-member workspace. lojix-cli, clavifaber,
goldragon stay independent. The signal-persona-* family stays a
family. The persona-* family stays a family.

### 4.2 Cluster-trust runtime needs a name

Designer/139 §6 names task E as "Name the cluster-trust runtime repo."
It is the only repo creation explicitly required by the Wi-Fi PKI work.
It is blocked on naming. Candidate names off the top:

- `criome-trust` — fits the existing `criome*` naming family but
  conflates with the eventual Criome system.
- `clavifaber-trust` — implies clavifaber owns the distribution layer,
  which it doesn't (clavifaber issues per-host material; the runtime
  distributes the cluster-wide public trust).
- `signal-trust` — fits if the runtime speaks a signal contract.
- `cluster-trust` — descriptive, generic.
- `cordon` — short, evocative ("the trust cordon around the cluster"),
  but unclaimed semantically.

**Recommendation:** the runtime is a *distribution* concern. It does
not issue (clavifaber does), it does not store (each host stores its
own material), it does not authorize (Wi-Fi/EAP-TLS does). The naming
should reflect distribution. `signal-cluster-trust` matches the
`signal-*` convention and names the function. (`signal-` because it
will be a contract crate the runtime and consumers both speak.)

But this is a system-specialist decision, not mine.

### 4.3 CriomOS-pkgs is invoked in commit history but absent from active-repositories.md

`reports/0004-3flake-implemented.md` references a CriomOS / CriomOS-pkgs /
CriomOS-home three-flake architecture, but `protocols/active-repositories.md`
does not list a `CriomOS-pkgs`. Either it was folded back into one of the
other two, or it exists as an external pin nobody is actively maintaining.

**Recommendation:** confirm with the system-specialist whether
CriomOS-pkgs is alive or retired. If retired, mention it in
`active-repositories.md`'s "Retired / Cleanup Targets" section. If alive
but quiet, add it to "Adjacent Active Work."

### 4.4 `criome` (the validator daemon) needs a clearer scope today

`active-repositories.md` notes that criome's `ARCHITECTURE.md` "blends
both [today and eventually] — leans toward the eventual description;
today's piece is narrower." That's a structural ambiguity in
a load-bearing repo. Anybody reading criome's architecture today gets
the eventual vision but doesn't get a clean answer to "what does this
repo currently do."

**Recommendation:** criome's `ARCHITECTURE.md` should split into two
sections, one "Today" and one "Eventually," with the "today" section
naming exactly the operations that work today (Graph/Node/Edge/
Derivation/CompiledBinary validation; capability-token signing). The
"eventually" section gets the universal-computing-paradigm vision.
Same recommendation as §3.7.

## 5 · Module / vocabulary patterns — generalize what's working

### 5.1 "Closed typed records replace implicit name/flag overloading"

The week's biggest pattern: roles, capabilities, secrets, services,
placements all converted from "node-name says it all" or "boolean flag
in a soup" to **closed typed records with explicit variants**.

This pattern has not been named in any skill yet. It should be. A
candidate name and home: `skills/typed-records-over-flags.md`, with the
core claim:

> Any time the system asks a yes/no question of a node, ask whether the
> "yes" carries data. If it does, that question wants to be a typed
> record (`Option<T>` or sum-with-data), not a boolean. The data the
> "yes" carries is the record's payload. Code that read the boolean
> migrates to `if let Some(record) = node.field`.

Examples already in the codebase:

- `is_nix_cache: bool` → `binary_cache: Option<BinaryCache>` (in
  progress, capability.rs).
- `is_dispatcher: bool` → could carry dispatcher policy (max parallel
  jobs, retry strategy) — not yet typed.
- `is_remote_nix_builder: bool` → `build_host: Option<BuildHost>`
  (in progress).
- `behaves_as.virtual_machine: bool` → `placement: NodePlacement`
  (in progress).
- `nordvpn: bool` → `nordvpn: Option<NordVpnAccount>` carrying
  credentials reference and policy (not in progress; would be a clean
  application of the rule).
- `wifi_cert: bool` → tracked by Wi-Fi PKI work; the "yes" carries the
  certificate profile reference.

**Recommendation:** write the skill. Use it as the test that future
boolean-on-a-node fields must pass.

### 5.2 "Verb belongs to noun" applied to actors

The kameo collapse demonstrated: actors that don't carry data aren't
actors, they're methods that escaped onto a thread. Clavifaber's actors
**do** carry data (gpg-agent session state, yggdrasil binary lifecycle,
certificate-issuance pipeline state).

The implicit rule that came out of the collapse: **a real actor has
state that survives between messages and that data is the noun the
actor is named for.** A ZST actor that just routes one message variant
to one method call is a ceremonial wrapper.

This is already in `skills/abstractions.md` §"Verb belongs to noun"
but not named in `skills/actor-systems.md` or `skills/kameo.md`. The
collapsed example is a more useful witness than the abstract
formulation.

**Recommendation:** add a "ZST-actor anti-pattern" section to
`skills/actor-systems.md` (or `skills/kameo.md`) citing the lojix-cli
collapse as the worked example. The rule is: "if your actor has no
state, it doesn't want to be an actor."

### 5.3 Witness tests as architecture record

ClaviFaber's `tests/actor_topology.rs` + `tests/forbidden_edges.rs` are
the model. They make the architecture an executable artifact: if
someone adds a non-permitted edge or removes a required actor, the
test fails.

This is one concrete shape of what `skills/architectural-truth-tests.md`
calls for. It deserves wider adoption:

- horizon-rs could have a `tests/projection_purity.rs` that asserts no
  module under `lib/src/` reads the environment or filesystem.
- CriomOS could have a NixOS test that asserts the literal-name scan
  (currently a recommendation in plan 04 §P2.4 — should land).
- lojix-cli could have a `tests/network_neutrality.rs` that asserts no
  hardcoded node names appear in the request → deploy path.

**Recommendation:** make "every named architectural rule has at least
one test that fails when it's broken" a standing expectation in
`skills/architectural-truth-tests.md`. Cite the clavifaber tests as the
exemplar.

## 6 · Missing tests — concrete proposals

The system-specialist is opening capacity for more tests. Concrete
candidates with rough effort estimates:

| Test | Repo | Effort | Why |
|---|---|---|---|
| `checks/literal-tld-policy/` — grep-fail for `"criome"` in `modules/` | CriomOS | small | locks in the cluster-TLD migration once `Cluster.tld` lands |
| `checks/unused-inputs/` — fail if any flake input has zero consumers | CriomOS-home | small–medium | combats the 50+ input bloat |
| `tests/projection_purity.rs` — assert no env/fs reads in lib/src/ | horizon-rs | small | locks in the projection-is-pure rule |
| `tests/network_neutrality.rs` — assert no node-name literals in request decode | lojix-cli | small | mirrors the CriomOS regression check |
| `tests/check_host_key_material.rs` — exercise the diff verb | lojix-cli | medium | the verb is documented but not tested |
| NOTA round-trip per record variant | signal-persona-mind | medium | largest contract crate, manual impls, no equivalent tests today |
| `checks/sentinel-control/` — `.disabled` honoured by all components | workspace | medium | only if §3.8 sentinel skill lands |
| `checks/nested-containment-rejected/` | horizon-rs | small | once P1 slice 4 lands `contained_nodes` |
| Property test on Magnitude ↔ AtLeast | horizon-rs | small | the ladder pattern is load-bearing; deserves a witness |
| Wi-Fi profile assertion tests (SAN/EKU/KeyUsage structure) | clavifaber | medium | designer/139 §4.6 marks them as the deploy gate |
| Cert-revocation TODO test (negative — asserts the gap) | clavifaber | tiny | makes designer-assistant/29's flag executable |
| Pod-migration test (legacy Pod proposal → Contained placement) | horizon-rs | small | once P1 slice 2 lands |
| Closure equivalence check on nix.nix split (diagnostic only) | CriomOS | small | post-P2 sanity even if not gating |
| ClusterSecretBinding presence — every SecretReference resolves | horizon-rs | small | once the binding shape lands |
| Sentinel-on-disabled-clavifaber test | clavifaber | small | confirms the lockout path actually locks out |

The shapes worth elevating into discipline are: **literal-name scans**
(static grep tests in `checks/`), **purity assertions** (no env/fs
reads in modules that claim to be pure), **round-trip witnesses** (for
every wire-bearing type), **forbidden-edge tests** (architectural
constraints expressed as Rust tests).

## 7 · Missing constraints — what should be on record but isn't

### 7.1 Already-followed but unwritten

These are constraints the code obeys today but no document declares:

1. **Every node has typed identity.** NodeName newtype, SSH host
   pubkey, optional Yggdrasil keypair (encrypted, 0600). Not in any
   ARCHITECTURE.md.
2. **Every secret is referenced by logical name, not path.** The shape
   exists (`SecretReference { name, purpose }`) but no skill says it.
3. **Projection is pure.** No wall-clock, no filesystem, no env reads
   in horizon-rs lib/src/. Should be in `skills/architectural-truth-tests.md`
   or horizon-rs ARCHITECTURE.md.
4. **Cluster uniqueness is projection-time validation, not a schema
   record.** "At most one Headscale server" lives in horizon-rs
   validation; goldragon doesn't have a `cluster_unique_singletons`
   field. Should be in horizon-rs ARCHITECTURE.md.
5. **Sentinel files trump configuration.** ClaviFaber's `.disabled`
   sentinel beats any configured "should this run." Should be a workspace
   skill if it generalizes (§3.8).
6. **Witness order via systemd ordering.** ClaviFaber's
   sshd.service → complex-init → publication.nota chain is encoded in
   systemd `After=`/`Requires=`. Not a written rule but a hard one;
   should be in clavifaber's ARCHITECTURE.md as "witness order matters."

### 7.2 New constraints worth declaring

1. **Typed records replace flag soup.** §5.1. Skill candidate.
2. **ZST-actor anti-pattern.** §5.2. Section candidate in
   `skills/actor-systems.md` or `skills/kameo.md`.
3. **Architectural rules have failing-test witnesses.** §5.3. Section
   candidate in `skills/architectural-truth-tests.md`.
4. **Today's piece carries a migration status.** §3.7. Section
   candidate in `skills/repository-management.md` or new skill.
5. **Workload is native NixOS, not OCI.** Already added this session to
   `skills/nix-discipline.md`. Done.
6. **One contract type owns wire AND text derives.** §1.2;
   designer/138 is updating `skills/contract-repo.md`. In progress.

## 8 · Weird questions / provocations

Open-ended, deliberately under-baked. The user asked for these.

### 8.1 Should `horizon.users` be its own repo?

Goldragon currently carries both node and user proposals. They are
nearly orthogonal: users have keyboard/style/editor/textSize/pubKeys;
nodes have hardware/network/role/capabilities. The fact that they
share a `Magnitude` ladder is incidental. Splitting goldragon into
`goldragon-nodes` and `goldragon-users` (or moving users into a
`persona-identity` shape) would let user authorship operate
independently of cluster topology.

Tactically: no, not today. Goldragon is one file per cluster, and users
and nodes co-locate naturally there. The question is worth re-asking
once `persona-mind` exists and human identity becomes its concern.

### 8.2 Should there be a `criomos-checks` repo?

CriomOS has `checks/` (currently 3 NixOS tests). CriomOS-home has its
own `checks/` (2 package tests). Recommendations above add several more.
If the check count grows to 20–30, the `checks/` subtree becomes a
non-trivial maintenance surface, and the cost of building all of them
on every CI run grows. A `criomos-checks` repo (or workspace flake
output) that exists exclusively to host architectural tests would let
"is the architecture healthy?" be a separate question from "does the
deploy work?"

Tactically: not yet. Worth considering once the check count crosses
~20.

### 8.3 What if there were no node-name strings anywhere?

Continuing the data-neutrality migration to its logical conclusion: if
no module mentions `"prometheus"` or `"ouranos"` or `"goldragon"` or
`"criome"` literally anywhere, then the cluster identity is purely
projected and the modules are reusable across any cluster. The
hardcoded TLD (§3.1) is the last big violation. The Wi-Fi SSID is
another. Once both fall, CriomOS modules become genuinely
cluster-agnostic.

This isn't a stretch goal; it's the natural endpoint of work already in
flight.

### 8.4 Should beads die sooner?

`.beads/` is "transitional" per AGENTS.md. The mind work graph is the
destination. The mind graph is not visibly being built today (the
recent persona work is daemon supervision, not work-graph storage).
The risk in long transitions is that the transitional thing acquires
discipline of its own (bd labels, bd workflows, bd memories) that
becomes hard to translate later.

The question: is the work graph being built in `persona-mind` and
`signal-persona-mind` right now? If yes, when does it overlap with bd
in operational use? If not, what's the next bead's worth of mind-work-
graph implementation?

This is a designer question.

### 8.5 Could the workspace skills/ be a `repos/lore/` slice instead?

Several workspace skills (`skills/abstractions.md`, `skills/naming.md`,
`skills/jj.md`, `skills/beauty.md`, `skills/reporting.md`) are not
Persona/CriomOS-specific — they apply to any workspace using the same
agent discipline. `repos/lore/AGENTS.md` is the cross-workspace contract.
The skills with cross-workspace applicability could migrate to
`repos/lore/skills/` and be sourced from there.

Workspace-specific skills (`skills/system-specialist.md`,
`skills/system-assistant.md`, `skills/operator.md`, etc.) stay in
`primary/skills/`.

This is a small reorganisation but it would clarify the lore vs primary
boundary. Worth considering if the lore repo continues to grow.

### 8.6 Why isn't `persona-system` paused-permanent?

Designer/127 paused persona-system because terminal-cell's input gate
removed the need for focus observations. The pause is presumably
reversible — but is there any current consumer of focus events anywhere
in the planned stack? If not, persona-system might be more honestly
"on ice" or "retired pending re-discovery."

Naming the pause matters: "paused, may return" reads differently from
"retired, would need a fresh justification."

## 9 · Concrete next moves

Prioritised. The first three are zero-friction; the rest are bigger
decisions.

1. **Add `Cluster.tld` to horizon-rs**, project it, replace the
   "criome" literal in headscale.nix / dnsmasq.nix / wifi-eap.nix /
   router/. Add `checks/literal-tld-policy/`. Small commit; closes the
   biggest remaining data-neutrality violation.
2. **Add a "ZST-actor anti-pattern" section** to
   `skills/actor-systems.md` or `skills/kameo.md`. Cite the lojix-cli
   collapse. Five-minute write; locks in the discipline.
3. **Add `tests/projection_purity.rs`** to horizon-rs. Trivial test;
   makes a hard rule executable.
4. **Land `signal-persona-*` commit train** so persona's lock file can
   stabilise. Order: signal-core → signal-persona → signal-persona-auth
   → signal-persona-message / mind / system / harness / terminal. Each
   crate gets full NOTA round-trip tests before merging — especially
   `signal-persona-mind`.
5. **Split `modules/nixos/metal/default.nix`** into concern-named
   siblings. Small refactor.
6. **Split `modules/home/profiles/min/default.nix`** into concern-named
   siblings. Larger refactor; could be a separate bead.
7. **Write `skills/typed-records-over-flags.md`** (§5.1). Workspace
   skill; locks in the pattern.
8. **Name the cluster-trust runtime** (designer/139 task E). Unblocks
   Wi-Fi PKI implementation.
9. **Audit CriomOS-home flake inputs** for dead consumers. Medium
   effort; concrete savings.
10. **Land P1 slice 2** (Node + capabilities wiring) once the
    horizon.rs lock releases. My queued work.

## 10 · Summary

The stack is in better shape than it looks from inside the daily
churn. Discipline patterns are converging (typed records over flag
soup; concern separation in module trees; witness tests over
documentation prose; verb-belongs-to-noun in action). Repository
boundaries are honest. The Rust workspace has no circular deps and no
obvious mis-splits. Clavifaber is the reference for what a healthy
component looks like.

The real risks are accumulation, not catastrophe: data-neutrality
violations that survived one migration round (`"criome"` TLD literal);
profile / module files that mix nine concerns; signal-persona-* crates
that can't push because of inter-dependency choreography; "today's
piece" implementations that haven't been given their migration runways.

The fix shape for nearly all of them is the same: name the pattern,
write the constraint as an executable test, land a small refactor that
clears the violation, move on.

## Sources

- `/git/github.com/LiGoldragon/CriomOS` (modules/, checks/, docs/, recent commits)
- `/git/github.com/LiGoldragon/CriomOS-home` (modules/home/, checks/, flake.nix)
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/` (every module; post-slice-1 state)
- `/git/github.com/LiGoldragon/lojix-cli/src/` (post-kameo-collapse state)
- `/git/github.com/LiGoldragon/clavifaber/` (recent PKI shaping)
- `/git/github.com/LiGoldragon/goldragon/`, `nota-codec/`, `nota-derive/`
- `/home/li/primary/reports/{designer,designer-assistant,system-specialist,system-assistant,operator,operator-assistant}/` (recent reports)
- `/home/li/primary/skills/` (current workspace discipline)
- `ESSENCE.md`, `protocols/active-repositories.md`, `AGENTS.md`
- Recent commit logs across all of the above.
- My prior reports: 02–06 (cloud-host plan, workload decision, status).
