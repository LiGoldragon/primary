# Native Claude launch proof

`tools/native-claude-launcher.mjs` prepares one supported native `claude --bg`
invocation from a manifest-backed package. It is a library, so preparing a plan
does not launch a session.

The launcher verifies the system and user artifacts before it returns a plan:
their manifest paths remain inside the package, byte counts and SHA-256 hashes
match, and the UTF-8 user prompt fits the configured argument limit. The system
context is supplied only through `--append-system-prompt-file`; the verified
user body occurs once after `--`. Structured Node subprocess arguments mean
prompt characters are literal and no shell is involved.

Its launch options map standard input to `DEVNULL` (`stdio[0] = 'ignore'`) and
remove `NO_COLOR` from the child environment. This prevents a heredoc or
launcher script inherited by the parent from becoming Claude input.

Run the focused fixture with:

```
node tools/native-claude-launcher.test.mjs
```

The mock process reads file descriptor zero and records its argv. The fixture
proves empty inherited input, exact one-time user-argument delivery with shell
metacharacters preserved literally, and refusal for missing, hash-mismatched,
or oversized artifacts. It never invokes Claude or starts a session.

This only establishes launcher input hygiene. A native daemon may parent its
worker outside a wrapper scope, so worker cgroup placement still requires an
actual-worker observation after an authorized real launch.
