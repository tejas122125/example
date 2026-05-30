#!/usr/bin/env python3
"""
Realistic human-like commit history with VARIED green shades on GitHub.
- Dark green days  : 8-15 commits (heavy work day)
- Medium green days: 3-6 commits
- Light green days : 1-2 commits
- Many grey gaps   : no commits (weekends, lazy days)

Each commit makes a tiny real file change (blank line toggle) so git
actually sees a diff and creates a proper commit.
"""

import os
import sys
import random
import subprocess
from datetime import datetime, timedelta

USER_NAME  = "tejas122125"
USER_EMAIL = "tejasweekumarsingh@gmail.com"
REPO_URL   = "https://github.com/tejas122125/example.git"
BRANCH     = "main"

MESSAGES = [
    "updated code", "fixed stuff", "minor fix", "changes", "small update",
    "fix", "updated", "more changes", "some changes", "update",
    "misc changes", "random fix", "small changes", "edited", "modified", "tweaks",
    "working on it", "almost done", "wip", "in progress", "not done yet",
    "still working", "halfway there", "making progress", "getting there",
    "rough version", "draft", "initial", "start", "beginning", "first pass",
    "done", "finished", "completed", "ok done", "finally done",
    "wrapped up", "should be good",
    "oops", "ugh fixed again", "why does this break", "fix again", "fixed again",
    "seriously fixed now", "stop breaking", "not again", "broken again",
    "hopefully fixed", "please work", "come on", "argh",
    "i hate this",
    "ok now it works", "this should work", "works now", "tested and working",
    "seems to work", "looks fine", "good enough", "lets see", "try this",
    "trying something", "trying a fix", "attempt fix",
    "removed extra code", "added missing part", "cleanup", "small cleanup",
    "cleaned up", "cleaned some stuff", "refactor", "reorganize",
    "moved things around", "deleted junk", "removed debug", "removed logs",
    "removed comment", "added comment", "added comments", "better naming",
    "test", "testing", "temp", "quick test", "just testing",
    "debug", "debug stuff", "added print", "removed print",
    "tweaked a bit", "minor tweak", "tiny change", "one line fix",
    "formatting", "whitespace", "indent fix", "typo", "typo fix",
    "spelling", "blank line",
    "reverted", "reverted changes", "going back", "undo last change",
    "revert broken thing",
    "quick fix", "final fix", "last fix", "one more fix", "another fix",
    "hot fix", "patch", "small patch", "minor patch",
    "forgot this file", "missed this", "oh wait", "actually fixed",
    "pushed wrong file", "added back", "this was missing",
    "had to add this", "needed this", "new stuff", "old stuff removed",
    "config fix", "not sure why", "works on my machine",
    "minor adjustment", "small adjustment", "adjusted",
    "cleaned it up", "code review changes", "nit fix",
    "addressed comments", "updated logic", "logic fix",
    "edge case", "handle edge case", "null check",
    "missed a case", "forgot to save", "late night fix",
    "morning fix", "before i forget", "adding file",
    "deleted file", "renamed stuff", "moved file",
    "updated imports", "import fix", "dependency update",
    "updated version", "version bump", "fixed build",
    "build fix", "fixed error", "error handled",
    "added handling", "better error", "log fix",
    "added logs", "verbose", "silent mode", "debug mode off",
    "clean run", "passes now", "green", "all good",
]

# Go files we can freely toggle blank lines in
EDITABLE_FILES = [
    "server/bi_stream.go",
    "server/client_stream.go",
    "server/main.go",
    "server/server_stream.go",
    "server/unary.go",
    "client/main.go",
    "client/bi_stream.go",
    "client/client_stream.go",
    "client/server_stream.go",
    "client/unary.go",
    "proto/greet.proto",
    "go.mod",
]

ALL_FILES = EDITABLE_FILES + ["proto/greet.pb.go", "proto/greet_grpc.pb.go", ".gitignore", "README.MD"]

def run(cmd, env=None):
    return subprocess.run(cmd, shell=True, env=env, text=True, capture_output=True)

def toggle_blank_line(filepath):
    """Add or remove a trailing blank line to create a real git diff."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if content.endswith("\n\n"):
        content = content.rstrip("\n") + "\n"
    else:
        content = content.rstrip("\n") + "\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def commit_at(message, dt, filepath):
    """Touch a file and commit it at the given datetime."""
    toggle_blank_line(filepath)
    date_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"]    = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    run(f"git add {filepath}")
    cmd = f'git commit -m "{message}" --author="{USER_NAME} <{USER_EMAIL}>" --date="{date_str}"'
    res = subprocess.run(cmd, shell=True, env=env, text=True, capture_output=True)
    if res.returncode == 0:
        print(f"  [✔] {date_str[:10]} {dt.strftime('%H:%M')}  \"{message}\"  → {filepath.split('/')[-1]}")
    else:
        print(f"  [!] {res.stderr.strip()}")

def random_msg(last=None):
    msg = last
    while msg == last:
        msg = random.choice(MESSAGES)
    return msg

def main():
    print("=" * 65)
    print("  Varied Shade Commit History  (3 months, realistic green graph)")
    print(f"  Author  : {USER_NAME} <{USER_EMAIL}>")
    print(f"  Repo    : {REPO_URL}")
    print("=" * 65)

    # ── wipe & re-init ──────────────────────────────────────────────
    if os.path.exists(".git"):
        print("\n[*] Clearing old git history...")
        subprocess.run("rmdir /s /q .git", shell=True)

    run(f"git init -b {BRANCH}")
    run(f'git config user.name  "{USER_NAME}"')
    run(f'git config user.email "{USER_EMAIL}"')
    run(f'git config --global user.name  "{USER_NAME}"')
    run(f'git config --global user.email "{USER_EMAIL}"')

    # ── initial commit: all files at once, 90 days ago ──────────────
    now  = datetime.now()
    init_date = now - timedelta(days=90)
    init_str  = init_date.strftime("%Y-%m-%dT%H:%M:%S")
    env0 = os.environ.copy()
    env0["GIT_AUTHOR_DATE"]    = init_str
    env0["GIT_COMMITTER_DATE"] = init_str
    run("git add -A")
    subprocess.run(
        f'git commit -m "init" --author="{USER_NAME} <{USER_EMAIL}>" --date="{init_str}"',
        shell=True, env=env0, text=True, capture_output=True
    )
    print(f"\n[✔] {init_str[:10]}  \"init\"  (all files added)")

    # ── build activity calendar ──────────────────────────────────────
    # Shade levels (GitHub colors based on commit count per day):
    #   1-3   → light green  (level 1-2)
    #   4-6   → medium green (level 3)
    #   7-9   → dark green   (level 4)
    #   10+   → darkest      (level 4 max)
    #
    # We pick ~30-35 active days across the 89 remaining days.

    # Day buckets: (day_offset_from_now, num_commits)
    active_days = []

    # Sprinkle ~5 "dark" days (8-14 commits) — looks like crunch sessions
    dark_days = random.sample(range(2, 88), 5)
    for d in dark_days:
        active_days.append((d, random.randint(8, 14)))

    # ~10 "medium" days (4-6 commits)
    available = [d for d in range(2, 88) if d not in [x[0] for x in active_days]]
    medium_days = random.sample(available, 10)
    for d in medium_days:
        active_days.append((d, random.randint(4, 6)))

    # ~18 "light" days (1-2 commits)
    available = [d for d in range(2, 88) if d not in [x[0] for x in active_days]]
    light_days = random.sample(available, 18)
    for d in light_days:
        active_days.append((d, random.randint(1, 2)))

    # Sort by day descending (oldest first)
    active_days.sort(key=lambda x: x[0], reverse=True)

    total_commits = sum(c for _, c in active_days)
    print(f"\n[*] {len(active_days)} active days | ~{total_commits} total commits planned")
    print(f"    Dark days (8-14):   {len(dark_days)}")
    print(f"    Medium days (4-6):  {len(medium_days)}")
    print(f"    Light days (1-2):   {len(light_days)}\n")

    last_msg = None
    file_cycle = EDITABLE_FILES * 20   # enough to cycle through
    file_idx   = 0

    for day_offset, num_commits in active_days:
        # Spread commits within the day at realistic times (9am-11pm)
        base = now - timedelta(days=day_offset)
        base = base.replace(hour=0, minute=0, second=0, microsecond=0)

        # Generate num_commits random times in the day
        minutes_in_day = list(range(9*60, 23*60))
        chosen_minutes = sorted(random.sample(minutes_in_day, min(num_commits, len(minutes_in_day))))

        for minute in chosen_minutes:
            h = minute // 60
            m = minute % 60
            s = random.randint(0, 59)
            dt = base + timedelta(hours=h, minutes=m, seconds=s)

            msg = random_msg(last_msg)
            last_msg = msg

            filepath = file_cycle[file_idx % len(file_cycle)]
            file_idx += 1

            commit_at(msg, dt, filepath)

    # ── push ─────────────────────────────────────────────────────────
    run(f"git branch -M {BRANCH}")
    r = run("git remote get-url origin")
    if r.returncode == 0:
        run(f"git remote set-url origin {REPO_URL}")
    else:
        run(f"git remote add origin {REPO_URL}")

    print(f"\n[*] Force pushing to GitHub ({BRANCH})...")
    push = subprocess.run(f"git push -u origin {BRANCH} --force", shell=True, text=True, capture_output=True)
    if push.returncode == 0:
        print("\n" + "=" * 65)
        print(" [SUCCESS] 3-month commit graph uploaded with varied shades!")
        print(f" Commits : https://github.com/tejas122125/example/commits/{BRANCH}")
        print(f" Profile : https://github.com/tejas122125")
        print("=" * 65)
    else:
        print(f"\n[ERROR] Push failed:\n{push.stderr.strip()}", file=sys.stderr)

if __name__ == "__main__":
    main()
