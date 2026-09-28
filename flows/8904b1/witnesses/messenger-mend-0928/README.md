# Messenger mend, 2026-09-28

Cause: `assert-native-not-retired!` (messenger-clj core.clj) re-validated every
other Flow's retirement marker, including its evidence file and SHA-256. The
markers of 00f95a, 38de5b, 88475f, 98ac2e, 9c7514, 9e7ea5, ae7862, b860be and
da88cf name evidence at
`/home/li/wt/primary/e167d8-cleanup/flows/e167d8/witnesses/herdr-cleanup-records-2026-09-26.md`;
that workspace was removed this morning (workspaces-0928.md, row
e167d8-cleanup), so every registration failed on 00f95a, the first in order.

Changed:

- Created (no prior file existed, so nothing to copy) the missing evidence
  file at its recorded path, copied from
  `/home/li/primary/flows/e167d8/witnesses/herdr-cleanup-records-2026-09-26.md`;
  digest 920cf3b41fefeb7739d706570f5811f1d6dca035b814d51e8561d3a86f9d0a46
  matches the markers. The directory `/home/li/wt/primary/e167d8-cleanup/`
  exists again only to hold it.
- Before any messenger mutation, an exact copy of the ledger:
  `/home/li/.local/state/messenger-clj.pre-mend-0928/` (data.mdb sha256
  36fa266937cc3cbd8e1954cc6e7fb2ed39398ac66e504f56535d58273399fbfd). Too
  large for this tree.
- By messenger commands: `hm-deregister` of 20 dead rows; `hm-register
  6f51ad` with readiness probe HM_READY_mindastra_6f51ad_20260928.
- Source: messenger-clj main fc7adef24d76537c9d0ba41c766fcf50e28ede61.

Held message fd09c63d-4344-4fff-b4d8-df814087399d stays in the ledger,
unconsumed: its body was sent again once by `hm-send`, so it must never be
repaired or released.
