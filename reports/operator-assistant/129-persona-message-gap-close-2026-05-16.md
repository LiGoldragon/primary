# 129 — `persona-message` gap close (per designer/187)

Date: 2026-05-16
Role: operator-assistant
Scope: close the residual cleanup tail in `persona-message`
identified by `reports/designer/187-persona-message-gap-scan.md`:
retire env-var fallback methods, inline `MessageOriginStamper`
onto `MessageDaemonRoot`, keep constraint witnesses, verify
`from_input` parity.

## 0. What landed

Two logical commits on `main`, plus one persona flake.lock bump
per commit (so the dev-stack smoke pulls the new daemon binary).

| Repo | Commit | Change |
|---|---|---|
| `persona-message` | `b0eeb55a` | Retire env-var fallback methods: `SignalRouterSocket::from_environment`, `SignalRouterSocket::from_peer_environment`, `PeerSocketEnvironment`, `PeerSocket`, `SupervisionListener::from_environment`. Drop unused `Error::SignalRouterSocketMissing`. Remove `_osstring_marker` dead-code workaround. Align mis-named flake check (`message-daemon-applies-spawn-envelope-socket-mode` → `message-daemon-applies-configured-socket-mode`). |
| `persona` | `24d258cd` | Bump `persona-message` flake.lock for the env-var fallback retirement. |
| `persona-message` | `aa474bcc` | Inline `MessageOriginStamper` onto `MessageDaemonRoot`. Stamping methods (`stamp_request`, `origin_for_peer`, `timestamp_now`) become methods on the root actor. `MessageOriginStamper` deleted. `MessageDaemonRootInput` now carries `owner_identity` directly. Constraint witness renamed and rewritten to exercise the root directly. ARCHITECTURE.md prose updated to match reality post-/127. |
| `persona` | `bcbc79b5` | Bump `persona-message` flake.lock for the inlined stamper. |

**End-to-end witness:** `nix run .#persona-dev-stack-smoke`
passed green after each commit's flake.lock bump. The
three-daemon stack (message + router + terminal) runs the full
submission/inbox flow through the inlined-stamper root.

## 1. Commit 1 — env-var fallback retirement

`reports/designer/187-persona-message-gap-scan.md` §12.1 listed
three dead-code env-var paths on the post-/127 daemon:

| Site | What was there | Action |
|---|---|---|
| `src/router.rs:19-24` | `SignalRouterSocket::from_environment` (reads `PERSONA_MESSAGE_ROUTER_SOCKET`) plus `from_peer_environment` (delegates to `PeerSocketEnvironment`) | Deleted both methods. |
| `src/router.rs:280-296` | `PeerSocketEnvironment::from_environment` (`PERSONA_PEER_SOCKET_COUNT` + numbered peer suffixes) + `PeerSocket` private type | Deleted both types entirely. |
| `src/supervision.rs:68-76` | `SupervisionListener::from_environment` (`PERSONA_SUPERVISION_SOCKET_PATH` + `PERSONA_SUPERVISION_SOCKET_MODE`) | Deleted the method; `SupervisionListener::new` remains the only constructor. |

The audit named these "dead code on the production path but
stand as temptations" — they were neither called by the daemon
binary (which uses typed `MessageDaemonConfiguration` via
`nota-config::ConfigurationSource::from_argv`) nor by tests.
Per ESSENCE §"Backward compatibility is not a constraint", a
dead fallback path retained as ambient capability is technical
debt the new shape doesn't have to carry.

Two incidental cleanups landed in the same commit because the
deletions exposed them:

1. **`Error::SignalRouterSocketMissing` was dead** — it was
   returned only by the deleted `from_environment` constructors
   and asserted-against by an `actor_runtime_truth.rs` test that
   proves the CLI does not return it. The test stays green
   without the variant; the variant goes.
2. **`_osstring_marker` was a dead `OsString`-import workaround**
   in `src/daemon.rs:370-373` left over from a prior fixture
   reshuffle. The `OsString` import wasn't used after the
   migration; the marker function existed only to silence the
   resulting `unused` lint. With both removed, the file is
   self-consistent again.

A flake.nix mis-rename (the cargo-test selector
`message_daemon_applies_spawn_envelope_socket_mode` predates
/127's test rename to `..._configured_...`) would have failed
`nix flake check` if anyone ran the specific check by name. It
didn't get caught because the default `cargoTest` derivation
runs all tests by harness, not by name; the named-check
derivation was passing on the previous test name with no
match. Fixed in the same commit. The `ARCHITECTURE.md`
constraint-test row updated to match.

## 2. Commit 2 — inline `MessageOriginStamper` onto `MessageDaemonRoot`

### 2.1 What was the smell

`MessageOriginStamper` (per `reports/designer/187` §6 and §10
Q1) was a noun-shaped wrapper around pure behavior:

- one immutable field (`engine_owner_identity: OwnerIdentity`),
- three constructors (`from_spawn_envelope_path`,
  `from_spawn_envelope`, `from_owner_identity`),
- one public method (`stamp_request`),
- two private methods (`origin_for_peer`, `timestamp_now`).

Per `skills/abstractions.md` §"The wrong-noun trap": when a type
carries one immutable value and exposes pure methods, those
methods belong on the noun that owns the data the verbs touch.
The data the stamping methods touch is `engine_owner_identity`,
which is part of the daemon root's own state — the stamper was a
method suite parked next to the noun.

### 2.2 The new shape

`MessageDaemonRoot` now owns the stamping behavior directly:

```text
pub struct MessageDaemonRoot {
    router: SignalRouterClient,
    owner_identity: OwnerIdentity,        // was: stamper: MessageOriginStamper
    forwarded_count: u64,
}
```

`stamp_request` is now a `pub fn` on `MessageDaemonRoot`. The
private helpers `origin_for_peer` and `timestamp_now` are
private methods on the same impl block. The actor handler still
calls `self.forward(...)` which in turn calls
`self.stamp_request(...)` — identical control flow, one less
type.

`MessageDaemonRootInput` correspondingly carries
`owner_identity: OwnerIdentity` instead of
`stamper: MessageOriginStamper`. `MessageDaemon::run` builds the
input directly from `self.owner_identity`, no stamper indirection.

### 2.3 Constraint witness survival

The audit's §3 §"Witness test" named the constraint:

> The daemon derives owner ingress from the spawn envelope, not
> the CLI payload.

The pre-refactor test
`message_origin_stamper_uses_spawn_envelope_owner_identity`
read a NOTA spawn envelope file, decoded `OwnerIdentity` from
it, built a stamper via `from_spawn_envelope_path`, and asserted
the non-owner classification for a non-matching peer UID.

After /127 the daemon's production path no longer reads spawn
envelopes — the persona manager extracts `owner_identity` from
the spawn envelope and writes it into the typed
`MessageDaemonConfiguration`. The constraint splits cleanly:

- **Manager-side**: spawn envelope → owner identity field in
  configuration. Owned by the persona manager; tested there.
- **Daemon-side**: configuration owner identity → stamped
  origin. Owned by `persona-message`; tested here.

The new witness
`message_daemon_root_stamps_owner_identity_from_configuration`
builds a `MessageDaemonRoot` directly from a
`MessageDaemonRootInput` carrying a specific `OwnerIdentity`,
calls `stamp_request` with a non-matching peer UID, and asserts
`ConnectionClass::NonOwnerUser`. This is a more precise
witness: it tests the actual surface that handles inbound
stamping, with no spawn-envelope file I/O standing between the
constraint and the assertion.

`ARCHITECTURE.md`'s constraint table row updated to point at
the new test name; `flake.nix`'s named check updated symmetrically.

### 2.4 Test surface changes

| File | Change |
|---|---|
| `tests/message.rs` | Constraint witness renamed and rewritten as described above. `MessageFixture::write_spawn_envelope` and `MessageFixture::spawn_envelope_path` deleted (only used by the pre-refactor witness). Import of `MessageOriginStamper` removed; imports of `MessageDaemonRoot` + `MessageDaemonRootInput` added. |
| `tests/actor_runtime_truth.rs` | No changes needed. The actor-shape assertions (`router: SignalRouterClient,` and `forwarded_count: u64,`) still match the post-refactor root. |

The constraint witness count is the same: 17 tests pass, both
before and after the refactor (11 in `tests/message.rs`, 6 in
`tests/actor_runtime_truth.rs`).

## 3. ARCHITECTURE.md drift correction

`/127` updated the daemon's code to read typed
`MessageDaemonConfiguration` but did not update the `ARCH.md`
prose, which still described the daemon as reading
`PERSONA_SPAWN_ENVELOPE` directly. The stamper inline commit
absorbed the prose fix since the same code paragraphs name both
the configuration-vs-envelope source and the stamper:

- §1 (component description): "reads a typed
  `MessageDaemonConfiguration` record passed by argv via
  `nota-config`" replaces the prior "reads the typed
  `PERSONA_SPAWN_ENVELOPE` when present".
- §1.5 (actor topology): "typed provenance from the typed
  `MessageDaemonConfiguration`'s `owner_identity`" replaces "from
  the typed spawn envelope".
- §2 (state and ownership): the legacy "Legacy direct launches
  without `PERSONA_SPAWN_ENVELOPE` fall back to the daemon's
  current Unix user" paragraph removed; replaced by the actual
  current shape (manager builds the configuration, daemon never
  reads env vars for control-plane settings).
- §4 (invariants): "managed spawn-envelope socket mode" replaced
  with "configured socket mode from
  `MessageDaemonConfiguration`"; "Managed daemon launches read
  the typed spawn envelope before accepting message ingress"
  replaced with "The daemon reads its typed
  `MessageDaemonConfiguration` from argv before accepting
  message ingress".

This is corrective work, not new architecture — the prose now
matches what the code has been doing since `ad73f810` (the /127
migration commit).

## 4. `from_input` constructor sanity check

Per the audit's §8: `MessageDaemon::from_input` is the test-only
constructor that takes `MessageDaemonInput` (explicit fields) and
produces the same internal state as `from_configuration` (which
unpacks `MessageDaemonConfiguration`'s `WirePath` / `SocketMode`
into the runtime types).

The stamper inline did not change `MessageDaemon`'s six fields —
the stamper lived inside `MessageDaemonRoot`, which `MessageDaemon`
builds at run time, not stores. Both constructors continue to
produce six identical fields. The `from_input` test path remains
green; no parity reshuffle was needed.

## 5. Verification

| Witness | Result |
|---|---|
| `cargo test --release` in `persona-message` | 17 tests passing (11 in `tests/message.rs` + 6 in `tests/actor_runtime_truth.rs`). |
| `cargo clippy --release --all-targets` | clean. |
| `nix flake check` in `persona-message` | all named checks pass (renamed check pulls the renamed test cleanly). |
| `nix run .#persona-dev-stack-smoke` after commit 1's flake.lock bump | `persona dev stack smoke=passed`. |
| `nix run .#persona-dev-stack-smoke` after commit 2's flake.lock bump | `persona dev stack smoke=passed`. |

The dev-stack smoke is the load-bearing witness: real daemons,
real Unix sockets, full `message → router → terminal` flow.
Both bumps stayed green end-to-end.

## 6. Residual notes

- **The CLI still reads `PERSONA_MESSAGE_SOCKET`** at
  `src/command.rs:45` via `SignalMessageSocket::from_environment`.
  Per `/127` §1.2 this is explicitly out of /183 scope: the CLI's
  socket env var names the daemon's *connection target*, not a
  control-plane configuration knob. Left as-is.
- **The persona manager still sets the legacy env vars** on the
  message-daemon spawn command (`/git/github.com/LiGoldragon/persona/src/direct_process.rs:333-369`).
  The daemon ignores them; the manager's set is harmless wasted
  setup. Cleaning it up touches the manager and a separate
  `tests/direct_process.rs` fixture that scrapes those env vars
  — out of scope for this gap close.
- **One async-discipline future refactor**, named in
  `reports/designer/187` §5: `router.submit()` is sync I/O
  inside the actor handler. Acceptable for prototype scale;
  refactor to async stream when ingress throughput becomes
  visible. Not load-bearing today.

## 7. See also

- `reports/designer/187-persona-message-gap-scan.md` — the
  originating audit; this report closes §12.1 (high-priority
  cleanup tail).
- `reports/operator-assistant/127-persona-message-daemon-typed-config-migration-2026-05-16.md`
  — the prior commit that landed the typed-configuration path;
  the env-var fallbacks retired here were dead code after /127.
- `reports/operator-assistant/126-nota-config-scaffold-2026-05-16.md`
  — the `nota-config` crate that the daemon consumes for argv
  configuration decoding.
- `reports/designer/183-typed-configuration-input-pattern.md` —
  the typed-configuration framework the daemon now exercises end
  to end.
- `~/primary/skills/abstractions.md` §"The wrong-noun trap" — the
  diagnostic reading that names `MessageOriginStamper`-shaped
  pseudo-actors and points at the inline-onto-real-noun fix.
- `https://github.com/LiGoldragon/persona-message/commit/b0eeb55a`
  — env-var fallback retirement.
- `https://github.com/LiGoldragon/persona-message/commit/aa474bcc`
  — stamper inline onto root.
- `https://github.com/LiGoldragon/persona/commit/24d258cd` and
  `https://github.com/LiGoldragon/persona/commit/bcbc79b5` —
  persona flake.lock bumps proving the dev-stack smoke stayed
  green per commit.
