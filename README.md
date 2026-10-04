# PowerCap RPMs

Unofficial RPM packages for [PowerCap](https://github.com/powercap/powercap),
a library and command-line tools for managing Linux power-capping devices.

## Install

```sh
sudo dnf copr enable grantson/powercap
sudo dnf install powercap
```

For headers and development libraries:

```sh
sudo dnf install powercap-devel
```

See [COPR](https://copr.fedorainfracloud.org/coprs/grantson/powercap/) for
available Fedora and EPEL targets, packages, and build results.

## Updates

GitHub Actions checks upstream `master` weekly and submits new snapshots to
COPR. Updates arrive through DNF alongside your other packages. These
packages follow development commits rather than only tagged releases.

You can also [run an update check manually](https://github.com/sos-michael/powercap-copr/actions/workflows/upstream.yml).
