---
title: "Development"
---

This section is for working on the plugin itself.
[Plugin layout](architecture/plugin-layout.md) describes how the package registers with karrio and what each module carries, and [Documentation site](architecture/docs-site.md) describes how `docs/` is built and published.
Working notes are indexed in [docs/notes](../notes/README.md).

## Setup

Create a virtual environment and install the forked SDK and the plugin with `pip install -r requirements-dev.txt -e .`.
`requirements-dev.txt` installs the SDK editable from a local checkout of the fork's `feat-shipment-advisors` branch; a `git+https` install cannot replace this, because pip recursively fetches the monorepo's private `karrioapi` submodules that `modules/sdk` does not need.

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

## Known limitations

The README is also the PyPI long description (`readme = "README.md"` in `pyproject.toml`), and its relative links into `docs/` do not resolve on PyPI; fixing them is deferred until the package is published.
