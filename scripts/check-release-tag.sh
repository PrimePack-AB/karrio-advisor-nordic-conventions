#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/check-release-tag.sh TAG

Exit non-zero unless TAG equals v followed by the [project] version in
pyproject.toml. Reads pyproject.toml with ${PYTHON:-python3}, which must
provide tomllib (Python 3.11 or later).
USAGE
}

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

tag=$1
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
version=$("${PYTHON:-python3}" -c '
import sys, tomllib
with open(sys.argv[1], "rb") as f:
    print(tomllib.load(f)["project"]["version"])
' "$root/pyproject.toml")

if [[ "$tag" != "v$version" ]]; then
  echo "tag $tag does not match pyproject.toml version $version (expected v$version)" >&2
  exit 1
fi
echo "tag $tag matches pyproject.toml version $version"
