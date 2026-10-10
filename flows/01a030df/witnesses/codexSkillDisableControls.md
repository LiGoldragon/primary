# Codex skill disable controls

Method: probe `codex debug prompt-input`

The `disable_controls` subflow probed the locally installed `codex-cli 0.149.0` with four configurations and reported whether representative system skills, plugin skills, and the recommended-plugin block appeared in generated prompt input.

| Configuration | `skill-creator` | `documents:documents` | `browser:control-in-app-browser` | recommended-plugin block |
|---|---:|---:|---:|---:|
| Default | present | present | present | present |
| `--disable plugins` | present | absent | absent | absent |
| `skills.bundled.enabled=false` | absent | present | present | present |
| Both | absent | absent | absent | absent |

The combined session-only invocation reported by the probe was:

```sh
codex --disable plugins -c 'skills.bundled.enabled=false'
```

The probe also reported that per-skill `[[skills.config]]` entries matched both a system skill name and a namespaced plugin skill name. It did not observe a wildcard or publisher-scoped deny rule.
