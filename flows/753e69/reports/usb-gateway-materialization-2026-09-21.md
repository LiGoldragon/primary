# USB gateway typed materialization checkpoint — 2026-09-21

Field Sol `753e69` owns the existing Lojix candidate. Terra's existing `claude_usage_research` lane alone owns CriomOS source and Ouranos runtime. No live network or activation change was made here.

## Published source graph

| Component | Exact published revision | Grade |
| --- | --- | --- |
| Horizon | `b45d6ad48b5ee5d28eb0127f17c6e0084b696e60` on main | Producer source; prior scoped Prometheus Nix check passed |
| signal-lojix | `01ae2b1e6fdf7319cb4498e524cfd9e893d6de01` on `usb-gateway-753e69` | Field-by-field `ClusterProposal` → typed `ClusterProposalWire` conversion, remote verified; new build not executed |
| meta-signal-lojix | `8fb526c471f0cfab3413673b2b3f2f34dd67a3b1` on `usb-gateway-753e69-meta` | Pins that exact ordinary Signal; remote verified; new build not executed |
| Lojix | `6b299ec17b6969fc8aaa44590a0f210e4b30061e` on `proposal/horizon-contract-repin-8565e8` | Pins one copy each of Horizon and the two Signal producers; remote verified candidate, not main |
| Goldragon | `a911515c69a77d81711d904d2da87612321be36e` on `usb-gateway-data-753e69` | Candidate assignment; main integration held for checks |
| CriomOS-home | `9842f51a86ce3a6c192033f759e90efd2c97b2b8` on `usb-gateway-consumer-6db4fe` | Terra consumer candidate; prior remote focused policy check passed; main integration held |

Goldragon's authored file is a Horizon `ClusterProposal` Datomic map. The old Lojix candidate incorrectly decoded that file as the vector-based Signal DTO. The producer now explicitly converts every authored node, user, domain, trust, machine, I/O, and service field into the typed DTO. Lojix's meta client, offline configuration writer, and bootstrap parse the authored Horizon Datomic record before that conversion. The typed Signal request remains binary; no JSON or Datomic blob is carried through Signal. The Lojix fixture and its shared test helper now exercise the authored record path. The Horizon parser is pinned to the same Protos revision as Horizon's Datomic implementation, separate from Lojix's older request codec.

## Checks and remaining gates

`cargo fmt --all -- --check`, `cargo metadata --offline --locked --no-deps`, `git apply --check --reverse --whitespace=error`, and a Lojix Nix derivation evaluation passed. Cargo.lock has one `horizon-lib`, one `signal-lojix`, and one `meta-signal-lojix` source. The Signal `test-datom-contract` remote-only build reached its derivation but Prometheus rejected the SSH builder connection before compilation. The Lojix remote-only test build has the same execution gate; its final result must be recorded separately. These checks do not prove Rust compilation, VM execution, or actual Lojix materialization.

Next: run the Signal and Lojix remote Nix checks with `--max-jobs 0` and fallback disabled once the Prometheus builder is reachable. Then materialize Goldragon's actual authored proposal through the pinned Lojix path, capture the normalized `horizon.node.services` USB gateway JSON and exact revision, and deliver that immutable payload to Terra's existing consumer lane. Check all nodes, absence behavior, same-payload unrelated nodes, duplicate refusal, and CriomOS NAT/DHCP/uplink ownership before branch integration or activation. Do not infer a payload from Horizon serde alone and do not activate Ouranos from this candidate.
