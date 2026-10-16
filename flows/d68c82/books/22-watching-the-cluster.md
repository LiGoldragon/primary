<!-- to-the-living:start -->
Presentation.{ «Watching the cluster» }

# Watching the cluster

```
 Ouranos   Zeus   Prometheus
 +----------------------+
 | one light collector  |
 | on each host         |
 +----------------------+
     |  over the tailnet
     v
 +----------------------+
 | one store on         |
 | Prometheus, with its |
 | charts               |
 +----------------------+
     |  a rule fires
     v
 +----------------------+
 | an alert you can     |
 | answer               |
 +----------------------+
```

The cluster has no monitoring yet, only checkup timers in the home configuration. What a first version watches comes from what has gone wrong this week:

| watch | today on Ouranos |
|---|---|
| a service failing or restarting in a loop | the OpenCode testing server restarted about 119,000 times |
| disk and memory pressure | processes wait on the disk 77% of the time |
| each harness session's memory | an old Codex session holds 2 GB |
| each sleep's deep idle and battery cost | zero deep idle in the last sleep |

## Crystallization

### Proposal 1: The cluster is watched

File: `psyche-context/skills/vision-monitoring.md`, new

+ ---
+ description: The cluster is watched, or a measure of a host reaches the living.
+ dependencies: []
+ ---
+
+ ## Monitoring
+
+ Every host carries one light collector, and one store on Prometheus keeps the measures and draws them.
+
+ It watches a service that fails or restarts in a loop, disk and memory pressure, each harness session's memory, and each sleep's deep idle with the battery it cost.
+
+ An alert reaches the living in a channel he can answer.

Ruling: land, amend, or reject.

## Choices

1. The collector: node exporter, which also counts failed units (recommended); Beszel, one agent with its own hub; or Netdata, the most charts, at 100–350 MB per host.
2. The store: VictoriaMetrics, lighter and Prometheus-compatible (recommended); or Prometheus itself.
3. The alert channel: a Matrix room on our own small server, two-way (recommended); a book in the living messenger; or ntfy, one-way push.
<!-- to-the-living:end -->
