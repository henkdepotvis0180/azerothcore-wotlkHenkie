#!/usr/bin/env python3
"""Validate and sync pinned funserver modules from GitHub. Python 3.8+."""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "funserver" / "modules.json"
MODULE_ROOT = ROOT / "modules"
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
NAME_RE = re.compile(r"^mod-[a-z0-9][a-z0-9_-]*$")


def run(*args):
    subprocess.run(args, check=True)


def validate():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema") != 1 or not isinstance(data.get("modules"), list):
        raise ValueError("Unsupported module manifest schema")
    seen = set()
    for mod in data["modules"]:
        name, repo, commit = (mod.get(k) for k in ("name", "repo", "commit"))
        if not all(isinstance(x, str) for x in (name, repo, commit)):
            raise ValueError("Each module requires name, repo and commit")
        if not NAME_RE.fullmatch(name) or not REPO_RE.fullmatch(repo) or not SHA_RE.fullmatch(commit):
            raise ValueError("Invalid module entry: " + name)
        if name in seen:
            raise ValueError("Duplicate module: " + name)
        seen.add(name)
    print(f"Validated {len(seen)} pinned module(s)")
    return data["modules"]


def sync(modules):
    MODULE_ROOT.mkdir(exist_ok=True)
    for mod in modules:
        name = mod["name"]
        target = MODULE_ROOT / name
        url = "https://github.com/" + mod["repo"] + ".git"
        sha = mod["commit"]
        if not target.exists():
            run("git", "clone", "--no-checkout", url, str(target))
        elif not (target / ".git").exists():
            raise RuntimeError(f"{target} exists but is not a git checkout")
        # Validate origin before any fetch or checkout.
        origin = subprocess.check_output(
            ["git", "-C", str(target), "remote", "get-url", "origin"], text=True
        ).strip()
        if origin.rstrip("/").replace(".git", "").lower() != url.removesuffix(".git").lower():
            raise RuntimeError(f"Origin mismatch for {name}: {origin}")
        if subprocess.check_output(["git", "-C", str(target), "status", "--porcelain"], text=True).strip():
            raise RuntimeError(f"Uncommitted module changes in {name}, refusing to overwrite")
        run("git", "-C", str(target), "fetch", "--no-tags", "origin", sha)
        run("git", "-C", str(target), "checkout", "--detach", sha)
        actual = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
        if actual != sha:
            raise RuntimeError(f"SHA mismatch for {name}")
        print(f"Ready: {name} @ {sha[:12]}")


def main():
    p = argparse.ArgumentParser(description="Manage pinned AzerothCore funserver modules")
    p.add_argument("command", choices=["validate", "sync"])
    args = p.parse_args()
    mods = validate()
    if args.command == "sync":
        sync(mods)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        sys.exit(f"Module management failed: {exc}")
