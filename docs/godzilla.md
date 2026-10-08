---
layout: default
title: "Godzilla and Monarch: Japan, USA, China and South Korea"
author: "Benjamin De Kosnik <bkoz@gnu.org>"
description: "Geographic and mobile-network comparison at matched sampling weeks"
---

{::nomarkdown}
<img src="../resources/a60-logo-block-gray.simple.svg?sanitize=true" height="50" width="100" alt="Alpha60">
<div style="height: 50px;"></div>
<link rel="stylesheet" href="../resources/izzi-table-wcag-22.css">
<link rel="stylesheet" href="../resources/mellon-7.6-analysis.css">
<script defer src="../resources/mellon-7.6-analysis.js"></script>
{:/}

[Asian American Media results](../index.html)

# Godzilla and Monarch: Japan, USA, China and South Korea

## Summary and conclusions

The sample now includes **three Godzilla films and Monarch 101, 110, 201 and
208**, using **weeks 1–15** throughout. Weekly downloader and uploader line
graphs use the **provisional 2026 Internet-user reference of 6.1 billion**.
That reference is a project estimate; historical denominators come from ITU.

- Minus One's Japanese downloader share is **1.42%**, compared with **1.12%**
  for The New Empire and **2.41%** for Vs. Kong. The four Monarch objects
  range from **0.76% to 1.25%**. Japanese production does not imply the
  highest Japanese share in this selection.
- Vs. Kong has the highest USA downloader share: **20.73%**, versus
  **7.80%** for Minus One and **6.84%** for The New Empire. Excluding hosting
  leaves **18.53% / 4.89% / 4.26%**, respectively. Hosting changes the gap
  but does not remove it. The compared films were sampled in 2021 and 2024.
- The 2026 Monarch objects have the largest South Korean and Chinese shares:
  **Monarch 201: 13.40% Korea / 10.05% China**;
  **Monarch 208: 14.48% Korea / 10.34% China**. Both countries exceed their
  USA shares (**7.13% / 6.83%**). These geographic concentrations coexist
  with low Korean mobile rates (**1.58% / 1.59%**).
- Only **weeks 6, 7, 8, 9 and 14** survive the strict all-seven coverage
  intersection. This sparse diagnostic cannot establish robustness of every
  fifteen-week difference. Missing collection hours are not imputed.

The new Monarch objects include one- and three-episode scopes; the original
objects are films. ITU scaling adjusts the global Internet-user reference, not
episodes per object, country penetration, collection gaps or torrent inventories.
The results describe observed swarms and do not estimate viewers' nationality
or a causal production-country effect.

## Objects and observation windows

The selection combines three Godzilla films and four Monarch objects. Monarch 101 and 201 each contain three episodes (101–103 and 201–203); 110 is one episode, and 208 contains episodes 208–210. Film, episode and episode-group scopes differ. These cases cannot isolate a production-country effect from year, title, inventory or distribution. “Korea” means South Korea (KOR); North Korea is not pooled into that result.

| Object / key | Full available sample | Analyzed weeks 1–15 | Worldwide downloader weight | Worldwide uploader weight |
| --- | --- | --- | --- | --- |
| Godzilla Minus One / `godzilla-minus-one` | 2024-05-02-to-2024-10-30 | 2024-05-02 to 2024-08-14 | 35,409,706 | 3,732,188 |
| Godzilla x Kong / `godzilla-x-kong-the-new-empire` | 2024-05-14-to-2024-11-11 | 2024-05-14 to 2024-08-26 | 49,834,220 | 7,772,066 |
| Godzilla vs. Kong / `godzilla-vs-kong` | 2021-03-31-to-2021-09-28 | 2021-03-31 to 2021-07-13 | 55,096,020 | 12,588,462 |
| Monarch 101 / `monarch-legacy-of-monsters-101` | 2023-11-17-to-2024-05-17 | 2023-11-17 to 2024-02-29 | 15,878,429 | 2,707,202 |
| Monarch 110 / `monarch-legacy-of-monsters-110` | 2024-01-12-to-2024-06-06 | 2024-01-12 to 2024-04-25 | 11,985,666 | 763,219 |
| Monarch 201 / `monarch-legacy-of-monsters-201` | 2026-02-27-to-2026-09-10 | 2026-02-27 to 2026-06-11 | 40,814,557 | 2,384,859 |
| Monarch 208 / `monarch-legacy-of-monsters-208` | 2026-04-17-to-2026-09-10 | 2026-04-17 to 2026-07-30 | 46,361,961 | 1,877,578 |


### Sampling coverage

- **Godzilla Minus One:** Hourly discontinuities: 1 (18 missing hours); Missing days: 0; hourly gap: last `2024-07-10 05:03`, resumed `2024-07-11 00:03` — missing 18 hour(s)
- **Godzilla x Kong:** Hourly discontinuities: 0 (0 missing hours); Missing days: 0
- **Godzilla vs. Kong:** missing Day index 113: `2021-07-21`
- **Monarch 101:** Hourly discontinuities: 2 (25 missing hours); Missing days: 1; hourly gap: last `2024-02-01 23:00`, resumed `2024-02-03 00:00` — missing 24 hour(s); hourly gap: last `2024-03-31 01:00`, resumed `2024-03-31 03:00` — missing 1 hour(s); missing day: `2024-02-02`
- **Monarch 110:** Hourly discontinuities: 3 (41 missing hours); Missing days: 0; hourly gap: last `2024-03-31 01:06`, resumed `2024-03-31 03:06` — missing 1 hour(s); hourly gap: last `2024-04-20 06:06`, resumed `2024-04-21 00:06` — missing 17 hour(s); hourly gap: last `2024-04-21 00:06`, resumed `2024-04-22 00:06` — missing 23 hour(s)
- **Monarch 201:** Hourly discontinuities: 3 (28 missing hours); Missing days: 1; hourly gap: last `2026-03-29 01:02`, resumed `2026-03-29 03:02` — missing 1 hour(s); hourly gap: last `2026-05-27 22:02`, resumed `2026-05-28 00:14` — missing 1 hour(s); hourly gap: last `2026-07-03 22:02`, resumed `2026-07-05 01:02` — missing 26 hour(s); missing day: `2026-07-04`
- **Monarch 208:** Hourly discontinuities: 2 (67 missing hours); Missing days: 1; hourly gap: last `2026-06-25 23:06`, resumed `2026-06-27 17:06` — missing 41 hour(s); hourly gap: last `2026-08-12 03:06`, resumed `2026-08-13 06:06` — missing 26 hour(s); missing day: `2026-06-26`

These are full-sample audit notes. Only dates overlapping the selected intervals enter the coverage sensitivity below. Opening bins are retained. Missing hours are not imputed.

## ITU adjustment to 2026 — provisional reference

**The 6.1-billion reference for 2026 is the project's provisional estimate,
not an official ITU 2026 observation.** The latest official release checked
on September 24, 2026 covers 2025. This status applies to every adjusted
number and adjusted-count figure on this page.

`2026 adjusted weight = raw weight × 6.1 / source-year Internet users (billions)`.
The sample-start year selects the denominator. This scales global Internet-user
growth; it does not adjust country-specific penetration, sampling coverage,
episodes per object or torrent inventories. It is not an estimate of viewers.
Applying the same multiplier to all counts within an object leaves country
shares, mobile rates, hosting rates and share-difference maps unchanged.

The historical 2023 and 2024 denominators retain the project's as-published
vintages for comparability. ITU later revised 2024 from 5.5 to 5.8 billion;
the sensitivity below makes the effect explicit. No official 2026 precision
or confidence interval is implied.

| Object | Sample year | Internet users (billions) | 2026 factor | Raw world downloaders | 2026 adjusted world downloaders |
| --- | --- | --- | --- | --- | --- |
| Godzilla Minus One | 2024 | 5.5 | 1.109091 | 35,409,706 | 39,272,583 |
| Godzilla x Kong | 2024 | 5.5 | 1.109091 | 49,834,220 | 55,270,680 |
| Godzilla vs. Kong | 2021 | 4.9 | 1.244898 | 55,096,020 | 68,588,923 |
| Monarch 101 | 2023 | 5.4 | 1.129630 | 15,878,429 | 17,936,744 |
| Monarch 110 | 2024 | 5.5 | 1.109091 | 11,985,666 | 13,293,193 |
| Monarch 201 | 2026 | 6.1 | 1.000000 | 40,814,557 | 40,814,557 |
| Monarch 208 | 2026 | 6.1 | 1.000000 | 46,361,961 | 46,361,961 |


### Country counts at the 2026 scale, weeks 1–15

Adjusted values are rounded only for display. Raw counts and unrounded calculations are retained in the ledger.

| Country | Object | Raw downloaders | 2026 adjusted downloaders | 2026 adjusted mobile downloaders | Raw uploaders | 2026 adjusted uploaders |
| --- | --- | --- | --- | --- | --- | --- |
| Japan | Godzilla Minus One | 502,472 | 557,287 | 145,310 | 23,031 | 25,543 |
| Japan | Godzilla x Kong | 556,252 | 616,934 | 162,016 | 21,040 | 23,335 |
| Japan | Godzilla vs. Kong | 1,327,945 | 1,653,156 | 206,669 | 47,990 | 59,743 |
| Japan | Monarch 101 | 121,464 | 137,209 | 32,654 | 10,322 | 11,660 |
| Japan | Monarch 110 | 136,004 | 150,841 | 38,580 | 2,353 | 2,610 |
| Japan | Monarch 201 | 511,511 | 511,511 | 130,974 | 8,885 | 8,885 |
| Japan | Monarch 208 | 580,962 | 580,962 | 148,350 | 7,387 | 7,387 |
| USA | Godzilla Minus One | 2,761,311 | 3,062,545 | 99,759 | 437,018 | 484,693 |
| USA | Godzilla x Kong | 3,407,707 | 3,779,457 | 231,854 | 623,305 | 691,302 |
| USA | Godzilla vs. Kong | 11,423,028 | 14,220,504 | 408,934 | 835,697 | 1,040,357 |
| USA | Monarch 101 | 1,451,823 | 1,640,022 | 81,756 | 353,553 | 399,384 |
| USA | Monarch 110 | 849,565 | 942,245 | 25,431 | 80,115 | 88,855 |
| USA | Monarch 201 | 2,908,451 | 2,908,451 | 91,626 | 426,292 | 426,292 |
| USA | Monarch 208 | 3,166,199 | 3,166,199 | 88,739 | 390,175 | 390,175 |
| China | Godzilla Minus One | 1,783,148 | 1,977,673 | 47,001 | 111,127 | 123,250 |
| China | Godzilla x Kong | 2,090,740 | 2,318,821 | 49,673 | 146,329 | 162,292 |
| China | Godzilla vs. Kong | 3,086,478 | 3,842,350 | 93,504 | 264,659 | 329,473 |
| China | Monarch 101 | 701,557 | 792,500 | 17,597 | 136,043 | 153,678 |
| China | Monarch 110 | 522,485 | 579,483 | 9,489 | 24,208 | 26,849 |
| China | Monarch 201 | 4,100,297 | 4,100,297 | 40,828 | 238,177 | 238,177 |
| China | Monarch 208 | 4,791,803 | 4,791,803 | 46,192 | 274,875 | 274,875 |
| South Korea | Godzilla Minus One | 3,080,576 | 3,416,639 | 63,103 | 28,089 | 31,153 |
| South Korea | Godzilla x Kong | 3,625,988 | 4,021,550 | 97,568 | 73,255 | 81,246 |
| South Korea | Godzilla vs. Kong | 1,312,313 | 1,633,696 | 92,109 | 313,122 | 389,805 |
| South Korea | Monarch 101 | 701,468 | 792,399 | 15,026 | 17,165 | 19,390 |
| South Korea | Monarch 110 | 884,654 | 981,162 | 16,525 | 6,176 | 6,850 |
| South Korea | Monarch 201 | 5,467,928 | 5,467,928 | 86,288 | 12,756 | 12,756 |
| South Korea | Monarch 208 | 6,715,166 | 6,715,166 | 106,759 | 8,509 | 8,509 |


### Revised 2024 denominator sensitivity

Using the later 5.8-billion estimate changes every 2024 object’s multiplier from 1.109091 to 1.051724, lowering its adjusted weights by 5.17%. Country shares and mobile rates are unchanged. This replaces only the 2024 denominator; it is not a fully revised historical ITU series.

| Country | 2024 object | Adjusted with 5.5b | Adjusted with revised 5.8b |
| --- | --- | --- | --- |
| Japan | Godzilla Minus One | 557,287 | 528,462 |
| USA | Godzilla Minus One | 3,062,545 | 2,904,137 |
| China | Godzilla Minus One | 1,977,673 | 1,875,380 |
| South Korea | Godzilla Minus One | 3,416,639 | 3,239,916 |
| Japan | Godzilla x Kong | 616,934 | 585,024 |
| USA | Godzilla x Kong | 3,779,457 | 3,583,968 |
| China | Godzilla x Kong | 2,318,821 | 2,198,882 |
| South Korea | Godzilla x Kong | 4,021,550 | 3,813,539 |
| Japan | Monarch 110 | 150,841 | 143,039 |
| USA | Monarch 110 | 942,245 | 893,508 |
| China | Monarch 110 | 579,483 | 549,510 |
| South Korea | Monarch 110 | 981,162 | 930,412 |


Sources: [ITU 2021](https://www.itu.int/itu-d/reports/statistics/facts-figures-2021/), [ITU 2023](https://www.itu.int/en/mediacentre/Pages/PR-2023-11-27-facts-and-figures-measuring-digital-development.aspx), [ITU 2024](https://www.itu.int/en/mediacentre/Pages/PR-2024-11-27-facts-and-figures.aspx), [ITU 2025 and revised 2024](https://www.itu.int/en/mediacentre/Pages/PR-2025-11-17-Facts-and-Figures.aspx), [latest publication index](https://www.itu.int/en/ITU-D/Statistics/Pages/facts/default.aspx), and [versioned calculation policy](../data/mellon-7.6-itu-2026.json).

{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.6-godzilla-world-weekly-itu-2026.svg %}
<figcaption>Standard Izzi C++ weekly graphs with media-object names directly on their lines. Worldwide weekly downloaders and uploaders, weeks 1–15, scaled to the provisional 6.1-billion 2026 reference. The two role panels use different vertical scales. Raw interval values are retained in the ledger. <a href="../resources/mellon-7.6-godzilla-world-weekly-itu-2026.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{:/}


### Coverage sensitivity

As a conservative check, exclude every elapsed-week index that has a `-partial` export flag or overlaps an audit-reported gap in **any** compared object, from **all** objects. Partial flags can reflect member-level coverage and are not an estimate of missing hours. Retained week indices: **6, 7, 8, 9, 14**. The table compares downloader world shares; it does not impute missing observations.

| Country | Object | Weeks 1–15 share | Retained-weeks share |
| --- | --- | --- | --- |
| Japan | Godzilla Minus One | 1.42% | 1.35% |
| Japan | Godzilla x Kong | 1.12% | 1.14% |
| Japan | Godzilla vs. Kong | 2.41% | 3.16% |
| Japan | Monarch 101 | 0.76% | 0.77% |
| Japan | Monarch 110 | 1.13% | 1.31% |
| Japan | Monarch 201 | 1.25% | 1.25% |
| Japan | Monarch 208 | 1.25% | 1.25% |
| USA | Godzilla Minus One | 7.80% | 7.63% |
| USA | Godzilla x Kong | 6.84% | 6.84% |
| USA | Godzilla vs. Kong | 20.73% | 25.87% |
| USA | Monarch 101 | 9.14% | 8.86% |
| USA | Monarch 110 | 7.09% | 6.67% |
| USA | Monarch 201 | 7.13% | 6.77% |
| USA | Monarch 208 | 6.83% | 6.56% |
| China | Godzilla Minus One | 5.04% | 4.67% |
| China | Godzilla x Kong | 4.20% | 3.98% |
| China | Godzilla vs. Kong | 5.60% | 6.05% |
| China | Monarch 101 | 4.42% | 3.63% |
| China | Monarch 110 | 4.36% | 4.75% |
| China | Monarch 201 | 10.05% | 10.09% |
| China | Monarch 208 | 10.34% | 9.90% |
| South Korea | Godzilla Minus One | 8.70% | 8.35% |
| South Korea | Godzilla x Kong | 7.28% | 7.34% |
| South Korea | Godzilla vs. Kong | 2.38% | 2.31% |
| South Korea | Monarch 101 | 4.42% | 4.47% |
| South Korea | Monarch 110 | 7.38% | 8.72% |
| South Korea | Monarch 201 | 13.40% | 13.09% |
| South Korea | Monarch 208 | 14.48% | 14.66% |

This leaves 5 of 15 intervals. It is a sparse coverage diagnostic; missing observations are not estimated.

## Country distribution and network composition

Counts below are summed weekly swarm weights. Geographic shares use the worldwide role total; flag rates use the country role total.
### Downloaders

| Country | Object | Weight | World share | Mobile rate | Hosting rate | VPN rate | World share excluding hosting |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Japan | Godzilla Minus One | 502,472 | 1.42% | 26.07% | 13.36% | 8.35% | 1.46% |
| Japan | Godzilla x Kong | 556,252 | 1.12% | 26.26% | 12.66% | 7.51% | 1.13% |
| Japan | Godzilla vs. Kong | 1,327,945 | 2.41% | 12.50% | 7.88% | 1.12% | 2.49% |
| Japan | Monarch 101 | 121,464 | 0.76% | 23.80% | 18.04% | 12.33% | 0.75% |
| Japan | Monarch 110 | 136,004 | 1.13% | 25.58% | 10.99% | 6.69% | 1.18% |
| Japan | Monarch 201 | 511,511 | 1.25% | 25.61% | 15.73% | 10.97% | 1.27% |
| Japan | Monarch 208 | 580,962 | 1.25% | 25.54% | 14.80% | 10.25% | 1.28% |
| USA | Godzilla Minus One | 2,761,311 | 7.80% | 3.26% | 47.22% | 22.85% | 4.89% |
| USA | Godzilla x Kong | 3,407,707 | 6.84% | 6.13% | 46.11% | 20.19% | 4.26% |
| USA | Godzilla vs. Kong | 11,423,028 | 20.73% | 2.88% | 20.29% | 3.14% | 18.53% |
| USA | Monarch 101 | 1,451,823 | 9.14% | 4.99% | 53.92% | 30.65% | 5.03% |
| USA | Monarch 110 | 849,565 | 7.09% | 2.70% | 45.92% | 24.03% | 4.48% |
| USA | Monarch 201 | 2,908,451 | 7.13% | 3.15% | 53.22% | 32.17% | 4.02% |
| USA | Monarch 208 | 3,166,199 | 6.83% | 2.80% | 50.46% | 27.42% | 4.06% |
| China | Godzilla Minus One | 1,783,148 | 5.04% | 2.38% | 5.31% | 1.30% | 5.67% |
| China | Godzilla x Kong | 2,090,740 | 4.20% | 2.14% | 5.21% | 1.30% | 4.60% |
| China | Godzilla vs. Kong | 3,086,478 | 5.60% | 2.43% | 5.97% | 0.57% | 5.91% |
| China | Monarch 101 | 701,557 | 4.42% | 2.22% | 4.75% | 1.00% | 5.03% |
| China | Monarch 110 | 522,485 | 4.36% | 1.64% | 5.05% | 1.24% | 4.83% |
| China | Monarch 201 | 4,100,297 | 10.05% | 1.00% | 5.11% | 2.66% | 11.49% |
| China | Monarch 208 | 4,791,803 | 10.34% | 0.96% | 5.08% | 2.31% | 11.79% |
| South Korea | Godzilla Minus One | 3,080,576 | 8.70% | 1.85% | 2.90% | 1.28% | 10.04% |
| South Korea | Godzilla x Kong | 3,625,988 | 7.28% | 2.43% | 2.85% | 1.25% | 8.17% |
| South Korea | Godzilla vs. Kong | 1,312,313 | 2.38% | 5.64% | 4.68% | 0.54% | 2.55% |
| South Korea | Monarch 101 | 701,468 | 4.42% | 1.90% | 3.18% | 1.15% | 5.11% |
| South Korea | Monarch 110 | 884,654 | 7.38% | 1.68% | 2.95% | 1.16% | 8.36% |
| South Korea | Monarch 201 | 5,467,928 | 13.40% | 1.58% | 2.20% | 1.50% | 15.79% |
| South Korea | Monarch 208 | 6,715,166 | 14.48% | 1.59% | 2.22% | 1.50% | 17.02% |

### Uploaders

| Country | Object | Weight | World share | Mobile rate | Hosting rate | VPN rate | World share excluding hosting |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Japan | Godzilla Minus One | 23,031 | 0.62% | 24.89% | 35.78% | 25.58% | 0.50% |
| Japan | Godzilla x Kong | 21,040 | 0.27% | 26.67% | 32.44% | 19.77% | 0.21% |
| Japan | Godzilla vs. Kong | 47,990 | 0.38% | 20.84% | 17.22% | 7.59% | 0.34% |
| Japan | Monarch 101 | 10,322 | 0.38% | 21.94% | 39.37% | 28.95% | 0.30% |
| Japan | Monarch 110 | 2,353 | 0.31% | 21.59% | 36.55% | 31.15% | 0.25% |
| Japan | Monarch 201 | 8,885 | 0.37% | 15.66% | 60.08% | 49.04% | 0.23% |
| Japan | Monarch 208 | 7,387 | 0.39% | 11.66% | 66.08% | 53.53% | 0.21% |
| USA | Godzilla Minus One | 437,018 | 11.71% | 4.78% | 67.14% | 36.61% | 4.81% |
| USA | Godzilla x Kong | 623,305 | 8.02% | 8.33% | 62.10% | 26.83% | 3.49% |
| USA | Godzilla vs. Kong | 835,697 | 6.64% | 6.46% | 35.52% | 11.39% | 4.63% |
| USA | Monarch 101 | 353,553 | 13.06% | 5.38% | 64.98% | 36.72% | 5.90% |
| USA | Monarch 110 | 80,115 | 10.50% | 4.96% | 58.49% | 41.66% | 5.56% |
| USA | Monarch 201 | 426,292 | 17.87% | 3.64% | 77.84% | 42.43% | 6.04% |
| USA | Monarch 208 | 390,175 | 20.78% | 2.98% | 80.59% | 36.81% | 6.35% |
| China | Godzilla Minus One | 111,127 | 2.98% | 6.86% | 5.69% | 0.63% | 3.51% |
| China | Godzilla x Kong | 146,329 | 1.88% | 5.10% | 4.61% | 0.80% | 2.06% |
| China | Godzilla vs. Kong | 264,659 | 2.10% | 2.62% | 1.89% | 0.78% | 2.23% |
| China | Monarch 101 | 136,043 | 5.03% | 2.84% | 3.25% | 0.71% | 6.27% |
| China | Monarch 110 | 24,208 | 3.17% | 2.32% | 4.68% | 0.84% | 3.86% |
| China | Monarch 201 | 238,177 | 9.99% | 1.13% | 0.59% | 1.16% | 15.13% |
| China | Monarch 208 | 274,875 | 14.64% | 1.33% | 0.67% | 1.14% | 22.91% |
| South Korea | Godzilla Minus One | 28,089 | 0.75% | 5.28% | 4.49% | 2.37% | 0.90% |
| South Korea | Godzilla x Kong | 73,255 | 0.94% | 8.51% | 2.45% | 1.21% | 1.06% |
| South Korea | Godzilla vs. Kong | 313,122 | 2.49% | 4.81% | 1.47% | 0.66% | 2.65% |
| South Korea | Monarch 101 | 17,165 | 0.63% | 4.63% | 6.85% | 1.78% | 0.76% |
| South Korea | Monarch 110 | 6,176 | 0.81% | 4.49% | 5.18% | 1.39% | 0.98% |
| South Korea | Monarch 201 | 12,756 | 0.53% | 5.37% | 5.27% | 5.62% | 0.77% |
| South Korea | Monarch 208 | 8,509 | 0.45% | 5.63% | 7.17% | 6.40% | 0.66% |


## Hot and cold locations

Orange upward triangles favor the first named object; blue downward triangles favor the second. These are selected differences in **city share of the worldwide swarm**, rather than differences in raw title size. Hover or focus a triangle for its values; the following table provides the same evidence.

{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.6-godzilla-map-1.svg %}
<figcaption>Selected shared city locations; weeks 1–15. Full counts and periods are in the calculation ledger. Land: Natural Earth via Cartofreako. <a href="../resources/mellon-7.6-godzilla-map-1.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{:/}


| Country / city | Godzilla Minus One weight | Godzilla x Kong weight | First world share | Second world share | Difference (pp) |
| --- | --- | --- | --- | --- | --- |
| Japan / Tokyo | 131,402 | 146,092 | 0.371% | 0.293% | +0.078 |
| Japan / Kawasaki | 17,393 | 3,222 | 0.049% | 0.006% | +0.043 |
| Japan / Yokohama | 26,232 | 45,114 | 0.074% | 0.091% | -0.016 |
| Japan / Ōta | 1,426 | 3,418 | 0.004% | 0.007% | -0.003 |
| USA / Los Angeles | 151,288 | 169,364 | 0.427% | 0.340% | +0.087 |
| USA / Seattle | 68,649 | 73,711 | 0.194% | 0.148% | +0.046 |
| USA / Newark | 17,585 | 43,949 | 0.050% | 0.088% | -0.039 |
| USA / Ashburn | 336,316 | 490,623 | 0.950% | 0.985% | -0.035 |
| China / Shanghai | 314,270 | 372,546 | 0.888% | 0.748% | +0.140 |
| China / Nanjing | 246,538 | 292,075 | 0.696% | 0.586% | +0.110 |
| China / Xiuying | 1,687 | 2,510 | 0.005% | 0.005% | -0.000 |
| China / Nanshan | 21 | 160 | 0.000% | 0.000% | -0.000 |
| South Korea / Seoul | 1,203,804 | 1,312,316 | 3.400% | 2.633% | +0.766 |
| South Korea / Incheon | 275,632 | 322,675 | 0.778% | 0.647% | +0.131 |
| South Korea / Gangseo-gu | 2,645 | 114,200 | 0.007% | 0.229% | -0.222 |
| South Korea / Seolcheon | 21 | 84 | 0.000% | 0.000% | -0.000 |

Among the selected shared locations, Seoul has the largest positive difference (+0.766 pp) and Gangseo-gu the smallest difference (-0.222 pp). These comparisons normalize by each object's worldwide swarm weight; they do not imply the same ordering of absolute counts.

{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.6-godzilla-map-2.svg %}
<figcaption>Selected shared city locations; weeks 1–15. Full counts and periods are in the calculation ledger. Land: Natural Earth via Cartofreako. <a href="../resources/mellon-7.6-godzilla-map-2.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{:/}


| Country / city | Godzilla Minus One weight | Godzilla vs. Kong weight | First world share | Second world share | Difference (pp) |
| --- | --- | --- | --- | --- | --- |
| Japan / Ōi | 14,592 | 4,507 | 0.041% | 0.008% | +0.033 |
| Japan / Kawasaki | 17,393 | 12,823 | 0.049% | 0.023% | +0.026 |
| Japan / Tokyo | 131,402 | 284,547 | 0.371% | 0.516% | -0.145 |
| Japan / Yokohama | 26,232 | 55,022 | 0.074% | 0.100% | -0.026 |
| USA / Miami | 72,523 | 80,848 | 0.205% | 0.147% | +0.058 |
| USA / Los Angeles | 151,288 | 207,755 | 0.427% | 0.377% | +0.050 |
| USA / Columbus | 42,666 | 872,576 | 0.120% | 1.584% | -1.463 |
| USA / Seattle | 68,649 | 567,452 | 0.194% | 1.030% | -0.836 |
| China / Nanjing | 246,538 | 176,756 | 0.696% | 0.321% | +0.375 |
| China / Qingdao | 190,018 | 104,789 | 0.537% | 0.190% | +0.346 |
| China / Shenzhen | 120,000 | 346,698 | 0.339% | 0.629% | -0.290 |
| China / Beijing | 113,865 | 337,072 | 0.322% | 0.612% | -0.290 |
| South Korea / Seoul | 1,203,804 | 673,425 | 3.400% | 1.222% | +2.177 |
| South Korea / Incheon | 275,632 | 112,160 | 0.778% | 0.204% | +0.575 |
| South Korea / Damyang | 110 | 731 | 0.000% | 0.001% | -0.001 |

Among the selected shared locations, Seoul has the largest positive difference (+2.177 pp) and Columbus the smallest difference (-1.463 pp). These comparisons normalize by each object's worldwide swarm weight; they do not imply the same ordering of absolute counts.

## Weekly behavior

Each line shows that week’s country share of worldwide downloader weight. All panels use the same vertical scale. Comparing shares separates geographic composition from changes in total observed swarm size.

{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.6-godzilla-weekly.svg %}
<figcaption>Standard Izzi C++ weekly graphs with media-object names directly on their lines. Seven-day interval shares, elapsed weeks 1–15; calendar dates differ by object. Missing sampling hours remain unadjusted. <a href="../resources/mellon-7.6-godzilla-weekly.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{:/}


{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.6-godzilla-weekly-itu-2026.svg %}
<figcaption>Standard Izzi C++ weekly graphs with media-object names directly on their lines. Downloaders swarm weights, weeks 1–15, at the provisional 2026 Internet-user scale (6.1 billion). Each object uses its sample-start-year factor; country-specific penetration and missing hours are not adjusted. <a href="../resources/mellon-7.6-godzilla-weekly-itu-2026.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{:/}


{::nomarkdown}
<figure class="analysis-figure">
{% include mellon-7.6-godzilla-weekly-itu-2026-uploaders.svg %}
<figcaption>Standard Izzi C++ weekly graphs with media-object names directly on their lines. Uploaders swarm weights, weeks 1–15, at the provisional 2026 Internet-user scale (6.1 billion). Each object uses its sample-start-year factor; country-specific penetration and missing hours are not adjusted. <a href="../resources/mellon-7.6-godzilla-weekly-itu-2026-uploaders.svg">Download SVG</a>.</figcaption>
<div class="map-tooltip" role="status" aria-live="polite" hidden></div>
</figure>
{:/}

Vs. Kong shows a pronounced USA change between weeks 4 and 5 (April 21–27 versus April 28–May 4, 2021): downloader weight rises from **224,155 to 1,210,927**, and world share from **7.54% to 24.41%**. Excluding hosting still leaves a rise from **5.81% to 22.33%**. The weekly aggregate does not establish whether this reflects torrent-inventory changes, collection behavior or demand; it should not be attributed to a release event or mobile adoption without further evidence.

- **Godzilla Minus One:** Japan peaks in week 13 (45,644); week 15 versus week 1 weight changes +89.0%, and mobile rate changes +0.85 pp; USA peaks in week 6 (222,765); week 15 versus week 1 weight changes +1.0%, and mobile rate changes -4.53 pp; China peaks in week 13 (173,094); week 15 versus week 1 weight changes +92.7%, and mobile rate changes -1.81 pp; South Korea peaks in week 13 (324,736); week 15 versus week 1 weight changes +242.7%, and mobile rate changes -1.89 pp.
- **Godzilla x Kong:** Japan peaks in week 11 (49,776); week 15 versus week 1 weight changes -14.1%, and mobile rate changes +0.38 pp; USA peaks in week 1 (333,801); week 15 versus week 1 weight changes -47.3%, and mobile rate changes -6.15 pp; China peaks in week 12 (187,856); week 15 versus week 1 weight changes -32.1%, and mobile rate changes -1.54 pp; South Korea peaks in week 11 (354,421); week 15 versus week 1 weight changes -3.3%, and mobile rate changes -3.66 pp.
- **Godzilla vs. Kong:** Japan peaks in week 7 (156,468); week 15 versus week 1 weight changes +223.7%, and mobile rate changes -5.44 pp; USA peaks in week 7 (1,270,827); week 15 versus week 1 weight changes +76.9%, and mobile rate changes -7.29 pp; China peaks in week 5 (324,717); week 15 versus week 1 weight changes -42.0%, and mobile rate changes -0.31 pp; South Korea peaks in week 1 (161,906); week 15 versus week 1 weight changes -59.5%, and mobile rate changes -2.65 pp.
- **Monarch 101:** Japan peaks in week 3 (10,942); week 15 versus week 1 weight changes +30.7%, and mobile rate changes +3.77 pp; USA peaks in week 1 (161,677); week 15 versus week 1 weight changes -57.1%, and mobile rate changes -7.06 pp; China peaks in week 1 (130,483); week 15 versus week 1 weight changes -68.3%, and mobile rate changes -1.65 pp; South Korea peaks in week 15 (68,462); week 15 versus week 1 weight changes +125.3%, and mobile rate changes -2.53 pp.
- **Monarch 110:** Japan peaks in week 11 (16,367); week 15 versus week 1 weight changes +16.5%, and mobile rate changes +2.32 pp; USA peaks in week 1 (87,549); week 15 versus week 1 weight changes -49.7%, and mobile rate changes -4.62 pp; China peaks in week 10 (58,622); week 15 versus week 1 weight changes -45.2%, and mobile rate changes +0.03 pp; South Korea peaks in week 10 (111,250); week 15 versus week 1 weight changes +40.2%, and mobile rate changes -0.65 pp.
- **Monarch 201:** Japan peaks in week 5 (48,823); week 15 versus week 1 weight changes +157.6%, and mobile rate changes +2.30 pp; USA peaks in week 3 (272,075); week 15 versus week 1 weight changes +31.8%, and mobile rate changes -4.45 pp; China peaks in week 5 (376,637); week 15 versus week 1 weight changes +154.2%, and mobile rate changes -0.77 pp; South Korea peaks in week 5 (505,872); week 15 versus week 1 weight changes +228.4%, and mobile rate changes -0.26 pp.
- **Monarch 208:** Japan peaks in week 10 (51,270); week 15 versus week 1 weight changes +280.0%, and mobile rate changes +2.48 pp; USA peaks in week 3 (262,797); week 15 versus week 1 weight changes +145.9%, and mobile rate changes -1.83 pp; China peaks in week 10 (406,621); week 15 versus week 1 weight changes +229.5%, and mobile rate changes -0.61 pp; South Korea peaks in week 10 (624,688); week 15 versus week 1 weight changes +378.8%, and mobile rate changes -0.08 pp.

These are descriptive peaks within the selected bins, not release-day peaks or evidence of a weekday effect. No daily or hourly behavioral claim is inferred from weekly data.

<details markdown="1"><summary>Weekly counts, mobile rates and calendar dates</summary>


| Object | Week / dates | World downloaders | Country | Country downloaders | World share | Mobile rate | 2026 adjusted country weight (provisional) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Godzilla Minus One | 1 / 2024-05-02-to-2024-05-08-partial | 2,006,997 | Japan | 20,755 | 1.03% | 25.23% | 23,019 |
| Godzilla Minus One | 1 / 2024-05-02-to-2024-05-08-partial | 2,006,997 | USA | 175,861 | 8.76% | 6.49% | 195,046 |
| Godzilla Minus One | 1 / 2024-05-02-to-2024-05-08-partial | 2,006,997 | China | 80,241 | 4.00% | 3.40% | 88,995 |
| Godzilla Minus One | 1 / 2024-05-02-to-2024-05-08-partial | 2,006,997 | South Korea | 78,657 | 3.92% | 3.70% | 87,238 |
| Godzilla Minus One | 2 / 2024-05-09-to-2024-05-15-partial | 2,282,575 | Japan | 25,913 | 1.14% | 25.30% | 28,740 |
| Godzilla Minus One | 2 / 2024-05-09-to-2024-05-15-partial | 2,282,575 | USA | 178,159 | 7.81% | 4.78% | 197,595 |
| Godzilla Minus One | 2 / 2024-05-09-to-2024-05-15-partial | 2,282,575 | China | 102,795 | 4.50% | 3.56% | 114,009 |
| Godzilla Minus One | 2 / 2024-05-09-to-2024-05-15-partial | 2,282,575 | South Korea | 124,807 | 5.47% | 2.19% | 138,422 |
| Godzilla Minus One | 3 / 2024-05-16-to-2024-05-22 | 2,319,683 | Japan | 31,830 | 1.37% | 25.60% | 35,302 |
| Godzilla Minus One | 3 / 2024-05-16-to-2024-05-22 | 2,319,683 | USA | 191,459 | 8.25% | 3.59% | 212,345 |
| Godzilla Minus One | 3 / 2024-05-16-to-2024-05-22 | 2,319,683 | China | 104,723 | 4.51% | 3.27% | 116,147 |
| Godzilla Minus One | 3 / 2024-05-16-to-2024-05-22 | 2,319,683 | South Korea | 171,401 | 7.39% | 1.89% | 190,099 |
| Godzilla Minus One | 4 / 2024-05-23-to-2024-05-29-partial | 2,324,450 | Japan | 37,623 | 1.62% | 26.24% | 41,727 |
| Godzilla Minus One | 4 / 2024-05-23-to-2024-05-29-partial | 2,324,450 | USA | 188,869 | 8.13% | 3.38% | 209,473 |
| Godzilla Minus One | 4 / 2024-05-23-to-2024-05-29-partial | 2,324,450 | China | 128,729 | 5.54% | 2.64% | 142,772 |
| Godzilla Minus One | 4 / 2024-05-23-to-2024-05-29-partial | 2,324,450 | South Korea | 223,969 | 9.64% | 1.85% | 248,402 |
| Godzilla Minus One | 5 / 2024-05-30-to-2024-06-05-partial | 2,615,417 | Japan | 38,045 | 1.45% | 26.00% | 42,195 |
| Godzilla Minus One | 5 / 2024-05-30-to-2024-06-05-partial | 2,615,417 | USA | 218,514 | 8.35% | 4.93% | 242,352 |
| Godzilla Minus One | 5 / 2024-05-30-to-2024-06-05-partial | 2,615,417 | China | 133,547 | 5.11% | 1.84% | 148,116 |
| Godzilla Minus One | 5 / 2024-05-30-to-2024-06-05-partial | 2,615,417 | South Korea | 231,057 | 8.83% | 1.84% | 256,263 |
| Godzilla Minus One | 6 / 2024-06-06-to-2024-06-12 | 2,689,284 | Japan | 40,138 | 1.49% | 26.13% | 44,517 |
| Godzilla Minus One | 6 / 2024-06-06-to-2024-06-12 | 2,689,284 | USA | 222,765 | 8.28% | 3.58% | 247,067 |
| Godzilla Minus One | 6 / 2024-06-06-to-2024-06-12 | 2,689,284 | China | 132,737 | 4.94% | 1.90% | 147,217 |
| Godzilla Minus One | 6 / 2024-06-06-to-2024-06-12 | 2,689,284 | South Korea | 235,819 | 8.77% | 1.85% | 261,545 |
| Godzilla Minus One | 7 / 2024-06-13-to-2024-06-19 | 2,424,787 | Japan | 30,029 | 1.24% | 26.09% | 33,305 |
| Godzilla Minus One | 7 / 2024-06-13-to-2024-06-19 | 2,424,787 | USA | 184,625 | 7.61% | 3.19% | 204,766 |
| Godzilla Minus One | 7 / 2024-06-13-to-2024-06-19 | 2,424,787 | China | 95,957 | 3.96% | 2.67% | 106,425 |
| Godzilla Minus One | 7 / 2024-06-13-to-2024-06-19 | 2,424,787 | South Korea | 172,040 | 7.10% | 1.86% | 190,808 |
| Godzilla Minus One | 8 / 2024-06-20-to-2024-06-26 | 2,183,356 | Japan | 22,310 | 1.02% | 24.80% | 24,744 |
| Godzilla Minus One | 8 / 2024-06-20-to-2024-06-26 | 2,183,356 | USA | 143,692 | 6.58% | 3.23% | 159,367 |
| Godzilla Minus One | 8 / 2024-06-20-to-2024-06-26 | 2,183,356 | China | 70,978 | 3.25% | 2.83% | 78,721 |
| Godzilla Minus One | 8 / 2024-06-20-to-2024-06-26 | 2,183,356 | South Korea | 122,589 | 5.61% | 1.78% | 135,962 |
| Godzilla Minus One | 9 / 2024-06-27-to-2024-07-03 | 2,176,024 | Japan | 31,609 | 1.45% | 25.96% | 35,057 |
| Godzilla Minus One | 9 / 2024-06-27-to-2024-07-03 | 2,176,024 | USA | 168,618 | 7.75% | 2.41% | 187,013 |
| Godzilla Minus One | 9 / 2024-06-27-to-2024-07-03 | 2,176,024 | China | 103,841 | 4.77% | 2.00% | 115,169 |
| Godzilla Minus One | 9 / 2024-06-27-to-2024-07-03 | 2,176,024 | South Korea | 194,893 | 8.96% | 1.81% | 216,154 |
| Godzilla Minus One | 10 / 2024-07-04-to-2024-07-10 | 2,020,393 | Japan | 33,169 | 1.64% | 25.92% | 36,787 |
| Godzilla Minus One | 10 / 2024-07-04-to-2024-07-10 | 2,020,393 | USA | 167,498 | 8.29% | 2.40% | 185,771 |
| Godzilla Minus One | 10 / 2024-07-04-to-2024-07-10 | 2,020,393 | China | 109,229 | 5.41% | 2.10% | 121,145 |
| Godzilla Minus One | 10 / 2024-07-04-to-2024-07-10 | 2,020,393 | South Korea | 209,021 | 10.35% | 1.80% | 231,823 |
| Godzilla Minus One | 11 / 2024-07-11-to-2024-07-17-partial | 2,151,340 | Japan | 27,373 | 1.27% | 26.29% | 30,359 |
| Godzilla Minus One | 11 / 2024-07-11-to-2024-07-17-partial | 2,151,340 | USA | 161,898 | 7.53% | 2.35% | 179,560 |
| Godzilla Minus One | 11 / 2024-07-11-to-2024-07-17-partial | 2,151,340 | China | 95,507 | 4.44% | 2.76% | 105,926 |
| Godzilla Minus One | 11 / 2024-07-11-to-2024-07-17-partial | 2,151,340 | South Korea | 175,835 | 8.17% | 1.73% | 195,017 |
| Godzilla Minus One | 12 / 2024-07-18-to-2024-07-24 | 2,344,422 | Japan | 38,175 | 1.63% | 26.40% | 42,340 |
| Godzilla Minus One | 12 / 2024-07-18-to-2024-07-24 | 2,344,422 | USA | 176,170 | 7.51% | 2.20% | 195,389 |
| Godzilla Minus One | 12 / 2024-07-18-to-2024-07-24 | 2,344,422 | China | 132,047 | 5.63% | 2.06% | 146,452 |
| Godzilla Minus One | 12 / 2024-07-18-to-2024-07-24 | 2,344,422 | South Korea | 255,432 | 10.90% | 1.72% | 283,297 |
| Godzilla Minus One | 13 / 2024-07-25-to-2024-07-31 | 2,615,180 | Japan | 45,644 | 1.75% | 26.90% | 50,623 |
| Godzilla Minus One | 13 / 2024-07-25-to-2024-07-31 | 2,615,180 | USA | 197,336 | 7.55% | 2.25% | 218,864 |
| Godzilla Minus One | 13 / 2024-07-25-to-2024-07-31 | 2,615,180 | China | 173,094 | 6.62% | 2.17% | 191,977 |
| Godzilla Minus One | 13 / 2024-07-25-to-2024-07-31 | 2,615,180 | South Korea | 324,736 | 12.42% | 1.65% | 360,162 |
| Godzilla Minus One | 14 / 2024-08-01-to-2024-08-07 | 2,691,468 | Japan | 40,630 | 1.51% | 26.75% | 45,062 |
| Godzilla Minus One | 14 / 2024-08-01-to-2024-08-07 | 2,691,468 | USA | 208,226 | 7.74% | 1.82% | 230,942 |
| Godzilla Minus One | 14 / 2024-08-01-to-2024-08-07 | 2,691,468 | China | 165,077 | 6.13% | 2.22% | 183,085 |
| Godzilla Minus One | 14 / 2024-08-01-to-2024-08-07 | 2,691,468 | South Korea | 290,772 | 10.80% | 1.69% | 322,493 |
| Godzilla Minus One | 15 / 2024-08-08-to-2024-08-14 | 2,564,330 | Japan | 39,229 | 1.53% | 26.09% | 43,509 |
| Godzilla Minus One | 15 / 2024-08-08-to-2024-08-14 | 2,564,330 | USA | 177,621 | 6.93% | 1.96% | 196,998 |
| Godzilla Minus One | 15 / 2024-08-08-to-2024-08-14 | 2,564,330 | China | 154,646 | 6.03% | 1.60% | 171,516 |
| Godzilla Minus One | 15 / 2024-08-08-to-2024-08-14 | 2,564,330 | South Korea | 269,548 | 10.51% | 1.82% | 298,953 |
| Godzilla x Kong | 1 / 2024-05-14-to-2024-05-20 | 4,682,214 | Japan | 32,662 | 0.70% | 25.58% | 36,225 |
| Godzilla x Kong | 1 / 2024-05-14-to-2024-05-20 | 4,682,214 | USA | 333,801 | 7.13% | 10.47% | 370,216 |
| Godzilla x Kong | 1 / 2024-05-14-to-2024-05-20 | 4,682,214 | China | 169,376 | 3.62% | 3.14% | 187,853 |
| Godzilla x Kong | 1 / 2024-05-14-to-2024-05-20 | 4,682,214 | South Korea | 199,409 | 4.26% | 5.63% | 221,163 |
| Godzilla x Kong | 2 / 2024-05-21-to-2024-05-27 | 4,289,660 | Japan | 44,805 | 1.04% | 26.15% | 49,693 |
| Godzilla x Kong | 2 / 2024-05-21-to-2024-05-27 | 4,289,660 | USA | 289,250 | 6.74% | 8.14% | 320,805 |
| Godzilla x Kong | 2 / 2024-05-21-to-2024-05-27 | 4,289,660 | China | 161,656 | 3.77% | 2.56% | 179,291 |
| Godzilla x Kong | 2 / 2024-05-21-to-2024-05-27 | 4,289,660 | South Korea | 269,091 | 6.27% | 3.19% | 298,446 |
| Godzilla x Kong | 3 / 2024-05-28-to-2024-06-03 | 3,948,582 | Japan | 45,340 | 1.15% | 26.47% | 50,286 |
| Godzilla x Kong | 3 / 2024-05-28-to-2024-06-03 | 3,948,582 | USA | 263,859 | 6.68% | 7.22% | 292,644 |
| Godzilla x Kong | 3 / 2024-05-28-to-2024-06-03 | 3,948,582 | China | 163,001 | 4.13% | 1.67% | 180,783 |
| Godzilla x Kong | 3 / 2024-05-28-to-2024-06-03 | 3,948,582 | South Korea | 282,287 | 7.15% | 2.48% | 313,082 |
| Godzilla x Kong | 4 / 2024-06-04-to-2024-06-10 | 3,665,641 | Japan | 45,291 | 1.24% | 26.22% | 50,232 |
| Godzilla x Kong | 4 / 2024-06-04-to-2024-06-10 | 3,665,641 | USA | 260,624 | 7.11% | 7.17% | 289,056 |
| Godzilla x Kong | 4 / 2024-06-04-to-2024-06-10 | 3,665,641 | China | 161,179 | 4.40% | 1.69% | 178,762 |
| Godzilla x Kong | 4 / 2024-06-04-to-2024-06-10 | 3,665,641 | South Korea | 277,481 | 7.57% | 2.33% | 307,752 |
| Godzilla x Kong | 5 / 2024-06-11-to-2024-06-17 | 3,383,188 | Japan | 30,944 | 0.91% | 26.36% | 34,320 |
| Godzilla x Kong | 5 / 2024-06-11-to-2024-06-17 | 3,383,188 | USA | 224,486 | 6.64% | 6.43% | 248,975 |
| Godzilla x Kong | 5 / 2024-06-11-to-2024-06-17 | 3,383,188 | China | 105,528 | 3.12% | 2.42% | 117,040 |
| Godzilla x Kong | 5 / 2024-06-11-to-2024-06-17 | 3,383,188 | South Korea | 179,676 | 5.31% | 3.05% | 199,277 |
| Godzilla x Kong | 6 / 2024-06-18-to-2024-06-24 | 3,134,906 | Japan | 28,356 | 0.90% | 25.92% | 31,449 |
| Godzilla x Kong | 6 / 2024-06-18-to-2024-06-24 | 3,134,906 | USA | 199,067 | 6.35% | 6.65% | 220,783 |
| Godzilla x Kong | 6 / 2024-06-18-to-2024-06-24 | 3,134,906 | China | 93,427 | 2.98% | 2.42% | 103,619 |
| Godzilla x Kong | 6 / 2024-06-18-to-2024-06-24 | 3,134,906 | South Korea | 167,711 | 5.35% | 2.79% | 186,007 |
| Godzilla x Kong | 7 / 2024-06-25-to-2024-07-01 | 2,996,099 | Japan | 28,343 | 0.95% | 25.30% | 31,435 |
| Godzilla x Kong | 7 / 2024-06-25-to-2024-07-01 | 2,996,099 | USA | 194,029 | 6.48% | 6.49% | 215,196 |
| Godzilla x Kong | 7 / 2024-06-25-to-2024-07-01 | 2,996,099 | China | 96,180 | 3.21% | 2.32% | 106,672 |
| Godzilla x Kong | 7 / 2024-06-25-to-2024-07-01 | 2,996,099 | South Korea | 169,698 | 5.66% | 2.45% | 188,211 |
| Godzilla x Kong | 8 / 2024-07-02-to-2024-07-08 | 2,987,428 | Japan | 38,025 | 1.27% | 25.60% | 42,173 |
| Godzilla x Kong | 8 / 2024-07-02-to-2024-07-08 | 2,987,428 | USA | 227,314 | 7.61% | 5.56% | 252,112 |
| Godzilla x Kong | 8 / 2024-07-02-to-2024-07-08 | 2,987,428 | China | 133,549 | 4.47% | 2.04% | 148,118 |
| Godzilla x Kong | 8 / 2024-07-02-to-2024-07-08 | 2,987,428 | South Korea | 242,775 | 8.13% | 2.23% | 269,260 |
| Godzilla x Kong | 9 / 2024-07-09-to-2024-07-15 | 3,055,307 | Japan | 36,475 | 1.19% | 26.13% | 40,454 |
| Godzilla x Kong | 9 / 2024-07-09-to-2024-07-15 | 3,055,307 | USA | 216,101 | 7.07% | 5.65% | 239,676 |
| Godzilla x Kong | 9 / 2024-07-09-to-2024-07-15 | 3,055,307 | China | 125,317 | 4.10% | 2.51% | 138,988 |
| Godzilla x Kong | 9 / 2024-07-09-to-2024-07-15 | 3,055,307 | South Korea | 235,922 | 7.72% | 2.10% | 261,659 |
| Godzilla x Kong | 10 / 2024-07-16-to-2024-07-22-partial | 2,166,099 | Japan | 24,479 | 1.13% | 26.14% | 27,149 |
| Godzilla x Kong | 10 / 2024-07-16-to-2024-07-22-partial | 2,166,099 | USA | 149,861 | 6.92% | 4.80% | 166,209 |
| Godzilla x Kong | 10 / 2024-07-16-to-2024-07-22-partial | 2,166,099 | China | 89,497 | 4.13% | 2.75% | 99,260 |
| Godzilla x Kong | 10 / 2024-07-16-to-2024-07-22-partial | 2,166,099 | South Korea | 165,192 | 7.63% | 2.05% | 183,213 |
| Godzilla x Kong | 11 / 2024-07-23-to-2024-07-29 | 3,376,015 | Japan | 49,776 | 1.47% | 27.05% | 55,206 |
| Godzilla x Kong | 11 / 2024-07-23-to-2024-07-29 | 3,376,015 | USA | 236,856 | 7.02% | 4.31% | 262,695 |
| Godzilla x Kong | 11 / 2024-07-23-to-2024-07-29 | 3,376,015 | China | 184,307 | 5.46% | 2.16% | 204,413 |
| Godzilla x Kong | 11 / 2024-07-23-to-2024-07-29 | 3,376,015 | South Korea | 354,421 | 10.50% | 1.82% | 393,085 |
| Godzilla x Kong | 12 / 2024-07-30-to-2024-08-05 | 3,358,879 | Japan | 46,101 | 1.37% | 26.87% | 51,130 |
| Godzilla x Kong | 12 / 2024-07-30-to-2024-08-05 | 3,358,879 | USA | 245,796 | 7.32% | 3.47% | 272,610 |
| Godzilla x Kong | 12 / 2024-07-30-to-2024-08-05 | 3,358,879 | China | 187,856 | 5.59% | 2.18% | 208,349 |
| Godzilla x Kong | 12 / 2024-07-30-to-2024-08-05 | 3,358,879 | South Korea | 336,168 | 10.01% | 1.79% | 372,841 |
| Godzilla x Kong | 13 / 2024-08-06-to-2024-08-12 | 2,996,063 | Japan | 36,547 | 1.22% | 26.85% | 40,534 |
| Godzilla x Kong | 13 / 2024-08-06-to-2024-08-12 | 2,996,063 | USA | 196,752 | 6.57% | 3.60% | 218,216 |
| Godzilla x Kong | 13 / 2024-08-06-to-2024-08-12 | 2,996,063 | China | 152,758 | 5.10% | 1.55% | 169,423 |
| Godzilla x Kong | 13 / 2024-08-06-to-2024-08-12 | 2,996,063 | South Korea | 262,688 | 8.77% | 1.84% | 291,345 |
| Godzilla x Kong | 14 / 2024-08-13-to-2024-08-19 | 2,902,020 | Japan | 41,057 | 1.41% | 26.40% | 45,536 |
| Godzilla x Kong | 14 / 2024-08-13-to-2024-08-19 | 2,902,020 | USA | 193,980 | 6.68% | 3.66% | 215,141 |
| Godzilla x Kong | 14 / 2024-08-13-to-2024-08-19 | 2,902,020 | China | 152,175 | 5.24% | 1.47% | 168,776 |
| Godzilla x Kong | 14 / 2024-08-13-to-2024-08-19 | 2,902,020 | South Korea | 290,567 | 10.01% | 1.91% | 322,265 |
| Godzilla x Kong | 15 / 2024-08-20-to-2024-08-26 | 2,892,119 | Japan | 28,051 | 0.97% | 25.96% | 31,111 |
| Godzilla x Kong | 15 / 2024-08-20-to-2024-08-26 | 2,892,119 | USA | 175,931 | 6.08% | 4.31% | 195,123 |
| Godzilla x Kong | 15 / 2024-08-20-to-2024-08-26 | 2,892,119 | China | 114,934 | 3.97% | 1.59% | 127,472 |
| Godzilla x Kong | 15 / 2024-08-20-to-2024-08-26 | 2,892,119 | South Korea | 192,902 | 6.67% | 1.97% | 213,946 |
| Godzilla vs. Kong | 1 / 2021-03-31-to-2021-04-06-partial | 5,392,240 | Japan | 30,946 | 0.57% | 17.58% | 38,525 |
| Godzilla vs. Kong | 1 / 2021-03-31-to-2021-04-06-partial | 5,392,240 | USA | 464,686 | 8.62% | 9.09% | 578,487 |
| Godzilla vs. Kong | 1 / 2021-03-31-to-2021-04-06-partial | 5,392,240 | China | 302,010 | 5.60% | 2.64% | 375,972 |
| Godzilla vs. Kong | 1 / 2021-03-31-to-2021-04-06-partial | 5,392,240 | South Korea | 161,906 | 3.00% | 5.87% | 201,556 |
| Godzilla vs. Kong | 2 / 2021-04-07-to-2021-04-13 | 4,595,486 | Japan | 31,640 | 0.69% | 15.36% | 39,389 |
| Godzilla vs. Kong | 2 / 2021-04-07-to-2021-04-13 | 4,595,486 | USA | 385,660 | 8.39% | 8.01% | 480,107 |
| Godzilla vs. Kong | 2 / 2021-04-07-to-2021-04-13 | 4,595,486 | China | 204,451 | 4.45% | 2.43% | 254,521 |
| Godzilla vs. Kong | 2 / 2021-04-07-to-2021-04-13 | 4,595,486 | South Korea | 133,340 | 2.90% | 8.35% | 165,995 |
| Godzilla vs. Kong | 3 / 2021-04-14-to-2021-04-20 | 3,321,353 | Japan | 8,886 | 0.27% | 24.39% | 11,062 |
| Godzilla vs. Kong | 3 / 2021-04-14-to-2021-04-20 | 3,321,353 | USA | 180,970 | 5.45% | 13.27% | 225,289 |
| Godzilla vs. Kong | 3 / 2021-04-14-to-2021-04-20 | 3,321,353 | China | 111,155 | 3.35% | 2.75% | 138,377 |
| Godzilla vs. Kong | 3 / 2021-04-14-to-2021-04-20 | 3,321,353 | South Korea | 61,135 | 1.84% | 10.67% | 76,107 |
| Godzilla vs. Kong | 4 / 2021-04-21-to-2021-04-27 | 2,972,988 | Japan | 13,444 | 0.45% | 18.69% | 16,736 |
| Godzilla vs. Kong | 4 / 2021-04-21-to-2021-04-27 | 2,972,988 | USA | 224,155 | 7.54% | 9.46% | 279,050 |
| Godzilla vs. Kong | 4 / 2021-04-21-to-2021-04-27 | 2,972,988 | China | 83,705 | 2.82% | 2.55% | 104,204 |
| Godzilla vs. Kong | 4 / 2021-04-21-to-2021-04-27 | 2,972,988 | South Korea | 54,288 | 1.83% | 10.43% | 67,583 |
| Godzilla vs. Kong | 5 / 2021-04-28-to-2021-05-04 | 4,960,450 | Japan | 148,241 | 2.99% | 11.92% | 184,545 |
| Godzilla vs. Kong | 5 / 2021-04-28-to-2021-05-04 | 4,960,450 | USA | 1,210,927 | 24.41% | 2.29% | 1,507,481 |
| Godzilla vs. Kong | 5 / 2021-04-28-to-2021-05-04 | 4,960,450 | China | 324,717 | 6.55% | 2.40% | 404,240 |
| Godzilla vs. Kong | 5 / 2021-04-28-to-2021-05-04 | 4,960,450 | South Korea | 120,456 | 2.43% | 5.72% | 149,955 |
| Godzilla vs. Kong | 6 / 2021-05-05-to-2021-05-11 | 4,517,424 | Japan | 142,706 | 3.16% | 11.99% | 177,654 |
| Godzilla vs. Kong | 6 / 2021-05-05-to-2021-05-11 | 4,517,424 | USA | 1,167,825 | 25.85% | 2.01% | 1,453,823 |
| Godzilla vs. Kong | 6 / 2021-05-05-to-2021-05-11 | 4,517,424 | China | 279,464 | 6.19% | 2.45% | 347,904 |
| Godzilla vs. Kong | 6 / 2021-05-05-to-2021-05-11 | 4,517,424 | South Korea | 107,170 | 2.37% | 5.19% | 133,416 |
| Godzilla vs. Kong | 7 / 2021-05-12-to-2021-05-18 | 4,672,259 | Japan | 156,468 | 3.35% | 11.99% | 194,787 |
| Godzilla vs. Kong | 7 / 2021-05-12-to-2021-05-18 | 4,672,259 | USA | 1,270,827 | 27.20% | 1.94% | 1,582,050 |
| Godzilla vs. Kong | 7 / 2021-05-12-to-2021-05-18 | 4,672,259 | China | 295,237 | 6.32% | 2.41% | 367,540 |
| Godzilla vs. Kong | 7 / 2021-05-12-to-2021-05-18 | 4,672,259 | South Korea | 110,042 | 2.36% | 4.69% | 136,991 |
| Godzilla vs. Kong | 8 / 2021-05-19-to-2021-05-25 | 3,640,619 | Japan | 104,079 | 2.86% | 12.40% | 129,568 |
| Godzilla vs. Kong | 8 / 2021-05-19-to-2021-05-25 | 3,640,619 | USA | 867,659 | 23.83% | 2.20% | 1,080,147 |
| Godzilla vs. Kong | 8 / 2021-05-19-to-2021-05-25 | 3,640,619 | China | 207,620 | 5.70% | 2.54% | 258,466 |
| Godzilla vs. Kong | 8 / 2021-05-19-to-2021-05-25 | 3,640,619 | South Korea | 80,085 | 2.20% | 4.95% | 99,698 |
| Godzilla vs. Kong | 9 / 2021-05-26-to-2021-06-01 | 3,254,132 | Japan | 92,209 | 2.83% | 12.58% | 114,791 |
| Godzilla vs. Kong | 9 / 2021-05-26-to-2021-06-01 | 3,254,132 | USA | 766,433 | 23.55% | 2.44% | 954,131 |
| Godzilla vs. Kong | 9 / 2021-05-26-to-2021-06-01 | 3,254,132 | China | 182,502 | 5.61% | 2.42% | 227,196 |
| Godzilla vs. Kong | 9 / 2021-05-26-to-2021-06-01 | 3,254,132 | South Korea | 72,732 | 2.24% | 4.98% | 90,544 |
| Godzilla vs. Kong | 10 / 2021-06-02-to-2021-06-08 | 3,206,836 | Japan | 96,318 | 3.00% | 12.49% | 119,906 |
| Godzilla vs. Kong | 10 / 2021-06-02-to-2021-06-08 | 3,206,836 | USA | 817,874 | 25.50% | 2.14% | 1,018,170 |
| Godzilla vs. Kong | 10 / 2021-06-02-to-2021-06-08 | 3,206,836 | China | 187,371 | 5.84% | 2.39% | 233,258 |
| Godzilla vs. Kong | 10 / 2021-06-02-to-2021-06-08 | 3,206,836 | South Korea | 71,108 | 2.22% | 4.68% | 88,522 |
| Godzilla vs. Kong | 11 / 2021-06-09-to-2021-06-15 | 3,002,410 | Japan | 94,538 | 3.15% | 12.39% | 117,690 |
| Godzilla vs. Kong | 11 / 2021-06-09-to-2021-06-15 | 3,002,410 | USA | 769,363 | 25.62% | 2.14% | 957,778 |
| Godzilla vs. Kong | 11 / 2021-06-09-to-2021-06-15 | 3,002,410 | China | 186,193 | 6.20% | 2.30% | 231,791 |
| Godzilla vs. Kong | 11 / 2021-06-09-to-2021-06-15 | 3,002,410 | South Korea | 68,863 | 2.29% | 4.21% | 85,727 |
| Godzilla vs. Kong | 12 / 2021-06-16-to-2021-06-22 | 2,882,422 | Japan | 99,429 | 3.45% | 11.75% | 123,779 |
| Godzilla vs. Kong | 12 / 2021-06-16-to-2021-06-22 | 2,882,422 | USA | 772,992 | 26.82% | 1.99% | 962,296 |
| Godzilla vs. Kong | 12 / 2021-06-16-to-2021-06-22 | 2,882,422 | China | 173,499 | 6.02% | 2.33% | 215,989 |
| Godzilla vs. Kong | 12 / 2021-06-16-to-2021-06-22 | 2,882,422 | South Korea | 66,330 | 2.30% | 3.87% | 82,574 |
| Godzilla vs. Kong | 13 / 2021-06-23-to-2021-06-29 | 3,013,412 | Japan | 105,222 | 3.49% | 12.07% | 130,991 |
| Godzilla vs. Kong | 13 / 2021-06-23-to-2021-06-29 | 3,013,412 | USA | 863,804 | 28.67% | 1.91% | 1,075,348 |
| Godzilla vs. Kong | 13 / 2021-06-23-to-2021-06-29 | 3,013,412 | China | 189,382 | 6.28% | 2.36% | 235,761 |
| Godzilla vs. Kong | 13 / 2021-06-23-to-2021-06-29 | 3,013,412 | South Korea | 70,328 | 2.33% | 3.79% | 87,551 |
| Godzilla vs. Kong | 14 / 2021-06-30-to-2021-07-06 | 2,895,433 | Japan | 103,641 | 3.58% | 12.25% | 129,022 |
| Godzilla vs. Kong | 14 / 2021-06-30-to-2021-07-06 | 2,895,433 | USA | 837,677 | 28.93% | 1.88% | 1,042,822 |
| Godzilla vs. Kong | 14 / 2021-06-30-to-2021-07-06 | 2,895,433 | China | 184,020 | 6.36% | 2.28% | 229,086 |
| Godzilla vs. Kong | 14 / 2021-06-30-to-2021-07-06 | 2,895,433 | South Korea | 69,022 | 2.38% | 3.46% | 85,925 |
| Godzilla vs. Kong | 15 / 2021-07-07-to-2021-07-13 | 2,768,556 | Japan | 100,178 | 3.62% | 12.13% | 124,711 |
| Godzilla vs. Kong | 15 / 2021-07-07-to-2021-07-13 | 2,768,556 | USA | 822,176 | 29.70% | 1.80% | 1,023,525 |
| Godzilla vs. Kong | 15 / 2021-07-07-to-2021-07-13 | 2,768,556 | China | 175,152 | 6.33% | 2.33% | 218,046 |
| Godzilla vs. Kong | 15 / 2021-07-07-to-2021-07-13 | 2,768,556 | South Korea | 65,508 | 2.37% | 3.22% | 81,551 |
| Monarch 101 | 1 / 2023-11-17-to-2023-11-23-partial | 1,398,335 | Japan | 7,893 | 0.56% | 21.68% | 8,916 |
| Monarch 101 | 1 / 2023-11-17-to-2023-11-23-partial | 1,398,335 | USA | 161,677 | 11.56% | 9.20% | 182,635 |
| Monarch 101 | 1 / 2023-11-17-to-2023-11-23-partial | 1,398,335 | China | 130,483 | 9.33% | 2.99% | 147,397 |
| Monarch 101 | 1 / 2023-11-17-to-2023-11-23-partial | 1,398,335 | South Korea | 30,389 | 2.17% | 4.18% | 34,328 |
| Monarch 101 | 2 / 2023-11-24-to-2023-11-30 | 1,341,030 | Japan | 8,832 | 0.66% | 23.58% | 9,977 |
| Monarch 101 | 2 / 2023-11-24-to-2023-11-30 | 1,341,030 | USA | 130,513 | 9.73% | 7.57% | 147,431 |
| Monarch 101 | 2 / 2023-11-24-to-2023-11-30 | 1,341,030 | China | 60,910 | 4.54% | 2.85% | 68,806 |
| Monarch 101 | 2 / 2023-11-24-to-2023-11-30 | 1,341,030 | South Korea | 45,606 | 3.40% | 1.92% | 51,518 |
| Monarch 101 | 3 / 2023-12-01-to-2023-12-07 | 1,383,237 | Japan | 10,942 | 0.79% | 23.38% | 12,360 |
| Monarch 101 | 3 / 2023-12-01-to-2023-12-07 | 1,383,237 | USA | 142,116 | 10.27% | 6.62% | 160,538 |
| Monarch 101 | 3 / 2023-12-01-to-2023-12-07 | 1,383,237 | China | 66,017 | 4.77% | 2.68% | 74,575 |
| Monarch 101 | 3 / 2023-12-01-to-2023-12-07 | 1,383,237 | South Korea | 56,086 | 4.05% | 1.90% | 63,356 |
| Monarch 101 | 4 / 2023-12-08-to-2023-12-14 | 1,270,221 | Japan | 10,087 | 0.79% | 22.88% | 11,395 |
| Monarch 101 | 4 / 2023-12-08-to-2023-12-14 | 1,270,221 | USA | 121,474 | 9.56% | 5.46% | 137,221 |
| Monarch 101 | 4 / 2023-12-08-to-2023-12-14 | 1,270,221 | China | 55,088 | 4.34% | 2.42% | 62,229 |
| Monarch 101 | 4 / 2023-12-08-to-2023-12-14 | 1,270,221 | South Korea | 55,156 | 4.34% | 1.76% | 62,306 |
| Monarch 101 | 5 / 2023-12-15-to-2023-12-21 | 1,123,818 | Japan | 6,770 | 0.60% | 23.75% | 7,648 |
| Monarch 101 | 5 / 2023-12-15-to-2023-12-21 | 1,123,818 | USA | 104,648 | 9.31% | 5.08% | 118,213 |
| Monarch 101 | 5 / 2023-12-15-to-2023-12-21 | 1,123,818 | China | 39,413 | 3.51% | 2.27% | 44,522 |
| Monarch 101 | 5 / 2023-12-15-to-2023-12-21 | 1,123,818 | South Korea | 33,126 | 2.95% | 1.82% | 37,420 |
| Monarch 101 | 6 / 2023-12-22-to-2023-12-28 | 1,027,484 | Japan | 5,561 | 0.54% | 23.56% | 6,282 |
| Monarch 101 | 6 / 2023-12-22-to-2023-12-28 | 1,027,484 | USA | 93,238 | 9.07% | 4.91% | 105,324 |
| Monarch 101 | 6 / 2023-12-22-to-2023-12-28 | 1,027,484 | China | 30,964 | 3.01% | 2.32% | 34,978 |
| Monarch 101 | 6 / 2023-12-22-to-2023-12-28 | 1,027,484 | South Korea | 26,959 | 2.62% | 2.14% | 30,454 |
| Monarch 101 | 7 / 2023-12-29-to-2024-01-04 | 1,102,862 | Japan | 7,700 | 0.70% | 23.60% | 8,698 |
| Monarch 101 | 7 / 2023-12-29-to-2024-01-04 | 1,102,862 | USA | 99,118 | 8.99% | 4.84% | 111,967 |
| Monarch 101 | 7 / 2023-12-29-to-2024-01-04 | 1,102,862 | China | 35,068 | 3.18% | 1.95% | 39,614 |
| Monarch 101 | 7 / 2023-12-29-to-2024-01-04 | 1,102,862 | South Korea | 39,960 | 3.62% | 1.62% | 45,140 |
| Monarch 101 | 8 / 2024-01-05-to-2024-01-11 | 1,094,142 | Japan | 8,978 | 0.82% | 23.94% | 10,142 |
| Monarch 101 | 8 / 2024-01-05-to-2024-01-11 | 1,094,142 | USA | 101,497 | 9.28% | 4.34% | 114,654 |
| Monarch 101 | 8 / 2024-01-05-to-2024-01-11 | 1,094,142 | China | 39,349 | 3.60% | 1.88% | 44,450 |
| Monarch 101 | 8 / 2024-01-05-to-2024-01-11 | 1,094,142 | South Korea | 51,938 | 4.75% | 1.97% | 58,671 |
| Monarch 101 | 9 / 2024-01-12-to-2024-01-18 | 1,079,437 | Japan | 8,315 | 0.77% | 23.56% | 9,393 |
| Monarch 101 | 9 / 2024-01-12-to-2024-01-18 | 1,079,437 | USA | 95,114 | 8.81% | 3.91% | 107,444 |
| Monarch 101 | 9 / 2024-01-12-to-2024-01-18 | 1,079,437 | China | 43,513 | 4.03% | 1.82% | 49,154 |
| Monarch 101 | 9 / 2024-01-12-to-2024-01-18 | 1,079,437 | South Korea | 50,712 | 4.70% | 1.95% | 57,286 |
| Monarch 101 | 10 / 2024-01-19-to-2024-01-25 | 883,762 | Japan | 5,905 | 0.67% | 23.37% | 6,670 |
| Monarch 101 | 10 / 2024-01-19-to-2024-01-25 | 883,762 | USA | 72,736 | 8.23% | 2.39% | 82,165 |
| Monarch 101 | 10 / 2024-01-19-to-2024-01-25 | 883,762 | China | 28,374 | 3.21% | 1.70% | 32,052 |
| Monarch 101 | 10 / 2024-01-19-to-2024-01-25 | 883,762 | South Korea | 37,660 | 4.26% | 2.00% | 42,542 |
| Monarch 101 | 11 / 2024-01-26-to-2024-02-01 | 841,192 | Japan | 6,879 | 0.82% | 24.44% | 7,771 |
| Monarch 101 | 11 / 2024-01-26-to-2024-02-01 | 841,192 | USA | 68,385 | 8.13% | 2.13% | 77,250 |
| Monarch 101 | 11 / 2024-01-26-to-2024-02-01 | 841,192 | China | 31,505 | 3.75% | 1.64% | 35,589 |
| Monarch 101 | 11 / 2024-01-26-to-2024-02-01 | 841,192 | South Korea | 45,861 | 5.45% | 1.73% | 51,806 |
| Monarch 101 | 12 / 2024-02-02-to-2024-02-08-partial | 746,994 | Japan | 7,328 | 0.98% | 25.82% | 8,278 |
| Monarch 101 | 12 / 2024-02-02-to-2024-02-08-partial | 746,994 | USA | 60,124 | 8.05% | 1.85% | 67,918 |
| Monarch 101 | 12 / 2024-02-02-to-2024-02-08-partial | 746,994 | China | 32,073 | 4.29% | 1.74% | 36,231 |
| Monarch 101 | 12 / 2024-02-02-to-2024-02-08-partial | 746,994 | South Korea | 51,238 | 6.86% | 1.68% | 57,880 |
| Monarch 101 | 13 / 2024-02-09-to-2024-02-15 | 808,230 | Japan | 6,701 | 0.83% | 24.32% | 7,570 |
| Monarch 101 | 13 / 2024-02-09-to-2024-02-15 | 808,230 | USA | 61,642 | 7.63% | 2.06% | 69,633 |
| Monarch 101 | 13 / 2024-02-09-to-2024-02-15 | 808,230 | China | 28,245 | 3.49% | 1.36% | 31,906 |
| Monarch 101 | 13 / 2024-02-09-to-2024-02-15 | 808,230 | South Korea | 46,183 | 5.71% | 1.62% | 52,170 |
| Monarch 101 | 14 / 2024-02-16-to-2024-02-22 | 880,303 | Japan | 9,254 | 1.05% | 23.72% | 10,454 |
| Monarch 101 | 14 / 2024-02-16-to-2024-02-22 | 880,303 | USA | 70,125 | 7.97% | 2.40% | 79,215 |
| Monarch 101 | 14 / 2024-02-16-to-2024-02-22 | 880,303 | China | 39,208 | 4.45% | 1.31% | 44,291 |
| Monarch 101 | 14 / 2024-02-16-to-2024-02-22 | 880,303 | South Korea | 62,132 | 7.06% | 1.61% | 70,186 |
| Monarch 101 | 15 / 2024-02-23-to-2024-02-29 | 897,382 | Japan | 10,319 | 1.15% | 25.45% | 11,657 |
| Monarch 101 | 15 / 2024-02-23-to-2024-02-29 | 897,382 | USA | 69,416 | 7.74% | 2.13% | 78,414 |
| Monarch 101 | 15 / 2024-02-23-to-2024-02-29 | 897,382 | China | 41,347 | 4.61% | 1.34% | 46,707 |
| Monarch 101 | 15 / 2024-02-23-to-2024-02-29 | 897,382 | South Korea | 68,462 | 7.63% | 1.65% | 77,337 |
| Monarch 110 | 1 / 2024-01-12-to-2024-01-18-partial | 818,674 | Japan | 4,875 | 0.60% | 24.10% | 5,407 |
| Monarch 110 | 1 / 2024-01-12-to-2024-01-18-partial | 818,674 | USA | 87,549 | 10.69% | 6.13% | 97,100 |
| Monarch 110 | 1 / 2024-01-12-to-2024-01-18-partial | 818,674 | China | 33,295 | 4.07% | 2.14% | 36,927 |
| Monarch 110 | 1 / 2024-01-12-to-2024-01-18-partial | 818,674 | South Korea | 22,320 | 2.73% | 2.41% | 24,755 |
| Monarch 110 | 2 / 2024-01-19-to-2024-01-25 | 658,486 | Japan | 4,036 | 0.61% | 21.80% | 4,476 |
| Monarch 110 | 2 / 2024-01-19-to-2024-01-25 | 658,486 | USA | 53,953 | 8.19% | 3.79% | 59,839 |
| Monarch 110 | 2 / 2024-01-19-to-2024-01-25 | 658,486 | China | 21,366 | 3.24% | 1.91% | 23,697 |
| Monarch 110 | 2 / 2024-01-19-to-2024-01-25 | 658,486 | South Korea | 23,374 | 3.55% | 2.22% | 25,924 |
| Monarch 110 | 3 / 2024-01-26-to-2024-02-01-partial | 685,779 | Japan | 5,331 | 0.78% | 24.25% | 5,913 |
| Monarch 110 | 3 / 2024-01-26-to-2024-02-01-partial | 685,779 | USA | 53,563 | 7.81% | 3.04% | 59,406 |
| Monarch 110 | 3 / 2024-01-26-to-2024-02-01-partial | 685,779 | China | 24,680 | 3.60% | 1.41% | 27,372 |
| Monarch 110 | 3 / 2024-01-26-to-2024-02-01-partial | 685,779 | South Korea | 36,243 | 5.28% | 1.84% | 40,197 |
| Monarch 110 | 4 / 2024-02-02-to-2024-02-08 | 719,296 | Japan | 6,870 | 0.96% | 24.50% | 7,619 |
| Monarch 110 | 4 / 2024-02-02-to-2024-02-08 | 719,296 | USA | 53,549 | 7.44% | 2.54% | 59,391 |
| Monarch 110 | 4 / 2024-02-02-to-2024-02-08 | 719,296 | China | 29,264 | 4.07% | 1.58% | 32,456 |
| Monarch 110 | 4 / 2024-02-02-to-2024-02-08 | 719,296 | South Korea | 47,694 | 6.63% | 1.57% | 52,897 |
| Monarch 110 | 5 / 2024-02-09-to-2024-02-15 | 659,303 | Japan | 5,374 | 0.82% | 23.60% | 5,960 |
| Monarch 110 | 5 / 2024-02-09-to-2024-02-15 | 659,303 | USA | 44,833 | 6.80% | 2.62% | 49,724 |
| Monarch 110 | 5 / 2024-02-09-to-2024-02-15 | 659,303 | China | 22,819 | 3.46% | 2.07% | 25,308 |
| Monarch 110 | 5 / 2024-02-09-to-2024-02-15 | 659,303 | South Korea | 36,889 | 5.60% | 1.66% | 40,913 |
| Monarch 110 | 6 / 2024-02-16-to-2024-02-22 | 720,799 | Japan | 7,575 | 1.05% | 24.46% | 8,401 |
| Monarch 110 | 6 / 2024-02-16-to-2024-02-22 | 720,799 | USA | 50,772 | 7.04% | 2.35% | 56,311 |
| Monarch 110 | 6 / 2024-02-16-to-2024-02-22 | 720,799 | China | 31,557 | 4.38% | 1.42% | 35,000 |
| Monarch 110 | 6 / 2024-02-16-to-2024-02-22 | 720,799 | South Korea | 52,658 | 7.31% | 1.57% | 58,403 |
| Monarch 110 | 7 / 2024-02-23-to-2024-02-29 | 749,900 | Japan | 8,760 | 1.17% | 25.39% | 9,716 |
| Monarch 110 | 7 / 2024-02-23-to-2024-02-29 | 749,900 | USA | 49,997 | 6.67% | 2.33% | 55,451 |
| Monarch 110 | 7 / 2024-02-23-to-2024-02-29 | 749,900 | China | 33,500 | 4.47% | 1.64% | 37,155 |
| Monarch 110 | 7 / 2024-02-23-to-2024-02-29 | 749,900 | South Korea | 59,209 | 7.90% | 1.51% | 65,668 |
| Monarch 110 | 8 / 2024-03-01-to-2024-03-07 | 976,207 | Japan | 13,529 | 1.39% | 25.86% | 15,005 |
| Monarch 110 | 8 / 2024-03-01-to-2024-03-07 | 976,207 | USA | 65,901 | 6.75% | 2.22% | 73,090 |
| Monarch 110 | 8 / 2024-03-01-to-2024-03-07 | 976,207 | China | 48,487 | 4.97% | 1.58% | 53,776 |
| Monarch 110 | 8 / 2024-03-01-to-2024-03-07 | 976,207 | South Korea | 97,735 | 10.01% | 1.63% | 108,397 |
| Monarch 110 | 9 / 2024-03-08-to-2024-03-14 | 1,049,700 | Japan | 14,675 | 1.40% | 26.14% | 16,276 |
| Monarch 110 | 9 / 2024-03-08-to-2024-03-14 | 1,049,700 | USA | 70,700 | 6.74% | 1.94% | 78,413 |
| Monarch 110 | 9 / 2024-03-08-to-2024-03-14 | 1,049,700 | China | 54,854 | 5.23% | 1.57% | 60,838 |
| Monarch 110 | 9 / 2024-03-08-to-2024-03-14 | 1,049,700 | South Korea | 99,574 | 9.49% | 1.60% | 110,437 |
| Monarch 110 | 10 / 2024-03-15-to-2024-03-21 | 1,086,587 | Japan | 16,354 | 1.51% | 26.48% | 18,138 |
| Monarch 110 | 10 / 2024-03-15-to-2024-03-21 | 1,086,587 | USA | 69,685 | 6.41% | 1.96% | 77,287 |
| Monarch 110 | 10 / 2024-03-15-to-2024-03-21 | 1,086,587 | China | 58,622 | 5.40% | 1.46% | 65,017 |
| Monarch 110 | 10 / 2024-03-15-to-2024-03-21 | 1,086,587 | South Korea | 111,250 | 10.24% | 1.66% | 123,386 |
| Monarch 110 | 11 / 2024-03-22-to-2024-03-28 | 964,965 | Japan | 16,367 | 1.70% | 26.46% | 18,152 |
| Monarch 110 | 11 / 2024-03-22-to-2024-03-28 | 964,965 | USA | 64,844 | 6.72% | 2.00% | 71,918 |
| Monarch 110 | 11 / 2024-03-22-to-2024-03-28 | 964,965 | China | 57,274 | 5.94% | 1.27% | 63,522 |
| Monarch 110 | 11 / 2024-03-22-to-2024-03-28 | 964,965 | South Korea | 110,465 | 11.45% | 1.65% | 122,516 |
| Monarch 110 | 12 / 2024-03-29-to-2024-04-04 | 698,930 | Japan | 7,133 | 1.02% | 25.91% | 7,911 |
| Monarch 110 | 12 / 2024-03-29-to-2024-04-04 | 698,930 | USA | 44,386 | 6.35% | 1.86% | 49,228 |
| Monarch 110 | 12 / 2024-03-29-to-2024-04-04 | 698,930 | China | 26,256 | 3.76% | 1.87% | 29,120 |
| Monarch 110 | 12 / 2024-03-29-to-2024-04-04 | 698,930 | South Korea | 44,152 | 6.32% | 1.70% | 48,969 |
| Monarch 110 | 13 / 2024-04-05-to-2024-04-11 | 754,537 | Japan | 7,519 | 1.00% | 26.41% | 8,339 |
| Monarch 110 | 13 / 2024-04-05-to-2024-04-11 | 754,537 | USA | 44,674 | 5.92% | 2.22% | 49,548 |
| Monarch 110 | 13 / 2024-04-05-to-2024-04-11 | 754,537 | China | 25,364 | 3.36% | 1.70% | 28,131 |
| Monarch 110 | 13 / 2024-04-05-to-2024-04-11 | 754,537 | South Korea | 44,306 | 5.87% | 1.72% | 49,139 |
| Monarch 110 | 14 / 2024-04-12-to-2024-04-18 | 825,293 | Japan | 11,929 | 1.45% | 25.80% | 13,230 |
| Monarch 110 | 14 / 2024-04-12-to-2024-04-18 | 825,293 | USA | 51,080 | 6.19% | 1.98% | 56,652 |
| Monarch 110 | 14 / 2024-04-12-to-2024-04-18 | 825,293 | China | 36,904 | 4.47% | 1.67% | 40,930 |
| Monarch 110 | 14 / 2024-04-12-to-2024-04-18 | 825,293 | South Korea | 67,496 | 8.18% | 1.73% | 74,859 |
| Monarch 110 | 15 / 2024-04-19-to-2024-04-25 | 617,210 | Japan | 5,677 | 0.92% | 26.42% | 6,296 |
| Monarch 110 | 15 / 2024-04-19-to-2024-04-25 | 617,210 | USA | 44,079 | 7.14% | 1.51% | 48,888 |
| Monarch 110 | 15 / 2024-04-19-to-2024-04-25 | 617,210 | China | 18,243 | 2.96% | 2.18% | 20,233 |
| Monarch 110 | 15 / 2024-04-19-to-2024-04-25 | 617,210 | South Korea | 31,289 | 5.07% | 1.76% | 34,702 |
| Monarch 201 | 1 / 2026-02-27-to-2026-03-05-partial | 1,001,446 | Japan | 8,633 | 0.86% | 23.09% | 8,633 |
| Monarch 201 | 1 / 2026-02-27-to-2026-03-05-partial | 1,001,446 | USA | 104,050 | 10.39% | 6.79% | 104,050 |
| Monarch 201 | 1 / 2026-02-27-to-2026-03-05-partial | 1,001,446 | China | 71,161 | 7.11% | 1.80% | 71,161 |
| Monarch 201 | 1 / 2026-02-27-to-2026-03-05-partial | 1,001,446 | South Korea | 77,525 | 7.74% | 1.89% | 77,525 |
| Monarch 201 | 2 / 2026-03-06-to-2026-03-12 | 2,041,057 | Japan | 24,188 | 1.19% | 24.79% | 24,188 |
| Monarch 201 | 2 / 2026-03-06-to-2026-03-12 | 2,041,057 | USA | 188,199 | 9.22% | 4.56% | 188,199 |
| Monarch 201 | 2 / 2026-03-06-to-2026-03-12 | 2,041,057 | China | 183,860 | 9.01% | 1.20% | 183,860 |
| Monarch 201 | 2 / 2026-03-06-to-2026-03-12 | 2,041,057 | South Korea | 236,707 | 11.60% | 1.67% | 236,707 |
| Monarch 201 | 3 / 2026-03-13-to-2026-03-19 | 3,258,870 | Japan | 42,114 | 1.29% | 25.30% | 42,114 |
| Monarch 201 | 3 / 2026-03-13-to-2026-03-19 | 3,258,870 | USA | 272,075 | 8.35% | 4.30% | 272,075 |
| Monarch 201 | 3 / 2026-03-13-to-2026-03-19 | 3,258,870 | China | 324,536 | 9.96% | 1.17% | 324,536 |
| Monarch 201 | 3 / 2026-03-13-to-2026-03-19 | 3,258,870 | South Korea | 438,906 | 13.47% | 1.56% | 438,906 |
| Monarch 201 | 4 / 2026-03-20-to-2026-03-26 | 3,256,370 | Japan | 45,048 | 1.38% | 26.03% | 45,048 |
| Monarch 201 | 4 / 2026-03-20-to-2026-03-26 | 3,256,370 | USA | 238,419 | 7.32% | 3.34% | 238,419 |
| Monarch 201 | 4 / 2026-03-20-to-2026-03-26 | 3,256,370 | China | 340,273 | 10.45% | 1.08% | 340,273 |
| Monarch 201 | 4 / 2026-03-20-to-2026-03-26 | 3,256,370 | South Korea | 461,575 | 14.17% | 1.56% | 461,575 |
| Monarch 201 | 5 / 2026-03-27-to-2026-04-02 | 3,268,119 | Japan | 48,823 | 1.49% | 26.17% | 48,823 |
| Monarch 201 | 5 / 2026-03-27-to-2026-04-02 | 3,268,119 | USA | 235,668 | 7.21% | 3.07% | 235,668 |
| Monarch 201 | 5 / 2026-03-27-to-2026-04-02 | 3,268,119 | China | 376,637 | 11.52% | 0.96% | 376,637 |
| Monarch 201 | 5 / 2026-03-27-to-2026-04-02 | 3,268,119 | South Korea | 505,872 | 15.48% | 1.58% | 505,872 |
| Monarch 201 | 6 / 2026-04-03-to-2026-04-09 | 3,195,382 | Japan | 46,199 | 1.45% | 25.73% | 46,199 |
| Monarch 201 | 6 / 2026-04-03-to-2026-04-09 | 3,195,382 | USA | 243,287 | 7.61% | 2.72% | 243,287 |
| Monarch 201 | 6 / 2026-04-03-to-2026-04-09 | 3,195,382 | China | 361,463 | 11.31% | 0.95% | 361,463 |
| Monarch 201 | 6 / 2026-04-03-to-2026-04-09 | 3,195,382 | South Korea | 471,933 | 14.77% | 1.56% | 471,933 |
| Monarch 201 | 7 / 2026-04-10-to-2026-04-16 | 2,930,468 | Japan | 37,715 | 1.29% | 25.26% | 37,715 |
| Monarch 201 | 7 / 2026-04-10-to-2026-04-16 | 2,930,468 | USA | 195,062 | 6.66% | 2.74% | 195,062 |
| Monarch 201 | 7 / 2026-04-10-to-2026-04-16 | 2,930,468 | China | 296,830 | 10.13% | 0.99% | 296,830 |
| Monarch 201 | 7 / 2026-04-10-to-2026-04-16 | 2,930,468 | South Korea | 389,309 | 13.28% | 1.58% | 389,309 |
| Monarch 201 | 8 / 2026-04-17-to-2026-04-23 | 2,721,049 | Japan | 27,444 | 1.01% | 24.91% | 27,444 |
| Monarch 201 | 8 / 2026-04-17-to-2026-04-23 | 2,721,049 | USA | 171,025 | 6.29% | 2.86% | 171,025 |
| Monarch 201 | 8 / 2026-04-17-to-2026-04-23 | 2,721,049 | China | 243,456 | 8.95% | 1.00% | 243,456 |
| Monarch 201 | 8 / 2026-04-17-to-2026-04-23 | 2,721,049 | South Korea | 276,897 | 10.18% | 1.53% | 276,897 |
| Monarch 201 | 9 / 2026-04-24-to-2026-04-30 | 2,657,822 | Japan | 30,636 | 1.15% | 25.14% | 30,636 |
| Monarch 201 | 9 / 2026-04-24-to-2026-04-30 | 2,657,822 | USA | 177,611 | 6.68% | 2.78% | 177,611 |
| Monarch 201 | 9 / 2026-04-24-to-2026-04-30 | 2,657,822 | China | 262,966 | 9.89% | 0.93% | 262,966 |
| Monarch 201 | 9 / 2026-04-24-to-2026-04-30 | 2,657,822 | South Korea | 299,956 | 11.29% | 1.58% | 299,956 |
| Monarch 201 | 10 / 2026-05-01-to-2026-05-07 | 2,669,260 | Japan | 33,892 | 1.27% | 25.60% | 33,892 |
| Monarch 201 | 10 / 2026-05-01-to-2026-05-07 | 2,669,260 | USA | 180,566 | 6.76% | 2.72% | 180,566 |
| Monarch 201 | 10 / 2026-05-01-to-2026-05-07 | 2,669,260 | China | 283,427 | 10.62% | 0.91% | 283,427 |
| Monarch 201 | 10 / 2026-05-01-to-2026-05-07 | 2,669,260 | South Korea | 363,399 | 13.61% | 1.58% | 363,399 |
| Monarch 201 | 11 / 2026-05-08-to-2026-05-14 | 2,637,489 | Japan | 30,163 | 1.14% | 25.65% | 30,163 |
| Monarch 201 | 11 / 2026-05-08-to-2026-05-14 | 2,637,489 | USA | 173,521 | 6.58% | 2.56% | 173,521 |
| Monarch 201 | 11 / 2026-05-08-to-2026-05-14 | 2,637,489 | China | 274,134 | 10.39% | 0.89% | 274,134 |
| Monarch 201 | 11 / 2026-05-08-to-2026-05-14 | 2,637,489 | South Korea | 347,853 | 13.19% | 1.55% | 347,853 |
| Monarch 201 | 12 / 2026-05-15-to-2026-05-21 | 2,971,070 | Japan | 39,409 | 1.33% | 26.20% | 39,409 |
| Monarch 201 | 12 / 2026-05-15-to-2026-05-21 | 2,971,070 | USA | 203,575 | 6.85% | 2.53% | 203,575 |
| Monarch 201 | 12 / 2026-05-15-to-2026-05-21 | 2,971,070 | China | 315,057 | 10.60% | 0.87% | 315,057 |
| Monarch 201 | 12 / 2026-05-15-to-2026-05-21 | 2,971,070 | South Korea | 452,172 | 15.22% | 1.53% | 452,172 |
| Monarch 201 | 13 / 2026-05-22-to-2026-05-28 | 2,987,881 | Japan | 37,444 | 1.25% | 25.63% | 37,444 |
| Monarch 201 | 13 / 2026-05-22-to-2026-05-28 | 2,987,881 | USA | 200,195 | 6.70% | 2.47% | 200,195 |
| Monarch 201 | 13 / 2026-05-22-to-2026-05-28 | 2,987,881 | China | 297,784 | 9.97% | 0.89% | 297,784 |
| Monarch 201 | 13 / 2026-05-22-to-2026-05-28 | 2,987,881 | South Korea | 444,315 | 14.87% | 1.58% | 444,315 |
| Monarch 201 | 14 / 2026-05-29-to-2026-06-04 | 2,896,155 | Japan | 37,564 | 1.30% | 26.34% | 37,564 |
| Monarch 201 | 14 / 2026-05-29-to-2026-06-04 | 2,896,155 | USA | 188,035 | 6.49% | 2.47% | 188,035 |
| Monarch 201 | 14 / 2026-05-29-to-2026-06-04 | 2,896,155 | China | 287,815 | 9.94% | 0.93% | 287,815 |
| Monarch 201 | 14 / 2026-05-29-to-2026-06-04 | 2,896,155 | South Korea | 446,945 | 15.43% | 1.59% | 446,945 |
| Monarch 201 | 15 / 2026-06-05-to-2026-06-11 | 2,322,119 | Japan | 22,239 | 0.96% | 25.38% | 22,239 |
| Monarch 201 | 15 / 2026-06-05-to-2026-06-11 | 2,322,119 | USA | 137,163 | 5.91% | 2.33% | 137,163 |
| Monarch 201 | 15 / 2026-06-05-to-2026-06-11 | 2,322,119 | China | 180,898 | 7.79% | 1.04% | 180,898 |
| Monarch 201 | 15 / 2026-06-05-to-2026-06-11 | 2,322,119 | South Korea | 254,564 | 10.96% | 1.63% | 254,564 |
| Monarch 208 | 1 / 2026-04-17-to-2026-04-23 | 1,038,427 | Japan | 9,189 | 0.88% | 23.76% | 9,189 |
| Monarch 208 | 1 / 2026-04-17-to-2026-04-23 | 1,038,427 | USA | 83,501 | 8.04% | 4.41% | 83,501 |
| Monarch 208 | 1 / 2026-04-17-to-2026-04-23 | 1,038,427 | China | 94,523 | 9.10% | 1.52% | 94,523 |
| Monarch 208 | 1 / 2026-04-17-to-2026-04-23 | 1,038,427 | South Korea | 86,354 | 8.32% | 1.65% | 86,354 |
| Monarch 208 | 2 / 2026-04-24-to-2026-04-30 | 2,096,935 | Japan | 22,215 | 1.06% | 24.39% | 22,215 |
| Monarch 208 | 2 / 2026-04-24-to-2026-04-30 | 2,096,935 | USA | 166,535 | 7.94% | 4.25% | 166,535 |
| Monarch 208 | 2 / 2026-04-24-to-2026-04-30 | 2,096,935 | China | 210,438 | 10.04% | 1.05% | 210,438 |
| Monarch 208 | 2 / 2026-04-24-to-2026-04-30 | 2,096,935 | South Korea | 203,578 | 9.71% | 1.59% | 203,578 |
| Monarch 208 | 3 / 2026-05-01-to-2026-05-07 | 3,332,160 | Japan | 39,444 | 1.18% | 24.66% | 39,444 |
| Monarch 208 | 3 / 2026-05-01-to-2026-05-07 | 3,332,160 | USA | 262,797 | 7.89% | 4.13% | 262,797 |
| Monarch 208 | 3 / 2026-05-01-to-2026-05-07 | 3,332,160 | China | 348,843 | 10.47% | 1.24% | 348,843 |
| Monarch 208 | 3 / 2026-05-01-to-2026-05-07 | 3,332,160 | South Korea | 397,626 | 11.93% | 1.56% | 397,626 |
| Monarch 208 | 4 / 2026-05-08-to-2026-05-14 | 3,290,355 | Japan | 37,165 | 1.13% | 24.82% | 37,165 |
| Monarch 208 | 4 / 2026-05-08-to-2026-05-14 | 3,290,355 | USA | 227,566 | 6.92% | 2.90% | 227,566 |
| Monarch 208 | 4 / 2026-05-08-to-2026-05-14 | 3,290,355 | China | 341,101 | 10.37% | 0.96% | 341,101 |
| Monarch 208 | 4 / 2026-05-08-to-2026-05-14 | 3,290,355 | South Korea | 418,958 | 12.73% | 1.62% | 418,958 |
| Monarch 208 | 5 / 2026-05-15-to-2026-05-21 | 3,604,967 | Japan | 48,735 | 1.35% | 25.22% | 48,735 |
| Monarch 208 | 5 / 2026-05-15-to-2026-05-21 | 3,604,967 | USA | 253,690 | 7.04% | 2.56% | 253,690 |
| Monarch 208 | 5 / 2026-05-15-to-2026-05-21 | 3,604,967 | China | 388,404 | 10.77% | 0.86% | 388,404 |
| Monarch 208 | 5 / 2026-05-15-to-2026-05-21 | 3,604,967 | South Korea | 543,604 | 15.08% | 1.59% | 543,604 |
| Monarch 208 | 6 / 2026-05-22-to-2026-05-28 | 3,492,352 | Japan | 45,620 | 1.31% | 25.56% | 45,620 |
| Monarch 208 | 6 / 2026-05-22-to-2026-05-28 | 3,492,352 | USA | 239,764 | 6.87% | 2.47% | 239,764 |
| Monarch 208 | 6 / 2026-05-22-to-2026-05-28 | 3,492,352 | China | 350,437 | 10.03% | 0.90% | 350,437 |
| Monarch 208 | 6 / 2026-05-22-to-2026-05-28 | 3,492,352 | South Korea | 520,285 | 14.90% | 1.60% | 520,285 |
| Monarch 208 | 7 / 2026-05-29-to-2026-06-04 | 3,459,436 | Japan | 46,151 | 1.33% | 25.46% | 46,151 |
| Monarch 208 | 7 / 2026-05-29-to-2026-06-04 | 3,459,436 | USA | 229,088 | 6.62% | 2.52% | 229,088 |
| Monarch 208 | 7 / 2026-05-29-to-2026-06-04 | 3,459,436 | China | 348,009 | 10.06% | 0.93% | 348,009 |
| Monarch 208 | 7 / 2026-05-29-to-2026-06-04 | 3,459,436 | South Korea | 539,781 | 15.60% | 1.58% | 539,781 |
| Monarch 208 | 8 / 2026-06-05-to-2026-06-11 | 2,802,551 | Japan | 27,135 | 0.97% | 24.85% | 27,135 |
| Monarch 208 | 8 / 2026-06-05-to-2026-06-11 | 2,802,551 | USA | 165,584 | 5.91% | 2.33% | 165,584 |
| Monarch 208 | 8 / 2026-06-05-to-2026-06-11 | 2,802,551 | China | 223,743 | 7.98% | 0.95% | 223,743 |
| Monarch 208 | 8 / 2026-06-05-to-2026-06-11 | 2,802,551 | South Korea | 301,757 | 10.77% | 1.62% | 301,757 |
| Monarch 208 | 9 / 2026-06-12-to-2026-06-18 | 3,535,030 | Japan | 48,211 | 1.36% | 25.62% | 48,211 |
| Monarch 208 | 9 / 2026-06-12-to-2026-06-18 | 3,535,030 | USA | 240,933 | 6.82% | 2.34% | 240,933 |
| Monarch 208 | 9 / 2026-06-12-to-2026-06-18 | 3,535,030 | China | 379,850 | 10.75% | 0.96% | 379,850 |
| Monarch 208 | 9 / 2026-06-12-to-2026-06-18 | 3,535,030 | South Korea | 569,645 | 16.11% | 1.57% | 569,645 |
| Monarch 208 | 10 / 2026-06-19-to-2026-06-25 | 3,727,102 | Japan | 51,270 | 1.38% | 25.78% | 51,270 |
| Monarch 208 | 10 / 2026-06-19-to-2026-06-25 | 3,727,102 | USA | 242,988 | 6.52% | 2.52% | 242,988 |
| Monarch 208 | 10 / 2026-06-19-to-2026-06-25 | 3,727,102 | China | 406,621 | 10.91% | 0.95% | 406,621 |
| Monarch 208 | 10 / 2026-06-19-to-2026-06-25 | 3,727,102 | South Korea | 624,688 | 16.76% | 1.59% | 624,688 |
| Monarch 208 | 11 / 2026-06-26-to-2026-07-02-partial | 2,713,044 | Japan | 38,550 | 1.42% | 26.58% | 38,550 |
| Monarch 208 | 11 / 2026-06-26-to-2026-07-02-partial | 2,713,044 | USA | 185,305 | 6.83% | 2.56% | 185,305 |
| Monarch 208 | 11 / 2026-06-26-to-2026-07-02-partial | 2,713,044 | China | 311,164 | 11.47% | 0.95% | 311,164 |
| Monarch 208 | 11 / 2026-06-26-to-2026-07-02-partial | 2,713,044 | South Korea | 467,851 | 17.24% | 1.65% | 467,851 |
| Monarch 208 | 12 / 2026-07-03-to-2026-07-09 | 3,313,235 | Japan | 46,977 | 1.42% | 25.72% | 46,977 |
| Monarch 208 | 12 / 2026-07-03-to-2026-07-09 | 3,313,235 | USA | 220,638 | 6.66% | 2.52% | 220,638 |
| Monarch 208 | 12 / 2026-07-03-to-2026-07-09 | 3,313,235 | China | 366,573 | 11.06% | 0.88% | 366,573 |
| Monarch 208 | 12 / 2026-07-03-to-2026-07-09 | 3,313,235 | South Korea | 574,851 | 17.35% | 1.61% | 574,851 |
| Monarch 208 | 13 / 2026-07-10-to-2026-07-16 | 3,463,704 | Japan | 46,252 | 1.34% | 26.32% | 46,252 |
| Monarch 208 | 13 / 2026-07-10-to-2026-07-16 | 3,463,704 | USA | 231,562 | 6.69% | 2.52% | 231,562 |
| Monarch 208 | 13 / 2026-07-10-to-2026-07-16 | 3,463,704 | China | 374,105 | 10.80% | 0.89% | 374,105 |
| Monarch 208 | 13 / 2026-07-10-to-2026-07-16 | 3,463,704 | South Korea | 556,454 | 16.07% | 1.57% | 556,454 |
| Monarch 208 | 14 / 2026-07-17-to-2026-07-23 | 3,270,114 | Japan | 39,134 | 1.20% | 25.85% | 39,134 |
| Monarch 208 | 14 / 2026-07-17-to-2026-07-23 | 3,270,114 | USA | 210,909 | 6.45% | 2.49% | 210,909 |
| Monarch 208 | 14 / 2026-07-17-to-2026-07-23 | 3,270,114 | China | 336,585 | 10.29% | 0.95% | 336,585 |
| Monarch 208 | 14 / 2026-07-17-to-2026-07-23 | 3,270,114 | South Korea | 496,249 | 15.18% | 1.53% | 496,249 |
| Monarch 208 | 15 / 2026-07-24-to-2026-07-30 | 3,222,549 | Japan | 34,914 | 1.08% | 26.23% | 34,914 |
| Monarch 208 | 15 / 2026-07-24-to-2026-07-30 | 3,222,549 | USA | 205,339 | 6.37% | 2.58% | 205,339 |
| Monarch 208 | 15 / 2026-07-24-to-2026-07-30 | 3,222,549 | China | 311,407 | 9.66% | 0.92% | 311,407 |
| Monarch 208 | 15 / 2026-07-24-to-2026-07-30 | 3,222,549 | South Korea | 413,485 | 12.83% | 1.57% | 413,485 |


</details>

## Map projection and country outlines

The city-difference panels use **Cartofreako's native Cahill–Keyes projection**,
with its one-degree longitude registration, and **Izzi** for the vector SVG.
Each country's complete projected outline and selected city coordinates are
uniformly fitted into its panel, preserving projected proportions. Panel scales
therefore differ by country; geographic area is not comparable between panels.
City values still use the same world denominators and color scale across maps.

Natural Earth v5.1.2 1:10m country polygons have intersecting lake and reservoir
water removed. Interior rings are retained with even-odd filling, and country
polygons are split at the registered octant seams before projection. This keeps
Great Lakes shorelines visible and avoids lines bridging projection cuts.
Boundaries follow Natural Earth's de facto geometry. The six Pitt resolution
plates use this same vector geometry, with their original weekly by-BTIH input
method and one shared circle-area scale across countries.

References: [Cartofreako Cahill–Keyes geometry and octants](https://bdekoz.github.io/cartofreako/docs/pages/projections/cahill-keyes/context.html),
[Izzi](https://github.com/bdekoz/izzi), and the
[country and lake geometry with source hashes](../data/mellon-7.6-map-boundaries.json).

## Methods and limits

- **Units:** sum `downloaders.size` or `uploaders.size` in the top-level
  `features` array of each weekly aggregate GeoJSON. Summing the selected intervals
  produces repeated swarm weights across weeks and torrents, not unique people,
  unique addresses over the full window, or completed views. The nested
  `collection_week_by_btiha` is not added again.
- **Window:** weeks 1–15 inclusive, including the opening bin. Every selected
  interval spans seven calendar days within the actual sample cutoff. Some bins
  carry a `-partial` member-coverage flag or overlap an audit gap; the sensitivity
  excludes those elapsed-week indices from every object. Calendar dates differ.
  Matching elapsed weeks does not match release conditions or hourly coverage.
- **Shares:** country or city downloader weight divided by worldwide downloader
  weight over the same intervals, including unclassified-country features.
  Pooled shares use sums of counts, not the unweighted mean of weekly percentages.
  Uploader shares have a separate uploader denominator.
- **Flags:** mobile, hosting and VPN rates divide the country's flagged weight by
  that country's size for the same role. Flags overlap. A mobile flag describes
  IP network classification, not a device, connection technology, citizenship,
  residence or verified audience. Wi-Fi versus cellular usage is not resolved.
- **Hosting sensitivity:** subtract hosting from size in both country and global
  denominators. This removes one flag; it does not identify residential traffic.
- **Difference maps:** geolocated city aggregates keyed by country and GeoNames ID, using
  source representative coordinates. Only shared identified cities with at least
  100 combined downloader weight qualify. Show at most two positive and two
  negative differences per country, ranked by percentage-point difference.
  An absent or suppressed location is not zero. Triangles indicate sign;
  color intensity encodes magnitude on a symmetric scale shared by all difference maps on this page.
  “Hot” and “cold” describe larger and smaller observed shares, without a test of
  statistical significance. They do not describe population-adjusted demand.
- **Export:** all selected files declare H3 resolution 5 and minimum swarm size 3.
  Geographic filtering and aggregation mean these denominators differ from
  companion JSON unique-BTIH totals. Do not interpret the discrepancy as a known
  missing-data percentage. Weekly JSON `collection_week` values are cumulative
  prefixes; the geographic interval series used here is a different product.


## References and reproduction

- [Weekly graph series and native Izzi renderer provenance](../data/mellon-7.6-weekly-graphs.json). All weekly lines use Izzi `make_line_graph` and its native marker API; download the [C++ renderer](../resources/izzi-weekly-graphs.cc) and [Python wrapper](../resources/izzi_weekly_graphs.py).
- [Calculation ledger: every interval, country, network field, city and source SHA-256](../data/mellon-7.6-analysis.json). All ten flags for both roles are retained.
- [Godzilla Minus One: godzilla-minus-one-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/data/json/godzilla-minus-one-cumulative.json).
- [Godzilla Minus One: godzilla-minus-one-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/docs/itemized/godzilla-minus-one-sample-cache-audit.md).
- [Godzilla Minus One: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/data/geojson.week/godzilla-minus-one-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Godzilla x Kong: godzilla-x-kong-the-new-empire-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/data/json/godzilla-x-kong-the-new-empire-cumulative.json).
- [Godzilla x Kong: godzilla-x-kong-the-new-empire-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/docs/itemized/godzilla-x-kong-the-new-empire-sample-cache-audit.md).
- [Godzilla x Kong: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/data/geojson.week/godzilla-x-kong-the-new-empire-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Godzilla vs. Kong: godzilla-vs-kong-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2021/blob/95af5fee975b04b25bad7f03aa5e1d571a939437/data/json/godzilla-vs-kong-cumulative.json).
- [Godzilla vs. Kong: godzilla-vs-kong-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2021/blob/95af5fee975b04b25bad7f03aa5e1d571a939437/docs/itemized/godzilla-vs-kong-sample-cache-audit.md).
- [Godzilla vs. Kong: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2021/blob/95af5fee975b04b25bad7f03aa5e1d571a939437/data/geojson.week/godzilla-vs-kong-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Monarch 101: monarch-legacy-of-monsters-101-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2023/blob/188eac9b11645cc48caa174c7785c554bf972402/data/json/monarch-legacy-of-monsters-101-cumulative.json).
- [Monarch 101: monarch-legacy-of-monsters-101-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2023/blob/188eac9b11645cc48caa174c7785c554bf972402/docs/itemized/monarch-legacy-of-monsters-101-sample-cache-audit.md).
- [Monarch 101: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2023/blob/188eac9b11645cc48caa174c7785c554bf972402/data/geojson.week/monarch-legacy-of-monsters-101-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Monarch 110: monarch-legacy-of-monsters-110-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/data/json/monarch-legacy-of-monsters-110-cumulative.json).
- [Monarch 110: monarch-legacy-of-monsters-110-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/docs/itemized/monarch-legacy-of-monsters-110-sample-cache-audit.md).
- [Monarch 110: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2024/blob/92a3c99741588412cbc26644d1e3879b1d97740f/data/geojson.week/monarch-legacy-of-monsters-110-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Monarch 201: monarch-legacy-of-monsters-201-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2026/blob/834a62f1dda3071906190c64caef241282d90bff/data/json/monarch-legacy-of-monsters-201-cumulative.json).
- [Monarch 201: monarch-legacy-of-monsters-201-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2026/blob/834a62f1dda3071906190c64caef241282d90bff/docs/itemized/monarch-legacy-of-monsters-201-sample-cache-audit.md).
- [Monarch 201: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2026/blob/834a62f1dda3071906190c64caef241282d90bff/data/geojson.week/monarch-legacy-of-monsters-201-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Monarch 208: monarch-legacy-of-monsters-208-cumulative.json](https://github.com/alpha60-devops/alpha60-results-2026/blob/834a62f1dda3071906190c64caef241282d90bff/data/json/monarch-legacy-of-monsters-208-cumulative.json).
- [Monarch 208: monarch-legacy-of-monsters-208-sample-cache-audit.md](https://github.com/alpha60-devops/alpha60-results-2026/blob/834a62f1dda3071906190c64caef241282d90bff/docs/itemized/monarch-legacy-of-monsters-208-sample-cache-audit.md).
- [Monarch 208: first analyzed weekly GeoJSON](https://github.com/alpha60-devops/alpha60-results-2026/blob/834a62f1dda3071906190c64caef241282d90bff/data/geojson.week/monarch-legacy-of-monsters-208-week-00001.geojson.gz); matched and extended interval filenames and hashes are in the ledger. Companion export version `2026-08-05`; IP-geolocation version `6:1777968300`.
- [Native projection source](https://github.com/bdekoz/cartofreako/blob/ec201801a0386fc681c7637e26a838117ecf23de/src.projections/cart0freak0-cahill-keyes.h); SHA-256 `0c3b945711e655d4dd70208457bca2f400fd6edc0869f1a1c87ad57847f56ba2`. Natural Earth data are public domain; [country and lake geometry with upstream hashes](../data/mellon-7.6-map-boundaries.json).
- [Download the analysis script](../resources/mellon-7.6-analyze.py) and [ITU configuration](../data/mellon-7.6-itu-2026.json). Run with `--source-root /path/to/checkouts --output /path/to/output --itu-config /path/to/mellon-7.6-itu-2026.json`, with the annual repositories checked out at the ledger commits. It emits JSON only. Then run the [extension script](../resources/mellon-7.6-extend.py) in the same directory as the analysis script with `--source-root /path/to/checkouts --ledger /path/to/output/analysis.json` to add extended intervals and by-BTIH resolution weights. [Figure and validation scripts (repository access required)](https://github.com/bdekoz/alpha60/tree/main/scripts): `render-mellon-7-6-aapi.py` and `check-mellon-7-6-aapi.py`.
- [Toho's official Minus One announcement](https://godzilla.com/blogs/news/new-godzilla-minus-one-trailer-movie-tickets): identifies the film and director Takashi Yamazaki.
- [Legendary: Godzilla vs. Kong](https://www.legendary.com/film/godzilla-vs-kong/) and [Godzilla x Kong: The New Empire](https://www.legendary.com/film/godzilla-x-kong-the-new-empire/): official film records and Warner Bros. distribution credits.
- [Legendary and Warner Bros. franchise announcement](https://www.legendary.com/legendary-and-warner-bros-pictures-announce-cinematic-franchise-uniting-godzilla-king-kong-and-other-iconic-giant-monsters/): describes Legendary's Godzilla/Kong films and collaboration with Toho. The requested production contrast does not imply that the U.S. films have no Toho involvement.
