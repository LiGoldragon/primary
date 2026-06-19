# 435 - Criome-gated propagation stack mainlined

## Result

The criome-gated propagation stack is on main in all three code repos, and the feature bookmarks plus local feature worktrees have been removed.

| Repo | Main commit | Result |
|---|---:|---|
| `criome` | `6c75804c` | mainlined publish-side authorized-object matching retirement |
| `router` | `94712199` | mainlined criome authorized-object projection |
| `spirit` | `1ea773e3` | mainlined the criome-gated propagation loop integration |

Bead `primary-l6xg` (Spirit criome-gated typed propagation loop) is closed.

## Checks Run

`criome`:

```sh
cargo fmt --check
cargo test
```

Result: green.

`router`:

```sh
cargo fmt --check
cargo test --test authorized_object_fanout
```

Result: green.

`spirit`:

```sh
cargo fmt --check
cargo test --offline --features mirror-shipper --test end_to_end_offline_full_chain
```

Result: green, including `authorized_d1_head_routes_and_rejects_restore_latest_after_d2`.

## Integration Notes

Spirit main had advanced past the propagation branch with the stale-mirror-restore-head work, so the Spirit stack was rebased rather than moved sideways. The final Spirit integration preserves the mainline mirror shipper dependency gate:

```toml
mirror-shipper = ["dep:mirror", "dep:signal-mirror"]
```

I avoided a broad `cargo update` after it pulled unrelated moving main heads and exposed stale generated artifacts in the mirror/schema chain. The final Spirit lockfile keeps the existing generated-artifact chain and only points `criome` and `router` at their newly mainlined commits.

## Cleanup

Removed the `criome-gated-propagation-loop` bookmarks locally and remotely in:

- `criome`
- `router`
- `spirit`

Forgot and removed the matching `~/wt/github.com/LiGoldragon/.../criome-gated-propagation-loop` worktrees.

## Not Run

No Nix checks were run for this stack. The verification was cargo-level and targeted at the propagation integration path.
