#!/usr/bin/env python3
"""
Single-file backdated commit test script.
Hardcoded credentials: tejas122125 <tejasweekumarsingh@gmail.com>
Zero prompts - fully automated.
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta

USER_NAME = "tejas122125"
USER_EMAIL = "tejasweekumarsingh@gmail.com"
REPO_URL = "https://github.com/tejas122125/example.git"
TARGET_FILE = "server/bi_stream.go"
DAYS_AGO = 30
COMMIT_MESSAGE = "implement bidirectional streaming endpoint"
BRANCH = "main"

def run_cmd(cmd, env=None):
    print(f"[*] Running: {cmd}")
    res = subprocess.run(cmd, shell=True, env=env, text=True, capture_output=True)
    if res.stdout.strip():
        print(res.stdout.strip())
    if res.returncode != 0 and res.stderr.strip():
        print(f"[!] {res.stderr.strip()}", file=sys.stderr)
    return res

def main():
    print("=" * 60)
    print("  Backdated Commit (Single File Test - Fully Automated)")
    print(f"  Author      : {USER_NAME} <{USER_EMAIL}>")
    print(f"  Target File : {TARGET_FILE}")
    print(f"  Repo URL    : {REPO_URL}")
    print(f"  Backdate    : {DAYS_AGO} days ago")
    print("=" * 60)

    # 1. Set Git user config
    run_cmd(f'git config user.name "{USER_NAME}"')
    run_cmd(f'git config user.email "{USER_EMAIL}"')
    run_cmd(f'git config --global user.name "{USER_NAME}"')
    run_cmd(f'git config --global user.email "{USER_EMAIL}"')

    # 2. Calculate backdate (30 days ago)
    now = datetime.now()
    backdate = now - timedelta(days=DAYS_AGO, hours=3, minutes=15)
    date_str = backdate.strftime("%Y-%m-%dT%H:%M:%S")

    # 3. Stage the file
    run_cmd(f"git add {TARGET_FILE}")

    # 4. Set environment dates
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    # 5. Commit or amend
    has_commits = subprocess.run("git rev-parse --verify HEAD", shell=True, text=True, capture_output=True).returncode == 0
    if has_commits:
        print(f"\n[*] Amending commit with author {USER_EMAIL} and date {date_str}...")
        cmd = f'git commit --amend --no-edit --author="{USER_NAME} <{USER_EMAIL}>" --date="{date_str}"'
    else:
        print(f"\n[*] Creating new backdated commit on {date_str}...")
        cmd = f'git commit -m "{COMMIT_MESSAGE}" --author="{USER_NAME} <{USER_EMAIL}>" --date="{date_str}"'

    res = subprocess.run(cmd, shell=True, env=env, text=True, capture_output=True)
    if res.returncode == 0:
        print(f"[✔] Commit recorded successfully!")
    else:
        print(f"[!] Commit output:\n{res.stdout}\n{res.stderr}")

    # 6. Branch and remote
    run_cmd(f"git branch -M {BRANCH}")
    remote_check = subprocess.run("git remote get-url origin", shell=True, text=True, capture_output=True)
    if remote_check.returncode == 0:
        run_cmd(f"git remote set-url origin {REPO_URL}")
    else:
        run_cmd(f"git remote add origin {REPO_URL}")

    # 7. Force push to GitHub
    print(f"\n[*] Pushing to GitHub ({BRANCH})...")
    push_res = subprocess.run(f"git push -u origin {BRANCH} --force", shell=True, text=True, capture_output=True)
    if push_res.returncode == 0:
        print("\n" + "=" * 60)
        print(" [SUCCESS] Pushed to GitHub with your verified email & backdate!")
        print(f" View commit: https://github.com/tejas122125/example/commits/{BRANCH}")
        print("=" * 60)
    else:
        print(f"\n[ERROR] Push failed:\n{push_res.stderr.strip()}", file=sys.stderr)

if __name__ == "__main__":
    main()
