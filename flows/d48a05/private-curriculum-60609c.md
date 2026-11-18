# Private Curriculum60609c bootstrap — source-only packet for occ6

Read against immutable Curriculum `60609c55f90432782625275294636a4e396d9497` (package0.2.0), available in `/git/worktrees/curriculum-notion-404d40`. This packet has not been executed or runtime-reviewed. FlowNexus Sol owns bootstrap approval; Field runs only accepted commands. It grants no build, deployment, production query or native context injection. The newer Notion/Panel packets are not this cohort.

## Exact source pointers
At that commit, `tests/nexus_roundtrip.rs` lines24–114 supplies the isolated environment and bare daemon invocation; `src/registry.rs` SourceConfiguration, beginning around305, supplies the required layout/source/refresh variables and reads each root's `.git/HEAD`; `src/service.rs` lines175 onward and `src/client.rs` socket_path use `$XDG_RUNTIME_DIR/curriculum/curriculum.sock`; `src/service.rs` compose_startup requires CURRICULUM_RECORDS_DIR even with no selected records; `src/startup.rs` compose requires explicit Spirit and Intent system selections. `src/roles.rs` read_declared makes CURRICULUM_ROLES_FILE optional. Inspect with `git -C /git/worktrees/curriculum-notion-404d40 show 60609c55f90432782625275294636a4e396d9497:<file>`.

## Owner-supplied inputs
`PRIVATE_ROOT`: a fresh absolute private directory, unused by production. `CURRICULUM_BIN`: an existing immutable binary directory containing the datom-enabled curriculum client and curriculum-nexus proven built from60609c; the package version string alone is not revision evidence. `PSYCHE_ROOT`, `MIND_ROOT`, `FIELD_ROOT`: three separate private pinned authored root copies, their immutable revisions and byte hashes recorded in the bootstrap packet. No source pins or artifact provenance were supplied in occ6, so this packet does not invent them or authorize a build.

Each source root must carry a compatible typed modules.datom and the files it declares. This reader supports the pre-Notion vocabulary and Single/Span versions, not the later Notion/Panel/All additions. Each copy needs a real `.git` directory and a resolvable immutable `.git/HEAD`/refs, not a linked-worktree `.git` file. Preserve the authored source bytes and manifest for its selected pin; do not rewrite a production registry or claim a generated test manifest is an authored one. GitHub/local pinned copy preparation and compatibility review belong in Flow's packet before Field execution. The60609c native test's synthetic roots are a proof fixture, not a substitute for these authored copies.

## Preparation and startup commands (for review, not executed)
The variables below are required packet inputs. No running process is started by this document. The refresh program deliberately leaves frozen private copies unchanged; it performs no fetch, update or production action, matching the immutable-root test's no-op refresh contract.

```sh
: "${PRIVATE_ROOT:?fresh absolute private root}"
: "${CURRICULUM_BIN:?existing proven 60609c binary directory}"
: "${PSYCHE_ROOT:?private pinned psyche root}"
: "${MIND_ROOT:?private pinned mind root}"
: "${FIELD_ROOT:?private pinned field root}"
mkdir -p "$PRIVATE_ROOT/home" "$PRIVATE_ROOT/runtime/curriculum" \
  "$PRIVATE_ROOT/records" "$PRIVATE_ROOT/config" "$PRIVATE_ROOT/state" \
  "$PRIVATE_ROOT/cache" "$PRIVATE_ROOT/bin"
chmod 700 "$PRIVATE_ROOT/home" "$PRIVATE_ROOT/runtime" \
  "$PRIVATE_ROOT/runtime/curriculum" "$PRIVATE_ROOT/records"
printf '#!/bin/sh\nexit 0\n' > "$PRIVATE_ROOT/bin/refresh-pinned-contexts"
chmod 700 "$PRIVATE_ROOT/bin/refresh-pinned-contexts"
env -i \
  HOME="$PRIVATE_ROOT/home" \
  XDG_RUNTIME_DIR="$PRIVATE_ROOT/runtime" \
  XDG_CONFIG_HOME="$PRIVATE_ROOT/config" \
  XDG_STATE_HOME="$PRIVATE_ROOT/state" \
  XDG_CACHE_HOME="$PRIVATE_ROOT/cache" \
  CURRICULUM_CONTEXT_LAYOUT=2 \
  CURRICULUM_CONTEXT_REFRESH_PROGRAM="$PRIVATE_ROOT/bin/refresh-pinned-contexts" \
  CURRICULUM_PSYCHES_REPOSITORY_DIR="$PSYCHE_ROOT" \
  CURRICULUM_MIND_CONTEXT_DIR="$MIND_ROOT" \
  CURRICULUM_FIELD_CONTEXT_DIR="$FIELD_ROOT" \
  CURRICULUM_RECORDS_DIR="$PRIVATE_ROOT/records" \
  "$CURRICULUM_BIN/curriculum-nexus"
```

The last command is foreground, zero daemon arguments: this pin does not take a Place datom. Field's reviewed supervisor owns its child, readiness event, terminal evidence and cleanup; no polling or detached lifetime is prescribed. `env -i` excludes ambient production variables and roles. If the no-op script's `/bin/sh` is not present on the execution host, the owner must supply a verified absolute shell path in that private script; do not substitute an ambient refresh program. No ORIGIN or generic RECORDS_DIR variable replaces the required Curriculum variables above.

## Minimum authored selection and private client
A single module is insufficient for ComposeStartup at this pin: it explicitly requires Spirit and seat Intent. The briefest normal authored selection is spirit:core:0 plus intent:main-flow:0, provided the approved authored root pin declares those IDs and their dependency closure. No USER module or old flow record is selected. There is no caller-inline text, caller path, production configuration replay, or production record replay.

```sh
env -i HOME="$PRIVATE_ROOT/home" XDG_RUNTIME_DIR="$PRIVATE_ROOT/runtime" \
  XDG_CONFIG_HOME="$PRIVATE_ROOT/config" XDG_STATE_HOME="$PRIVATE_ROOT/state" \
  XDG_CACHE_HOME="$PRIVATE_ROOT/cache" \
  "$CURRICULUM_BIN/curriculum" \
  'ResolveSources.[ { Spirit core Single.0 } { Intent main-flow Single.0 } ]'
env -i HOME="$PRIVATE_ROOT/home" XDG_RUNTIME_DIR="$PRIVATE_ROOT/runtime" \
  XDG_CONFIG_HOME="$PRIVATE_ROOT/config" XDG_STATE_HOME="$PRIVATE_ROOT/state" \
  XDG_CACHE_HOME="$PRIVATE_ROOT/cache" \
  "$CURRICULUM_BIN/curriculum" \
  'ComposeStartup.{ { Mind flowNexus Sol } Codex [ { Spirit core Single.0 } { Intent main-flow Single.0 } ] [] [] }'
```

The socket is private `runtime/curriculum/curriculum.sock`. ComposeStartup returns typed text and provenance; the caller must verify source revisions/paths/hashes against the frozen inputs. Returning that composition does not itself insert instructions into a native harness. If Flow's isolated test needs additional exact IDs, name them in its approved selection; leave its private records root empty unless it explicitly tests a separately authored record fixture. Optional ComposeRole needs a separately reviewed scratch roles.datom with exact module IDs and CURRICULUM_ROLES_FILE on daemon startup; none is needed or configured here.
