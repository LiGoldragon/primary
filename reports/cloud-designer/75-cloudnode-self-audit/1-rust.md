# Critic 1 — Rust deploy harness + adapter fix (cloud / do-deploy-test)

Adversarial read of the live DigitalOcean deploy harness, the `from_spec`
monitoring/ipv6 fix, the flake app/check, and the mint script. Every finding
cites `file:line`. No praise; the author cut corners and admitted only some.

Files:
- `tests/digitalocean_deploy_live.rs` (509-line harness)
- `src/digitalocean.rs` (`DropletPayload::from_spec`, ~443-466)
- `flake.nix` (deploy-live app + compile check)
- `scripts/digitalocean-mint-criomos-image.sh`

## Findings

### HIGH-1 — `DeployCleanup` is a copy of `LiveCleanup`, not a generalization
`tests/digitalocean_deploy_live.rs:438` calls the type a generalization of
"the Tier-1 `LiveCleanup`", but it generalizes nothing. `DeployCleanup`
(441-509) is a field-for-field, method-for-method copy of `LiveCleanup` in
`tests/digitalocean_live.rs:163-224`: same `api`/`token`/`droplet`/
`ssh_key_fingerprint` fields, same `track_droplet`/`track_ssh_key`/
`destroy_droplet`/`delete_ssh_key`, same `Drop` body verbatim including the
identical error strings (`"live cleanup failed to destroy droplet"`). The only
delta is the added `tear_down_and_log`. Two integration-test files can't share
a `mod`, but the shared cleanup machine belongs in a `pub` item under
`src/` (e.g. a `live_support` module behind the `digitalocean` feature) that
both tests import — exactly where the production `ServerSpec`/`HostIdentifier`
already live. The doc comment lying that it "generalizes" the other is worse
than silence: it claims a refactor that never happened.
Fix: extract the cleanup type into the crate (`src/`), delete both copies,
have each test construct it. Then `tear_down_and_log` is one more method on the
single owner.

### HIGH-2 — MODE detection by "image string is all ASCII digits" is a hand-rolled type-from-string sniff
`tests/digitalocean_deploy_live.rs:163-165` decides mode 1 vs mode 2 with
`self.image.chars().all(|c| c.is_ascii_digit())`. This is a parser
masquerading as a predicate, and it is wrong on its own terms: it is dead
weight (the result is only ever fed to a `println!` at line 58 choosing a
human label — it gates no behavior), AND it is fragile (a future numeric
distribution slug, or DO image ids that aren't pure-decimal, silently
mislabel). The whole concept of "mode" is a string the environment carries;
the honest model is a typed enum decided once at parse time, not a boolean
recomputed from character classes. Per `typed-records-over-flags.md`: the
distinction between a snapshot id and a distribution slug is a closed set of
named variants, so it should be `enum ImageSource { Snapshot(u64), Slug(String) }`
parsed in `from_environment`, with `Display` carrying the label — not a `bool`
method re-sniffing the raw string at the call site.
Fix: parse `CRIOMOS_IMAGE` into `ImageSource` once; the create path takes the
typed value; the label is `ImageSource`'s `Display`. Delete `is_custom_image`.

### HIGH-3 — `monitoring=false` / `ipv6=false` hardcoded; the admitting comment is a cop-out
`src/digitalocean.rs:457,463` hardcode both flags to `false`, and the comment
at 451-456 admits it: "(Both flags should become desired-state fields on
ServerSpec rather than hardcoded.)" Writing the correct design into a comment
and then shipping the wrong one is the textbook cop-out — the comment is a
TODO wearing a justification's clothes. `ServerSpec` (`src/digitalocean.rs:92`)
is the shared production desired-state struct (consumed by `create_server`
274 and `create_host` 337); it is the obvious and already-open home for these
fields. Hardcoding `false` also silently overrides any caller — the mint
script POSTs `ipv6:true, monitoring:true` for its stock-Ubuntu droplet
(`scripts/...:61`), so the two provisioning paths now disagree on the same two
flags with no shared type enforcing the choice. The "custom images reject
ipv6/monitoring" fact is real, but the fix is a typed desired-state field plus
a provider-side rule, not a constant.
Fix: add `ipv6: Ipv6Networking` and `monitoring: MonitoringAgent` (or
`bool` if a richer type is overkill) to `ServerSpec`; default them in the
harness's spec; let `from_spec` read `spec.*`. Delete the comment.

### MEDIUM-1 — `DeployConfirmation` is three responsibilities welded into one `resolve`
`tests/digitalocean_deploy_live.rs:241-267`: `resolve` (a) waits for ssh to
come up, (b) runs a remote `nixos-rebuild switch`, and (c) reads
`/etc/os-release` and marker-matches. Those are three independent capabilities
— reachability, mutation, and inspection — fused into one method on one type
holding `host`/`key`/`parameters`. The single-responsibility smell shows in
the return type: `DeployLevel` has to encode "I am also the deploy-failed
signal" (`DeployFailed`, 354) because the mutation step leaks its failure mode
into what is nominally a *confirmation* level. SSH waiting, remote switch, and
release inspection each want to be their own small data-bearing step the
harness sequences, so a reader sees the deploy pipeline instead of one
20-line method that does everything.
Fix: split into `SshReadiness::wait`, a `RemoteSwitch::run` returning a real
`Result`, and `ReleaseProbe::read` returning the marker outcome; the test body
sequences them and maps to `DeployLevel`.

### MEDIUM-2 — deploy target recomputed; `resolve` builds the string `run_remote_switch` rebuilds
`tests/digitalocean_deploy_live.rs:252` computes
`let target = format!("{flake}#{}", self.parameters.deploy_attribute)` purely
to print it, then `run_remote_switch` recomputes the identical expression at
282. Same inputs, same format string, two sites — change the attribute syntax
once and you must remember both. The target is a property of the deploy, so it
should be computed once (ideally a typed `DeployTarget` with a `Display`) and
both the log line and the command read it.
Fix: build the target once before the `if let`, pass it (or a `DeployTarget`)
into `run_remote_switch`; the `println!` and the `--flake` arg share it.

### MEDIUM-3 — `expect()`/`panic` as the harness error strategy at every step
The harness panics on every fallible boundary: `expect("DIGITALOCEAN_ACCESS_TOKEN must be set")`
(44), `expect("ensure_ssh_key...")` (53), `expect("create_server")` (73),
`expect("droplet reached Running...")` (85), plus `TemporarySshKey::new`'s
`expect("temporary ssh-key directory")` / `expect("run ssh-keygen")` /
`assert!` / `expect("read generated public key")` (392-407). In a test that
*spends real money provisioning a droplet*, an `expect` on a step *after*
create (e.g. the `until_running` expect at 85, or the os-release read) aborts
the process; the `Drop` guard does run, but mixing "assertion" panics with
"setup failed" panics means a CI log can't distinguish a genuine deploy
failure from ssh-keygen-not-on-PATH. The module doc sells `Drop`-guaranteed
teardown; leaning on panics for control flow makes that guarantee the only
thing standing between a panic and a leaked $4/mo droplet.
Fix: setup failures (token unset, ssh-keygen missing) are `eprintln!` +
early `return`; only genuine post-provision invariants are `assert!`. Keep
the panic surface small and labeled "assertion", not "I/O failed".

### MEDIUM-4 — mint script defaults to `nixos-infect`, the approach that produced the rejected image
`scripts/digitalocean-mint-criomos-image.sh:33` sets `CONVERT=${CONVERT:-infect}`
and 80-86 runs `elitak/nixos-infect` piped from raw GitHub through `bash -x`,
swallowed with `|| true` (82). The harness module doc and the script's own
header (referencing report 73) treat nixos-infect output as the substrate that
yields the bloated GRUB image; `anywhere` (nixos-anywhere onto a real flake) is
the fidelity path but is opt-in. Defaulting to the known-bad converter, then
`|| true`-ing its failure and proceeding to snapshot whatever survived, is
how you mint another wrong image by accident. `curl | bash -x` of an external
master branch also pins nothing — non-reproducible by construction, in a Nix
repo whose whole point is reproducibility.
Fix: make `anywhere` the default (or remove `infect` entirely if report 73
rejected it); drop the `|| true` on the conversion so a failed convert aborts
before the snapshot; pin the converter to a flake input, not `master`.

### MEDIUM-5 — mint script is orphaned: not wired into the flake at all
`grep -c mint flake.nix` = 0. The mint script (the only way mode 1 ever gets
an image) is a loose `scripts/*.sh` with no flake app, no `runtimeInputs`, no
`writeShellApplication` wrapper — unlike `digitaloceanDeployLiveTest`
(`flake.nix:125`) which *does* get curl/jq/nixos-rebuild/gopass pinned. So the
script's `curl`/`jq`/`ssh`/`nix` are unmanaged ambient PATH, and a user is told
(harness doc line 20-22) to feed `CRIOMOS_IMAGE=<id>` with no supported,
reproducible producer of that id. The two halves of mode 1 don't connect.
Fix: wrap the mint script as `pkgs.writeShellApplication` with pinned
`runtimeInputs` and expose `apps.digitalocean-mint-image`, mirroring the
deploy-live app.

### LOW-1 — `DeployLevel` carries a result code the witness line could derive
`tests/digitalocean_deploy_live.rs:350-378` defines `DeployLevel` with BOTH
`as_witness_field` (358, machine token) AND a `Display` (368, prose), hand-kept
in lock-step across four variants — two parallel match arms that must agree.
`SshReachable` and the `Some(_)`/`None` arms of `resolve` (264-265) collapse to
the same variant, so the type already can't distinguish "read os-release but no
marker" from "couldn't read os-release" — information the harness had and threw
away. Two stringly representations of one enum, plus a lossy mapping, is more
surface than the four states need.
Fix: one canonical representation (derive the prose from the token, or vice
versa); if the os-release-read-failure case matters, give it a variant instead
of folding it into `SshReachable`.

### LOW-2 — ssh option list rebuilt as `Vec<String>` and `root@{ip}` formatted at four sites
`ssh_options()` (332-345) returns a fresh `Vec<String>` of nine literals on
every call, and `format!("root@{address}")` is re-spelled at 253, 288, 313,
327. The ssh identity ("this key, these hardening options, this `root@ip`
target") is a thing — an `SshTarget { address, key_path }` with a
`command(&self, remote) -> Command` method would own the option list and the
`root@` formatting once. As written, a fifth ssh call means a fifth `root@`
format and a reader must trust all four option lists are byte-identical.
Fix: introduce `SshTarget`; build options once; `root@` lives in one method.

### LOW-3 — `run_remote_switch`/`read_release`/`ssh`/`wait_for_ssh` return bare `bool`/`Option`, losing the error
`run_remote_switch` returns `bool` (281), `wait_for_ssh` returns `bool` (269),
`read_release` returns `Option<String>` (310) — every failure cause is
`eprintln!`'d and then discarded into a sentinel. The workspace discipline is
typed errors at boundaries, not boolean success flags; a deploy step that can
fail four distinct ways (spawn failed, non-zero exit, transport, timeout) and
returns `bool` is the bool-flag-soup the rules name explicitly. The caller at
254 can only say `DeployFailed` with no cause.
Fix: return `Result<(), DeployError>` from the remote steps; map the error to
the witness line so a failed run says *why*.

### LOW-4 — `until_running` returns the last observation as if it were success
`tests/digitalocean_deploy_live.rs:203-220`: on budget exhaustion it returns
`latest` (the last non-running observation) rather than signaling timeout, and
the caller's `expect` at 85 then panics with a message ("reached Running")
that is a lie when `latest` was `Some(non-running-host)` — the `Option` is
`Some`, so `expect` *succeeds* and the harness proceeds to ssh a droplet that
never reached Running. The "running" bit computed at 208-209 is thrown away on
the timeout path.
Fix: return `Result<ApiServer, PollTimeout>` (or `Option` only on true
success); the loop's last value isn't a success and shouldn't impersonate one.

### NIT-1 — `_directory: tempfile::TempDir` keep-alive field is an undocumented load-bearing leading-underscore
`tests/digitalocean_deploy_live.rs:387` parks the `TempDir` in `_directory`
purely so its `Drop` doesn't fire early. The leading underscore says "unused"
while the field is in fact the most load-bearing thing in the struct (it's what
keeps the private key on disk). A one-line comment or a named `guard` field
would stop the next reader from "cleaning up the unused field".

### NIT-2 — `number_or` lives on `DeployParameters` but is called from `PollBudget`
`PollBudget::from_environment` (174-182) reaches across to
`DeployParameters::number_or` (154) twice. The env-parsing helper isn't
`DeployParameters`' job specifically; it's a generic "u32 from env" that two
types want. Minor, but it's the same "where does this logic live" question the
method-placement rule asks — an `EnvironmentNumber`/`EnvironmentValue` reader
owns it, and both parameter types use it.

## Severity roll-up
- HIGH: copy-not-generalize cleanup (1), all-digit MODE sniff (2),
  hardcoded flags with cop-out comment (3).
- MEDIUM: 3-responsibility `resolve` (1), recomputed deploy target (2),
  panic-as-control-flow (3), infect-default mint (4), orphaned mint script (5).
- LOW: dual-stringly `DeployLevel` (1), rebuilt ssh options/`root@` (2),
  bool-return remote steps (3), timeout-as-success poll (4).
- NIT: `_directory` keep-alive (1), misplaced `number_or` (2).
