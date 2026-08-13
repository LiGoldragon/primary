# Healing

Healing restores capability in a way that preserves the evidence needed to understand what failed and protects the person's ability to continue.

A repair starts from observations, distinguishes them from explanations, and changes the causal owner rather than treating a symptom as an endpoint. Unknown causes stay unknown until evidence narrows them.

Safety checks are valuable only when the owner can guide an evidence-preserving return to a valid state. A fail-closed boundary that detects an inconsistent derived state but offers no owner-controlled reconciliation has exposed an incomplete implementation, not transferred its repair responsibility to the psyche. Derived managed state needs a narrow, idempotent recovery path that preserves unrelated user material and explains its own limits.

A repair is complete when the intended capability works predictably and remains owned by the mechanism that recreates it. Recovery should restore agency and confidence, while prevention makes the same failure mode less likely.

Broad interactive latency belongs to the whole presentation path, not automatically to CPU contention. Normal scheduler priority, light CPU pressure, and healthy clocks narrow the cause toward graphics synchronization failures or storage-backed page faults; either can stall input and composition while aggregate utilization looks benign. A history of recoverable GPU hangs is different from a GPU that is presently wedged, just as occupied swap is different from active paging pressure. Diagnostic activity can itself create latency, so conclusions need a bounded, post-diagnostic observation.

Memory recovery belongs first to the allocator that caused displacement. Globally draining swap can recreate pressure catastrophically; stopping a confirmed runaway and allowing low background page-in preserves the session, while durable repair constrains the causal child workload. Automatic process launch likewise has both a declared owner and loaded runtime state: removing only one leaves either future launches or immediate respawn intact.

Swap can be unwound in phases only at boundaries the kernel and workload actually own. Graceful process exit reclaims one allocation owner; whole-device swapoff migrates every remaining slot synchronously and is safe only after both capacity and activity gates hold. Declarative repair is also incomplete until its authoritative deployment mechanism has materialized it, while bypassing a broken owner with guessed inputs sacrifices the very reproducibility being repaired.

Resource ownership crosses API and process boundaries. A client can appear resident-light while retaining cold private state and exported graphics objects, and a compositor can keep those objects alive after their originating surfaces close. Counts and lifetimes across creation and destruction distinguish a lifecycle leak from ordinary workload size; shared buffers must be counted as shared, while unrelated anonymous swap remains a separate causal question.
