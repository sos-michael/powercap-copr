#!/usr/bin/env python3
"""Build changed upstream sources in COPR; skip successful unchanged snapshots."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

from copr.v3 import Client

def decide(commit, latest, successful, force=False):
    if latest and latest["state"] not in ("succeeded", "failed", "canceled", "skipped"):
        return False, f"Build {latest['id']} is still {latest['state']}; no duplicate submitted."
    if force:
        return True, "Rebuilding after a packaging change or manual request."
    if latest and latest["state"] != "succeeded":
        return True, f"Retrying after build {latest['id']} {latest['state']}."
    version = (successful or {}).get("source_package", {}).get("version", "")
    match = re.search(r"git([0-9a-f]{7,40})(?:\b|$)", version)
    if match and commit.startswith(match.group(1)):
        return False, f"Up to date: {commit[:12]} is already in successful build {successful['id']}."
    return True, f"New upstream revision {commit[:12]}; building all configured targets."

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    commit = subprocess.check_output([
        "git", "ls-remote", "--exit-code", "https://github.com/powercap/powercap.git", "refs/heads/master"
    ], text=True, timeout=120).split()[0]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Invalid upstream commit")
    package = Client.create_from_config_file().package_proxy.get(
        "grantson", "powercap", "powercap", with_latest_build=True, with_latest_succeeded_build=True)
    history = package.get("builds", {})
    build, message = decide(commit, history.get("latest"), history.get("latest_succeeded"), args.force)
    print(message, flush=True)
    if build and not args.dry_run:
        # The saved make_srpm recipe fetches current master and records the
        # exact source revision. Wait so failed RPM builds fail the workflow.
        subprocess.run([str(Path(sys.executable).with_name("copr-cli")), "build-package",
                        "grantson/powercap", "--name", "powercap"], check=True)

if __name__ == "__main__":
    main()
