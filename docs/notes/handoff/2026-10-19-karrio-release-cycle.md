---
title: "Hand-off: karrio release cycle and consumer integration"
---

This note hands off a cross-repository session from 2026-10-19 that added a release cycle so `releases.atom` feeds drive the jqpkgs karrio derivations.
It covers what landed, what is in flight, and the decisions awaiting the user.

## Landed and pushed

The fork Joaqim/karrio tags each deployed `develop` with a transient annotated tag `snapshot-YYYY.MM.DD.N`, created by `docs/notes/workflow/snapshot-tag.sh` and called from `rebuild-develop.sh` on `docs-openspec` (commit `057ea5fa5`).
Snapshot tags are not releases, have no GitHub Release object, and may be deleted once no jqpkgs pin, plugin `karrio-ref`, or consumer npins pin refers to them; the policy is in `develop-assembly.md` under "Snapshot tags".
Existing tags: `snapshot-2026.07.07.1` (`e2960b597`), `snapshot-2026.10.13.1` (`62f4d4764`), `snapshot-2026.10.15.1` (`71936ac88`), `snapshot-2026.10.19.1` (`a7355a5c8`), and `snapshot-2026.10.19.2` (`7aacaa2e4`, the deployed `develop`).

PrimePack-AB/karrio-postnord `v2026.10.1`, karrio-dhl-freight-sweden `v2026.10.1`, and karrio-advisor-nordic-conventions `v2026.10.7` are published GitHub Releases.
Each repository has `[tool.primepack] karrio-ref` in `pyproject.toml`, `scripts/check-release-tag.sh`, `scripts/release.sh <YYYY.M.N>`, `.github/workflows/release.yml` on `v*` tags, and a "Releasing" section in its development docs.
The dhl-freight-sweden release note says "tested against" rather than "requires", because that connector works with upstream karrio.

jqpkgs main (`d05117b`) fetches `pkgs/ka/karrio` by `snapshot-${version}` and the plugins by `v${version}`, each with a nix-update `passthru.updateScript` (karrio uses `--version-regex snapshot-(.*)`).
Each plugin has `passthru.tests.unit` running its suite against the jqpkgs karrio, collected into a flake `checks` output that `hydraJobs` includes.
The first buildbot run of those checks has not been inspected.
`nix flake check --no-build` fails on `uncenter-scripts`, also on the previous main; it is outside `hydraJobs`.

## In flight, not committed

A `karrio-nix` plugins seam was started and stopped before any commit; the empty worktree is `/home/joaqim/projects/karrio-nix.worktrees/server-plugins` on branch `server-plugins` and can be removed or reused.
Its brief: a `plugins ? [ ]` argument on `pkgs/karrio-server.nix` and a `services.karrio.plugins` option (default empty, server `.drv` unchanged when empty), a check proving a dummy plugin is discovered, generic README docs, and exposing the `karrioPython` and `karrio-sdk` that plugins must be built against, following any `src` override, with a guard against a second karrio in a plugin closure if cheap.
`karrio-nix` must stay generic: upstream `main` by default, no fork, jqpkgs, or PrimePack references.

## Awaiting the user's decision

The consumer pins of the fork's `develop` are now covered by snapshot tags but still pinned by sha.
npins 0.5.1 supports `npins add git https://github.com/Joaqim/karrio.git --name <pin> --release-prefix snapshot- --at <tag>` and release-tracking `npins add github <owner> <repo>`; tag hashes equal the current commit-pin hashes, so the switch changes no derivation.
Proposed answers, not yet confirmed by the user:

1. Hold plan's pin change until the user commits the in-progress work in plan's main checkout, which includes an uncommitted `npins/sources.json` moving `karrio` to `a7355a5c8` and two plugin pins; committed plan main pins `62f4d4764` (`snapshot-2026.10.13.1`).
2. Convert only the fork pins now (ongoing-karrio-bridge `karrio` at `snapshot-2026.10.13.1`, karrio-workspace `karrio-fork` at `snapshot-2026.07.07.1`), unfrozen; the plugin pins sit 6 to 96 commits behind their releases, so moving them is a version bump deferred to the plan integration.
3. Run `npins upgrade` as a separate `chore(npins)` commit in ongoing-karrio-bridge and karrio-workspace, whose `sources.json` format 7 npins 0.5.1 cannot read.
4. karrio-workspace has an uncommitted `npins/sources.json` bumping only its `karrio-nix` pin, plus an uncommitted `primepack/module.nix`; leave both alone.

The user's stated target for plan: use the jqpkgs plugin derivations while overriding their `src` from plan's own npins.
Proposed integration, three parts in order:

1. jqpkgs: make `karrio` and `python3` arguments of each plugin `package.nix`, defaulting through the by-name scope to the jqpkgs karrio so derivations stay identical, letting consumers `.override { python3 = karrioPython; karrio = karrio-sdk; }`.
2. karrio-nix: the plugins seam above.
3. plan: take the plugins from the jqpkgs overlay (plan already has the `jqpkgs` flake input), apply that override plus `.overrideAttrs { src = sources.<plugin>; version = …; }`, pass them through `services.karrio.plugins` in place of the bind mounts in `modules/clan/services/karrio/flake-module.nix` and the local builds in `modules/nixpkgs/overlays/karrio.nix`, move the plugin pins to releases, and bump the `jqpkgs` and `karrio-nix` inputs; verify with a targeted build of the karrio server for its machine, proposing rather than running a full system build.

ongoing-karrio-bridge builds the plugins locally in a similar way and is proposed to follow later.
Work happens in worktrees with local commits; pushes are batched for the user's approval.
