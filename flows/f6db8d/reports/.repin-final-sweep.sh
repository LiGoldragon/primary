#!/usr/bin/env bash
# Repin one repository's Cargo.toml and Cargo.lock to the final producer heads.
# Usage: repin.sh <repo-abs-path>
set -euo pipefail
R="$1"
declare -A REV=(
  [protos]=1febca7836bf8d5f5973a302fdd50aa9c84c159b
  [datom-codec]=09e2a9d52bf7f2f11e51d15cb6c3177f72c6c927
  [ethos-zero]=4bf73cae8d4f5a2072c76a11cd2f00aa3fe9f8e3
  [nexus]=c495f2acbfff57e017092b9cc1fbf9f73ca2badf
)
declare -A VER=(
  [protos]=0.31.0
  [datom-codec]=0.31.0
  [datom-codec-derive]=0.31.0
  [ethos-zero]=10.0.0
)
# Cargo.toml / any manifest: rewrite the rev of each producer git dep.
for f in $(find "$R" -name 'Cargo.toml' -not -path '*/target/*' -not -path '*/.git/*'); do
  for p in protos datom-codec ethos-zero nexus; do
    python3 - "$f" "$p" "${REV[$p]}" <<'PY'
import re,sys
path,pkg,rev=sys.argv[1],sys.argv[2],sys.argv[3]
s=open(path).read()
pat=re.compile(r'(LiGoldragon/'+re.escape(pkg)+r'(?:\.git)?"?\s*,?\s*[^\n]*?rev\s*=\s*")[0-9a-f]{40}(")')
s2=pat.sub(lambda m:m.group(1)+rev+m.group(2),s)
if s2!=s: open(path,'w').write(s2)
PY
  done
done
# Cargo.lock: rewrite version + source of each producer package entry.
for f in $(find "$R" -name 'Cargo.lock' -not -path '*/target/*' -not -path '*/.git/*'); do
  python3 - "$f" <<PY
import re,sys
path=sys.argv[1]
rev={'protos':'${REV[protos]}','datom-codec':'${REV[datom-codec]}','datom-codec-derive':'${REV[datom-codec]}','ethos-zero':'${REV[ethos-zero]}'}
ver={'protos':'${VER[protos]}','datom-codec':'${VER[datom-codec]}','datom-codec-derive':'${VER[datom-codec-derive]}','ethos-zero':'${VER[ethos-zero]}'}
repo={'protos':'protos','datom-codec':'datom-codec','datom-codec-derive':'datom-codec','ethos-zero':'ethos-zero'}
blocks=open(path).read().split('[[package]]')
out=[blocks[0]]
for b in blocks[1:]:
    m=re.search(r'^name = "([^"]+)"',b,re.M)
    n=m.group(1) if m else None
    if n in rev:
        b=re.sub(r'^version = "[^"]+"','version = "%s"'%ver[n],b,count=1,flags=re.M)
        b=re.sub(r'^source = "git\+https://github.com/LiGoldragon/[^"]+"',
                 'source = "git+https://github.com/LiGoldragon/%s?rev=%s#%s"'%(repo[n],rev[n],rev[n]),
                 b,count=1,flags=re.M)
    out.append(b)
open(path,'w').write('[[package]]'.join(out))
PY
done
