# 7 — adversarial verification + completeness critique

Four skeptics, each tasked to **refute** a load-bearing thesis by re-reading the
source, plus a completeness critic. The completeness pass surfaced the decisive
workspace-relative evidence the six in-cloud dimensions missed — it materially
sharpens the verdict, so it is reproduced in full.

## Verification verdicts (one line each + what was trimmed)

| Thesis | Verdict | What survived / what was trimmed |
|---|---|---|
| **T1** — zero kameo/actors in BOTH runtimes; both std::thread+Mutex / sync engine-traits | **confirmed** | Survived every axis: grep, Cargo.lock transitive closure, and `git -S kameo --all` (kameo never existed in any commit). The only "Actor" tokens are dead emitted `ActorStartFailure`/`on_start` hooks with no callers. Two precision fixes: schema path is **single-threaded serial, NOT thread-per-connection** (the cited `thread::spawn` is in the unused `BoundedWorkers`); in-code "serve connections concurrently" comments **overstate** the provably-serial spine. |
| **T2** — §"Actor Shape" was NEVER implemented; stale aspiration; "workspace's most explicit unfulfilled mandate" | **partial** | Core (never implemented, contradicts same-repo code, frozen since birth) confirmed. Trimmed: "only `ba35849`" is imprecise (**two** birth commits `ba35849`+`db5dc5c`); "MOST explicit" is an **unverified superlative** (report-35 shows zero-actor is workspace-wide) — it is *a* maximally-concrete unfulfilled mandate. |
| **T3** — a slow Cloudflare call blocks the listener (global lock held across IO + serial accept), violating ARCHITECTURE.md | **confirmed** | Both mechanisms true and compounding; no timeout anywhere; worst case = unbounded stall of both sockets. Sole caveat: requires a request that reaches live IO (which the thesis premises). |
| **T4** — sync/no-actor shape is INHERITED from the substrate; cloud can't be actor-native alone (but COULD host actors behind the listener) | **partial** | SPINE-inheritance and "could host actors behind the listener" confirmed. Trimmed: the **actor-TREE absence is cloud's CHOICE, not inherited**; and the inheritance argument applies **only to the schema path** — the production runtime is hand-written and bypasses the substrate entirely. |

Net: all four theses survive on their load-bearing points. The trims **strengthen**
the divergence reading (the actorlessness is more a choice and less a constraint than
"inherited" implied), and remove two over-claims (the provenance and the
superlative).

## Completeness critique — the workspace-relative evidence (verbatim substance)

The six dimensions answered "is cloud's sync shape a reason or a divergence?" almost
entirely *inside* cloud, and so missed the evidence that most decisively settles it.
Findings ordered by materiality.

### MISS 1 — the workspace is BIFURCATED, and cloud sits on the wrong side of its own mandate

A per-component kameo census shows the workspace runs **two parallel substrate
stacks**, not one uniform sync stack:
- **Actor stack (kameo 0.20 + tokio):** `nexus` (`impl Actor`/`ActorRef` in
  `nexus/src/daemon.rs`, `connection.rs`, `listener.rs`) and **`criome`** — a full
  actor-per-concern tree under
  `criome/src/actors/{root,store,registry,signer,verifier,authorization,subscription}.rs`.
- **Sync triad-runtime stack (zero kameo/tokio):** `cloud`, `spirit`, `lojix`,
  `domain-criome`.

This is the single most material omission. cloud's §"Actor Shape" (one actor per
concern, listener-non-blocking) is **almost verbatim the realized `criome` pattern**
— `criome/src/actors/` is living proof that actor-per-concern is **buildable in this
workspace TODAY with kameo 0.20**, on the same domain. So the mandate is neither
stale-because-impossible nor abstract aspiration: **it is implemented next door.**
The correct framing is not "cloud chose a consistent sync realization" but **"the
workspace runs two substrate stacks, and cloud was placed on the sync stack while
authoring an actor mandate copied from the kameo stack."** The "consistent" verdict
holds only *within* the sync sub-stack; against the whole workspace, cloud is a
documented self-contradiction adjacent to a working counter-example.

### MISS 2 — cloud has a structural TWIN (domain-criome); the divergence is two daemons wide on one domain

`domain-criome` (cloud's named sibling — `ARCHITECTURE.md:26`) is an **exact
actorless template match**: same file set (`daemon.rs`, `daemon_command.rs`,
`client.rs`, `frame_io.rs`, `schema/`), same legacy `thread::spawn`-per-listener over
`Arc<Mutex<Store>>` (`domain-criome/src/daemon.rs:37,40,65,80,170`), same
schema-engine track. Implications:
- cloud is **not an isolated outlier** — it inherits a shared hand-written daemon
  template, so any fix (provider actors behind the spine; dropping the coarse
  `Arc<Mutex<Store>>`) is a **template-level decision affecting domain-criome too**,
  not a cloud-local patch.
- The criome domain therefore runs **THREE daemons side by side**: `criome` (full
  kameo actor tree) + `cloud` (sync) + `domain-criome` (sync). The real question is
  "**why does one domain mix both substrates?**" — which only the workspace-level
  audit can adjudicate.

### MISS 3 — tests encode an actor expectation in their NAMES (fossil of abandoned intent)

`tests/runtime.rs:499` is literally named
**`cloudflare_record_observation_uses_provider_actor_and_caches_last_known_state`** —
yet the body (`:500-535`) exercises only `store.last_known_records(...)`, and the
"cache" is a plain `Mutex<Vec<CachedRecordListing>>` field (`lib.rs:536`, set via
`replace_last_known_records` at `lib.rs:964`). **The test name claims a "provider
actor"; no actor exists.** This is the strongest single piece of evidence that the
actor design was **active intent abandoned mid-flight**, not idle aspiration — the
author named the behavior after the mandated actor and then implemented it as a mutex
field. Separately: **no cloud test exercises concurrent connections** — every
daemon-socket test (`tests/runtime.rs:784`, `tests/schema_daemon.rs:87`) drives one
client serially, so the serialization / head-of-line-blocking hazard is **completely
untested**; nothing in the suite would fail if the blocking got worse.

### MISS 4 — secret-handle provenance conflict

Two independent credential paths both write `CF_API_TOKEN` and **conflict**:
1. Rust side: `ProcessRunner::run` sets `.env("CF_API_TOKEN", token.as_str())` on the
   flarectl `Command` (`cloudflare_cli.rs:18,48-50`), `token` from
   `EnvironmentCredentialSource` reading the `CredentialHandle` env var
   (`cloudflare.rs:52-55`).
2. Deploy side: the flake wraps flarectl with a **gopass** `--run` doing
   `CF_API_TOKEN=$(gopass show -o cloudflare/api-token); export CF_API_TOKEN` at
   wrapped-binary startup (`flake.nix:48-56`).

In production both fire on every provider call; which value wins is order-dependent
(outer `Command` env vs. inner wrapper-script export) and undocumented. The
in-process `Token`/`CredentialHandle` Rust plumbing may be **dead in production**
(gopass supplies the real secret), making `EnvironmentCredentialSource`/`Token`
possibly vestigial for the live flarectl runtime — while the `HttpApi` path that
*does* use the Rust `Token` is the unwired `production_http()`. (No secret values
exposed; mechanism only.)

### MISS 5 — named concerns map to already-partly-modeled contract types, not greenfield actors

The contract already carries the seams:
- `signal-cloud/src/lib.rs:318` defines `UnsupportedReason::ProviderRateLimited`
  (mirrored in emitted `signal-cloud/src/schema/lib.rs:295`) — currently **unused**
  (no emitter of it in cloud src). So `RateLimitGate` is **not greenfield**; the
  reply variant exists and is un-wired — stronger "abandoned intent" evidence than
  "never started."
- `RemoteOperationTracker`'s "last known state" is realized as the
  `last_known_records`/`last_known_zones` mutex fields (`lib.rs:535-536`).

The concerns the mandate names are **half-present as data, missing as actors** — the
natural actor-extraction boundaries, and the exact CommandPool/timeout targets the
remedy points at.

### MISS 6 — schema path is single-threaded SERIAL, not "thread-per-connection"

Confirmed against `triad-runtime/src/daemon.rs:368-380`: `try_serve_next_stream`
calls `handle_stream(...)` **inline on the accept thread**; `BoundedWorkers` is
exported at `lib.rs:46` but has **zero callers** in triad-runtime, the emitter, or
cloud. So the realized schema daemon is **single-threaded, strictly serial**. The
"authorized BoundedWorkers thread-per-connection shape would mitigate axis 2"
remediation describes an **unrealized** primitive: the bounded-concurrency intent
(`k6w1`) is recorded but **wired NOWHERE in the entire triad stack** — as un-realized
as the actors.

### MISS 7 — CLI client path is correctly sync (scopes the actor question)

The CLI (`src/bin/cloud.rs` → `client::Client::run_from_environment`,
`src/client.rs:56` `UnixStream::connect` → one request → reply → exit) is a
synchronous one-shot with no concurrency need — actors here would be wrong. The actor
question scopes to the **daemon-side provider/store concerns only**;
`tests/runtime.rs:825`
(`runtime_slice_does_not_reintroduce_signal_core_or_provider_access_in_cli`) already
fences the CLI off from provider access (consistent with the triad rule that the CLI
is the daemon's first client, not a runtime root).

## Net effect on the verdict

The four theses survive, but the headline "unblessed-but-consistent realization" is
**too generous** because the in-cloud dimensions never looked sideways. With the
census added: (a) actor-per-concern is **proven buildable here** (`criome`); (b)
cloud's mandate is **a copy of the working kameo pattern placed on the sync stack**;
(c) the abandonment is **evidenced in test names and unused contract variants**, not
merely absent code; (d) the bounded-concurrency fallback the remedy leans on is
**itself unrealized everywhere**. The sharper open question is not "did cloud
diverge" (it did, against a live counter-example) but **"why does the criome domain
straddle both substrates, and is cloud/domain-criome's placement on the sync stack a
deliberate decision or an unblessed default?"** — which requires a cloud-or-domain
Spirit record that, per dimension 3, **does not exist**.

## Cross-references for the orchestrator

`cloud/tests/runtime.rs:499` (actor-named test, mutex body) ·
`cloud/flake.nix:48-56` (gopass `CF_API_TOKEN`) ·
`cloud/src/cloudflare_cli.rs:46-50` (Rust-side `CF_API_TOKEN` conflict) ·
`triad-runtime/src/daemon.rs:368-380` + `triad-runtime/src/workers.rs:1-50`
(BoundedWorkers exported, zero callers → serial) ·
`criome/src/actors/` (working actor-per-concern counter-example) ·
`domain-criome/src/daemon.rs:37,40` (cloud's actorless twin) ·
`signal-cloud/src/lib.rs:318` (`ProviderRateLimited`, defined-unused).
