# Prometheus and the Network

## Page 1 · Flowchart — The cable between ouranos and Prometheus

**What this flowchart shows:** the direct cable link as witnessed on 09-24 morning, and which traffic gets through Prometheus's firewall.

- "ouranos (USB network card)" ⟶ cable ⟶ "Prometheus eno1 (its WAN side)" → "firewall".
- From the firewall, four arrows:
  - "ssh (22)" → green, "through";
  - "ping" → green, "through";
  - "binary cache (port 80)" → red, "dropped";
  - "neighbour discovery (IPv6)" → red, "dropped".
- Next to them, a second, longer path: "Yggdrasil over wireless, via br-lan", green, "works, but slow (92 ms)".

## Page 2 · What you said

> Well when the builder isn't reachable we just build locally.

-- living, 2026-09-24.

> Is there a firewall problem on Prometheus? ... I want Prometheus up, right? Let's fix the firewall so it's fully up or whatever is wrong with it.

-- living, 2026-09-24, to d8df70.

> They're built and installed from CriomOS so you can check the source that built that generation. I guess find out how that link is made if you want to know.

-- living, 2026-09-24, on how running services trace back to source.

## Page 3 · Flowchart — Why port 80 is dropped

**What this flowchart shows:** the composition fault d8df70 witnessed in CriomOS source.

- "cache module: open port 80" → an arrow into "NixOS firewall", which is shown switched off on routers.
- "router module: writes its own nftables rules by hand" → "only ssh opened".
- Result: "port 80 never reaches the router's rules" (red). The same happens to port 11434 (the local LLM).
- A proposed fix, dashed: "router reads the node's declared open ports" → "every declared port is honoured".

## Page 4 · Where it stands

- **Neighbour discovery:** Terra's fix is in CriomOS main. On 09-24 morning it wasn't deployed on Prometheus. *(Witnessed by d8df70; current state in the overview.)*
- **Port 80:** a source fix was ordered. Whether it should open to the WAN at all is your call: the cache already works over Yggdrasil.
- **Builder recovered:** b80e55 reports the whole chain proven, ouranos → Prometheus → Zeus, with a runtime firewall fix persisted. The declarative source still needs a typed capability for USB Internet sharing. *(Relayed.)*
- **IPv6 on ouranos's cable side:** turned off since 09-21.

## Page 5 · Flowchart — The open question on port 80

**What this flowchart shows:** the choice the witness left for you, as a fork.

- "Binary cache must reach ouranos" → a fork:
  - Left: "open port 80 on the router's WAN, only on cache nodes, only from the cable's subnet" → "fast, direct; the cache is exposed upstream".
  - Right: "use the cache over Yggdrasil only" → "already works; nothing opened; slower path".

## Page 6 · Proposals

1. ☐ Deploy the neighbour-discovery fix to Prometheus (a rebuild against current CriomOS main).
2. ☐ Choose the port 80 fork: open it to the WAN on cache nodes only, or use Yggdrasil only.
3. ☐ Have the router module honour every port a node declares open, fixing the whole class of faults, not just this one.
