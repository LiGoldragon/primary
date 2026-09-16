#!/usr/bin/env bash
set -euo pipefail
package_dir="$(cd "$(dirname "$0")" && pwd)"
(cd "$package_dir/current" && sha256sum -c "$package_dir/current-source-sha256sums.txt" --quiet)
node "$package_dir/prepare.mjs" | grep -F '"dryRun":true'
