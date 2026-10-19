---
title: "Development"
---

This section is for working on the plugin itself.
[Plugin layout](architecture/plugin-layout.md) describes how the package registers with karrio and what each module carries, and [Documentation site](architecture/docs-site.md) describes how `docs/` is built and published.
Working notes are indexed in [docs/notes](../notes/README.md).

## Setup

Create a virtual environment and install the forked SDK and the plugin with `pip install -r requirements-dev.txt -e .`.
`requirements-dev.txt` installs the SDK editable from a local checkout of the fork's `develop` branch at `../karrio/modules/sdk`.
The checkout must provide `karrio.core.metadata.PluginMetadata.shipment_advisors`, the advisor hook proposed upstream in [karrioapi/karrio#1150](https://github.com/karrioapi/karrio/pull/1150), and `karrio.lib.StampSeed`, which the PostNord connector needs.
The development setup uses `develop` rather than the branch of the upstream pull request because `develop` carries both, last verified at a7355a5c8 on 2026-10-19.
`develop` is regenerated, so its commit shas are not durable and the requirement is stated by capability rather than by commit.
Each release records the fork snapshot tag it was tested against, as described in [Releasing](#releasing).
A `git+https` install cannot replace the local checkout, because pip recursively fetches the monorepo's private `karrioapi` submodules that `modules/sdk` does not need.

## Connector submodules

`connectors/postnord` and `connectors/dhl-freight-sweden` are git submodules of the standalone PostNord and DHL Freight Sweden connectors, used only during development.
`.gitmodules` sets `update = none` for both, so a plain `git submodule update --init` and pip's VCS installs leave them empty, and the built sdist and wheel do not include them.
Each submodule's gitlink is the last connector commit audited against the advisor's claims about that connector.

Check them out and install them once, copying objects from local clones under `~/projects` when they exist; the script passes `--dissociate`, so the submodules do not depend on those clones afterwards:

```bash
PYTHON=.venv/bin/python scripts/init-connectors --reference-dir ~/projects --install
```

The script overrides `update = none` for its own run and installs both connectors editable with `--no-deps`, so the forked SDK stays in place.
`requirements-dev.txt` does not list them, because a requirements file cannot set `--no-deps` per requirement and would fail where the submodules are not checked out.
The connector-sync skill in `.claude/skills/connector-sync/SKILL.md` audits a connector's new commits against the advisor and bumps a gitlink only when no claim has gone stale.

## Tests

Tests use `unittest` and run from the repository root with an interpreter that can import a karrio SDK providing the advisors hook:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -v -f tests
```

The suite includes `tests/advisor_nordic_conventions/test_examples.py`, which runs the shipment requests in `examples/` through the advisors, and `tests/advisor_nordic_conventions/test_doc_links.py`, which checks that every relative link in the README and the published `docs/` pages resolves.
The connector cross-check tests run when the PostNord and DHL Freight Sweden connectors are importable, as after `scripts/init-connectors --install`, and are skipped otherwise.

## Releasing

Releases are in-development builds published as GitHub releases of this repository only; nothing is published to PyPI or another index.
Versions are CalVer `YYYY.M.N`, where `N` counts releases within the month, and each is tagged `vYYYY.M.N`.
`karrio-ref` under `[tool.primepack]` in `pyproject.toml` names the fork snapshot tag, of the form `snapshot-YYYY.MM.DD.N`, that the release is tested against; update it to a snapshot tag that provides the capabilities listed under [Setup](#setup) before releasing.

Prepare a release from a clean `main` that is up to date with `origin/main`:

```bash
scripts/release.sh 2026.10.7
```

The script sets the `[project] version`, commits it as `chore(release): <version>`, creates the annotated tag `v<version>`, and prints the push command without running it.
Pushing the tag runs `.github/workflows/release.yml`, which checks with `scripts/check-release-tag.sh` that the tag matches the version, installs the fork SDK from the `karrio-ref` snapshot, runs the test suite without the connector submodules, and creates the GitHub release with generated notes headed by the required snapshot.

## Known limitations

The README is also the PyPI long description (`readme = "README.md"` in `pyproject.toml`), and its relative links into `docs/` do not resolve on PyPI; fixing them is deferred until the package is published.
