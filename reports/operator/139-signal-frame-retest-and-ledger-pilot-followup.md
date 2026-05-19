# 139 — signal-frame retest and ledger pilot follow-up

Role: operator  
Date: 2026-05-19  
Repos touched: `signal-frame`, `signal-repository-ledger`

## Summary

The `signal-frame` collapse from designer report `/240` was already
landed before this slice. I retested it directly, then advanced the
pilot contract `signal-repository-ledger` to consume the collapsed
request surface.

Load-bearing result:

```rust
let request = Request::Query(Query::Catalog(Catalog)).into_request();
assert_eq!(request.payloads().len(), 1);
```

`Request::operations()` is gone from the pilot; the request now exposes
the `NonEmpty<Payload>` shape as `payloads()`, matching current
`signal-frame`.

## signal-frame verification

Commit tested: `4bdf1e1e` on `signal-frame` `main`.

Passed:

```sh
CARGO_BUILD_JOBS=2 cargo test --locked
CARGO_BUILD_JOBS=2 cargo clippy --all-targets --locked -- -D warnings
nix flake check -L --max-jobs 0
```

The Nix run used `--max-jobs 0` as requested.

## signal-repository-ledger follow-up

Two commits now form the pilot witness:

- `bb1dab8a` — migrated the contract from old `signal-core`
  verb-tagged requests to `signal-frame` contract-local operations:
  `Receive`, `Observe`, `Query`.
- `e3592c04` — bumped to `signal-frame` `4bdf1e1e`, switched the test
  witness from `operations()` to `payloads()`, and refreshed NOTA
  examples for the current `Option` projection.

The public shape is:

```rust
signal_channel! {
    channel Ledger {
        operation Receive(ReceiveHookNotification),
        operation Observe(PushObservation),
        operation Query(Query),
    }
    reply Reply {
        EventRecorded(EventRecorded),
        EventListing(EventListing),
        RecentRepositoriesListing(RecentRepositoriesListing),
        ChangedFileListing(ChangedFileListing),
        CommitListing(CommitListing),
        CatalogListing(CatalogListing),
        RequestUnimplemented(RequestUnimplemented),
    }
}
```

The text witness is now:

```nota
(Query (RecentRepositories ((Some "20260519T000000Z") 16)))
```

That parenthesized `Some` shape comes from the current `nota-codec`
lock pulled in while pinning the latest `signal-frame`.

## Verification

For `signal-repository-ledger`, passed:

```sh
CARGO_BUILD_JOBS=2 cargo test --locked
CARGO_BUILD_JOBS=2 cargo clippy --all-targets --locked -- -D warnings
nix flake check -L --max-jobs 0
```

The Nix check ran on the remote builder and passed all checks.

## Bead

Closed bead `primary-yrfr` (signal public request migration) because
its acceptance criteria are now met by:

- `signal-frame` macro and request-kernel tests;
- `signal-frame` collapse tests from `/240`;
- the real `signal-repository-ledger` pilot contract running against
  current `signal-frame`.

## Remaining work

This closes only the foundation bead. The broad migration remains:
other contracts still need the same `signal-core` to `signal-frame`
conversion, and daemons consuming those contracts need their dispatch
code moved from public Sema verbs to contract-local operations.
