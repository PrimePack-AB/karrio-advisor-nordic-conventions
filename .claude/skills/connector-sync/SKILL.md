---
name: connector-sync
description: Audit and sync this advisor's claims about the standalone PostNord and DHL Freight Sweden connectors against new connector commits, using the development-only submodules under connectors/. Use when a connector has new commits on origin/main, when asked to sync, bump, update, or audit the connector submodules or the connector commits the advisor cites, when checking whether advisory messages, mirrored unit tables, sources.py connector citations, or docs/concepts/advisories.md connector footnotes are stale, or when a connector cross-check test fails.
---

# Connector sync

This procedure carries changes in one direction only, from the PostNord and DHL Freight Sweden connectors into this advisor's code, citations, and docs.
It never edits a connector.
The submodules `connectors/postnord` and `connectors/dhl-freight-sweden` are development-only: `.gitmodules` sets `update = none`, packaging excludes them, and consumers of the plugin never need them.
Each submodule's gitlink is the last connector commit audited against the advisor; there is no other lock file.

Run every connector separately, and finish one connector's outcome before starting the other.
In the commands below `<c>` is `postnord` or `dhl-freight-sweden`, `<pkg>` is `postnord` or `dhl_freight_sweden`, and `$PY` is the interpreter of the development virtual environment, normally `.venv/bin/python`.
[reference.md](reference.md) holds the path classification table, the citation inventory commands, and the report template; read it before the claim audit.

## Preflight

Confirm both submodules are checked out; a leading `-` in `git submodule status` means they are not, and `scripts/init-connectors --reference-dir ~/projects --install` (with `PYTHON=$PY`) initializes them.
Confirm the superproject and the submodule are clean with `git status --short` and `git -C connectors/<c> status --short`.
Fetch with `git -C connectors/<c> fetch origin`.
The sync target is `origin/main`; a commit that is not on the connector's remote cannot be cited, so never sync to a local branch or an unpushed commit.

Record the old and new commits:

```bash
old=$(git rev-parse HEAD:connectors/<c>)
new=$(git -C connectors/<c> rev-parse origin/main)
git -C connectors/<c> log --oneline --first-parent "$old..$new"
```

If the range is empty there is nothing to sync.

Check that the connector imports against the installed karrio SDK at both commits (`git -C connectors/<c> checkout <commit>` then `$PY -c "import karrio.providers.<pkg>"`).
The cross-check tests skip only on `ImportError`; an `AttributeError` from a missing SDK symbol leaves part of the package in `sys.modules`, so later tests run against a half-imported connector and their outcome depends on test order.
Report an import failure with the missing symbol, and check that the installed SDK provides the capabilities named in the `requirements-dev.txt` comment; `PluginMetadata` is an attrs class, so test its fields with `attr.fields_dict`:

```bash
$PY -c 'import attr, karrio.lib as lib; from karrio.core.metadata import PluginMetadata; assert "shipment_advisors" in attr.fields_dict(PluginMetadata); lib.StampSeed'
```

Report a failure of this check; never change the SDK checkout or `requirements-dev.txt`.

## Classify the range

List the changed paths with `git -C connectors/<c> diff --stat "$old" "$new"` and sort them with the classification table in [reference.md](reference.md).
Provider constants in `karrio/providers/<pkg>/units.py` are mirrored as literals in `lanes.py`, `territories.py`, `exclusions.py`, and `rules/`.
Booking behaviour in `karrio/providers/<pkg>/shipment/*.py` backs the advisory messages that state what the connector sends, refuses, or validates.
`README.md` and `docs/concepts/*.md` are cited documents.
For `vendor/` and `schemas/` compare tree ids, `git -C connectors/<c> rev-parse "$old:vendor" "$new:vendor"`, and read the diff only when they differ.
A `pyproject.toml` version change is noted in the report and needs no action on its own.

## Mechanical checks

Check out the target in the submodule and reinstall:

```bash
git -C connectors/<c> checkout --detach "$new"
$PY -m pip install --no-deps -e connectors/<c>
```

Run the suite and keep the log outside the repository, because `logs/` is not ignored here:

```bash
log_dir=${XDG_STATE_HOME:-$HOME/.local/state}/agent-logs/karrio-advisor-nordic-conventions
mkdir -p "$log_dir"
PYTHONDONTWRITEBYTECODE=1 $PY -m pytest -q -rs 2>&1 | tee "$log_dir/connector-sync-<c>-$(date +%Y%m%d-%H%M%S).log"
```

The cross-check tests are `tests/advisor_nordic_conventions/test_lanes.py`, `test_territories.py`, `test_exclusions.py`, `test_dhl_freight_sweden.py`, and `test_dhl_country_requirements.py`.
A skip of a cross-check test for the connector under audit is a preflight failure, not a pass.
A failure is a stale mirrored literal; record it as a finding.
Then run the four verification commands in `AGENTS.md`.

## Claim audit

Inventory every place the advisor cites this connector with the commands in [reference.md](reference.md): the `Source` constants and URL constants in `sources.py`, the sha-bearing comments in `lanes.py`, `exclusions.py`, and `rules/`, the footnotes in `docs/concepts/advisories.md`, and the commit references in `openspec/specs/plugins/advisor-nordic-conventions/spec.md`.

For each citation, diff the cited file at the cited commit against the target, `git -C connectors/<c> diff <cited> "$new" -- <path>`, and decide whether the cited statement still holds.
A citation that names a commit as the point a behaviour began ("from commit X the connector refuses …", a `/commit/<sha>` URL) records a historical event: it stays true as long as the behaviour still exists at the target, so check that the behaviour survives, and never rewrite the commit.
A citation that reads a file at a commit (a `/blob/<sha>/` URL with a read date, or a comment naming a commit and `units.py`) is a reading pin.
A reading pin whose cited content is unchanged may advance; one whose cited content changed while the claim still holds stays at its commit and is listed in the report; one whose claim no longer holds is a stale claim.

Audit every claim against the target commit, not only those the range touched: a claim can already be stale at the old gitlink, and the range classification only says where new drift is likely.
Then read every advisory message in `rules/` that asserts connector behaviour, found with `rg -n -i 'connector' karrio/plugins/advisor_nordic_conventions/rules/`, together with each `Source` whose statement describes what the connector does.
For each, find the code that implements the behaviour at the target commit and confirm the message still describes it.
Messages state their claims in present tense ("currently sends", "refuses", "validates"); one counter-example in the target code makes the claim stale.
List new connector behaviour that bears on an advisory's lane but contradicts no claim, such as a new refusal or a changed EU VAT area test, under its own heading; it does not block a sync.
Claims backed by `PNS`, `DFS`, `FACTS_NOTE`, or a `karrio develop` or `karrio modules/connectors/...` path describe the karrio fork rather than the standalone connector, but the advisory still runs against the standalone connector, so audit the claim against the standalone code all the same.

## Outcome

If any claim is stale, write the report from the template in [reference.md](reference.md) and stop.
Do not bump the gitlink, do not edit advisories, and do not commit the report.
Each finding names the claim, its `file:line`, the evidence at the old and the new commit with shas, and the requirement in `openspec/specs/plugins/advisor-nordic-conventions/spec.md` that must change.
The spec is normative, so the fix goes through an OpenSpec change, after which this procedure runs again.

If no claim is stale:

1. Leave the submodule at `$new` and stage it with `git add connectors/<c>`.
2. Advance each reading pin whose cited content is unchanged between its commit and `$new`: the `blob/<sha>` in the `sources.py` constant, its read date (today), and the matching footnote in `docs/concepts/advisories.md`, which repeats the URL and date annotation verbatim as `AGENTS.md` requires. Advance sha-bearing reading comments the same way.
3. Leave historical-event citations, the README matrix, and the advisory reference tables alone unless `AGENTS.md` requires an edit because a constant changed.
4. Run the `AGENTS.md` verification commands and the test suite again.
5. Commit with `chore(connectors): sync <c> to <short-sha>`, listing the audited range and the pins advanced in the body.

## Out of scope, reported only

Some citations point into the karrio fork rather than the standalone connectors, and this procedure does not sync them: `FACTS_NOTE`, `PNS`, `DFS`, the `CONNECTOR_FLAG_MAPPING` path, and comments citing `karrio develop <sha>`.
List them in every report as orphaned fork pins, together with any change in the standalone connector that touches the behaviour they describe.
Report an installed SDK that fails the capability check above without changing the checkout or `requirements-dev.txt`.
