# Operational: the VM runs on the node, not on the flow's host — resource allocation needs the Horizon Nexus, a proper nexus where the cluster state can be queried

## The virtual machine is running on the node. Allocating resources is not easy. Prometheus is the workhorse. It should be a feature on a node that people can query through Horizon. We need to make Horizon a proper nexus so the cluster state can be queried

Context: living correction to Psyche Fable f38926 on 2026-09-19, relayed to
primary Psyche opus b81560 with psyche propagation. The living corrects: the
sandbox VM runs on a node (Prometheus is the workhorse), not necessarily on
the flow's own host. Resource allocation is a cluster-level concern. The
Horizon must become a proper nexus so flows can query the cluster state to
know where to run things. Fable logged this at flows/f38926/vision/horizon.md
and is asking the living for the Horizon Nexus anatomy. Logged by the main
flow before acting.

> No, the virtual machine is running on the node. This is a bit complicated, but allocating resources is not easy. We haven't really gotten into that, but Prometheus is mostly the workhorse, so it should be a feature on a node. People should be able to know by querying the Horizon. That's why we need to make this a proper nexus. We need to make the Horizon a proper nexus, so the current state of the cluster can be queried from that.

-- psyche, to Psyche Fable f38926, relayed to primary Psyche opus b81560. Input mode not established.
