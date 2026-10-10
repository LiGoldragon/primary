# Hashes and flow ids: what Rust uses, what the code does (witnessed 2026-10-07)

## A 256-bit hash in fast Rust code
The common shape is a newtype over 32 bytes: `struct Hash([u8; 32])`, often `#[repr(transparent)]`, `Copy Clone Eq Hash`, usually `Ord`; hex `Display`/`FromStr`; serde as raw bytes in binary formats, hex in human-readable ones.
- blake3 1.8.7: `Hash([u8; 32])`, constant-time equality, hex via `to_hex()`.
- gitoxide gix-hash: `enum ObjectId { Sha1([u8;20]), Sha256([u8;32]) }`, `Copy Eq Ord`, hex `Display`.
- bitcoin_hashes: `#[repr(transparent)] Hash([u8; 32])`, `Copy Eq Ord Hash`.
- iroh-blobs: `Hash(blake3::Hash)`; parses 64 hex or 52 base32 (claimed, from source summary).
- sha2/digest: a bare `GenericArray<u8, U32>`, no newtype; ring and aws-lc: a digest buffer plus algorithm, not a storage key.

## A flow id today
- Minted by `flow-id` (`repos/harness/src/flow_id.rs`): the harness session id, hyphens removed (128 bits, kept whole in the marker as `identity=`); the alias is 6 hex characters (24 bits), growing by one hex character on a clash. Claude takes the first 6; Codex starts at hex index 23 (past the time-ordered prefix); OpenCode hashes the session with blake3.
- Rendered as lowercase hex only. No word form exists in code.
- Transcripts: Flow Nexus finds them by the full native session id; the `transcript` tool matches a Claude prefix only and has no Codex support.

## Against the three-word design
- The designed id is the first 33 bits as three BIP-39 words (`abandonAbilityAble`); not built.
- 33 bits is 8.25 hex characters, so words → transcript means a 9-hex prefix whose last character spans 8 values: a glob or regex over a superset, then a filter. For Codex the 33 bits must be cut at index 23, or matched as a substring.
- Birthday bound: clashes near 50% around 2^16.5 ≈ 108,000 sessions (arithmetic, not witnessed).
