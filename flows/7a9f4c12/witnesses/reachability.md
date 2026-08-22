Subject: Zeus direct-IP and DNS endpoint reachability.

Method: probe `hostname; getent ahosts zeus.goldragon.criome; ip route get
192.168.18.95; ip route get <DNS answer>; ssh-keygen -F <host> -f
<known-hosts-file>`; strict probes `timeout 15 ssh -o BatchMode=yes
-o ConnectTimeout=8 -o ConnectionAttempts=1 -o StrictHostKeyChecking=yes
-o LogLevel=ERROR root@192.168.18.95 'hostname; uname -sr'` and the same
command against `root@zeus.goldragon.criome`; public-key scans
`ssh-keyscan -T 8 -t ed25519 <host> | ssh-keygen -lf -`; and
`NIX_SSHOPTS='-o StrictHostKeyChecking=yes -o BatchMode=yes -o ConnectTimeout=8
-o ConnectionAttempts=1' timeout 20 nix store info --store
ssh-ng://root@<host>` for each endpoint.

Observed:

- The local probe host is `ouranos`.
- `zeus.goldragon.criome` resolves to
  `200:17f7:4fad:e50b:a50c:2048:2169:41f7` over `yggTun`; the direct route is
  `192.168.18.95 via 10.18.0.1 dev wlp0s20f3`.
- Strict noninteractive SSH succeeded for both `root@192.168.18.95` and
  `root@zeus.goldragon.criome`; each returned `hostname=zeus` and
  `kernel=Linux 7.0.1`.
- The direct-IP key is present in the user known-hosts file and the DNS name is
  present in the global known-hosts file. Both fetched Ed25519 keys have
  fingerprint `SHA256:5w4Jj0zqvfZdiGmJLCTKOG6JdXSdMCf3OaBd4EY65Mk`.
- `nix store info` succeeded through both explicit `ssh-ng` URIs and returned
  `Version: 2.34.6` and `Trusted: 1`.

Inference: at this observation time both configured endpoints are reachable,
strictly host-key authenticated, and identify the same target with high
confidence: both return the same hostname and the same public host-key
fingerprint. A host-key match alone is not a cryptographic proof that no
intermediate address translation or cloned endpoint exists.

Unknown: no target-side deployment or Lojix generation record is implied by
transport reachability or `nix store info`.
