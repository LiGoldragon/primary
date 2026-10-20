# Monitoring agent and store memory, measured on Ouranos

Host: Ouranos (laptop), 14 CPUs, 31.5 GiB RAM. Date: 2026-10-16.
Binaries: Nix cache only (`nix build --dry-run` showed "will be fetched" for each; nothing compiled locally).
Scratch: `/tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/mon` (data deleted after runs).

## Method

- Each process started alone from its store path, 3 s warm-up, then sampled once per second for 90 s.
  Each sample sums VmRSS, Pss (smaps_rollup) and utime+stime over the process and its children (`/proc`).
- Peak = max over the window. Steady = median of samples from t=30 s onward. CPU = tick delta over the window (full) and from t=30 s (steady); ticks are 10 ms, so 0.0 means below 0.05 %.
- Config: all listeners bound to 127.0.0.1. Telegraf: `telegraf config --input-filter cpu:disk:diskio:kernel:mem:processes:swap:system --output-filter file`, output `files = ["stdout"]`.
- Stores scrape `127.0.0.1:9100` with default 1 m scrape interval, so each 90 s window holds about one scrape.

## Results

| Tool | Version | Steady RSS MB | Peak RSS MB | Steady PSS MB | CPU % (window) | Series |
|---|---|---|---|---|---|---|
| node_exporter | 1.12.1 | 17.5 | 17.5 | 15.6 | 0.0 | 1272 lines of /metrics |
| node_exporter, while scraped by prometheus | 1.12.1 | 22.8 | 22.8 | 20.9 | 0.0 (steady 0.1) | — |
| telegraf, default inputs, stdout | 1.39.3 | 166.2 | 167.3 | 164.3 | 0.4 | not counted; 295 stdout lines per window |
| telegraf, rerun | 1.39.3 | 166.1 | 166.8 | 164.3 | 0.4 | — |
| beszel-agent, no hub | 0.18.7 | 16.0 | 16.0 | 14.3 | 0.0 | — |
| zabbix_agent2, idle | 6.0.48 | 21.1 | 21.1 | 14.9 | 0.0 | — |
| beszel-hub, idle | 0.18.7 | 32.2 | 32.2 | 30.5 | 0.0 | — |
| prometheus, scraping node_exporter | 3.13.2 | 91.4 | 91.5 | 89.6 | 0.2 | 1277 (instant `count`) |
| prometheus, rerun | 3.13.2 | 89.5 | 96.2 | 87.7 | 0.2 | — |
| victoria-metrics single-node, scraping node_exporter | 1.149.0 | 50.2 | 66.5 | 50.2 | 0.2–0.3 | 1279 (instant `count`) |
| victoria-metrics, rerun | 1.149.0 | 49.3 | 50.0 | 49.2 | 0.2 | — |

Notes on the numbers:
- Telegraf was still rising at the end of both windows (152 MB at 0 s, 171 MB at 75 s). Steady is therefore a lower bound on a 90 s sample, not a plateau.
- Prometheus's peak in the rerun (96 MB) is above its steady value; that is a scrape or compaction spike, not a trend.
- Series counts come from the instant query `count({__name__=~".+"})` on each store.

## Skipped

- **netdata 2.10.3**: starts with `-D` and `-W set directories ...`, but as a non-root user it fails. It needs `/var/lib/netdata/registry` and reads `/etc/netdata/stream.conf`; neither is redirected by the `-W set directories` options. Not measured.
- **zabbix agent2**: `zabbix.agent2` (nixpkgs attribute name) was measured. `zabbix` alone and `zabbix-agent2` do not resolve.
- **Beszel hub**: measured idle, with no agent connected.
