# Reviewed Messenger CLI-only switch plan

Status: reviewed plan for Field execution; no switch has occurred.

## Ownership and boundary

- Execution and rollback owner: Field `9ac67c`.
- Source coordination: Mind `6fe957`.
- Scope is the current-user Messenger CLI selection only. Full Home activation
  and the Message daemon remain held.
- Exact maintenance lock name and legitimate live-message recipient are assigned
  by Field's immediately pre-action witness. They are not invented here.

## Witnessed targets

- Current `/home/li/.local/libexec/messenger-clj` is a directory symlink to
  `/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5`.
- Candidate package directory is
  `/nix/store/37jlvv66px2407h4pshgg808n0100rlh-messenger-clj-0.2.6`.
- Candidate derivation is
  `/nix/store/d1vh77n2ibc9k3dmap6drjck588rpgv0-messenger-clj-0.2.6.drv`.
- Candidate source is `93c12756f9c00dd3c13762590f17cee3a3712530`, with
  Babashka `1.13.219`.
- The accepted isolated native `--stdin` same-thread proof is for the exact
  `37j` candidate, not `b1jm`.
- The existing rollback root is
  `/home/li/.local/state/da88cf-gcroots/messenger-clj-0.2.5`.

## Preconditions and evidence

Field acquires a precise wrapper-and-Messenger-state maintenance reservation
through the supported lock service. Before any replacement, verify there is no
live `hm` process, the raw link target is exactly `p8mz`, and all ten expected
aliases are symlinks through `libexec/bin`:

`hm-{deregister,heartbeat-state,list,move,rebind,register,repair,retire,send,send-abrupt}`.

Stop on drift; do not kill a process. Record link attributes, prior root, and
supported `--help` output. `--version` is not implemented; prove version by the
exact selected store path and package metadata. Validate both package outputs
locally before rooting; never realize or build a missing path.

After that witness, add a uniquely named Field-owned GC root with supported
`nix-store --add-root <new-unique-Field-path> -r` for the exact `37j` package
only. Verify that the root actually retains `37j`. A Home result is not enough.

## Atomic switch and rollback

Create a same-directory temporary symlink to the candidate package directory,
then atomically `mv -Tf` it to `libexec/messenger-clj`. Compare the old target
immediately before the replacement. Do not link `bin/messenger-clj`.

Read back raw and resolved targets for all ten aliases and run supported
`hm-send --help` and `messenger-clj --help` through the existing selection,
recording exact 0.2.6 provenance.

On failure, atomically roll back only the shared `libexec/messenger-clj` link to
the exact `p8mz` package directory. Verify all aliases, help output, and 0.2.5
provenance, preserving both GC roots and all evidence.

## One post-handoff delivery witness

Only after the supported maintenance handoff/release, so the lock does not
block legitimate delivery, resolve a fresh exact recipient binding. Send one
harmless unique work message to an established live receiver using positional
native delivery. Do not retry with `--stdin` here. Retain actual exit and grade,
the target's exact native body, and same-thread reply. If uncertain, do not
blindly resend. Normal delivery may append normal Messenger state; make no
manual ledger change.

No daemon or service action, Home profile activation, source pin change, ledger
repair, build, fetch, or store realization belongs to this plan.
