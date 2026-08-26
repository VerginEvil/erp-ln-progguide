#!/usr/bin/env python3
"""Token-efficient full-text search over the ERP LN Programmer's Guide skill.

Usage:
  python search.py <terms...> [--dir guide|sql|extensions|public_interfaces|all] [--max N]
                   [--group NAME] [--regex PATTERN] [--list-groups]

Examples:
  python search.py seq.open
  python search.py date.add --group functions_date
  python search.py "ref" "enum" --max 10
"""
import argparse
import os
import re
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(SKILL, "references")
MAX_OUTPUT_CHARS = 12000


def iter_md(scope):
    base = REFS if scope == "all" else os.path.join(REFS, scope)
    for dirpath, dirs, names in os.walk(base):
        dirs.sort()
        for n in sorted(names):
            if n.endswith(".md"):
                yield os.path.join(dirpath, n)


def relpath(p):
    return os.path.relpath(p, SKILL).replace("\\", "/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("terms", nargs="*", help="space-separated terms (AND, case-insensitive)")
    ap.add_argument("--dir", default="all",
                    choices=["guide", "sql", "extensions", "public_interfaces", "all"])
    ap.add_argument("--max", type=int, default=25, help="max matching files shown (default 25)")
    ap.add_argument("--group", default=None, help="only paths containing this substring")
    ap.add_argument("--regex", default=None, help="treat pattern as regex instead of terms")
    ap.add_argument("--list-groups", action="store_true", help="list topic folders with file counts")
    args = ap.parse_args()

    if args.list_groups:
        counts = {}
        for p in iter_md(args.dir if args.dir != "all" else "guide"):
            parts = relpath(p).split("/")
            if len(parts) >= 5:
                key = "/".join(parts[2:4])
            elif len(parts) >= 3:
                key = "/".join(parts[2:-1]) or parts[-1]
            else:
                continue
            counts[key] = counts.get(key, 0) + 1
        for k in sorted(counts):
            print("%4d  %s" % (counts[k], k))
        return

    if not args.terms and not args.regex:
        ap.error("provide terms or --regex")

    if args.regex:
        try:
            rx = re.compile(args.regex, re.I)
        except re.error as e:
            sys.exit("bad regex: %s" % e)
        match_line = lambda ln: rx.search(ln)
    else:
        terms = [t.lower() for t in args.terms]
        match_line = lambda ln: all(t in ln.lower() for t in terms)

    scored = []
    for path in iter_md(args.dir):
        rp = relpath(path)
        if args.group and args.group.lower() not in rp.lower():
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                lines = fh.read().splitlines()
        except OSError:
            continue
        hits = []
        for i, ln in enumerate(lines, 1):
            if match_line(ln):
                hits.append((i, ln.strip()))
        if hits:
            title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("#") else ""
            score = sum(1 for _ in hits)
            scored.append((score, len(rp), rp, title, hits))

    scored.sort(key=lambda t: (-t[0], t[1]))
    out = []
    shown = 0
    total_hits = 0
    for score, _rlen, rp, title, hits in scored:
        if shown >= args.max or sum(len(o) for o in out) > MAX_OUTPUT_CHARS:
            break
        shown += 1
        total_hits += len(hits)
        head = "%s | %s" % (rp, title) if title else rp
        out.append(head)
        for lineno, text in hits[:6]:
            snippet = text if len(text) <= 160 else text[:157] + "..."
            out.append("  %d: %s" % (lineno, snippet))
        if len(hits) > 6:
            out.append("  ... +%d more lines" % (len(hits) - 6))
    print("\n".join(out))
    if len(scored) > shown:
        print("(%d more files matched; refine terms or raise --max)" % (len(scored) - shown))


if __name__ == "__main__":
    main()
