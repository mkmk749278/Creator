#!/usr/bin/env bash
# Pull native 4K scene renders from the shard branches (cantpay-4k-a/b/c): each pushes parts4k/<id>.url
# ("<url> <md5> <duration> <WxH>"); download into assets/scenes4k/ and check the md5. Prints how many are in place.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"; OUT="$ROOT/projects/cant-pay-minimum/assets/scenes4k"; mkdir -p "$OUT"
cd "$ROOT"
for b in cantpay-4k-a cantpay-4k-b cantpay-4k-c; do
  git fetch -q origin "$b" 2>/dev/null || continue
  for f in $(git ls-tree --name-only origin/$b projects/cant-pay-minimum/parts4k/ 2>/dev/null); do
    id=$(basename "$f" .url); [ -s "$OUT/$id.mp4" ] && continue
    read -r url md5 _ <<< "$(git show origin/$b:$f)"
    for i in 1 2 3 4; do curl -sSL -m 900 "$url" -o "$OUT/$id.part" && break; sleep $((2**i)); done
    if [ "$(md5sum "$OUT/$id.part" | cut -c1-32)" = "$md5" ]; then mv "$OUT/$id.part" "$OUT/$id.mp4"; echo "got $id"; else echo "BAD md5 $id"; rm -f "$OUT/$id.part"; fi
  done
done
echo "have $(ls "$OUT"/*.mp4 2>/dev/null | wc -l) of $(ls "$ROOT/video/cantpay" | wc -l)"
