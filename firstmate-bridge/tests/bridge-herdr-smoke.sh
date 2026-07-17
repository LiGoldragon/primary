#!/usr/bin/env bash
set -euo pipefail

bridge_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
exec "$bridge_root/bin/bridge-herdr" smoke
