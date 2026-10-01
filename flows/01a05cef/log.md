# Flow 01a05cef

Bounded read-only transport and ancestry witness for the current Zeus rollout.

Settled: reject `ssh-ng://root@192.168.18.95` because it is the user's LAN route. The current non-LAN pair is store URI `ssh-ng://root@zeus.goldragon.criome` and SSH destination `root@zeus.goldragon.criome`. The hostname resolves to `200:17f7:4fad:e50b:a50c:2048:2169:41f7` through `yggTun`; strict root SSH identifies `zeus` and host-key fingerprint `SHA256:5w4Jj0zqvfZdiGmJLCTKOG6JdXSdMCf3OaBd4EY65Mk`; `nix store info` returns Nix `2.35.1`, `Trusted: 1`.

Current pushed CriomOS `main` is `2929538c510ce2f84bf5317cfe21f450d5140b9d`; it pins CriomOS-home `cf21965b7934364fcd6edf3edcbedf60a72d5972`. Home ancestry includes `b04edb442f522e0b0588d661e93c109554ba2962` (ChatGPT resolver), `a74adda5f4afb894f5649fbcae0b8e025da9820b`, `35013ded85cb8a4beb9ea2354abccd3e3efffb8b`, and current `cf21965b` (Wispr medium tier). Goldragon Bird profile data is a separate immutable input at `2a139455ba6d2f71c3ba60bf56452c0be446f0d3`; it is not a CriomOS commit ancestor.

Observation: ordinary query for deployment 125 returned terminal `Some.Succeeded` for immutable source `7b9d0880dbc28c94acb305eef371218c14e227ea`; this is recorded without inferring any additional activation state.
