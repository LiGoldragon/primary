# Orchestrate Edge: Locks, Dirty State, Deployment, and Wire Shape

Witnessed 2026-09-04 by subflow of flow 6329f1.
Method: `orchestrate 'Observe.Locks'`, `git diff`, `git status`, `jj op log`,
`systemctl --user status`, file reading, `grep`, `stat`. No modifications made.

---

## 1. Current Orchestrate Locks

Verbatim reply:

```
Observed.Locks.[{440 WisprAuthWitness run_wispr_live_witness [/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness] [create isolated workspace for one authorized witness]} {441 WisprEdgeProxy implement_wispr_edge_proxy [/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588] [implement offline EdgeProxy witness in isolated workspace]}]
```

Two locks held:
- Lock 440 `WisprAuthWitness` by flow `run_wispr_live_witness`, path `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness`
- Lock 441 `WisprEdgeProxy` by flow `implement_wispr_edge_proxy`, path `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588`

No locks cover any path under orchestrate, signal-orchestrate, meta-signal-orchestrate,
datomic, protos, or ethos-zero checkouts.

---

## 2. Dirty Working Copies

### 2a. orchestrate (4 files modified)

Path: `/git/github.com/LiGoldragon/orchestrate`
jj-managed: yes (.jj present, default workspace)
HEAD: detached at `e0f3bc5` (v0.25.0, "Realize durable ordinary Lock Nexus")
origin/main: `dadd537` (v0.26.0, "Port Orchestrate to WireContract 0.26")
The local HEAD is one commit behind origin/main.

File modification timestamps: all four files share epoch `1787835739` (2026-08-26 13:42:19 UTC).

#### Full diff

```diff
diff --git a/ARCHITECTURE.md b/ARCHITECTURE.md
index 63e855f..163fe7a 100644
--- a/ARCHITECTURE.md
+++ b/ARCHITECTURE.md
@@ -68,8 +68,8 @@ the socket boundaries remain generated binary Signal frames.
 
 Both clients accept exactly one concrete Datom carrier value and no flags. The
 ordinary client accepts the generated type-directed `Operation` root (`Lock`,
-`Release`, or `Observe`) and prints the typed reply's structural debug
-representation rather than defining a reply-text codec. Its canonical
+`Release`, or `Observe`) and prints the typed reply as canonical Datom text.
+Its canonical
 observation input is `Observe.Locks`.
 It has no Dotos parser or prior-operation fallback. `meta-orchestrate` accepts
 `Configure` and does the analogue on the meta socket. The component-specific
diff --git a/README.md b/README.md
index 072d972..82ec9d3 100644
--- a/README.md
+++ b/README.md
@@ -14,8 +14,7 @@ values and exchange the generated framed Signal values directly.
 
 The ordinary client accepts exactly one positional, type-directed Datom value,
 with no flags. Its generated `Operation` root selects `Lock`, `Release`, or
-`Observe`; it prints the corresponding typed reply's structural debug
-representation rather than defining a second textual contract. Set
+`Observe`; it prints the corresponding typed reply as canonical Datom text. Set
 `ORCHESTRATE_SOCKET` to select the ordinary socket. The CLI is only a Datom to
 Signal boundary: it has no old Dotos parser or compatibility grammar.
 
diff --git a/src/bin/orchestrate.rs b/src/bin/orchestrate.rs
index b6bd2ca..868735f 100644
--- a/src/bin/orchestrate.rs
+++ b/src/bin/orchestrate.rs
@@ -5,7 +5,7 @@ use std::{
     process::ExitCode,
 };
 
-use datom::DatomText;
+use datom::{DatomRoot, DatomText};
 use protos::{Realize, SourceText};
 use signal_frame_ordinary::{
     ExchangeFrameBody, ExchangeIdentifier, ExchangeLane, LaneSequence, Reply, RequestPayload,
@@ -29,7 +29,10 @@ fn run() -> Result<(), String> {
         .realize()
         .map_err(|error| format!("{error:?}"))?;
     let reply = exchange(request)?;
-    println!("{reply:?}");
+    let text = reply
+        .textualize_source()
+        .map_err(|error| format!("{error:?}"))?;
+    println!("{}", text.0);
     Ok(())
 }
 
diff --git a/tests/live_nexus.rs b/tests/live_nexus.rs
index 68c3919..18bea99 100644
--- a/tests/live_nexus.rs
+++ b/tests/live_nexus.rs
@@ -5,6 +5,13 @@ use std::{
     process::{Child, Command, Output, Stdio},
 };
 
+use datom::DatomText;
+use protos::{Realize, SourceText};
+use signal_orchestrate::{
+    FlowId, Lock, LockId, LockName, LockPath, LockPaths, LockReason, LockRejection, LockSnapshot,
+    Locks, Observation, OrchestrateReply, ReleaseRejection,
+};
+
 struct IsolatedXdg {
     state_home: PathBuf,
     runtime_directory: PathBuf,
@@ -98,6 +105,12 @@ fn reply(output: Output, binary: &str, request: &str) -> String {
         .to_owned()
 }
 
+fn datom_reply(text: String) -> OrchestrateReply {
+    DatomText::<OrchestrateReply>::from(SourceText(text))
+        .realize()
+        .expect("ordinary client emits a typed Datom reply")
+}
+
 fn stop(nexus: &mut Child) {
     nexus.kill().expect("stop Orchestrate Nexus");
     nexus.wait().expect("reap Orchestrate Nexus");
@@ -222,7 +235,7 @@ fn ordinary_cli_uses_the_generated_datom_roots_against_a_live_nexus() {
             "orchestrate",
             "Observe.Locks",
         ),
-        "Observed(Locks(LockSnapshot { locks: Locks([]) }))"
+        "Observed.Locks.[]"
     );
 
     let lock_path = temporary.path().join("cli-owned");
@@ -241,7 +254,48 @@ fn ordinary_cli_uses_the_generated_datom_roots_against_a_live_nexus() {
         "orchestrate",
         &lock_request,
     );
-    assert!(locked.starts_with("Locked(Lock { lock_id: LockId(1),"));
+    let lock = Lock {
+        lock_id: LockId(1),
+        lock_name: LockName("cli-lock".into()),
+        flow_id: FlowId("01a03eda".into()),
+        lock_paths: LockPaths(vec![LockPath(lock_path.to_string_lossy().into_owned())]),
+        lock_reason: LockReason("cli-reason".into()),
+    };
+    assert_eq!(datom_reply(locked), OrchestrateReply::Locked(lock.clone()));
+
+    let observed = reply(
+        invoke(
+            &roots,
+            ordinary_binary,
+            "ORCHESTRATE_SOCKET",
+            &roots.ordinary_socket(),
+            "Observe.Locks",
+        ),
+        "orchestrate",
+        "Observe.Locks",
+    );
+    assert_eq!(
+        datom_reply(observed),
+        OrchestrateReply::Observed(Observation::Locks(LockSnapshot {
+            locks: Locks(vec![lock.clone()]),
+        }))
+    );
+
+    let rejected = reply(
+        invoke(
+            &roots,
+            ordinary_binary,
+            "ORCHESTRATE_SOCKET",
+            &roots.ordinary_socket(),
+            &lock_request,
+        ),
+        "orchestrate",
+        &lock_request,
+    );
+    assert_eq!(
+        datom_reply(rejected),
+        OrchestrateReply::LockRejected(LockRejection::DuplicateName(lock.clone()))
+    );
 
     let released = reply(
         invoke(
@@ -254,7 +308,23 @@ fn ordinary_cli_uses_the_generated_datom_roots_against_a_live_nexus() {
         "orchestrate",
         "Release.{1}",
     );
-    assert!(released.starts_with("Released(Lock { lock_id: LockId(1),"));
+    assert_eq!(datom_reply(released), OrchestrateReply::Released(lock));
+
+    let missing = reply(
+        invoke(
+            &roots,
+            ordinary_binary,
+            "ORCHESTRATE_SOCKET",
+            &roots.ordinary_socket(),
+            "Release.{1}",
+        ),
+        "orchestrate",
+        "Release.{1}",
+    );
+    assert_eq!(
+        datom_reply(missing),
+        OrchestrateReply::ReleaseRejected(ReleaseRejection::UnknownLockId)
+    );
 
     let obsolete = invoke(
         &roots,
```

#### Reading

The dirty changes attempt to switch the ordinary CLI from Rust Debug formatting
(`println!("{reply:?}")`) to canonical Datom text (`reply.textualize_source()`),
and extend the `live_nexus` integration test to parse CLI output back through
the old-API `DatomText<OrchestrateReply>` round-trip. Documentation was updated
to say "canonical Datom text" instead of "structural debug representation".

This does not compile because `textualize_source()` does not exist on the
signal-orchestrate types at the pinned revision `6fc8c5b` (v0.17.0, old API).

#### Who made it

jj operation log for the orchestrate default workspace shows the most recent
snapshot at "1 week ago" (approximately 2026-08-28), workspace `default@`.
The E4 work was done in a separate `e4-wire-integration` workspace 5 days ago,
culminating in commit `dadd537` pushed to origin/main. Flow `01a03eda` log
records signal-orchestrate `6fc8c5b` v0.17.0 and the Lock Datom contract
generation; flow `01a04a30` E4 log records completing the E4 integration and
explicitly states "the canonical ordinary checkout's preexisting dirty patch
remains untouched; its reply-root intent was preserved in stronger generated
coverage."

**The dirty orchestrate changes are a pre-E4 draft, now superseded by the
deployed 0.26.0.**

### 2b. signal-orchestrate (4 files modified)

Path: `/git/github.com/LiGoldragon/signal-orchestrate`
jj-managed: yes (.jj present, default workspace)
HEAD: detached at `6fc8c5b` (v0.17.0, "Generate Orchestrate Lock Datom contract")
origin/main: `a597f1a` (v0.18.0, "Fix Orchestrate WireContract Nix check")
The local HEAD is two commits behind origin/main.

File modification timestamps: range from epoch `1787836166` to `1787836289`
(2026-08-26 13:49 to 13:51 UTC).

#### Full diff

```diff
diff --git a/Cargo.lock b/Cargo.lock
index c2bdbf0..9242f4f 100644
--- a/Cargo.lock
+++ b/Cargo.lock
@@ -59,8 +59,8 @@ checksum = "877a4ace8713b0bcf2a4e7eec82529c029f1d0619886d18145fea96c3ffe5c0f"
 
 [[package]]
 name = "ethos-monolith"
-version = "0.5.3"
-source = "git+https://github.com/LiGoldragon/ethos-monolith.git?rev=5fd6aa4c5cf24aff65e5b99406aa773b9cdc2640#5fd6aa4c5cf24aff65e5b99406aa773b9cdc2640"
+version = "0.5.5"
+source = "git+https://github.com/LiGoldragon/ethos-monolith.git?rev=b73d535118c2#b73d535118c23bb218719da6fc81dd37795adc6a"
 dependencies = [
  "protos",
  "syn 3.0.4",
@@ -276,7 +276,7 @@ dependencies = [
 
 [[package]]
 name = "signal-orchestrate"
-version = "0.17.0"
+version = "0.17.1"
 dependencies = [
  "datom",
  "ethos-monolith",
diff --git a/Cargo.toml b/Cargo.toml
index 27a0ce1..ea0a4c8 100644
--- a/Cargo.toml
+++ b/Cargo.toml
@@ -1,6 +1,6 @@
 [package]
 name         = "signal-orchestrate"
-version      = "0.17.0"
+version      = "0.17.1"
 edition      = "2024"
 rust-version = "1.89"
 license      = "MIT OR Apache-2.0"
@@ -21,7 +21,7 @@ protos = { git = "https://github.com/LiGoldragon/protos", rev = "3b190f9fc2c2a07
 rkyv = { version = "0.8", default-features = false, features = ["std", "bytecheck", "little_endian", "pointer_width_32", "unaligned"] }
 
 [build-dependencies]
-ethos-monolith = { git = "https://github.com/LiGoldragon/ethos-monolith.git", rev = "5fd6aa4c5cf24aff65e5b99406aa773b9cdc2640" }
+ethos-monolith = { git = "https://github.com/LiGoldragon/ethos-monolith.git", rev = "b73d535118c2" }
 
 [lints.rust]
 unsafe_code = "forbid"
diff --git a/src/generated/signal.rs b/src/generated/signal.rs
index 1c8d2ae..68b5239 100644
--- a/src/generated/signal.rs
+++ b/src/generated/signal.rs
@@ -744,3 +744,81 @@ impl ::datom::DatomTextualizing for Operation {
 pub type OrchestrateRequest = Operation;
 
 impl DatomRoot for Operation {}
+
+impl ::datom::DatomRealizing for OrchestrateReply {
+    fn realize_block(
+        scope: &mut RealizeScope<'_>,
+        block: &Block,
+    ) -> Result<Self, ::datom::DatomFault> {
+        match (block.shape, block.head()) {
+            (Shape::DottedBraced, Some(head)) if head.0 == "Locked" => Ok(Self::Locked(
+                <Lock as EthosDatomRecord>::realize_fields(scope)?,
+            )),
+            (Shape::DottedBraced, Some(head)) if head.0 == "LockRejected" => {
+                let mut values = scope.realize_body(&mut |child_scope, child| {
+                    <LockRejection as ::datom::DatomRealizing>::realize_block(child_scope, child)
+                })?;
+                if values.len() != 1 {
+                    return Err(::datom::DatomFault {
+                        problem: ::datom::DatomProblem::Position,
+                    });
+                }
+                Ok(Self::LockRejected(values.remove(0)))
+            }
+            (Shape::DottedBraced, Some(head)) if head.0 == "Released" => Ok(Self::Released(
+                <Lock as EthosDatomRecord>::realize_fields(scope)?,
+            )),
+            (Shape::DottedBare, Some(head))
+                if head.0 == "ReleaseRejected" && block.body.0 == "UnknownLockId" =>
+            {
+                Ok(Self::ReleaseRejected(ReleaseRejection::UnknownLockId))
+            }
+            (Shape::DottedBraced, Some(head)) if head.0 == "Observed.Locks" => Ok(Self::Observed(
+                Observation::Locks(<LockSnapshot as EthosDatomRecord>::realize_fields(scope)?),
+            )),
+            _ => Err(::datom::DatomFault {
+                problem: ::datom::DatomProblem::Shape,
+            }),
+        }
+    }
+}
+
+impl ::datom::DatomTextualizing for OrchestrateReply {
+    fn textualize_in(&self, scope: &mut TextualizeScope<'_>) -> Result<(), ::datom::DatomFault> {
+        match self {
+            Self::Locked(payload) => {
+                let head = Head("Locked".into());
+                scope.textualize_block(Shape::DottedBraced, Some(&head), |body| {
+                    <Lock as EthosDatomRecord>::textualize_fields(payload, body)
+                })
+            }
+            Self::LockRejected(payload) => {
+                let head = Head("LockRejected".into());
+                scope.textualize_block(Shape::DottedBraced, Some(&head), |body| {
+                    ::datom::DatomTextualizing::textualize_in(payload, body)
+                })
+            }
+            Self::Released(payload) => {
+                let head = Head("Released".into());
+                scope.textualize_block(Shape::DottedBraced, Some(&head), |body| {
+                    <Lock as EthosDatomRecord>::textualize_fields(payload, body)
+                })
+            }
+            Self::ReleaseRejected(ReleaseRejection::UnknownLockId) => {
+                let head = Head("ReleaseRejected".into());
+                scope.textualize_block(Shape::DottedBare, Some(&head), |body| {
+                    body.emit_scalar("UnknownLockId");
+                    Ok(())
+                })
+            }
+            Self::Observed(Observation::Locks(payload)) => {
+                let head = Head("Observed.Locks".into());
+                scope.textualize_block(Shape::DottedBraced, Some(&head), |body| {
+                    <LockSnapshot as EthosDatomRecord>::textualize_fields(payload, body)
+                })
+            }
+        }
+    }
+}
+
+impl DatomRoot for OrchestrateReply {}
diff --git a/tests/generated_contract.rs b/tests/generated_contract.rs
index 294c4de..c21d66c 100644
--- a/tests/generated_contract.rs
+++ b/tests/generated_contract.rs
@@ -54,6 +54,40 @@ fn approved_contract_has_its_distinct_wire_binding_and_complete_snapshots() {
     assert_eq!(replies.len(), 5);
 }
 
+#[test]
+fn generated_replies_have_one_typed_datom_text_root() {
+    let lock = lock();
+    let replies = [
+        OrchestrateReply::Locked(lock.clone()),
+        OrchestrateReply::LockRejected(LockRejection::DuplicateName(lock.clone())),
+        OrchestrateReply::Released(lock.clone()),
+        OrchestrateReply::ReleaseRejected(ReleaseRejection::UnknownLockId),
+        OrchestrateReply::Observed(Observation::Locks(LockSnapshot {
+            locks: Locks(vec![lock]),
+        })),
+    ];
+
+    let empty = OrchestrateReply::Observed(Observation::Locks(LockSnapshot {
+        locks: Locks(vec![]),
+    }))
+    .textualize_source()
+    .expect("empty observation projects");
+    assert_eq!(empty.0, "Observed.Locks.[]");
+
+    for reply in replies {
+        let source = reply
+            .clone()
+            .textualize_source()
+            .expect("reply projects as Datom");
+        assert_eq!(
+            DatomText::<OrchestrateReply>::from(source)
+                .realize()
+                .expect("reply Datom realizes"),
+            reply
+        );
+    }
+}
+
 #[test]
 fn generated_datom_request_round_trips_without_legacy_command_aliases() {
     let request = OrchestrateRequest::Lock(LockRequest {
```

#### Reading

The dirty changes attempt to:
1. Bump version from 0.17.0 to 0.17.1
2. Re-pin ethos-monolith from `5fd6aa4` (v0.5.3) to `b73d535` (v0.5.5) — an ethos-zero commit
3. Hand-write `DatomRealizing` and `DatomTextualizing` impls for `OrchestrateReply` (the reply root), using the old API (`RealizeScope`, `Block`, `Shape`, `TextualizeScope`)
4. Add `DatomRoot for OrchestrateReply`
5. Add a round-trip test proving all five reply variants via `textualize_source()` / `realize()`

#### Who made it

jj operation log shows the most recent default-workspace snapshot at "1 week ago".
The E4 work was done in a separate `e4-wire-contract` workspace 5 days ago,
culminating in `a597f1a` (v0.18.0) pushed to origin/main. Flow `01a04a30` E4
log states that signal-orchestrate 0.18.0 removes build.rs, ethos-monolith,
signal-frame, Dotos, and legacy Datom dependencies.

**The dirty signal-orchestrate changes are a pre-E4 draft, now superseded by
signal-orchestrate 0.18.0 on origin/main.**

---

## 3. meta-signal-orchestrate

### Location and state

- Path: `/git/github.com/LiGoldragon/meta-signal-orchestrate`
- Remote: `git@github.com:LiGoldragon/meta-signal-orchestrate.git`
- Local HEAD: `d4dd208` (v0.11.0, "Own Orchestrate Nexus storage configuration")
- origin/main: `5cdf35a` (v0.12.0, "Fix Meta Orchestrate WireContract Nix check")
- Working tree: clean
- jj-managed: yes

Local HEAD is 2 commits behind origin/main. The E4 version (0.12.0) at
origin/main removes build.rs, ethos-monolith, and Dotos; pins Protos `bfde3...`,
Datomic `b670...`, and Ethos-zero `2309e5b...`.

### Ethos source

File: `ethos/signal.ethos`

```
Interface.{0 1 0}
Channel.{MetaOrchestrate 2 4}
[]
{
  [Configure.Configure]
  [Configured.Configured ConfigurationRejected.ConfigurationRejected]
  []
  []
  [
    OrdinarySocketPath.String
    MetaSocketPath.String
    Configure.{OrdinarySocketPath MetaSocketPath}
    ConfigurationRefusal.[InvalidConfiguration]
    Configured.{Configure}
    ConfigurationRejected.{Configure ConfigurationRefusal}
  ]
}
```

### Generated code

- Path: `src/generated/signal.rs` (committed, verified against build.rs output)
- Generator: `ethos-monolith` (at rev `b273030ee68f`) invoked by `build.rs`
- The generated code uses Dotos traits (`DotosEncode`, `DotosDecode`, `DotosSource`) for text encoding/decoding
- Uses `signal-frame` at rev `8aa0bca` (v0.4.0, with `dotos-text` feature)
- Depends on `dotos` at rev `80c7b17`

### How `meta-orchestrate` CLI consumes it

`src/bin/meta_orchestrate.rs` (in the orchestrate repo) uses:
- `DotosSource::new(&text).parse::<Configure>()` to parse the CLI argument
- `value.to_dotos()` to format the reply
- `signal_frame::ClientFrame` for frame encoding

### Dotos usage in orchestrate and its signal crates

Every Dotos usage is in the meta (privileged) path:

| File | Line | Usage |
|------|------|-------|
| `orchestrate/Cargo.toml` | 33 | `dotos = { ... rev = "80c7b17..." }` dependency |
| `orchestrate/Cargo.toml` | 37 | `signal-frame = { ... features = ["dotos-text"] }` for meta contract |
| `orchestrate/src/bin/meta_orchestrate.rs` | 8 | `use dotos::{DotosEncode, DotosSource}` |
| `orchestrate/src/bin/meta_orchestrate.rs` | 27 | `DotosSource::new(&text).parse::<Configure>()` |
| `orchestrate/src/bin/meta_orchestrate.rs` | 34-35 | `value.to_dotos()` for reply formatting |
| `meta-signal-orchestrate/Cargo.toml` | features | `dotos-text = ["signal-frame/dotos-text"]` |
| `meta-signal-orchestrate/Cargo.toml` | deps | `dotos = { ... rev = "80c7b17..." }` |
| `meta-signal-orchestrate/src/generated/signal.rs` | throughout | `EthosValueEncoding::to_ethos_value`, `DotosEncode`, `DotosDecode`, `DotosCollection`, `Delimiter` |

**However: at origin/main, the deployed orchestrate 0.26.0 and meta-signal-orchestrate 0.12.0 have already removed all Dotos dependencies.** The local checkouts are behind remote.

---

## 4. Text Formats Inside the Orchestrate Nexus

Beyond the two CLIs, every place a text format (datom, dotos, Debug, Display) appears:

### Sema store (`src/store.rs`)

| Line | Format | Usage |
|------|--------|-------|
| 31 | `#[derive(Debug, Error)]` | `StoreError` thiserror display |
| 72 | `.to_string()` | `RecordKey::new(self.lock.lock_id.0.to_string())` - sema key, not user-visible |
| 150 | `.to_string_lossy()` | `NormalizedLockPath` path component to string - internal |
| 243 | `.display().to_string()` | Store path to sema engine open string - internal |

No Datom/Dotos text is used in the store. The store exchanges typed
`OrchestrateRequest` / `OrchestrateReply` / `MetaOrchestrateRequest` /
`MetaOrchestrateReply` Rust values. Sema records are rkyv-serialized
`StoredLock`, `StoredConfiguration`, `StoredAllocator` structs.

### Transport (`src/transport.rs`)

| Line | Format | Usage |
|------|--------|-------|
| 50 | `println!("orchestrate-nexus ready")` | Readiness line, not a wire format |
| 387 | `#[derive(Debug, thiserror::Error)]` | `TransportError` display |
| 413 | `#[error("store failed: {0}")]` | Error display |

No Datom/Dotos text. The transport reads and writes length-prefixed rkyv-encoded
Signal frames. Typed values flow through `replies_from_ordinary_request` /
`replies_from_meta_request` which call `store.ordinary(request)` /
`store.meta(request)` and wrap the results in `SubReply::Ok(value)`.

### Preflight binary (`src/bin/orchestrate_upgrade_preflight.rs`)

| Line | Format | Usage |
|------|--------|-------|
| 13 | `println!("active legacy PathLock rows: {}", count)` | Human-readable status line |
| 20 | `eprintln!("orchestrate-upgrade-preflight: {error}")` | Error message |

### Ordinary domain (`src/ordinary.rs`)

No text formatting at all. Pure trait definitions for `Locks`, `Releases`, `Observes`.

### Tests (`tests/ordinary_lock_contract.rs`)

| Line | Format | Usage |
|------|--------|-------|
| 79 | `{other:?}` | `panic!("expected Locked reply, found {other:?}")` - test assertion |

Tests construct and compare typed values; no text format dependency.

### Tests (`tests/live_nexus.rs`) — committed version

The committed version asserts Debug output from the CLI:
- Line 225: `"Observed(Locks(LockSnapshot { locks: Locks([]) }))"`
- Line 244: `locked.starts_with("Locked(Lock { lock_id: LockId(1),")`
- Line 257: `released.starts_with("Released(Lock { lock_id: LockId(1),")`

The dirty version replaces these with typed Datom round-trips.

**In the deployed 0.26.0, the live_nexus test asserts canonical Datom text output:**
`"Observed.Locks.[]"`, `"Locked.$lock"`, `"Released.$lock"` (confirmed from the
CriomOS-home orchestrate-service-path check).

---

## 5. Deployment

### Nix flake

The orchestrate repo flake (`flake.nix`) has three inputs:
- `nixpkgs` (nixpkgs-unstable)
- `flake-utils`
- `rust-build` (LiGoldragon/rust-build)

Protos and datomic are **not** flake inputs; they are resolved by Cargo via git
pins in `Cargo.toml`. The Nix build uses `craneLib.buildPackage` from
`rust-build`, which delegates to Cargo. No `ETHOS_PROTOS_MAP` or
`ETHOS_DATOMIC_MAP` env vars are needed because orchestrate does not run
ethos-zero at build time.

The flake exposes:
- `packages.default` (all 4 binaries)
- `apps.default` (orchestrate CLI)
- `apps.nexus` (orchestrate-nexus daemon)
- `apps.meta` (meta-orchestrate CLI)
- 7 checks: build, test, live-nexus, ordinary-lock-contract, test-doc, doc, fmt, clippy

### CriomOS / CriomOS-home deployment

CriomOS (`/git/github.com/LiGoldragon/CriomOS/flake.nix`):
- Input: `orchestrate.url = "github:LiGoldragon/orchestrate/dadd537bbd2ed2ffc5260fffc5735f9f020cc774"` (v0.26.0)
- Override: `criomos-home.inputs.orchestrate.follows = "orchestrate"`

CriomOS-home (`/git/github.com/LiGoldragon/CriomOS-home/flake.nix`):
- Own input: `orchestrate.url = "github:LiGoldragon/orchestrate/e0f3bc5..."` (v0.25.0)
- Effective input: overridden by CriomOS to `dadd537` (v0.26.0)

Module: `CriomOS-home/modules/home/profiles/min/orchestrate.nix`
- Creates wrappers that set `ORCHESTRATE_SOCKET` and `ORCHESTRATE_META_SOCKET`
  to `${XDG_RUNTIME_DIR}/orchestrate-nexus/{orchestrate,meta-orchestrate}.sock`
- Defines `systemd.user.services.orchestrate-nexus`:
  - `ExecStart = "${orchestratePackage}/bin/orchestrate-nexus"`
  - `StateDirectory = "orchestrate-nexus"` (durable sema store under `~/.local/state/orchestrate-nexus/`)
  - `RuntimeDirectory = "orchestrate-nexus"` (sockets under `$XDG_RUNTIME_DIR/orchestrate-nexus/`)
  - `Restart = "on-failure"`, enabled via `default.target`

Two Nix checks verify the deployment:
- `orchestrate-wrapper-fallback`: tests socket-path fallback wiring
- `orchestrate-service-path`: starts the nexus, exercises Lock/Observe/Release/Configure round-trips through the CLI wrappers, and asserts canonical Datom text output

### Running service

```
orchestrate-nexus.service - Orchestrate Nexus path-reservation service
  Active: active (running) since Sat 2026-08-29 06:37:25 CEST; 5 days ago
  Main PID: 2052947
  Binary: /nix/store/pbjprrhnas2vijypwz87zrnzla92f8d5-orchestrate-0.26.0/bin/orchestrate-nexus
```

Socket paths:
- Ordinary: `/run/user/1001/orchestrate-nexus/orchestrate.sock`
- Meta: `/run/user/1001/orchestrate-nexus/meta-orchestrate.sock`

### How a new revision would be rolled out

1. Push the orchestrate commit to GitHub
2. Update the orchestrate flake input rev in CriomOS's `flake.nix`
3. Rebuild the NixOS/home-manager configuration (the CriomOS `follows` override
   carries the pin into CriomOS-home automatically)
4. `systemctl --user restart orchestrate-nexus`

No Lojix is involved; it is a pure flake-input-bump deployment.

### ethos-zero Nix and ETHOS env vars

The ethos-zero flake (`/git/github.com/LiGoldragon/ethos-zero/flake.nix`) has
two additional inputs:
- `protos-map`: `github:LiGoldragon/protos/2f605fd...`
- `datomic-map`: `github:LiGoldragon/datomic/4baeaac...`

These supply the env vars consumed by ethos-zero tests:
- `ETHOS_PROTOS_MAP = "${protos-map}/protos.ethos"`
- `ETHOS_DATOMIC_MAP = "${datomic-map}/datomic.ethos"`
- `ETHOS_PROTOS_RUST = "${protos-map}/src/lib.rs"`
- `ETHOS_DATOMIC_RUST = "${datomic-map}/src/lib.rs"`
- `ETHOS_PROTOS_CRATE = "${protos-map}"`
- `ETHOS_DATOMIC_CRATE = "${datomic-map}"`

These point to the Protos and Datomic Nix store paths, letting ethos-zero tests
read the real `.ethos` map files and Rust source for structural comparison.

---

## 6. signal-frame Crate

### Path and versions

Path: `/git/github.com/LiGoldragon/signal-frame`
HEAD: detached at `d61ebf2`
Crate version: `signal-frame` v0.4.0

Orchestrate uses two different signal-frame revisions:
- Ordinary contract: rev `000d866` ("Allow shared Signal reply payload variants")
  via `signal-frame-ordinary` (renamed import in `orchestrate/Cargo.toml`)
- Meta contract: rev `8aa0bca` ("propagate strict archive bounds through channel roots")
  via `signal-frame` (with `dotos-text` feature)

There are 4 commits between them: `8aa0bca` -> `80f70d9` -> `302f713` -> `a8a1c28` -> `000d866`.

signal-orchestrate pins `000d866` (ordinary); meta-signal-orchestrate pins `8aa0bca` (meta).

**In the deployed orchestrate 0.26.0, neither `signal-frame` nor `signal-frame-ordinary`
appear as direct dependencies.** The frame types are re-exported from the signal
crates themselves (signal-orchestrate 0.18.0 and meta-signal-orchestrate 0.12.0
each own their own `Frame`, `FrameBody`, `SignalFrameCodec`).

### Type definitions (at HEAD, applicable to both revisions)

#### ExchangeFrameBody (`src/frame.rs:93`)

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum ExchangeFrameBody<RequestPayload, ReplyPayload> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request {
        exchange: ExchangeIdentifier,
        request: Request<RequestPayload>,
    },
    Reply {
        exchange: ExchangeIdentifier,
        reply: Reply<ReplyPayload>,
    },
}
```

#### Reply (`src/reply.rs:37`)

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum Reply<ReplyPayload> {
    Accepted {
        outcome: AcceptedOutcome,
        per_operation: NonEmpty<SubReply<ReplyPayload>>,
    },
    Rejected { reason: RequestRejectionReason },
}
```

#### SubReply (`src/reply.rs:202`)

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub enum SubReply<ReplyPayload> {
    Ok(ReplyPayload),
    Invalidated,
    Failed {
        reason: OperationFailureReason,
        detail: Option<ReplyPayload>,
    },
    Skipped,
}
```

### Wire stability

The signal-frame types (`ExchangeFrameBody`, `Reply`, `SubReply`) are generic
over `RequestPayload` and `ReplyPayload`. They are rkyv-serialized. The wire
shape is determined by:
1. The frame envelope types above (stable across signal-frame revisions used)
2. The concrete payload types generated by each signal contract crate

In the deployed 0.26.0, the signal crates generate their own `Frame` and
`FrameBody` types that wrap the rkyv payload directly, rather than using
signal-frame's `ExchangeFrameBody`. The new frame shape in signal-orchestrate
0.18.0 is:

```rust
pub struct Frame {
    pub channel_contract_id: ...,
    pub channel_wire_revision: ...,
    pub protocol_version: ...,
    pub body: FrameBody,
}

pub enum FrameBody {
    Request(Request),
    Reply(Reply),
    Refusal(Refusal),
}
```

This is a **different wire format** from the old `ExchangeFrameBody`-based
frames. The E4 wire revision was bumped (channel 1 rev 5 -> 1 rev 6, channel 2
rev 4 -> 2 rev 5) and the Nexus was rebuilt. The old signal-frame
`ExchangeFrameBody` types are no longer used in the deployed system.

---

## Sources

- `/git/github.com/LiGoldragon/orchestrate` -- HEAD `e0f3bc5`, origin/main `dadd537`, dirty working copy, `src/`, `tests/`, `Cargo.toml`, `flake.nix`, `flake.lock`
- `/git/github.com/LiGoldragon/signal-orchestrate` -- HEAD `6fc8c5b`, origin/main `a597f1a`, dirty working copy, `Cargo.toml`, `src/generated/signal.rs`, `tests/`
- `/git/github.com/LiGoldragon/meta-signal-orchestrate` -- HEAD `d4dd208`, origin/main `5cdf35a`, clean, `Cargo.toml`, `build.rs`, `ethos/signal.ethos`, `src/generated/signal.rs`, `src/lib.rs`
- `/git/github.com/LiGoldragon/signal-frame` -- HEAD `d61ebf2`, `src/frame.rs`, `src/reply.rs`, `Cargo.toml`
- `/git/github.com/LiGoldragon/ethos-zero` -- `flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`, `modules/home/profiles/min/orchestrate.nix`, `checks/orchestrate-service-path/default.nix`, `checks/orchestrate-wrapper-fallback/default.nix`
- `orchestrate 'Observe.Locks'` live output
- `systemctl --user status orchestrate-nexus` live output
- `/home/li/primary/flows/01a04a30/log.md`, `/home/li/primary/flows/01a03eda/log.md`
- jj operation logs for orchestrate and signal-orchestrate default workspaces
