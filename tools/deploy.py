"""Deploys the committed site to Cloudflare, then submits the sitemap to IndexNow.
Run: python tools/deploy.py
Only HEAD is published, from a temporary worktree, so uncommitted files never go live.
"""
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WRANGLER = "wrangler@4.151.0"


def run(*args, cwd=ROOT):
    subprocess.run(args, cwd=cwd, check=True, shell=os.name == "nt")


def main():
    tree = os.path.join(tempfile.mkdtemp(prefix="xluna-deploy-"), "site")
    run("git", "worktree", "add", "--detach", tree, "HEAD")
    try:
        run("npx", "-y", WRANGLER, "deploy", cwd=tree)
    finally:
        run("git", "worktree", "remove", "--force", tree)
        shutil.rmtree(os.path.dirname(tree), ignore_errors=True)
    run(sys.executable, os.path.join(ROOT, "tools", "indexnow.py"))


if __name__ == "__main__":
    main()
