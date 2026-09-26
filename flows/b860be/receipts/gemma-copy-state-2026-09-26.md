# Gemma copy state and disk headroom, ouranos / Prometheus

Passive observation only, 2026-09-26 00:41 CST (see date outputs below). Nothing
built, copied, deployed, submitted, or changed on either host. This is a
read-only check of the "Gemma copy over ssh first" precondition for the
Prometheus boot-once gate (da88cf handoff.md:93, log.md:17 "Gemma copy over
ssh first"; direction and rationale in `flows/da88cf/reports/prometheus-deploy-risk.md`
§5.3 and `flows/da88cf/receipts/gcroot-messenger-clj.md`: Gemma is pre-seeded
**onto ouranos, sourced from Prometheus over ssh-ng**, before Realize, so the
build does not have to stream it over nix-serve HTTP the way deployment 31
failed). Grades: **W** = witnessed this session.

## Sources for paths and hosts (W)

- `flows/da88cf/reports/prometheus-deploy-risk.md` §3 ("The two models") for
  the six store paths and their claimed validity on each host.
- `flows/da88cf/reports/prometheus-deploy-risk.md` §5.3 for the copy
  direction and command shape.
- `flows/da88cf/receipts/gcroot-messenger-clj.md` for confirmation that
  Gemma was not pre-seeded as of 2026-09-26T04:06Z UTC (the Qwen-root
  receipt) and that pre-seeding is left to the deploy owner.
- `/etc/nix/machines` on ouranos (this session): `ssh-ng://nix-ssh@prometheus.goldragon.criome`.
- `~/.ssh/config` and `/etc/hosts` on ouranos (this session): `prometheus.goldragon.criome`
  (alias `prometheus`) resolves via `/etc/hosts` to a Yggdrasil address
  (`200:ca41:...`); ssh reached it without prompting (key-based, `BatchMode=yes`).

## Store paths checked

Gemma 4 26B-A4B-it (BF16) plus its mmproj, and the three Qwen3.5-122B-A10B
shards already rooted on ouranos:

```
/nix/store/dqr9jn4rq8975lrww1dyi2yx9vihw7ln-gemma-4-26B-A4B-it-BF16-00001-of-00002.gguf   (46.5 GiB)
/nix/store/xcr75awhc1xj82m3zi8x9nzg1klspf1y-gemma-4-26B-A4B-it-BF16-00002-of-00002.gguf   (555 MiB)
/nix/store/w0gsg8nzw31psz0z58sflw29wr719r33-mmproj-F16.gguf                                (1.1 GiB)
/nix/store/cr3yl0w80abpb9mwlm8w9c90sx5w287c-Qwen3.5-122B-A10B-Q4_K_M-00001-of-00003.gguf   (10.4 MiB)
/nix/store/3dl3vi57wll2j32097crcjbxw90bq6v5-Qwen3.5-122B-A10B-Q4_K_M-00002-of-00003.gguf   (46.5 GiB)
/nix/store/24z4j1lnv614aaig28q1qi6nigx35vrc-Qwen3.5-122B-A10B-Q4_K_M-00003-of-00003.gguf   (24.7 GiB)
```

## 1. Ouranos (local, W)

`test -e` and `nix-store --query --roots` for each path:

| Path (short) | Present | Root |
|---|---|---|
| gemma …00001-of-00002 | **ABSENT** | none |
| gemma …00002-of-00002 | **ABSENT** | none |
| mmproj-F16 | **ABSENT** | none |
| Qwen …00001-of-00003 | present | `/home/li/.local/state/da88cf-gcroots/qwen-shard-1` |
| Qwen …00002-of-00003 | present | `/home/li/.local/state/da88cf-gcroots/qwen-shard-2` |
| Qwen …00003-of-00003 | present | `/home/li/.local/state/da88cf-gcroots/qwen-shard-3` |

`nix-store --query --roots` on the absent Gemma paths printed only stale
temp-root cleanup lines (Nix's own maintenance) and no root — consistent
with the paths not existing.

`df -h /nix/store` on ouranos:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  916G  811G   58G  94% /nix/store
```

`pgrep -af 'nix copy|nix-copy|nix-store --import|nix-store -i'`: no matching
process (only this session's own shell snapshot matched the grep pattern
literally, which is not a copy process). **No nix copy or import toward
Prometheus is running from ouranos right now.**

## 2. Prometheus (over ssh, read-only, W)

`ssh -o BatchMode=yes prometheus.goldragon.criome` succeeded without a
password prompt (key-based). Hostname `prometheus`, clock agrees with
ouranos to the second.

`nix path-info` and `test -e` for the three Gemma paths: all **EXIST** and
are valid on Prometheus (as the deploy-risk report already claimed).

`df -h /nix/store` on Prometheus:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  1.9T  836G 1007G  46% /nix/store
```

`pgrep -af 'nix copy|nix-copy|nix-store --import|nix-store -i|nix-serve'` on
Prometheus: only the standing `nix-serve` (starman master + 5 workers)
listening on port 80, which is the ordinary nix-serve HTTP cache daemon, not
a copy in progress. No `nix copy`/`nix-store --import` process seen.

## Semantic outcome

- **Precondition ("Gemma copied to/onto ouranos over ssh first") is NOT MET.**
  All three Gemma-family paths are absent from ouranos's store and unrooted;
  they are valid on Prometheus, which is the intended source. No pre-seed
  copy has happened since the last receipt (`gcroot-messenger-clj.md`,
  2026-09-26T04:06Z UTC) confirmed the same absence.
- **No copy is currently in progress** toward or from Prometheus, on either
  host, at the time checked (2026-09-26 00:41 CST / see `date` below).
- **Headroom:**
  - Ouranos: 58 GiB free of 916 GiB (94% used) on `/nix/store`.
  - Prometheus: 1007 GiB free of 1.9 TiB (46% used) on `/nix/store`.
- **What would block starting the copy:** ouranos's 58 GiB free is less than
  the combined Gemma payload (46.5 GiB + 555 MiB + 1.1 GiB ≈ 48.1 GiB) plus
  any margin needed for the rest of the deploy closure and Nix's own
  build/copy overhead (temp space, hashing). It fits arithmetically today
  but leaves under 10 GiB of slack afterward, which matches the risk
  report's "tight but fits" arithmetic for a pre-00:00 Realize; if
  `nix-gc.timer` fires (00:00) before the copy and Realize land, or if
  the three Qwen shard roots are removed first, that changes the arithmetic.
  Prometheus-side headroom (1007 GiB free) is not a blocker for serving as
  copy source.
- **SSH to Prometheus:** succeeded cleanly, no error.

## Command outputs

Full command transcripts (ouranos and Prometheus) are in this session's
tool output; the values above are copied from them verbatim (paths, sizes,
`df` lines, `pgrep` results, `date`).

`date` (ouranos, at start and end of the checks): `Sat Sep 26 12:41:05 AM CST 2026`
… `Sat Sep 26 12:41:27 AM CST 2026`.
`date` (Prometheus, over ssh): `Sat Sep 26 12:41:21 AM CST 2026`.
