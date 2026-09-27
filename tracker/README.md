# Personal Recruiting Tracker — Class of 2029

A private layer on top of the forked Pitt CSC × Simplify list. Nothing here modifies
upstream files, so `git pull upstream dev` stays clean.

## Why this folder exists

The upstream list is a **tech** list: SWE, PM, Data Science/AI, Quant Finance, Hardware.
Target lanes here are consulting, wealth management, crypto exchanges, PE, and CRE —
only the Quantitative Finance section overlaps, and only partly. Upstream is a *feed*,
not the source of truth.

## Contents

| File | What it is | How it's maintained |
|---|---|---|
| `Programs-and-Workshops-Tracker.xlsx` | Pipeline programs, insight days, fellowships, networking orgs | **Automated** — deadlines refreshed on a schedule |
| `Internship-Application-Tracker.xlsx` | Paid internships / summer analyst seats only | **Manual** — status, dates, rejection reasons are yours to log |
| `Pipeline-Programs-Class-of-2029.md` | The strategy behind the programs sheet | Manual |
| `Internship-Application-Tracker.md` | The strategy behind the internships sheet | Manual |
| `scan.py` | Filters upstream README → NY/NJ, non-grad-gated roles | Run on a schedule |
| `feed.csv` | Output of `scan.py` | Regenerated |

## The split — do not merge these two sheets

They run on different calendars and different eligibility logic.

- **Programs** gate on a **graduation-date band** (`Dec 2028 – June 2029`, `Class of 2029`).
  Expected graduation is Fall 2028 or Spring 2029 — **both land inside that band**, so
  eligibility holds either way.
- **Internships** gate on **cycle** (Summer 2027 vs the decisive Summer 2028).

⚠️ Some programs gate on enrolled **class standing**, not grad date — Capital One AEIP
("must be in Sophomore Undergraduate Standing"), Citi Freshman Discovery ("first-year").
Those are **not eligible**. Report standing truthfully; offers run enrollment verification.

## Usage

```bash
python3 tracker/scan.py                 # quant finance only (default)
python3 tracker/scan.py --all-sections  # + data science and PM
```

## Staying synced with upstream

```bash
git remote add upstream https://github.com/SimplifyJobs/Summer2027-Internships.git
git fetch upstream && git merge upstream/dev
```
