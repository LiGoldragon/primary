# 150 — The lojix daemon can deploy, but needs build-on-target before it can safely deploy prometheus

*The psyche chose the daemon path ("use the lojix daemon and deprecate lojix-cli now") and asked: is it possible to proceed this way, and does the daemon need a redeploy with fixes? This is the grounded, read-only answer (no builds, no deploys were run). Bottom line: the daemon's Deploy pipeline is complete and needs no redeploy for normal nodes, but deploying prometheus — a large-AI node — via the daemon as it stands would build prometheus's closure on the daemon host (ouranos) and pull the giant models there, violating Spirit `ufjd`/`0a9p`. Safe daemon deploy of a large-AI node requires a build-on-target capability the daemon does not have yet. Bead `primary-dw95`.*

## Direct answers

1. **Possible to deploy prometheus via the daemon now?** Mechanically yes, but **not safely yet.** The live `lojix 0.3.4` daemon on ouranos has the full production Deploy pipeline — `DeploymentKind::OsOnly`, `SystemAction::BootOnce` (so the live router is never `Switch`ed), and a real FlakeAuth → MaterializeHorizon → Eval → NixBuild → CopyClosure → ActivateGeneration → Gc chain, none stubbed — and it already drove a real zeus FullOS deploy from ouranos. The blocker is build location, below.

2. **Does the daemon need a redeploy with fixes?** For a normal node, **no** — 0.3.4 has the whole Deploy pipeline; every commit since is additive Test-operation code, and the `live-deploy-test-chain` branch is the VM-Test bracket, not node Deploy. For **prometheus specifically, yes** — the daemon needs a build-on-target fix (and a light redeploy of the daemon itself) so it builds prometheus's closure on prometheus, not on ouranos.

## How a daemon deploy runs

- Driven from a **local session on ouranos as `li`**: the owner socket `/run/lojix/owner.sock` is `srw-------` (0600, uid/gid-gated), so `meta-lojix` deploys must originate locally on ouranos — a remote operator has no owner entry point.
- `meta-lojix` submits a `DeployRequest`: `OsOnly`, target prometheus, `BootOnce`. BootOnce ssh-runs a PID1-owned `systemd-run` oneshot on prometheus that `bootctl set-default OLD` + `bootctl set-oneshot NEW` — reboot 1 lands NEW, reboot 2 auto-reverts. Never `Switch`. Self-healing.
- **Credentials:** attended only — the daemon has no first-class credentials (bead `primary-srmq` / nix-auth unstarted) and leans on the operator's logged-in GPG SSH agent. Fine for an attended deploy.

## The build-location gap — the reason it isn't safe for prometheus

By default the daemon uses `BuildTarget::Local` and runs `nix build nixosConfigurations.prometheus...toplevel^*` **on ouranos**. To realize prometheus's toplevel, every referenced path — including the multi-tens-of-gigabyte `.gguf` model paths — must be **present in the building store (ouranos)**, so the daemon pulls the models onto ouranos. Naming a remote `builder` does not help: it offloads to a daemon-known machine and copies the result **back into ouranos's store** regardless. There is no Spirit-`lc28` target-cache resolution — the daemon never queries prometheus's own cache.

zeus deployed cleanly precisely because zeus carries no large models; prometheus does. So the daemon's existing behavior is safe for ordinary nodes and **unsafe for large-AI nodes**.

**The suggested substituter mitigation is not trustworthy here.** Passing the cluster cache as an `ExtraSubstituter` turns the build into a *substitute* rather than a *rebuild* — but a substitute still **downloads the model NARs into ouranos's store** to realize the toplevel. It changes build-from-scratch into download, not "stays off ouranos." After two model-pull incidents this session, that is not a margin to gamble on.

## The fix: build-on-target

The daemon should gain a build-on-target mode for the Deploy pipeline: for a node whose closure must not transit the daemon host, **realize the toplevel on the target node itself** (ssh the target, `nix build` there where its models already live), then run only the copy-noop + `BootOnce` activation — the daemon coordinates, the heavy realization never touches ouranos. This is the natural home for the `lc28` substituter-resolution intent (resolve the target's own cache / build on the target) and is the **proper cutover enabler**: it is what makes the daemon safe to deploy *any* large-AI node, not just prometheus.

The fix is a small daemon code change. Redeploying the daemon itself is light and safe: the daemon binary is a normal cargo/nix build with no large closure, and it is built **on ouranos** (the host it runs on), so there is no model-pull concern for the redeploy.

(Separately, there is one pre-existing Deploy-path bug — the BootOnce crash-resume unit-name mismatch: activation creates `lojix-boot-once-<seconds>-<pid>` while the resume cursor persists `lojix-boot-once-deploy-<id>`, so a daemon crash *during* the activation window can't reconcile. It does not block first-run deploy; treat the window as not crash-resumable. Worth folding into the same daemon fix.)

## Deprecating lojix-cli — what this means for the cutover

Using the daemon for prometheus is the cutover in practice (Spirit `bsg1`, already recorded). For *this* deploy the only hard requirement is the local owner-socket session on ouranos as `li`; none of report 145's seven retirement blockers gate it — **except** that doing it safely now surfaces the build-on-target gap as the real prerequisite for large-AI nodes. The remaining full-retirement work (daemon credentials `primary-srmq`, remote operator routing onto `meta-lojix`, repointing CriomOS-home off lojix-cli, then deletion) is unchanged.

## Recommendation

1. **Implement build-on-target in the daemon** (realize the target's closure on the target; the `lc28` direction), fold in the BootOnce unit-name fix.
2. **Redeploy the daemon on ouranos** (light, no models).
3. **Then deploy prometheus via `meta-lojix` BootOnce** from a local ouranos session — the build happens on prometheus, models never leave it, the router is never `Switch`ed.

If a faster path is wanted, the only alternative I'd trust is to **build prometheus's closure on prometheus directly** and drive the daemon only for the activation — but the daemon's current pipeline does not cleanly separate "activate-only" from "build", which is exactly why build-on-target is the right fix. I am not firing any deploy until the build is guaranteed to stay on prometheus.
