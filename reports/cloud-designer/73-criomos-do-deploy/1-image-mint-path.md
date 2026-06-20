# CriomOS → DigitalOcean: the image-mint path (Lane A)

*cloud-designer report 73 · 2026-06-20 · LIVE-verified against the real DO
account via `gopass digitalocean.com/api-token`.*

## TL;DR

**Pick Lane 2 (nixos-infect on a stock Ubuntu droplet → snapshot → private
image id) as primary, Lane 3 (nixos-anywhere kexec) as the higher-fidelity
variant. Reject Lane 1 (custom-image-by-URL) for two independent reasons.**

But the headline finding is a **hard blocker that gates all three lanes today**:
the DO token at `digitalocean.com/api-token` is **scoped read-mostly**. Live
probes show it can create/delete droplets and ssh keys, but **every
image-minting step returns `403 You are missing the required permission
image:create`** — including the droplet *snapshot* action. So:

- Lane 1 `POST /v2/images` (custom image by URL) → **403** (needs `image:create`).
- Lane 2 / Lane 3 `POST /v2/droplets/{id}/actions {type:snapshot}` → **403**
  (the snapshot action *also* needs `image:create`).

**No reusable pre-made image can be minted with the current token.** The first
action item is a token-scope fix (mint a new DO Personal Access Token with the
`image:create` + `image:read` write scopes, or a full-access token), stored at
the same gopass handle. Everything below assumes that fix; the command
sequences are exact and were validated up to the 403 wall.

Independently of scope, two **format constraints** would still sink Lane 1 even
with a write token, and they're why snapshot-based lanes win:

1. **DO custom images must boot BIOS — "UEFI boot is not supported. Custom
   images must boot using BIOS"** ([DO limits][do-limits]). The nixpkgs
   `digitalOceanImage` qcow2 must therefore be a BIOS/GRUB build; a UEFI
   `target` config silently produces an unbootable droplet.
2. **Lane 1 needs a publicly-fetchable URL** the DO importer can GET
   (HTTP/HTTPS/FTP) — there is no doctl-less, hosting-less path. Snapshot lanes
   need **zero hosting**: the bits never leave DO.

Lanes 2 and 3 inherit DO's already-working BIOS + DHCP + virtio droplet
environment by construction (you snapshot a machine DO already booted), so they
sidestep both the BIOS gotcha and the cloud-init/DHCP/networking guesswork.

## What was LIVE-verified (2026-06-20)

Account state (the prompt's premise — confirmed):

| Check | Endpoint | Result |
|---|---|---|
| Custom images | `GET /v2/images?private=true` | **0 images** |
| NixOS distro image | `GET /v2/images?type=distribution` | 16 distro images, **0 NixOS** |
| Ubuntu base for Lanes 2/3 | same | `ubuntu-24-04-x64` **present** (also 22-04, 25-10) |

Token scope (non-destructive probes — invalid POST body returns 422 if write is
allowed, 403 if the scope is absent; nonexistent-id returns 404 if write is
allowed):

| Operation | Probe | HTTP | Meaning |
|---|---|---|---|
| `account:read` | `GET /v2/account` | **403** | scoped token, no account read |
| `image:read` | `GET /v2/images` | 200 | read OK |
| `droplet:read` | `GET /v2/droplets` | 200 | read OK |
| `droplet:create` | `POST /v2/droplets {}` | 422 | **write OK** |
| `droplet:delete` | `DELETE /v2/droplets/999999999` | 404 | **write OK** |
| `ssh_key:create` | `POST /v2/account/keys {}` | 422 | **write OK** |
| **`image:create`** | `POST /v2/images {}` | **403** | **blocked** |
| **snapshot action** | `POST /v2/droplets/999999999/actions {snapshot}` | **403** | **blocked — body: "missing the required permission image:create"** |
| `image:delete` | `DELETE /v2/images/999999999` | 403 | blocked (snapshot cleanup also needs scope) |

These are the literal HTTP codes the in-process `HttpApi`
(`cloud/src/digitalocean.rs`) would receive — its `decode_call` /
`error_from_transport` path surfaces the same 403.

DO custom-image format facts (for completeness / Lane 1):

- Formats: **raw, qcow2, vhdx, vdi, vmdk**; compressed with **gzip or bzip2**;
  **< 100 GB decompressed** ([DO upload how-to][do-upload], [DO limits][do-limits]).
- **BIOS only, no UEFI**; droplets from custom images get networking via
  **DHCP on port 67** ([DO limits][do-limits]).
- nixpkgs `config.system.build.digitalOceanImage`
  (`nixos/modules/virtualisation/digital-ocean-image.nix`) emits **qcow2 + gzip
  by default** → `nixos.qcow2.gz`, configurable to `bzip2`
  ([nixpkgs module][do-image-module]). Format and compression already match
  DO's accepted set — verified against the module source.

## Why Lane 2/3 need no daemon schema change

`cloud/src/digitalocean.rs:431` — `DropletPayload.image` is a plain `String`
sourced from the typed `ImageName` (`spec.image.clone()` at `:448`). DO's
`/v2/droplets` accepts either a **distribution slug** (`ubuntu-24-04-x64`) or a
**numeric custom/snapshot image id** in that same field. So once a snapshot
mints a private image id, booting CriomOS from it is just
`ImageName::new("<numeric-id>")` through the existing `create_server` path — no
new wire type, no new endpoint on the create side. The *minting* side
(snapshot action + action poll) is the only new REST surface the daemon needs
(`digitalocean.rs` currently has `/v2/droplets`, `/v2/account/keys` only — no
`/v2/images`, no `/actions`).

## Lane comparison

| | Lane 1 image-by-URL | **Lane 2 nixos-infect → snapshot** | Lane 3 nixos-anywhere → snapshot |
|---|---|---|---|
| External hosting | **Required** (public URL) | **None** | **None** |
| BIOS/UEFI risk | Must hand-build BIOS qcow2 | Inherits DO BIOS | Inherits DO BIOS |
| Networking risk | Hand-match DHCP/cloud-init | Inherits DO DHCP | Inherits DO DHCP |
| Reproducible-as-code | Nix build is pure; upload step impure | infect script is the impurity | flake + disko is pure-ish; kexec impure |
| Config fidelity | Full CriomOS `target` | **Partial** — infect writes its own minimal config unless overridden | **Full CriomOS `target`** via chosen flake |
| RAM floor | n/a (build local) | low | **≥ 2.5 GB droplet for kexec** ([nixos-anywhere][na-quickstart]) |
| Blocked by token today | `image:create` (POST images) | `image:create` (snapshot) | `image:create` (snapshot) |
| Least external dependency | no | **yes** | yes (one more flake input: disko) |

**Lane 2 wins on "least external dependency"**: a single
`curl`-created Ubuntu droplet, one ssh command that runs the upstream
`nixos-infect` script, one snapshot action, one poll. No public file host, no
local kexec image build, no disko config. **Lane 3 wins on fidelity** — it
installs the exact CriomOS flake config (so the snapshot is already the real
system, not infect's bootstrap config), at the cost of a ≥2.5 GB droplet and a
`disko` disk-config. Recommended posture: **Lane 2 to prove the path end-to-end
fast; migrate to Lane 3 for the production golden image** because the snapshot
should capture the true `nixosConfigurations.target`, not nixos-infect's
generated config.

Caveat to verify live once the token is fixed: confirm the BIOS/GRUB profile of
the booted NixOS before snapshotting — DO custom *and snapshot* images boot
BIOS, and CriomOS `target` must not assume systemd-boot/UEFI on the DO node.
(Unverified: CriomOS `target`'s current bootloader default — `CriomOS/flake.nix`
exposes `nixosConfigurations.target` but the bootloader module wasn't inspected
in this pass.)

## Exact command sequence — Lane 2 (primary)

All `curl` hits the real REST API the daemon's `HttpApi` uses. Token is read
into a shell var and **never echoed**.

```bash
# 0. Token (scoped) — NEVER print it. After the scope fix this same handle
#    must carry image:create.
TOKEN=$(gopass show -o digitalocean.com/api-token)
API=https://api.digitalocean.com/v2
auth=(-H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json")

# 1. Ensure an ssh key DO can inject (write scope CONFIRMED, 422→ok).
#    Reuse the daemon's ensure_ssh_key logic, or directly:
PUBKEY=$(cat ~/.ssh/id_ed25519.pub)
curl -fsS "${auth[@]}" -X POST "$API/account/keys" \
  -d "{\"name\":\"criomos-mint\",\"public_key\":\"$PUBKEY\"}" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["ssh_key"]["fingerprint"])'
FINGERPRINT=...   # from above

# 2. Provision a stock Ubuntu droplet (write scope CONFIRMED). 2 GB+ is plenty
#    for infect; ubuntu-24-04-x64 verified present in this account.
curl -fsS "${auth[@]}" -X POST "$API/droplets" -d '{
  "name":"criomos-mint",
  "region":"nyc3",
  "size":"s-2vcpu-2gb",
  "image":"ubuntu-24-04-x64",
  "ssh_keys":["'$FINGERPRINT'"],
  "ipv6":true, "monitoring":true
}' | python3 -c 'import sys,json;d=json.load(sys.stdin)["droplet"];print(d["id"])'
DROPLET_ID=...    # from above

# 3. Poll until active + public IPv4 assigned.
until curl -fsS "${auth[@]}" "$API/droplets/$DROPLET_ID" \
  | python3 -c 'import sys,json;d=json.load(sys.stdin)["droplet"];
import sys;
nets=[n["ip_address"] for n in d["networks"]["v4"] if n["type"]=="public"];
print(nets[0] if d["status"]=="active" and nets else "");' | grep -q '[0-9]'; do
  sleep 10; done
IP=$(curl -fsS "${auth[@]}" "$API/droplets/$DROPLET_ID" \
  | python3 -c 'import sys,json;d=json.load(sys.stdin)["droplet"];print([n["ip_address"] for n in d["networks"]["v4"] if n["type"]=="public"][0])')

# 4. Convert in place to NixOS via upstream nixos-infect (the only impurity).
#    NIX_CHANNEL pins the release; PROVIDER=digitalocean wires DO specifics
#    (grub on /dev/vda, DHCP networking, the DO-detected config).
ssh -o StrictHostKeyChecking=accept-new root@$IP \
  'curl -fsSL https://raw.githubusercontent.com/elitak/nixos-infect/master/nixos-infect \
   | NIX_CHANNEL=nixos-25.05 PROVIDER=digitalocean bash -x'
#    Droplet reboots into NixOS. Wait for ssh to return.
until ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 root@$IP 'nixos-version'; do sleep 10; done

#    (Optional fidelity step: rsync the CriomOS flake, `nixos-rebuild switch
#     --flake .#target`, reboot — then the snapshot is closer to Lane 3.)

# 5. Snapshot the droplet → reusable PRIVATE image.  *** NEEDS image:create. ***
#    Today this returns 403; with a write token it returns an action object.
ACTION_ID=$(curl -fsS "${auth[@]}" -X POST "$API/droplets/$DROPLET_ID/actions" \
  -d '{"type":"snapshot","name":"criomos-base-2026-06-20"}' \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["action"]["id"])')

# 6. Poll the action to completion (snapshot is slow — minutes).
until [ "$(curl -fsS "${auth[@]}" "$API/droplets/$DROPLET_ID/actions/$ACTION_ID" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["action"]["status"])')" = completed ]; do
  sleep 15; done

# 7. Resolve the minted image id (the re-usable PRE-MADE image).
IMAGE_ID=$(curl -fsS "${auth[@]}" "$API/droplets/$DROPLET_ID/snapshots" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["snapshots"][0]["id"])')
echo "CriomOS golden image id: $IMAGE_ID"

# 8. Tear down the mint droplet (write scope CONFIRMED, 404→ok).
curl -fsS "${auth[@]}" -X DELETE "$API/droplets/$DROPLET_ID"

# 9. Boot CriomOS from the private image — NO daemon schema change:
#    ImageName::new("$IMAGE_ID") through the existing create_server path, or raw:
curl -fsS "${auth[@]}" -X POST "$API/droplets" -d '{
  "name":"criomos-node-1","region":"nyc3","size":"s-2vcpu-2gb",
  "image":'"$IMAGE_ID"', "ssh_keys":["'$FINGERPRINT'"], "ipv6":true,"monitoring":true
}'
```

## Lane 3 variant (production golden image — full CriomOS config)

Steps 0–3 identical (provision Ubuntu, **size ≥ `s-2vcpu-2gb`** — 1 GB lacks RAM
for kexec, ≥2.5 GB needed [nixos-anywhere][na-quickstart]). Then instead of
infect, from a workstation with the CriomOS flake:

```bash
# Requires a disko disk-config in the CriomOS flake (single GPT/MBR disk on
# /dev/vda, BIOS-grub for DO). nixos-anywhere kexecs, partitions, installs.
nix run github:nix-community/nixos-anywhere -- \
  --flake .#target --target-host root@$IP
# wait for reboot into the real CriomOS, then snapshot exactly as Lane 2 steps 5–8.
```

This snapshot captures `nixosConfigurations.target` itself, so the golden image
*is* CriomOS rather than infect's bootstrap. The added external dependency vs
Lane 2 is one flake input (`disko`) and a disk-config module.

## Lane 1 (rejected) — for the record

`nix build .#nixosConfigurations.target.config.system.build.digitalOceanImage`
(or `nix run github:nix-community/nixos-generators -- -f do`) → `nixos.qcow2.gz`,
then `POST /v2/images {url, distribution, region, name}`. Rejected because: (a)
**403 today** (no `image:create`); (b) even with scope, it needs the qcow2
served at a public HTTP/HTTPS/FTP URL — **no doctl-less, hosting-less option
exists** (DO Spaces would work as the host but that's *more* external
dependency, the opposite of the goal, and Spaces upload is its own
impure/credentialed step); (c) the image must be a **BIOS** build or the droplet
won't boot. Keep Lane 1 only if a CI artifact host already exists and a fully
declarative `target → qcow2 → image id` pipeline is wanted later.

## Action items

1. **Mint a write-scoped DO token** (`image:create`, `image:read`, plus the
   already-present droplet/ssh_key scopes) and store at
   `gopass digitalocean.com/api-token`. Without this, no lane completes.
2. **Run Lane 2 end-to-end** once scoped, capture the real `IMAGE_ID`, confirm
   a node boots from it.
3. **Confirm CriomOS `target` is BIOS/GRUB** before the production snapshot
   (inspect the bootloader module; DO snapshot/custom images boot BIOS only).
4. **Add the daemon's minting surface**: `/v2/droplets/{id}/actions` (snapshot)
   + action poll + `/v2/droplets/{id}/snapshots` to `digitalocean.rs`, so the
   cloud daemon can drive the whole mint, not just create/observe/destroy.

[do-upload]: https://docs.digitalocean.com/products/custom-images/how-to/upload/
[do-limits]: https://docs.digitalocean.com/products/custom-images/details/limits/
[do-image-module]: https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/virtualisation/digital-ocean-image.nix
[na-quickstart]: https://nix-community.github.io/nixos-anywhere/quickstart.html
