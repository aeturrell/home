"""Refresh GitHub star/fork counts and last-updated month in teaching/learning.yml.

Runs as a Quarto pre-render step. For each entry with a `repo:` line, the
`stars:`, `forks:` and `updated:` lines in the same entry are rewritten from
the GitHub API. Any failure (offline, rate limit) leaves the file untouched,
so the last known values are kept. Set GITHUB_TOKEN to avoid rate limits.
"""

import json
import os
import re
import urllib.request
from datetime import datetime
from pathlib import Path

YAML_PATH = Path(__file__).resolve().parent.parent / "teaching" / "learning.yml"


def fetch(repo: str) -> dict | None:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repo}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "quarto-site-build"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.load(response)
    except Exception as error:  # noqa: BLE001 - never fail the build over stats
        print(f"github_stats: could not fetch {repo} ({error}); keeping old values")
        return None


def update_entry(entry: str) -> str:
    match = re.search(r"^\s*repo:\s*(\S+)\s*$", entry, flags=re.MULTILINE)
    if not match:
        return entry
    data = fetch(match.group(1))
    if not data:
        return entry
    pushed = datetime.strptime(data["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
    values = {
        "stars": str(data["stargazers_count"]),
        "forks": str(data["forks_count"]),
        "updated": pushed.strftime("%b %Y"),
    }
    for key, value in values.items():
        entry = re.sub(
            rf"^(\s*{key}:\s*).*$", rf"\g<1>{value}", entry, count=1, flags=re.MULTILINE
        )
    return entry


def main() -> None:
    text = YAML_PATH.read_text(encoding="utf-8")
    # Split on top-level list items, keeping the "- " markers with each entry.
    entries = re.split(r"(?m)^(?=- )", text)
    updated = "".join(update_entry(entry) for entry in entries)
    if updated != text:
        YAML_PATH.write_text(updated, encoding="utf-8")
        print("github_stats: updated teaching/learning.yml")


if __name__ == "__main__":
    main()
