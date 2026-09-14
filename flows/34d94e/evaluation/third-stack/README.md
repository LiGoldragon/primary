# Third stack offline evaluation

This directory contains a deterministic, synthetic-only evaluation. It does not call a provider, download weights, install a harness, or read credentials. The default command is:

    node flows/34d94e/evaluation/third-stack/run.mjs

The runner executes 12 blinded cases against a fixed evidence rubric and a localhost OpenCode SDK replay fixture. A real adapter run requires an explicit `--provider-descriptor path` and `--secret-fd N`; absent either flag it exits before network/provider work. No secret is read from argv or environment.

The leading comparison is Kimi K3 + OpenCode, with DeepSeek V4.1 Flash, GLM 5.3, and Qwen 3.8 helper metadata retained from the current recommendation. These are evaluation labels, not a provider selection or production authorization.
