# Zeus connectivity

Method: probe `hostname; getent hosts zeus.goldragon.criome; ip -6 route get <resolved address>; ping -6 -c 1 -W 2 zeus.goldragon.criome; timeout 4 nc -6 -zv zeus.goldragon.criome 22; ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=yes li@zeus.goldragon.criome 'hostname'`.

Observed:

- The probe host is `ouranos`, not `zeus`.
- Zeus name resolution succeeds through the configured Yggdrasil route.
- The route selects `yggTun`.
- ICMP receives no reply and TCP/22 probes and strict noninteractive SSH time
  out.

Inference: this session cannot inspect Zeus's live profile, runtime links,
systemd state, or target-side Lojix socket. The timeout does not distinguish a
powered-off host, a route failure, or target-side filtering.
