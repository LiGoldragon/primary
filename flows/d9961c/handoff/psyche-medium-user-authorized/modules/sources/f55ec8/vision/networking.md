# Networking

## The internal networking of our own devices, Android included, runs over the house's Wi-Fi or LAN, a foreign router not configured for us; nodes on that router find each other by the mesh protocol, sending each other their addresses since they share the interface and network; everyone attached to that router is connected internally, even what does not speak our protocol; our own locally configured domain name servers route us internally to the messenger, the Git servers and file access when at home, even through a foreign router as intermediary

Context: typed to the primary Claude f55ec8 on 2026-09-16, mid-turn, while the reachability witness ran (which found prometheus behind a foreign router 192.168.1.1 with the site's single public IPv4 and no IPv6). Logged by the main flow before acting.

> And then, of course, all the internal networking of our own devices and Android devices is on our own Wi-Fi in the house or through the LAN. They are using the house's LAN, which is not configured to work with us, to connect the nodes that are connected to that router to find each other on that LAN. That's the mesh protocol.
>
> They have a way to do that: they send each other's IP addresses, because they actually are the same wireless interface and everything. We're probably on the same network, or even through a line, it might connect to Wi-Fi on that router. We should be able to connect everybody using that router in the house, whatever we connect to that doesn't even speak our protocol, to connect everybody internally.
>
> Our own domain name servers that are configured locally are going to route us internally with our messenger and everything else, like our Git servers and our file access when we're at home on our own Wi-Fi, or on our own LAN, even through a foreign router as an intermediary.

-- psyche, typed.
