# Goldragon topology roles and Horizon extension points

Witness basis: `goldragon` `8c4d03de76907f590072c0998b00037330ebcd82`, `horizon-rs` `8c11dfaa19accda0e1d0d8708542a13ed788ea0a`, and `CriomOS` `d193bafca6d7848d8fa3813533ceb78f3228a07e`. This is a read-only schema/consumer inspection; the proposed forms below have no decode, projection, or deployment witness.

## What the current declaration says

`goldragon/cluster-definition.datom:1` is one positional `ClusterDefinition` record. Its node records follow `NodeDefinition`'s declared order in `horizon-rs/lib/ethos/horizon.ethos:73`: name, install/live definition, size, trust, machine, environment, network, keys, online, capabilities, fixed location. The capability vector is the host-role declaration (`horizon.ethos:71-72`); the node's `RouterInterfaces` lives in `NodeNetwork` (`horizon.ethos:65-67`).

| Host | Declared capabilities | Topology fact actually declared |
| --- | --- | --- |
| `ouranos` | Edge, LowPower, NextGeneration, Nordvpn, HardwareVideo, TailnetClient, TailnetController, NixBuilder.None, OpenCodeTesting, PersonaDevelopment(GitoliteServer) | The only TailnetController capability; its optional router-interface field is `None`. |
| `prometheus` | Center, LargeAi, Router, TailnetClient, NixBuilder(6), NixCache, VmHost | The only Router capability and the only current RouterInterfaces payload: `eno1` WAN, `wlp195s0` WLAN, 2.4 GHz/channel 6/Wifi4, and two **secret identifiers** (`routerWifiSaePasswords`, `routerBackupWifiPassword`). |
| `mirror-alpha`, `mirror-beta`, `vm-testing` | TestVm, TailnetClient | No RouterInterfaces. |
| `tiger` | Edge, LowPower, NextGeneration, HardwareVideo, NixBuilder.None | No tailnet or router capability. |
| `balboa` | Center | No tailnet or router capability. |
| `zeus` | Edge, LowPower, HardwareVideo | No tailnet or router capability. |

Those names and payloads are read directly from `goldragon/cluster-definition.datom:1`. A Router is not inferred from an interface: Horizon projects `Router` to `behavesAs.router` (`horizon-rs/lib/src/projection/viewpoint.rs:24-48`), and CriomOS gates router configuration on that boolean (`CriomOS/modules/nixos/router/default.nix:94`). The Wi-Fi/router module consumes `network.routerInterfaces` and its secret-name references (`router/default.nix:23-39, 94-120`); it uses `country`/`wirelessCountryCode` only if projected, otherwise currently defaults to `PL` (`router/default.nix:37`). The schema does not declare either field.

Tailnet has two current, separate marker capabilities. `horizon-rs` rejects more than one `TailnetController` but permits zero (`lib/src/projection/node.rs:117-132`). CriomOS enables Headscale from that marker (`CriomOS/modules/nixos/network/headscale.nix:13-18,69-89`) and only enables Tailscale on `TailnetClient` nodes; enrollment remains manual (`network/tailscale.nix:11-17`). Thus the current data names the controller host and client-marked hosts, but names no client roster attached to a controller, no preauth secret reference, no recipient metadata, and no trust anchor. The control-host fact currently witnessed is `ouranos`; a proposed migration must not silently change it.

`UserRole` is only `Code|Multimedia|Unlimited` (`horizon.ethos:36`, `horizon-rs/lib/src/generated/horizon.rs:67-71`); it is not an administrator-role enum. Administrator SSH keys derive from **Max user trust**, subject to the cluster ceiling and a key residing on a fully trusted node (`projection/trust.rs:16-35`; `projection/viewpoint.rs:145-175`). The present cluster trust lists `bird` and `li` at Max in the trailing `ClusterTrust` on `goldragon/cluster-definition.datom:1`; their declared roles are Multimedia and Unlimited, respectively. This yields administrative-key eligibility, not a named network-administrator authority.

`SecretReference` has only a `SecretName` (`horizon.ethos:19-20`; generated type at `lib/src/generated/horizon.rs:27-33`). The two Wi-Fi identifiers above are consumed as SOPS-file keys, never values (`CriomOS/modules/nixos/router/default.nix:26-36,106-120`). No secret recipient set appears in the Horizon schema or in the inspected Goldragon declaration. Recipient values are therefore unresolved and must not be inferred from host keys, user trust, or `.sops` ciphertext.

## Ownership and interpretation

Goldragon owns the data record, while `horizon-rs` owns its positional schema (stated in `goldragon/AGENTS.md:7-13`). The authored schema is `horizon-rs/lib/ethos/horizon.ethos`; its generated Rust view is evidence of that schema, not the authoring point. Horizon projects `RouterInterfaces` field-by-field (`lib/src/projection/views.rs:70-95`) and each capability variant (`views.rs:117-155`). CriomOS then reads the JSON projection through Nix: router uses the `Router` behavior and network payload, Headscale/Tailscale use their marker capabilities, and the USB gateway module looks for a capability record whose projected `kind` is `usbIpv4Gateway` and whose payload has exactly `downstream`, `downstreamMac`, `gateway`, and `uplink` (`CriomOS/modules/nixos/network/usb-ipv4-gateway.nix:20-77`).

Consequently every schema addition needs three coordinated changes: authored Horizon schema, Horizon Rust/projection mapping, and the relevant CriomOS consumer/fixture policy. Merely adding a Goldragon atom cannot reach a consumer.

## Three proposed additions — schema locations and illustrative Datom

These are concrete placement sketches only. Angle-bracket terms are unresolved values, deliberately not guesses; they are not claimed to compile.

1. **Tailnet control, clients, anchor, and preauth recipients.** Add the following definitions immediately before `ClusterDefinition` at `horizon-rs/lib/ethos/horizon.ethos:87`, then append `Option<TailnetConfiguration>` as the final field of `ClusterDefinition` on that line. A cluster-level record prevents duplicated/conflicting controller/client declarations on nodes.

   ```datom
   TrustAnchor.{ String }
   PreauthSecretRecipients.{ SecretReference Vector<NodeName> }
   TailnetConfiguration.{ NodeName Vector<NodeName> TrustAnchor PreauthSecretRecipients }
   ClusterDefinition.{ ClusterName ClusterNodes GenericNodeNames Users Domains ClusterTrust Option<TailnetConfiguration> }
   ```

   The corresponding **trailing** Goldragon datum, after existing `ClusterTrust` in `goldragon/cluster-definition.datom:1`, would be:

   ```datom
   Some.{ <control-host> [ <tailnet-client-node> ... ] TrustAnchor.{ <authority-or-certificate-pin-identifier> } PreauthSecretRecipients.{ SecretReference.{ <preauth-secret-identifier> } [ <authorized-recipient-node> ... ] } }
   ```

   `ouranos` is the currently witnessed controller and the current TailnetClient-marked nodes are listed above, but this sketch intentionally does not select a migration roster, anchor identifier, secret identifier, or recipients. The current Headscale module self-generates a TLS certificate (`CriomOS/modules/nixos/network/headscale.nix:23-65`); wiring this anchor needs a defined consumer contract, not an assertion that it already exists.

2. **Router Wi-Fi country/regulatory value.** Add `CountryCode.String` with the scalar declarations at `horizon.ethos:7-20`, then append `CountryCode` as the final field of `RouterInterfaces` at `horizon.ethos:66`:

   ```datom
   CountryCode.String
   RouterInterfaces.{ Interface Interface WlanBand Integer WlanStandard Option<SecretReference> Option<BackupWireless> CountryCode }
   ```

   The current Prometheus `RouterInterfaces` record at `goldragon/cluster-definition.datom:1` would gain one final positional atom:

   ```datom
   Some.{ eno1 wlp195s0 TwoG 6 Wifi4 Some.{ routerWifiSaePasswords } Some.{ wlp199s0f0u4 criome-backup TwoG 11 Wifi4 { routerBackupWifiPassword } } <ISO-3166-1-alpha-2-country-code> }
   ```

   The physical coordinates on another host are not a regulatory declaration, and no country value is witnessed in this record. Update the projection to expose a single chosen property and make the router consumer require it before removing its `PL` fallback (`views.rs:70-95`; `router/default.nix:37`).

3. **Integrated-uplink to USB-downlink Internet sharing.** Add `MacAddress.String` at the scalar declarations and add the payload plus capability alternative at `horizon.ethos:71`:

   ```datom
   MacAddress.String
   UsbIpv4Gateway.{ Interface MacAddress NodeIp Interface }
   NodeCapability.[ ... UsbIpv4Gateway.UsbIpv4Gateway ... ]
   ```

   In the selected node's existing capabilities vector in `goldragon/cluster-definition.datom:1`, add:

   ```datom
   UsbIpv4Gateway.{ <usb-downlink-interface> <usb-downlink-mac> <shared-gateway-cidr> <integrated-uplink-interface> }
   ```

   This order matches the consumer's required JSON fields: downstream, downstream MAC, gateway CIDR, uplink. It names no node or interface because this declaration contains no such capability today. The current Router implementation instead bridges hot-plug USB Ethernet ports into `br-lan` (`CriomOS/modules/nixos/router/default.nix:439-451`), whereas the USB IPv4 gateway consumer requires NetworkManager, rejects networkd and nftables, and installs shared-profile/NAT rules (`network/usb-ipv4-gateway.nix:117-190`). A projection mapping must produce the exact object shape that consumer reads; it cannot be derived from a bare marker capability.

## Sources

- `goldragon@8c4d03de76907f590072c0998b00037330ebcd82`: `cluster-definition.datom:1`, `AGENTS.md:7-13`.
- `horizon-rs@8c11dfaa19accda0e1d0d8708542a13ed788ea0a`: `lib/ethos/horizon.ethos:7-89`; `lib/src/projection/{composition.rs:70-165,node.rs:117-132,trust.rs:16-35,user.rs:23-99,viewpoint.rs:121-176,views.rs:70-155}`.
- `CriomOS@d193bafca6d7848d8fa3813533ceb78f3228a07e`: `modules/nixos/{criomos.nix:16-62,router/default.nix:23-39,94-120,420-451,network/default.nix:68-90,network/headscale.nix:13-119,network/tailscale.nix:11-17,network/usb-ipv4-gateway.nix:20-190}`.
- Existing topology intent, not a schema witness: `flows/6cc91b/vision/network.md:3-5`, `flows/753e69/vision/transitiveNetworkTopologyAndCertificateWifi.md:10-16`, and `flows/752e0f/vision/internetPropagation.md:1-3`.
