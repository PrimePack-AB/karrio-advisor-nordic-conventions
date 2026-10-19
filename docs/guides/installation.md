---
title: "Installation"
---

Install the plugin from GitHub:

```bash
pip install "git+https://github.com/PrimePack-AB/karrio-advisor-nordic-conventions.git"
```

The plugin registers through the `karrio.plugins` entry point group under the id `advisor_nordic_conventions` and is reported with the plugin type `advisor`.
Installing it adds messages to shipment responses; uninstalling it removes them.

## The karrio fork requirement

The advisories need a karrio SDK with the shipment advisors hook, which is proposed upstream in [karrioapi/karrio#1150](https://github.com/karrioapi/karrio/pull/1150) and, until that pull request merges, is available on its branch `feat-shipment-advisors` in the [karrio fork](https://github.com/Joaqim/karrio).
With released karrio the plugin installs and loads but registers no advisors, so it changes nothing; it logs once that the hook is unavailable and leaves shipment responses unchanged.
Until the feature merges and ships in a karrio release, a working setup requires a local checkout of the fork; see [Development](../development/index.md#setup).
