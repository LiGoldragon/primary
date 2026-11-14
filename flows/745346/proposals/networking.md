Presentation.{ «Networking between the nodes» Proposal }

# Networking between the nodes

Created by Fable 5.2. Sonnet gathered his words; an earlier Fable flow did the research.

### Proposal 1: A new module, the mesh between his nodes · psyche-belief › vision/networking.md

::: comment
His words, 13 November: «this brings up the topic of reliable mesh networking.» «the IP address it's getting from the router here … it could tell the cloud about that IP address» «they can all try each other's 192.168 address to see if it routes internally, and then they can establish that connection in the manner that Yggdrasil currently is not able to do.» «tail scale … sounds like that's the one we should be using … I have a feeling that eventually we'll be making a better version of that» «I'd like to be able to run the whole harness on the cloud eventually, so that when I'm traveling, I can still work with you» «if they're on an encrypted file system on a like piece of memory, if the host shuts down, there's no passwords to be recovered, and then … the node can ask for the passwords again when it restarts from my computer here locally.» On the provider: «The place where that has the most likelihood of being actually secure, in that the provider is not spying on its customers, and that they're not likely to be hacked». No module speaks of networking between hosts today, so this is a module of its own. The types are tentative: they say his idea in our own words, and Tailscale carries it for now. The node names in the examples are examples.
:::

+ ---
+ description: Networking between the nodes, how they find and reach one another at home and away, or a node rented in the cloud, is being designed or judged.
+ dependencies: [vision-criomos, vision-horizon]
+ ---

+ ## The nodes reach one another wherever they are

+ Every node reaches every other, whatever network each is on. A public node is a node every other node can reach from anywhere; each node tells it every address it has, the one its local router gave it among them, and learns from it the addresses of the others.

+ Two nodes whose addresses share a network prefix try each other's local address, and connect directly when it routes. A node no direct path reaches is reached through the public node.

```mermaid
+ flowchart TB
+     a["a node"] -- "tells every address it has to" --> p["the public node"]
+     p -- "tells each node the addresses of" --> o["the other nodes"]
+     a -- "tries the local address of, and connects directly to" --> o
+     a -- "reaches, when no direct path routes, through" --> p
```

```ethos
+ Library                                   ; tentative
+ [ horizon:[ NodeName ] ]                  ; imports: a node, by its name
+ [ IpAddress.String                        ; types
+   PrefixLength.Integer
+   Endpoint.{ IpAddress PrefixLength }     ; one address a node has, and the network it sits in
+   Report.{ NodeName Vector<Endpoint> }    ; what a node tells the public node, on every change of its addresses
+   Path.[ Direct.Endpoint                  ; how one node reaches another: at one of its addresses,
+          Relayed ] ]                      ;   or through the public node
+ []                                        ; traits
+ []                                        ; associations
```

```datom
+ ; a node on a home network reports the address its router gave it, and its public one
+ Report.{ desktop [ { 192.168.1.20 24 } { 203.0.113.7 32 } ] }
+ ; a laptop on the same prefix reaches it directly
+ Direct.{ 192.168.1.20 24 }
```

+ ## Tailscale for now

+ For now the mesh is Tailscale. A mesh of our own, better than it, comes later.

+ ## A public node is a capability

+ Being the public node is a capability of a node, declared in the cluster data as every capability is.

```datom
+ ; tentative: a rented node whose capabilities are the mesh's coordination and its relay
+ { lighthouse Rented [ MeshCoordination MeshRelay ] }
```

+ ## The harness in the cloud

+ The whole harness runs in the cloud eventually, so that the living works with the machine while he travels.

+ A rented node keeps credentials in encrypted memory alone: when it shuts down nothing is left on it to recover, and when it starts again it asks his own computer for them.

+ A provider is chosen for how likely it is to be secure: one that does not spy on its customers and is unlikely to be broken into.

## Questions

1. Who runs the coordination: Tailscale the company, which works today with nothing to host, or Headscale on a public node of ours, which keeps the list of your nodes with you? My view: Headscale, on a small rented node that holds no credential.
2. Which provider for that first node? The research is at flows/d6c615/mesh-and-cloud-research.md; I can bring the three best candidates near central Mexico as a short page if you want to choose from a list.
3. You asked for a proper word for «the internet». «Public node» here says the one thing the design needs: a node reachable from anywhere. Is that enough, or do you want a word for the reachable network itself?
4. Rented is a new node type beside OnPremise, and MeshCoordination and MeshRelay are new capabilities. Are those the names?
