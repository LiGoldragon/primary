# Transport and link health

Method: probe `getent ahosts zeus.goldragon.criome`, `ip route get 192.168.18.95`, strict noninteractive SSH with `BatchMode=yes`, `ConnectTimeout=8`, `ConnectionAttempts=1`, `StrictHostKeyChecking=yes`, and `UserKnownHostsFile=/home/li/.ssh/known_hosts`; probe `NIX_SSHOPTS='-o StrictHostKeyChecking=yes -o BatchMode=yes -o ConnectTimeout=8 -o ConnectionAttempts=1 -o UserKnownHostsFile=/home/li/.ssh/known_hosts' nix store info --store ssh-ng://root@<endpoint>`; probe fresh Ed25519 keys with `ssh-keyscan -T 8 -t ed25519 <endpoint> | ssh-keygen -lf -`; read local `ip -s link show dev wlp0s20f3`, `/sys/class/net/*/{operstate,carrier,carrier_changes}`; read target `ip -s link`, the same carrier files, and bounded `journalctl -k` over SSH; and read target `journalctl` for the exact SSH session window.

Current endpoint and identity observations:

- `zeus.goldragon.criome` resolves to `200:17f7:4fad:e50b:a50c:2048:2169:41f7`.
- The direct-IP route is `192.168.18.95 via 10.18.0.1 dev wlp0s20f3 src 10.18.0.102`; the local physical Ethernet `enp0s31f6` is down/no-carrier, so the current local route is carried by Wi-Fi rather than that Ethernet interface.
- Strict SSH to both `root@192.168.18.95` and `root@zeus.goldragon.criome` returned `hostname=zeus`, Linux `7.0.1`, and the same booted system path.
- Fresh key scans for both endpoints returned Ed25519 fingerprint `SHA256:5w4Jj0zqvfZdiGmJLCTKOG6JdXSdMCf3OaBd4EY65Mk`, matching the known-host material.
- `nix store info` through both explicit `ssh-ng` URIs succeeded with Nix `2.34.6` and `Trusted: 1`.

Current link counters are cumulative, not time-localized. On Ouranos, `wlp0s20f3` is up/carrier 1 with RX errors 0, RX drops 1, TX errors 0, and TX drops 249; carrier changes are 76. On Zeus, the direct-IP Ethernet `enp0s31f6` is up/carrier 1 at 1000/full with RX/TX errors 0 and drops 0; its cumulative RX missed count is 0. Zeus's Wi-Fi is also up but is not the direct-IP route. No relevant link, carrier, TCP, Nix, OOM, reset, error, drop, or timeout event appeared in the bounded target kernel journal around 00:55–01:05.

The target SSH journal gives the decisive timing witness for the copy session:

```text
Aug 23 00:15:28.002144 zeus ... Accepted publickey for root from 192.168.18.80 port 33400 ...
Aug 23 01:00:27.658288 zeus ... Received disconnect from 192.168.18.80 port 33400:11: disconnected by user
Aug 23 01:00:27.658458 zeus ... Disconnected from user root 192.168.18.80 port 33400
```

The interval is `2699.656144` seconds, effectively the configured 2700-second Lojix effect timeout. The source IP is the local-path address as seen by Zeus; the SSH record itself does not prove which process requested the disconnect, but its duration and alignment with the Lojix failure make the copy command the clear correlated session.

No current transport probe proves sustained copy throughput, and no current counter proves that a transient link fault did not occur during the earlier transfer.

