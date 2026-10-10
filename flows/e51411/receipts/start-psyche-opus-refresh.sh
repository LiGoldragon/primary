#!/usr/bin/env bash
set -euo pipefail
exec claude --session-id b8785453-ff53-4e5a-9a74-e21edb554467 --model claude-opus-5-5 --effort medium --remote-control --dangerously-skip-permissions "$(< /home/li/primary/flows/e51411/refresh-inject.md)"
