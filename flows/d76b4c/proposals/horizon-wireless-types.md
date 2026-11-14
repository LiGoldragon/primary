# Horizon access points and link preference

Type proposal approved by Fable under `8d96` and `i3u7`, with the
current SAE-only correction applied. Bodies are authorized.

```ethos
Library
[ :horizon_lib:address:Interface                         ; existing interface identity
  :horizon_lib:name:WirelessNetworkName                  ; existing SSID type
  :horizon_lib:proposal:[ SecretReference WlanBand WlanStandard ] ] ; existing references and radio types
[ WirelessAccessPoint.{                                 ; one router-owned access point declaration
     Interface
     WirelessNetworkName
     WlanBand
     WirelessChannel.Integer                            ; radio channel
     WlanStandard
     SecretReference }                                  ; current SAE access-point password reference
  LinkKind.[ Wired Wireless Tether ]                     ; link kinds, independent of a particular ordering
  LinkKindOrdering.Vector<LinkKind>                     ; senior to junior, each kind exactly once
  WirelessInterfaces.Vector<Interface> ]                 ; node hardware fact; empty means no wireless interface
[]                                                       ; traits: none proposed at this type-only step
[]                                                       ; associations: none proposed at this type-only step
```

The router owns its access-point declarations, including its existing primary
and backup radios. Its current radio fields and SAE/backup records become these
declarations, rather than a second description alongside them. Every node with a
nonempty `WirelessInterfaces` joins the other nodes' access points; a node joins
none of its own. A radio serving an access point is not a client; a router's
spare radio is a client of the other routers like any node. Client profiles are derived,
including SSID and the router's `SecretReference`; client declarations carry no
router selection or repeated credentials. The reference grants no new secret
value or decryption permission by itself.

`WirelessInterfaces` is the one missing node hardware fact: current `Machine`,
`Io` and projected node fields expose no general wireless-interface inventory;
router radio roles alone cannot classify the other nodes.

The cluster carries `LinkKindOrdering`; a node carries `Option<LinkKindOrdering>`.
The cluster datum is `[ Tether Wired Wireless ]`; router node data explicitly
choose `[ Wired Tether Wireless ]`. A valid ordering is a permutation of all three
kinds. Lower position has seniority; metrics are derived monotonically from that
position, for both address families and every link consumer. Existing fixed
50/1024/2048 metric policy is replaced, not retained as another authority.

The vector wrapper is checked where data is read. A missing or doubled kind is
refused by a typed error naming that kind. Position gives seniority and metrics
follow from it. Current source confirms there is no declared EAP-TLS access
point; `wifi_cert` and `wifi-eap` are client-side facts. The field remains the
bare existing `SecretReference` until a second authentication method exists.

Field removes the exact stray manual UUID once at deployment and records the
evidence. No profile-retirement field is proposed.
