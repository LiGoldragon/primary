# Zeus current green gate — blocked receipt

Time: 2026-09-26 local. Scope: immutable current-main gate only; no activation.

## Frozen authority and ownership

The real remote read returned `origin/main = 030810ed712b0d07d7e3606f4f8905e822dd2a32` at `2026-09-26 18:51:03 -0600` (`Record Flow release and access recovery limits`). This supersedes the earlier recovered `d04257a8…` CriomOS lead. That Primary revision contains access status, not a new pinned CriomOS projection; it cannot establish current Zeus generated-input hashes.

`orchestrate 'Observe.Locks'` returned lock **7359**:

```
BuildZeus31147a 31147a
/home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a
Evaluate and build authorized regenerated Zeus target through Prometheus remote builder
```

The locked worktree's immutable observed HEAD is `dfb2c89cc918b4ebec1cbcb4927400505c9c1a90` (`bootstrap-b860be: pin Piper-free Home profile`, 2026-09-26 08:20:46 -0600). It belongs to the lock holder and was not evaluated, built, or changed by this flow. This identifies **31147a** as the current source/rematerialization/evaluate-and-build owner. No competing materialization or input mutation was attempted.

Earlier identity `CriomOS d04257a8…`, Home `fed50084…`, Lojix `3fc95f0…`, and Zeus Horizon SHA-256 `46ab9e13f090e5ae7972d04cb655beb2132cc09bf57dea1ea72e903a0ce4c648` are historical leads only. They were deliberately not used as current gate inputs.

## Prometheus access gate

Existing authenticated safe access was tested once, with no state change:

```
ssh -o BatchMode=yes -o ConnectTimeout=10 prometheus.goldragon.criome \
  'printf "%s\\n" PROMETHEUS_SAFE_ACCESS_OK; hostname; id -un; command -v nix; nix --version'
```

Result (exit 255): `ssh: connect to host prometheus.goldragon.criome port 22: Connection timed out`.

This matches the current-main recovery record and the completed network diagnosis: Prometheus is unreachable from Ouranos over its existing route. No alternate route, retry, scan, network mutation, model movement, or host action was attempted. The earlier diagnosis is `flows/6fe957/reports/prometheus-network-diagnosis.md`.

## Required builds and closure witness

None of the required artifacts were evaluated or realized:

* `nixosConfigurations.target.config.system.build.toplevel`
* `homeConfigurations.li.activationPackage`
* `homeConfigurations.bird.activationPackage`

Consequently there are no current derivation paths, realization output paths, input content hashes, or closure provenance to inspect. A model-free closure conclusion cannot be made: the actual three closures do not exist as receipts for this gate. No model data was copied to Ouranos or Zeus.

The old TLS error must not be called fixed. The historical report records that a prior `tlsCertificateReference` failure came from stale materialization, while the current owned materialization/revision was not evaluated here. Therefore its current status remains unestablished, not green.

## Result and next gate

**BLOCKED — not green.** Blockers are (1) lock 7359 held by 31147a for precisely this generated-input/evaluate/build work, and (2) no authenticated Prometheus SSH access, which prevents the required Prometheus-only builds.

After a handoff or released lock and restored existing Prometheus access, the owner must freeze one immutable CriomOS/Home/Lojix source set and all four Zeus generated inputs, evaluate all three named attributes from that same projection, build serially on Prometheus, then inspect the three realized closures and package provenance for model-bearing data before a green claim. Activation remains outside this receipt.

## Direct Field delivery

Immediately before delivery, `herdr api snapshot` passively confirmed the supplied native binding: `field-sol-9ac67c`, Codex session `01a0e029-558a-7852-b5df-1919ac67c6d7`, pane `w1:p9`, `idle`, `interactive_ready: true`, and the expected Field Sol worktree. No route test or echo was sent.

Exact delivered body:

```
From Mind Astra 6fe957: Zeus current green gate is BLOCKED, not green. Real remote origin/main is 030810ed712b0d07d7e3606f4f8905e822dd2a32. Observe.Locks shows 7359 BuildZeus31147a held by 31147a for precisely Evaluate and build authorized regenerated Zeus target through Prometheus remote builder, workspace /home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a, observed HEAD dfb2c89cc918b4ebec1cbcb4927400505c9c1a90. I did no competing rematerialization/evaluation/build. Single safe SSH to prometheus.goldragon.criome timed out (exit 255), so required Prometheus-only builds are unavailable. No current Zeus toplevel/li/bird derivations or closures exist in this gate; model-free status is unestablished, and no model data moved. tlsCertificateReference is also unestablished, not fixed. Full exact receipt: /home/li/primary/flows/6fe957/witnesses/zeus-current-green-gate.md. Next gate: 31147a ownership handoff/release plus restored Prometheus access; then freeze one source/input set, serially evaluate/build all three on Prometheus and inspect each realized closure before any green claim. No activation.
```

Command and result:

```
herdr agent prompt w1:p9 <exact-body>
{"id":"cli:agent:prompt","result":{"agent":{"name":"field-sol-9ac67c","agent_status":"idle","pane_id":"w1:p9","agent_session":{"value":"01a0e029-558a-7852-b5df-1919ac67c6d7"}},"type":"agent_prompted"}}
```

Delivery grade: **Sent / `agent_prompted`**. This is transport acceptance, not a read or acknowledgment receipt.

## 2026-09-27 — authorized stale-lock takeover

Psyche Fable 8904b1 transferred the exact Zeus generated-input/evaluate/build scope to this flow, limited to stale lock 7359. The authoritative stale witness was read from the separate Fable checkout at `/home/li/wt/primary/56ae53/flows/8904b1/receipts/stale-lock-witness-7359-31147a.md`.

Before release, this flow directly observed `Observe.Locks` and retained the lock's exact path/reason above; `hm-list` showed `31147a ... STALE`; the live Herdr snapshot had no 31147a pane; and the one required own-flow probe returned:

```
Held.{ 31147a RepairRequired d2830268-991b-4b5d-8b08-26a8918e1952 } candidates=[]
```

The locked worktree was clean (`git status --porcelain=v1` had no output), so no found work needed committing. The release and replacement replies were:

```
Released.{ 7359 BuildZeus31147a 31147a [ /home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a ] «Evaluate and build authorized regenerated Zeus target through Prometheus remote builder» }
Locked.{ 7707 ZeusCurrentGreenGate 6fe957 [ /home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a ] «Own Zeus current generated-input evaluation build gate after stale lock release» }
```

This does not establish whether Prometheus has an active build. The Fable witness establishes no local process only, and Prometheus remains unreachable; no duplicate remote build has been started.

## Contemporaneous source and input freeze

At the freeze read, the three real remotes were:

* CriomOS `main`: `d04257a8efcc73842970dadd782a19300c48f84d` (2026-09-26 17:03:46 -0600).
* CriomOS-home `main`: `fed500843629c828a91fa0e06b9946b69c167898`.
* Lojix `main`: `3fc95f0cf4eaf14ff62898c4783ebbc670fdf96b`.

CriomOS `d04257a8…` locks exactly the latter Home and Lojix revisions (nar hashes `sha256-xuWhR8h+MUncU5/6uhavR5P90V0/GpdV8nG0IYVNcnI=` and `sha256-9N8/8/rzG6DweT9nMp8CrV1lI05aKSHp50yheAmEc6A=`); its `flake.lock` content SHA-256 is `6210f7a9817db334d00e3d44fa6ea01b00339e54820dff255e2e7890720978a2`.

The existing Zeus `complete-host` generated input set timestamps at `2026-09-26 15:55:56 -0600` and has these non-secret identity hashes:

```
horizon/horizon.json 46ab9e13f090e5ae7972d04cb655beb2132cc09bf57dea1ea72e903a0ce4c648
system/flake.nix     6ab1f3dc5e0f09c13e61296368a00f9115b85307b1873898d42dc877afa8a21a
deployment/flake.nix 9828d64e78630becf96bb54946c5c985cee8c4c722bf25823495e1f1b8c2f334
secrets/flake.nix    2988f46e7526cb5d6ad3d26660432ba3cad13c18a2155ecf02b42f08ac5901c9
```

The Horizon projection contains `node.machine.hardware` with 4 cores and `ThinkPadT14Gen2Intel`; the inherited missing-hardware failure therefore is not present in this materialized input. The old claimed exact error remains unconfirmed, as Fable's witness records.

The contradictory Primary remote `030810ed…` is a Primary repository revision, while `d04257a8…` is the independently read CriomOS remote `main`; they are different repositories and do not conflict.

Prometheus's one bounded authenticated SSH probe still timed out (exit 255). This is the current gate: no Nix evaluation or build was initiated, because the authorization requires Prometheus-only serial realization and remote active-build state cannot be resolved through the unavailable access path. No activation occurred.

Fable phase delivery: `herdr agent prompt w1:p8` accepted the exact release/relock and freeze report with grade **Sent / `agent_prompted`**; it is transport acceptance only.

Field Sol 9ac67c ownership/blocker delivery: `herdr agent prompt w1:p9` accepted the transferred ownership, lock 7707, source/input freeze, and Prometheus-blocker report with grade **Sent / `agent_prompted`**. The route was the already confirmed exact native session `01a0e029-558a-7852-b5df-1919ac67c6d7`, pane `w1:p9`; this is transport acceptance only.

## 2026-09-27 — Ouranos pure evaluation gate

Field Sol authorized a narrow local evaluation only. Immediately before it, `Observe.Locks` still listed lock 7707 for this flow and all four frozen generated-input hashes and timestamps above were unchanged.

The evaluation safety audit found ordinary source metadata only; the local Nix default allows IFD and has configured builders/substituters, so the evaluation explicitly overrode those unsafe defaults. The command was a read-only, offline evaluation of only the requested derivation identity:

```
nix eval --raw --read-only --offline --no-write-lock-file --no-update-lock-file \
  --option allow-import-from-derivation false --option builders '' --option max-jobs 0 \
  --override-input system path:/var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/system \
  --override-input horizon path:/var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/horizon \
  --override-input deployment path:/var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/deployment \
  --override-input secrets path:/var/lib/lojix/generated-inputs/goldragon/zeus/complete-host/secrets \
  'git+file:///home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a?rev=d04257a8efcc73842970dadd782a19300c48f84d#nixosConfigurations.target.config.system.build.toplevel.drvPath'
```

It exited **1** after 20.3 seconds. The materialized target reached derivation evaluation and stopped exactly at:

```
error: cannot build '/nix/store/glxq1xr8a5qa4zqkwrnkkzl8lafsfkka-keyd-2.6.0.drv^out' during evaluation because the option 'allow-import-from-derivation' is disabled
```

This is an IFD safety gate, not a source-defect claim. `--read-only`, offline mode, disabled IFD, no builders, and zero jobs prevented realization, remote execution, and source/model fetches. The command returned no toplevel derivation identity. Per authorization, no retry with IFD, no Home-attribute evaluation, no build, and no model-policy bypass followed. Hence the requested embedded `li`/`bird` Home projection remains unevaluated; attempting it cannot make the red toplevel result green and would add another evaluation after the explicit IFD block.

The workspace remained clean. With the narrow evaluation finished, this flow released its protected path; `Release.7707` returned `Released.{ 7707 ZeusCurrentGreenGate 6fe957 [ /home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a ] «Own Zeus current generated-input evaluation build gate after stale lock release» }`. A subsequent `Observe.Locks` no longer listed 7707.

Terminal outcome was delivered to the passively confirmed Field Sol 9ac67c (`w1:p9`, session `01a0e029-558a-7852-b5df-1919ac67c6d7`) and Psyche Fable 8904b1 (`w1:p8`, session `8904b10d-7f06-4e44-9342-3a8a2d7e17bd`). Both returned **Sent / `agent_prompted`**, transport acceptance only. The first Fable message transcribed the store path with `glx1…` instead of exact `glxq1…`; a direct correction immediately followed and was independently accepted as **Sent / `agent_prompted`**. The exact terminal evidence in this receipt is authoritative.
