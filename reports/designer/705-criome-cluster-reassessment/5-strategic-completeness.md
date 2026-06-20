# 705-5 — Strategic / completeness: the whole arc vs the original goal

Read-only at `origin/main` across all four repos, plus the designer branch
`origin/criome-cluster-test`, plus Spirit. The mission: step back from the code
and judge the arc against the original psyche ask — a *fully tested networked
criome cluster with a nice reusable testing interface*.

## The original ask, restated (704/0:5-19)

Six explicit requirements: (1) fully tested criome cluster, (2) *actually
networked* sandboxes — not in-process mocks, (3) *spirit gate* authenticated
end-to-end, (4) a *nice, easily-reusable* interface for testing networked
things, (5) prometheus as VM host, (6) DigitalOcean as a second substrate.

## (a) What fraction of the goal is real

Honest measure against the ask, with the load-bearing correction that several
"GREEN in VMs" claims are **branch-only, not integrated to any main**.

| Requirement | State | Evidence |
|---|---|---|
| 1 — fully tested | Partial. Single-node gate logic proven; park flow unproven; quorum/negatives absent | below |
| 2 — actually networked (cross-machine) | **Zero.** `transport.rs` is `UnixStream`-only | `criome:src/transport.rs:2,233,254` (no `TcpStream`/`TcpListener` anywhere) |
| 3 — spirit gate end-to-end | Partial — the *criome half* of the gate runs over a real socket in a VM (branch). The spirit-daemon-drives-the-gate leg is not built | 704/0:117-137; gate-arming named as remaining 704/0:261-266 |
| 4 — reusable interface | Partial, see (c) — one of three layers is real-but-branch-only; two are pre-existing-and-reused; the headline N-node generator is single-member-only | below |
| 5 — prometheus VM host | Designated, not exercised for criome (hermetic on the driver vlan only) | 704/2:120-127 |
| 6 — DigitalOcean | Unbuilt for criome (lifecycle adapter exists; no criome bring-up) | 704/2:146-154; 704/5:54-57 |

**The most important correction this reassessment surfaces:** the criome cluster
tests do **not exist on `CriomOS-test-cluster` main** (`1844197`, a CriomOS
repin). `mkCriomeClusterTest.nix` and the `criome-cluster-1of1` /
`criome-cluster-auto-approve` checks live only on `origin/criome-cluster-test`
(`003bd2c`), and that branch pins criome to the **`criome-auto-approve` branch**,
not main (`test-cluster:flake.nix:49` on that branch). So the proven artifacts
are *branch-on-branch* and a generation behind the landed Track A
(`criome 245f0441`). Nothing criome-shaped is in the every-commit check surface
of test-cluster main. This is a real integration gap, not a wording nit.

What IS genuinely real and load-bearing:
- The criome 1-of-1 gate runs as a real `criome-daemon` process, real `blst`
  BLS, real `0o600` Unix socket, on a separate guest kernel — PROOF (a)
  authorized / (b) threshold-short-rejected (`criome:src/bin/criome-cluster-witness-test.rs:225-241`).
- The criome meta socket is fully bound + served at `0o600` alongside the
  working socket (`criome:src/daemon.rs:105,129-135`); `Configure` is implemented
  (increments a `configuration_generation`, `root.rs:35,314-316`).
- All three authorization modes are in the contract (`signal-criome:src/schema/lib.rs:247-250`
  `[Quorum AutoApprove ClientApproval]`) AND wired in the criome runtime: park on
  ClientApproval (`root.rs:331-348`), `ObserveParkedAuthorizations`
  (`root.rs:224,293`), approve→Granted+publish / reject→Denied / defer→re-park
  (`root.rs:434-451`).

**My fraction estimate: ~30-35% of the *original* ask is real.** The single-host
cross-kernel gate (the smaller, near-term half) is genuinely done; the headline
half — actually-networked, cross-machine, quorum-across-peers, with the spirit
daemon driving the gate — is 0%. Requirement 2 (the defining word "networked")
is the one most squarely at zero, and it is the headline.

## (b) Sequencing: ClientApproval park VM-proof FIRST, then E1

**Recommendation: prove the ClientApproval park flow in a VM before starting E1.**
This inverts neither lane's ownership — it's a fast designer-owned confidence
win that closes an open loop, and it de-risks E1 rather than competing with it.

Reasons:
1. **The park flow is landed-but-entirely-unproven — a latent risk sitting on
   three mains right now.** The runtime is fully wired (`root.rs:331-516`) and
   the contract is complete (`meta-signal-criome:src/schema/lib.rs:70-149`), but
   **no test anywhere exercises it.** The criome witness bin covers only PROOF
   (a)/(b) (`criome-cluster-witness-test.rs:225-241`); no park/approve/reject/
   defer check exists on test-cluster main or the branch. Unproven landed code on
   `main` is the worst state — it reads as done, gets built on, and the first
   failure surfaces far downstream. A park VM-proof is the cheapest way to
   convert "believed working" into "known working."
2. **It is small and fully inside the designer lane.** The substrate already
   exists: a guest running `criome-daemon` with both sockets, the meta client
   (`CriomeMetaClient`), and the auto-approve check already drives a
   `Configure` round-trip (704/3:83-89). A park check is the same shape plus
   one extra round-trip: working-socket submit under ClientApproval → assert
   `Parked` → meta `SubmitAuthorizationApproval(slot, Approve)` → assert
   `AuthorizedObjectUpdate` publishes; a sibling `Reject`→Denied, `Defer`→re-park.
   This is the meta socket finally proven for its *real* job, not just Configure.
3. **E1 is large, multi-file, multi-session, and partly blocked on design
   decisions** (framing, sync-vs-async peer transport, per-frame BLS envelope,
   cluster-root admission ceremony) — see 704/5 and investigator 3. Starting E1
   while a wired-but-unproven feature decays on main trades a guaranteed-cheap
   win for a long, uncertain one.
4. **A park proof also forces the first integration cleanup** that E1 will
   otherwise inherit: it requires repointing the test-cluster `criome` input
   off the stale `criome-auto-approve` branch onto `main` (`245f0441`), and ideally
   landing the cluster checks onto test-cluster main. Doing that now means E1's
   3-node test builds on integrated mains, not branch-on-branch.

**Caveat the psyche should weigh:** E1 is the actual *headline* goal — "actually
networked" is the word that makes this a cluster at all. The park-first
recommendation is explicitly *first*, not *instead*. If the psyche's priority is
the headline demo over loop-closing hygiene, E1-first is defensible — but it
should be a conscious choice to leave the park flow unproven on main meanwhile.
My judgment: a half-day park proof before a multi-session E1 is the right order;
the confidence and the integration cleanup compound into E1.

## (c) The "nice reusable testing interface" — partially built, with gaps glossed

704/2 (§2, lines 56-114) describes a **3-layer interface**: MODEL (horizon-rs
typed cluster), CONTROL (lojix typed `Test` op, "Live mode gated off"), SUBSTRATE
(`mkCriomeClusterTest`, NEW). Honest scoring:

- **MODEL (horizon-rs):** real and pre-existing — reused, not built for criome.
  704/2 is honest that it "exists" (704/2:38, marked LANDED in the inventory).
- **CONTROL (lojix `Test` op):** real and pre-existing, **but its Live mode is
  stubbed off** — 704/2:39 says so plainly ("Live mode stubbed-off, not absent").
  The diagram (704/2:69) shows lojix "drives, for durable/live" — but durable and
  live are both unbuilt for criome, so lojix drives *nothing criome-shaped today*.
  The control layer is real for other components; for criome it is aspirational.
- **SUBSTRATE (`mkCriomeClusterTest`):** **branch-only, and single-member-only.**
  It exists (`test-cluster:lib/mkCriomeClusterTest.nix` on `criome-cluster-test`)
  but **`throw`s if `members > 1`** (line 53: "multi-node quorum (Stage B) is
  unbuilt"). So the "N interconnected nodes from one decl" headline (704/2:47,72)
  is a 1-node generator with a deliberate guard, honestly labelled in code but
  easy to read past in the design prose. And it is not on any main.

**Verdict: the interface is partially built — one new layer (the substrate),
branch-only, single-node — composed with two reused-but-not-criome-specialized
layers (model real, control's live path stubbed).** It is NOT vapor — there is a
real runnable generator that produces a real VM check. But "3-layer reusable
interface for testing networked things" overstates today's reality in three
ways the design prose softens: (1) the substrate is single-node, not N-node; (2)
it is branch-only, not integrated; (3) the control layer's networked (live) path
is stubbed for everything and unbuilt for criome. 704/2 is internally honest
(each gloss has a line admitting it), but a reader skimming §2's diagram would
believe more is built than is. The *interface for actually-networked testing*
specifically — the thing the psyche asked for — does not exist yet; only the
single-host cross-kernel slice does.

## (d) p43g verification in Spirit — CONFIRMED and consistent

Spirit is reachable. `(PublicTextSearch [criome owns keys])`,
`[criome quorum]`, and `[criome custody]` all return **`p43g`**:

- **Record:** `p43g`, kind **Decision**, certainty **Medium**, priority
  **Minimum**, privacy **Zero**, referents **`[criome mentci spirit]`**, domains
  `[(Security Authorization) (Security Authentication) (Engineering Architecture)]`.
- **Text (verbatim opening):** "criome owns key custody and is the authorization
  decider. A requesting component submits a content-addressed object to its local
  per-Unix-user criome — the submitter authenticated by SO_PEERCRED (2st7) — and
  criome, holding the keys (9s52), decides the verdict and signs it. The requester
  does not hold or use a request-signing key; authorization is criome's decision
  (auto-approve, client-approval via mentci, or a criome-node quorum per t00s)…"
  It explicitly folds `9s52`/`2st7`/`t00s` and corrects the old
  identities-hold-their-own-keys wording.
- **Match to the mission's p43g description:** exact. criome owns custody and
  decides; quorum = peer criome-node signing (per t00s); requester only submits
  (SO_PEERCRED). The three legitimate verdict modes named in the record
  (auto-approve / client-approval / criome-node quorum) line up 1:1 with the
  signal-criome `AuthorizationMode [Quorum AutoApprove ClientApproval]`
  (`signal-criome:src/schema/lib.rs:247-250`).
- **Consistency with landed custody docs:** consistent. criome
  `ARCHITECTURE.md:405-407` now reads "Private keypair custody is daemon-managed.
  Requesters submit typed… Criome owns the key store it uses to sign or record
  decision" — the operator's Track A custody-doc correction matches p43g (the old
  "other identities hold their own keys" wording is gone).

One observation, not a flaw: p43g is **Medium** certainty (an explicit
disambiguation of a contradiction, not a long-repeated principle). It governs a
large architectural arc (all of E1-E3 quorum, the whole key model). If the psyche
considers it settled bedrock, a certainty bump to High would better signal that
to future agents; if it is still provisional, Medium is correct. Surfaced as a
question, not a recommendation.

## Open questions for the psyche (sharpest first)

1. **Proof-first or E1-first?** My recommendation is the ClientApproval park
   VM-proof first (small, designer-lane, closes a latent-risk loop, forces the
   integration cleanup E1 will inherit), *then* E1. Confirm — or say the headline
   networked demo (E1) takes priority over loop-closing, accepting the park flow
   stays unproven on main meanwhile.
2. **Integration: should the cluster checks land on test-cluster main now?** All
   the proven criome VM work is on `origin/criome-cluster-test`, pinned to a
   criome *branch* (`criome-auto-approve`), a generation behind the landed Track A
   (`245f0441`). Repointing the input to criome main and landing the checks onto
   test-cluster main is the de-branching that makes "GREEN in VMs" true on main.
   Do this before or as part of the next move?
3. **Rework the 1-of-1 witness to the criome-node-quorum now, or after E1?** The
   current witness uses the now-corrected developer-signer-signs-evidence model
   (704/4:25, 704/5:22-24); p43g says quorum = peer criome nodes signing. Rework
   it as a small standalone step now, or fold it into the E1 3-node build?
4. **DigitalOcean teardown/cost guard scope.** 704/2:146-154 makes the idempotent
   teardown + `Drop` guard + hard max-N droplet cap *mandatory from the first
   live run*. Confirm: on-demand manual only, strict create-and-destroy, low cost
   ceiling — or is a CI soak run wanted (which changes the guard design)?
   (Secondary: bump p43g certainty Medium→High if it's settled bedrock.)
