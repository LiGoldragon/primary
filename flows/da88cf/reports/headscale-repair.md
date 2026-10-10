# Headscale / tailscale repair — topology, cause, declarative proposal

Subflow of da88cf, read-only, 2026-09-25 ~21:20 CST (ouranos clock). Nothing was changed on any machine or repository. Grades: **Observed** = seen by this subflow in a command's output or a file; **Inferred** = reasoned from observations; **Unknown** = not established. Claims relayed from other seats are marked **Claimed**.

Repositories read at: CriomOS `19d5736`, CriomOS-home `478b4ea0`, goldragon `8c4d03d`, horizon-rs `8c11dfa`, lojix `c4bba4f`, CriomOS-lib `6e3bcb0`.

---

## 1. Topology

### 1.1 Where Headscale runs

- **Observed.** `goldragon/cluster-definition.datom`: **ouranos** carries `TailnetClient.{}` and `TailnetController.{}`. It is the only node with `TailnetController`. horizon-rs `lib/src/projection/node.rs:117` refuses a cluster with more than one controller.
- **Observed.** The module is `CriomOS/modules/nixos/network/headscale.nix`, gated on the `tailnetController` capability. Its settings:
  - `server_url = https://${node.criomeDomainName}:${constants.network.headscale.port}`, where the port is `8443` (`CriomOS-lib/lib/default.nix:109`).
  - Direct TLS with `tls_cert_path=/var/lib/headscale/tls/headscale.crt`.
  - `dns.magic_dns=true`, `base_domain = horizon.tailnetBaseDomain` (`tailnet.goldragon.criome`).
  - Firewall opens TCP 8443.
- **Observed.** The running config `/nix/store/15xv63x2…-headscale.yaml` has these values:
  - `server_url: https://ouranos.goldragon.criome:8443`
  - `listen_addr: 0.0.0.0:8443`
  - `derp.urls: https://controlplane.tailscale.com/derpmap/default`, so it uses Tailscale Inc.'s DERP relays and map.
  - `unix_socket: /run/headscale/headscale.sock`
- **Observed.** The unit runs `headscale-0.29.3` and has been active since 2026-09-10 13:33 CST.
- **Observed.** The certificate is made by a oneshot, `headscale-selfsigned-cert.service`, that runs before headscale:

  ```
  if [ -s "$certFile" ] && [ -s "$keyFile" ]; then
    exit 0
  fi
  ... openssl req -x509 ... -days 3650 -subj "/CN=$fqdn" -addext "subjectAltName=DNS:$fqdn,DNS:localhost,IP:127.0.0.1[,IP:<primary v4>]"
  ```

  Its comment says: "Self-signed cert for Phase 1; will be replaced with real PKI later."
- **Observed.** The served certificate (`openssl s_client -connect ouranos.goldragon.criome:8443 -servername ouranos.goldragon.criome`; identical on `127.0.0.1:8443`):

  ```
  subject=CN=ouranos.maisiliym.criome
  issuer=CN=ouranos.maisiliym.criome
  notBefore=Mar 13 04:01:58 2026 GMT
  notAfter=Mar 10 04:01:58 2036 GMT
  serial=23CF136582065748A1A8C882DB0178CD394D5D9A
  SAN: DNS:ouranos.maisiliym.criome, DNS:localhost, IP:127.0.0.1, IP:192.168.0.18
  sha256=CB:89:EF:91:53:E2:D7:EA:2B:18:F3:7F:FB:59:44:06:61:8F:17:82:2D:E1:8D:D0:6A:FA:DB:CB:7A:63:82:4F
  ```

  The certificate is self-signed and was issued under the **old cluster name `maisiliym`**. It does **not** carry `ouranos.goldragon.criome`, which is the current `server_url` host. It was issued on 2026-03-13, before the CriomOS rewrite began on 2026-04-23 (`eff6eea`).
- **Inferred.** The oneshot's `exit 0 if file exists` guard has kept the March certificate across the cluster rename. The declared SAN list has never reached the served certificate since then.

### 1.2 Tailnet clients in cluster data

| Node | TailnetClient | TailnetController | trust (cluster data) | reachable tonight |
|---|---|---|---|---|
| ouranos | yes | **yes** | Max | local |
| prometheus | yes | – | Max | ssh ok |
| mirror-alpha (TestVm on prometheus) | yes | – | not listed | network unreachable |
| mirror-beta (TestVm on prometheus) | yes | – | not listed | network unreachable |
| vm-testing (TestVm on prometheus) | yes | – | Max | network unreachable |
| tiger | – | – | Max | ssh timed out |
| zeus | – | – | Max | ssh ok; tailscaled `inactive` (consistent: not a client) |
| balboa | – | – | Max | name does not resolve |

- **Observed.** The client module is `CriomOS/modules/nixos/network/tailscale.nix`. It contains only this:

  ```nix
  # Phase 1 scaffolding only: enrollment remains manual.
  services.tailscale = { enable = true; openFirewall = true; };
  ```

  There is no `authKeyFile`, no `--login-server`, and no trust anchor. `services.tailscale` is not wrapped in any other way in CriomOS.
- **Observed.** No CA is declared anywhere in CriomOS or CriomOS-home: `grep security.pki|certificateFiles` returns nothing in `modules/`. The only cluster PKI is `clavifaber`, a GPG Ed25519 CA used for Wi-Fi EAP-TLS (`modules/nixos/router/wifi-pki.nix`, `network/wifi-eap.nix`). Its CA certificate is not placed in any trust store either.

### 1.3 What the tailnet is used for, in code and in the living's words

- **Observed, in code:**
  - `dnsmasq.nix:143` forwards `/tailnet.goldragon.criome/` to MagicDNS `100.100.100.100` when headscale is enabled.
  - `mirror.nix` binds the mirror daemon to `tailscale0` and orders it after `tailscaled`. It is force-disabled on all hosts (primary-h945.1).
  - `persona-router.nix` names its listen address `tailnetListenAddress`, but it binds `0.0.0.0:7440` on the global firewall.
  - Nothing in the build path uses the tailnet. Builders are reached as `prometheus.goldragon.criome` → `200:ca41:…` (Yggdrasil, from `/etc/hosts`).
  - **Inferred:** tonight the tailnet carries **no working function**. It is scaffolding for future Persona/mirror/Mentci traffic.
- **The living's words, verbatim:**
  - `flows/6cc91b/vision/network.md` (2026-09-13, STT):
    > We're going to have this tailnet identity-based network, super efficient, IPv6 internal, with intelligent subnet/subnetworks with IP4 to IP6 on the gateway server. Anybody can be a gateway that has enough features. […] If it gets a network and a working internet connection, it creates its VPN to the cloud nodes, and it gives this internal IPv6 to the internal tailnet network.
  - `flows/b05237/vision/operational-unityTailnetApp.md` (2026-09-18):
    > Let's just use Unity with a Tailnet mesh network and a server for connecting nodes, like a closed network. […] you have your Telnet public key already registered after you connect the first time, which could be done through the server, I guess. […] It doesn't have to be bulletproof, but it's going to be secure enough.
  - `flows/c8d79f/vision/operational-mentci.md` (2026-09-18 21:52, typed):
    > We would run the server on a trusted node, and then Tailnet authentication, I guess. […] Unity Slint app, which is a client that connects with Tailnet and has to request access if it's a new key.
  - `flows/c8d79f/vision/operational-criomeClusterIsTheTailnet.md` (2026-09-19):
    > The criome cluster is the trusted network, and that's the tailnet. Those are the trusted nodes based on the trust value there in the cluster.
  - `flows/e1953c/vision/mesh.md` (STT):
    > it can combine itself with the networking protocol that we're going to do, tailnet-based. […] Maybe it's called Mesh
  - `flows/00f95a/vision/prometheus-zeus-mesh-possibilities.md` (2026-09-24T23:44Z):
    > Maybe there's a tailnet kind of mesh out there. […] like internet propagation and domain name resolution of your own choosing type thing that already exists and that I'm wasting my time trying to emulate.
  - `flows/da88cf/vision/prometheus.md` (relayed, ~21:50):
    > Why was it working before? Would it help if I rebooted it? We need to use Prometheus.
  - `flows/da88cf/vision/clusterData.md` / `flows/e71dab/vision/tailscale.md` (2026-09-25 ~22:05, STT with corrections):
    > Okay well, you can get that Tailscale problem figured out and fixed. Make sure you follow the topology of the cluster, data, and administrator roles and features in order to add data in order to know which host does what. I leave it to Fable's best judgment […]
- **Inferred, discrepancy.** The living ties tailnet membership to the cluster **trust** value. In the data, tailnet membership is a separate `TailnetClient` capability, and the two sets disagree:
  - tiger, zeus and balboa are trust Max but not clients.
  - mirror-alpha and mirror-beta are clients but absent from the trust list.

---

## 2. Cause

### 2.1 Journal evidence on ouranos

The whole `tailscaled` journal is saved at `scratchpad/headscale-repair/ouranos-tailscaled.journal`: 646,339 lines, retained from 2026-06-05. The system journal as a whole starts 2026-05-31.

- **Observed, first retained tailscaled boot** (2026-06-05T07:00:46-06:00):

  ```
  pm: using backend prefs for "profile-bd89": Prefs{ra=false dns=false want=true routes=[] statefulFiltering=false nf=on url="https://127.0.0.1:8443" host="ouranos" update=check Persist{o=, n=[HPa9Y] u="li" ak=-}}
  control: client.Login(0)
  tlsdial: error: server cert for "" failed both system roots & Let's Encrypt root validation
  ```

- **Observed, from the `-14d` window onward and still current:**

  ```
  Sep 11 21:19:59 ouranos tailscaled[1482]: control: doLogin(regen=false, hasUrl=false)
  Sep 11 21:19:59 ouranos tailscaled[1482]: Received error: fetch control key: Get "https://127.0.0.1:8443/key?v=142": x509: certificate signed by unknown authority
  ```

- **Observed, counts over the whole retained journal:**
  - `loggedIn=true` appears **0** times.
  - `Received error: fetch control key …` appears about 309,550 times.
  - All 17 prefs lines carry `url="https://127.0.0.1:8443"`.
  - 30 daemon starts: v1.96.5 until 2026-07-28, then v1.102.2 from 2026-08-14. Every start fails the same way.
- **Observed.** `tailscale debug prefs` now shows:
  - `ControlURL: https://127.0.0.1:8443`, `WantRunning: true`, `LoggedOut: false`
  - Persisted `UserProfile {ID 1, LoginName "li"}`, `NodeID "2"`
  - `tailscale status` health: "You are logged out. The last login error was: fetch control key: … x509: certificate signed by unknown authority". BackendState is `NoState`.
- **Observed.** On the server side, the headscale journal (310,533 lines, from 2026-06-05) shows:
  - `TLS handshake error from 127.0.0.1: remote error: tls: bad certificate` 309,433 times. This is ouranos's own tailscaled refusing the certificate.
  - One handshake from ouranos's own Yggdrasil address on 2026-09-19: `local error: tls: bad record MAC`.
  - **No other peer address has ever reached Headscale** in the retained window.
  - Separately, Headscale crashed at start about 29 times with `getting DERPMap: Get "https://controlplane.tailscale.com/derpmap/default": … x509: certificate is valid for *.wifiplex.com, wifiplex.com, not controlplane.tailscale.com`. This happened on 2026-09-10, behind a captive portal. It is transient and unrelated, but it shows Headscale refuses to start without Tailscale Inc.'s DERP map.
- **Observed.** The `headscale-selfsigned-cert` journal on every boot shows only start, finish and resource lines, with no openssl output. **Inferred:** the certificate was never regenerated in the retained window, which is consistent with its 2026-03-13 notBefore. The certificate **did not change**.

### 2.2 Trust store

- **Observed.** `/etc/ssl/certs` on ouranos contains only `ca-bundle.crt` and `ca-certificates.crt` (symlinks to `/etc/static`, 121 certificates). No subject in the bundle matches `criome|goldragon|maisiliym|ouranos`. `trust` is not installed. `ls /etc/ssl/certs | grep -i -E 'criome|headscale|goldragon'` is empty on ouranos and on prometheus.
- **Observed.** No CriomOS module declares `security.pki.certificateFiles`/`certificates`.

### 2.3 State of the other client

- **Observed, prometheus:**
  - `tailscaled` active since 21:15:50 CST (after the living's power-on), Status "Needs login".
  - `BackendState: NeedsLogin`
  - `tailscale debug prefs`: `ControlURL: ""`, `WantRunning: false`, `LoggedOut: true`
  - Its journal (from 2026-06-08) contains no `url=` prefs line and no `loggedIn=true`.
  - **Inferred:** prometheus has **never been enrolled** with this Headscale in the retained window. With an empty ControlURL, a manual `tailscale up` would default to Tailscale Inc.'s control plane.

### 2.4 Why did it work before? Candidates, with grades

What "it" is matters.

1. **The ouranos→Prometheus link that the living asked about was never the tailnet.**
   - Observed: builds go over `prometheus.goldragon.criome` → `200:ca41:6b12:fba:…` (from `/etc/hosts`, Yggdrasil).
   - Observed: Headscale has never seen Prometheus.
   - Claimed by 88475f: builds resumed once Prometheus was powered on, with the tailnet still down.
   - **Grade: strong (observed plus claimed).** The build outage was the power-off. The tailnet did not cause it.
2. **The tailnet itself has not worked since at least 2026-06-05.** Grade: observed. This is the full journal retention, and no login succeeded in it.
3. **It did work once, before 2026-06-05.**
   - Observed: ouranos's persisted profile holds `UserProfile ID 1 "li"` and `NodeID 2`. A registration succeeded at some point, and node ID 2 implies at least one node registered before it.
   - How TLS was accepted then is **Unknown**. Candidates, none evidenced:
     - (a) in the older `maisiliym`-era system (criomos-archive, not present locally), the certificate or its issuer was in the trust store or given through `SSL_CERT_FILE` to tailscaled;
     - (b) the node was registered through a different URL or path, and prefs were later hand-set to `https://127.0.0.1:8443`;
     - (c) an older tailscale client or a debug environment knob relaxed verification.
   - Which node was ID 1 is **Unknown**. `headscale nodes list` was denied (see §3).
4. **Hand-set control URL.** The prefs `url="https://127.0.0.1:8443"` with `u="li"` can only come from a manual `tailscale up --login-server …`; no module sets it. **Grade: inferred, strong.**

---

## 3. Live state per node (read-only)

| | ouranos | prometheus | zeus |
|---|---|---|---|
| tailscaled unit | active since 2026-09-10 13:29 | active since 2026-09-25 21:15:50 | inactive |
| BackendState | `NoState` | `NeedsLogin` | – |
| ControlURL | `https://127.0.0.1:8443` (hand-set) | `""` (never set) | – |
| Last error | x509 unknown authority | none (never tried) | – |
| headscale unit | active, v0.29.3 | – | – |

- `headscale nodes list` as `li` failed with `open /run/headscale/headscale.sock: permission denied`. `sudo -n headscale nodes list` failed with `sudo: a password is required`. **Headscale's node list is Unknown**, and so is its user list, which the preauth key needs.
- `/var/lib/headscale` (0750 headscale) and `/var/lib/tailscale` are unreadable to `li`. The key files were not touched.
- tiger timed out; the mirror/vm-testing guests were network-unreachable; balboa does not resolve.
- **Side observation.** ouranos tailscaled uploads its logs to Tailscale Inc.'s log service (`logtail: upload succeeded…`, `429: rate limited`). This is the upstream default. The upstream option `services.tailscale.disableUpstreamLogging` exists and CriomOS does not set it.

---

## 4. Declarative repair proposal

The fix has three parts: trust, name, and enrollment. All three are needed. Fixing trust alone still fails, because the SAN does not carry `ouranos.goldragon.criome`. Fixing the name alone still fails, because the certificate stays self-signed and untrusted.

### 4a. Trust: a fork (no verdict)

**Fork A: a cluster-internal CA, declared into every node's trust store.**
- Shape:
  - A cluster CA certificate (public) is authored as cluster data or as a file in goldragon.
  - Every node gets `security.pki.certificateFiles = [ <clusterCa.pem> ]` through a CriomOS module.
  - The controller's server certificate is issued by that CA with SAN `DNS:<criomeDomainName>` (plus `localhost`, `127.0.0.1` if wanted). Its **private key** is a sops secret for the controller only.
  - Candidate CA: the existing `clavifaber` GPG Ed25519 CA (already used for Wi-Fi EAP-TLS). Go's x509, which tailscaled uses, accepts Ed25519.
- For: no public DNS; works over Yggdrasil and offline; `goldragon.criome` stays private; one CA can serve Wi-Fi, Headscale and later Mentci/Persona TLS; fits "the criome cluster is the trusted network".
- Against:
  - A CA trusted system-wide can mint a certificate for *any* name that all nodes' browsers and tools would accept. Mitigation: X.509 name constraints (`permitted;DNS:.criome`). clavifaber would need to support these (Unknown whether it does).
  - Creating the CA and server key is new secret material.
  - Certificate rotation becomes our job.
  - The trust anchor must be deployed to a node before that node can enroll.

**Fork A′ (narrower variant): pin only the Headscale certificate, not a CA.**
- Shape: add only the server certificate itself to `security.pki.certificateFiles`. Go accepts a self-signed leaf placed in the root pool.
- For: no CA power.
- Against: the certificate must be stable and public in the repository, so the current "generate on first boot" oneshot must go and the key becomes a sops secret. Regeneration breaks all clients.

**Fork B: a publicly trusted certificate (ACME).**
- Name situation:
  - **Observed:** `goldragon.criome` is not public DNS. `.criome` is not a public TLD; `goldragon.criome` does not resolve; `ouranos.goldragon.criome` resolves only through `/etc/hosts`.
  - **Observed:** `criome.net` is public (Cloudflare A/AAAA records). `goldragon.criome.net` does not resolve.
  - Therefore ACME would need a new public name, e.g. `headscale.criome.net` or `tailnet.goldragon.criome.net`.
  - ouranos is a laptop behind NAT (`192.168.1.1` resolver, captive portals seen), so HTTP-01 would not work. **DNS-01 via the Cloudflare API** would be needed, which is a Cloudflare API token as a new secret on ouranos.
- For: no trust-store changes; any stock client (phones, Unity/Android) trusts it; this fits "Unity Slint app … connects with Tailnet" from non-CriomOS devices.
- Against:
  - The control-plane name becomes public in DNS and in Certificate Transparency logs.
  - It depends on Cloudflare and Let's Encrypt.
  - A new third-party credential is needed.
  - The public name must resolve to wherever ouranos is. Headscale's `server_url` must be reachable by clients, and ouranos roams, so it would need dynamic DNS or a Yggdrasil-only AAAA record.
  - It moves against the private-part direction in CLAUDE.md, although that part is not active.

**Fork C (worth naming): move the controller.**
- The controller is a laptop that roams and sleeps. A "Center"/"Router" node such as prometheus, which is always on, may better match "a server for connecting nodes".
- This is a cluster-data change: move `TailnetController` to prometheus. It is the living's topology decision, and it is independent of A or B.

### 4b. Enrollment: non-interactive, secret-backed

**How secrets reach programs here (observed):**
- Ciphertext lives in `goldragon/secrets/*.sops`. It is age-encrypted to each consuming host's age key, which is derived from `/etc/ssh/ssh_host_ed25519_key` (`CriomOS/modules/nixos/secrets.nix`).
- Lojix passes it as `inputs.secrets.sopsFiles.<name>` from a caller-owned `SecretsDirectory` (lojix README/UPGRADES).
- sops-nix decrypts it at activation to `/run/secrets/<name>`, and a module consumes `config.sops.secrets.<name>.path`.
- Precedent: `localLlmApiToken`, which was "minted into gopass, encrypted to this host's age key […] decrypted to /run/secrets only on activation", and `opencodeServerPassword` (`LoadCredential`).
- The `secrets` skill's rules apply: the producer is piped straight to the consumer's own stdin or file interface; nothing goes through argv, environment, command substitution, temporary files, `tee` or filters; secret-bearing output is suppressed.

**The consuming option:**
- Upstream `services.tailscale.authKeyFile` (nixpkgs `tailscale.nix:80`) creates `tailscaled-autoconnect.service`. It runs:

  ```
  tailscale up --auth-key "$(cat ${cfg.authKeyFile})${params}" ${extraUpFlags}
  ```

  **This puts the key in `tailscale`'s argv**, which the skill forbids and which is visible in `/proc`.
- The tailscale client itself supports `--auth-key=file:<path>` (observed in `tailscale up --help`: "if it begins with "file:", then it's a path to a file containing the authkey").
- Therefore CriomOS should **not** use upstream `authKeyFile`. Its script puts the file's content into argv whatever the file holds. Instead, CriomOS declares its own oneshot that runs `tailscale up --login-server=https://<controller criomeDomainName>:8443 --auth-key=file:${config.sops.secrets.tailnetAuthKey.path} --hostname=<node.name>`. This keeps the key out of argv.
- The login server must be derived from Horizon: the node with `TailnetController`. Clients cannot see that today, because the CriomOS fixture's `exNodes` does not expose capabilities. **Unknown:** whether live Horizon exposes other nodes' capabilities to a client node. If it does not, horizon-rs needs a `tailnetControllerUrl` / `tailnet.controlUrl` projection field, similar to the existing `tailnetBaseDomain`.
- **Inferred caveat.** ouranos is in `NoState` with a hand-set ControlURL. The upstream autoconnect loop only acts on `NeedsLogin|NeedsMachineAuth|Stopped`. The own oneshot must handle a changed login server, which needs `--force-reauth` or `--reset`. That is to be verified against tailscale 1.102 in a VM test before deploy.

**The secret itself:**
- Headscale 0.29 has no declarative preauth key. A key is minted by `headscale preauthkeys create --user <ID> [--reusable] [--expiration …] [--tags …]` on the controller, as root or the headscale group.
- One reusable, tagged key could be sops-encrypted to all `TailnetClient` hosts' age recipients. The alternative is one key per node, which is safer but means N secrets.
- The living's hands (or an approved path) are needed once. Blind minting that satisfies the skill looks like this, on ouranos, as root:

  ```
  set -o pipefail
  headscale preauthkeys create --user <ID> --reusable --expiration <E> --tags tag:cluster \
    | gopass insert -f goldragon.criome/headscale-preauth-key >/dev/null
  gopass show -o goldragon.criome/headscale-preauth-key \
    | sops encrypt --age <recipients…> --input-type binary --output-type json \
        --filename-override secrets/tailnetAuthKey.sops /dev/stdin > secrets/tailnetAuthKey.sops
  ```

  The ciphertext goes to the file and nothing plain is printed. Per the skill, **first verify** two things:
  - that headscale 0.29 prints only the key on stdout in its default output (no `-o json` plus a filter);
  - that the installed sops accepts `/dev/stdin` with `--filename-override`.
- Recipients are derived from the nodes' public ssh host keys in cluster data (`ssh-to-age`). This is public data, not a secret.
- **Headscale's user ID is Unknown** (the node list was denied). The key's user must exist. Persisted profile `ID 1 "li"` suggests user 1 is `li`.
- Also: the controller's TLS **private key** under Fork A/A′, and a Cloudflare token under Fork B, are further secrets. No secret may be created before the living's word.

### 4c. Files that would change (sketch)

Fork A is shown. Fork B replaces the PKI parts with `tls_letsencrypt_*` settings plus a DNS-01 credential, or with an ACME module.

**goldragon** (cluster data, public plus ciphertext):

```
cluster-definition.datom   # possibly: move/confirm TailnetController; align TailnetClient with trust (question Q4)
clusterCa.pem              # NEW, public CA cert (or a Horizon field carrying it)          [Fork A]
secrets/headscaleTlsKey.sops  # NEW, controller server key, recipient = controller only  [Fork A/A′]
secrets/headscaleTlsCert…  # server cert is public — could be plain file, not sops
secrets/tailnetAuthKey.sops   # NEW, recipients = every TailnetClient host
```

**CriomOS** `modules/nixos/network/headscale.nix`:

```diff
-  systemd.services.headscale-selfsigned-cert = { … openssl req -x509 … exit 0 if exists … };
-  systemd.services.headscale.requires/after = [ "headscale-selfsigned-cert.service" ];
+  sops.secrets.headscaleTlsKey = { sopsFile = inputs.secrets.sopsFiles.headscaleTlsKey;
+    owner = config.services.headscale.user; mode = "0400"; restartUnits = [ "headscale.service" ]; };
+  services.headscale.settings.tls_cert_path = <declared cert (store path; public)>;
+  services.headscale.settings.tls_key_path  = config.sops.secrets.headscaleTlsKey.path;
+  assertions = [ { assertion = inputs.secrets.sopsFiles ? headscaleTlsKey; message = …; } ];
```

**CriomOS** `modules/nixos/network/tailscale.nix`:

```diff
-  # Phase 1 scaffolding only: enrollment remains manual.
   services.tailscale = { enable = true; openFirewall = true;
+    disableUpstreamLogging = true;          # question Q6
+  };
+  security.pki.certificateFiles = [ <clusterCa.pem from horizon/goldragon> ];   # Fork A
+  sops.secrets.tailnetAuthKey = { sopsFile = inputs.secrets.sopsFiles.tailnetAuthKey; mode = "0400"; };
+  systemd.services.tailnet-enroll = {        # argv-free: --auth-key=file:
+    after = [ "tailscaled.service" "network-online.target" ]; wants = [ "tailscaled.service" ];
+    wantedBy = [ "multi-user.target" ];
+    serviceConfig.Type = "oneshot";
+    script = ''
+      state=$(tailscale status --json --peers=false | jq -r .BackendState)
+      case "$state" in Running) exit 0;; esac
+      exec tailscale up --login-server=${controlUrl} --hostname=${node.name} \
+        --auth-key=file:${config.sops.secrets.tailnetAuthKey.path} --force-reauth
+    '';
+  };
```

Here `controlUrl` comes from a new or existing Horizon field; hard-coding a node name is forbidden by CriomOS AGENTS.md ("No node-name logic").

**horizon-rs**, if needed: expose the controller's control URL (or domain) to client nodes' projection, and carry the cluster CA reference.

**CriomOS** `checks/headscale-selfsigned-cert/`: replace with a check that asserts:
- the server certificate's SAN contains the controller's `criomeDomainName`;
- the key path is a sops path;
- clients carry the CA and the enroll unit, with no `$(cat` in any unit script.

A NixOS VM test (controller plus one client) would witness enrollment end to end with a test-only key.

**Who lands it:**
- Field lands it. Per the da88cf log, b7da5d (Field Sol) holds for this design brief.
- horizon-rs changes, if any, are Mind-side producer work first, then CriomOS consumes them.
- Deploy is through Lojix, `Horizon.{… <node> CompleteHost SecretsDirectory.{/git/github.com/LiGoldragon/goldragon/secrets} github:LiGoldragon/CriomOS/<rev> x86_64-linux …}`. Order:
  1. **controller first** (ouranos), so the trusted, SAN-matching certificate is served;
  2. then clients (prometheus).
- Per CriomOS ARCHITECTURE, prometheus is a large-AI node, so it gets **`BootOnce`, not a live `Switch`**, unless out-of-band access is confirmed.
- Builds run on prometheus per the living's order.

---

## 5. Decidable tonight versus needs the living

**Decidable without the living (no secret created, nothing activated):**
- Write the CriomOS change on a branch:
  - the SAN from the current domain, removing the stale-certificate guard or making the certificate follow the name;
  - the argv-free enroll unit shape;
  - checks;
  - a VM test with throwaway test keys generated inside the test.
- Write the horizon-rs projection field for the control URL if needed.
- State plainly to the living that the tailnet has not worked since at least June, and that it did not cause tonight's build outage.

**Needs the living's word (exact questions):**
1. **Trust fork.** "Should the Headscale certificate be issued by a cluster CA that every node trusts (private, e.g. clavifaber), or by Let's Encrypt under a public name such as `headscale.criome.net`?" Example: under the CA, your phone's Unity app must install the cluster CA; under Let's Encrypt, the name `headscale.criome.net` becomes publicly visible and ouranos needs a Cloudflare token.
2. **Secrets.** "May we create these secrets, and who mints them?"
   - (a) one Headscale preauth key (reusable? tagged? expiry?);
   - (b) the Headscale TLS private key (or CA key);
   - (c) under Fork B, a Cloudflare DNS token.

   Example: "run `sudo headscale preauthkeys create --user 1 --reusable --expiration 8760h | gopass insert -f goldragon.criome/headscale-preauth-key` once, or approve an agent to run it through the gopass-to-sops pipe." `sudo` on ouranos needs your password; agents cannot mint it now.
3. **One key or many.** "One reusable key shared by all tailnet hosts, or one key per host?" Example: a leaked shared key admits any machine until it expires; per-host keys mean N secrets to mint.
4. **Who is in the tailnet.** You said "those are the trusted nodes based on the trust value there in the cluster". Should tailnet membership derive from trust, or stay a separate `TailnetClient` role? Example: tiger and zeus are trust Max but not tailnet clients; mirror-alpha and mirror-beta are tailnet clients but have no trust entry.
5. **Where the controller runs.** "Keep Headscale on ouranos (laptop, roams, sleeps) or move `TailnetController` to prometheus (always-on Center/Router)?"
6. **Tailscale Inc. dependencies.** "Stop tailscaled sending logs to Tailscale Inc. (`disableUpstreamLogging`), and keep or replace Tailscale's public DERP relays?" Example: Headscale refused to start 29 times on 2026-09-10 because it could not fetch Tailscale's DERP map behind a hotel-style portal.
7. **Reset of the hand-set state.** "May the first deploy force-reauthenticate ouranos (drop the hand-set `127.0.0.1` login and node ID 2)?" This is a one-time non-declarative state change done by the declared unit.
