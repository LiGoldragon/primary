# Self-hosted monitoring for a small NixOS cluster: comparison

Research date: 2026-10-16. Scope: a laptop, a server and a build machine (a few hosts).
Compared: node_exporter + Prometheus, VictoriaMetrics single-node + vmagent, Grafana,
Netdata, Beszel, Telegraf + InfluxDB, Zabbix, Glances, Checkmk.

## Evidence grades used below

- **[measured here]** I ran `nix path-info --store https://cache.nixos.org -sSh` on
  2026-10-16 against store paths evaluated from the `nixos-unstable` channel tarball
  (https://channels.nixos.org/nixos-unstable/nixexprs.tar.xz). First number is the
  package's own NAR size, second is its full runtime closure. These are install sizes on
  NixOS, not RAM.
- **[measured, independent]** A third party measured it and published the method.
- **[measured, vendor]** The project's own company ran and published a benchmark.
- **[vendor claim]** The project states it with no published measurement.
- **[anecdote]** Blog, forum or hosting-template figure with no stated method.
- **[estimate]** My derivation from a stated rule; not measured.

No monitoring daemon was running on this host, so no RAM was measured locally.
github.com and api.github.com were unreachable from this host (connection refused);
raw.githubusercontent.com and img.shields.io worked. GitHub star counts and latest
releases below were read through img.shields.io JSON badges on 2026-10-16
(e.g. https://img.shields.io/github/stars/henrygd/beszel.json); they are rounded.

## Scale note that governs every RAM number

The central-store RAM of Prometheus-style systems is driven by active series, not by
host count. node_exporter exposes roughly 380 to 800 series per host
(~379 metrics counted in https://leonallen22.github.io/2019/11/06/netdata-telegraf-and-prometheus-exporters.html;
"around 800 unique metrics" per node_exporter in https://victoriametrics.com/blog/remote-write-benchmark/).
Three hosts therefore give about 1k to 3k active series. Every published benchmark is
at 100x to 10,000x this scale, so their ratios matter more than their absolute numbers.

## node_exporter + Prometheus server

- Stack: two Go binaries. node_exporter (HTTP :9100, about 50 collectors enabled by
  default, textfile collector for `*.prom` files) is scraped by Prometheus (pull model).
  Alertmanager is a separate optional binary. https://raw.githubusercontent.com/prometheus/node_exporter/master/README.md
- Install size [measured here]: node_exporter 1.12.1: 18.3 MiB own / 57.4 MiB closure.
  prometheus 3.15.0: 116.4 MiB / 155.5 MiB.
- Agent RAM/CPU: no official figure; README warns some non-default collectors have
  "significant resource demands on the host". No independent measured RSS found. The
  exporter reports its own `process_resident_memory_bytes`, so it is cheap to measure.
  One 2026 roundup tables node_exporter at ~15 MB [anecdote]
  (https://freebsdsoftware.org/blog/best-monitoring-tools-freebsd/).
- Store RAM: Robust Perception (Brian Brazil, Prometheus core developer) rule of thumb
  ~3 kB RAM per head-block series for 2.20+; "a tiny Prometheus with only 10k series
  would use around 30MB" [measured, independent expert profiling]
  (https://www.robustperception.io/why-does-prometheus-use-so-much-ram ,
  https://www.robustperception.io/how-much-ram-does-prometheus-2-x-need-for-cardinality-and-ingestion/).
  For 1k to 3k series: under 10 MB of head data plus Go runtime and page cache
  [estimate]; expect tens to low hundreds of MB RSS in practice [estimate].
  Prometheus 3.0 announcement shows prombench charts (8 CPU, 49 GB node) of CPU and
  memory falling from 2.0 to 3.0 but prints no numbers [measured, vendor]
  (https://prometheus.io/blog/2024/11/14/prometheus-3-0/).
- Reliability / storage: TSDB with in-memory head block protected by a WAL (128 MB
  segments), 2-hour blocks compacted up to 10% of retention or 31 days. Default
  retention 15d. ~1-2 bytes per sample. Docs: local storage "is not clustered or
  replicated" and "not arbitrarily scalable or durable in the face of drive or node
  outages"; corrupted blocks/WAL may have to be deleted, losing that range; NFS not
  supported. https://prometheus.io/docs/prometheus/latest/storage/
- Cadence: a new minor series every 6 weeks; v3.5 labelled LTS; older branches "best
  effort" (https://raw.githubusercontent.com/prometheus/prometheus/main/RELEASE.md).
  Latest: Prometheus v3.15.0, node_exporter v1.12.1 (shields.io). Prometheus 3.0 was
  2024-11-14, first major in 7 years.
- People: CNCF project, accepted 2016-05-09, graduated 2018-08-09; CNCF lists 19,378
  contributors from 3,456 organisations (https://www.cncf.io/projects/prometheus/).
  32 named maintainers in MAINTAINERS.md, 8 with grafana.com addresses, others Hetzner,
  Scaleway, independents (https://raw.githubusercontent.com/prometheus/prometheus/main/MAINTAINERS.md).
  License Apache-2.0, never changed. Stars: prometheus 67k, node_exporter 14k.
- Best at: the de-facto standard exposition format and query language (PromQL); every
  other tool here can feed or read it; huge exporter ecosystem; alerting rules as code.
- NixOS: `services.prometheus` (`nixos/modules/services/monitoring/prometheus/default.nix`),
  `services.prometheus.exporters.node` (`.../prometheus/exporters.nix`),
  `services.prometheus.alertmanager`, pushgateway
  (https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/nixos/modules/module-list.nix).

## VictoriaMetrics single-node + vmagent

- Stack: Go. Single-node `victoria-metrics` is "one small executable with no external
  dependencies"; it can scrape by itself (`-promscrape.config`), so vmagent is optional
  at this scale. vmagent scrapes Prometheus targets and pushes by remote_write, with an
  on-disk buffer (`-remoteWrite.tmpDataPath`, capped by `-remoteWrite.maxDiskUsagePerURL`)
  when the store is unreachable. vmalert for rules. Apache-2.0 for single and cluster;
  Enterprise is separate. https://docs.victoriametrics.com/victoriametrics/single-server-victoriametrics/ ,
  https://docs.victoriametrics.com/victoriametrics/vmagent/
- Install size [measured here]: VictoriaMetrics 1.153.0 (the nixpkgs package bundles the
  whole tool family, vmagent included): 243.6 MiB / 282.7 MiB.
- RAM: docs claim "up to 7x less RAM than Prometheus, Thanos or Cortex when dealing with
  millions of unique time series" [vendor claim], citing Aliaksandr Valialkin's Medium
  node_exporter benchmark (Medium returned 403 to me). Secondary reports of that
  benchmark disagree: 4.3 GB VM vs 14 GB Prometheus (https://last9.io/blog/prometheus-vs-victoriametrics)
  or vs 23 GB with ~2.8M active series (Packt, https://www.packtpub.com/en-jp/product/mastering-prometheus-12-9781805125662/chapter/chapter-9-utilizing-remote-storage-systems-with-prometheus/using-victoriametrics)
  [measured, vendor; old, pre-Prometheus 3]. Agent benchmark 2024-03-27, 5000 simulated
  node_exporter hosts, 12 h, v1.99.0 vs Prometheus 2.50.1 agent mode vs Grafana Agent
  0.40.2: vmagent 2.69 cores / 2.2 GB, Prometheus agent 3.69 cores / 19 GB, Grafana Agent
  4.16 cores / 25.3 GB [measured, vendor] (https://victoriametrics.com/blog/comparing-agents-for-scraping/).
  No published figure at 3-host scale; docs give no per-series RAM rule, only "keep 50%
  free RAM". At this scale RAM is dominated by the runtime, tens of MB [estimate].
- Reliability / storage: merge-tree-like parts with per-month partitions merged in the
  background; ingested data buffered "in memory for up to a second", then in-memory parts
  periodically flushed (`-inmemoryDataFlushInterval`); docs state it "protects the
  storage from data corruption on unclean shutdown (i.e. OOM, hardware reset or kill -9)".
  Default retention 1 month (minimum 24h). No notable data-loss incident found.
- Cadence: very frequent releases (latest v1.154.0 on shields.io); LTS lines are
  Enterprise-only, new line every 6 months, 12-month support; open-source users are told
  to track latest (https://docs.victoriametrics.com/victoriametrics/lts-releases/).
- People: VictoriaMetrics Inc., founded by Aliaksandr Valialkin (fasthttp author), Roman
  Khavronenko and others; bootstrapped, no outside funding reported
  (https://www.enterprisetimes.co.uk/2023/11/06/open-source-vendor-victoriametrics-delivers-stunning-growth/ ,
  https://underdogfounders.substack.com/p/victoriametrics-ukrainian-database).
  License Apache-2.0, unchanged. Stars 18k. Smaller core team than Prometheus; the
  company is the steward (no foundation).
- Best at: Prometheus-compatible ingest and PromQL-superset (MetricsQL) query at much
  lower RAM/disk; single binary does scrape + store + query; good long retention on a
  small disk; vmagent's disk buffer helps a laptop that is often offline.
- NixOS: `services.victoriametrics` (`nixos/modules/services/databases/victoriametrics.nix`:
  `listenAddress` :8428, `retentionPeriod`, `prometheusConfig` for built-in scraping,
  DynamicUser plus strong systemd hardening), `services.vmagent`, `services.vmalert`
  (https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/nixos/modules/services/databases/victoriametrics.nix).

## Grafana (display)

- Stack: Go backend + TypeScript/React frontend; embedded SQLite by default (MySQL 8+ /
  PostgreSQL 12+ optional). Stores dashboards and users, not metrics; reads Prometheus,
  VictoriaMetrics, InfluxDB, Zabbix (plugin) and others as data sources.
- Install size [measured here]: grafana 13.2.3: 731.3 MiB / 770.5 MiB (the largest single
  package here).
- RAM: docs minimum 512 MB and 1 CPU; "Small" deployment 2 cores, 2-4 GB [vendor claim]
  (https://grafana.com/docs/grafana/latest/setup-grafana/installation/).
- Reliability: mature (since 2014), monthly-ish minors; latest v13.2.4 (shields.io).
- People: Grafana Labs. Relicensed Apache-2.0 to AGPLv3 in April 2021 (with Loki, Tempo);
  CLA allows future relicensing (https://en.wikipedia.org/wiki/Grafana). Funding: $220M
  at $3B valuation in 2021 (https://www.bloomberg.com/news/articles/2021-08-24/grafana-labs-raises-220-million-round-at-3-billion-valuation),
  $270M at $6B in 2024 (https://www.lemondeinformatique.fr/actualites/lire-le-specialiste-de-l-observabilite-grafana-leve-270-m$-94501.html).
  Stars 77k. Grafana Labs also employs a large share of Prometheus maintainers.
- Best at: one dashboard over many back ends; community dashboards (e.g. "Node Exporter
  Full") ready-made for node_exporter data.
- NixOS: `services.grafana` (`nixos/modules/services/monitoring/grafana.nix`) with
  declarative provisioning of data sources and dashboards.

## Netdata

- Stack: agent in C with Go plugins (and optional Python plugins); per-second
  collection, built-in dbengine store, built-in dashboard at :19999, ML anomaly detection,
  alerts. Agents can stream to a Netdata "Parent" for centralisation. Exports to
  Prometheus (scrape endpoint) and other back ends.
- Install size [measured here]: netdata 2.11.0: 441.6 MiB / 1.1 GiB closure (largest
  closure here; includes Python environment and plugins).
- Agent RAM/CPU: docs say "1%-5% of a single core" default, "5%-20% in production"; RAM
  "100-200 MB" empty system, "250-350 MB in typical production"; ~4 GiB disk by default
  [vendor claim] (https://learn.netdata.cloud/docs/netdata-agent/resource-utilization).
  2019 independent test on AWS t3.micro, default config: "<1%" CPU, "<100MB" RAM, ~1833
  metrics [measured, independent; old version]
  (https://leonallen22.github.io/2019/11/06/netdata-telegraf-and-prometheus-exporters.html).
  Central (Parent) at 1000 nodes / 4.6M metrics/s: 9.36 cores, 47.1 GiB peak RSS vs
  Prometheus 3.1.0 14.76 cores, 383 GiB [measured, vendor; Netdata CEO, 2025-01-23]
  (https://www.netdata.cloud/blog/netdata-vs-prometheus-2025/).
- Storage: dbengine with 3 tiers (per-second 14 d / 1 GiB, per-minute 3 months / 1 GiB,
  per-hour 2 years / 1 GiB by default), ~0.5 byte/sample, size limits are soft caps;
  `ram` and `none` modes for children (https://learn.netdata.cloud/docs/netdata-agent/database).
  No confirmed data-loss report found; v2.3.2 fixed journal-file validation and a
  dbengine crash (https://firehol.org/download/netdata/releases).
- People: Netdata Inc. (Costa Tsaousis, founder/CEO; Greece/US). Series A $17M led by Bain
  Capital Ventures (2019) and $14.2M extension led by Bessemer (2020), ~$31M total
  (https://www.trendingtopics.eu/silicon-valley-vc-bessemer-leads-the-new-14-2m-round-of-greek-startup-netdata/).
  Stars 81k (highest here). Latest v2.12.1.
- License: agent GPLv3+. The newer dashboard (v2/v3 UI) is under the Netdata Cloud UI
  License (NCUL1), proprietary and shipped as a minified blob; distributions reacted:
  nixpkgs builds without it by default (`withCloudUi = false`; enabling it adds the
  `ncul1` license) (https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/pkgs/tools/system/netdata/default.nix ,
  https://gitlab.alpinelinux.org/alpine/aports/-/merge_requests/70500 ,
  https://scancode-licensedb.aboutcode.org/netdata-ncul1.html). Netdata Cloud itself is
  closed SaaS. Analytics reporting to Netdata Inc. exists; the NixOS module defaults it off.
- Best at: zero-configuration, per-second, very broad auto-detected metrics with a
  ready dashboard and anomaly detection; troubleshooting "what is happening right now".
- NixOS: `services.netdata` (`nixos/modules/services/monitoring/netdata.nix`;
  `enableAnalyticsReporting` default false, `claimTokenFile` for Cloud, python plugin
  options). Without the unfree UI override the local dashboard is limited; see
  https://wiki.nixos.org/wiki/Netdata .

## Beszel

- Stack: Go. Two binaries: agent (on each host) and hub (web app built on PocketBase,
  i.e. embedded SQLite). Agent either listens for SSH from the hub on :45876 or dials out
  to the hub over WebSocket (`HUB_URL`, `KEY`, `TOKEN`; universal token since 0.12.0).
  Collects CPU, memory, disk, network, Docker/Podman per container, GPU, SMART, systemd
  units; alerts, OIDC, multi-user, backups to disk or S3.
  https://beszel.dev/guide/what-is-beszel , https://beszel.dev/guide/agent-installation ,
  https://beszel.dev/guide/getting-started
- Install size [measured here]: beszel 0.20.0 (agent + hub in one package): 51.3 MiB /
  90.4 MiB.
- RAM: project says only "smaller and less resource-intensive than leading solutions"
  [vendor claim]. Agent "typically uses less than 10MB of RAM"
  (https://akashrajpurohit.com/blog/beszel-selfhosted-server-monitoring-solution/) and
  agent ~15 MB / hub ~50 MB (https://selfhosting.sh/compare/beszel-vs-netdata/) [anecdote].
- Reliability: young (pre-1.0; latest v0.21.0, nixpkgs has 0.20.0); storage is PocketBase
  SQLite with its own migrations on upgrade (PocketBase upgrade guides advise backing up
  `pb_data`: https://pocketbase.io/v023upgrade/jsvm/). Resolution is coarse
  (~1-minute records) compared with Netdata. No reported Beszel data-loss incident found.
- People: essentially one author, Hank (henrygd); 172 contributors and ~730 commits in the
  past year (shields.io); no company or funding. License MIT. Stars 26k, fast-growing.
- Best at: smallest whole stack with a usable web UI and alerts out of the box; ideal for
  "is each box healthy, what is its history" across a handful of machines.
- Integration: does not speak Prometheus exposition; it is a closed loop (agent to hub).
  It can sit alongside a Prometheus/VictoriaMetrics stack but does not feed it.
- NixOS: `services.beszel.agent` and `services.beszel.hub`
  (`nixos/modules/services/monitoring/beszel-agent.nix`, `beszel-hub.nix`); agent module
  has `environmentFile` for keys, `smartmon.enable`, GPU collector selection, and strong
  systemd hardening (https://raw.githubusercontent.com/NixOS/nixpkgs/nixos-unstable/nixos/modules/services/monitoring/beszel-agent.nix).

## Telegraf + InfluxDB

- Stack: Telegraf is a Go static binary with "over 300 plugins", MIT
  (https://raw.githubusercontent.com/influxdata/telegraf/master/README.md); it can output
  to InfluxDB, Prometheus (`outputs.prometheus_client`), VictoriaMetrics (Influx line
  protocol or remote_write) and many others. InfluxDB has three generations: 1.x (Go, TSM
  engine, InfluxQL), 2.x (Go, Flux, buckets/orgs), 3.x (Rust rewrite; Parquet files,
  local disk or object store, SQL + InfluxQL; 3 Core is the open-source single node)
  (https://docs.influxdata.com/influxdb3/core/).
- Install size [measured here]: telegraf 1.40.2: 311.5 MiB / 350.6 MiB (all plugins
  compiled in); influxdb 1.12.2: 152.6 MiB / 283.7 MiB; influxdb2: 281.3 MiB closure.
  InfluxDB 3 Core not checked in nixpkgs.
- RAM: no official Telegraf baseline; ~200 MB with 1,600 SNMP nodes [anecdote]
  (https://community.influxdata.com/t/telegraf-memory-sizing/601); memory scales with
  `metric_buffer_limit` x plugins. InfluxDB: VictoriaMetrics claims "10x less RAM than
  InfluxDB" [vendor claim by a competitor]. No small-scale measurement found.
- Reliability: the main risk is product churn, not crashes. Flux, the 2.x query language,
  is in maintenance (security and critical fixes only) and is not in 3.x
  (https://docs.influxdata.com/flux/v0/future-of-flux/); 2.x to 3.x is a migration
  (Flux queries rewritten to SQL/InfluxQL; https://computingforgeeks.com/migrate-influxdb-2-to-3/).
  InfluxDB 3 Core shipped with a 72-hour query limit in alpha, later lifted
  (https://influxdata.com/blog/influxdb3-open-source-public-alpha).
- People: InfluxData Inc.; $171M total equity after $51M Series E (Feb 2023)
  (https://www.influxdata.com/blog/influxdata-closes-series-e-round-and-raises-81-million/).
  Licenses: Telegraf MIT; InfluxDB 1.x/2.x MIT (clustering of 1.x was closed-source);
  InfluxDB 3 Core MIT/Apache-2.0 dual. Stars: telegraf 18k, influxdb 32k.
- Best at: Telegraf as a universal collector (SNMP, IPMI, MQTT, logs, many apps) that can
  feed whatever store you choose; InfluxDB for push-based event/IoT style data.
- NixOS: `services.telegraf`, `services.influxdb` (1.x), `services.influxdb2`.

## Zabbix

- Stack: server and proxy in C, classic agent in C, agent 2 in Go, frontend in PHP,
  history in an SQL database (MySQL/MariaDB/PostgreSQL, optionally TimescaleDB). Current
  7.4, 8.0 in development. Small install (1,000 metrics): 2 vCPU, 8 GiB RAM [vendor
  claim] (https://www.zabbix.com/documentation/current/en/manual/installation/requirements).
- Install size [measured here]: zabbix-agent 7.4.15: 1.7 MiB / 49.2 MiB; zabbix-agent2:
  20.9 MiB / 71.2 MiB; zabbix-server (pgsql): 33.5 MiB / 173.4 MiB, plus PHP frontend
  and the database server.
- Agent RAM: no official figure; ~20 MB in one roundup table [anecdote]
  (https://freebsdsoftware.org/blog/best-monitoring-tools-freebsd/).
- Reliability: very mature (first release 2001); LTS releases every ~18 months (6.0,
  7.0) with long support. Storage reliability is that of the SQL database used.
- People: Zabbix SIA, Riga, founded by Alexei Vladishev; ~107 employees in 2024 and
  profitable by registry data; no venture funding reported (https://datreal.com/en/lv/company/40003738045 ,
  https://assets.zabbix.com/files/company/Zabbix-Alexei-Vladishev-bio.pdf).
  License: GPLv2+ until 6.4; AGPLv3 from 7.0 (June 2024)
  (https://blog.zabbix.com/striking-the-right-balance-zabbix-7-0-to-be-released-under-agplv3-license/).
  GitHub mirror stars 6.5k (development is on Zabbix's own Git/Jira).
- Best at: classic IT/network monitoring with templates, SNMP, inventory, escalations
  and maintenance windows; overkill and heavy for three hosts.
- NixOS: `services.zabbixAgent`, `services.zabbixServer`, `services.zabbixProxy`,
  `services.zabbixWeb` (`nixos/modules/services/monitoring/zabbix-*.nix`,
  `nixos/modules/services/web-apps/zabbix.nix`).

## Glances (relevant as a lightweight per-host view and exporter)

- Stack: Python 3.10+ on psutil; terminal UI, client/server, or web server with REST API
  and WebUI on :61208; exports to Prometheus, InfluxDB, PostgreSQL/TimescaleDB, Graphite,
  Kafka, etc. LGPLv3. Author Nicolas Hennion (nicolargo).
  https://raw.githubusercontent.com/nicolargo/glances/develop/README.rst
- Install size [measured here]: glances 4.5.7: 6.1 MiB / 279.6 MiB (Python closure).
- RAM: no official figure; Python process, typically more than a Go exporter [estimate].
- No history store of its own; it is a live view or a collector feeding another store.
  Stars 34k. NixOS: `services.glances` (`nixos/modules/services/monitoring/glances.nix`).

## Checkmk (relevant only for comparison; poor fit on NixOS)

- Stack: server is an OMD "site" bundling a monitoring core, Apache, Python, RRD
  storage; agent is a shell script plus `cmk-agent-ctl` Agent Controller, pull on TCP
  6556 (unencrypted until registered with TLS)
  (https://docs.checkmk.com/2.4.0/en/agent_linux.html).
- People and license: Checkmk GmbH (formerly Mathias Kettner GmbH, then tribe29 GmbH,
  renamed April 2023). Community edition (formerly "Raw") GPLv2; Pro/Ultimate editions
  proprietary; Raw renamed Community per Werk #19391 (Nov 2025)
  (https://checkmk.com/werk/19391 , https://en.wikipedia.org/wiki/Checkmk). Stars 2.6k.
- NixOS: no module in nixpkgs module-list (searched for checkmk/check_mk: no matches).
  Server ships as distro packages or Docker; poor fit for a declarative NixOS cluster.

## How they combine

- node_exporter on every host -> Prometheus or VictoriaMetrics (scraping directly, or
  vmagent on a host that is often offline, which buffers to disk) -> Grafana reading the
  store as a Prometheus data source. VictoriaMetrics accepts Prometheus remote_write, so
  Prometheus can also forward to it.
- Netdata can be scraped by Prometheus/VictoriaMetrics (endpoint path from memory, not
  re-read: `/api/v1/allmetrics?format=prometheus`; the 2025 Netdata benchmark had Prometheus scrape 1,000 Netdata agents over
  OpenMetrics), so Netdata can be the per-host collector and dashboard while a central
  TSDB keeps history.
- Telegraf can replace node_exporter as collector and write to VictoriaMetrics (Influx
  line protocol is accepted natively) or expose a Prometheus endpoint.
- Glances can export to Prometheus or InfluxDB.
- Grafana reads Prometheus, VictoriaMetrics, InfluxDB and (via plugin) Zabbix.
- Beszel is self-contained; it does not export to or read from the others.

## Images usable as figures

- Prometheus logo: https://upload.wikimedia.org/wikipedia/commons/3/38/Prometheus_software_logo.svg
  Apache-2.0, author Alexander Schwartz (https://commons.wikimedia.org/wiki/File:Prometheus_software_logo.svg).
  node_exporter has no separate logo; use this.
- VictoriaMetrics logo: https://upload.wikimedia.org/wikipedia/commons/c/c6/VictoriaMetrics_logo.svg
  public domain (below threshold of originality), trademark may apply.
- Grafana logo: https://upload.wikimedia.org/wikipedia/commons/a/a1/Grafana_logo.svg
  tagged AGPLv3+ on Commons, trademark of Grafana Labs. Dashboard screenshots also on
  Commons, e.g. https://commons.wikimedia.org/wiki/File:Grafana_screenshot_(2018).png
  (check licence on its page before use).
- Netdata dashboard screenshot (2016): https://upload.wikimedia.org/wikipedia/commons/e/ed/Netdata.png
  GPLv3+ / CC BY-SA 4.0, author UCULinuxData.
- Beszel dashboard screenshot: https://beszel.dev/image/home-dashboard.png
  (project is MIT; the docs site does not state a separate image licence: confirm).
- InfluxDB logo: https://commons.wikimedia.org/wiki/File:Influxdb_logo.svg (direct
  upload URL not read), public domain (simple shapes). Telegraf: only old logos on Commons (File:Telegraf-logo-old1.jpg), licence
  not checked.
- Zabbix logo: https://upload.wikimedia.org/wikipedia/commons/6/6f/Zabbix_logo.svg
  public domain (below threshold), trademark.
- Glances screenshot: https://raw.githubusercontent.com/nicolargo/glances/develop/docs/_static/glances-summary.png
  (repository LGPLv3).
- Checkmk: no freely licensed image found quickly.

## Gaps

- No measured agent RSS at small scale exists for node_exporter, vmagent, Telegraf,
  Zabbix agent or Beszel in a primary source. Measuring is cheap on our own hosts:
  `systemctl show -p MemoryCurrent <unit>` or `process_resident_memory_bytes`.
- The original Valialkin Medium benchmark (Prometheus vs VictoriaMetrics on node_exporter
  data) returned HTTP 403; its figures above are from secondary sources that disagree.
- GitHub repository pages (contributors, issue history) were not reachable directly.
