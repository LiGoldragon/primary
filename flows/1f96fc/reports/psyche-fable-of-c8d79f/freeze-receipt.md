# Psyche Fable c8d79f native-launch freeze

The frozen manifest is [frozen-manifest.json](frozen-manifest.json). It binds a single forthcoming `PsycheHigh` session named `psyche-fable-of-c8d79f` to `claude-fable-5-1[1m]` at `medium` effort, with predecessor `c8d79f66-5ea6-4034-94e4-b685bd359393` preserved.

At the cutoff, the immutable raw vector contains 175 paths and 284030 bytes. Its canonical JSON-vector SHA-256 is `9fd528e4e350d1c6cc9fe9774dc96eb2aed72fb209c3b23c329d4ff54a144541`; the manifest SHA-256 is `5371a0515a050de8aceef0de69ccfdcb75d753fa89f13f0b2e4a589e359d6658`.

The set contains all files in `flows/b81560/vision`, `flows/b05237/vision`, `flows/1ac573/vision`, `flows/c7128c/vision`, and the current c8d79f Unity/vision directory, plus all distilled `Vision/` and `Intent/` files. It also includes whole copies of the detailed Herdr report, c8d79f target shape, and b05237 Fable handoff. The b81560 directory had 20 current paths at cutoff, including two untracked files; that observed set takes precedence over the earlier 19-file claim.

The controller will create only one UUID with forced persistence and `CLAUDE_CODE_CHILD_SESSION` removed. Before its receipt becomes `bootstrap-created`, it must witness `BOOTSTRAP_GUARD_ACK` from that UUID's transcript and one exact native agents-registry row with the configured name and an idle state. Any source hash change aborts native refresh; it never refreshes against mutable roots. After the native 21-skill receipts and exact frozen-payload acknowledgement, the same UUID alone may reach activation. The protected c8d79f session is neither retired nor altered by these steps.
