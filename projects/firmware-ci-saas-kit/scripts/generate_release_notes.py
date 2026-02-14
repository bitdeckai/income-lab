import os
import subprocess
from datetime import datetime, timezone


def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def main():
    latest_tag = os.environ.get("LATEST_TAG", "")
    range_ref = f"{latest_tag}..HEAD" if latest_tag else "HEAD"

    try:
        log = run(["git", "log", "--pretty=format:- %s (%h)", range_ref])
    except subprocess.CalledProcessError:
        log = "- Initial release"

    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    notes = [
        "## Release Summary",
        f"Generated: {dt}",
        "",
        "## Changes",
        log if log else "- No commits found",
        "",
        "## Artifacts",
        "- firmware.bin",
        "- bootloader.bin",
        "- partitions.bin",
    ]

    path = os.environ.get("OUT_PATH", "release_notes.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(notes) + "\n")


if __name__ == "__main__":
    main()
