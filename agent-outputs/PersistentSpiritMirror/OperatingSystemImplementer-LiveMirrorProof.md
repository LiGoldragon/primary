# Live A→B Spirit Mirror Proof on the Standing Pair — Evidence

## Scope (coordinator direction)

De-risk the sender-leg build, then prove the A→B mirror mechanism LIVE (ad-hoc,
no persistent node config, no host/router change) on the two standing prometheus
guests: create a Spirit record on `mirror-alpha` (node A, `5::7`) and confirm the
same head lands on `mirror-beta` (node B, `5::8`) over the real tap network. HOLD
persistent productionization; defer the production-data copy. Everything
reversible.

Result: **BOTH DONE.** Build is green; the mirror works end-to-end on the metal.

## 1. Sender-leg build de-risk — GREEN

Added a first-class buildable output for the shipper on a spirit feature branch
and built all three daemons on prometheus (the sole KVM/Rust builder):

- spirit `flake.nix`: new `packages.mirror-shipper-daemon` = `spirit-daemon` built
  `--features mirror-shipper` (the A→B shipper + 1-of-1 criome gate). Pushed on
  bookmark **`mirror-shipper-daemon-output`** @ `aff00c988634` (spirit main was
  `d20982c4`; main untouched). No prior flake output compiled this feature.
- Build results on prometheus (`nix build …#packages.x86_64-linux.<name>`):
  - spirit `mirror-shipper-daemon` → `BUILD_EXIT=0`, closure
    `/nix/store/w9hc2dxm1sylxy4v8myv6vivhq4rv5cn-spirit-0.21.0` (bin `spirit-daemon`).
    **Compiled clean — no fenix FOD bomb, no error** (the Scout's #1 build risk for
    bead `1e6b.5` is cleared: the shipper build is real).
  - criome `default` → exit 0, `6c7rba6…-criome-0.4.3` (criome-daemon, criome-encode-configuration).
  - mirror `default` → exit 0, `9nlk113…-mirror-0.2.0` (mirror-daemon, meta-mirror, mirror-write-configuration).

## 2. Live A→B mirror proof — SUCCESS (identical head landed on B)

Closures copied ouranos→guest over the admin-key ProxyJump (guests are tap-isolated:
reachable only through the prometheus jump; their `/nix/store` is a read-only erofs
image, so a **writable overlay** on `/dev/vdb` was mounted per guest — fully
reversible via `umount`). All daemons run ad-hoc from `/tmp/*`.

Topology proven:

```
mirror-alpha (5::7)  spirit-daemon(mirror-shipper, Gating) --gate--> criome-daemon(AutoApprove, local)
        |  Record committed locally -> gate_and_ship_head authorized by criome
        |  TCP ship  [5::7] -> [5::8]:7474  (real vmt tap network)
        v
mirror-beta  (5::8)  mirror-daemon(listen [::]:7474, store spirit:sema)
```

Observed sequence:
- B: `mirror-daemon` up on `*:7474`; `meta-mirror '(RegisterStore (spirit:sema SemaVersionedLog))'` → `(StoreRegistered spirit:sema)`; baseline `ObserveHeads` = `[(spirit None) (spirit:sema None)]`.
- A: `criome-daemon` (AutoApprove, identity `Host(mirror-alpha)`) up; `spirit-daemon` (mirror-shipper, `Gating`) up.
- A: `meta-spirit '(Configure (Default (Some (Address [|[5::8]:7474|])) (Some (Socket /tmp/criome/criome.sock)) None))'` → `(Configured …)`. (IPv6 literal encoded as NOTA pipe-text `[|…|]`; bare/bracket forms fail the codec — a confirmed gotcha.)
- A: organic working-socket `Record` → **`(RecordAccepted azwq)`**; A head advances to `(4 …) 38b6de6a1c652749fc68fca3d4320967c2f18bbb7a8dd69325125c384feecf53`.
- B: **`ObserveHeads` → `(spirit:sema (Some (4 38b6de6a1c652749fc68fca3d4320967c2f18bbb7a8dd69325125c384feecf53)))`** — the IDENTICAL digest. Mirror store grew 0→180 KB (bodies transferred; SemaVersionedLog does append-time content-address verification, so a matching digest means the real entries landed and verified).

**A head digest === B `spirit:sema` head digest = `38b6de6a1c652749fc68fca3d4320967c2f18bbb7a8dd69325125c384feecf53`.**

The criome gate is load-bearing in this path: `Gating` mode ships **only** on an
`Authorized` verdict; the head shipped, so criome (AutoApprove) authorized it. An
unarmed/denied/unreachable criome holds the head back (source: `spirit
engine.rs`/`criome_gate.rs`; proven by `spirit tests/criome_gate_1of1.rs`).

## 3. Durability (mirror level)

`/tmp` on the guests is on the persistent `/dev/vdb` (ext4), not tmpfs. Killed +
cleanly relaunched B's `mirror-daemon` (fresh pid, same on-disk store) →
`ObserveHeads` still returns `(4 38b6de6a…)`. The landed head is durable across a
daemon restart (and, being on `/dev/vdb`, across a guest reboot — only the ad-hoc
daemons would need relaunch, which is the persistent-productionization step on hold).

## Real gap discovered + fixed live (feeds productionization)

**Port 7474 must be opened on the guest firewall.** The first ship wedged in TCP
`SYN-SENT` to `[5::8]:7474`: the minimal guest firewall opens only 22 (sshd), so it
dropped the mirror's 7474 SYN (criome had already authorized — the hang was purely
the receiver firewall). Fixed live with `ip6tables -I nixos-fw 1 -p tcp --dport 7474
-j nixos-fw-accept` (and the IPv4 twin) on beta; the ship then completed instantly.
This is the concrete instance of the earlier "open 7474 on the guest/tap path" gap —
a persistent deploy must open 7474 in the mirror module's firewall on the guest
network (mirror.nix opens it on `tailscale0` only; the guests talk over the `vmt` tap).

## Live state left running (for inspection; all reversible)

- `mirror-alpha`: `/nix/store` overlay; `criome-daemon` (AutoApprove) + `spirit-daemon`
  (mirror-shipper, armed) from `/tmp/criome`, `/tmp/spirit-a`.
- `mirror-beta`: `/nix/store` overlay; `mirror-daemon` from `/tmp/mirror`; ip6tables/iptables 7474 accept rule.
- **Teardown (any time):** `pkill -f 'spirit-daemon|criome-daemon|mirror-daemon'` on the
  guests; `ip6tables -D nixos-fw …7474` + `iptables -D`; `umount /nix/store`; or simply
  reboot the guests (`systemctl restart microvm@mirror-{alpha,beta}` on prometheus) —
  overlay + `/tmp` daemons + rules are all transient; the guests return to gen-51 clean.

## What this does NOT yet cover (held for the psyche decision)

- **Persistent daemons baked into node configs** (survive guest reboot autonomously):
  needs the module/build authoring in `OperatingSystemImplementer-MirrorStandUpFindings.md`
  (new `spirit.nix`, criome enablement, mirror store-row seed + 7474 guest-path open, a
  spirit `mirror-shipper` package on spirit main). ON HOLD per coordinator.
- **Full spirit-on-B equality** (a `spirit` daemon on B whose store equals A's): the
  mirror→spirit hop is not autonomous — `Restore` currently returns `NoCheckpoint` (needs
  a checkpoint-publish + Import into a spirit-B). The mirror-level head equality above is
  the criome-authenticated A→B landing; the spirit-B re-materialization is the downstream
  feed hop.
- **Production-data copy** — deferred per coordinator. (Ready: production Spirit on
  ouranos, store `/home/li/.local/state/spirit/spirit.sema`, read-only `ObserveHead` =
  `61cef06a…`.)

## Disposition / follow-up

- spirit feature bookmark `mirror-shipper-daemon-output` @ `aff00c988634` is pushed
  (not merged to spirit main). It is the real sender-leg build surface for bead
  `1e6b.5`; land on spirit main during productionization, or discard if superseded.
- Bead `primary-1e6b.5`: sender-leg build de-risk = GREEN; live mechanism proven.
