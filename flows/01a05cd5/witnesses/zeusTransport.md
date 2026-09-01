Subject: Current non-LAN Zeus Lojix deployment transport and immutable source ancestry.

Method: probe `getent ahosts zeus.goldragon.criome`; `ip -6 route get 200:17f7:4fad:e50b:a50c:2048:2169:41f7`; `ip route get 192.168.18.95`; strict `ssh -o BatchMode=yes -o ConnectTimeout=8 -o ConnectionAttempts=1 -o StrictHostKeyChecking=yes root@zeus.goldragon.criome 'hostname; hostname -f; uname -sr; ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub'`; and `NIX_SSHOPTS='-o StrictHostKeyChecking=yes -o BatchMode=yes -o ConnectTimeout=8 -o ConnectionAttempts=1 -o LogLevel=ERROR' nix store info --store ssh-ng://root@zeus.goldragon.criome`.

Observed on 2026-09-01:

- `zeus.goldragon.criome` resolves to `200:17f7:4fad:e50b:a50c:2048:2169:41f7`; the route is `dev yggTun` with local Ygg source `201:6de1:5500:7cac:2db9:759e:42d2:fb1d`.
- `192.168.18.95` routes via `10.18.0.1 dev wlp0s20f3`; this is the rejected LAN route.
- Strict root SSH returned `hostname=zeus`, `fqdn=zeus`, `kernel=Linux 7.1.8`, and host-key fingerprint `SHA256:5w4Jj0zqvfZdiGmJLCTKOG6JdXSdMCf3OaBd4EY65Mk`.
- The Nix store probe returned `Store URL: ssh-ng://root@zeus.goldragon.criome`, `Version: 2.35.1`, and `Trusted: 1`.
- Therefore the transport pair is `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)`.

Method: probe `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByDeployment.(125)'`.

Observed: deployment 125 returned source `7b9d0880dbc28c94acb305eef371218c14e227ea`, terminal marker `Completed Some.(3161 3161) Some.Succeeded`, and query marker `(3165 3165)`. This does not establish that the stale LAN transport is suitable for a new request.

Method: probe GitHub REST `branches/main`, `commits/<sha>`, `compare/<base>...<head>`, and `contents/flake.nix`/`contents/flake.lock` for `LiGoldragon/CriomOS`, `CriomOS-home`, and `goldragon`.

Observed:

- CriomOS `main`: `2929538c510ce2f84bf5317cfe21f450d5140b9d`, subject `Pin the medium-tier Wispr Flow profile`, parent `7b9d0880dbc28c94acb305eef371218c14e227ea`.
- CriomOS ancestry continues `7b9d0880dbc28c94acb305eef371218c14e227ea` (`Pin the repaired CriomOS Home profile`) to `69a946b1d0e522d6ad04162a497992641c87bcfb` (`Pin CriomOS-home ChatGPT resolver candidate`).
- At that CriomOS tip, `flake.nix` pins Home `cf21965b7934364fcd6edf3edcbedf60a72d5972`; `flake.lock` records `narHash = sha256-UEKAxF3urk4bw6PM6M6+QHIE72sN5bbdaDYjmRdLqTQ=`.
- CriomOS-home `main`: `cf21965b7934364fcd6edf3edcbedf60a72d5972`, subject `Place Wispr Flow in the medium profile tier`, parent `35013ded85cb8a4beb9ea2354abccd3e3efffb8b`.
- Home ancestry continues `35013ded85cb8a4beb9ea2354abccd3e3efffb8b` (`Check Wispr Flow profile-tier selection`) to `a74adda5f4afb894f5649fbcae0b8e025da9820b` (`Make Wispr Flow a maximum-profile package`) to `b04edb442f522e0b0588d661e93c109554ba2962` (`Restore ChatGPT shared-daemon resolver candidate`).
- Goldragon `main`: `2a139455ba6d2f71c3ba60bf56452c0be446f0d3`, subject `align Bird profile tier with Li`; its `proposal.datom` projects `bird Max` and `zeus Max`. This is a separate immutable proposal input, not a CriomOS commit ancestor.

Inference: `github:LiGoldragon/CriomOS?rev=2929538c510ce2f84bf5317cfe21f450d5140b9d` is the exact pushed CriomOS source revision that pins the Home line containing both the Wispr medium-tier correction and the ChatGPT Desktop resolver fix. The Bird profile correction is combined only when the deployment also consumes the separate Goldragon proposal revision `2a139455ba6d2f71c3ba60bf56452c0be446f0d3`.
