#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: scripts/release.sh VERSION

Prepare release VERSION (CalVer YYYY.M.N) on a clean main: set the
[project] version in pyproject.toml, commit it as chore(release): VERSION,
and create the annotated tag vVERSION. Prints the push command instead of
running it.
USAGE
}

if [[ $# -ne 1 ]]; then
  usage >&2
  exit 2
fi

version=$1
tag="v$version"
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$root"

if [[ ! "$version" =~ ^[0-9]{4}\.[1-9][0-9]?\.[0-9]+$ ]]; then
  echo "version $version is not CalVer YYYY.M.N" >&2
  exit 1
fi
if [[ "$(git symbolic-ref --quiet --short HEAD || true)" != main ]]; then
  echo "release from main; HEAD is not main" >&2
  exit 1
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "working tree is not clean" >&2
  exit 1
fi
if git rev-parse --quiet --verify "refs/tags/$tag" >/dev/null; then
  echo "tag $tag already exists" >&2
  exit 1
fi

sed -i -E "s/^version = \"[^\"]*\"$/version = \"$version\"/" pyproject.toml
scripts/check-release-tag.sh "$tag" >/dev/null

git commit --quiet -m "chore(release): $version" -- pyproject.toml
git tag --annotate --message "$tag" "$tag"

echo "Tagged $tag at $(git rev-parse --short HEAD). Publish with:"
echo "  git push --atomic origin main $tag"
