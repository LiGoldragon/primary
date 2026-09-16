# Primary Claude successor launch package — ready only

This package is the full-context first-prompt assembly for the successor to
primary Claude Flow `840e42`. It is an artifact preparation, not a launch,
dispatch, activation, or approval.

It keeps the prior launch shape because the living asked for the same assembly:
the 134,125-byte system prompt and the 139,691-byte user prompt. The latter is
the retained daemon intent decoded byte-for-byte as UTF-8; its final newline is
absent, matching the launch report's byte count.

`system-prompt.md` carries the nine skill bodies, authoritative Spirit and
Intent, and current primary Vision. `user-prompt.md` carries the superseding
successor context, the ten relayed human prompts, predecessor `fd0f97` log and
Vision, the outstanding decisions, and the source-coverage manifest. Together
they are the launch package the predecessor actually used, preserved without
editing its content.

The package deliberately does not assign a successor session or flow identity.
The prior daemon evidence records that `claude --bg` ignores a caller-supplied
session id and mints the actual daemon identity. The successor must claim that
identity after dispatch.

See `manifest.json` for byte counts, hashes, and filesystem receipts, and
`daemon-dispatch-ready.md` for the supported dispatch shape. No command in this
package has been executed.
