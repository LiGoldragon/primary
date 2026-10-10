# Mentci Web on Android: tailnet proposal

Field Sol 753e69 to PsycheHigh 1b8ac0, 2026-09-21. Proposal only; no phone, CriomOS, firewall, DNS, or runtime change was made.

## Choice for the living

- **Tailscale with the living's own account (recommended for the proof of concept):** the shortest Android and host setup, using Tailscale's managed coordination and identity service. [Android setup](https://tailscale.com/docs/install/android)
- **Self-hosted Headscale:** we own the coordination server and its data, but must operate a publicly reachable controller with DNS, trusted HTTPS, updates, and recovery. [Headscale requirements](https://headscale.net/stable/setup/requirements/)

## Proposed host and CriomOS change

**Ouranos should serve the Mentci Web proof of concept.** This is a placement proposal, not a running-listener observation. The living's [Mentci Web Vision](../../1b8ac0/vision/mentciWeb.md) names the UI and Nexus boundary; no current Mentci Web listener or URL was found in the Field/Mind reports inspected for this proposal. Mind should publish the actual port and URL before phone testing. Keep the web listener private to Ouranos's tailnet interface (or proxy a loopback listener over the tailnet), with access limited to the living's devices. No public Mentci Web port is needed.

CriomOS already has a capability-gated `tailnetClient` module that enables `services.tailscale`, but its comment says enrollment remains manual. For the recommended option, assign `tailnetClient` to Ouranos in the typed node service source, evaluate the generated CriomOS configuration, and enroll Ouranos in the living's own tailnet. First enrollment can use interactive approval, with no SOPS auth key. If unattended enrollment is later required, store a short-lived, scoped host auth key in SOPS and pass it as a runtime systemd credential; keep it out of the Nix store and command logs. [Tailscale server setup](https://tailscale.com/kb/1245/set-up-servers), [secure auth keys](https://tailscale.com/docs/features/access-control/auth-keys/how-to/secure-auth-keys)

For Headscale, use the existing `tailnetController` capability on a reachable node and `tailnetClient` on Ouranos if the controller runs elsewhere. The current CriomOS `headscale.nix` creates a **self-signed Phase 1 certificate** and opens its service port; this is not an out-of-home Android-ready endpoint. A CriomOS proposal would supply a public DNS name, trusted HTTPS, exact ingress/firewall rule, persistent controller state and backup, then enroll Ouranos's `tailscaled` against that controller. Headscale supports interactive registration or a preauth key; SOPS is needed for a host preauth key only if automated enrollment is chosen. Do not put an Android enrollment key in the repo. [Android alternate server](https://headscale.net/stable/usage/connect/android/), [registration](https://headscale.net/stable/ref/registration/)

## Android steps for the living (three lines)

1. Install the official Tailscale app on each Android device and allow its VPN request.
2. For Tailscale, sign in with your own account; for Headscale, open **Settings → Accounts → ⋮ → Use an alternate server**, enter the supplied HTTPS controller URL, and complete registration.
3. Turn the connection on, then open the Mentci Web tailnet URL that Mind publishes in the phone browser.

The choice is with the living through PsycheHigh. Phone setup and host activation wait for that choice and the actual Mentci Web endpoint.
