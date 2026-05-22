# Bird on Zeus local update authority design

## Summary

The psyche intent was recorded in Spirit under topic `zeus` as records 64
and 65. The implementation target is a narrow authority path: Bird's
persona operator, Aether, should be able to update Bird's own deployed
system on Zeus through her forked workspace, without granting general
root, broad Nix trust, or root SSH.

This belongs on the production stack first:

- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/CriomOS-home`
- `/git/github.com/LiGoldragon/horizon-rs`
- `/git/github.com/LiGoldragon/lojix-cli`
- `/git/github.com/LiGoldragon/goldragon`

The lean `lojix` daemon rewrite can absorb the same authority model later,
but the running Zeus system currently uses production `lojix-cli`.

## Current facts in code

Bird is already present in `goldragon/datom.nota` with a Zeus key:

```nota
(Entry bird (UserProposal ... [
  (Entry zeus (UserPubKeyEntry ...))
]))
```

The cluster trust override currently says:

```nota
(Entry bird Medium)
(Entry li Max)
```

This matters because current CriomOS root SSH access is derived from
`horizon.node.adminSshPubKeys`, and `horizon-rs` fills that list from
users whose projected trust is `Max` and whose key lives on a fully trusted
node. Since Bird is `Medium`, she does not get root SSH today. That is good.

CriomOS user projection currently derives broad local groups from trust:

- `Medium` gives ordinary desktop/media groups such as `video` and
  possibly `networkmanager`.
- `Max` gives broad development/admin-ish groups such as `nixdev`,
  `systemd-journal`, `libvirtd`, `storage`, and so on.

Therefore the wrong fix is to make Bird `Max`. That would grant too much
and would not express the intended authority: "can update this node's
system", not "is a global max-trust operator".

Production `lojix-cli` currently performs system activation through
`root@target` SSH. `src/activate.rs` builds root remote invocations like:

```text
ssh root@<target> nix-env -p /nix/var/nix/profiles/system --set ...
```

That is also too broad for Bird's path. The desired privilege is local,
per-user, per-node, and update-shaped. It should not require adding Bird's
key to root authorized keys.

## Correct authority shape

Add an explicit Horizon-authored grant for local system update authority.
Do not reuse `trust = Max`, node species, user species, root SSH, `wheel`,
or `nixdev`.

Sketch:

```nota
(SystemUpdateGrant bird zeus [FullOs OsOnly] [Boot Switch Test BootOnce])
```

The exact field names belong in `horizon-rs`, but the noun should say what
it is: a system update grant. It is a cluster fact because the cluster
owner decides which user can update which node.

Suggested location:

- proposal side: `ClusterProposal.system_update_grants: Vec<SystemUpdateGrant>`
- view side: `view::Node.system_update_grants: Vec<SystemUpdateGrant>` filtered
  to the viewpoint node, or a simpler `system_update_users: Vec<UserName>` if
  the action policy is fixed in CriomOS for the first slice

The first Goldragon entry should grant only:

- user: `bird`
- node: `zeus`
- deploy kinds: `FullOs`, optionally `OsOnly`
- actions: likely `BootOnce`, `Test`, and later `Switch`

## Correct privilege surface in CriomOS

CriomOS should render a root-owned local update helper only for users named
by the projected Horizon grant. The helper is the only command allowed by
sudo for that user.

Do not add:

- `bird` to `wheel`
- `bird` to `nixdev`
- Bird's key to root SSH
- a generic `sudo lojix ...` rule
- a generic "trusted Nix user" rule

The sudo rule should be command-specific, like the existing
`criomos-nspawn` pattern, but narrower:

```nix
security.sudo.extraRules = [
  {
    users = [ "bird" ];
    commands = [
      {
        command = "/run/current-system/sw/bin/criomos-local-update";
        options = [ "NOPASSWD" ];
      }
    ];
  }
];
```

The helper must not accept an arbitrary `lojix-cli` request. Arbitrary
flake refs or proposal paths are root code execution. The helper should
accept a small NOTA request, validate it against the compiled policy, and
construct the full `lojix-cli` request itself.

Sketch:

```nota
(LocalUpdate BootOnce)
(LocalUpdate Test)
(LocalUpdate Switch)
```

The helper fills in:

- cluster: `goldragon`
- node: `zeus`
- user: the Unix caller, checked as `bird`
- source: Bird's checked-out cluster proposal path or a policy-selected
  repository path
- `criomos`: Bird's allowed CriomOS fork named reference
- `home`: Bird's allowed CriomOS-home fork named reference
- builder/substituters: policy-selected defaults, not caller-supplied

The helper can live in CriomOS as a small Rust or shell wrapper, but a Rust
wrapper is preferable because it can parse the NOTA shape and reject
unknown fields precisely.

## Needed `lojix-cli` change

Production `lojix-cli` needs a local activation path. A root-owned local
helper should not SSH to `root@zeus` to update Zeus from Zeus.

Add a target execution mode:

```text
SystemTarget::Local
SystemTarget::Remote(SshTarget)
```

When the deploy target is the current viewpoint node and the process is
already running as root through the CriomOS helper, activation should run
the same system commands locally:

```text
nix-env -p /nix/var/nix/profiles/system --set <store>
<store>/bin/switch-to-configuration <action>
```

The existing `BootOnce` transient-unit shape can still use `systemd-run`,
but locally instead of through SSH.

This is the smallest production code change that preserves the existing
`lojix-cli` projection/build/copy/activation pipeline while avoiding the
root SSH grant.

## Fork and repository bootstrap

Aether's user-level setup is separate from the OS privilege path.

User-level bootstrap should:

1. Clone or fork Bird's `primary`, `CriomOS`, `CriomOS-home`,
   `horizon-rs`, `lojix-cli`, and `goldragon` repositories as needed.
2. Keep Bird's branches aligned with LiGoldragon's stable named references.
3. Work from Bird's primary workspace using the workspace skills and role
   discipline.
4. Avoid raw commit revisions as the user-facing policy target. Named
   references such as branches, bookmarks, or tags are the stable interface;
   lock files can still resolve them to exact revisions internally.

This bootstrap does not need root. The root boundary begins only when Bird
asks the local update helper to activate a built system closure.

## Public and private soul repositories

The psyche intent says Aether's repository is Bird's public soul repo, with
a corresponding private encrypted soul part using the existing SOPS system
on private repositories.

Implementation-wise, this should be kept out of the root update grant. It
is a repository and secret-materialization concern:

- public soul: ordinary Git repository readable by Aether and other agents
- private soul: private repository with SOPS-encrypted content
- CriomOS-home: may install agent tooling and point Aether to the local
  checkout paths
- CriomOS: may install secret tooling and access paths, but should not bake
  private decrypted content into the system closure

The exact repo topology still needs psyche confirmation.

## Tests

The implementation should not be considered complete without Nix witnesses.

Horizon tests:

- `system_update_grant_round_trips_from_nota`
- `system_update_grant_projects_only_on_target_node`
- `bird_medium_trust_does_not_gain_admin_ssh`

CriomOS tests:

- `system_update_grant_installs_one_sudo_command`
- `system_update_grant_does_not_add_wheel_or_nixdev`
- `system_update_grant_does_not_add_root_authorized_key`
- `local_update_helper_rejects_ungranted_user`
- `local_update_helper_rejects_wrong_node`
- `local_update_helper_rejects_unapproved_flake_ref`

`lojix-cli` tests:

- `local_system_activation_does_not_construct_ssh_invocation`
- `remote_system_activation_still_constructs_ssh_invocation`
- `local_boot_once_uses_systemd_run_without_ssh`

End-to-end production smoke:

- Build a Zeus projection with Bird's grant.
- Build the CriomOS system config.
- Assert the generated sudo rule names exactly the helper path.
- Assert Bird is not in broad admin groups as a side effect.

## Open questions

### 1. What is the allowed action for the first Bird update path?

The safest first grant is `BootOnce` plus `Test`: it lets Bird install a
new generation for the next boot without changing the persistent default
forever. If the goal is day-to-day local self-maintenance, `Switch` may be
needed too. The report recommends starting with `BootOnce` and `Test`, then
adding `Switch` once the local helper and rollback path are proven.

### 2. Where exactly is Bird's allowed source of truth?

The design assumes Bird updates Zeus from Bird-owned forks tracking
LiGoldragon's named references. The implementation needs a policy record
that names either local checkout paths or allowed flake references. This
should be explicit; letting the caller pass arbitrary paths would turn the
helper into root code execution.

### 3. Is Aether's public soul repo Bird's `primary` fork or a separate repo?

The prompt says Aether's repo will be used as her public soul repo. If that
means Bird's `primary` fork, then the public soul is mixed with workspace
coordination. If it means a dedicated `aether` repository, then `primary`
can reference it. The latter is cleaner, but the psyche intent is not yet
precise.

### 4. Should home-only updates use the same root helper?

Home-only activation can often be user-owned, but the full system path may
also update the Home Manager profile through CriomOS. The first helper can
focus on full OS updates; a separate user-owned home update path can stay
outside sudo unless a concrete privilege need appears.

## Recommended first implementation slice

1. Add `SystemUpdateGrant` to `horizon-rs` and project it to the viewpoint
   node.
2. Add Bird-on-Zeus grant to `goldragon/datom.nota`.
3. Add CriomOS module code that renders `criomos-local-update` and a sudo
   rule only for projected grants.
4. Add `lojix-cli` local system activation path.
5. Add the tests listed above.
6. Deploy to Zeus only after the tests prove the grant does not widen into
   root SSH, `wheel`, `nixdev`, or arbitrary `lojix-cli` execution.
