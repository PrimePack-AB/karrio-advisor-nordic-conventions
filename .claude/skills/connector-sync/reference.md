# Connector sync reference

## Path classification

| Changed path in the connector | What it can make stale in the advisor |
|---|---|
| `karrio/providers/<pkg>/units.py` | Literals mirrored in `lanes.py`, `territories.py`, `exclusions.py`, and `rules/`; sha-bearing comments naming `units.py`; `Source` statements about service codes, lanes, or territories |
| `karrio/providers/<pkg>/shipment/*.py` | Advisory messages and `Source` statements about what the connector sends, refuses, or validates at booking |
| `karrio/providers/<pkg>/*.py` (other) | Claims about document production, stamping, and option handling |
| `README.md`, `docs/concepts/*.md` | `blob/<sha>` URL constants in `sources.py` and their footnotes |
| `vendor/`, `schemas/` | Claims resting on the carrier specification the connector vendors; compare tree ids first |
| `pyproject.toml` | Nothing by itself; note the version in the report |
| `tests/`, `docs/notes/`, `docs/development/`, `.github/`, `CLAUDE.md` | Nothing the advisor cites, unless the inventory below finds a citation |

## Mirrored constants

The connector constants that the cross-check tests compare with the advisor's literals:

```bash
rg -o -N --no-filename 'units\.[A-Z][A-Z0-9_]+' tests/advisor_nordic_conventions/ | sort -u
```

Diff each listed constant across the range with `git -C connectors/<c> diff "$old" "$new" -- karrio/providers/<pkg>/units.py`.

## Citation inventory

Connector URL constants, `Source` objects, and fork pins in `sources.py`:

```bash
rg -n 'karrio-(postnord|dhl-freight-sweden)|providers/(postnord|dhl_freight_sweden)|karrio fork|karrio modules/' karrio/plugins/advisor_nordic_conventions/sources.py
rg -n -i -B2 -A2 'connector' karrio/plugins/advisor_nordic_conventions/sources.py
```

Sha-bearing comments in code, which may wrap over two lines:

```bash
rg -n -B1 -A1 'karrio-(postnord|dhl-freight-sweden)|karrio develop|\b[0-9a-f]{7,40}\b, (units|shipment)' karrio/plugins/advisor_nordic_conventions/
```

Footnotes, the spec, and the published pages:

```bash
rg -n 'PrimePack-AB/karrio-(postnord|dhl-freight-sweden)' docs/concepts/advisories.md
rg -n 'karrio-(postnord|dhl-freight-sweden)|PrimePack-AB/karrio-' openspec/specs README.md docs --glob '!docs/notes/**'
```

Advisory messages that assert connector behaviour, and the spec requirements that state the same:

```bash
rg -n -i 'connector' karrio/plugins/advisor_nordic_conventions/rules/
rg -n -i 'the connector' openspec/specs/plugins/advisor-nordic-conventions/spec.md
```

Map an advisory to its requirement through its code in `codes.py`, which the spec names in the requirement's scenarios.

## Report template

Write the report in the conversation, not in a file.

```markdown
# Connector sync report: <c>

Range: <old-short>..<new-short> (<n> first-parent commits), origin/main fetched <date>.
Outcome: stale claims found; gitlink not bumped.

## Mechanical checks

Import at <old-short> and <new-short>: <ok, or the error and missing symbol>.
Tests: <passed>/<failed>/<skipped>, log at <path>; cross-check failures: <test and subtest, constant, difference>.
AGENTS.md verification: <clean, or the diff>.

## Stale claims

### <short name> (`<code>`)

Claim: "<quoted text>" at `<file>:<line>`, cited source `<constant>`.
Old evidence: `<connector path>:<lines>` at <old-short> shows <behaviour>.
New evidence: `<connector path>:<lines>` at <new-short> shows <behaviour>, introduced by <sha> "<subject>".
Spec requirement to change: "<requirement heading>" at `openspec/specs/plugins/advisor-nordic-conventions/spec.md:<line>`.

## Current claims

<citation>: unchanged between <cited> and <new-short>; <reading pin that may advance, or historical event whose behaviour survives>.

## Pins that stay

<citation>: cited content changed between <cited> and <new-short>, claim still holds; the pin stays at <cited>.

## New behaviour without an advisory

<sha> "<subject>": <behaviour>, bearing on <advisory or lane>.

## Reported only

Orphaned fork pins: <FACTS_NOTE, PNS, DFS, CONNECTOR_FLAG_MAPPING, karrio develop comments>, with any range commit touching what they describe.
SDK capabilities: the capability check <passes | fails with <error>>, the checkout is at <sha>.
```
