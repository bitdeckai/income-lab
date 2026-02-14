#!/usr/bin/env python3
import csv
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.github.com/search/issues?q={query}&sort=updated&order=desc&per_page=30"

QUERIES = [
    'is:issue is:open label:bounty android in:title,body',
    'is:issue is:open label:bounty esp32 in:title,body',
    'is:issue is:open label:bounty firmware in:title,body',
    'is:issue is:open label:bounty iot in:title,body',
    'is:issue is:open label:bounty "good-first-issue"',
]

KEYWORDS_HIGH_VALUE = ["android", "esp32", "matter", "zephyr", "firmware", "ble", "iot"]
MONEY_RE = re.compile(r"\$(\d+)", re.IGNORECASE)
POINT_RE = re.compile(r"points[:\s]*(\d+)", re.IGNORECASE)


def fetch(query: str):
    url = API.format(query=quote(query, safe=""))
    req = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "income-lab-bounty-bot"})
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("items", [])


def parse_dt(s: str):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def estimate_reward(title: str, body: str, labels):
    text = f"{title}\n{body or ''}"
    money = MONEY_RE.findall(text)
    points = POINT_RE.findall(text)
    label_names = [l.get("name", "") for l in labels]
    if money:
        return f"${max(int(x) for x in money)}"
    for name in label_names:
        m = re.search(r"points[:\-]?(\d+)", name, flags=re.IGNORECASE)
        if m:
            return f"points:{m.group(1)}"
    if points:
        return f"points:{max(int(x) for x in points)}"
    if any("bounty-medium" in n.lower() for n in label_names):
        return "bounty-medium"
    return "unknown"


def score(item):
    s = 0
    title = item.get("title", "").lower()
    body = (item.get("body") or "").lower()
    labels = [l.get("name", "").lower() for l in item.get("labels", [])]

    if any(k in title or k in body for k in KEYWORDS_HIGH_VALUE):
        s += 3

    updated = parse_dt(item["updated_at"])
    days = (datetime.now(timezone.utc) - updated).days
    if days <= 7:
        s += 3
    elif days <= 30:
        s += 2
    elif days <= 90:
        s += 1

    if "good-first-issue" in labels:
        s += 1

    if item.get("assignee") is not None:
        s -= 3

    if "help wanted" in labels:
        s += 1

    return s


def dedupe(items):
    out = {}
    for it in items:
        out[it["html_url"]] = it
    return list(out.values())


def main():
    all_items = []
    for q in QUERIES:
        try:
            all_items.extend(fetch(q))
        except Exception as e:
            print(f"warn: query failed: {q} => {e}", file=sys.stderr)

    items = dedupe(all_items)
    enriched = []
    for it in items:
        enriched.append({
            "repo": it["repository_url"].split("/repos/")[-1],
            "title": it["title"],
            "url": it["html_url"],
            "created_at": it["created_at"],
            "updated_at": it["updated_at"],
            "labels": ",".join(l.get("name", "") for l in it.get("labels", [])),
            "reward_hint": estimate_reward(it["title"], it.get("body") or "", it.get("labels", [])),
            "score": score(it),
            "assignee": (it.get("assignee") or {}).get("login", ""),
        })

    enriched.sort(key=lambda x: (x["score"], x["updated_at"]), reverse=True)
    top = enriched[:25]

    csv_path = "docs/bounty/live-opportunities.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["score", "reward_hint", "repo", "title", "url", "updated_at", "labels", "assignee"])
        w.writeheader()
        for row in top:
            w.writerow({k: row.get(k, "") for k in ["score", "reward_hint", "repo", "title", "url", "updated_at", "labels", "assignee"]})

    md_path = "docs/bounty/live-opportunities.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Live Bounty Opportunities",
        "",
        f"Generated: {now}",
        "",
        "Ranking logic: recency + embedded/android relevance + claimability.",
        "",
        "| Score | Reward Hint | Repo | Title | Updated |",
        "|---:|---|---|---|---|",
    ]
    for x in top[:15]:
        title = x["title"].replace("|", " ")
        repo = x["repo"].replace("|", " ")
        lines.append(f"| {x['score']} | {x['reward_hint']} | `{repo}` | [{title}]({x['url']}) | {x['updated_at'][:10]} |")

    lines.extend([
        "",
        "## Fast Execution Steps",
        "1. Pick one unassigned issue with score >= 4.",
        "2. Comment to claim and propose ETA.",
        "3. Open PR with tests and short demo/proof.",
        "4. Address review comments quickly.",
        "5. After merge, request bounty payout according to project rules.",
    ])

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"wrote {csv_path} and {md_path} with {len(top)} entries")


if __name__ == "__main__":
    main()

