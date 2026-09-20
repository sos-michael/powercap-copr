#!/usr/bin/env python3
"""Prepare a snapshot SRPM from upstream master, including its current version."""
import argparse
import datetime
from pathlib import Path
import re
import subprocess
import tempfile

UPSTREAM = "https://github.com/powercap/powercap.git"

def git(*args):
    return subprocess.check_output(["git", *map(str, args)], text=True).strip()

def prepare(tree, spec, out):
    commit = git("-C", tree, "rev-parse", "HEAD")
    cmake = git("-C", tree, "show", "HEAD:CMakeLists.txt")
    match = re.search(r"project\(powercap\s+VERSION\s+(\d+\.\d+\.\d+)", cmake)
    if not match:
        raise ValueError("Cannot find upstream CMake project version")
    version = match.group(1)
    epoch = int(git("-C", tree, "show", "-s", "--format=%ct", "HEAD"))
    stamp = datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
    text = spec.read_text()
    for name, value in {"commit": commit, "shortc": commit[:12], "cdate": stamp, "upstream_version": version}.items():
        text, count = re.subn(r"^%global " + name + r"\s+.*$", "%global " + name + " " + value, text, flags=re.M)
        if count != 1:
            raise ValueError(f"Expected exactly one {name} macro")
    git("-C", tree, "archive", "--format=tar.gz", f"--prefix=powercap-{commit}/",
        f"--output={out / ('powercap-' + commit + '.tar.gz')}", "HEAD")
    result = out / "powercap.spec"
    result.write_text(text)
    print(f"Prepared PowerCap {version} from {commit} ({stamp} UTC)", flush=True)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--source-tree", type=Path, help="Use an existing checkout for local validation")
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    out = args.outdir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tree = args.source_tree
        if tree is None:
            tree = Path(tmp) / "upstream"
            git("clone", "--depth=1", "--branch=master", UPSTREAM, tree)
        spec = prepare(tree.resolve(), args.spec.resolve(), out)
        if not args.prepare_only:
            subprocess.run(["rpmbuild", "-bs", "--define", f"_sourcedir {out}",
                            "--define", f"_srcrpmdir {out}", "--define", "dist %{nil}", str(spec)], check=True)

if __name__ == "__main__":
    main()
