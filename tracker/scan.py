#!/usr/bin/env python3
"""
Pull finance-relevant Summer 2027 roles out of the upstream Pitt CSC / Simplify
README and write a filtered CSV.

The upstream list is a TECH list. Only the Quantitative Finance section is
relevant here, and only partly. This script does not invent roles and does not
touch the upstream README.

Usage:  python3 tracker/scan.py [--all-sections] [--out tracker/feed.csv]
"""
import re, html, csv, argparse, os, datetime

SECTIONS = {
    "quant":    ("## 📈 Quantitative Finance Internship Roles", "## 🔧 Hardware"),
    "ds":       ("## 🤖 Data Science, AI & Machine Learning Internship Roles", "## 📈 Quantitative Finance"),
    "pm":       ("## 📱 Product Management Internship Roles", "## 🤖 Data Science"),
}

# NY/NJ metro — commutable or realistic from Morris Plains / New Brunswick
GEO = ("NYC", "New York", "NJ", "Jersey", "Newark", "Stamford", "Greenwich", "Hoboken")

# roles that are NOT PhD/MFE-gated and plausibly open to an undergrad finance major
UNDERGRAD_OK = re.compile(
    r"summer analyst|business analyst|finance intern|investment|wealth|asset manage|"
    r"private (credit|equity|bank)|real estate|capital markets|strategy|operations|"
    r"sales|trading operations|risk|analyst intern", re.I)
GRAD_GATED = re.compile(r"master|mfe|phd|doctoral", re.I)


def parse_section(text, start, end):
    i = text.find(start)
    if i == -1:
        return []
    j = text.find(end, i)
    seg = text[i: j if j != -1 else len(text)]
    out, prev = [], None
    for r in re.findall(r"<tr>(.*?)</tr>", seg, re.S):
        tds = re.findall(r"<td>(.*?)</td>", r, re.S)
        if len(tds) < 5:
            continue
        clean = lambda s: html.unescape(re.sub("<[^>]+>", "", s)).strip()
        company, role, loc, age = clean(tds[0]), clean(tds[1]), clean(tds[2]), clean(tds[4])
        m = re.search(r'href="(https://(?!simplify|i\.imgur)[^"]+)"', tds[3])
        link = html.unescape(m.group(1)) if m else ""
        if company in ("↳", "") and prev:
            company = prev
        else:
            prev = company
        out.append(dict(company=company, role=role, location=loc, age=age, link=link))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-sections", action="store_true")
    ap.add_argument("--out", default="tracker/feed.csv")
    ap.add_argument("--readme", default="README.md")
    a = ap.parse_args()

    text = open(a.readme, encoding="utf-8").read()
    keys = SECTIONS.keys() if a.all_sections else ["quant"]
    rows = []
    for k in keys:
        rows += parse_section(text, *SECTIONS[k])

    kept = []
    for r in rows:
        if not any(g in r["location"] for g in GEO):
            continue
        if GRAD_GATED.search(r["role"]):
            continue
        r["undergrad_fit"] = "likely" if UNDERGRAD_OK.search(r["role"]) else "check"
        kept.append(r)

    kept.sort(key=lambda r: (r["undergrad_fit"] != "likely", r["company"]))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "role", "location", "age", "undergrad_fit", "link"])
        w.writeheader()
        w.writerows(kept)

    likely = sum(1 for r in kept if r["undergrad_fit"] == "likely")
    print(f"[{datetime.date.today()}] parsed {len(rows)} -> kept {len(kept)} NY/NJ "
          f"({likely} likely undergrad-fit) -> {a.out}")


if __name__ == "__main__":
    main()
