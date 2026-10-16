---
description: An internet interruption or temporary network route requires reachability checks and a Wi-Fi fallback.
dependencies: []
---

Use `Network topology`, `Network preferred Wi-Fi` and `Network fallback Wi-Fi` for the temporary arrangement. After an interruption, check each host's actual address, route and SSH reachability, then DNS and an internet HTTPS request.

Before switching a host, witness that the preferred access point is visible and that association, DHCP, gateway reachability and internet access work. Use NetworkManager's checkpoint rollback for a remote Wi-Fi change and retain the fallback connection. Confirm the change from the new route before removing the checkpoint. Change one host at a time while another management path remains available.

Measure packet loss and the access point's station signal, retries and failures over a stated interval. A short successful sample establishes that interval; longer stability remains unmeasured. When the preferred access point is not visible, retain the working fallback and report the observed gap.

Two local routes through the same internet router share its upstream outage. Describe the fallback as a local Wi-Fi or access-point fallback, not independent internet redundancy. Preserve saved credentials without displaying them.

Remove the temporary arrangement's values when it ends, and retain reusable network procedure in its owning module.
