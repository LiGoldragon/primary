<!-- to-the-living:start -->
Presentation.{ «Knowledge: monitoring systems» }

# Knowledge: monitoring systems

```
 every host
 +------------------------+
 | a collector            |
 | node_exporter, vmagent,|
 | Beszel agent, Telegraf |
 +------------------------+
     |  measures, every
     |  minute or faster
     v
 +------------------------+
 | a store                |
 | Prometheus or          |
 | VictoriaMetrics        |
 +------------------------+
     |  queries
     v
 +------------------------+
 | a view and alerts      |
 | Grafana, vmalert,      |
 | or a built-in screen   |
 +------------------------+
```

Most systems split into these three parts and speak the Prometheus format between them, so a part can be swapped. Beszel, Netdata and Zabbix bring all three in one product, in their own formats.

## Memory, measured on Ouranos

Each ran alone for 90 seconds, collecting from one host (about 1,280 series).

| part | memory |
|---|---|
| Beszel agent | 16 MB |
| node_exporter | 18 MB |
| Zabbix agent 2 | 21 MB |
| Beszel hub | 32 MB |
| VictoriaMetrics, storing | 50 to 67 MB |
| Prometheus, storing | 90 to 96 MB |
| Telegraf | 166 MB and still rising |

Netdata would not run without root; its makers state 100 to 350 MB per host.

## Who stands behind each

| system | steward | licence | since |
|---|---|---|---|
| Prometheus, node_exporter | CNCF foundation, 32 maintainers | Apache 2.0 | 2012 |
| VictoriaMetrics | VictoriaMetrics Inc., self-funded | Apache 2.0; long-term support paid | 2018 |
| Grafana | Grafana Labs, venture-funded | AGPL since 2021 | 2014 |
| Netdata | Netdata Inc., venture-funded | GPL agent; newer dashboard proprietary | 2013 |
| Beszel | one author | MIT | 2024, before 1.0 |
| Telegraf, InfluxDB | InfluxData, venture-funded | MIT; database rewritten twice | 2013 |
| Zabbix | Zabbix SIA, profitable, private | AGPL since 2024 | 2001 |

Every one except Checkmk has a NixOS module.

## Why one or the other

- **node_exporter with VictoriaMetrics**: the lightest standard pair; one store binary that collects by itself and keeps data while a laptop is away.
- **node_exporter with Prometheus**: the reference, the longest record, a foundation behind it.
- **Beszel**: the lightest whole product with a screen and alerts, held by one person, one-minute detail, not in the Prometheus format.
- **Netdata**: the most charts out of the box, the heaviest, part of it proprietary.
- **Zabbix**: built for many hosts and a database; more than a small cluster needs.
- **Telegraf with InfluxDB**: many inputs, the heaviest agent here.

## Proposal 1: the knowledge module

File: mind-context/knowledge/monitoring-systems.md, new

+ ---
+ description: A monitoring collector, store or view is chosen for the cluster.
+ dependencies: []
+ ---
+
+ ## Monitoring systems
+
+ A monitoring system has a collector on each host, a store, and a view with alerts; Prometheus-format parts can be swapped one for another. Measured on Ouranos, one host, about 1,280 series: Beszel agent 16 MB, node_exporter 18 MB, Zabbix agent 2 21 MB, Beszel hub 32 MB, VictoriaMetrics 50 to 67 MB, Prometheus 90 to 96 MB, Telegraf above 166 MB. Netdata states 100 to 350 MB per host and needs root. Prometheus and node_exporter belong to the CNCF under Apache 2.0; VictoriaMetrics to a self-funded company under Apache 2.0; Beszel to one author under MIT, before 1.0; Grafana and Zabbix moved to AGPL; Netdata's newer dashboard is proprietary.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
