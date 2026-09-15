# Identifier token-count witness

This is a small measurement witness, not an entropy benchmark. An existing Nix Python 3.14 environment supplied `tiktoken 0.12.0`; both `cl100k_base` and `o200k_base` produced the same counts:

| String | Tokens |
|---|---:|
| `a1b2c3` | 6 |
| `a1b2c3d4` | 8 |
| `k9m2x7` | 6 |
| `amber-river` | 3 |
| `amber-river-stone` | 5 |
| `a1b2c3d4e5f6` | 12 |

The exact Codex production encoding/model mapping remains unknown. Claude remains unmeasured; no secret, account setup, or provider call was used. These six strings are chosen examples and do not establish equal entropy or statistical efficiency. Earlier identifier design remains a proposal: model-token cost is one criterion, while readability, sayability, legal symbol grammar, and the three local/private, cluster, and public security contexts remain separate decisions.
