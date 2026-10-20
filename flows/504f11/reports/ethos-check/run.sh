for f in "$@"; do echo "== $f"; nix run github:LiGoldragon/ethos-zero/ethos-proposals -- "Inspect.«$PWD/$f»" 2>&1 | head -${N:-15}; done
