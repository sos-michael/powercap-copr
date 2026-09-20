# PowerCap RPM repository

Native RPM packages for [PowerCap](https://github.com/powercap/powercap),
including its Linux power-capping library, command-line tools, and development
files. The COPR repository is **grantson/powercap**; `sos-michael` is the
GitHub packaging account, not the COPR owner.

## Install

Enable the repository and install the tools:

```sh
sudo dnf copr enable grantson/powercap && sudo dnf install powercap
```

For headers and development libraries, also run:

```sh
sudo dnf install powercap-devel
```

[Packages and build results](https://copr.fedorainfracloud.org/coprs/grantson/powercap/)

## Automatic updates

GitHub Actions checks upstream `master` every Monday at 14:23 UTC. A new
commit triggers a COPR build for all configured Fedora and EPEL targets.
Successful unchanged revisions are skipped; failed builds are retried.
Packaging changes also trigger a build. The Actions page supports manual
checks and forced rebuilds. No personal computer needs to remain running.

Each source build reads the version from upstream CMake metadata and creates
an archive of the exact Git commit. RPM versions include its UTC commit time
and abbreviated hash. The package runs upstream's hardware-independent
CTest suite; the root-only RAPL hardware test remains disabled upstream.

The `COPR_CONFIG` GitHub repository secret contains the COPR API configuration.
It is used only by trusted default-branch workflows and is never committed.
If credentials expire, renew them at https://copr.fedorainfracloud.org/api/
and update the repository secret.

GitHub disables scheduled workflows in public repositories after 60 days
without repository activity. The scheduler records a successful check once
per month in `.github/last-scheduled-check` to keep this quiet upstream's
schedule active. That file does not trigger RPM builds.

## Local validation

```sh
python3 -m venv .venv
.venv/bin/pip install copr-cli==2.6 copr==2.7
.venv/bin/python -m unittest discover -s .copr -p 'test_*.py' -v
.venv/bin/python .copr/check_upstream.py --dry-run
```

With RPM build tools installed, `make -f .copr/Makefile srpm outdir=/tmp/powercap-srpm`
prepares an SRPM in a Fedora source-build environment. `.copr/prepare.py`
also supports `--prepare-only` and `--source-tree PATH` for offline inspection.
